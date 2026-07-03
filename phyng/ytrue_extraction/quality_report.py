"""Generate quality report for the assembled y_true dataset."""

from __future__ import annotations

from phyng.ytrue_extraction.schemas import DatasetQualityReport, QueueItem


def build_quality_report(
    targets: list[dict],
    candidates: list[dict],
    blocked_list: list[dict],
    table_q: list[QueueItem],
    fig_q: list[QueueItem],
    pub_q: list[QueueItem],
    supp_q: list[QueueItem],
    accepted_count: int,
    ready_for_predictive_gain: bool,
) -> DatasetQualityReport:
    """Build the dataset quality report summarising audit findings."""
    qc_pass = sum(1 for c in candidates if c["qc_status"] == "PASS")
    qc_fail = len(candidates) - qc_pass

    # Source coverage issues: candidates where hash is missing or local PDF missing
    coverage_issues = sum(1 for c in candidates if not c["can_enter_dataset"] and "provenance" in c["qc_status"].lower())

    # Prediction matching issues: accepted records with 0 matched predictions
    # (not applicable in this simplified schema, default to 0)
    pred_issues = 0

    if ready_for_predictive_gain:
        status = "YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN"
    elif accepted_count > 0:
        status = "YTRUE_DATASET_READY_PARTIAL"
    else:
        status = "YTRUE_DATASET_EMPTY_NEEDS_EXTRACTION"

    recs = []
    if accepted_count < 3:
        recs.append("Acquire additional y_true measurements to meet the minimum viable threshold (>= 3).")
    if len(table_q) > 0:
        recs.append("Execute manual table review sprint to extract values from local PDFs.")
    if len(fig_q) > 0:
        recs.append("Initiate figure digitization workflow for queued items.")

    return DatasetQualityReport(
        target_count=len(targets),
        candidate_count=len(candidates),
        accepted_y_true_count=accepted_count,
        blocked_count=len(blocked_list),
        manual_table_queue_count=len(table_q),
        figure_digitization_queue_count=len(fig_q),
        public_dataset_lookup_count=len(pub_q),
        supplementary_lookup_count=len(supp_q),
        qc_pass_count=qc_pass,
        qc_fail_count=qc_fail,
        unit_normalization_issues=0,
        source_coverage_issues=coverage_issues,
        prediction_matching_issues=pred_issues,
        readiness_status=status,
        recommendations=recs,
    )

