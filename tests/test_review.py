import pytest

from investor_db.review import add_pending_reviews, fact_sample_size, sample_fact_ids
from investor_db.schema import REVIEW_COLUMNS


@pytest.mark.parametrize(
    ("population", "expected"),
    [(0, 0), (1, 1), (20, 17), (150, 59), (300, 73), (10000, 96)],
)
def test_fact_sample_size(population: int, expected: int) -> None:
    assert fact_sample_size(population) == expected


def test_fact_sample_is_reproducible_subset() -> None:
    fact_ids = [f"f-{number:05d}" for number in range(1, 301)]

    first = sample_fact_ids(fact_ids)

    assert first == sample_fact_ids(list(reversed(fact_ids)))
    assert len(first) == 73 and set(first) <= set(fact_ids)


def test_add_pending_reviews_keeps_existing_and_skips_listed() -> None:
    existing = [{"investor_id": "inv-0001", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "TP", "note": ""}]

    rows = add_pending_reviews(existing, REVIEW_COLUMNS, "investor_id", ["inv-0001", "inv-0002"], "R1")

    assert rows[0] == existing[0]
    assert rows[1:] == [{"investor_id": "inv-0002", "reviewer": "R1", "reviewed_at": "", "verdict": "", "note": ""}]


def test_add_pending_reviews_is_per_reviewer() -> None:
    existing = [{"investor_id": "inv-0001", "reviewer": "R1", "reviewed_at": "", "verdict": "", "note": ""}]

    rows = add_pending_reviews(existing, REVIEW_COLUMNS, "investor_id", ["inv-0001"], "R2")

    assert [row["reviewer"] for row in rows] == ["R1", "R2"]
