from __future__ import annotations

import json
from pathlib import Path

from phyng.manual_data_extraction.loader import load_manual_extraction_inputs


def test_missing_manual_queue_blocks_extraction(tmp_path: Path) -> None:
    inputs = load_manual_extraction_inputs(tmp_path)

    assert inputs.blocked_reason == "PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE"


def write_minimal_v4_4_inputs(tmp_path: Path, queue: list[dict] | None = None) -> None:
    root = tmp_path / "data"
    y = root / "y_true"
    obs = root / "observables"
    model = root / "model_comparison"
    real = root / "real_sources"
    debts = root / "debts"
    for path in (y, obs, model, real, debts):
        path.mkdir(parents=True, exist_ok=True)
    queue_items = queue if queue is not None else [queue_item()]
    (y / "phi_gradient_manual_table_extraction_queue_v4_3.json").write_text(
        json.dumps({"manual_table_extraction_queue": queue_items, "queue_item_count": len(queue_items)}),
        encoding="utf-8",
    )
    (y / "phi_gradient_source_coverage_audit_v4_3.json").write_text(json.dumps({"source_coverage_audit": []}), encoding="utf-8")
    (y / "phi_gradient_y_true_extraction_candidates_v4_3.json").write_text(json.dumps({"candidates": []}), encoding="utf-8")
    (y / "phi_gradient_assembled_y_true_dataset_v4_3.json").write_text(json.dumps({"records": [], "y_true_record_count": 0}), encoding="utf-8")
    (y / "phi_gradient_blocked_y_true_targets_v4_3.json").write_text(json.dumps({"blocked_targets": []}), encoding="utf-8")
    (y / "phi_gradient_dataset_quality_report_v4_3.json").write_text(json.dumps({"accepted_y_true_count": 0}), encoding="utf-8")
    (y / "phi_gradient_v4_3_next_predictive_gain_inputs.json").write_text(json.dumps({"ready_for_predictive_gain": False}), encoding="utf-8")
    (obs / "phi_gradient_normalized_observable_targets_v4_2.json").write_text(json.dumps({"target_count": 1, "normalized_targets": [target()]}), encoding="utf-8")
    (obs / "phi_gradient_quality_control_rules_v4_2.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
    (model / "phi_gradient_model_predictions_v4_1.json").write_text(json.dumps({"predictions": predictions()}), encoding="utf-8")
    (real / "source_hashes_v3_6.json").write_text(json.dumps({"hashes": [{"source_id": "SRC-TEST", "sha256": "abc123", "local_path": "data/real_sources/pdfs/test.pdf"}]}), encoding="utf-8")
    (debts / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json").write_text(json.dumps({"status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}), encoding="utf-8")


def queue_item(**overrides: object) -> dict:
    payload = {
        "target_id": "TGT-1",
        "source_id": "SRC-TEST",
        "observable_class": "VISIBILITY",
        "expected_measurement": "fringe visibility",
        "source_location_hint": "page 3 table 1",
        "required_action": "Perform manual PDF review.",
        "priority": "CRITICAL",
        "blocking_reason": "manual table extraction required",
    }
    payload.update(overrides)
    return payload


def target(**overrides: object) -> dict:
    payload = {
        "target_id": "TGT-1",
        "benchmark_id": "BM-1",
        "observable_class": "VISIBILITY",
        "normalized_variable_name": "visibility",
        "source_observable_text": "Visibility = 0.42",
        "unit": "dimensionless",
    }
    payload.update(overrides)
    return payload


def predictions() -> list[dict]:
    return [
        {"prediction_id": "PRED-1", "benchmark_id": "BM-1", "comparison_allowed": True},
        {"prediction_id": "PRED-2", "benchmark_id": "BM-1", "comparison_allowed": True},
        {"prediction_id": "PRED-3", "benchmark_id": "BM-1", "comparison_allowed": True},
    ]
