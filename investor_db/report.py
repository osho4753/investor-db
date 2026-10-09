from datetime import date

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
    fact_accuracy,
    field_completeness,
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
    EFFORT_ACTOR_MODEL,
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    REVIEWER_INDEPENDENT,
    REVIEWER_PRIMARY,
    STATUSES,
)

PROCESSING_LABELS = {
    "": "nezpracováno",
    EFFORT_TRIAGE: "rychlá triáž",
    EFFORT_VERIFICATION: "plné ověření",
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
    for reviewer in (REVIEWER_PRIMARY, REVIEWER_INDEPENDENT):
        result = fact_accuracy(dataset, reviewer)
        if result.accuracy.denominator + result.unverifiable == 0:
            lines.append(f"- {reviewer}: kontrola faktů zatím není vyplněna.")
            continue
        lines.append(
            f"- {reviewer}: {format_proportion(result.accuracy)}; nelze ověřit: {result.unverifiable}"
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


def format_decimal(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def effort_section(dataset: Dataset) -> list[str]:
    lines = [
        "## Pracnost",
        "",
        "### Model",
        "",
        f"- Hledání kandidátů: {len(dataset.search_log)} průchodů, {search_minutes(dataset.search_log)} min celkem",
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
                f"{effort.total_minutes} min celkem"
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
        f"| `{summary.activity}` | {summary.actor} | {len(summary.minutes_per_investor)} | {summary.total_minutes} "
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
