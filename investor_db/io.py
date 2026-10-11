import csv
from dataclasses import dataclass, field
from pathlib import Path

from investor_db.schema import (
    CANDIDATE_SOURCE_COLUMNS,
    CATEGORY_ASSESSMENT_COLUMNS,
    EFFORT_COLUMNS,
    FACT_COLUMNS,
    FACT_REVIEW_COLUMNS,
    FUND_COLUMNS,
    INVESTOR_COLUMNS,
    REVIEW_COLUMNS,
    SEARCH_LOG_COLUMNS,
    SOURCE_COLUMNS,
)

Row = dict[str, str]

TABLE_COLUMNS: dict[str, tuple[str, ...]] = {
    "investors": INVESTOR_COLUMNS,
    "facts": FACT_COLUMNS,
    "sources": SOURCE_COLUMNS,
    "search_log": SEARCH_LOG_COLUMNS,
    "reviews": REVIEW_COLUMNS,
    "fact_reviews": FACT_REVIEW_COLUMNS,
    "effort_log": EFFORT_COLUMNS,
    "candidate_sources": CANDIDATE_SOURCE_COLUMNS,
    "funds": FUND_COLUMNS,
    "category_assessments": CATEGORY_ASSESSMENT_COLUMNS,
}


class SchemaError(Exception):
    pass


@dataclass
class Dataset:
    investors: list[Row] = field(default_factory=list)
    facts: list[Row] = field(default_factory=list)
    sources: list[Row] = field(default_factory=list)
    search_log: list[Row] = field(default_factory=list)
    reviews: list[Row] = field(default_factory=list)
    fact_reviews: list[Row] = field(default_factory=list)
    effort_log: list[Row] = field(default_factory=list)
    candidate_sources: list[Row] = field(default_factory=list)
    funds: list[Row] = field(default_factory=list)
    category_assessments: list[Row] = field(default_factory=list)


def table_path(data_dir: Path, table: str) -> Path:
    return data_dir / f"{table}.csv"


def read_table(path: Path, columns: tuple[str, ...]) -> list[Row]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        header = tuple(reader.fieldnames or ())
        if header != columns:
            raise SchemaError(f"{path.name}: očekávané sloupce {list(columns)}, nalezené {list(header)}")
        return [_complete_row(path, reader.line_num, row) for row in reader]


def _complete_row(path: Path, line_number: int, row: dict[str | None, str | None]) -> Row:
    if None in row:
        raise SchemaError(f"{path.name}:{line_number}: řádek má více hodnot než sloupců")
    return {key: value or "" for key, value in row.items() if key is not None}


def write_table(path: Path, columns: tuple[str, ...], rows: list[Row]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_dataset(data_dir: Path) -> Dataset:
    tables = {
        table: read_table(table_path(data_dir, table), columns)
        for table, columns in TABLE_COLUMNS.items()
    }
    return Dataset(**tables)
