import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from investor_db.io import Dataset, Row
from investor_db.schema import (
    CATEGORY_VC,
    AMOUNT_INVESTED_PERIOD,
    AMOUNT_TARGET,
    APPROX_YES,
    FACT_FUND_COUNT,
    AMOUNT_LP_COMMITMENT,
    FUND_AMOUNT_TYPES,
    FUNDRAISING_OPEN,
    INVESTED_AMOUNT_TYPES,
    LOWER_BOUND_AMOUNT_TYPES,
    RAISED_AMOUNT_PRIORITY,
    SEARCH_TARGET_CAPITAL,
    SEARCH_TARGET_TICKET,
    SEARCH_TARGETS,
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    EXCLUSION_DUPLICATE,
    FRESHNESS_WINDOW_DAYS,
    INVESTOR_COLUMNS,
    MONEY_FIELDS,
    REVIEWER_INDEPENDENT,
    REVIEWER_PRIMARY,
    REVIEW_ROUND_SAMPLE,
    STATUS_CANDIDATE,
    STATUS_VERIFIED,
    VERDICT_FACT_CORRECT,
    VERDICT_FACT_UNVERIFIABLE,
    VERDICT_FACT_WRONG,
    VERDICT_FALSE_POSITIVE,
    VERDICT_TRUE_POSITIVE,
    VERDICT_UNSURE,
)
from investor_db.validation import (
    find_duplicate_groups,
    group_facts_by_investor,
    has_primary_registry_fact,
    has_recent_investment,
    is_primary_source,
)
from investor_db.values import parse_date, parse_minutes

COMPLETENESS_FIELDS = tuple(
    column for column in INVESTOR_COLUMNS if column not in ("investor_id", "verification_status", "exclusion_reason")
)


@dataclass(frozen=True)
class Proportion:
    numerator: int
    denominator: int

    @property
    def value(self) -> float | None:
        return self.numerator / self.denominator if self.denominator else None

    def wilson_interval(self, z: float = 1.96) -> tuple[float, float] | None:
        if not self.denominator:
            return None
        n = self.denominator
        p = self.numerator / n
        scale = 1 + z**2 / n
        centre = (p + z**2 / (2 * n)) / scale
        margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / scale
        return max(0.0, centre - margin), min(1.0, centre + margin)


@dataclass(frozen=True)
class PrecisionResult:
    true_positives: int
    false_positives: int
    unsure: int

    @property
    def strict(self) -> Proportion:
        return Proportion(self.true_positives, self.true_positives + self.false_positives)

    @property
    def pessimistic(self) -> Proportion:
        return Proportion(self.true_positives, self.true_positives + self.false_positives + self.unsure)


@dataclass(frozen=True)
class FactAccuracyResult:
    correct: int
    wrong: int
    unverifiable: int

    @property
    def accuracy(self) -> Proportion:
        return Proportion(self.correct, self.correct + self.wrong)


@dataclass(frozen=True)
class AgreementResult:
    agreement: Proportion
    kappa: float | None


def verified_investors(investors: list[Row]) -> list[Row]:
    return [row for row in investors if row["verification_status"] == STATUS_VERIFIED]


def verified_ids(investors: list[Row]) -> set[str]:
    return {row["investor_id"] for row in verified_investors(investors)}


def category_investors(dataset: Dataset, category: str, statuses: tuple[str, ...] = (STATUS_VERIFIED,)) -> list[Row]:
    assessed = {
        row["investor_id"]
        for row in dataset.category_assessments
        if row["category"] == category and row["verification_status"] in statuses
    }
    return [row for row in dataset.investors if row["investor_id"] in assessed]


def eligible_for_precision(dataset: Dataset, category: str) -> set[str]:
    if category == CATEGORY_VC:
        return verified_ids(dataset.investors)
    return {row["investor_id"] for row in category_investors(dataset, category)}


def investor_verdicts(dataset: Dataset, reviewer: str, category: str = CATEGORY_VC) -> dict[str, str]:
    eligible = eligible_for_precision(dataset, category)
    return {
        row["investor_id"]: row["verdict"]
        for row in dataset.reviews
        if row["reviewer"] == reviewer and row["verdict"] and row["category"] == category and row["investor_id"] in eligible
    }


def precision(dataset: Dataset, reviewer: str = REVIEWER_PRIMARY, category: str = CATEGORY_VC) -> PrecisionResult:
    counts = Counter(investor_verdicts(dataset, reviewer, category).values())
    return PrecisionResult(counts[VERDICT_TRUE_POSITIVE], counts[VERDICT_FALSE_POSITIVE], counts[VERDICT_UNSURE])


def cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    n = len(pairs)
    observed = sum(first == second for first, second in pairs) / n
    first_counts = Counter(first for first, _ in pairs)
    second_counts = Counter(second for _, second in pairs)
    expected = sum(first_counts[label] * second_counts[label] for label in first_counts) / n**2
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)


def reviewer_agreement(dataset: Dataset) -> AgreementResult | None:
    primary = investor_verdicts(dataset, REVIEWER_PRIMARY)
    independent = investor_verdicts(dataset, REVIEWER_INDEPENDENT)
    common_ids = sorted(primary.keys() & independent.keys())
    if not common_ids:
        return None
    pairs = [(primary[investor_id], independent[investor_id]) for investor_id in common_ids]
    agreement = Proportion(sum(first == second for first, second in pairs), len(pairs))
    return AgreementResult(agreement, cohen_kappa(pairs))


def fact_accuracy(
    dataset: Dataset, reviewer: str = REVIEWER_PRIMARY, review_round: str = REVIEW_ROUND_SAMPLE
) -> FactAccuracyResult:
    fact_ids = {row["fact_id"] for row in dataset.facts}
    counts = Counter(
        row["verdict"]
        for row in dataset.fact_reviews
        if row["reviewer"] == reviewer
        and row["review_round"] == review_round
        and row["verdict"]
        and row["fact_id"] in fact_ids
    )
    return FactAccuracyResult(counts[VERDICT_FACT_CORRECT], counts[VERDICT_FACT_WRONG], counts[VERDICT_FACT_UNVERIFIABLE])


def field_completeness(investors: list[Row]) -> dict[str, Proportion]:
    verified = verified_investors(investors)
    return {
        column: Proportion(sum(bool(row[column]) for row in verified), len(verified))
        for column in COMPLETENESS_FIELDS
    }


def primary_registry_share(dataset: Dataset) -> Proportion:
    facts_by_investor = group_facts_by_investor(dataset.facts)
    sources_by_id = {row["source_id"]: row for row in dataset.sources}
    verified = verified_investors(dataset.investors)
    documented = sum(
        has_primary_registry_fact(row, facts_by_investor.get(row["investor_id"], []), sources_by_id)
        for row in verified
    )
    return Proportion(documented, len(verified))


def primary_fact_share(dataset: Dataset) -> Proportion:
    sources_by_id = {row["source_id"]: row for row in dataset.sources}
    primary = sum(is_primary_source(row["source_id"], sources_by_id) for row in dataset.facts)
    return Proportion(primary, len(dataset.facts))


def investment_activity_share(dataset: Dataset, today: date) -> Proportion:
    facts_by_investor = group_facts_by_investor(dataset.facts)
    verified = verified_investors(dataset.investors)
    active = sum(has_recent_investment(facts_by_investor.get(row["investor_id"], []), today) for row in verified)
    return Proportion(active, len(verified))


def freshness_share(investors: list[Row], today: date) -> Proportion:
    verified = verified_investors(investors)
    window_start = today - timedelta(days=FRESHNESS_WINDOW_DAYS)
    fresh = sum(
        (verified_at := parse_date(row["last_verified_at"])) is not None and verified_at >= window_start
        for row in verified
    )
    return Proportion(fresh, len(verified))


def excluded_duplicate_count(investors: list[Row]) -> int:
    return sum(row["exclusion_reason"] == EXCLUSION_DUPLICATE for row in investors)


def duplicate_group_count(investors: list[Row]) -> int:
    return len(find_duplicate_groups(investors))


def values_only_in_facts_due_to_currency(dataset: Dataset) -> int:
    investors_by_id = {row["investor_id"]: row for row in dataset.investors}
    return sum(
        1
        for fact in dataset.facts
        if fact["field"] in MONEY_FIELDS
        and (investor := investors_by_id.get(fact["investor_id"])) is not None
        and investor["currency"]
        and fact["currency"] != investor["currency"]
        and not investor[fact["field"]]
    )


def status_counts(investors: list[Row]) -> Counter[str]:
    return Counter(row["verification_status"] for row in investors)


def exclusion_reason_counts(investors: list[Row]) -> Counter[str]:
    return Counter(row["exclusion_reason"] for row in investors if row["exclusion_reason"])


@dataclass(frozen=True)
class EffortSummary:
    activity: str
    actor: str
    minutes_per_investor: tuple[Decimal, ...]

    @property
    def total_minutes(self) -> Decimal:
        return sum(self.minutes_per_investor)

    @property
    def mean_minutes(self) -> float:
        return statistics.mean(self.minutes_per_investor)

    @property
    def median_minutes(self) -> float:
        return statistics.median(self.minutes_per_investor)


def effort_summaries(effort_log: list[Row]) -> list[EffortSummary]:
    minutes: dict[tuple[str, str], dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    for row in effort_log:
        if (parsed := parse_minutes(row["minutes"])) is not None:
            minutes[(row["activity"], row["actor"])][row["investor_id"]] += parsed
    return [
        EffortSummary(activity, actor, tuple(sorted(per_investor.values())))
        for (activity, actor), per_investor in sorted(minutes.items())
    ]


def total_parsed_minutes(texts: list[str]) -> Decimal:
    return sum((parsed for text in texts if (parsed := parse_minutes(text)) is not None), Decimal(0))


def search_minutes(search_log: list[Row]) -> Decimal:
    return total_parsed_minutes([row["minutes"] for row in search_log])


@dataclass(frozen=True)
class PopulationEstimate:
    first_search_id: str
    second_search_id: str
    first_count: int
    second_count: int
    overlap: int

    @property
    def observed(self) -> int:
        return self.first_count + self.second_count - self.overlap

    @property
    def lincoln_petersen(self) -> float | None:
        if not self.overlap:
            return None
        return self.first_count * self.second_count / self.overlap

    @property
    def chapman(self) -> float:
        return (self.first_count + 1) * (self.second_count + 1) / (self.overlap + 1) - 1

    @property
    def chapman_variance(self) -> float:
        n1, n2, m = self.first_count, self.second_count, self.overlap
        return (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))

    def chapman_interval(self, z: float = 1.96) -> tuple[float, float]:
        margin = z * math.sqrt(self.chapman_variance)
        return max(float(self.observed), self.chapman - margin), self.chapman + margin


def ids_by_search(dataset: Dataset, eligible_ids: set[str]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = defaultdict(set)
    for row in dataset.candidate_sources:
        if row["investor_id"] in eligible_ids:
            found[row["search_id"]].add(row["investor_id"])
    return found


MIN_SEARCH_SIZE = 5


def population_estimates(
    dataset: Dataset, statuses: tuple[str, ...], min_search_size: int = MIN_SEARCH_SIZE
) -> list[PopulationEstimate]:
    eligible = {row["investor_id"] for row in dataset.investors if row["verification_status"] in statuses}
    found = ids_by_search(dataset, eligible)
    search_ids = sorted(search_id for search_id, ids in found.items() if len(ids) >= min_search_size)
    return [
        PopulationEstimate(first, second, len(found[first]), len(found[second]), len(found[first] & found[second]))
        for index, first in enumerate(search_ids)
        for second in search_ids[index + 1 :]
    ]


VERIFIED_POPULATION: tuple[str, ...] = (STATUS_VERIFIED,)
OPEN_POPULATION: tuple[str, ...] = (STATUS_VERIFIED, STATUS_CANDIDATE)


def processing_level(investor_id: str, activities_by_investor: dict[str, set[str]]) -> str:
    activities = activities_by_investor.get(investor_id, set())
    if EFFORT_VERIFICATION in activities:
        return EFFORT_VERIFICATION
    if EFFORT_TRIAGE in activities:
        return EFFORT_TRIAGE
    return ""


def funnel(dataset: Dataset) -> dict[str, Counter[str]]:
    activities_by_investor: dict[str, set[str]] = defaultdict(set)
    for row in dataset.effort_log:
        activities_by_investor[row["investor_id"]].add(row["activity"])
    stages: dict[str, Counter[str]] = defaultdict(Counter)
    for row in dataset.investors:
        stages[processing_level(row["investor_id"], activities_by_investor)][row["verification_status"]] += 1
    return dict(stages)


@dataclass(frozen=True)
class ReviewEffort:
    reviewer: str
    reviews: int
    timed_reviews: int
    total_minutes: Decimal


def review_efforts(rows: list[Row]) -> list[ReviewEffort]:
    completed = [row for row in rows if row["verdict"]]
    reviewers = sorted({row["reviewer"] for row in completed})
    return [
        ReviewEffort(
            reviewer,
            sum(row["reviewer"] == reviewer for row in completed),
            sum(row["reviewer"] == reviewer and parse_minutes(row["review_minutes"]) is not None for row in completed),
            total_parsed_minutes([row["review_minutes"] for row in completed if row["reviewer"] == reviewer]),
        )
        for reviewer in reviewers
    ]


CAPITAL_AUM = "assets_under_management"
CAPITAL_INVESTED = "invested_capital"
CAPITAL_KINDS = (*FUND_AMOUNT_TYPES, CAPITAL_AUM, CAPITAL_INVESTED)


def funds_by_investor(funds: list[Row]) -> dict[str, list[Row]]:
    grouped: dict[str, list[Row]] = defaultdict(list)
    for row in funds:
        grouped[row["investor_id"]].append(row)
    return grouped


def funds_by_name(funds: list[Row]) -> dict[str, list[Row]]:
    grouped: dict[str, list[Row]] = defaultdict(list)
    for row in funds:
        grouped[row["fund_name"]].append(row)
    return grouped


def best_raised_amount(rows: list[Row]) -> Row | None:
    raised = [row for row in rows if row["amount"] and row["amount_type"] in RAISED_AMOUNT_PRIORITY]
    return min(raised, key=lambda row: RAISED_AMOUNT_PRIORITY.index(row["amount_type"]), default=None)


def raised_fund_amounts(funds: list[Row]) -> list[Row]:
    return [row for row in map(best_raised_amount, funds_by_name(funds).values()) if row is not None]


def capital_kinds(investor: Row, funds: list[Row]) -> set[str]:
    kinds = {row["amount_type"] for row in funds if row["amount"]}
    kinds |= {column for column in (CAPITAL_AUM, CAPITAL_INVESTED) if investor[column]}
    return kinds


def has_capital(investor: Row, funds: list[Row]) -> bool:
    return bool(raised_fund_amounts(funds) or investor[CAPITAL_AUM])


def has_target_only(investor: Row, funds: list[Row]) -> bool:
    return not has_capital(investor, funds) and any(row["amount_type"] == AMOUNT_TARGET for row in funds)


def has_ticket(investor: Row) -> bool:
    return bool(investor["typical_ticket_min"] or investor["typical_ticket_max"])


def requirement_met(target: str, investor: Row, funds: list[Row]) -> bool:
    if target == SEARCH_TARGET_TICKET:
        return has_ticket(investor)
    if target == SEARCH_TARGET_CAPITAL:
        return has_capital(investor, funds)
    return bool(investor[target])


@dataclass(frozen=True)
class RequirementCompleteness:
    filled: dict[str, Proportion]
    searched_not_found: dict[str, int]
    tickets_both: Proportion
    capital_by_kind: dict[str, Proportion]
    target_only: Proportion
    sources: Proportion


def searched_targets(search_log: list[Row]) -> set[tuple[str, str]]:
    return {(row["investor_id"], row["target_field"]) for row in search_log if row["investor_id"]}


def requirement_completeness(dataset: Dataset, investors: list[Row] | None = None) -> RequirementCompleteness:
    verified = verified_investors(dataset.investors) if investors is None else investors
    funds = funds_by_investor(dataset.funds)
    searched = searched_targets(dataset.search_log)
    total = len(verified)
    filled: dict[str, Proportion] = {}
    not_found: dict[str, int] = {}
    for target in SEARCH_TARGETS:
        present = [requirement_met(target, row, funds.get(row["investor_id"], [])) for row in verified]
        filled[target] = Proportion(sum(present), total)
        not_found[target] = sum(
            not is_present and (row["investor_id"], target) in searched
            for row, is_present in zip(verified, present)
        )
    kinds = [capital_kinds(row, funds.get(row["investor_id"], [])) for row in verified]
    return RequirementCompleteness(
        filled=filled,
        searched_not_found=not_found,
        tickets_both=Proportion(
            sum(bool(row["typical_ticket_min"] and row["typical_ticket_max"]) for row in verified), total
        ),
        capital_by_kind={kind: Proportion(sum(kind in found for found in kinds), total) for kind in CAPITAL_KINDS},
        target_only=Proportion(
            sum(has_target_only(row, funds.get(row["investor_id"], [])) for row in verified), total
        ),
        sources=Proportion(sum(bool(row["evidence_urls"]) for row in verified), total),
    )


@dataclass(frozen=True)
class CapitalSummary:
    investor_id: str
    name: str
    raised: dict[str, Decimal]
    lower_bound: bool
    targets: dict[str, Decimal]
    invested: dict[str, Decimal]
    fund_count: int
    funds_with_raised: int
    lp_commitments: dict[str, Decimal]
    fundraising_open: tuple[str, ...]
    conflicts: tuple[str, ...]
    invested_fact_id: str
    invested_period_fact_ids: tuple[str, ...]
    documented_fund_count: int | None
    raised_types: tuple[str, ...]
    aum: str
    aum_currency: str


def sum_by_currency(amounts: list[tuple[str, str]]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for amount, currency in amounts:
        totals[currency] += Decimal(amount)
    return dict(sorted(totals.items()))


def amounts_of(rows: list[Row]) -> list[tuple[str, str]]:
    return [(row["amount"], row["currency"]) for row in rows]


def documented_fund_count(facts: list[Row]) -> int | None:
    counts = [row for row in facts if row["field"] == FACT_FUND_COUNT and row["value"].isdigit()]
    if not counts:
        return None
    latest = max(counts, key=lambda row: (row["value_as_of"], row["fact_id"]))
    return int(latest["value"])


def is_lower_bound_amount(fund: Row) -> bool:
    return fund["approx"] == APPROX_YES or fund["amount_type"] in LOWER_BOUND_AMOUNT_TYPES


def invested_capital_fact_id(facts: list[Row]) -> str:
    return next((row["fact_id"] for row in facts if row["field"] == CAPITAL_INVESTED), "")


def capital_summary(investor: Row, funds: list[Row], facts: list[Row]) -> CapitalSummary:
    raised = raised_fund_amounts(funds)
    raised_names = {row["fund_name"] for row in raised}
    fund_count = len(funds_by_name(funds))
    documented = documented_fund_count(facts)
    all_funds_known = documented == fund_count == len(raised)
    still_raising = tuple(sorted({row["fund_name"] for row in funds if row["fundraising_open"] == FUNDRAISING_OPEN}))
    conflicts = tuple(f"{row['fund_name']}: {row['conflict_note']}" for row in funds if row["conflict_note"])
    exact = all_funds_known and not still_raising and not conflicts and not any(map(is_lower_bound_amount, raised))
    targets = [row for row in funds if row["amount_type"] == AMOUNT_TARGET and row["fund_name"] not in raised_names]
    invested_rows = [row for row in funds if row["amount_type"] in INVESTED_AMOUNT_TYPES]
    invested = amounts_of(invested_rows)
    if investor[CAPITAL_INVESTED]:
        invested.append((investor[CAPITAL_INVESTED], investor["currency"]))
    return CapitalSummary(
        investor_id=investor["investor_id"],
        name=investor["name"],
        raised=sum_by_currency(amounts_of(raised)),
        lower_bound=bool(raised) and not exact,
        targets=sum_by_currency(amounts_of(targets)),
        invested=sum_by_currency(invested),
        fund_count=fund_count,
        funds_with_raised=len(raised),
        lp_commitments=sum_by_currency(amounts_of([row for row in raised if row['amount_type'] == AMOUNT_LP_COMMITMENT])),
        fundraising_open=still_raising,
        conflicts=conflicts,
        invested_fact_id=invested_capital_fact_id(facts) if investor[CAPITAL_INVESTED] else '',
        invested_period_fact_ids=tuple(row["fact_id"] for row in invested_rows if row["amount_type"] == AMOUNT_INVESTED_PERIOD),
        documented_fund_count=documented,
        raised_types=tuple(sorted({row["amount_type"] for row in raised})),
        aum=investor[CAPITAL_AUM],
        aum_currency=investor["currency"] if investor[CAPITAL_AUM] else "",
    )


def investor_capital(dataset: Dataset, investors: list[Row] | None = None) -> list[CapitalSummary]:
    funds = funds_by_investor(dataset.funds)
    facts = group_facts_by_investor(dataset.facts)
    return [
        capital_summary(investor, funds.get(investor["investor_id"], []), facts.get(investor["investor_id"], []))
        for investor in (verified_investors(dataset.investors) if investors is None else investors)
    ]
