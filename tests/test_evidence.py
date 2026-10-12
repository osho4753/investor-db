import re
from dataclasses import replace
from pathlib import Path

from conftest import build_valid_dataset, fact
from test_cli import write_dataset

from investor_db.__main__ import DEFAULT_INVESTOR_CHECKLIST_PATH, main
from investor_db.evidence import fund_evidence, latest_activity, verified_evidence
from investor_db.io import load_dataset
from investor_db.review_guide import REVIEW_BLANKS, render_investor_checklist
from investor_db.schema import AGGREGATOR_NAMES

ROOT = Path(__file__).resolve().parents[1]


def test_fund_evidence_prefers_amount_over_manager() -> None:
    facts = build_valid_dataset().facts

    assert fund_evidence(facts)["fact_id"] == "f-00008"


def test_latest_activity_prefers_newest_investment() -> None:
    facts = [*build_valid_dataset().facts, fact("f-00012", "dolozena_investice", "Novější s.r.o.", "src-0003", value_as_of="2026-01-10")]

    assert latest_activity(facts)["fact_id"] == "f-00012"


def test_latest_activity_falls_back_to_fund_without_investment() -> None:
    facts = [row for row in build_valid_dataset().facts if row["field"] != "dolozena_investice"]

    assert latest_activity(facts)["fact_id"] == "f-00008"


def test_verified_evidence_covers_only_verified_investors() -> None:
    evidence = verified_evidence(build_valid_dataset())

    assert [item.investor["investor_id"] for item in evidence] == ["inv-0001"]
    assert evidence[0].registry_fact["fact_id"] == "f-00001"
    assert evidence[0].is_investment


def test_investor_checklist_has_links_and_empty_blanks() -> None:
    checklist = render_investor_checklist(build_valid_dataset())

    assert "## 1. Fiktivní Ventures (`inv-0001`)" in checklist
    assert "IČO 12345679" in checklist
    assert "Fakt `f-00008`" in checklist
    assert "Fakt `f-00009`" in checklist
    assert checklist.count("| Verdikt (`TP` / `FP` / `nejiste`) | |") == 1
    assert all(line in checklist for line in REVIEW_BLANKS)


def test_investor_checklist_marks_missing_investment() -> None:
    dataset = build_valid_dataset()
    dataset = replace(dataset, facts=[row for row in dataset.facts if row["field"] != "dolozena_investice"])

    assert "Nejnovější doložený fond (Z4, investice chybí)" in render_investor_checklist(dataset)


def test_cli_writes_investor_checklist(tmp_path: Path) -> None:
    write_dataset(tmp_path, build_valid_dataset())
    output = tmp_path / "list.md"

    assert main(["--data-dir", str(tmp_path), "investor-review-guide", "--output", str(output)]) == 0
    assert output.read_text(encoding="utf-8").startswith("# Kontrolní list R1-v2")


def test_committed_investor_checklist_is_current_and_unfilled() -> None:
    dataset = load_dataset(ROOT / "data")
    committed = (ROOT / DEFAULT_INVESTOR_CHECKLIST_PATH).read_text(encoding="utf-8")

    assert committed == render_investor_checklist(dataset)
    assert committed.count("| Verdikt (`TP` / `FP` / `nejiste`) | |") == len(verified_evidence(dataset))
    urls = re.findall(r"<(https?://[^>]+)>", committed)
    assert urls
    assert not [url for url in urls if any(name in url.lower() for name in (*AGGREGATOR_NAMES, "linkedin"))]


def test_registry_link_points_to_ares_even_when_website_fact_comes_first() -> None:
    dataset = build_valid_dataset()
    website_source = {"source_id": "src-0009", "url": "https://fiktivni-ventures.example.com/kontakt", "publisher": "Fiktivní Ventures", "source_type": "web_investora"}
    website_fact = fact("f-00000", "registry_id", "12345679", "src-0009")
    dataset = replace(dataset, facts=[website_fact, *dataset.facts], sources=[*dataset.sources, website_source])

    checklist = render_investor_checklist(dataset)

    assert verified_evidence(dataset)[0].registry_fact["fact_id"] == "f-00001"
    assert "ARES: <https://ares.gov.cz/" in checklist
    assert "ARES: <https://fiktivni-ventures" not in checklist


def test_committed_checklist_ares_links_point_to_ares() -> None:
    committed = (ROOT / DEFAULT_INVESTOR_CHECKLIST_PATH).read_text(encoding="utf-8")
    links = re.findall(r"ARES: <([^>]+)>", committed)

    assert len(links) == 16
    assert all(link.startswith("https://ares.gov.cz/") for link in links)
