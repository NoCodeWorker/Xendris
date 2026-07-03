"""Dataset quality assessment."""

from __future__ import annotations

from phyng.dataset_expansion.schemas import VisibilityDecoherenceDataset, YTrueCandidate


def assess_dataset_quality(dataset: VisibilityDecoherenceDataset, rejected: list[YTrueCandidate]) -> dict:
    source_ids = {record["source_id"] for record in dataset.records}
    return {
        "artifact_id": "VISIBILITY-DECOHERENCE-DATASET-QUALITY-v5_7",
        "accepted_ytrue_count_total": dataset.accepted_ytrue_count,
        "independent_source_count": len(source_ids),
        "rejected_or_review_required_count": len(rejected),
        "quality_flags": dataset.limitation_flags,
        "blocking_limitations": [
            "single-source dataset",
            "accepted_ytrue_count_total below 10",
            "no out-of-source split possible",
        ],
        "log_boundary_remains_archived": True,
        "physical_claim_created": False,
        "frontera_c_validated": False,
    }
