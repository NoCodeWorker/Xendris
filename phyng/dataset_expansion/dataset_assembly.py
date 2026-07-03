"""Dataset assembly for visibility/decoherence y_true."""

from __future__ import annotations

from collections import Counter

from phyng.dataset_expansion.schemas import VisibilityDecoherenceDataset, YTrueCandidate


LIMITATION_FLAGS = [
    "SINGLE_SOURCE",
    "N_SMALL_4",
    "PASS_WITH_LIMITATIONS_YTRUE",
    "DATASET_EXPANSION_ONLY",
    "NOT_VALIDATION",
    "NOT_PHYSICAL_CLAIM",
]


def assemble_dataset(accepted: list[YTrueCandidate]) -> VisibilityDecoherenceDataset:
    records = [item.model_dump() for item in accepted]
    source_count = len({item.source_id for item in accepted})
    observable_distribution = Counter(item.observable_class for item in accepted)
    condition_distribution = Counter(key for item in accepted for key in item.conditions.keys())
    return VisibilityDecoherenceDataset(
        dataset_id="VISIBILITY-DECOHERENCE-DATASET-v5_7",
        version="v5.7",
        records=records,
        source_count=source_count,
        accepted_ytrue_count=len(accepted),
        observable_class_distribution=dict(observable_distribution),
        condition_key_distribution=dict(condition_distribution),
        limitation_flags=LIMITATION_FLAGS,
        notes=[
            "Dataset expansion is not candidate rescue.",
            "LOG_BOUNDARY remains archived as a validation candidate.",
        ],
    )
