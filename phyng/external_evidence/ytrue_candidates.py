"""Candidate synthesis and acceptance evaluation."""

from __future__ import annotations

from phyng.external_evidence.schemas import (
    ExternalYTrueCandidate,
    AcceptedExternalYTrueRecord,
    RejectedExternalYTrueRecord,
    TableReviewResult,
    SupplementarySearchResult,
    PublicDatasetSearchResult,
)


def process_external_candidates(
    table_results: list[TableReviewResult],
    supp_results: list[SupplementarySearchResult],
    pub_results: list[PublicDatasetSearchResult],
    inputs: dict,
) -> tuple[list[ExternalYTrueCandidate], list[AcceptedExternalYTrueRecord], list[RejectedExternalYTrueRecord]]:
    candidates: list[ExternalYTrueCandidate] = []
    accepted: list[AcceptedExternalYTrueRecord] = []
    rejected: list[RejectedExternalYTrueRecord] = []

    # Map targets and predictions for lookup
    targets = inputs.get("normalized_targets_v4_2", {}).get("normalized_targets", [])
    target_by_id = {t["target_id"]: t for t in targets}

    predictions = inputs.get("model_predictions_v4_1", {}).get("predictions", [])
    preds_by_target: dict[str, list[str]] = {}
    for p in predictions:
        t_id = p.get("target_id", "")
        p_id = p.get("prediction_id", "")
        preds_by_target.setdefault(t_id, []).append(p_id)

    # Process Track A Table Review Results
    for idx, r in enumerate(table_results, start=1):
        target = target_by_id.get(r.target_id, {})
        matched_preds = preds_by_target.get(r.target_id, [])

        blockers = list(r.blockers)
        qc_status = "PASS" if not blockers else f"FAIL_{blockers[0]}"

        # Apply y_true rules
        can_enter = True
        if r.numeric_value is None:
            can_enter = False
            blockers.append("NO_NUMERIC_VALUE")
        if not r.unit and target.get("observable_class") in {"DECOHERENCE_RATE", "CONTRAST_DECAY"}:
            can_enter = False
            blockers.append("MISSING_UNIT")
        if not r.source_id:
            can_enter = False
            blockers.append("MISSING_SOURCE_HASH")
        if not r.page_number and not r.table_number:
            can_enter = False
            blockers.append("MISSING_SOURCE_LOCATION")
        if not matched_preds:
            can_enter = False
            blockers.append("NO_MATCHED_PREDICTION")
        if target.get("observable_class") in {"PARAMETER_BOUND", "LIMITATION_FLAG"}:
            can_enter = False
            blockers.append("NOT_OBSERVED_YTRUE")

        # Deduplicate blockers
        blockers = sorted(list(set(blockers)))

        candidate = ExternalYTrueCandidate(
            candidate_id=f"CAND-v4_5-{idx:03d}",
            acquisition_track="TRACK_A_TABLE_REVIEW",
            target_id=r.target_id,
            benchmark_id=target.get("benchmark_id", ""),
            source_id=r.source_id,
            source_hash=target.get("source_hash", "") or r.source_id,
            observable_class=target.get("observable_class", ""),
            normalized_variable_name=target.get("normalized_variable_name", ""),
            candidate_value_text=r.candidate_value_text or "",
            numeric_value=r.numeric_value,
            unit=r.unit,
            uncertainty=r.uncertainty,
            source_location_type="TABLE_OR_PAGE" if (r.page_number or r.table_number) else "UNKNOWN",
            source_location_value=f"page={r.page_number}; table={r.table_number}",
            local_artifact_path=r.local_pdf_path,
            local_artifact_hash=None,
            extraction_method="MANUAL_TABLE_EXTRACTION",
            provenance_status="LOCAL_PDF_ONLY" if r.local_pdf_path else "MISSING",
            qc_status=qc_status if not blockers else f"FAIL_{blockers[0]}",
            matched_prediction_ids=matched_preds,
            can_enter_dataset=can_enter,
            blockers=blockers,
        )
        candidates.append(candidate)

        if can_enter:
            accepted.append(
                AcceptedExternalYTrueRecord(
                    y_true_id=f"YTRUE-EXT-v4_5-{len(accepted)+1:03d}",
                    candidate_id=candidate.candidate_id,
                    acquisition_track=candidate.acquisition_track,
                    target_id=candidate.target_id,
                    benchmark_id=candidate.benchmark_id,
                    source_id=candidate.source_id,
                    source_hash=candidate.source_hash,
                    observable_class=candidate.observable_class,
                    normalized_variable_name=candidate.normalized_variable_name,
                    value=candidate.numeric_value,  # type: ignore
                    unit=candidate.unit or "dimensionless",
                    uncertainty=candidate.uncertainty,
                    source_location_type=candidate.source_location_type,
                    source_location_value=candidate.source_location_value,
                    local_artifact_path=candidate.local_artifact_path,
                    local_artifact_hash=candidate.local_artifact_hash,
                    extraction_method=candidate.extraction_method,
                    approximate=False,
                    qc_status=candidate.qc_status,
                    matched_prediction_ids=candidate.matched_prediction_ids,
                    limitations=[],
                )
            )
        else:
            rejection_reason = blockers[0] if blockers else "REJECTED_UNKNOWN"
            rejected.append(
                RejectedExternalYTrueRecord(
                    candidate_id=candidate.candidate_id,
                    target_id=candidate.target_id,
                    source_id=candidate.source_id,
                    acquisition_track=candidate.acquisition_track,
                    rejection_reason=rejection_reason,
                    required_next_action="Locate exact table/figure and page details." if rejection_reason in {"MISSING_SOURCE_LOCATION", "PAGE_LOCATION_MISSING"} else "Keep as context/constraint.",
                    claim_impact="No PredictiveGain and no physical claim may use this item.",
                )
            )

    return candidates, accepted, rejected
