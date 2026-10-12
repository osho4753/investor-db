from dataclasses import dataclass
from typing import Final

from investor_db.io import Dataset, Row
from investor_db.schema import (
    FACT_DOCUMENTED_INVESTMENT,
    FUND_ACTIVITY_FACT_FIELDS,
    FUND_AMOUNT_FACT_FIELDS,
    FUND_SCOPED_FACT_FIELDS,
    STATUS_VERIFIED,
)

ARES_API_URL: Final = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{}"
FUND_EVIDENCE_PRIORITY: Final = (
    *FUND_AMOUNT_FACT_FIELDS,
    "total_fund_size",
    *(field for field in FUND_SCOPED_FACT_FIELDS if field not in FUND_AMOUNT_FACT_FIELDS and field != "total_fund_size"),
)


@dataclass(frozen=True)
class InvestorEvidence:
    investor: Row
    registry_fact: Row | None
    fund_fact: Row | None
    activity_fact: Row | None

    @property
    def is_investment(self) -> bool:
        return self.activity_fact is not None and self.activity_fact["field"] == FACT_DOCUMENTED_INVESTMENT


def ares_url(registry_id: str) -> str:
    return ARES_API_URL.format(registry_id)


def newest(facts: list[Row]) -> Row | None:
    dated = [fact for fact in facts if fact["value_as_of"]]
    if not dated:
        return None
    return max(dated, key=lambda fact: (fact["value_as_of"], fact["fact_id"]))


def fund_evidence(facts: list[Row]) -> Row | None:
    for field in FUND_EVIDENCE_PRIORITY:
        candidates = [fact for fact in facts if fact["field"] == field and fact["fund_name"]]
        if candidates:
            return newest(candidates) or candidates[0]
    return next((fact for fact in facts if fact["fund_name"]), None)


def latest_activity(facts: list[Row]) -> Row | None:
    investment = newest([fact for fact in facts if fact["field"] == FACT_DOCUMENTED_INVESTMENT])
    if investment:
        return investment
    return newest([fact for fact in facts if fact["field"] in FUND_ACTIVITY_FACT_FIELDS])


def registry_evidence(investor: Row, facts: list[Row]) -> Row | None:
    return next((fact for fact in facts if fact["field"] == "registry_id" and fact["value"] == investor["registry_id"]), None)


def verified_evidence(dataset: Dataset) -> list[InvestorEvidence]:
    investors = sorted(
        (row for row in dataset.investors if row["verification_status"] == STATUS_VERIFIED),
        key=lambda row: row["name"].lower(),
    )
    result = []
    for investor in investors:
        facts = [fact for fact in dataset.facts if fact["investor_id"] == investor["investor_id"]]
        result.append(InvestorEvidence(investor, registry_evidence(investor, facts), fund_evidence(facts), latest_activity(facts)))
    return result
