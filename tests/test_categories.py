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
