"""Assemble raw extraction candidates into the final y_true dataset."""

from __future__ import annotations

from phyng.ytrue_extraction.schemas import (
    AssembledDatasetPayload,
    BlockedTarget,
    NextPredictiveGainInputs,
    YTrueRecord,
)


def assemble_y_true_dataset(
    targets: list[dict],
    candidates: list[dict],
    source_hashes: dict,
    model_predictions: dict,
) -> tuple[AssembledDatasetPayload, list[BlockedTarget], NextPredictiveGainInputs]:
    """Assemble final dataset, blocked targets list, and next gate inputs."""
    records: list[YTrueRecord] = []
    blocked_list: list[BlockedTarget] = []

    # Map source_id to hash record
    hash_map = {h["source_id"]: h for h in source_hashes.get("hashes", [])}

    # Map target_id to target dict
    target_map = {t["target_id"]: t for t in targets}

    # Map target_id to prediction records
    preds = model_predictions.get("predictions", [])
    pred_map: dict[str, list[dict]] = {}
    for p in preds:
        tid = p.get("target_id")
        if tid:
            if tid not in pred_map:
                pred_map[tid] = []
            pred_map[tid].append(p)

    index = 1
    matched_pred_ids = set()

    for c in candidates:
        tid = c["target_id"]
        t = target_map.get(tid, {})
        can_enter = c["can_enter_dataset"]

        if can_enter:
            bid = t.get("benchmark_id", "")
            sid = t.get("source_id", "")
            eid = t.get("extract_id", "")
            obs_class = t.get("observable_class", "")
            var_name = t.get("normalized_variable_name", "")
            val = c["numeric_value"]
            unit = c["unit"]

            h_rec = hash_map.get(sid, {})
            sha256 = h_rec.get("sha256", "UNKNOWN_HASH")

            t_preds = pred_map.get(tid, [])
            t_pred_ids = [p["prediction_id"] for p in t_preds if "prediction_id" in p]
            matched_pred_ids.update(t_pred_ids)

            records.append(
                YTrueRecord(
                    y_true_id=f"YTR-v4_3-{index:03d}",
                    target_id=tid,
                    benchmark_id=bid,
                    observable_class=obs_class,
                    normalized_variable_name=var_name,
                    value=val,
                    unit=unit,
                    uncertainty=c.get("uncertainty"),
                    source_id=sid,
                    extract_id=eid,
                    source_hash=sha256,
                    source_location_type="page_number",
                    source_location_value=str(t.get("page_number", "") or ""),
                    extraction_method=c["extraction_method"],
                    approximate=False,
                    qc_status="PASS",
                    limitations=[],
                    matched_prediction_ids=t_pred_ids,
                )
            )
            index += 1
        else:
            blocker_reason = c["blockers"][0] if c["blockers"] else "Missing numeric value."
            obs_class = t.get("observable_class", "")

            # Set required action and unblockability
            if obs_class in ("PARAMETER_BOUND", "LIMITATION_FLAG", "EXPERIMENTAL_CONTEXT"):
                action = "No action; target remains blocked as model constraint or limit."
                can_unblock = False
            elif obs_class in ("VISIBILITY", "DECOHERENCE_RATE", "COHERENCE_LOSS"):
                action = "Review source tables or digitize figures from local PDF."
                can_unblock = True
            else:
                action = "Search public repositories or request author dataset."
                can_unblock = True

            # Determine priority
            priority = "MEDIUM"
            if obs_class in ("VISIBILITY", "CONTRAST_DECAY"):
                priority = "CRITICAL"
            elif obs_class in ("DECOHERENCE_RATE", "COHERENCE_LOSS"):
                priority = "HIGH"

            blocked_list.append(
                BlockedTarget(
                    target_id=tid,
                    benchmark_id=t.get("benchmark_id", ""),
                    source_id=t.get("source_id", ""),
                    observable_class=obs_class,
                    blocked_reason=blocker_reason,
                    required_action=action,
                    priority=priority,
                    can_be_unblocked=can_unblock,
                )
            )

    # 3. Rules for ready_for_predictive_gain
    accepted_count = len(records)
    matched_pred_count = len(matched_pred_ids)

    # Threshold: >= 3 accepted y_true records and >= 3 matched predictions
    ready = accepted_count >= 3 and matched_pred_count >= 3

    assembled = AssembledDatasetPayload(
        dataset_id="YTRUE-DATASET-v4_3",
        created_at="2026-07-01",
        source_plan_ref="data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json",
        target_count=len(targets),
        y_true_record_count=accepted_count,
        records=records,
        ready_for_predictive_gain=ready,
        predictive_gain_status=None,  # Remains undefined / null in JSON
        slot4_debt_status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        physical_claim_permission="BLOCKED",
        notes=[
            f"Assembled {accepted_count} high-quality y_true records.",
            "SLOT_4 debt remains open blocking.",
            "Predictive gain remains undefined unless accepted count >= 3.",
        ],
    )

    next_inputs = NextPredictiveGainInputs(
        ready_for_predictive_gain=ready,
        y_true_dataset_path="data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json",
        prediction_dataset_path="data/model_comparison/phi_gradient_model_predictions_v4_1.json",
        matched_prediction_count=matched_pred_count,
        minimum_viable_y_true_count=3,
        predictive_gain_status=None,
        recommended_next_phase="v4.4 — PredictiveGain Smoke Test & Error Comparison"
        if ready
        else "v4.4 — Manual Data Extraction Sprint",
        blocked_claims=[
            "PHI_GRADIENT is validated.",
            "PHI_GRADIENT has predictive gain.",
            "Gradient mechanism is supported.",
            "Frontera C is validated.",
        ],
        notes=[
            f"Assemble status: ready_for_predictive_gain={ready}.",
            "Physics validation claims remain BLOCKED.",
        ],
    )

    return assembled, blocked_list, next_inputs
