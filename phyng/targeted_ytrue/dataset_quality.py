"""Dataset quality metrics for v5.7.3."""

from __future__ import annotations

from collections import Counter

from phyng.targeted_ytrue.schemas import DatasetQuality


def build_dataset_quality(dataset: dict, new_accepted_count: int, human_review_count: int) -> DatasetQuality:
    records = dataset.get("records", [])
    source_count = len({record.get("source_id") for record in records})
    total = len(records)
    if total >= 10 and source_count >= 2:
        quality_status = "MULTI_SOURCE_THRESHOLD_REACHED"
        readiness = "READY_FOR_OUT_OF_SOURCE_CONTROL"
    elif source_count >= 2:
        quality_status = "MULTI_SOURCE_N_SMALL"
        readiness = "PARTIAL_MULTI_SOURCE_N_SMALL"
    elif total > 0:
        quality_status = "SINGLE_SOURCE_N_SMALL"
        readiness = "PARTIAL_SINGLE_SOURCE_ONLY"
    else:
        quality_status = "REQUIRES_MORE_YTRUE"
        readiness = "NOT_READY_NO_YTRUE"
    flags = []
    if human_review_count:
        flags.append("HUMAN_FIGURE_REVIEW_LIMITATIONS_PRESENT")
    if total < 10:
        flags.append("TOTAL_YTRUE_BELOW_THRESHOLD_10")
    if source_count < 2:
        flags.append("INDEPENDENT_SOURCE_COUNT_BELOW_2")
    return DatasetQuality(
        dataset_id=dataset.get("dataset_id", "VISIBILITY-DECOHERENCE-EXPANDED-YTRUE-DATASET-v5_7_3"),
        total_accepted_ytrue_count=total,
        new_accepted_ytrue_count=new_accepted_count,
        independent_source_count=source_count,
        observable_class_distribution=dict(Counter(record.get("observable_class") for record in records)),
        qc_status_distribution=dict(Counter(record.get("qc_status") for record in records)),
        source_distribution=dict(Counter(record.get("source_id") for record in records)),
        condition_key_distribution=dict(Counter(",".join(sorted((record.get("conditions") or {}).keys())) or "none" for record in records)),
        limitation_flags=flags,
        quality_status=quality_status,
        benchmark_readiness=readiness,
        notes=["Dataset quality does not compute PredictiveGain or validate Frontera C."],
    )
