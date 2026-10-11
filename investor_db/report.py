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
    primary_registry_share,
    review_efforts,
    reviewer_agreement,
    search_minutes,
    status_counts,
    values_only_in_facts_due_to_currency,
)
from investor_db.schema import (
    EFFORT_COMPLETION,
    SEARCH_TARGET_CAPITAL,
    SEARCH_TARGET_TICKET,
    EFFORT_ACTOR_MODEL,
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    REVIEWER_INDEPENDENT,
    REVIEWER_PRIMARY,
    REVIEW_ROUND_COMPLETION,
    REVIEW_ROUND_SAMPLE,
    STATUSES,
)

PROCESSING_LABELS = {
    "": "nezpracováno",
    EFFORT_TRIAGE: "rychlá triáž",
    EFFORT_VERIFICATION: "plné ověření",
    EFFORT_COMPLETION: "doplňování",
}

REVIEW_ROUND_LABELS = {
    REVIEW_ROUND_SAMPLE: "Původní kontrola – náhodný vzorek faktů",
    REVIEW_ROUND_COMPLETION: "Kontrola po doplnění – všechny fakty přidané doplňováním",
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
    result = requirement_completeness(dataset)
    lines = [
        "## Úplnost podle požadavků zadání (ověření investoři)",
        "",
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
    if summary.invested_fact_id:
        return f"{amounts} (údaj za celého správce; formulace a rozsah ve faktu {summary.invested_fact_id})"
    return amounts


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
        "nemá získanou částku), částka je přibližná, jde o first close nebo závazek jednoho LP, fundraising některého fondu podle zdrojů pokračuje nebo se zdroje u některého fondu rozcházejí (sloupec Konflikt zdrojů). Investováno a AUM jsou zvlášť; investovaný kapitál za celého správce odkazuje na fakt s doslovnou formulací.",
        "",
        "| Investor | Fondů ve funds.csv (se získanou částkou) / dle zdroje | Typy získaných částek "
        "| Získaný kapitál | Cíl (nezapočten) | Investováno | AUM | Konflikt zdrojů |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for summary in investor_capital(dataset):
        aum = f"{format_amount(Decimal(summary.aum))} {summary.aum_currency}" if summary.aum else "–"
        lines.append(
            f"| {summary.name} | {format_fund_count(summary)} | {', '.join(summary.raised_types) or '–'} "
            f"| {format_raised(summary)} | {format_amounts(summary.targets) or '–'} "
            f"| {format_invested(summary)} | {aum} | {format_conflicts(summary)} |"
        )
    return lines


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
        f"- Fakta z primárních zdrojů: {format_proportion(primary_fact_share(dataset))}",
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
        f"- Hledání kandidátů: {len(dataset.search_log)} průchodů, {format_decimal(search_minutes(dataset.search_log))} min celkem",
    ]
    lines += effort_table([row for row in dataset.effort_log if row["actor"] == EFFORT_ACTOR_MODEL])
    lines += ["", "Čas modelu je čas běhu nástrojů včetně čekání na stránky a není přímo srovnatelný s časem člověka."]
    lines += ["", "### Člověk", ""]
    lines += effort_table([row for row in dataset.effort_log if row["actor"] != EFFORT_ACTOR_MODEL])
    for label, rows in (("Kontrola investorů", dataset.reviews), ("Kontrola faktů", dataset.fact_reviews)):
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
