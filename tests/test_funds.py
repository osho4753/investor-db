from decimal import Decimal

import pytest
from conftest import FUND_NAME, TODAY, fact

from investor_db.io import Dataset, Row
from investor_db.metrics import investor_capital, requirement_completeness
from investor_db.report import render_report
from investor_db.validation import validate_dataset


def messages(dataset: Dataset) -> list[str]:
    return [issue.message for issue in validate_dataset(dataset, TODAY)]


def assert_reported(dataset: Dataset, fragment: str) -> None:
    found = messages(dataset)
    assert any(fragment in message for message in found), found


def fund(fund_id: str, fund_name: str, fact_id: str, **overrides: str) -> Row:
    row = {
        "fund_id": fund_id,
        "investor_id": "inv-0001",
        "fund_name": fund_name,
        "vintage": "",
        "amount": "",
        "currency": "",
        "amount_type": "",
        "approx": "",
        "amount_wording": "",
        "value_as_of": "",
        "fact_id": fact_id,
        "fundraising_open": "",
        "conflict_note": "",
    }
    row.update(overrides)
    return row


def add_approximate_first_close(dataset: Dataset) -> None:
    dataset.facts.append(
        fact("f-00012", "fond_first_close", "55000000", "src-0002", currency="EUR", fund_name="Fiktivní Fond II")
    )
    dataset.funds.append(
        fund(
            "fd-0002",
            "Fiktivní Fond II",
            "f-00012",
            amount="55000000",
            currency="EUR",
            amount_type="first_close",
            approx="ano",
            amount_wording="téměř 55 mil. EUR",
        )
    )


def test_valid_funds_have_no_issues(dataset: Dataset) -> None:
    add_approximate_first_close(dataset)

    assert validate_dataset(dataset, TODAY) == []


@pytest.mark.parametrize(
    ("column", "value", "fragment"),
    [
        ("fund_id", "fond-1", "neplatný formát fund_id"),
        ("investor_id", "inv-9999", "neexistujícího investora"),
        ("fund_name", "", "chybí povinné pole fund_name"),
        ("fact_id", "", "chybí povinné pole fact_id"),
        ("fact_id", "f-99999", "neexistující fakt"),
        ("vintage", "25", "vintage není rok"),
        ("value_as_of", "2027-01-01", "v budoucnosti"),
        ("amount", "30 000 000", "amount není nezáporné číslo"),
        ("amount", "31000000", "neshoduje s faktem"),
        ("currency", "", "chybí povinné pole currency"),
        ("currency", "CZK", "neshoduje s faktem"),
        ("amount_type", "", "chybí povinné pole amount_type"),
        ("amount_type", "odhad", "amount_type má neplatnou hodnotu"),
        ("amount_type", "first_close", "typ first_close musí dokládat fakt fond_first_close"),
        ("approx", "", "chybí povinné pole approx"),
        ("approx", "asi", "approx má neplatnou hodnotu"),
        ("approx", "ano", "musí mít amount_wording"),
        ("fund_name", "Jiný fond", "fund_name faktu se neshoduje"),
        ("fundraising_open", "možná", "fundraising_open má neplatnou hodnotu"),
    ],
)
def test_invalid_fund_is_reported(dataset: Dataset, column: str, value: str, fragment: str) -> None:
    dataset.funds[0][column] = value

    assert_reported(dataset, fragment)


def test_fund_fact_of_other_investor_is_reported(dataset: Dataset) -> None:
    dataset.facts[7]["investor_id"] = "inv-0002"

    assert_reported(dataset, "fakt patří jinému investorovi")


def test_fund_without_amount_must_not_have_amount_columns(dataset: Dataset) -> None:
    dataset.funds.append(fund("fd-0002", FUND_NAME, "f-00010", amount_type="cil"))

    assert_reported(dataset, "fond bez částky nesmí mít vyplněné amount_type")


def test_fund_without_amount_needs_fund_fact(dataset: Dataset) -> None:
    dataset.funds.append(fund("fd-0002", "Fiktivní Fond II", "f-00004"))

    assert_reported(dataset, "nedokládá existenci fondu")


def test_fund_without_amount_is_valid_with_fund_fact(dataset: Dataset) -> None:
    dataset.facts[9]["fund_name"] = "Fiktivní Fond II"
    dataset.funds.append(fund("fd-0002", "Fiktivní Fond II", "f-00010"))

    assert validate_dataset(dataset, TODAY) == []


def test_duplicate_fund_of_investor_is_reported(dataset: Dataset) -> None:
    dataset.funds.append(dict(dataset.funds[0], fund_id="fd-0002"))

    assert_reported(dataset, "je zapsán s velikostí vícekrát")


def add_invested(dataset: Dataset, fund_name: str = FUND_NAME) -> None:
    dataset.facts.append(fact("f-00014", "fond_investovano", "12000000", "src-0002", currency="CZK", fund_name=fund_name))
    dataset.funds.append(
        fund("fd-0004", fund_name, "f-00014", amount="12000000", currency="CZK", amount_type="investovano", approx="ne")
    )


def test_fund_may_have_size_and_invested_amount(dataset: Dataset) -> None:
    add_invested(dataset)

    assert validate_dataset(dataset, TODAY) == []


def add_fund_count(dataset: Dataset, count: str) -> None:
    dataset.facts.append(fact("f-00015", "pocet_fondu", count, "src-0002", value_as_of="2026-01-01"))


@pytest.mark.parametrize("count", ["0", "dva", "1.5"])
def test_invalid_fund_count_is_reported(dataset: Dataset, count: str) -> None:
    add_fund_count(dataset, count)

    assert_reported(dataset, "počet fondů není kladné celé číslo")


@pytest.mark.parametrize(
    ("investor_id", "target_field", "fragment"),
    [
        ("inv-0001", "", "se vyplňují jen společně"),
        ("", "kapital", "se vyplňují jen společně"),
        ("inv-9999", "kapital", "neexistujícího investora"),
        ("inv-0001", "velikost", "target_field má neplatnou hodnotu"),
    ],
)
def test_invalid_search_target_is_reported(dataset: Dataset, investor_id: str, target_field: str, fragment: str) -> None:
    dataset.search_log[0].update(investor_id=investor_id, target_field=target_field)

    assert_reported(dataset, fragment)


def test_requirement_completeness_counts_capital_kinds(dataset: Dataset) -> None:
    add_approximate_first_close(dataset)

    result = requirement_completeness(dataset)

    assert result.filled["kapital"].numerator == 1
    assert result.capital_by_kind["final_close"].numerator == 1
    assert result.capital_by_kind["first_close"].numerator == 1
    assert result.capital_by_kind["assets_under_management"].numerator == 0


def test_requirement_completeness_counts_searched_and_not_found(dataset: Dataset) -> None:
    dataset.investors[0]["typical_ticket_min"] = ""
    dataset.investors[0]["typical_ticket_max"] = ""
    dataset.investors[0]["currency"] = ""
    dataset.investors[0]["total_fund_size"] = ""
    dataset.search_log[0].update(investor_id="inv-0001", target_field="typical_ticket")

    result = requirement_completeness(dataset)

    assert result.filled["typical_ticket"].numerator == 0
    assert result.searched_not_found["typical_ticket"] == 1
    assert result.searched_not_found["kapital"] == 0


def test_capital_is_summed_per_currency_and_marked_as_lower_bound(dataset: Dataset) -> None:
    add_approximate_first_close(dataset)
    dataset.facts.append(
        fact("f-00013", "fond_zavazek_lp", "94000000", "src-0002", currency="CZK", fund_name="Fiktivní Fond III")
    )
    dataset.funds.append(
        fund("fd-0003", "Fiktivní Fond III", "f-00013", amount="94000000", currency="CZK", amount_type="zavazek_jednoho_lp", approx="ne")
    )

    add_fund_count(dataset, "3")

    summary = investor_capital(dataset)[0]

    assert summary.raised == {"CZK": Decimal("94000000"), "EUR": Decimal("85000000")}
    assert summary.lower_bound
    assert summary.fund_count == 3


def add_target_fund(dataset: Dataset) -> None:
    dataset.facts.append(
        fact("f-00016", "cilova_velikost_fondu", "150000000", "src-0002", currency="EUR", fund_name="Fiktivní Fond IV")
    )
    dataset.funds.append(
        fund("fd-0005", "Fiktivní Fond IV", "f-00016", amount="150000000", currency="EUR", amount_type="cil", approx="ne")
    )


def test_target_is_never_added_to_raised_capital(dataset: Dataset) -> None:
    add_target_fund(dataset)
    add_fund_count(dataset, "2")

    summary = investor_capital(dataset)[0]

    assert summary.raised == {"EUR": Decimal("30000000")}
    assert summary.targets == {"EUR": Decimal("150000000")}
    assert summary.lower_bound


def test_investor_with_only_target_has_unknown_raised_capital(dataset: Dataset) -> None:
    dataset.funds.clear()
    add_target_fund(dataset)

    summary = investor_capital(dataset)[0]
    completeness = requirement_completeness(dataset)

    assert summary.raised == {}
    assert summary.targets == {"EUR": Decimal("150000000")}
    assert not summary.lower_bound
    assert completeness.target_only.numerator == 1


def test_invested_amount_is_shown_separately(dataset: Dataset) -> None:
    add_invested(dataset)

    summary = investor_capital(dataset)[0]

    assert summary.raised == {"EUR": Decimal("30000000")}
    assert summary.invested == {"CZK": Decimal("12000000")}


def test_raised_capital_is_lower_bound_without_documented_fund_count(dataset: Dataset) -> None:
    summary = investor_capital(dataset)[0]

    assert summary.raised == {"EUR": Decimal("30000000")}
    assert summary.documented_fund_count is None
    assert summary.lower_bound


def test_exact_raised_capital_of_all_documented_funds_is_not_lower_bound(dataset: Dataset) -> None:
    add_fund_count(dataset, "1")

    summary = investor_capital(dataset)[0]

    assert summary.documented_fund_count == 1
    assert not summary.lower_bound


def test_report_contains_requirement_and_capital_sections(dataset: Dataset) -> None:
    report = render_report(dataset, TODAY)

    assert "## Úplnost podle požadavků zadání" in report
    assert "| Fiktivní Ventures | 1 (1) / – | final_close | 30 000 000 EUR (dolní mez) | – | – | – | – |" in report


def test_first_close_is_always_lower_bound(dataset: Dataset) -> None:
    dataset.funds.clear()
    add_approximate_first_close(dataset)
    dataset.funds[0].update(approx="ne", amount_wording="")
    add_fund_count(dataset, "1")

    assert investor_capital(dataset)[0].lower_bound


@pytest.mark.parametrize(
    ("column", "value"),
    [("fundraising_open", "ano"), ("conflict_note", "měna: zdroj A uvádí EUR, zdroj B USD")],
)
def test_open_fundraising_or_conflict_makes_raised_capital_lower_bound(dataset: Dataset, column: str, value: str) -> None:
    add_fund_count(dataset, "1")
    dataset.funds[0][column] = value

    assert investor_capital(dataset)[0].lower_bound


def test_report_shows_lp_commitment_part_and_conflict(dataset: Dataset) -> None:
    dataset.facts.append(
        fact("f-00013", "fond_zavazek_lp", "94000000", "src-0002", currency="EUR", fund_name="Fiktivní Fond III")
    )
    dataset.funds.append(
        fund("fd-0003", "Fiktivní Fond III", "f-00013", amount="94000000", currency="EUR", amount_type="zavazek_jednoho_lp", approx="ne")
    )
    dataset.funds[0]["conflict_note"] = "měna sporná"

    report = render_report(dataset, TODAY)

    assert "124 000 000 EUR (dolní mez; z toho závazek jednoho LP 94 000 000 EUR)" in report
    assert "**KONFLIKT** Fiktivní Fond I: měna sporná" in report


def test_investor_level_invested_capital_points_to_its_fact(dataset: Dataset) -> None:
    dataset.investors[0]["invested_capital"] = "5000000"
    dataset.facts.append(fact("f-00017", "invested_capital", "5000000", "src-0002", currency="EUR"))

    summary = investor_capital(dataset)[0]

    assert summary.invested == {"EUR": Decimal("5000000")}
    assert summary.invested_fact_id == "f-00017"


def add_invested_in_period(dataset: Dataset) -> None:
    dataset.facts.append(fact("f-00018", "fond_investovano_za_obdobi", "30000000", "src-0002", currency="CZK", fund_name=FUND_NAME))
    dataset.funds.append(
        fund(
            "fd-0005",
            FUND_NAME,
            "f-00018",
            amount="30000000",
            currency="CZK",
            amount_type="investovano_za_obdobi",
            approx="ne",
            amount_wording="během minulého roku",
        )
    )


def test_amount_invested_in_period_is_shown_as_lower_bound_of_invested_capital(dataset: Dataset) -> None:
    add_invested_in_period(dataset)

    summary = investor_capital(dataset)[0]
    report = render_report(dataset, TODAY)

    assert validate_dataset(dataset, TODAY) == []
    assert summary.invested == {"CZK": Decimal("30000000")}
    assert summary.invested_period_fact_ids == ("f-00018",)
    assert "30 000 000 CZK (dolní mez: jen investice za období, formulace ve faktu f-00018)" in report


def test_fund_may_not_have_two_invested_amounts(dataset: Dataset) -> None:
    add_invested(dataset)
    add_invested_in_period(dataset)

    assert_reported(dataset, "je zapsán s investovanou částkou vícekrát")


def test_announced_fund_size_is_not_capital(dataset: Dataset) -> None:
    dataset.funds.clear()
    dataset.facts.append(
        fact("f-00019", "oznamena_velikost_fondu", "40000000", "src-0002", currency="EUR", fund_name=FUND_NAME)
    )
    dataset.funds.append(fund("fd-0006", FUND_NAME, "f-00019"))

    summary = investor_capital(dataset)[0]

    assert validate_dataset(dataset, TODAY) == []
    assert summary.raised == {}
    assert not requirement_completeness(dataset).filled["kapital"].numerator
