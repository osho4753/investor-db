from datetime import date

from investor_db.io import Dataset
from investor_db.metrics import (
    Proportion,
    duplicate_group_count,
    effort_summaries,
    exclusion_reason_counts,
    excluded_duplicate_count,
    fact_accuracy,
    field_completeness,
    freshness_share,
    investment_activity_share,
    precision,
    primary_fact_share,
    primary_registry_share,
    reviewer_agreement,
    search_minutes,
    status_counts,
    values_only_in_facts_due_to_currency,
)
from investor_db.schema import REVIEWER_INDEPENDENT, REVIEWER_PRIMARY, STATUSES


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
        precision_section(dataset),
        agreement_section(dataset),
        fact_accuracy_section(dataset),
        completeness_section(dataset),
        evidence_section(dataset, today),
        effort_section(dataset),
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


def format_minutes(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def effort_section(dataset: Dataset) -> list[str]:
    lines = [
        "## Pracnost",
        "",
        f"- Hledání kandidátů: {len(dataset.search_log)} průchodů, {search_minutes(dataset.search_log)} min celkem",
    ]
    summaries = effort_summaries(dataset.effort_log)
    if not summaries:
        return lines + ["- Čas po investorech zatím není zaznamenán."]
    lines += [
        "",
        "| Činnost | Kdo | Investorů | Minut celkem | Průměr na investora | Medián na investora |",
        "|---|---|---|---|---|---|",
    ]
    lines += [
        f"| `{summary.activity}` | {summary.actor} | {len(summary.minutes_per_investor)} | {summary.total_minutes} "
        f"| {format_minutes(summary.mean_minutes)} | {format_minutes(summary.median_minutes)} |"
        for summary in summaries
    ]
    return lines + ["", "Čas modelu je čas běhu nástrojů a není přímo srovnatelný s časem člověka."]


def limitation_section(dataset: Dataset) -> list[str]:
    return [
        "## Omezení dat",
        "",
        f"- Peněžní hodnoty jen ve facts.csv kvůli jiné měně než řádek: {values_only_in_facts_due_to_currency(dataset)}",
    ]
