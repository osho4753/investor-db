import html
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Final

from investor_db.evidence import InvestorEvidence, verified_evidence
from investor_db.io import Dataset, Row, load_dataset
from investor_db.markup import (
    REPOSITORY_URL,
    first_table,
    inline,
    render_table,
    render_text,
    repository_url,
    section_lines,
    timeline_entries,
)
from investor_db.metrics import (
    CapitalSummary,
    Proportion,
    category_scope,
    category_verdicts,
    effort_summaries,
    exclusion_reason_counts,
    exclusion_review,
    fact_accuracy,
    funnel,
    investor_capital,
    precision,
    requirement_completeness,
    review_efforts,
    status_counts,
)
from investor_db.report import format_amount, format_amounts, format_percent, format_raised
from investor_db.review_guide import LIST_LABELS
from investor_db.schema import (
    CATEGORY_PE,
    CATEGORY_VC,
    EFFORT_ACTOR_MODEL,
    EFFORT_CATEGORY_VERIFICATION,
    EFFORT_COMPLETION,
    EFFORT_TRIAGE,
    EFFORT_VERIFICATION,
    MONEY_FACT_FIELDS,
    REVIEW_ROUNDS,
    REVIEWER_PRIMARY,
    SEARCH_TARGET_CAPITAL,
    SEARCH_TARGET_TICKET,
    STATUS_CANDIDATE,
    STATUS_EXCLUDED,
    STATUS_VERIFIED,
    STATUSES,
)

TEXTS_DIR: Final = "site_texts"
SITE_DIR: Final = "site"
STATUS_PILLS: Final = {
    STATUS_VERIFIED: ("ok", "ověřený"),
    STATUS_CANDIDATE: ("cand", "kandidát"),
    STATUS_EXCLUDED: ("out", "vyloučený"),
}
REASON_LABELS: Final = {
    "cvc": "Korporátní VC",
    "fond_fondu": "Fond fondů",
    "statni_fond": "Státní fond nebo program",
    "dluhovy_fond": "Dluhový fond",
    "digitalni_aktiva": "Digitální aktiva",
    "otevreny_smiseny_fond": "Otevřený smíšený fond",
    "zahranicni_subjekt": "Zahraniční subjekt",
    "pe_budouci_rozsireni": "Private equity",
    "business_angel": "Business angel",
    "family_office": "Family office",
    "bez_fondu": "Bez fondu s cizím kapitálem",
    "neaktivni": "Neaktivní",
    "zanikly_subjekt": "Zaniklý subjekt",
    "duplicita": "Duplicita",
    "vc_ne_pe": "VC, ne PE",
    "realitni_fond": "Realitní fond",
}
FIELD_LABELS: Final = {
    "name": "Název",
    "registry_id": "IČO",
    "website": "Web",
    "investment_sectors": "Sektory",
    "investment_stages": "Fáze",
    "typical_ticket_min": "Ticket od",
    "typical_ticket_max": "Ticket do",
    "total_fund_size": "Velikost fondu",
    "assets_under_management": "AUM",
    "invested_capital": "Investováno celkem",
    "informace_o_fondu": "O fondu",
    "pravni_spravce": "Právní správce",
    "cilova_velikost_fondu": "Cílová velikost",
    "oznamena_velikost_fondu": "Oznámená velikost",
    "fond_final_close": "Final close",
    "fond_uzavren": "Fond uzavřen",
    "fond_first_close": "First close",
    "fond_zavazek_lp": "Závazek jednoho LP",
    "fond_investovano": "Fond investoval",
    "fond_investovano_za_obdobi": "Investováno za období",
    "pocet_fondu": "Počet fondů",
    "registrace_regulator": "Registrace u regulátora",
    "dolozena_investice": "Doložená investice",
    "duvod_vylouceni": "Důvod vyloučení",
}
TYPE_LABELS: Final = {
    "vc": "VC",
    "pe": "PE",
    "cvc": "korporátní VC",
    "fond_fondu": "fond fondů",
    "statni_fond": "státní fond",
    "business_angel": "business angel",
    "family_office": "family office",
    "akcelerator": "akcelerátor",
    "crowdfunding": "crowdfunding",
    "jiny": "jiný",
}
FACT_VERDICT_LABELS: Final = {"spravne": "správně", "chybne": "chybně", "nelze_overit": "nelze ověřit"}
ROUND_LABELS: Final = {"vzorek": "vzorek", "po_doplneni": "po doplnění", "po_oprave": "po opravě"}
INVESTOR_VERDICT_LABELS: Final = {"TP": "TP", "FP": "FP", "nejiste": "nejisté"}
DOCUMENTS: Final = (
    ("docs/00-zadani.md", "zadání"),
    ("docs/01-plan-a-kriteria.md", "plán a kritéria"),
    ("docs/02-metodika.md", "metodika"),
    ("docs/03-globalni-odhad.md", "globální odhad"),
    ("docs/04-rucni-kontrola.md", "ruční kontrola"),
    ("README.md", "README"),
    ("ai-log/", "ai-log"),
)
SUMMARY_HEADING: Final = "### Souhrnná tabulka (základní scénář, v závorce nízký – vysoký)"
ERRORS_HEADING: Final = "### Kde se agent (a zadání) mýlil"


@dataclass(frozen=True)
class SiteSources:
    dataset: Dataset
    texts: dict[str, str]
    readme: str
    estimate: str


def load_sources(root: Path) -> SiteSources:
    texts = {path.stem: path.read_text(encoding="utf-8") for path in sorted((root / TEXTS_DIR).glob("*.md"))}
    return SiteSources(
        dataset=load_dataset(root / "data"),
        texts=texts,
        readme=(root / "README.md").read_text(encoding="utf-8"),
        estimate=(root / "docs" / "03-globalni-odhad.md").read_text(encoding="utf-8"),
    )


def escape(text: str) -> str:
    return html.escape(text)


def share_text(proportion: Proportion) -> str:
    return f"{proportion.numerator}/{proportion.denominator}"


def percent_text(proportion: Proportion) -> str:
    return format_percent(proportion.value) if proportion.value is not None else "–"


def data_date(dataset: Dataset) -> str:
    dates = [row["last_verified_at"] for row in dataset.investors]
    dates += [row["reviewed_at"] for row in dataset.reviews + dataset.fact_reviews]
    dates += [row["logged_at"] for row in dataset.effort_log]
    latest = max(date for date in dates if date)
    year, month, day = latest.split("-")
    return f"{int(day)}. {int(month)}. {year}"


def links(paths: list[tuple[str, str]]) -> str:
    anchors = "".join(f'<a href="{escape(repository_url(path))}">{escape(label)}</a>' for path, label in paths)
    return f'<div class="links">{anchors}</div>'


def stat(number: str, label: str, detail: str) -> str:
    return f'<div class="stat"><span class="n">{escape(number)}</span><span class="l">{escape(label)}</span><span class="s">{escape(detail)}</span></div>'


def headline_stats(dataset: Dataset) -> str:
    vc_precision = precision(dataset, REVIEWER_PRIMARY)
    sample = fact_accuracy(dataset, REVIEWER_PRIMARY, REVIEW_ROUNDS[0]).accuracy
    completion = fact_accuracy(dataset, REVIEWER_PRIMARY, REVIEW_ROUNDS[1]).accuracy
    counts = status_counts(dataset.investors)
    excluded = exclusion_review(dataset, REVIEWER_PRIMARY)
    pe = category_scope(dataset, CATEGORY_PE)
    tiles = [
        stat(share_text(vc_precision.strict), "precision VC", f"ověření investoři potvrzení ruční kontrolou R1 podle současných statusů ({percent_text(vc_precision.strict)})"),
        stat(share_text(sample), "přesnost faktů", f"náhodný vzorek; všechna doplněná fakta {share_text(completion)}"),
        stat(f"{len(dataset.investors)} → {counts[STATUS_VERIFIED]}", "nalezeno → ověřeno", f"{counts[STATUS_CANDIDATE]} kandidáti, {counts[STATUS_EXCLUDED]} vyloučeno s doloženým důvodem"),
        stat(f"{excluded.correct}/{excluded.reviewed}", "správná vyloučení", f"náhodný vzorek {excluded.reviewed} z {excluded.excluded} vyloučených; nejisté {excluded.unsure}"),
        stat(f"{pe.authentic}/{pe.assessed}", "PE mini-pilot: pravost", f"v zemi pilotu {pe.in_pilot_country}/{pe.assessed}"),
    ]
    return f'<div class="stats">{"".join(tiles)}</div>'


def funnel_svg(dataset: Dataset) -> str:
    stages = funnel(dataset)
    total = len(dataset.investors)
    triage = stages.get(EFFORT_TRIAGE, {})
    verified = stages.get(EFFORT_VERIFICATION, {})
    triaged = sum(triage.values())
    full = sum(verified.values())
    unit = 590 / total
    rows = [
        ("Nalezeno", f"{total} subjektů", 0, [(total, "var(--accent)")]),
        ("Rychlá triáž", f"{triaged} vyloučeno · {full} dál", 0, [(triaged, "var(--out)"), (full, "var(--accent)")]),
        (
            "Plné ověření",
            " · ".join(str(verified.get(status, 0)) for status in STATUSES),
            triaged,
            [(verified.get(STATUS_VERIFIED, 0), "var(--ok)"), (verified.get(STATUS_CANDIDATE, 0), "var(--cand)"), (verified.get(STATUS_EXCLUDED, 0), "var(--out)")],
        ),
    ]
    shapes = []
    for index, (title, subtitle, offset, segments) in enumerate(rows):
        top = 10 + index * 54
        shapes.append(f'<text x="0" y="{top + 15}" font-weight="600">{escape(title)}</text>')
        shapes.append(f'<text x="0" y="{top + 31}" class="lbl">{escape(subtitle)}</text>')
        left = 150 + offset * unit
        for count, color in segments:
            width = max(count * unit - 2, 1)
            shapes.append(f'<rect x="{left:.1f}" y="{top}" width="{width:.1f}" height="34" rx="4" fill="{color}"/>')
            if count * unit > 26:
                shapes.append(f'<text x="{left + 8:.1f}" y="{top + 22}" class="in">{count}</text>')
            left += count * unit
    label = f"Trychtýř: {total} nalezených subjektů, {triaged} vyloučeno rychlou triáží, {full} plně ověřeno."
    legend = (
        '<div class="legend"><span><i style="background:var(--ok)"></i>ověřený investor</span>'
        '<span><i style="background:var(--cand)"></i>kandidát</span><span><i style="background:var(--out)"></i>vyloučený</span>'
        '<span><i style="background:var(--accent)"></i>pokračuje</span></div>'
    )
    return f'<div class="funnel" role="img" aria-label="{escape(label)}"><svg viewBox="0 0 760 170">{"".join(shapes)}</svg>{legend}</div>'


def block(number: str, title: str, summary: str, body: str, anchor: str = "", is_open: bool = False) -> str:
    attributes = (f' id="{anchor}"' if anchor else "") + (" open" if is_open else "")
    return (
        f'<details class="block"{attributes}><summary><span class="num">{escape(number)}</span>'
        f'<span class="sumtxt"><h3>{escape(title)}</h3><p>{escape(summary)}</p></span><span class="chev">›</span></summary>'
        f'<div class="body">{body}</div></details>'
    )


def timeline(text: str) -> str:
    items = "".join(
        f'<li><span class="d">{escape(entry.label)}</span><div><h4>{inline(entry.title)}</h4><p>{inline(entry.text)}</p></div></li>'
        for entry in timeline_entries(text)
    )
    return f'<ol class="timeline">{items}</ol>'


def requirement_list(dataset: Dataset) -> str:
    result = requirement_completeness(dataset)
    rows = [
        ("Sektor", result.filled["investment_sectors"]),
        ("Fáze", result.filled["investment_stages"]),
        ("Ticket (alespoň jedna mez)", result.filled[SEARCH_TARGET_TICKET]),
        ("Kapitál (získaná částka nebo AUM)", result.filled[SEARCH_TARGET_CAPITAL]),
        ("Zdroj", result.sources),
    ]
    items = "".join(f"<li><b>{escape(label)}</b> {share_text(value)}</li>" for label, value in rows)
    return f'<ul class="clean">{items}</ul>'


def accuracy_list(dataset: Dataset) -> str:
    items = []
    for review_round in REVIEW_ROUNDS:
        result = fact_accuracy(dataset, REVIEWER_PRIMARY, review_round)
        strict = Proportion(result.correct, result.correct + result.wrong + result.unverifiable)
        items.append(
            f"<li><b>Kolo {escape(ROUND_LABELS[review_round])}</b>: {share_text(result.accuracy)}, "
            f"přísně (nelze ověřit = chyba) {share_text(strict)}</li>"
        )
    return f'<ul class="clean">{"".join(items)}</ul>'


def pe_list(dataset: Dataset) -> str:
    scope = category_scope(dataset, CATEGORY_PE)
    verdicts = category_verdicts(dataset, REVIEWER_PRIMARY, CATEGORY_PE)
    checked = sum(counts.get("TP", 0) for counts in verdicts.values())
    reviewed = sum(counts.total() for counts in verdicts.values())
    return (
        f'<ul class="clean"><li><b>PE mini-pilot</b>: posouzeno {scope.assessed}, pravost {scope.authentic}/{scope.assessed}, '
        f"česká právnická osoba {scope.in_pilot_country}/{scope.assessed}, kontrola R1 TP {checked}/{reviewed}.</li></ul>"
    )


def results_body(sources: SiteSources) -> str:
    dataset = sources.dataset
    vc_precision = precision(dataset, REVIEWER_PRIMARY)
    summary = render_table(first_table(section_lines(sources.estimate, SUMMARY_HEADING)), "docs")
    return "".join([
        render_text(sources.texts["vysledky"]),
        f"<h4>VC pilot ČR</h4><p>Precision podle současných statusů {share_text(vc_precision.strict)}. Přesnost faktů po kolech kontroly:</p>",
        accuracy_list(dataset),
        "<p>Pole zadání u ověřených VC investorů:</p>",
        requirement_list(dataset),
        pe_list(dataset),
        "<h4>Odhad pro všechny kategorie</h4><p>Souhrnná tabulka z docs/03: [M] změřeno, [Z] zdroj, [P] předpoklad.</p>",
        summary,
        links([("docs/03-globalni-odhad.md", "docs/03-globalni-odhad.md"), ("docs/04-rucni-kontrola.md", "docs/04-rucni-kontrola.md")]),
    ])


def error_rows(readme: str) -> list[list[str]]:
    return first_table(section_lines(readme, ERRORS_HEADING))[1:]


def ai_body(sources: SiteSources) -> str:
    count = len(error_rows(sources.readme))
    return "".join([
        render_text(sources.texts["prace-s-ai"]),
        f'<p>Chyb agenta a zadání je zapsáno {count}. Každá je na <a href="data.html#chyby">stránce Data</a> s tím, jak se našla a jak se opravila.</p>',
        links([("README.md", "README – Práce s AI"), ("ai-log/", "ai-log/")]),
    ])


def index_page(sources: SiteSources) -> str:
    texts = sources.texts
    headline, *lede = texts["uvod"].strip().split("\n\n")
    blocks = "".join([
        block("1", "Plán a kritéria", "Koho do databáze pustit, koho ne a proč.", render_text(texts["plan"]) + links([("docs/01-plan-a-kriteria.md", "docs/01-plan-a-kriteria.md"), ("docs/02-metodika.md", "docs/02-metodika.md")]), "plan", True),
        block("2", "Jak jsem pracoval", "Od plánu přes sběr a ruční kontroly až po uzávěrku.", timeline(texts["casova-osa"]) + links([("docs/04-rucni-kontrola.md", "docs/04-rucni-kontrola.md")]), "postup"),
        block("AI", "Práce s AI", "Pokyny pro agenta, kontrola výstupu a chyby.", ai_body(sources), "ai"),
        block("3", "Výsledky a škálování", "Co vyšlo pro VC a PE a odhad pro všechny kategorie.", results_body(sources), "vysledky"),
        block("4", "Co chybí a další kroky", "Skutečné hranice řešení a kam dál.", render_text(texts["chybi"]), "dalsi"),
    ])
    header = (
        f'<header class="wrap hero"><p class="eyebrow">Investor Intelligence Database · stav dat k {escape(data_date(sources.dataset))}</p>'
        f"<h1>{inline(headline.strip())}</h1>"
        f'<div class="lede">{render_text(chr(10).join(lede))}</div>'
        f"{headline_stats(sources.dataset)}{funnel_svg(sources.dataset)}"
        '<div class="cta"><a class="btn primary" href="#postup">Jak jsem postupoval</a><a class="btn" href="data.html">Prohlédnout data</a></div></header>'
    )
    section = f'<section><div class="wrap"><p class="eyebrow">Projekt</p><h2>Plán, postup, výsledky</h2><div class="blocks">{blocks}</div>{documents_links()}</div></section>'
    return page("Investor Intelligence Database", header + section, "index")


def documents_links() -> str:
    return f'<h3 class="docs">Plné dokumenty</h3>{links(list(DOCUMENTS))}'


def reason_bars(dataset: Dataset) -> str:
    counts = exclusion_reason_counts(dataset.investors)
    maximum = max(counts.values())
    bars = "".join(
        f'<div class="bar"><span>{escape(REASON_LABELS[reason])}</span><span class="t"><span style="width:{100 * count / maximum:.1f}%"></span></span><span class="v">{count}</span></div>'
        for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    )
    return f'<div class="panel"><h3>Proč je vyloučeno {sum(counts.values())} subjektů</h3><div class="bars">{bars}</div></div>'


def mean_minutes(total: Decimal, count: int) -> str:
    return (format_amount_decimal(total / count) + " min") if count else "–"


def format_amount_decimal(value: Decimal) -> str:
    return f"{value:.1f}".replace(".", ",")


def time_panel(dataset: Dataset) -> str:
    model = {summary.activity: summary for summary in effort_summaries([row for row in dataset.effort_log if row["actor"] == EFFORT_ACTOR_MODEL])}
    labels = (
        (EFFORT_TRIAGE, "rychlá triáž subjektu"),
        (EFFORT_VERIFICATION, "plné ověření subjektu (VC)"),
        (EFFORT_COMPLETION, "doplnění polí zadání (VC)"),
        (EFFORT_CATEGORY_VERIFICATION, "ověření v kategorii PE"),
    )
    lines = ['<span class="h">Model, průměr na subjekt</span>']
    for activity, label in labels:
        if activity in model:
            summary = model[activity]
            lines.append(f"<span>{escape(label)}</span><b>{format_amount_decimal(Decimal(str(summary.mean_minutes)))} min</b>")
    lines.append('<span class="h">Člověk (R1), průměr</span>')
    for label, rows in (
        ("kontrola investora VC", [row for row in dataset.reviews if row["category"] == CATEGORY_VC]),
        ("kontrola investora PE", [row for row in dataset.reviews if row["category"] == CATEGORY_PE]),
        ("kontrola faktu", dataset.fact_reviews),
    ):
        for effort in review_efforts(rows):
            lines.append(f"<span>{escape(label)}</span><b>{mean_minutes(effort.total_minutes, effort.timed_reviews)}</b>")
    return f'<div class="panel"><h3>Kolik práce stojí záznam</h3><div class="time">{"".join(lines)}</div></div>'


def fact_value(fact: Row) -> str:
    field = fact["field"]
    if field in MONEY_FACT_FIELDS and fact["currency"]:
        return f"{format_amount(Decimal(fact['value']))} {fact['currency']}"
    if field in LIST_LABELS:
        labels = LIST_LABELS[field]
        return ", ".join(labels.get(code, code) for code in fact["value"].split(";"))
    if field == "duvod_vylouceni":
        return REASON_LABELS.get(fact["value"], fact["value"])
    return fact["value"]


def fact_verdicts(dataset: Dataset) -> dict[str, list[tuple[str, str]]]:
    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for row in dataset.fact_reviews:
        if row["verdict"]:
            grouped[row["fact_id"]].append((row["review_round"], row["verdict"]))
    return grouped


def fact_item(fact: Row, source: Row, verdicts: list[tuple[str, str]]) -> str:
    details = [fact_value(fact)]
    details += [f"fond {fact['fund_name']}"] if fact["fund_name"] else []
    details += [f"k {fact['value_as_of']}"] if fact["value_as_of"] else []
    badges = "".join(
        f'<span class="vd {escape(verdict)}">R1 {escape(ROUND_LABELS[review_round])}: {escape(FACT_VERDICT_LABELS[verdict])}</span>'
        for review_round, verdict in verdicts
    )
    return (
        f'<li><span class="f">{escape(FIELD_LABELS[fact["field"]])}</span>'
        f'<span class="val">{escape(" · ".join(details))} <a href="{escape(source["url"])}" rel="noopener">{escape(source["publisher"])} ↗</a> '
        f'<span class="mono">{escape(fact["fact_id"])}, přístup {escape(fact["accessed_at"])}</span></span>'
        f'<span class="badges">{badges}</span></li>'
    )


def capital_text(summary: CapitalSummary) -> str:
    parts = []
    if summary.raised:
        parts.append(f"získáno {format_raised(summary)}")
    if summary.targets:
        parts.append(f"cíl {format_amounts(summary.targets)}")
    if summary.invested:
        parts.append(f"investováno {format_amounts(summary.invested)}")
    if summary.aum:
        parts.append(f"AUM {format_amount(Decimal(summary.aum))} {summary.aum_currency}")
    if summary.conflicts:
        parts.append("konflikt zdrojů")
    return "; ".join(parts) or "–"


def investor_row(investor: Row, facts: list[Row], sources_by_id: dict[str, Row], verdicts: dict[str, list[tuple[str, str]]], context: dict[str, str]) -> str:
    pill_class, pill_label = STATUS_PILLS[investor["verification_status"]]
    status = f'<span class="pill {pill_class}">{pill_label}</span>'
    if context.get("pe"):
        pe_class, pe_label = STATUS_PILLS[context["pe"]]
        status += f' <span class="pill {pe_class}">PE: {pe_label}</span>'
    note = REASON_LABELS[investor["exclusion_reason"]] if investor["exclusion_reason"] else context.get("review", "–")
    items = "".join(fact_item(fact, sources_by_id[fact["source_id"]], verdicts.get(fact["fact_id"], [])) for fact in facts)
    search = escape(f"{investor['name']} {investor['investor_id']}".lower())
    return (
        f'<details class="inv" data-status="{investor["verification_status"]}" data-search="{search}">'
        f'<summary><span class="name"><b>{escape(investor["name"])}</b><span class="mono">{investor["investor_id"]}</span></span>'
        f'<span class="st">{status}</span><span class="cap">{escape(context.get("capital", "–"))}</span>'
        f'<span class="note">{escape(note)}</span><span class="mono cnt">{len(facts)} faktů ›</span></summary>'
        f'<ul class="facts">{items}</ul></details>'
    )


def investor_contexts(dataset: Dataset) -> dict[str, dict[str, str]]:
    contexts: dict[str, dict[str, str]] = defaultdict(dict)
    for summary in investor_capital(dataset, dataset.investors):
        contexts[summary.investor_id]["capital"] = capital_text(summary)
    for row in dataset.category_assessments:
        if row["category"] == CATEGORY_PE:
            contexts[row["investor_id"]]["pe"] = row["verification_status"]
    for row in dataset.reviews:
        if row["verdict"] and row["reviewer"] == REVIEWER_PRIMARY and row["category"] == CATEGORY_VC:
            contexts[row["investor_id"]]["review"] = f"R1: {INVESTOR_VERDICT_LABELS[row['verdict']]}"
    return contexts


def investor_list(dataset: Dataset) -> str:
    facts_by_investor: dict[str, list[Row]] = defaultdict(list)
    for fact in dataset.facts:
        facts_by_investor[fact["investor_id"]].append(fact)
    sources_by_id = {row["source_id"]: row for row in dataset.sources}
    verdicts = fact_verdicts(dataset)
    contexts = investor_contexts(dataset)
    order = {status: index for index, status in enumerate(STATUSES)}
    investors = sorted(dataset.investors, key=lambda row: (order[row["verification_status"]], row["name"].lower()))
    rows = "".join(
        investor_row(investor, facts_by_investor[investor["investor_id"]], sources_by_id, verdicts, contexts[investor["investor_id"]])
        for investor in investors
    )
    counts = status_counts(dataset.investors)
    chips = [f'<button class="chip" data-f="all" aria-pressed="true">Vše · {len(dataset.investors)}</button>']
    chips += [
        f'<button class="chip" data-f="{status}" aria-pressed="false">{STATUS_PILLS[status][1]} · {counts[status]}</button>'
        for status in STATUSES
    ]
    filters = (
        f'<div class="filters" role="group" aria-label="Filtr podle statusu">{"".join(chips)}'
        '<input id="q" type="search" placeholder="Hledat investora" aria-label="Hledat investora"></div>'
    )
    head = '<div class="invhead"><span>Investor</span><span>Status</span><span>Kapitál podle typu</span><span>Důvod nebo verdikt R1</span><span></span></div>'
    return f'{filters}<div class="invlist">{head}{rows}</div>'


def activity_text(evidence: InvestorEvidence) -> str:
    fact = evidence.activity_fact
    if fact is None:
        return "–"
    label = fact["value"] if evidence.is_investment else f"nový fond: {fact['fund_name']}"
    return f"{label} ({fact['value_as_of']})"


def verified_table(dataset: Dataset) -> str:
    sources_by_id = {row["source_id"]: row for row in dataset.sources}
    rows = []
    for evidence in verified_evidence(dataset):
        investor = evidence.investor
        fact = evidence.activity_fact
        source = (
            f'<a href="{escape(sources_by_id[fact["source_id"]]["url"])}" rel="noopener">{escape(sources_by_id[fact["source_id"]]["publisher"])} ↗</a>'
            if fact
            else "–"
        )
        rows.append(
            f'<tr><td><b>{escape(investor["name"])}</b></td><td class="mono">{escape(investor["registry_id"])}</td>'
            f'<td>{escape(TYPE_LABELS[investor["investor_type"]])}</td><td>{escape(activity_text(evidence))}</td><td>{source}</td></tr>'
        )
    head = "<tr><th>Investor</th><th>IČO</th><th>Typ</th><th>Poslední doložená investice</th><th>Zdroj</th></tr>"
    return (
        f'<h3 id="overeni" class="docs">Ověření investoři ({len(rows)})</h3>'
        f'<div class="tablewrap"><table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'
        '<p class="note-small">U investorů bez doložené investice je uveden nejnovější doložený fond (kritérium Z4).</p>'
    )


def stories(readme: str) -> str:
    cards = "".join(
        f'<div class="story"><span class="k">chyba {escape(number)}</span><p>{inline(error)}</p>'
        f'<p class="found"><b>Jak se našla:</b> {inline(found)}</p><p class="fix"><b>Oprava:</b> {inline(fix)}</p></div>'
        for number, error, found, fix in error_rows(readme)
    )
    return f'<div class="stories">{cards}</div>'


def data_page(sources: SiteSources) -> str:
    dataset = sources.dataset
    body = (
        '<section><div class="wrap"><p class="eyebrow">Data</p><h2>Co je v databázi</h2>'
        f"{render_text(sources.texts['data'])}{funnel_svg(dataset)}"
        f'<div class="grid2">{reason_bars(dataset)}{time_panel(dataset)}</div>'
        f"{verified_table(dataset)}"
        f'<h3 class="docs">Všechny nalezené subjekty</h3>{investor_list(dataset)}'
        f'<h2 id="chyby" class="spaced">Co se pokazilo a jak se to opravilo</h2>{render_text(sources.texts["chyby"])}{stories(sources.readme)}'
        f"{links([('data/', 'data/ (CSV)'), ('README.md', 'README')])}</div></section>"
    )
    return page("Data – Investor Intelligence Database", body, "data")


def current_marker(current: str, href: str) -> str:
    return ' aria-current="page"' if current == "data" and href == "data.html" else ""


def navigation(current: str) -> str:
    items = [("index.html#plan", "Plán"), ("index.html#postup", "Postup"), ("index.html#ai", "Práce s AI"), ("index.html#vysledky", "Výsledky"), ("index.html#dalsi", "Co chybí"), ("data.html", "Data")]
    anchors = "".join(
        f'<a href="{href}"{current_marker(current, href)}>{label}</a>' for href, label in items
    )
    return (
        f'<nav class="top" aria-label="Hlavní navigace"><div class="wrap"><a class="brand" href="index.html">Investor Intelligence</a>'
        f'{anchors}<a href="{REPOSITORY_URL}">GitHub ↗</a></div></nav>'
    )


def page(title: str, body: str, current: str) -> str:
    return (
        '<!doctype html>\n<html lang="cs">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{escape(title)}</title>\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">\n'
        '<link rel="stylesheet" href="style.css">\n</head>\n<body>\n'
        f"{navigation(current)}\n{body}\n"
        f'<footer><div class="wrap">Vygenerováno příkazem <code>python -m investor_db site</code> z <code>data/*.csv</code>, <code>docs/</code> a <code>{TEXTS_DIR}/</code>. '
        f'Zdroje jsou veřejné a u každého faktu uvedené s datem přístupu. <a href="{REPOSITORY_URL}">github.com/osho4753/investor-db</a></div></footer>\n'
        '<script src="app.js"></script>\n</body>\n</html>\n'
    )


def build_site(root: Path) -> dict[str, str]:
    sources = load_sources(root)
    return {
        "index.html": index_page(sources),
        "data.html": data_page(sources),
        "style.css": STYLE,
        "app.js": SCRIPT,
    }


def write_site(root: Path, output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in build_site(root).items():
        target = output / name
        target.write_text(content, encoding="utf-8", newline="\n")
        written.append(target)
    return written


SCRIPT: Final = """(function () {
  var chips = document.querySelectorAll(".chip");
  var query = document.getElementById("q");
  if (!query) { return; }
  var filter = "all";
  function apply() {
    var text = query.value.trim().toLowerCase();
    document.querySelectorAll("details.inv").forEach(function (row) {
      var visible = (filter === "all" || row.dataset.status === filter) && (!text || row.dataset.search.indexOf(text) !== -1);
      row.hidden = !visible;
    });
  }
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      filter = chip.dataset.f;
      chips.forEach(function (other) { other.setAttribute("aria-pressed", String(other === chip)); });
      apply();
    });
  });
  query.addEventListener("input", apply);
})();
"""

STYLE: Final = """:root{
  --bg:#eef1f4;--paper:#ffffff;--ink:#141d26;--muted:#56616d;--line:#d3d9e0;
  --accent:#2340a0;--accent-soft:#e2e8f8;
  --ok:#1d7a4e;--ok-soft:#dcefe5;--cand:#a36b0c;--cand-soft:#f6ead2;--out:#7b8590;--out-soft:#e4e8ec;--bad:#b0362b;
  --display:"Bricolage Grotesque","Avenir Next","Segoe UI",system-ui,sans-serif;
  --body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0f151b;--paper:#17202a;--ink:#e6ebf0;--muted:#9aa6b2;--line:#2b3744;
  --accent:#8ea8ff;--accent-soft:#1f2a4a;
  --ok:#5fc996;--ok-soft:#163327;--cand:#e2ad4b;--cand-soft:#3a2d12;--out:#8f9aa6;--out-soft:#242e38;--bad:#f0877c;color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f151b;--paper:#17202a;--ink:#e6ebf0;--muted:#9aa6b2;--line:#2b3744;
  --accent:#8ea8ff;--accent-soft:#1f2a4a;
  --ok:#5fc996;--ok-soft:#163327;--cand:#e2ad4b;--cand-soft:#3a2d12;--out:#8f9aa6;--out-soft:#242e38;--bad:#f0877c;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55}
a{color:var(--accent)}
code{font-family:var(--mono);font-size:.86em}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1040px;margin:0 auto;padding-inline:16px}
nav.top{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;flex-wrap:wrap;gap:4px 18px;align-items:center;padding-block:10px}
nav.top .brand{font-family:var(--display);font-weight:700;margin-right:auto;color:var(--ink);text-decoration:none}
nav.top a{text-decoration:none;font-size:.92rem;color:var(--muted)}
nav.top a:hover,nav.top a[aria-current]{color:var(--ink)}
.hero{padding-block:56px 40px}
section{padding-block:48px}
.eyebrow{font-family:var(--mono);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
h1,h2,h3{font-family:var(--display);line-height:1.12;text-wrap:balance;margin:0}
h1{font-size:clamp(2rem,5.4vw,3.4rem);font-weight:700;max-width:20ch}
h2{font-size:clamp(1.5rem,3.4vw,2.1rem);font-weight:700;margin-bottom:10px}
h2.spaced{margin-top:56px}
h3{font-size:1.15rem;font-weight:700}
h3.docs{margin-top:28px;margin-bottom:10px}
.note-small{font-size:.85rem;color:var(--muted);margin-top:8px}
h4{margin:6px 0 0;font-size:1rem}
.lede p{font-size:1.1rem;color:var(--muted);max-width:66ch}
p{max-width:70ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:30px}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:4px;min-width:0}
.stat .n{font-family:var(--display);font-size:2.1rem;font-weight:700;font-variant-numeric:tabular-nums;line-height:1}
.stat .l{font-weight:600}
.stat .s{font-size:.84rem;color:var(--muted)}
.cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.btn{display:inline-block;text-decoration:none;padding:10px 16px;border-radius:8px;font-weight:600;border:1px solid var(--line);color:var(--ink);background:var(--paper)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.funnel{margin-top:26px;background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px;overflow-x:auto}
.funnel svg{display:block;width:100%;min-width:560px;height:auto}
.funnel text{font-family:var(--body);font-size:13px;fill:var(--ink)}
.funnel .lbl{fill:var(--muted);font-size:12px}
.funnel .in{fill:var(--paper);font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:.85rem;color:var(--muted);margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}
.blocks{display:flex;flex-direction:column;gap:14px;margin-top:22px}
details.block{background:var(--paper);border:1px solid var(--line);border-radius:10px}
details.block>summary{cursor:pointer;list-style:none;padding:20px;display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start}
details.block>summary::-webkit-details-marker{display:none}
.num{font-family:var(--mono);font-size:.85rem;color:var(--accent);border:1px solid var(--accent);border-radius:50%;width:30px;height:30px;display:grid;place-items:center}
.sumtxt p{margin:6px 0 0;color:var(--muted)}
.chev{font-family:var(--mono);color:var(--muted);transition:transform .2s}
details[open]>summary .chev{transform:rotate(90deg)}
.body{padding:0 20px 22px 66px;display:flex;flex-direction:column;gap:12px;min-width:0}
.body p{margin:0}
@media (max-width:600px){.body{padding-left:20px}}
.timeline{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.timeline li{display:grid;grid-template-columns:110px 1fr;gap:14px;padding-block:12px;border-top:1px solid var(--line)}
.timeline li:first-child{border-top:0}
.timeline .d{font-family:var(--mono);font-size:.82rem;color:var(--muted);padding-top:3px}
.timeline h4{margin:0}
.timeline p{margin:4px 0 0;font-size:.94rem;color:var(--muted)}
@media (max-width:520px){.timeline li{grid-template-columns:1fr;gap:2px}}
.links{display:flex;flex-wrap:wrap;gap:8px}
.links a{font-size:.86rem;font-family:var(--mono);text-decoration:none;border:1px solid var(--line);padding:4px 10px;border-radius:6px;background:var(--paper)}
ul.clean{margin:0;padding-left:18px;max-width:70ch}
ul.clean li{margin:4px 0}
.tablewrap{overflow-x:auto;background:var(--paper);border:1px solid var(--line);border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:.86rem;min-width:820px}
th{text-align:left;font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600;padding:10px 12px;border-bottom:1px solid var(--line)}
td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;margin-top:24px}
@media (max-width:760px){.grid2{grid-template-columns:1fr}}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px;min-width:0}
.panel h3{margin-bottom:12px}
.bars{display:flex;flex-direction:column;gap:7px}
.bar{display:grid;grid-template-columns:minmax(0,190px) 1fr 28px;gap:10px;align-items:center;font-size:.88rem}
.bar .t{height:12px;background:var(--out-soft);border-radius:3px;overflow:hidden}
.bar .t span{display:block;height:100%;background:var(--out)}
.bar .v{font-family:var(--mono);text-align:right;font-variant-numeric:tabular-nums}
.time{display:grid;grid-template-columns:1fr auto;gap:8px 14px;font-size:.92rem}
.time b{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
.time .h{grid-column:1/-1;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-top:6px}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:26px 0 12px}
.chip{border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:6px 12px;font:inherit;font-size:.88rem;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.filters input{margin-left:auto;font:inherit;font-size:.9rem;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);min-width:0;width:220px}
.invlist{background:var(--paper);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.invhead,details.inv>summary{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.9fr) minmax(0,1.8fr) minmax(0,1fr) 80px;gap:12px;padding:10px 14px;align-items:start}
.invhead{font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600;border-bottom:1px solid var(--line)}
details.inv{border-bottom:1px solid var(--line)}
details.inv:last-child{border-bottom:0}
details.inv>summary{cursor:pointer;list-style:none;font-size:.9rem}
details.inv>summary::-webkit-details-marker{display:none}
details.inv>summary:hover{background:var(--bg)}
details.inv .name{display:flex;flex-direction:column;min-width:0}
details.inv .cap{font-size:.84rem;overflow-wrap:anywhere}
details.inv .note{font-size:.84rem;color:var(--muted)}
details.inv .cnt{text-align:right}
@media (max-width:760px){.invhead{display:none}details.inv>summary{grid-template-columns:1fr}details.inv .cnt{text-align:left}}
.pill{display:inline-block;font-size:.76rem;font-weight:600;padding:2px 9px;border-radius:999px;white-space:nowrap;margin:0 4px 4px 0}
.pill.ok{background:var(--ok-soft);color:var(--ok)}
.pill.cand{background:var(--cand-soft);color:var(--cand)}
.pill.out{background:var(--out-soft);color:var(--out)}
.mono{font-family:var(--mono);font-size:.78rem;color:var(--muted)}
ul.facts{list-style:none;margin:0;padding:8px 14px 14px;display:flex;flex-direction:column;gap:6px;background:var(--bg)}
ul.facts li{display:grid;grid-template-columns:160px minmax(0,1fr) auto;gap:10px;align-items:baseline;font-size:.85rem;padding-block:4px;border-bottom:1px dashed var(--line)}
ul.facts li:last-child{border-bottom:0}
ul.facts .f{color:var(--muted)}
ul.facts .val{overflow-wrap:anywhere}
ul.facts .val a{font-size:.8rem;margin-left:4px}
.badges{display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end}
.vd{font-family:var(--mono);font-size:.72rem;padding:1px 6px;border-radius:4px;white-space:nowrap}
.vd.spravne{background:var(--ok-soft);color:var(--ok)}
.vd.chybne{background:var(--bad);color:var(--paper)}
.vd.nelze_overit{background:var(--cand-soft);color:var(--cand)}
@media (max-width:560px){ul.facts li{grid-template-columns:1fr}.badges{justify-content:flex-start}}
.stories{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin:22px 0}
.story{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:16px;min-width:0;display:flex;flex-direction:column;gap:6px}
.story .k{font-family:var(--mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
.story p{margin:0;font-size:.9rem}
.story .found{color:var(--muted)}
.story .fix{color:var(--ok)}
footer{padding-block:40px;color:var(--muted);font-size:.86rem;border-top:1px solid var(--line)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

