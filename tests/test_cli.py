from pathlib import Path

import pytest
from conftest import build_valid_dataset

from investor_db.__main__ import main
from investor_db.io import TABLE_COLUMNS, Dataset, load_dataset, table_path, write_table
from investor_db.review import sample_fact_ids


def write_dataset(data_dir: Path, dataset: Dataset) -> None:
    for table, columns in TABLE_COLUMNS.items():
        write_table(table_path(data_dir, table), columns, getattr(dataset, table))


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    write_dataset(tmp_path, build_valid_dataset())
    return tmp_path


def test_validate_succeeds_on_valid_data(data_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--data-dir", str(data_dir), "validate"]) == 0
    assert "bez chyb" in capsys.readouterr().out


def test_validate_fails_and_lists_issues(data_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = build_valid_dataset()
    dataset.investors[0]["registry_id"] = "12345678"
    write_dataset(data_dir, dataset)

    assert main(["--data-dir", str(data_dir), "validate"]) == 1
    assert "není platné IČO" in capsys.readouterr().out


def test_metrics_refuses_invalid_data(data_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    dataset = build_valid_dataset()
    dataset.investors[0]["name"] = ""
    write_dataset(data_dir, dataset)

    assert main(["--data-dir", str(data_dir), "metrics"]) == 1
    assert "Metriky se nepočítají" in capsys.readouterr().out


def test_metrics_prints_report(data_dir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--data-dir", str(data_dir), "metrics"]) == 0
    assert "Precision" in capsys.readouterr().out


def test_review_template_adds_rows_for_second_reviewer(data_dir: Path) -> None:
    assert main(["--data-dir", str(data_dir), "review-template", "--reviewer", "R2"]) == 0

    reviews = load_dataset(data_dir).reviews
    assert [(row["investor_id"], row["reviewer"], row["verdict"]) for row in reviews] == [
        ("inv-0001", "R1", "TP"),
        ("inv-0001", "R2", ""),
    ]


def test_fact_review_template_adds_sample(data_dir: Path) -> None:
    assert main(["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R2"]) == 0

    dataset = load_dataset(data_dir)
    listed = [row for row in dataset.fact_reviews if row["reviewer"] == "R2"]
    assert {row["fact_id"] for row in listed} == set(sample_fact_ids([row["fact_id"] for row in dataset.facts]))
    assert {row["review_round"] for row in listed} == {"vzorek"}
    assert main(["--data-dir", str(data_dir), "validate"]) == 0


def test_fact_review_template_keeps_existing_sample(data_dir: Path) -> None:
    before = load_dataset(data_dir).fact_reviews

    assert main(["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R1"]) == 0

    assert load_dataset(data_dir).fact_reviews == before


def test_completion_round_lists_all_facts_from_given_id(data_dir: Path) -> None:
    arguments = ["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R1"]
    assert main([*arguments, "--round", "po_doplneni", "--from-fact", "f-00005"]) == 0

    dataset = load_dataset(data_dir)
    completion = [row for row in dataset.fact_reviews if row["review_round"] == "po_doplneni"]
    expected = sorted(row["fact_id"] for row in dataset.facts if row["fact_id"] >= "f-00005")
    assert [row["fact_id"] for row in completion] == expected
    assert [row["fact_id"] for row in dataset.fact_reviews if row["review_round"] == "vzorek"] == ["f-00001"]
    assert main(["--data-dir", str(data_dir), "validate"]) == 0


def test_completion_round_requires_first_fact(data_dir: Path) -> None:
    arguments = ["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R1", "--round", "po_doplneni"]

    assert main(arguments) == 1


def test_missing_data_file_is_reported(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--data-dir", str(tmp_path), "validate"]) == 2
    assert "Chyba načtení dat" in capsys.readouterr().out


def test_correction_round_lists_given_facts_even_if_reviewed_before(data_dir: Path) -> None:
    arguments = ["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R1", "--round", "po_oprave"]

    assert main([*arguments, "--facts", "f-00001,f-00003,f-99999"]) == 0

    dataset = load_dataset(data_dir)
    assert [row["fact_id"] for row in dataset.fact_reviews if row["review_round"] == "po_oprave"] == ["f-00001", "f-00003"]
    assert [row["fact_id"] for row in dataset.fact_reviews if row["review_round"] == "vzorek"] == ["f-00001"]
    assert main(["--data-dir", str(data_dir), "validate"]) == 0
    assert main([*arguments, "--facts", "f-00001"]) == 0
    assert len(load_dataset(data_dir).fact_reviews) == 3


def test_correction_round_requires_facts(data_dir: Path) -> None:
    arguments = ["--data-dir", str(data_dir), "fact-review-template", "--reviewer", "R1", "--round", "po_oprave"]

    assert main(arguments) == 1
