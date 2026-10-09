from datetime import date

import pytest
from conftest import TODAY, fact

from investor_db.io import Dataset
from investor_db.metrics import (
    Proportion,
    cohen_kappa,
    fact_accuracy,
    field_completeness,
    freshness_share,
    investment_activity_share,
    precision,
    primary_fact_share,
    primary_registry_share,
    reviewer_agreement,
    values_only_in_facts_due_to_currency,
)
from investor_db.report import render_report


def review(investor_id: str, reviewer: str, verdict: str) -> dict[str, str]:
    return {"investor_id": investor_id, "reviewer": reviewer, "reviewed_at": "2026-10-05", "verdict": verdict, "note": ""}


def test_wilson_interval_matches_reference_values() -> None:
    low, high = Proportion(8, 10).wilson_interval() or (0, 0)

    assert (round(low, 4), round(high, 4)) == (0.4902, 0.9433)


def test_empty_proportion_has_no_value_or_interval() -> None:
    assert Proportion(0, 0).value is None and Proportion(0, 0).wilson_interval() is None


def test_precision_counts_only_verified_investors(dataset: Dataset) -> None:
    dataset.reviews.append(review("inv-0002", "R1", "FP"))

    result = precision(dataset)

    assert (result.true_positives, result.false_positives, result.unsure) == (1, 0, 0)


def test_precision_reports_unsure_separately_and_pessimistically(dataset: Dataset) -> None:
    dataset.investors[1].update(dataset.investors[0], investor_id="inv-0002")
    dataset.investors.append(dict(dataset.investors[0], investor_id="inv-0004"))
    dataset.reviews += [review("inv-0002", "R1", "FP"), review("inv-0004", "R1", "nejiste")]

    result = precision(dataset)

    assert result.strict == Proportion(1, 2)
    assert result.pessimistic == Proportion(1, 3)


def test_precision_ignores_pending_reviews(dataset: Dataset) -> None:
    dataset.reviews[0]["verdict"] = ""

    assert precision(dataset).strict == Proportion(0, 0)


def test_cohen_kappa_reference_value() -> None:
    pairs = [("TP", "TP"), ("TP", "FP"), ("FP", "FP"), ("TP", "TP")]

    assert cohen_kappa(pairs) == pytest.approx(0.5)


def test_cohen_kappa_is_undefined_when_both_use_single_category() -> None:
    assert cohen_kappa([("TP", "TP"), ("TP", "TP")]) is None


def test_agreement_is_absent_without_second_reviewer(dataset: Dataset) -> None:
    assert reviewer_agreement(dataset) is None


def test_agreement_reports_percent_and_kappa(dataset: Dataset) -> None:
    dataset.reviews.append(review("inv-0001", "R2", "FP"))

    result = reviewer_agreement(dataset)

    assert result is not None
    assert result.agreement == Proportion(0, 1)
    assert result.kappa == pytest.approx(0.0)


def test_fact_accuracy_separates_unverifiable(dataset: Dataset) -> None:
    dataset.fact_reviews += [
        {"fact_id": "f-00002", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "chybne", "note": ""},
        {"fact_id": "f-00003", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "nelze_overit", "note": ""},
    ]

    result = fact_accuracy(dataset)

    assert result.accuracy == Proportion(1, 2)
    assert result.unverifiable == 1


def test_field_completeness_counts_verified_investors_only(dataset: Dataset) -> None:
    completeness = field_completeness(dataset.investors)

    assert completeness["total_fund_size"] == Proportion(1, 1)
    assert completeness["assets_under_management"] == Proportion(0, 1)


def test_primary_source_shares(dataset: Dataset) -> None:
    assert primary_registry_share(dataset) == Proportion(1, 1)
    assert primary_fact_share(dataset) == Proportion(9, 10)


@pytest.mark.parametrize(("today", "expected"), [(TODAY, Proportion(1, 1)), (date(2029, 1, 1), Proportion(0, 1))])
def test_investment_activity_share(dataset: Dataset, today: date, expected: Proportion) -> None:
    assert investment_activity_share(dataset, today) == expected


@pytest.mark.parametrize(("today", "expected"), [(TODAY, Proportion(1, 1)), (date(2028, 1, 1), Proportion(0, 1))])
def test_freshness_share(dataset: Dataset, today: date, expected: Proportion) -> None:
    assert freshness_share(dataset.investors, today) == expected


@pytest.mark.parametrize(("currency", "expected"), [("CZK", 1), ("EUR", 0)])
def test_values_only_in_facts_due_to_currency(dataset: Dataset, currency: str, expected: int) -> None:
    dataset.facts.append(fact("f-00011", "assets_under_management", "900000000", "src-0002", currency=currency))

    assert values_only_in_facts_due_to_currency(dataset) == expected


def test_report_contains_all_sections(dataset: Dataset) -> None:
    report = render_report(dataset, TODAY)

    for heading in ("Stav záznamů", "Precision", "Shoda hodnotitelů", "Přesnost faktů", "Úplnost polí", "Omezení dat"):
        assert heading in report
    assert "Data R2 nejsou k dispozici" in report


def test_report_handles_empty_dataset() -> None:
    report = render_report(Dataset(), TODAY)

    assert "Ruční kontrola R1 zatím není vyplněna." in report
