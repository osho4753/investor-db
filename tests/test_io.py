from pathlib import Path

import pytest

from investor_db.io import TABLE_COLUMNS, SchemaError, load_dataset, read_table, table_path, write_table
from investor_db.schema import SOURCE_COLUMNS

REPOSITORY_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_write_and_read_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "sources.csv"
    rows = [{"source_id": "src-0001", "url": "https://example.com", "publisher": "Příklad, s.r.o.", "source_type": "media"}]

    write_table(path, SOURCE_COLUMNS, rows)

    assert read_table(path, SOURCE_COLUMNS) == rows


def test_read_table_rejects_unexpected_header(tmp_path: Path) -> None:
    path = tmp_path / "sources.csv"
    path.write_text("source_id,url\n", encoding="utf-8")

    with pytest.raises(SchemaError, match="očekávané sloupce"):
        read_table(path, SOURCE_COLUMNS)


def test_read_table_rejects_row_with_extra_values(tmp_path: Path) -> None:
    path = tmp_path / "sources.csv"
    path.write_text("source_id,url,publisher,source_type\nsrc-0001,https://example.com,X,media,navic\n", encoding="utf-8")

    with pytest.raises(SchemaError, match="více hodnot"):
        read_table(path, SOURCE_COLUMNS)


def test_read_table_fills_missing_values_with_empty_string(tmp_path: Path) -> None:
    path = tmp_path / "sources.csv"
    path.write_text("source_id,url,publisher,source_type\nsrc-0001,https://example.com\n", encoding="utf-8")

    assert read_table(path, SOURCE_COLUMNS)[0]["publisher"] == ""


def test_load_dataset_reads_all_tables(tmp_path: Path) -> None:
    for table, columns in TABLE_COLUMNS.items():
        write_table(table_path(tmp_path, table), columns, [])

    dataset = load_dataset(tmp_path)

    assert dataset.investors == [] and dataset.fact_reviews == []


def test_repository_data_files_match_schema() -> None:
    load_dataset(REPOSITORY_DATA_DIR)
