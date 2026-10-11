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
SEARCH_LOG_COLUMNS: Final = (
    "search_id",
    "searched_at",
    "source_url",
    "query",
    "results_count",
    "minutes",
    "note",
    "investor_id",
    "target_field",
)
REVIEW_COLUMNS: Final = ("investor_id", "reviewer", "reviewed_at", "verdict", "review_minutes", "note", "category")
FACT_REVIEW_COLUMNS: Final = (
    "fact_id",
    "reviewer",
    "reviewed_at",
    "verdict",
    "review_minutes",
    "note",
    "review_round",
)
CANDIDATE_SOURCE_COLUMNS: Final = ("investor_id", "search_id")
EFFORT_COLUMNS: Final = ("investor_id", "activity", "actor", "minutes", "logged_at", "note")
CATEGORY_ASSESSMENT_COLUMNS: Final = (
    "investor_id",
    "category",
    "verification_status",
    "exclusion_reason",
    "last_verified_at",
    "note",
)
FUND_COLUMNS: Final = (
    "fund_id",
    "investor_id",
    "fund_name",
    "vintage",
    "amount",
    "currency",
    "amount_type",
    "approx",
    "amount_wording",
    "value_as_of",
    "fact_id",
    "fundraising_open",
    "conflict_note",
)

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
CATEGORY_EXCLUSION_REASONS: Final = (*EXCLUSION_REASONS, "vc_ne_pe", "realitni_fond")

CATEGORY_VC: Final = INVESTOR_TYPE_VC
CATEGORY_PE: Final = "pe"
ASSESSED_CATEGORIES: Final = (CATEGORY_PE,)
CATEGORY_VC_EXCLUDED: Final = "vc_vyloucene"
REVIEW_CATEGORIES: Final = (CATEGORY_VC, CATEGORY_VC_EXCLUDED, *ASSESSED_CATEGORIES)
EXCLUDED_SAMPLE_SIZE: Final = 10

VC_INVESTMENT_STAGES: Final = ("pre_seed", "seed", "serie_a", "serie_b", "growth")
PE_INVESTMENT_STAGES: Final = ("buyout", "growth_equity")
INVESTMENT_STAGES: Final = (*VC_INVESTMENT_STAGES, *PE_INVESTMENT_STAGES)
PE_INVESTMENT_SECTORS: Final = (
    "sluzby_firmam",
    "zdravotnictvi",
    "vzdelavani",
    "financni_sluzby",
    "maloobchod",
    "stavebnictvi",
    "tmt",
    "potravinarstvi",
)
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
    *PE_INVESTMENT_SECTORS,
)

PRIMARY_SOURCE_TYPES: Final = ("regulator", "rejstrik", "vyrocni_zprava", "web_investora")
SECONDARY_SOURCE_TYPES: Final = ("asociace", "media", "jine")
SOURCE_TYPES: Final = PRIMARY_SOURCE_TYPES + SECONDARY_SOURCE_TYPES
AGGREGATOR_NAMES: Final = (
    "altss",
    "caplight",
    "cbinsights",
    "crunchbase",
    "dealroom",
    "pitchbook",
    "seedtable",
    "superscout",
)

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

REVIEW_ROUND_SAMPLE: Final = "vzorek"
REVIEW_ROUND_COMPLETION: Final = "po_doplneni"
REVIEW_ROUND_CORRECTION: Final = "po_oprave"
REVIEW_ROUNDS: Final = (REVIEW_ROUND_SAMPLE, REVIEW_ROUND_COMPLETION, REVIEW_ROUND_CORRECTION)

EFFORT_TRIAGE: Final = "triaz"
EFFORT_VERIFICATION: Final = "overeni"
EFFORT_COMPLETION: Final = "doplneni"
EFFORT_CATEGORY_VERIFICATION: Final = "overeni_kategorie"
EFFORT_ACTIVITIES: Final = (EFFORT_TRIAGE, EFFORT_VERIFICATION, EFFORT_COMPLETION, EFFORT_CATEGORY_VERIFICATION)
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
FACT_ANNOUNCED_FUND_SIZE: Final = "oznamena_velikost_fondu"
FACT_REGULATOR_REGISTRATION: Final = "registrace_regulator"
FACT_DOCUMENTED_INVESTMENT: Final = "dolozena_investice"
FACT_EXCLUSION_REASON: Final = "duvod_vylouceni"
FACT_FUND_INFO: Final = "informace_o_fondu"
FACT_FUND_FINAL_CLOSE: Final = "fond_final_close"
FACT_FUND_CLOSED: Final = "fond_uzavren"
FACT_FUND_FIRST_CLOSE: Final = "fond_first_close"
FACT_FUND_LP_COMMITMENT: Final = "fond_zavazek_lp"
FACT_FUND_INVESTED: Final = "fond_investovano"
FACT_FUND_INVESTED_PERIOD: Final = "fond_investovano_za_obdobi"
FACT_FUND_COUNT: Final = "pocet_fondu"
FUND_AMOUNT_FACT_FIELDS: Final = (
    FACT_FUND_FINAL_CLOSE,
    FACT_FUND_CLOSED,
    FACT_FUND_FIRST_CLOSE,
    FACT_FUND_LP_COMMITMENT,
    FACT_FUND_INVESTED,
    FACT_FUND_INVESTED_PERIOD,
)
SUPPLEMENTARY_FACT_FIELDS: Final = (
    FACT_FUND_INFO,
    FACT_LEGAL_MANAGER,
    FACT_TARGET_FUND_SIZE,
    FACT_ANNOUNCED_FUND_SIZE,
    *FUND_AMOUNT_FACT_FIELDS,
    FACT_FUND_COUNT,
    FACT_REGULATOR_REGISTRATION,
    FACT_DOCUMENTED_INVESTMENT,
    FACT_EXCLUSION_REASON,
)
FACT_FIELDS: Final = EVIDENCED_FIELDS + SUPPLEMENTARY_FACT_FIELDS
MONEY_FACT_FIELDS: Final = MONEY_FIELDS + (FACT_TARGET_FUND_SIZE, FACT_ANNOUNCED_FUND_SIZE, *FUND_AMOUNT_FACT_FIELDS)
FUND_ACTIVITY_FACT_FIELDS: Final = (
    "total_fund_size",
    FACT_TARGET_FUND_SIZE,
    FACT_ANNOUNCED_FUND_SIZE,
    FACT_FUND_INFO,
    FACT_FUND_FINAL_CLOSE,
    FACT_FUND_CLOSED,
    FACT_FUND_FIRST_CLOSE,
)
FUND_SCOPED_FACT_FIELDS: Final = (
    "total_fund_size",
    FACT_TARGET_FUND_SIZE,
    FACT_ANNOUNCED_FUND_SIZE,
    FACT_LEGAL_MANAGER,
    FACT_FUND_INFO,
    *FUND_AMOUNT_FACT_FIELDS,
)

AMOUNT_FINAL_CLOSE: Final = "final_close"
AMOUNT_CLOSED: Final = "uzavren_bez_upresneni"
AMOUNT_FIRST_CLOSE: Final = "first_close"
AMOUNT_TARGET: Final = "cil"
AMOUNT_LP_COMMITMENT: Final = "zavazek_jednoho_lp"
AMOUNT_INVESTED: Final = "investovano"
AMOUNT_INVESTED_PERIOD: Final = "investovano_za_obdobi"
INVESTED_AMOUNT_TYPES: Final = (AMOUNT_INVESTED, AMOUNT_INVESTED_PERIOD)
RAISED_AMOUNT_PRIORITY: Final = (AMOUNT_FINAL_CLOSE, AMOUNT_CLOSED, AMOUNT_FIRST_CLOSE, AMOUNT_LP_COMMITMENT)
LOWER_BOUND_AMOUNT_TYPES: Final = (AMOUNT_FIRST_CLOSE, AMOUNT_LP_COMMITMENT)
FUND_AMOUNT_TYPES: Final = (*RAISED_AMOUNT_PRIORITY[:3], AMOUNT_TARGET, AMOUNT_LP_COMMITMENT, *INVESTED_AMOUNT_TYPES)
FACT_FIELDS_BY_AMOUNT_TYPE: Final = {
    AMOUNT_FINAL_CLOSE: (FACT_FUND_FINAL_CLOSE, "total_fund_size"),
    AMOUNT_CLOSED: (FACT_FUND_CLOSED, "total_fund_size"),
    AMOUNT_FIRST_CLOSE: (FACT_FUND_FIRST_CLOSE,),
    AMOUNT_TARGET: (FACT_TARGET_FUND_SIZE,),
    AMOUNT_LP_COMMITMENT: (FACT_FUND_LP_COMMITMENT,),
    AMOUNT_INVESTED: (FACT_FUND_INVESTED,),
    AMOUNT_INVESTED_PERIOD: (FACT_FUND_INVESTED_PERIOD,),
}
APPROX_YES: Final = "ano"
APPROX_NO: Final = "ne"
APPROX_VALUES: Final = (APPROX_YES, APPROX_NO)
FUNDRAISING_OPEN: Final = "ano"
FUNDRAISING_VALUES: Final = (FUNDRAISING_OPEN, "ne")

SEARCH_TARGET_TICKET: Final = "typical_ticket"
SEARCH_TARGET_CAPITAL: Final = "kapital"
SEARCH_TARGETS: Final = ("investment_sectors", "investment_stages", SEARCH_TARGET_TICKET, SEARCH_TARGET_CAPITAL)

ID_PATTERNS: Final = {
    "investor_id": r"inv-\d{4}",
    "fact_id": r"f-\d{5}",
    "source_id": r"src-\d{4}",
    "search_id": r"s-\d{3}",
    "fund_id": r"fd-\d{4}",
}

LIST_SEPARATOR: Final = ";"
PILOT_COUNTRY: Final = "CZ"
ACTIVITY_WINDOW_DAYS: Final = 1096
FRESHNESS_WINDOW_DAYS: Final = 365
