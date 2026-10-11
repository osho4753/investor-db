from datetime import date

import pytest

from investor_db.io import Dataset, Row
from investor_db.schema import FACT_COLUMNS

TODAY = date(2026, 10, 9)

FUND_NAME = "Fiktivní Fond I"
REGISTRY_URL = "https://rejstrik.example.org/subjekt/12345679"
INVESTOR_URL = "https://fiktivni-ventures.example.com/fond"
MEDIA_URL = "https://zpravy.example.net/fiktivni-investice"


def fact(fact_id: str, field: str, value: str, source_id: str, **overrides: str) -> Row:
    row = dict.fromkeys(FACT_COLUMNS, "")
    row.update(
        fact_id=fact_id,
        investor_id="inv-0001",
        field=field,
        value=value,
        source_id=source_id,
        accessed_at="2026-09-30",
        evidence_note="Fiktivní testovací důkaz.",
    )
    row.update(overrides)
    return row


def build_valid_dataset() -> Dataset:
    return Dataset(
        investors=[
            {
                "investor_id": "inv-0001",
                "name": "Fiktivní Ventures",
                "investor_type": "vc",
                "country": "CZ",
                "registry_id": "12345679",
                "website": "https://fiktivni-ventures.example.com",
                "investment_sectors": "software;fintech",
                "investment_stages": "seed;serie_a",
                "typical_ticket_min": "500000",
                "typical_ticket_max": "2000000",
                "currency": "EUR",
                "total_fund_size": "30000000",
                "assets_under_management": "",
                "invested_capital": "",
                "verification_status": "overeny",
                "exclusion_reason": "",
                "evidence_urls": ";".join(sorted([REGISTRY_URL, INVESTOR_URL, MEDIA_URL])),
                "last_verified_at": "2026-10-01",
            },
            {
                "investor_id": "inv-0002",
                "name": "Jiný Fiktivní Kapitál",
                "investor_type": "vc",
                "country": "CZ",
                "registry_id": "",
                "website": "",
                "investment_sectors": "",
                "investment_stages": "",
                "typical_ticket_min": "",
                "typical_ticket_max": "",
                "currency": "",
                "total_fund_size": "",
                "assets_under_management": "",
                "invested_capital": "",
                "verification_status": "kandidat",
                "exclusion_reason": "",
                "evidence_urls": "",
                "last_verified_at": "",
            },
            {
                "investor_id": "inv-0003",
                "name": "Fiktivní Anděl",
                "investor_type": "business_angel",
                "country": "CZ",
                "registry_id": "",
                "website": "",
                "investment_sectors": "",
                "investment_stages": "",
                "typical_ticket_min": "",
                "typical_ticket_max": "",
                "currency": "",
                "total_fund_size": "",
                "assets_under_management": "",
                "invested_capital": "",
                "verification_status": "vyloucen",
                "exclusion_reason": "business_angel",
                "evidence_urls": MEDIA_URL,
                "last_verified_at": "",
            },
        ],
        facts=[
            fact("f-00001", "registry_id", "12345679", "src-0001"),
            fact("f-00002", "name", "Fiktivní Ventures", "src-0002"),
            fact("f-00003", "website", "https://fiktivni-ventures.example.com", "src-0002"),
            fact("f-00004", "investment_sectors", "software;fintech", "src-0002"),
            fact("f-00005", "investment_stages", "seed;serie_a", "src-0002"),
            fact("f-00006", "typical_ticket_min", "500000", "src-0002", currency="EUR"),
            fact("f-00007", "typical_ticket_max", "2000000", "src-0002", currency="EUR"),
            fact(
                "f-00008",
                "total_fund_size",
                "30000000",
                "src-0002",
                currency="EUR",
                fund_name=FUND_NAME,
                value_as_of="2025-06-30",
            ),
            fact("f-00009", "dolozena_investice", "Fiktivní Startup s.r.o.", "src-0003", value_as_of="2025-11-15"),
            fact("f-00010", "pravni_spravce", "Fiktivní Správce a.s.", "src-0002", fund_name=FUND_NAME),
            fact("f-00011", "duvod_vylouceni", "business_angel", "src-0003", investor_id="inv-0003"),
        ],
        sources=[
            {"source_id": "src-0001", "url": REGISTRY_URL, "publisher": "Fiktivní rejstřík", "source_type": "rejstrik"},
            {"source_id": "src-0002", "url": INVESTOR_URL, "publisher": "Fiktivní Ventures", "source_type": "web_investora"},
            {"source_id": "src-0003", "url": MEDIA_URL, "publisher": "Fiktivní zprávy", "source_type": "media"},
        ],
        search_log=[
            {
                "search_id": "s-001",
                "searched_at": "2026-09-29",
                "source_url": "https://seznam.example.org",
                "query": "průchod fiktivního seznamu",
                "results_count": "3",
                "minutes": "15",
                "note": "",
                "investor_id": "",
                "target_field": "",
            }
        ],
        reviews=[
            {"investor_id": "inv-0001", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "TP", "review_minutes": "20", "note": ""}
        ],
        fact_reviews=[
            {"fact_id": "f-00001", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "spravne", "review_minutes": "3", "note": "", "review_round": "vzorek"}
        ],
        effort_log=[
            {"investor_id": "inv-0001", "activity": "overeni", "actor": "model", "minutes": "12", "logged_at": "2026-10-01", "note": ""},
            {"investor_id": "inv-0001", "activity": "overeni", "actor": "model", "minutes": "3", "logged_at": "2026-10-01", "note": ""},
            {"investor_id": "inv-0003", "activity": "triaz", "actor": "model", "minutes": "4", "logged_at": "2026-09-29", "note": ""},
        ],
        candidate_sources=[
            {"investor_id": "inv-0001", "search_id": "s-001"},
            {"investor_id": "inv-0002", "search_id": "s-001"},
            {"investor_id": "inv-0003", "search_id": "s-001"},
        ],
        funds=[
            {
                "fund_id": "fd-0001",
                "investor_id": "inv-0001",
                "fund_name": FUND_NAME,
                "vintage": "2025",
                "amount": "30000000",
                "currency": "EUR",
                "amount_type": "final_close",
                "approx": "ne",
                "amount_wording": "",
                "value_as_of": "2025-06-30",
                "fact_id": "f-00008",
                "fundraising_open": "",
                "conflict_note": "",
            }
        ],
    )


@pytest.fixture
def dataset() -> Dataset:
    return build_valid_dataset()
