import math
import random

from investor_db.io import Row

FACT_SAMPLE_SEED = 2026
FACT_SAMPLE_MARGIN = 0.10
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


def add_pending_reviews(
    existing: list[Row],
    columns: tuple[str, ...],
    target_column: str,
    target_ids: list[str],
    reviewer: str,
) -> list[Row]:
    already_listed = {row[target_column] for row in existing if row["reviewer"] == reviewer}
    pending = [
        {**dict.fromkeys(columns, ""), target_column: target_id, "reviewer": reviewer}
        for target_id in target_ids
        if target_id not in already_listed
    ]
    return existing + pending
