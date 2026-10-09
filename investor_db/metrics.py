import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from investor_db.io import Dataset, Row
from investor_db.schema import (
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    EXCLUSION_DUPLICATE,
    FRESHNESS_WINDOW_DAYS,
    INVESTOR_COLUMNS,
    MONEY_FIELDS,
    REVIEWER_INDEPENDENT,
    REVIEWER_PRIMARY,
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


def investor_verdicts(dataset: Dataset, reviewer: str) -> dict[str, str]:
    eligible = verified_ids(dataset.investors)
    return {
        row["investor_id"]: row["verdict"]
        for row in dataset.reviews
        if row["reviewer"] == reviewer and row["verdict"] and row["investor_id"] in eligible
    }


def precision(dataset: Dataset, reviewer: str = REVIEWER_PRIMARY) -> PrecisionResult:
    counts = Counter(investor_verdicts(dataset, reviewer).values())
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


def fact_accuracy(dataset: Dataset, reviewer: str = REVIEWER_PRIMARY) -> FactAccuracyResult:
    fact_ids = {row["fact_id"] for row in dataset.facts}
    counts = Counter(
        row["verdict"]
        for row in dataset.fact_reviews
        if row["reviewer"] == reviewer and row["verdict"] and row["fact_id"] in fact_ids
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
