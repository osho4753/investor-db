import re
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import date, timedelta

from investor_db.io import Dataset, Row
from investor_db.schema import (
    ACTIVITY_WINDOW_DAYS,
    CURRENCIES,
    EFFORT_ACTIVITIES,
    EFFORT_ACTORS,
    EVIDENCED_FIELDS,
    EXCLUSION_DUPLICATE,
    EXCLUSION_FOREIGN,
    EXCLUSION_REASONS,
    FACT_DOCUMENTED_INVESTMENT,
    FACT_EXCLUSION_REASON,
    FACT_FIELDS,
    FACT_VERDICTS,
    FUND_SCOPED_FACT_FIELDS,
    ID_PATTERNS,
    INVESTOR_TYPE_VC,
    INVESTOR_TYPES,
    INVESTOR_VERDICTS,
    LIST_FIELD_VOCABULARIES,
    MONEY_FACT_FIELDS,
    MONEY_FIELDS,
    PILOT_COUNTRY,
    PRIMARY_SOURCE_TYPES,
    REVIEWERS,
    SOURCE_TYPES,
    STATUS_EXCLUDED,
    STATUS_VERIFIED,
    STATUSES,
)
from investor_db.values import (
    is_valid_country,
    is_valid_ico,
    is_valid_url,
    normalize_name,
    parse_date,
    parse_money,
    split_list,
    website_domain,
)


@dataclass(frozen=True)
class Issue:
    table: str
    row_id: str
    message: str

    def __str__(self) -> str:
        return f"{self.table} [{self.row_id}]: {self.message}"


@dataclass(frozen=True)
class DuplicateGroup:
    criterion: str
    key: str
    investor_ids: tuple[str, ...]


def validate_dataset(dataset: Dataset, today: date) -> list[Issue]:
    return [
        *check_investors(dataset.investors, today),
        *check_sources(dataset.sources),
        *check_facts(dataset, today),
        *check_investor_evidence(dataset),
        *check_duplicate_investors(dataset.investors),
        *check_search_log(dataset.search_log, today),
        *check_reviews(dataset, today),
        *check_fact_reviews(dataset, today),
        *check_effort_log(dataset, today),
        *check_candidate_sources(dataset),
    ]


def check_identifiers(table: str, rows: list[Row], id_column: str) -> Iterator[Issue]:
    pattern = re.compile(ID_PATTERNS[id_column])
    for row in rows:
        if not pattern.fullmatch(row[id_column]):
            yield Issue(table, row[id_column] or "?", f"neplatný formát {id_column}")
    for identifier, count in Counter(row[id_column] for row in rows).items():
        if count > 1:
            yield Issue(table, identifier, f"duplicitní {id_column} ({count}×)")


def required_issues(table: str, row_id: str, row: Row, columns: Iterable[str]) -> Iterator[Issue]:
    for column in columns:
        if not row[column]:
            yield Issue(table, row_id, f"chybí povinné pole {column}")


def vocabulary_issues(table: str, row_id: str, column: str, text: str, vocabulary: Iterable[str]) -> Iterator[Issue]:
    if text and text not in vocabulary:
        yield Issue(table, row_id, f"{column} má neplatnou hodnotu {text!r}")


def list_issues(table: str, row_id: str, column: str, text: str) -> Iterator[Issue]:
    items = split_list(text)
    for item in items:
        if item not in LIST_FIELD_VOCABULARIES[column]:
            yield Issue(table, row_id, f"{column} má neplatnou položku {item!r}")
    if len(items) != len(set(items)):
        yield Issue(table, row_id, f"{column} obsahuje opakované položky")


def date_issues(table: str, row_id: str, column: str, text: str, today: date, required: bool) -> Iterator[Issue]:
    if not text:
        if required:
            yield Issue(table, row_id, f"chybí povinné pole {column}")
        return
    parsed = parse_date(text)
    if parsed is None:
        yield Issue(table, row_id, f"{column} není platné datum RRRR-MM-DD: {text!r}")
    elif parsed > today:
        yield Issue(table, row_id, f"{column} je v budoucnosti: {text}")


def check_investors(investors: list[Row], today: date) -> Iterator[Issue]:
    yield from check_identifiers("investors", investors, "investor_id")
    for row in investors:
        yield from check_investor_row(row, today)


def check_investor_row(row: Row, today: date) -> Iterator[Issue]:
    row_id = row["investor_id"]
    yield from required_issues("investors", row_id, row, ("name", "verification_status"))
    yield from vocabulary_issues("investors", row_id, "investor_type", row["investor_type"], INVESTOR_TYPES)
    yield from vocabulary_issues("investors", row_id, "verification_status", row["verification_status"], STATUSES)
    yield from format_issues(row)
    for column in LIST_FIELD_VOCABULARIES:
        yield from list_issues("investors", row_id, column, row[column])
    yield from investor_money_issues(row)
    yield from date_issues("investors", row_id, "last_verified_at", row["last_verified_at"], today, required=False)
    yield from exclusion_issues(row)
    if row["verification_status"] == STATUS_VERIFIED:
        yield from verified_row_issues(row)


def format_issues(row: Row) -> Iterator[Issue]:
    row_id = row["investor_id"]
    if row["country"] and not is_valid_country(row["country"]):
        yield Issue("investors", row_id, f"country není kód ISO 3166-1 alpha-2: {row['country']!r}")
    if row["registry_id"] and not is_valid_ico(row["registry_id"]):
        yield Issue("investors", row_id, f"registry_id není platné IČO: {row['registry_id']!r}")
    if row["website"] and not is_valid_url(row["website"]):
        yield Issue("investors", row_id, f"website není platná URL: {row['website']!r}")
    for url in split_list(row["evidence_urls"]):
        if not is_valid_url(url):
            yield Issue("investors", row_id, f"evidence_urls obsahuje neplatnou URL: {url!r}")


def investor_money_issues(row: Row) -> Iterator[Issue]:
    row_id = row["investor_id"]
    for column in MONEY_FIELDS:
        if row[column] and parse_money(row[column]) is None:
            yield Issue("investors", row_id, f"{column} není nezáporné číslo s desetinnou tečkou: {row[column]!r}")
    if any(row[column] for column in MONEY_FIELDS) and not row["currency"]:
        yield Issue("investors", row_id, "částky jsou vyplněny bez měny")
    yield from vocabulary_issues("investors", row_id, "currency", row["currency"], CURRENCIES)
    ticket_min = parse_money(row["typical_ticket_min"])
    ticket_max = parse_money(row["typical_ticket_max"])
    if ticket_min is not None and ticket_max is not None and ticket_min > ticket_max:
        yield Issue("investors", row_id, "typical_ticket_min je větší než typical_ticket_max")


def exclusion_issues(row: Row) -> Iterator[Issue]:
    row_id = row["investor_id"]
    reason = row["exclusion_reason"]
    if row["verification_status"] == STATUS_EXCLUDED:
        yield from required_issues("investors", row_id, row, ("investor_type",))
    if reason == EXCLUSION_FOREIGN and row["country"] in ("", PILOT_COUNTRY):
        yield Issue("investors", row_id, "zahraniční subjekt musí mít country jiné než CZ")
    if row["verification_status"] == STATUS_EXCLUDED and not reason:
        yield Issue("investors", row_id, "vyloučený subjekt nemá exclusion_reason")
    if row["verification_status"] != STATUS_EXCLUDED and reason:
        yield Issue("investors", row_id, "exclusion_reason je vyplněn u nevyloučeného subjektu")
    yield from vocabulary_issues("investors", row_id, "exclusion_reason", reason, EXCLUSION_REASONS)


def verified_row_issues(row: Row) -> Iterator[Issue]:
    row_id = row["investor_id"]
    yield from required_issues(
        "investors", row_id, row, ("registry_id", "investment_stages", "evidence_urls", "last_verified_at")
    )
    if row["investor_type"] != INVESTOR_TYPE_VC:
        yield Issue("investors", row_id, f"ověřený investor musí mít investor_type {INVESTOR_TYPE_VC!r}")
    if row["country"] != PILOT_COUNTRY:
        yield Issue("investors", row_id, f"ověřený investor musí mít country {PILOT_COUNTRY!r}")


def check_sources(sources: list[Row]) -> Iterator[Issue]:
    yield from check_identifiers("sources", sources, "source_id")
    for row in sources:
        row_id = row["source_id"]
        yield from required_issues("sources", row_id, row, ("url", "publisher", "source_type"))
        if row["url"] and not is_valid_url(row["url"]):
            yield Issue("sources", row_id, f"url není platná URL: {row['url']!r}")
        yield from vocabulary_issues("sources", row_id, "source_type", row["source_type"], SOURCE_TYPES)
    for url, count in Counter(row["url"] for row in sources if row["url"]).items():
        if count > 1:
            yield Issue("sources", url, f"duplicitní url ({count}×)")


def check_facts(dataset: Dataset, today: date) -> Iterator[Issue]:
    investor_ids = {row["investor_id"] for row in dataset.investors}
    source_ids = {row["source_id"] for row in dataset.sources}
    yield from check_identifiers("facts", dataset.facts, "fact_id")
    for row in dataset.facts:
        row_id = row["fact_id"]
        yield from required_issues("facts", row_id, row, ("investor_id", "field", "value", "source_id", "evidence_note"))
        if row["investor_id"] and row["investor_id"] not in investor_ids:
            yield Issue("facts", row_id, f"odkaz na neexistujícího investora {row['investor_id']!r}")
        if row["source_id"] and row["source_id"] not in source_ids:
            yield Issue("facts", row_id, f"odkaz na neexistující zdroj {row['source_id']!r}")
        yield from vocabulary_issues("facts", row_id, "field", row["field"], FACT_FIELDS)
        yield from date_issues("facts", row_id, "accessed_at", row["accessed_at"], today, required=True)
        yield from date_issues("facts", row_id, "value_as_of", row["value_as_of"], today, required=False)
        yield from fact_value_issues(row)
    yield from duplicate_fact_issues(dataset.facts)


def fact_value_issues(row: Row) -> Iterator[Issue]:
    row_id = row["fact_id"]
    field = row["field"]
    value = row["value"]
    if field in MONEY_FACT_FIELDS:
        if value and parse_money(value) is None:
            yield Issue("facts", row_id, f"hodnota není nezáporné číslo s desetinnou tečkou: {value!r}")
        if not row["currency"]:
            yield Issue("facts", row_id, "peněžní fakt nemá měnu")
        yield from vocabulary_issues("facts", row_id, "currency", row["currency"], CURRENCIES)
    elif row["currency"]:
        yield Issue("facts", row_id, "nepeněžní fakt má vyplněnou měnu")
    if field in LIST_FIELD_VOCABULARIES:
        yield from list_issues("facts", row_id, field, value)
    if field == "registry_id" and value and not is_valid_ico(value):
        yield Issue("facts", row_id, f"hodnota není platné IČO: {value!r}")
    if field == "website" and value and not is_valid_url(value):
        yield Issue("facts", row_id, f"hodnota není platná URL: {value!r}")
    if field in FUND_SCOPED_FACT_FIELDS and not row["fund_name"]:
        yield Issue("facts", row_id, f"fakt {field} musí mít fund_name")
    if field == FACT_EXCLUSION_REASON:
        yield from vocabulary_issues("facts", row_id, "hodnota", value, EXCLUSION_REASONS)
    if field == FACT_DOCUMENTED_INVESTMENT and not row["value_as_of"]:
        yield Issue("facts", row_id, "doložená investice musí mít value_as_of (datum investice)")


def duplicate_fact_issues(facts: list[Row]) -> Iterator[Issue]:
    content_keys = Counter(
        (row["investor_id"], row["field"], row["value"], row["currency"], row["fund_name"], row["source_id"])
        for row in facts
    )
    for key, count in content_keys.items():
        if count > 1:
            yield Issue("facts", key[0], f"duplicitní fakt {key[1]}={key[2]!r} ze zdroje {key[5]} ({count}×)")


def group_facts_by_investor(facts: list[Row]) -> dict[str, list[Row]]:
    grouped: dict[str, list[Row]] = defaultdict(list)
    for row in facts:
        grouped[row["investor_id"]].append(row)
    return grouped


def check_investor_evidence(dataset: Dataset) -> Iterator[Issue]:
    facts_by_investor = group_facts_by_investor(dataset.facts)
    sources_by_id = {row["source_id"]: row for row in dataset.sources}
    for investor in dataset.investors:
        facts = facts_by_investor.get(investor["investor_id"], [])
        yield from field_support_issues(investor, facts)
        yield from evidence_url_issues(investor, facts, sources_by_id)
        yield from verification_date_issues(investor, facts)
        if investor["verification_status"] == STATUS_VERIFIED:
            yield from inclusion_criteria_issues(investor, facts, sources_by_id)
        if investor["verification_status"] == STATUS_EXCLUDED:
            yield from exclusion_evidence_issues(investor, facts)


def fields_requiring_evidence(investor: Row) -> tuple[str, ...]:
    if investor["verification_status"] == STATUS_VERIFIED:
        return EVIDENCED_FIELDS
    return tuple(column for column in EVIDENCED_FIELDS if column != "name")


def field_support_issues(investor: Row, facts: list[Row]) -> Iterator[Issue]:
    for column in fields_requiring_evidence(investor):
        value = investor[column]
        if value and not is_supported(column, value, investor["currency"], facts):
            yield Issue("investors", investor["investor_id"], f"hodnota pole {column} nemá podpůrný fakt")


def is_supported(column: str, value: str, currency: str, facts: list[Row]) -> bool:
    candidates = [row for row in facts if row["field"] == column]
    if column in LIST_FIELD_VOCABULARIES:
        documented = {item for row in candidates for item in split_list(row["value"])}
        return set(split_list(value)) <= documented
    if column in MONEY_FIELDS:
        amount = parse_money(value)
        return amount is not None and any(
            parse_money(row["value"]) == amount and row["currency"] == currency for row in candidates
        )
    return any(row["value"] == value for row in candidates)


def expected_evidence_urls(facts: list[Row], sources_by_id: dict[str, Row]) -> list[str]:
    return sorted({sources_by_id[row["source_id"]]["url"] for row in facts if row["source_id"] in sources_by_id})


def evidence_url_issues(investor: Row, facts: list[Row], sources_by_id: dict[str, Row]) -> Iterator[Issue]:
    expected = expected_evidence_urls(facts, sources_by_id)
    if set(split_list(investor["evidence_urls"])) != set(expected):
        yield Issue(
            "investors",
            investor["investor_id"],
            f"evidence_urls neodpovídá zdrojům faktů; očekáváno: {';'.join(expected)!r}",
        )


def verification_date_issues(investor: Row, facts: list[Row]) -> Iterator[Issue]:
    last_verified = parse_date(investor["last_verified_at"])
    access_dates = [parsed for row in facts if (parsed := parse_date(row["accessed_at"])) is not None]
    if last_verified is not None and access_dates and last_verified < max(access_dates):
        yield Issue("investors", investor["investor_id"], "last_verified_at je starší než nejnovější accessed_at faktů")


def inclusion_criteria_issues(investor: Row, facts: list[Row], sources_by_id: dict[str, Row]) -> Iterator[Issue]:
    row_id = investor["investor_id"]
    if not has_primary_registry_fact(investor, facts, sources_by_id):
        yield Issue("investors", row_id, "kritérium Z1: IČO není doloženo faktem z primárního zdroje")
    if not any(row["fund_name"] for row in facts):
        yield Issue("investors", row_id, "kritérium Z3: chybí fakt o fondu (fund_name)")
    last_verified = parse_date(investor["last_verified_at"])
    if last_verified is not None and not has_recent_investment(facts, last_verified):
        yield Issue("investors", row_id, f"kritérium Z4: chybí doložená investice za posledních {ACTIVITY_WINDOW_DAYS} dní")


def exclusion_evidence_issues(investor: Row, facts: list[Row]) -> Iterator[Issue]:
    reason = investor["exclusion_reason"]
    if reason and not any(row["field"] == FACT_EXCLUSION_REASON and row["value"] == reason for row in facts):
        yield Issue("investors", investor["investor_id"], f"důvod vyloučení {reason!r} není doložen faktem {FACT_EXCLUSION_REASON}")


def is_primary_source(source_id: str, sources_by_id: dict[str, Row]) -> bool:
    source = sources_by_id.get(source_id)
    return source is not None and source["source_type"] in PRIMARY_SOURCE_TYPES


def has_primary_registry_fact(investor: Row, facts: list[Row], sources_by_id: dict[str, Row]) -> bool:
    return any(
        row["field"] == "registry_id"
        and row["value"] == investor["registry_id"]
        and is_primary_source(row["source_id"], sources_by_id)
        for row in facts
    )


def has_recent_investment(facts: list[Row], reference_date: date) -> bool:
    window_start = reference_date - timedelta(days=ACTIVITY_WINDOW_DAYS)
    investment_dates = [
        parse_date(row["value_as_of"]) for row in facts if row["field"] == FACT_DOCUMENTED_INVESTMENT
    ]
    return any(invested_at is not None and invested_at >= window_start for invested_at in investment_dates)


DUPLICATE_KEYS: dict[str, Callable[[Row], str]] = {
    "IČO": lambda row: row["registry_id"],
    "doména webu": lambda row: website_domain(row["website"]) if row["website"] else "",
    "normalizovaný název": lambda row: normalize_name(row["name"]),
}


def find_duplicate_groups(investors: list[Row]) -> list[DuplicateGroup]:
    candidates = [row for row in investors if row["exclusion_reason"] != EXCLUSION_DUPLICATE]
    groups: list[DuplicateGroup] = []
    for criterion, key_of in DUPLICATE_KEYS.items():
        ids_by_key: dict[str, list[str]] = defaultdict(list)
        for row in candidates:
            if key := key_of(row):
                ids_by_key[key].append(row["investor_id"])
        groups.extend(DuplicateGroup(criterion, key, tuple(ids)) for key, ids in ids_by_key.items() if len(ids) > 1)
    return groups


def check_duplicate_investors(investors: list[Row]) -> Iterator[Issue]:
    for group in find_duplicate_groups(investors):
        yield Issue("investors", ",".join(group.investor_ids), f"možná duplicita podle kritéria {group.criterion}: {group.key!r}")


def check_search_log(search_log: list[Row], today: date) -> Iterator[Issue]:
    yield from check_identifiers("search_log", search_log, "search_id")
    for row in search_log:
        row_id = row["search_id"]
        yield from required_issues("search_log", row_id, row, ("source_url", "query", "results_count", "minutes"))
        yield from date_issues("search_log", row_id, "searched_at", row["searched_at"], today, required=True)
        if row["source_url"] and not is_valid_url(row["source_url"]):
            yield Issue("search_log", row_id, f"source_url není platná URL: {row['source_url']!r}")
        if row["results_count"] and not row["results_count"].isdigit():
            yield Issue("search_log", row_id, f"results_count není nezáporné celé číslo: {row['results_count']!r}")
        yield from minutes_issues("search_log", row_id, row["minutes"])


def minutes_issues(table: str, row_id: str, text: str) -> Iterator[Issue]:
    if text and not (text.isdigit() and int(text) > 0):
        yield Issue(table, row_id, f"minutes není kladné celé číslo: {text!r}")


def check_effort_log(dataset: Dataset, today: date) -> Iterator[Issue]:
    investor_ids = {row["investor_id"] for row in dataset.investors}
    for row in dataset.effort_log:
        row_id = f"{row['investor_id']}/{row['activity']}/{row['actor']}"
        yield from required_issues("effort_log", row_id, row, ("activity", "actor", "minutes"))
        if row["investor_id"] not in investor_ids:
            yield Issue("effort_log", row_id, f"odkaz na neexistujícího investora {row['investor_id']!r}")
        yield from vocabulary_issues("effort_log", row_id, "activity", row["activity"], EFFORT_ACTIVITIES)
        yield from vocabulary_issues("effort_log", row_id, "actor", row["actor"], EFFORT_ACTORS)
        yield from minutes_issues("effort_log", row_id, row["minutes"])
        yield from date_issues("effort_log", row_id, "logged_at", row["logged_at"], today, required=True)


def check_reviews(dataset: Dataset, today: date) -> Iterator[Issue]:
    investor_ids = {row["investor_id"] for row in dataset.investors}
    yield from check_review_rows("reviews", dataset.reviews, "investor_id", investor_ids, INVESTOR_VERDICTS, today)


def check_fact_reviews(dataset: Dataset, today: date) -> Iterator[Issue]:
    fact_ids = {row["fact_id"] for row in dataset.facts}
    yield from check_review_rows("fact_reviews", dataset.fact_reviews, "fact_id", fact_ids, FACT_VERDICTS, today)


def check_review_rows(
    table: str,
    rows: list[Row],
    target_column: str,
    target_ids: set[str],
    verdicts: Iterable[str],
    today: date,
) -> Iterator[Issue]:
    for row in rows:
        row_id = f"{row[target_column]}/{row['reviewer']}"
        if row[target_column] not in target_ids:
            yield Issue(table, row_id, f"odkaz na neexistující {target_column} {row[target_column]!r}")
        yield from required_issues(table, row_id, row, ("reviewer",))
        yield from vocabulary_issues(table, row_id, "reviewer", row["reviewer"], REVIEWERS)
        yield from vocabulary_issues(table, row_id, "verdict", row["verdict"], verdicts)
        yield from date_issues(table, row_id, "reviewed_at", row["reviewed_at"], today, required=bool(row["verdict"]))
        yield from minutes_issues(table, row_id, row["review_minutes"])
    for (target_id, reviewer), count in Counter((row[target_column], row["reviewer"]) for row in rows).items():
        if count > 1:
            yield Issue(table, f"{target_id}/{reviewer}", f"hodnotitel má více kontrol téhož záznamu ({count}×)")


def check_candidate_sources(dataset: Dataset) -> Iterator[Issue]:
    investor_ids = {row["investor_id"] for row in dataset.investors}
    search_ids = {row["search_id"] for row in dataset.search_log}
    for row in dataset.candidate_sources:
        row_id = f"{row['investor_id']}/{row['search_id']}"
        if row["investor_id"] not in investor_ids:
            yield Issue("candidate_sources", row_id, f"odkaz na neexistujícího investora {row['investor_id']!r}")
        if row["search_id"] not in search_ids:
            yield Issue("candidate_sources", row_id, f"odkaz na neexistující průchod {row['search_id']!r}")
    for (investor_id, search_id), count in Counter(
        (row["investor_id"], row["search_id"]) for row in dataset.candidate_sources
    ).items():
        if count > 1:
            yield Issue("candidate_sources", f"{investor_id}/{search_id}", f"duplicitní vazba ({count}×)")
    found_ids = {row["investor_id"] for row in dataset.candidate_sources}
    for investor_id in sorted(investor_ids - found_ids):
        yield Issue("investors", investor_id, "chybí záznam v candidate_sources (ve kterém průchodu byl subjekt nalezen)")
