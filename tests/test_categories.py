import pytest
from conftest import TODAY, fact

from investor_db.io import Dataset, Row
from investor_db.metrics import precision
from investor_db.report import render_report
from investor_db.validation import validate_dataset


def messages(dataset: Dataset) -> list[str]:
    return [issue.message for issue in validate_dataset(dataset, TODAY)]


def assessment(status: str = "overeny", reason: str = "") -> Row:
    return {
        "investor_id": "inv-0003",
        "category": "pe",
        "verification_status": status,
        "exclusion_reason": reason,
        "last_verified_at": "2026-10-01",
        "note": "",
    }


def make_pe_candidate(dataset: Dataset) -> None:
    investor = dataset.investors[2]
    investor.update(investor_type="pe", registry_id="27590003", country="CZ")
    dataset.facts += [
        fact("f-00012", "registry_id", "27590003", "src-0001", investor_id="inv-0003"),
        fact("f-00013", "informace_o_fondu", "fond PE", "src-0002", investor_id="inv-0003", fund_name="PE Fond I", value_as_of="2025-06-30"),
    ]
    investor["evidence_urls"] = ";".join(sorted({row["url"] for row in dataset.sources}))


def test_verified_pe_assessment_is_valid_and_keeps_vc_status(dataset: Dataset) -> None:
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment())

    assert messages(dataset) == []
    assert dataset.investors[2]["verification_status"] == "vyloucen"


@pytest.mark.parametrize(
    ("field_to_drop", "fragment"),
    [("informace_o_fondu", "kritérium P3"), ("registry_id", "kritérium P1")],
)
def test_verified_pe_assessment_requires_criteria(dataset: Dataset, field_to_drop: str, fragment: str) -> None:
    make_pe_candidate(dataset)
    dataset.facts = [row for row in dataset.facts if not (row["investor_id"] == "inv-0003" and row["field"] == field_to_drop)]
    dataset.investors[2]["evidence_urls"] = ";".join(
        sorted({source["url"] for row in dataset.facts if row["investor_id"] == "inv-0003" for source in dataset.sources if source["source_id"] == row["source_id"]})
    )
    dataset.category_assessments.append(assessment())

    assert any(fragment in message for message in messages(dataset)), messages(dataset)


def test_assessment_category_must_match_investor_type(dataset: Dataset) -> None:
    dataset.category_assessments.append(assessment(status="kandidat"))

    assert any("investor_type investora se neshoduje" in message for message in messages(dataset))


def test_excluded_assessment_needs_documented_reason(dataset: Dataset) -> None:
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment(status="vyloucen", reason="vc_ne_pe"))

    assert any("'vc_ne_pe' není doložen" in message for message in messages(dataset))


def test_precision_is_computed_per_category(dataset: Dataset) -> None:
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment())
    dataset.reviews.append(
        {"investor_id": "inv-0003", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "FP", "review_minutes": "5", "note": "", "category": "pe"}
    )

    assert precision(dataset, "R1").false_positives == 0
    assert precision(dataset, "R1", "pe").false_positives == 1


def test_report_shows_category_section_separately(dataset: Dataset) -> None:
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment())

    report = render_report(dataset, TODAY)

    assert "### Private equity (mini-pilot)" in report
    assert "- Posouzeno: 1; overeny 1, kandidat 0, vyloucen 0" in report


def test_category_facts_do_not_change_vc_pilot_fact_share(dataset: Dataset) -> None:
    before = render_report(dataset, TODAY)
    vc_line = next(line for line in before.splitlines() if line.startswith("- Fakta z primárních zdrojů (VC pilot)"))
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment())

    after = render_report(dataset, TODAY)

    assert vc_line in after


def test_foreign_investor_counts_as_authentic_but_outside_pilot_country(dataset: Dataset) -> None:
    make_pe_candidate(dataset)
    dataset.category_assessments.append(assessment())
    dataset.investors.append(dict(dataset.investors[2], investor_id="inv-0004", registry_id="", country="PL"))
    dataset.facts.append(fact("f-00020", "duvod_vylouceni", "zahranicni_subjekt", "src-0003", investor_id="inv-0004"))
    dataset.investors[-1]["evidence_urls"] = "https://zpravy.example.net/fiktivni-investice"
    dataset.category_assessments.append(dict(assessment("vyloucen", "zahranicni_subjekt"), investor_id="inv-0004"))
    dataset.reviews.append(
        {"investor_id": "inv-0004", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "TP", "review_minutes": "5", "note": "", "category": "pe"}
    )

    report = render_report(dataset, TODAY)

    assert "- Ověřená pravost (skutečný investor kategorie, i mimo zemi pilotu): 2/2" in report
    assert "- V rámci země pilotu (česká právnická osoba, status `overeny`): 1/2" in report
    assert "- Kontrola R1 u statusu `vyloucen`: TP 1 (z 1)" in report


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("investment_sectors", "sluzby_firmam;zdravotnictvi;vzdelavani;financni_sluzby;maloobchod;stavebnictvi;tmt;potravinarstvi"),
        ("investment_stages", "buyout;growth_equity"),
    ],
)
def test_pe_vocabulary_codes_are_valid(dataset: Dataset, column: str, value: str) -> None:
    make_pe_candidate(dataset)
    dataset.investors[2][column] = value
    dataset.facts.append(fact("f-00021", column, value, "src-0002", investor_id="inv-0003"))
    dataset.category_assessments.append(assessment())

    assert messages(dataset) == []


def test_unknown_pe_stage_is_reported(dataset: Dataset) -> None:
    dataset.investors[0]["investment_stages"] = "seed;mbo"

    assert any("mbo" in message for message in messages(dataset))
