import pytest
from conftest import REGISTRY_URL, TODAY, fact

from investor_db.io import Dataset
from investor_db.validation import find_duplicate_groups, validate_dataset


def messages(dataset: Dataset) -> list[str]:
    return [issue.message for issue in validate_dataset(dataset, TODAY)]


def assert_reported(dataset: Dataset, fragment: str) -> None:
    found = messages(dataset)
    assert any(fragment in message for message in found), found


def test_valid_dataset_has_no_issues(dataset: Dataset) -> None:
    assert validate_dataset(dataset, TODAY) == []


@pytest.mark.parametrize(
    ("table", "index", "column", "value", "fragment"),
    [
        ("investors", 0, "investor_id", "inv-1", "neplatný formát investor_id"),
        ("investors", 0, "name", "", "chybí povinné pole name"),
        ("investors", 2, "investor_type", "", "chybí povinné pole investor_type"),
        ("investors", 0, "investor_type", "andel", "investor_type má neplatnou hodnotu"),
        ("investors", 0, "investor_type", "pe", "musí mít investor_type"),
        ("investors", 0, "country", "cz", "ISO 3166-1"),
        ("investors", 0, "country", "SK", "musí mít country"),
        ("investors", 0, "registry_id", "12345678", "registry_id není platné IČO"),
        ("investors", 0, "registry_id", "", "chybí povinné pole registry_id"),
        ("investors", 0, "website", "fiktivni.example.com", "website není platná URL"),
        ("investors", 0, "investment_sectors", "software;kryptomeny", "neplatnou položku"),
        ("investors", 0, "investment_stages", "seed;seed", "opakované položky"),
        ("investors", 0, "investment_stages", "", "chybí povinné pole investment_stages"),
        ("investors", 0, "typical_ticket_min", "1 000", "není nezáporné číslo"),
        ("investors", 0, "typical_ticket_min", "3000000", "větší než typical_ticket_max"),
        ("investors", 0, "currency", "", "bez měny"),
        ("investors", 0, "currency", "EURO", "currency má neplatnou hodnotu"),
        ("investors", 0, "verification_status", "hotovo", "verification_status má neplatnou hodnotu"),
        ("investors", 0, "exclusion_reason", "duplicita", "u nevyloučeného subjektu"),
        ("investors", 0, "last_verified_at", "2026-13-01", "není platné datum"),
        ("investors", 0, "last_verified_at", "2027-01-01", "v budoucnosti"),
        ("investors", 0, "last_verified_at", "2026-09-01", "starší než nejnovější accessed_at"),
        ("investors", 0, "last_verified_at", "", "chybí povinné pole last_verified_at"),
        ("investors", 0, "name", "Nedoložený název", "name nemá podpůrný fakt"),
        ("investors", 0, "total_fund_size", "31000000", "total_fund_size nemá podpůrný fakt"),
        ("investors", 0, "investment_sectors", "software;fintech;ai", "investment_sectors nemá podpůrný fakt"),
        ("investors", 0, "currency", "CZK", "typical_ticket_min nemá podpůrný fakt"),
        ("investors", 0, "evidence_urls", REGISTRY_URL, "evidence_urls neodpovídá"),
        ("investors", 0, "evidence_urls", "neplatna-url", "evidence_urls obsahuje neplatnou URL"),
        ("investors", 1, "website", "https://jiny.example.com", "website nemá podpůrný fakt"),
        ("investors", 2, "exclusion_reason", "", "nemá exclusion_reason"),
        ("investors", 2, "exclusion_reason", "nelibi_se", "exclusion_reason má neplatnou hodnotu"),
        ("facts", 0, "fact_id", "f-1", "neplatný formát fact_id"),
        ("facts", 0, "investor_id", "inv-9999", "neexistujícího investora"),
        ("facts", 0, "source_id", "src-9999", "neexistující zdroj"),
        ("facts", 0, "source_id", "src-0003", "kritérium Z1"),
        ("facts", 0, "field", "neznamy", "field má neplatnou hodnotu"),
        ("facts", 0, "value", "1234", "hodnota není platné IČO"),
        ("facts", 0, "evidence_note", "", "chybí povinné pole evidence_note"),
        ("facts", 0, "accessed_at", "", "chybí povinné pole accessed_at"),
        ("facts", 0, "accessed_at", "2027-01-01", "accessed_at je v budoucnosti"),
        ("facts", 0, "currency", "EUR", "nepeněžní fakt má vyplněnou měnu"),
        ("facts", 2, "value", "nejde", "hodnota není platná URL"),
        ("facts", 4, "value", "seed;andel", "neplatnou položku"),
        ("facts", 5, "currency", "", "peněžní fakt nemá měnu"),
        ("facts", 5, "currency", "XXX", "currency má neplatnou hodnotu"),
        ("facts", 5, "value", "abc", "hodnota není nezáporné číslo"),
        ("facts", 7, "fund_name", "", "musí mít fund_name"),
        ("facts", 7, "value_as_of", "2025-02-30", "value_as_of není platné datum"),
        ("facts", 8, "value_as_of", "", "musí mít value_as_of"),
        ("sources", 0, "source_id", "src-1", "neplatný formát source_id"),
        ("sources", 0, "url", "rejstrik", "url není platná URL"),
        ("sources", 0, "publisher", "", "chybí povinné pole publisher"),
        ("sources", 0, "source_type", "blog", "source_type má neplatnou hodnotu"),
        ("sources", 1, "url", REGISTRY_URL, "duplicitní url"),
        ("search_log", 0, "search_id", "s-1", "neplatný formát search_id"),
        ("search_log", 0, "searched_at", "", "chybí povinné pole searched_at"),
        ("search_log", 0, "source_url", "seznam", "source_url není platná URL"),
        ("search_log", 0, "query", "", "chybí povinné pole query"),
        ("search_log", 0, "results_count", "-1", "results_count není nezáporné celé číslo"),
        ("search_log", 0, "minutes", "", "chybí povinné pole minutes"),
        ("search_log", 0, "minutes", "0", "minutes není kladné číslo"),
        ("investors", 2, "exclusion_reason", "family_office", "není doložen faktem duvod_vylouceni"),
        ("facts", 10, "value", "nelibi_se", "hodnota má neplatnou hodnotu"),
        ("facts", 10, "investor_id", "inv-0002", "není doložen faktem duvod_vylouceni"),
        ("effort_log", 0, "investor_id", "inv-0999", "neexistujícího investora"),
        ("effort_log", 0, "activity", "pauza", "activity má neplatnou hodnotu"),
        ("effort_log", 0, "actor", "R3", "actor má neplatnou hodnotu"),
        ("effort_log", 0, "minutes", "1.555", "minutes není kladné číslo"),
        ("effort_log", 0, "minutes", "", "chybí povinné pole minutes"),
        ("effort_log", 0, "logged_at", "", "chybí povinné pole logged_at"),
        ("effort_log", 0, "activity", "kontrola", "activity má neplatnou hodnotu"),
        ("reviews", 0, "review_minutes", "0", "minutes není kladné číslo"),
        ("fact_reviews", 0, "review_minutes", "-2", "minutes není kladné číslo"),
        ("candidate_sources", 0, "investor_id", "inv-0999", "neexistujícího investora"),
        ("candidate_sources", 0, "search_id", "s-999", "neexistující průchod"),
        ("candidate_sources", 1, "investor_id", "inv-0001", "duplicitní vazba"),
        ("candidate_sources", 2, "investor_id", "inv-0002", "chybí záznam v candidate_sources"),
        ("reviews", 0, "investor_id", "inv-0999", "neexistující investor_id"),
        ("reviews", 0, "reviewer", "R3", "reviewer má neplatnou hodnotu"),
        ("reviews", 0, "verdict", "ano", "verdict má neplatnou hodnotu"),
        ("reviews", 0, "reviewed_at", "", "chybí povinné pole reviewed_at"),
        ("fact_reviews", 0, "fact_id", "f-99999", "neexistující fact_id"),
        ("fact_reviews", 0, "verdict", "TP", "verdict má neplatnou hodnotu"),
    ],
)
def test_invalid_value_is_reported(
    dataset: Dataset, table: str, index: int, column: str, value: str, fragment: str
) -> None:
    getattr(dataset, table)[index][column] = value

    assert_reported(dataset, fragment)


def test_candidate_with_unknown_type_and_country_is_allowed(dataset: Dataset) -> None:
    dataset.investors[1].update(investor_type="", country="")

    assert validate_dataset(dataset, TODAY) == []


def test_duplicate_investor_id_is_reported(dataset: Dataset) -> None:
    dataset.investors[2]["investor_id"] = "inv-0002"

    assert_reported(dataset, "duplicitní investor_id")


def test_pending_review_without_verdict_is_allowed(dataset: Dataset) -> None:
    dataset.reviews[0].update(verdict="", reviewed_at="")

    assert validate_dataset(dataset, TODAY) == []


def test_duplicate_review_by_same_reviewer_is_reported(dataset: Dataset) -> None:
    dataset.reviews.append(dict(dataset.reviews[0]))

    assert_reported(dataset, "více kontrol téhož záznamu")


def test_second_reviewer_is_allowed(dataset: Dataset) -> None:
    dataset.reviews.append(dict(dataset.reviews[0], reviewer="R2"))

    assert validate_dataset(dataset, TODAY) == []


def test_verified_investor_without_fund_fact_violates_z3(dataset: Dataset) -> None:
    dataset.facts = [row for row in dataset.facts if not row["fund_name"]]
    dataset.investors[0]["total_fund_size"] = ""

    assert_reported(dataset, "kritérium Z3")


def test_duplicate_fact_is_reported(dataset: Dataset) -> None:
    dataset.facts.append(dict(dataset.facts[1], fact_id="f-00099"))

    assert_reported(dataset, "duplicitní fakt name")


def test_money_fact_in_other_currency_is_allowed(dataset: Dataset) -> None:
    dataset.facts.append(
        fact("f-00012", "assets_under_management", "900000000", "src-0002", currency="CZK", value_as_of="2025-12-31")
    )

    assert validate_dataset(dataset, TODAY) == []


def test_fund_info_requires_fund_name(dataset: Dataset) -> None:
    dataset.facts.append(fact("f-00012", "informace_o_fondu", "first close 10 mil. EUR", "src-0002"))

    assert_reported(dataset, "fakt informace_o_fondu musí mít fund_name")


def test_target_fund_size_requires_fund_name(dataset: Dataset) -> None:
    dataset.facts.append(fact("f-00012", "cilova_velikost_fondu", "50000000", "src-0002", currency="EUR"))

    assert_reported(dataset, "fakt cilova_velikost_fondu musí mít fund_name")


def test_foreign_excluded_subject_is_allowed(dataset: Dataset) -> None:
    dataset.investors[2].update(investor_type="vc", country="DE", exclusion_reason="zahranicni_subjekt")
    dataset.facts[10]["value"] = "zahranicni_subjekt"

    assert validate_dataset(dataset, TODAY) == []


@pytest.mark.parametrize(
    ("column", "value", "criterion"),
    [
        ("name", "FIKTIVNÍ VENTURES, a.s.", "normalizovaný název"),
        ("website", "https://www.fiktivni-ventures.example.com/o-nas", "doména webu"),
        ("registry_id", "12345679", "IČO"),
    ],
)
def test_duplicate_investors_are_detected(dataset: Dataset, column: str, value: str, criterion: str) -> None:
    dataset.investors[1][column] = value

    groups = find_duplicate_groups(dataset.investors)

    assert [(group.criterion, group.investor_ids) for group in groups] == [(criterion, ("inv-0001", "inv-0002"))]
    assert_reported(dataset, f"možná duplicita podle kritéria {criterion}")


def test_record_excluded_as_duplicate_is_not_reported(dataset: Dataset) -> None:
    dataset.investors[2].update(name="Fiktivní Ventures", exclusion_reason="duplicita")

    assert find_duplicate_groups(dataset.investors) == []


@pytest.mark.parametrize("country", ["", "CZ"])
def test_foreign_excluded_subject_needs_foreign_country(dataset: Dataset, country: str) -> None:
    dataset.investors[2].update(country=country, exclusion_reason="zahranicni_subjekt")
    dataset.facts[10]["value"] = "zahranicni_subjekt"

    assert_reported(dataset, "musí mít country jiné než CZ")


def test_excluded_subject_with_unknown_country_is_allowed(dataset: Dataset) -> None:
    dataset.investors[2]["country"] = ""

    assert validate_dataset(dataset, TODAY) == []


def test_old_investment_without_new_fund_violates_z4(dataset: Dataset) -> None:
    dataset.facts[8]["value_as_of"] = "2023-01-01"
    dataset.facts[7]["value_as_of"] = "2020-01-01"

    assert_reported(dataset, "kritérium Z4")


def test_new_fund_within_window_satisfies_z4(dataset: Dataset) -> None:
    dataset.facts[8]["value_as_of"] = "2023-01-01"

    assert validate_dataset(dataset, TODAY) == []


@pytest.mark.parametrize("minutes", ["0.04", "1.5", "12"])
def test_decimal_minutes_are_allowed(dataset: Dataset, minutes: str) -> None:
    dataset.effort_log[0]["minutes"] = minutes
    dataset.search_log[0]["minutes"] = minutes

    assert validate_dataset(dataset, TODAY) == []
