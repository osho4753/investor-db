from pathlib import Path

import pytest
from conftest import build_valid_dataset, fact
from test_cli import write_dataset

from investor_db.__main__ import main
from investor_db.review_guide import (
    EXCLUSION_GUIDES,
    FIELD_GUIDES,
    GuideTemplateError,
    build_fact_guide,
    build_fact_guides,
    format_money,
    missing_templates,
    render_checklist,
)
from investor_db.schema import EXCLUSION_REASONS, FACT_EXCLUSION_REASON, FACT_FIELDS, MONEY_FACT_FIELDS

INVESTOR = {"investor_id": "inv-0001", "name": "Fiktivní Ventures", "verification_status": "overeny"}
MEDIA_SOURCE = {"source_id": "src-0001", "url": "https://zpravy.example.net/a", "publisher": "Fiktivní zprávy", "source_type": "media"}
ARES_SOURCE = {
    "source_id": "src-0002",
    "url": "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/12345679",
    "publisher": "ARES",
    "source_type": "rejstrik",
}


def sample_value(field: str) -> dict[str, str]:
    if field in MONEY_FACT_FIELDS:
        return {"value": "22000000", "currency": "EUR"}
    if field == "investment_sectors":
        return {"value": "ai;fintech"}
    if field == "investment_stages":
        return {"value": "seed;serie_a"}
    return {"value": "Fiktivní hodnota"}


def guide_for(field: str, **overrides: str):
    values = sample_value(field) | overrides
    row = fact("f-00001", field, values.pop("value"), "src-0001", fund_name="Fiktivní Fond I", **values)
    return build_fact_guide(row, INVESTOR, MEDIA_SOURCE)


def test_every_field_reason_and_label_has_template() -> None:
    assert missing_templates() == []


@pytest.mark.parametrize("field", [field for field in FACT_FIELDS if field != FACT_EXCLUSION_REASON])
def test_every_field_produces_complete_text(field: str) -> None:
    guide = guide_for(field)

    assert guide.claim and guide.look_for
    assert "{" not in guide.claim + guide.look_for
    assert guide.claim == guide_for(field).claim


@pytest.mark.parametrize("reason", EXCLUSION_REASONS)
def test_every_exclusion_reason_has_its_own_text(reason: str) -> None:
    guide = guide_for(FACT_EXCLUSION_REASON, value=reason)

    assert "Fiktivní Ventures" in guide.claim
    assert guide.claim == EXCLUSION_GUIDES[reason].claim.format(investor="Fiktivní Ventures")


def test_exclusion_texts_differ_between_reasons() -> None:
    claims = [guide.claim for guide in EXCLUSION_GUIDES.values()]

    assert len(set(claims)) == len(claims)


def test_unknown_field_is_an_error() -> None:
    with pytest.raises(GuideTemplateError, match="nemá šablonu"):
        guide_for("neznamy_typ")


def test_unknown_exclusion_reason_is_an_error() -> None:
    with pytest.raises(GuideTemplateError, match="nemá šablonu"):
        guide_for(FACT_EXCLUSION_REASON, value="jiny_duvod")


def test_unknown_list_code_is_an_error() -> None:
    with pytest.raises(GuideTemplateError, match="nemá popis"):
        guide_for("investment_sectors", value="ai;vesmir")


def test_money_claim_names_amount_currency_and_fund() -> None:
    guide = guide_for("total_fund_size", value_as_of="2023-12-22")

    assert guide.claim == (
        "Fond „Fiktivní Fond I“ investora Fiktivní Ventures byl uzavřen s konečnou velikostí "
        "22 000 000 EUR (stav k 22. 12. 2023)."
    )
    assert "cílovou velikost" in guide.look_for and "22 000 000 EUR" in guide.look_for


def test_format_money_keeps_decimals() -> None:
    assert format_money("2500000.5", "CZK") == "2 500 000,5 CZK"


def test_list_codes_are_translated() -> None:
    assert guide_for("investment_stages").claim == "Fiktivní Ventures investuje v těchto fázích: seed, série A."


def test_month_precision_hint_for_first_day_of_month() -> None:
    assert "přesností na měsíc" in guide_for("dolozena_investice", value_as_of="2026-04-01").look_for
    assert "přesností na měsíc" not in guide_for("dolozena_investice", value_as_of="2026-04-02").look_for


def test_ares_source_gets_json_hint() -> None:
    row = fact("f-00001", "registry_id", "12345679", "src-0002")
    guide = build_fact_guide(row, INVESTOR, ARES_SOURCE)

    assert guide.claim == "Fiktivní Ventures má českou právnickou osobu s IČO 12345679."
    assert "JSON" in guide.look_for
    assert guide.source_label == "veřejný rejstřík (primární), vydavatel: ARES"


def test_checklist_covers_sample_without_evidence_note() -> None:
    dataset = build_valid_dataset()
    dataset.fact_reviews = [
        {"fact_id": row["fact_id"], "reviewer": "R1", "review_round": "vzorek"} for row in dataset.facts[:3]
    ]
    fact_ids = sorted(row["fact_id"] for row in dataset.facts[:3])

    checklist = render_checklist(dataset)

    assert [guide.fact_id for guide in build_fact_guides(dataset, fact_ids)] == fact_ids
    assert "Fiktivní testovací důkaz" not in checklist
    assert checklist == render_checklist(dataset)


def test_checklist_lists_review_rounds_separately() -> None:
    dataset = build_valid_dataset()
    dataset.fact_reviews = [
        {"fact_id": "f-00001", "reviewer": "R1", "review_round": "vzorek"},
        {"fact_id": "f-00002", "reviewer": "R1", "review_round": "po_doplneni"},
        {"fact_id": "f-00003", "reviewer": "R1", "review_round": "po_doplneni"},
        {"fact_id": "f-00003", "reviewer": "R1", "review_round": "po_oprave"},
    ]

    checklist = render_checklist(dataset)

    assert "ve 3 kolech" not in checklist and "v 3 kolech" in checklist
    assert "# Kontrola po opravě – fakty změněné po kontrole (1 faktů)" in checklist
    assert "# Původní kontrola – náhodný vzorek (1 faktů)" in checklist
    assert "# Kontrola po doplnění – všechny nové fakty (2 faktů)" in checklist
    assert checklist.index("`f-00001`") < checklist.index("## 2. `f-00002`")


def test_cli_writes_checklist(tmp_path: Path) -> None:
    dataset = build_valid_dataset()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    write_dataset(data_dir, dataset)
    output = tmp_path / "review" / "kontrolni-list-faktu.md"

    assert main(["--data-dir", str(data_dir), "review-guide", "--output", str(output)]) == 0
    assert output.read_text(encoding="utf-8").startswith("# Kontrolní list faktů")


def test_field_guides_cover_only_known_fields() -> None:
    assert set(FIELD_GUIDES) <= set(FACT_FIELDS)


def test_debt_fund_reason_names_venture_debt() -> None:
    assert "venture debt" in guide_for(FACT_EXCLUSION_REASON, value="dluhovy_fond").claim
