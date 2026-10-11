from datetime import date
from decimal import Decimal

import pytest
from conftest import TODAY, fact

from investor_db.io import Dataset
from investor_db.metrics import (
    Proportion,
    PopulationEstimate,
    cohen_kappa,
    funnel,
    population_estimates,
    review_efforts,
    effort_summaries,
    search_minutes,
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
    return {"investor_id": investor_id, "reviewer": reviewer, "reviewed_at": "2026-10-05", "verdict": verdict, "review_minutes": "", "note": ""}


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
        fact_review("f-00002", "chybne", "vzorek"),
        fact_review("f-00003", "nelze_overit", "vzorek"),
    ]

    result = fact_accuracy(dataset)

    assert result.accuracy == Proportion(1, 2)
    assert result.unverifiable == 1


def fact_review(fact_id: str, verdict: str, review_round: str) -> dict[str, str]:
    return {
        "fact_id": fact_id,
        "reviewer": "R1",
        "reviewed_at": "2026-10-05",
        "verdict": verdict,
        "review_minutes": "",
        "note": "",
        "review_round": review_round,
    }


def test_fact_accuracy_is_reported_per_review_round(dataset: Dataset) -> None:
    dataset.fact_reviews += [
        fact_review("f-00002", "chybne", "po_doplneni"),
        fact_review("f-00003", "chybne", "po_doplneni"),
        fact_review("f-00004", "spravne", "po_doplneni"),
    ]

    assert fact_accuracy(dataset, "R1", "vzorek").accuracy == Proportion(1, 1)
    assert fact_accuracy(dataset, "R1", "po_doplneni").accuracy == Proportion(1, 3)


def test_field_completeness_counts_verified_investors_only(dataset: Dataset) -> None:
    completeness = field_completeness(dataset.investors)

    assert completeness["total_fund_size"] == Proportion(1, 1)
    assert completeness["assets_under_management"] == Proportion(0, 1)


def test_primary_source_shares(dataset: Dataset) -> None:
    assert primary_registry_share(dataset) == Proportion(1, 1)
    assert primary_fact_share(dataset) == Proportion(9, 11)


@pytest.mark.parametrize(("today", "expected"), [(TODAY, Proportion(1, 1)), (date(2029, 1, 1), Proportion(0, 1))])
def test_investment_activity_share(dataset: Dataset, today: date, expected: Proportion) -> None:
    assert investment_activity_share(dataset, today) == expected


@pytest.mark.parametrize(("today", "expected"), [(TODAY, Proportion(1, 1)), (date(2028, 1, 1), Proportion(0, 1))])
def test_freshness_share(dataset: Dataset, today: date, expected: Proportion) -> None:
    assert freshness_share(dataset.investors, today) == expected


@pytest.mark.parametrize(("currency", "expected"), [("CZK", 1), ("EUR", 0)])
def test_values_only_in_facts_due_to_currency(dataset: Dataset, currency: str, expected: int) -> None:
    dataset.facts.append(fact("f-00012", "assets_under_management", "900000000", "src-0002", currency=currency))

    assert values_only_in_facts_due_to_currency(dataset) == expected


def test_report_contains_all_sections(dataset: Dataset) -> None:
    report = render_report(dataset, TODAY)

    for heading in ("Stav záznamů", "Trychtýř", "Precision", "Shoda hodnotitelů", "Přesnost faktů", "Úplnost polí", "Pracnost", "capture–recapture", "Omezení dat"):
        assert heading in report
    assert "Data R2 nejsou k dispozici" in report


def test_report_handles_empty_dataset() -> None:
    report = render_report(Dataset(), TODAY)

    assert "Ruční kontrola R1 zatím není vyplněna." in report


def test_effort_summaries_sum_minutes_per_investor(dataset: Dataset) -> None:
    summaries = {(summary.activity, summary.actor): summary for summary in effort_summaries(dataset.effort_log)}

    verification = summaries[("overeni", "model")]
    assert verification.minutes_per_investor == (15,)
    assert summaries[("triaz", "model")].total_minutes == 4


def test_effort_mean_and_median_across_investors(dataset: Dataset) -> None:
    dataset.effort_log.append(dict(dataset.effort_log[2], investor_id="inv-0002", minutes="10"))
    dataset.effort_log.append(dict(dataset.effort_log[2], investor_id="inv-0001", minutes="1"))

    triage = next(summary for summary in effort_summaries(dataset.effort_log) if summary.activity == "triaz")

    assert triage.minutes_per_investor == (1, 4, 10)
    assert triage.mean_minutes == 5 and triage.median_minutes == 4


def test_search_minutes(dataset: Dataset) -> None:
    assert search_minutes(dataset.search_log) == 15


def test_population_estimate_reference_values() -> None:
    estimate = PopulationEstimate("s-001", "s-002", first_count=27, second_count=16, overlap=5)

    assert estimate.observed == 38
    assert estimate.lincoln_petersen == pytest.approx(86.4)
    assert estimate.chapman == pytest.approx(476 / 6 - 1)
    assert estimate.chapman_interval()[0] >= estimate.observed


def test_lincoln_petersen_is_undefined_without_overlap() -> None:
    assert PopulationEstimate("s-001", "s-002", 3, 4, 0).lincoln_petersen is None


def test_population_estimates_use_pairs_of_searches(dataset: Dataset) -> None:
    dataset.search_log.append(dict(dataset.search_log[0], search_id="s-002"))
    dataset.candidate_sources += [
        {"investor_id": "inv-0001", "search_id": "s-002"},
        {"investor_id": "inv-0002", "search_id": "s-002"},
    ]

    verified_only = population_estimates(dataset, ("overeny",), min_search_size=1)
    with_candidates = population_estimates(dataset, ("overeny", "kandidat"), min_search_size=1)

    assert [(item.first_count, item.second_count, item.overlap) for item in verified_only] == [(1, 1, 1)]
    assert [(item.first_count, item.second_count, item.overlap) for item in with_candidates] == [(2, 2, 2)]


def test_funnel_groups_by_processing_level(dataset: Dataset) -> None:
    dataset.effort_log = [row for row in dataset.effort_log if row["investor_id"] != "inv-0002"]

    stages = funnel(dataset)

    assert stages["overeni"] == {"overeny": 1}
    assert stages["triaz"] == {"vyloucen": 1}
    assert stages[""] == {"kandidat": 1}


def test_review_efforts_count_only_completed_reviews(dataset: Dataset) -> None:
    dataset.reviews.append(review("inv-0002", "R1", ""))

    efforts = review_efforts(dataset.reviews)

    assert [(item.reviewer, item.reviews, item.timed_reviews, item.total_minutes) for item in efforts] == [
        ("R1", 1, 1, 20)
    ]


def test_population_estimates_skip_small_searches(dataset: Dataset) -> None:
    dataset.search_log.append(dict(dataset.search_log[0], search_id="s-002"))
    dataset.candidate_sources.append({"investor_id": "inv-0001", "search_id": "s-002"})

    assert population_estimates(dataset, ("overeny", "kandidat"), min_search_size=2) == []


def test_effort_summaries_sum_decimal_minutes(dataset: Dataset) -> None:
    dataset.effort_log[0]["minutes"] = "0.25"
    dataset.effort_log[1]["minutes"] = "0.5"

    verification = next(item for item in effort_summaries(dataset.effort_log) if item.activity == "overeni")

    assert verification.minutes_per_investor == (Decimal("0.75"),)


def test_search_minutes_accepts_decimals(dataset: Dataset) -> None:
    dataset.search_log[0]["minutes"] = "0.48"

    assert search_minutes(dataset.search_log) == Decimal("0.48")
