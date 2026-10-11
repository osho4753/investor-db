from datetime import date
from decimal import Decimal

from investor_db.io import Dataset
from investor_db.metrics import (
    OPEN_POPULATION,
    VERIFIED_POPULATION,
    PopulationEstimate,
    Proportion,
    duplicate_group_count,
    effort_summaries,
    exclusion_reason_counts,
    excluded_duplicate_count,
    CAPITAL_AUM,
    CAPITAL_INVESTED,
    CapitalSummary,
    RequirementCompleteness,
    category_investors,
    category_scope,
    category_verdicts,
    fact_accuracy,
    field_completeness,
    investor_capital,
    requirement_completeness,
    freshness_share,
    funnel,
    investment_activity_share,
    population_estimates,
    precision,
    primary_fact_share,
    category_facts,
    vc_pilot_facts,
    vc_pilot_searches,
    primary_registry_share,
    review_efforts,
    reviewer_agreement,
    search_minutes,
    status_counts,
    values_only_in_facts_due_to_currency,
)
from investor_db.schema import (
    ASSESSED_CATEGORIES,
    CATEGORY_VC,
    EFFORT_CATEGORY_VERIFICATION,
    EFFORT_COMPLETION,
    SEARCH_TARGET_CAPITAL,
    SEARCH_TARGET_TICKET,
    EFFORT_ACTOR_MODEL,
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    REVIEWER_INDEPENDENT,
    REVIEWER_PRIMARY,
    REVIEW_ROUND_COMPLETION,
    REVIEW_ROUND_CORRECTION,
    REVIEW_ROUND_SAMPLE,
    STATUSES,
)

CATEGORY_LABELS = {
    "pe": "Private equity (mini-pilot)",
}

PROCESSING_LABELS = {
    "": "nezpracováno",
    EFFORT_TRIAGE: "rychlá triáž",
    EFFORT_VERIFICATION: "plné ověření",
    EFFORT_COMPLETION: "doplňování",
}

REVIEW_ROUND_LABELS = {
    REVIEW_ROUND_SAMPLE: "Původní kontrola – náhodný vzorek faktů",
    REVIEW_ROUND_COMPLETION: "Kontrola po doplnění – všechny fakty přidané doplňováním",
    REVIEW_ROUND_CORRECTION: "Kontrola po opravě – fakty změněné nebo přidané při opravách po kontrole",
}

REQUIREMENT_LABELS = {
    "investment_sectors": "Sektor (`investment_sectors`)",
    "investment_stages": "Do čeho investuje – fáze (`investment_stages`)",
    SEARCH_TARGET_TICKET: "Výše investice – ticket (alespoň jedna mez)",
    SEARCH_TARGET_CAPITAL: "Kapitál (získaná částka fondu nebo AUM)",
}

CAPITAL_LABELS = {
    "final_close": "fond – final close",
    "uzavren_bez_upresneni": "fond – uzavřen bez upřesnění",
    "first_close": "fond – first close",
    "cil": "fond – cílová velikost",
    "zavazek_jednoho_lp": "fond – závazek jednoho LP (jen část fondu)",
    "investovano": "fond – investováno",
    "investovano_za_obdobi": "fond – investováno jen za období (dolní mez)",
    CAPITAL_AUM: "AUM správce",
    CAPITAL_INVESTED: "investovaný kapitál (`invested_capital`)",
}


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}".replace(".", ",") + " %"


def format_proportion(proportion: Proportion) -> str:
    if proportion.value is None:
        return "nelze spočítat (0 záznamů)"
    low, high = proportion.wilson_interval() or (0.0, 0.0)
    return (
        f"{proportion.numerator}/{proportion.denominator} = {format_percent(proportion.value)} "
        f"(95% Wilsonův interval {format_percent(low)} – {format_percent(high)})"
    )


def render_report(dataset: Dataset, today: date) -> str:
    sections = [
        [f"# Metriky kvality dat k {today.isoformat()}"],
        status_section(dataset),
        funnel_section(dataset),
        precision_section(dataset),
        agreement_section(dataset),
        fact_accuracy_section(dataset),
        requirement_section(dataset),
        capital_section(dataset),
        category_section(dataset),
        completeness_section(dataset),
        evidence_section(dataset, today),
        effort_section(dataset),
        coverage_section(dataset),
        limitation_section(dataset),
    ]
    return "\n\n".join("\n".join(lines) for lines in sections) + "\n"


def status_section(dataset: Dataset) -> list[str]:
    statuses = status_counts(dataset.investors)
    reasons = exclusion_reason_counts(dataset.investors)
    lines = ["## Stav záznamů", "", "| Status | Počet |", "|---|---|"]
    lines += [f"| `{status}` | {statuses[status]} |" for status in STATUSES]
    if reasons:
        lines += ["", "| Důvod vyloučení | Počet |", "|---|---|"]
        lines += [f"| `{reason}` | {count} |" for reason, count in sorted(reasons.items())]
    return lines


def funnel_section(dataset: Dataset) -> list[str]:
    stages = funnel(dataset)
    lines = [
        "## Trychtýř",
        "",
        f"Nalezeno subjektů: {len(dataset.investors)}",
        "",
        "| Úroveň zpracování | Celkem | " + " | ".join(f"`{status}`" for status in STATUSES) + " |",
        "|---|---|" + "---|" * len(STATUSES),
    ]
    for level, label in PROCESSING_LABELS.items():
        counts = stages.get(level)
        if counts:
            cells = " | ".join(str(counts[status]) for status in STATUSES)
            lines.append(f"| {label} | {sum(counts.values())} | {cells} |")
    return lines


def precision_section(dataset: Dataset) -> list[str]:
    result = precision(dataset, REVIEWER_PRIMARY)
    lines = ["## Precision (ověření investoři, hodnotitel R1)", ""]
    if result.strict.denominator + result.unsure == 0:
        return lines + ["Ruční kontrola R1 zatím není vyplněna."]
    return lines + [
        f"- TP = {result.true_positives}, FP = {result.false_positives}, nejisté = {result.unsure}",
        f"- Precision TP / (TP + FP): {format_proportion(result.strict)}",
        f"- Pesimistická varianta (nejisté jako FP): {format_proportion(result.pessimistic)}",
    ]


def agreement_section(dataset: Dataset) -> list[str]:
    lines = ["## Shoda hodnotitelů R1 a R2", ""]
    result = reviewer_agreement(dataset)
    if result is None:
        return lines + ["Data R2 nejsou k dispozici; Cohenovo κ se nepočítá."]
    kappa = "nelze určit (oba hodnotitelé použili jedinou kategorii)" if result.kappa is None else f"{result.kappa:.2f}".replace(".", ",")
    return lines + [
        f"- Prostá shoda: {format_proportion(result.agreement)}",
        f"- Cohenovo κ: {kappa}",
        "- Při malém vzorku a vysokém podílu TP je κ nestabilní; rozhodující je prostá shoda a rozbor neshod.",
    ]


def fact_accuracy_section(dataset: Dataset) -> list[str]:
    lines = ["## Přesnost faktů", ""]
    for review_round, label in REVIEW_ROUND_LABELS.items():
        lines.append(f"### {label}")
        lines.append("")
        for reviewer in (REVIEWER_PRIMARY, REVIEWER_INDEPENDENT):
            result = fact_accuracy(dataset, reviewer, review_round)
            if result.accuracy.denominator + result.unverifiable == 0:
                lines.append(f"- {reviewer}: kontrola faktů zatím není vyplněna.")
                continue
            lines.append(
                f"- {reviewer}: {format_proportion(result.accuracy)}; nelze ověřit: {result.unverifiable}"
            )
        lines.append("")
    return lines[:-1]


def format_share(proportion: Proportion) -> str:
    share = "–" if proportion.value is None else format_percent(proportion.value)
    return f"{proportion.numerator}/{proportion.denominator} ({share})"


def requirement_section(dataset: Dataset) -> list[str]:
    return ["## Úplnost podle požadavků zadání (ověření investoři)", ""] + requirement_lines(requirement_completeness(dataset))


def requirement_lines(result: RequirementCompleteness) -> list[str]:
    lines = [
        "| Požadavek | Vyplněno | Chybí, hledáno a nenalezeno |",
        "|---|---|---|",
    ]
    lines += [
        f"| {label} | {format_share(result.filled[target])} | {result.searched_not_found[target]} |"
        for target, label in REQUIREMENT_LABELS.items()
    ]
    lines += [
        f"| Ticket – obě meze | {format_share(result.tickets_both)} | |",
        f"| Kapitál – jen cílová velikost (získaný kapitál neznámý) | {format_share(result.target_only)} | |",
        f"| Zdroj (`evidence_urls`) | {format_share(result.sources)} | |",
        "",
        "| Typ kapitálu | Investorů s údajem |",
        "|---|---|",
    ]
    lines += [f"| {CAPITAL_LABELS[kind]} | {format_share(share)} |" for kind, share in result.capital_by_kind.items()]
    return lines


def capital_rows(summaries: list[CapitalSummary]) -> list[str]:
    lines = [
        "| Investor | Fondů ve funds.csv (se získanou částkou) / dle zdroje | Typy získaných částek "
        "| Získaný kapitál | Cíl (nezapočten) | Investováno | AUM | Konflikt zdrojů |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for summary in summaries:
        aum = f"{format_amount(Decimal(summary.aum))} {summary.aum_currency}" if summary.aum else "–"
        lines.append(
            f"| {summary.name} | {format_fund_count(summary)} | {', '.join(summary.raised_types) or '–'} "
            f"| {format_raised(summary)} | {format_amounts(summary.targets) or '–'} "
            f"| {format_invested(summary)} | {aum} | {format_conflicts(summary)} |"
        )
    return lines


def category_section(dataset: Dataset) -> list[str]:
    lines = ["## Hodnocení v dalších kategoriích", ""]
    categories = [category for category in ASSESSED_CATEGORIES if any(row["category"] == category for row in dataset.category_assessments)]
    if not categories:
        return lines + ["Žádný subjekt zatím není hodnocen v jiné kategorii než VC."]
    for category in categories:
        lines += category_lines(dataset, category)
    return lines


def category_lines(dataset: Dataset, category: str) -> list[str]:
    assessed = [row for row in dataset.category_assessments if row["category"] == category]
    verified = category_investors(dataset, category)
    counts = {status: sum(row["verification_status"] == status for row in assessed) for status in STATUSES}
    reasons = sorted({row["exclusion_reason"] for row in assessed if row["exclusion_reason"]})
    assessed_ids = {row["investor_id"] for row in assessed}
    effort = [
        row for row in dataset.effort_log
        if row["activity"] == EFFORT_CATEGORY_VERIFICATION and row["investor_id"] in assessed_ids
    ]
    lines = [
        f"### {CATEGORY_LABELS[category]}",
        "",
        "Status podle pravidel kategorie (tabulka `category_assessments.csv`); status ve VC pilotu se nemění.",
        "",
        f"- Posouzeno: {len(assessed)}; " + ", ".join(f"{status} {count}" for status, count in counts.items())
        + (f"; důvody vyloučení: {', '.join(reasons)}" if reasons else ""),
    ]
    lines += effort_table(effort)
    lines += ["", f"- Fakta z primárních zdrojů: {format_proportion(primary_fact_share(dataset, category_facts(dataset, assessed_ids)))}"]
    scope = category_scope(dataset, category)
    lines += [
        f"- Ověřená pravost (skutečný investor kategorie, i mimo zemi pilotu): {scope.authentic}/{scope.assessed}",
        f"- V rámci země pilotu (česká právnická osoba, status `overeny`): {scope.in_pilot_country}/{scope.assessed}",
        "- Studie proveditelnosti: výsledky se uvádějí v počtech, ne jako procento.",
    ]
    verdicts = category_verdicts(dataset, REVIEWER_PRIMARY, category)
    if verdicts:
        lines += [""] + [
            f"- Kontrola R1 u statusu `{status}`: " + ", ".join(f"{verdict} {count}" for verdict, count in sorted(counts.items()))
            + f" (z {counts.total()})"
            for status, counts in sorted(verdicts.items())
        ]
    else:
        lines += ["", "- Ruční kontrola R1 v této kategorii zatím není vyplněna."]
    if not verified:
        return lines + [""]
    lines += ["", f"#### Úplnost podle požadavků zadání (ověření v kategorii, n = {len(verified)})", ""]
    lines += requirement_lines(requirement_completeness(dataset, verified))
    lines += ["", "#### Kapitál", ""]
    lines += capital_rows(investor_capital(dataset, verified))
    return lines + [""]


def format_amount(amount: Decimal) -> str:
    return f"{amount:,.0f}".replace(",", " ")


def format_amounts(amounts: dict[str, Decimal]) -> str:
    return " + ".join(f"{format_amount(amount)} {currency}" for currency, amount in amounts.items())


def format_raised(summary: CapitalSummary) -> str:
    if not summary.raised:
        return "neznámý"
    notes = ["dolní mez"] if summary.lower_bound else []
    if summary.lp_commitments:
        notes.append(f"z toho závazek jednoho LP {format_amounts(summary.lp_commitments)}")
    if summary.fundraising_open:
        notes.append(f"fundraising pokračuje: {', '.join(summary.fundraising_open)}")
    amounts = format_amounts(summary.raised)
    return f"{amounts} ({'; '.join(notes)})" if notes else amounts


def format_invested(summary: CapitalSummary) -> str:
    amounts = format_amounts(summary.invested) or "–"
    notes = []
    if summary.invested_period_fact_ids:
        notes.append(f"dolní mez: jen investice za období, formulace ve faktu {', '.join(summary.invested_period_fact_ids)}")
    if summary.invested_fact_id:
        notes.append(f"údaj za celého správce; formulace a rozsah ve faktu {summary.invested_fact_id}")
    return f"{amounts} ({'; '.join(notes)})" if notes else amounts


def format_conflicts(summary: CapitalSummary) -> str:
    return "**KONFLIKT** " + "; ".join(summary.conflicts) if summary.conflicts else "–"


def format_fund_count(summary: CapitalSummary) -> str:
    documented = "–" if summary.documented_fund_count is None else str(summary.documented_fund_count)
    return f"{summary.fund_count} ({summary.funds_with_raised}) / {documented}"


def capital_section(dataset: Dataset) -> list[str]:
    lines = [
        "## Celkový investiční kapitál (odvozený z funds.csv)",
        "",
        "Získaný kapitál je součet skutečně získaných částek (u každého fondu nejlepší typ: final close > "
        "uzavřen bez upřesnění > first close > závazek jednoho LP); měny se nesčítají. Cílová velikost se do "
        "získaného kapitálu nikdy nepřičítá a uvádí se zvlášť u fondů bez získané částky. „Dolní mez“: nejsou "
        "známé získané částky všech fondů správce (počet fondů nedoložen faktem `pocet_fondu` nebo některý fond "
        "nemá získanou částku), částka je přibližná, jde o first close nebo závazek jednoho LP, fundraising některého fondu podle zdrojů pokračuje nebo se zdroje u některého fondu rozcházejí (sloupec Konflikt zdrojů). Investováno a AUM jsou zvlášť; investovaný kapitál za celého správce odkazuje na fakt s doslovnou formulací a částka investovaná jen za určité období je dolní mez.",
        "",
    ]
    return lines + capital_rows(investor_capital(dataset))


def completeness_section(dataset: Dataset) -> list[str]:
    lines = ["## Úplnost polí (ověření investoři)", "", "| Pole | Vyplněno |", "|---|---|"]
    for column, proportion in field_completeness(dataset.investors).items():
        share = "–" if proportion.value is None else format_percent(proportion.value)
        lines.append(f"| `{column}` | {proportion.numerator}/{proportion.denominator} ({share}) |")
    return lines


def evidence_section(dataset: Dataset, today: date) -> list[str]:
    return [
        "## Doložení a aktuálnost",
        "",
        f"- Ověření investoři s IČO z primárního zdroje: {format_proportion(primary_registry_share(dataset))}",
        f"- Fakta z primárních zdrojů (VC pilot): {format_proportion(primary_fact_share(dataset, vc_pilot_facts(dataset)))}",
        f"- Ověření investoři s doloženou investicí za 36 měsíců: {format_proportion(investment_activity_share(dataset, today))}",
        f"- Ověření investoři ověření za posledních 12 měsíců: {format_proportion(freshness_share(dataset.investors, today))}",
        f"- Skupiny možných duplicit: {duplicate_group_count(dataset.investors)}",
        f"- Záznamy vyloučené jako duplicita: {excluded_duplicate_count(dataset.investors)}",
    ]


def format_decimal(value: float | Decimal) -> str:
    return f"{value:.1f}".replace(".", ",")


def effort_section(dataset: Dataset) -> list[str]:
    lines = [
        "## Pracnost",
        "",
        "### Model",
        "",
        f"- Hledání kandidátů a cílená hledání (VC pilot): {len(vc_pilot_searches(dataset))} průchodů, "
        f"{format_decimal(search_minutes(vc_pilot_searches(dataset)))} min celkem",
    ]
    lines += effort_table(
        [row for row in dataset.effort_log if row["actor"] == EFFORT_ACTOR_MODEL and row["activity"] != EFFORT_CATEGORY_VERIFICATION]
    )
    lines += ["", "Čas modelu je čas běhu nástrojů včetně čekání na stránky a není přímo srovnatelný s časem člověka."]
    lines += ["", "### Člověk", ""]
    lines += effort_table([row for row in dataset.effort_log if row["actor"] != EFFORT_ACTOR_MODEL])
    vc_reviews = [row for row in dataset.reviews if row["category"] == CATEGORY_VC]
    for label, rows in (("Kontrola investorů (VC)", vc_reviews), ("Kontrola faktů", dataset.fact_reviews)):
        efforts = review_efforts(rows)
        if not efforts:
            lines.append(f"- {label}: zatím neprovedena.")
        for effort in efforts:
            lines.append(
                f"- {label} {effort.reviewer}: {effort.reviews} kontrol, čas uveden u {effort.timed_reviews}, "
                f"{format_decimal(effort.total_minutes)} min celkem"
            )
    return lines


def effort_table(rows: list[dict[str, str]]) -> list[str]:
    summaries = effort_summaries(rows)
    if not summaries:
        return ["- Čas po investorech zatím není zaznamenán."]
    lines = [
        "",
        "| Činnost | Kdo | Investorů | Minut celkem | Průměr na investora | Medián na investora |",
        "|---|---|---|---|---|---|",
    ]
    lines += [
        f"| `{summary.activity}` | {summary.actor} | {len(summary.minutes_per_investor)} | {format_decimal(summary.total_minutes)} "
        f"| {format_decimal(summary.mean_minutes)} | {format_decimal(summary.median_minutes)} |"
        for summary in summaries
    ]
    return lines


def format_estimate(estimate: PopulationEstimate) -> str:
    lincoln = "–" if estimate.lincoln_petersen is None else format_decimal(estimate.lincoln_petersen)
    low, high = estimate.chapman_interval()
    return (
        f"| {estimate.first_search_id} × {estimate.second_search_id} | {estimate.first_count} | {estimate.second_count} "
        f"| {estimate.overlap} | {estimate.observed} | {lincoln} | {format_decimal(estimate.chapman)} "
        f"| {format_decimal(low)} – {format_decimal(high)} |"
    )


def coverage_section(dataset: Dataset) -> list[str]:
    lines = ["## Odhad celkového počtu (capture–recapture)"]
    for label, statuses in (("ověření investoři", VERIFIED_POPULATION), ("ověření a dosud otevření kandidáti", OPEN_POPULATION)):
        estimates = [estimate for estimate in population_estimates(dataset, statuses) if estimate.overlap]
        lines += ["", f"### Populace: {label}", ""]
        if not estimates:
            lines.append("Žádná dvojice průchodů nemá společný subjekt; odhad nelze spočítat.")
            continue
        lines += [
            "| Dvojice průchodů | n1 | n2 | Překryv m | Pozorováno | Lincoln–Petersen | Chapman | 95% interval (Chapman) |",
            "|---|---|---|---|---|---|---|---|",
        ]
        lines += [format_estimate(estimate) for estimate in estimates]
    return lines + [
        "",
        "Zdroje nejsou nezávislé (sekundární zdroje přebírají viditelné fondy), proto je odhad spíše dolní mezí.",
    ]


def limitation_section(dataset: Dataset) -> list[str]:
    return [
        "## Omezení dat",
        "",
        f"- Peněžní hodnoty jen ve facts.csv kvůli jiné měně než řádek: {values_only_in_facts_due_to_currency(dataset)}",
    ]
