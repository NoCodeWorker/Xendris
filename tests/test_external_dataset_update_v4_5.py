"""Tests for dataset update and threshold logic."""

from __future__ import annotations

from phyng.external_evidence.schemas import AcceptedExternalYTrueRecord
from phyng.external_evidence.dataset_update import update_assembled_dataset


def test_threshold_reached_allows_next_predictive_gate() -> None:
    inputs = {
        "assembled_dataset_v4_4": {
            "records": []
        }
    }

    # Case A: Less than 3 accepted records
    accepted_1 = [
        AcceptedExternalYTrueRecord(
            y_true_id="Y-1",
            candidate_id="C-1",
            acquisition_track="TRACK_A",
            target_id="TGT-1",
            benchmark_id="BM-1",
            source_id="SRC-1",
            source_hash="H-1",
            observable_class="VISIBILITY",
            normalized_variable_name="visibility",
            value=0.5,
            unit="dimensionless",
            uncertainty=None,
            source_location_type="PAGE",
            source_location_value="page 3",
            local_artifact_path=None,
            local_artifact_hash=None,
            extraction_method="MANUAL",
            approximate=False,
            qc_status="PASS",
            matched_prediction_ids=["P-1"],
            limitations=[],
        )
    ]

    assembled, next_inputs = update_assembled_dataset(inputs, accepted_1)
    assert assembled.ready_for_predictive_gain is False
    assert next_inputs.ready_for_predictive_gain is False
    assert assembled.predictive_gain_status == "UNDEFINED_INSUFFICIENT_YTRUE"

    # Case B: 3 accepted records with matched predictions
    accepted_3 = [
        AcceptedExternalYTrueRecord(
            y_true_id=f"Y-{i}",
            candidate_id=f"C-{i}",
            acquisition_track="TRACK_A",
            target_id=f"TGT-{i}",
            benchmark_id=f"BM-{i}",
            source_id=f"SRC-{i}",
            source_hash=f"H-{i}",
            observable_class="VISIBILITY",
            normalized_variable_name="visibility",
            value=0.5,
            unit="dimensionless",
            uncertainty=None,
            source_location_type="PAGE",
            source_location_value="page 3",
            local_artifact_path=None,
            local_artifact_hash=None,
            extraction_method="MANUAL",
            approximate=False,
            qc_status="PASS",
            matched_prediction_ids=[f"P-{i}"],
            limitations=[],
        )
        for i in range(1, 4)
    ]

    assembled, next_inputs = update_assembled_dataset(inputs, accepted_3)
    assert assembled.ready_for_predictive_gain is True
    assert next_inputs.ready_for_predictive_gain is True
    assert assembled.predictive_gain_status == "READY_FOR_SMOKE_TEST"
    assert next_inputs.recommended_next_phase == "v4.6 — PredictiveGain Smoke Test & Error Comparison"
