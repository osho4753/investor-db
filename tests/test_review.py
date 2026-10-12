import pytest

from investor_db.review import add_pending_reviews, fact_sample_size, sample_excluded_ids, sample_fact_ids
from investor_db.schema import REVIEW_COLUMNS


@pytest.mark.parametrize(
    ("population", "expected"),
    [(0, 0), (1, 1), (20, 14), (150, 34), (205, 36), (300, 38), (10000, 43)],
)
def test_fact_sample_size(population: int, expected: int) -> None:
    assert fact_sample_size(population) == expected


def test_fact_sample_is_reproducible_subset() -> None:
    fact_ids = [f"f-{number:05d}" for number in range(1, 301)]

    first = sample_fact_ids(fact_ids)

    assert first == sample_fact_ids(list(reversed(fact_ids)))
    assert len(first) == 38 and set(first) <= set(fact_ids)


def test_add_pending_reviews_keeps_existing_and_skips_listed() -> None:
    existing = [{"investor_id": "inv-0001", "reviewer": "R1", "reviewed_at": "2026-10-05", "verdict": "TP", "review_minutes": "", "note": ""}]

    rows = add_pending_reviews(existing, REVIEW_COLUMNS, "investor_id", ["inv-0001", "inv-0002"], "R1")

    assert rows[0] == existing[0]
    assert rows[1:] == [{"investor_id": "inv-0002", "reviewer": "R1", "reviewed_at": "", "verdict": "", "review_minutes": "", "note": "", "category": "", "review_round": ""}]


def test_add_pending_reviews_is_per_reviewer() -> None:
    existing = [{"investor_id": "inv-0001", "reviewer": "R1", "reviewed_at": "", "verdict": "", "review_minutes": "", "note": ""}]

    rows = add_pending_reviews(existing, REVIEW_COLUMNS, "investor_id", ["inv-0001"], "R2")

    assert [row["reviewer"] for row in rows] == ["R1", "R2"]


def test_excluded_sample_is_reproducible_and_bounded() -> None:
    ids = [f"inv-{number:04d}" for number in range(1, 33)]

    sample = sample_excluded_ids(ids, 10)

    assert sample == sample_excluded_ids(list(reversed(ids)), 10)
    assert len(sample) == 10 and set(sample) <= set(ids)
    assert sample_excluded_ids(ids[:3], 10) == ids[:3]
