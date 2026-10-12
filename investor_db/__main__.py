import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

from investor_db.io import Dataset, SchemaError, load_dataset, table_path, write_table
from investor_db.metrics import verified_ids
from investor_db.rawtext import fetch_raw_text, find_first
from investor_db.report import render_report
from investor_db.review import add_pending_reviews, facts_from, has_round, sample_excluded_ids, sample_fact_ids
from investor_db.review_guide import GuideTemplateError, render_checklist, render_investor_checklist, sampled_fact_ids
from investor_db.schema import (
    CATEGORY_VC_EXCLUDED,
    EXCLUDED_SAMPLE_SIZE,
    STATUS_EXCLUDED,
    CATEGORY_VC,
    REVIEW_CATEGORIES,
    INVESTOR_REVIEW_ROUNDS,
    INVESTOR_ROUND_FIRST,
    FACT_REVIEW_COLUMNS,
    REVIEW_COLUMNS,
    REVIEW_ROUND_COMPLETION,
    REVIEW_ROUND_CORRECTION,
    REVIEW_ROUND_SAMPLE,
    REVIEW_ROUNDS,
    REVIEWERS,
)
from investor_db.site import SITE_DIR, write_site
from investor_db.tokens import render_usage, session_usage
from investor_db.validation import validate_dataset

DEFAULT_DATA_DIR = Path("data")
DEFAULT_RAW_CACHE_DIR = Path(tempfile.gettempdir()) / "investor-db-raw"
DEFAULT_CHECKLIST_PATH = Path("review") / "kontrolni-list-faktu.md"
DEFAULT_INVESTOR_CHECKLIST_PATH = Path("review") / "kontrolni-list-r1-v2.md"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="investor_db", description="Validace a metriky databáze investorů.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="složka s CSV soubory")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="zkontroluje integritu dat").set_defaults(handler=run_validate)
    commands.add_parser("metrics", help="vypíše metriky kvality dat").set_defaults(handler=run_metrics)
    for name, handler, help_text in (
        ("review-template", run_review_template, "doplní šablonu kontroly ověřených investorů"),
        ("fact-review-template", run_fact_review_template, "doplní šablonu kontroly vzorku faktů"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--reviewer", choices=REVIEWERS, required=True)
        command.set_defaults(handler=handler)
        if name == "review-template":
            command.add_argument("--category", choices=REVIEW_CATEGORIES, default=CATEGORY_VC)
            command.add_argument("--round", dest="investor_round", choices=INVESTOR_REVIEW_ROUNDS, default=INVESTOR_ROUND_FIRST)
        if name == "fact-review-template":
            command.add_argument("--round", dest="review_round", choices=REVIEW_ROUNDS, default=REVIEW_ROUND_SAMPLE)
            command.add_argument("--from-fact", help="u kola po_doplneni: první fact_id přidaný doplňováním")
            command.add_argument("--facts", help="u kola po_oprave: fact_id opravených faktů oddělená čárkou")
    guide = commands.add_parser("review-guide", help="vygeneruje kontrolní list faktů pro hodnotitele")
    guide.add_argument("--output", type=Path, default=DEFAULT_CHECKLIST_PATH)
    guide.set_defaults(handler=run_review_guide)
    investor_guide = commands.add_parser("investor-review-guide", help="vygeneruje kontrolní list R1-v2 ověřených investorů")
    investor_guide.add_argument("--output", type=Path, default=DEFAULT_INVESTOR_CHECKLIST_PATH)
    investor_guide.set_defaults(handler=run_investor_review_guide)
    site = commands.add_parser("site", help="vygeneruje statický web z dat a dokumentace")
    site.add_argument("--output", type=Path, default=Path(SITE_DIR))
    site.set_defaults(handler=run_site)
    tokens = commands.add_parser("tokens", help="sečte spotřebu tokenů a cenu z transkriptu Claude Code (JSONL)")
    tokens.add_argument("transcripts", type=Path, nargs="+")
    tokens.add_argument("--investors", type=int, required=True, help="počet ověřovaných investorů")
    tokens.set_defaults(handler=run_tokens)
    raw = commands.add_parser("raw-text", help="stáhne surový text stránky (mimo repozitář) a vyhledá v něm výraz")
    raw.add_argument("url")
    raw.add_argument("--grep", help="regulární výraz k vyhledání")
    raw.add_argument("--cache-dir", type=Path, default=DEFAULT_RAW_CACHE_DIR)
    raw.set_defaults(handler=run_raw_text)
    return parser


def report_issues(data_dir: Path) -> bool:
    issues = validate_dataset(load_dataset(data_dir), date.today())
    for issue in issues:
        print(issue)
    return not issues


def run_validate(args: argparse.Namespace) -> int:
    if not report_issues(args.data_dir):
        print("Validace selhala.")
        return 1
    print("Validace prošla bez chyb.")
    return 0


def run_metrics(args: argparse.Namespace) -> int:
    if not report_issues(args.data_dir):
        print("Metriky se nepočítají, dokud data neprojdou validací.")
        return 1
    print(render_report(load_dataset(args.data_dir), date.today()), end="")
    return 0


def review_targets(dataset: Dataset, category: str) -> list[str]:
    if category == CATEGORY_VC:
        return sorted(verified_ids(dataset.investors))
    if category == CATEGORY_VC_EXCLUDED:
        if any(row["category"] == CATEGORY_VC_EXCLUDED for row in dataset.reviews):
            return []
        excluded = [row["investor_id"] for row in dataset.investors if row["verification_status"] == STATUS_EXCLUDED]
        return sample_excluded_ids(excluded, EXCLUDED_SAMPLE_SIZE)
    return sorted({row["investor_id"] for row in dataset.category_assessments if row["category"] == category})


def run_review_template(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    target_ids = review_targets(dataset, args.category)
    rows = add_pending_reviews(
        dataset.reviews, REVIEW_COLUMNS, "investor_id", target_ids, args.reviewer, {"category": args.category, "review_round": args.investor_round}
    )
    write_table(table_path(args.data_dir, "reviews"), REVIEW_COLUMNS, rows)
    print(f"Přidáno {len(rows) - len(dataset.reviews)} řádků ke kontrole pro {args.reviewer}.")
    return 0


def fact_review_targets(args: argparse.Namespace, dataset: Dataset) -> list[str]:
    fact_ids = [row["fact_id"] for row in dataset.facts]
    if args.review_round == REVIEW_ROUND_COMPLETION:
        return facts_from(fact_ids, args.from_fact)
    if args.review_round == REVIEW_ROUND_CORRECTION:
        return sorted(set(args.facts.split(",")) & set(fact_ids))
    if has_round(dataset.fact_reviews, args.reviewer, REVIEW_ROUND_SAMPLE):
        return []
    return sample_fact_ids(fact_ids)


def run_fact_review_template(args: argparse.Namespace) -> int:
    if args.review_round == REVIEW_ROUND_COMPLETION and not args.from_fact:
        print("Kolo po_doplneni vyžaduje --from-fact.")
        return 1
    if args.review_round == REVIEW_ROUND_CORRECTION and not args.facts:
        print("Kolo po_oprave vyžaduje --facts.")
        return 1
    dataset = load_dataset(args.data_dir)
    targets = fact_review_targets(args, dataset)
    rows = add_pending_reviews(
        dataset.fact_reviews,
        FACT_REVIEW_COLUMNS,
        "fact_id",
        targets,
        args.reviewer,
        {"review_round": args.review_round},
    )
    write_table(table_path(args.data_dir, "fact_reviews"), FACT_REVIEW_COLUMNS, rows)
    print(
        f"Kolo {args.review_round}: {len(targets)} z {len(dataset.facts)} faktů; "
        f"přidáno {len(rows) - len(dataset.fact_reviews)} řádků ke kontrole pro {args.reviewer}."
    )
    return 0


def run_review_guide(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    try:
        checklist = render_checklist(dataset)
    except GuideTemplateError as error:
        print(f"Kontrolní list nelze vygenerovat: {error}")
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(checklist, encoding="utf-8", newline="\n")
    print(f"Kontrolní list {len(sampled_fact_ids(dataset))} faktů uložen do {args.output}.")
    return 0


def run_investor_review_guide(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.data_dir)
    try:
        checklist = render_investor_checklist(dataset)
    except GuideTemplateError as error:
        print(f"Kontrolní list nelze vygenerovat: {error}")
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(checklist, encoding="utf-8", newline="\n")
    print(f"Kontrolní list R1-v2 uložen do {args.output}.")
    return 0


def run_site(args: argparse.Namespace) -> int:
    if not report_issues(args.data_dir):
        print("Web se negeneruje, dokud data neprojdou validací.")
        return 1
    written = write_site(args.data_dir.parent, args.output)
    print(f"Web uložen do {args.output}: {', '.join(path.name for path in written)}.")
    return 0


def run_tokens(args: argparse.Namespace) -> int:
    print(render_usage(session_usage(args.transcripts), args.investors), end="")
    return 0


def run_raw_text(args: argparse.Namespace) -> int:
    page = fetch_raw_text(args.url, args.cache_dir)
    print(f"{page.status}; znaků textu: {len(page.text)}")
    if not page.has_text:
        return 1
    if args.grep:
        snippet = find_first(page.text, [re.compile(args.grep, re.IGNORECASE)])
        print(snippet if snippet is not None else "výraz nenalezen")
        return 0 if snippet is not None else 1
    print(page.text[:2000])
    return 0


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except (SchemaError, FileNotFoundError) as error:
        print(f"Chyba načtení dat: {error}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
