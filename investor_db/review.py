import math
import random

from investor_db.io import Row

FACT_SAMPLE_SEED = 2026
FACT_SAMPLE_MARGIN = 0.15
FACT_SAMPLE_Z = 1.96
FACT_SAMPLE_PROPORTION = 0.5


def fact_sample_size(population: int) -> int:
    if population <= 0:
        return 0
    infinite_population_size = FACT_SAMPLE_Z**2 * FACT_SAMPLE_PROPORTION * (1 - FACT_SAMPLE_PROPORTION) / FACT_SAMPLE_MARGIN**2
    corrected_size = infinite_population_size / (1 + (infinite_population_size - 1) / population)
    return min(population, math.ceil(corrected_size))


def sample_fact_ids(fact_ids: list[str], seed: int = FACT_SAMPLE_SEED) -> list[str]:
    population = sorted(set(fact_ids))
    return sorted(random.Random(seed).sample(population, fact_sample_size(len(population))))


def facts_from(fact_ids: list[str], first_fact_id: str) -> list[str]:
    return sorted(fact_id for fact_id in set(fact_ids) if fact_id >= first_fact_id)


def has_round(fact_reviews: list[Row], reviewer: str, review_round: str) -> bool:
    return any(row["reviewer"] == reviewer and row["review_round"] == review_round for row in fact_reviews)


def add_pending_reviews(
    existing: list[Row],
    columns: tuple[str, ...],
    target_column: str,
    target_ids: list[str],
    reviewer: str,
    defaults: Row | None = None,
) -> list[Row]:
    review_round = (defaults or {}).get("review_round")
    already_listed = {
        row[target_column]
        for row in existing
        if row["reviewer"] == reviewer and (review_round is None or row.get("review_round") == review_round)
    }
    pending = [
        {**dict.fromkeys(columns, ""), **(defaults or {}), target_column: target_id, "reviewer": reviewer}
        for target_id in target_ids
        if target_id not in already_listed
    ]
    return existing + pending
