from typing import Final

INVESTOR_COLUMNS: Final = (
    "investor_id",
    "name",
    "investor_type",
    "country",
    "registry_id",
    "website",
    "investment_sectors",
    "investment_stages",
    "typical_ticket_min",
    "typical_ticket_max",
    "currency",
    "total_fund_size",
    "assets_under_management",
    "invested_capital",
    "verification_status",
    "exclusion_reason",
    "evidence_urls",
    "last_verified_at",
)
FACT_COLUMNS: Final = (
    "fact_id",
    "investor_id",
    "field",
    "value",
    "currency",
    "fund_name",
    "value_as_of",
    "source_id",
    "accessed_at",
    "evidence_note",
)
SOURCE_COLUMNS: Final = ("source_id", "url", "publisher", "source_type")
SEARCH_LOG_COLUMNS: Final = ("search_id", "searched_at", "source_url", "query", "results_count", "minutes", "note")
REVIEW_COLUMNS: Final = ("investor_id", "reviewer", "reviewed_at", "verdict", "review_minutes", "note")
FACT_REVIEW_COLUMNS: Final = ("fact_id", "reviewer", "reviewed_at", "verdict", "review_minutes", "note")
CANDIDATE_SOURCE_COLUMNS: Final = ("investor_id", "search_id")
EFFORT_COLUMNS: Final = ("investor_id", "activity", "actor", "minutes", "logged_at", "note")

STATUS_VERIFIED: Final = "overeny"
STATUS_CANDIDATE: Final = "kandidat"
STATUS_EXCLUDED: Final = "vyloucen"
STATUSES: Final = (STATUS_VERIFIED, STATUS_CANDIDATE, STATUS_EXCLUDED)

INVESTOR_TYPE_VC: Final = "vc"
INVESTOR_TYPES: Final = (
    INVESTOR_TYPE_VC,
    "pe",
    "cvc",
    "fond_fondu",
    "statni_fond",
    "business_angel",
    "family_office",
    "akcelerator",
    "crowdfunding",
    "jiny",
)

EXCLUSION_DUPLICATE: Final = "duplicita"
EXCLUSION_FOREIGN: Final = "zahranicni_subjekt"
OUT_OF_SCOPE_EXCLUSION_REASONS: Final = (
    "cvc",
    "fond_fondu",
    "statni_fond",
    "dluhovy_fond",
    "digitalni_aktiva",
    "otevreny_smiseny_fond",
)
EXCLUSION_REASONS: Final = (
    *OUT_OF_SCOPE_EXCLUSION_REASONS,
    EXCLUSION_FOREIGN,
    "pe_budouci_rozsireni",
    "business_angel",
    "family_office",
    "bez_fondu",
    "neaktivni",
    "zanikly_subjekt",
    EXCLUSION_DUPLICATE,
)
RETIRED_EXCLUSION_REASONS: Final = {"mimo_definici_pilotu": OUT_OF_SCOPE_EXCLUSION_REASONS}

INVESTMENT_STAGES: Final = ("pre_seed", "seed", "serie_a", "serie_b", "growth")
INVESTMENT_SECTORS: Final = (
    "ai",
    "agritech",
    "biotech",
    "cleantech",
    "deeptech",
    "ecommerce",
    "edtech",
    "energetika",
    "fintech",
    "gaming",
    "hardware",
    "healthtech",
    "kyberbezpecnost",
    "media",
    "mobilita",
    "proptech",
    "prumysl",
    "software",
    "spotrebitelske",
    "obrana_bezpecnost",
    "cestovani",
    "logistika",
    "jine",
    "sektorove_agnosticky",
)

PRIMARY_SOURCE_TYPES: Final = ("regulator", "rejstrik", "vyrocni_zprava", "web_investora")
SECONDARY_SOURCE_TYPES: Final = ("asociace", "media", "jine")
SOURCE_TYPES: Final = PRIMARY_SOURCE_TYPES + SECONDARY_SOURCE_TYPES

CURRENCIES: Final = ("CZK", "EUR", "USD", "GBP", "CHF", "PLN")

REVIEWER_PRIMARY: Final = "R1"
REVIEWER_INDEPENDENT: Final = "R2"
REVIEWERS: Final = (REVIEWER_PRIMARY, REVIEWER_INDEPENDENT)

VERDICT_TRUE_POSITIVE: Final = "TP"
VERDICT_FALSE_POSITIVE: Final = "FP"
VERDICT_UNSURE: Final = "nejiste"
INVESTOR_VERDICTS: Final = (VERDICT_TRUE_POSITIVE, VERDICT_FALSE_POSITIVE, VERDICT_UNSURE)

VERDICT_FACT_CORRECT: Final = "spravne"
VERDICT_FACT_WRONG: Final = "chybne"
VERDICT_FACT_UNVERIFIABLE: Final = "nelze_overit"
FACT_VERDICTS: Final = (VERDICT_FACT_CORRECT, VERDICT_FACT_WRONG, VERDICT_FACT_UNVERIFIABLE)

EFFORT_TRIAGE: Final = "triaz"
EFFORT_VERIFICATION: Final = "overeni"
EFFORT_ACTIVITIES: Final = (EFFORT_TRIAGE, EFFORT_VERIFICATION)
EFFORT_ACTOR_MODEL: Final = "model"
EFFORT_ACTORS: Final = (EFFORT_ACTOR_MODEL, *REVIEWERS)

MONEY_FIELDS: Final = (
    "typical_ticket_min",
    "typical_ticket_max",
    "total_fund_size",
    "assets_under_management",
    "invested_capital",
)
LIST_FIELD_VOCABULARIES: Final = {
    "investment_sectors": INVESTMENT_SECTORS,
    "investment_stages": INVESTMENT_STAGES,
}
EVIDENCED_FIELDS: Final = (
    "name",
    "registry_id",
    "website",
    "investment_sectors",
    "investment_stages",
    *MONEY_FIELDS,
)

FACT_LEGAL_MANAGER: Final = "pravni_spravce"
FACT_TARGET_FUND_SIZE: Final = "cilova_velikost_fondu"
FACT_REGULATOR_REGISTRATION: Final = "registrace_regulator"
FACT_DOCUMENTED_INVESTMENT: Final = "dolozena_investice"
FACT_EXCLUSION_REASON: Final = "duvod_vylouceni"
FACT_FUND_INFO: Final = "informace_o_fondu"
SUPPLEMENTARY_FACT_FIELDS: Final = (
    FACT_FUND_INFO,
    FACT_LEGAL_MANAGER,
    FACT_TARGET_FUND_SIZE,
    FACT_REGULATOR_REGISTRATION,
    FACT_DOCUMENTED_INVESTMENT,
    FACT_EXCLUSION_REASON,
)
FACT_FIELDS: Final = EVIDENCED_FIELDS + SUPPLEMENTARY_FACT_FIELDS
MONEY_FACT_FIELDS: Final = MONEY_FIELDS + (FACT_TARGET_FUND_SIZE,)
FUND_ACTIVITY_FACT_FIELDS: Final = ("total_fund_size", FACT_TARGET_FUND_SIZE, FACT_FUND_INFO)
FUND_SCOPED_FACT_FIELDS: Final = ("total_fund_size", FACT_TARGET_FUND_SIZE, FACT_LEGAL_MANAGER, FACT_FUND_INFO)

ID_PATTERNS: Final = {
    "investor_id": r"inv-\d{4}",
    "fact_id": r"f-\d{5}",
    "source_id": r"src-\d{4}",
    "search_id": r"s-\d{3}",
}

LIST_SEPARATOR: Final = ";"
PILOT_COUNTRY: Final = "CZ"
ACTIVITY_WINDOW_DAYS: Final = 1096
FRESHNESS_WINDOW_DAYS: Final = 365
