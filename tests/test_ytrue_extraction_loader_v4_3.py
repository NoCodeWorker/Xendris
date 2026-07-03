"""Tests for v4.3 y_true extraction loader."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.ytrue_extraction.loader import load_extraction_inputs


def test_missing_ytrue_plan_blocks_extraction(tmp_path: Path) -> None:
    inputs = load_extraction_inputs(tmp_path)
    assert inputs.blocked_reason == "PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN"


def test_loader_loads_all_inputs(tmp_path: Path) -> None:
    write_minimal_v4_3_inputs(tmp_path)
    inputs = load_extraction_inputs(tmp_path)
    assert inputs.blocked_reason is None
    assert "hashes" in inputs.source_hashes


def write_minimal_v4_3_inputs(tmp_path: Path) -> None:
    obs_dir = tmp_path / "data" / "observables"
    bm_dir = tmp_path / "data" / "benchmarks"
    debt_dir = tmp_path / "data" / "debts"
    mc_dir = tmp_path / "data" / "model_comparison"
    rs_dir = tmp_path / "data" / "real_sources"
    pdf_dir = tmp_path / "data" / "real_sources" / "pdfs"

    obs_dir.mkdir(parents=True, exist_ok=True)
    bm_dir.mkdir(parents=True, exist_ok=True)
    debt_dir.mkdir(parents=True, exist_ok=True)
    mc_dir.mkdir(parents=True, exist_ok=True)
    rs_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Write source hashes and dummy PDF
    hashes = {
        "hashes": [
            {
                "file_type": ".pdf",
                "local_path": "data/real_sources/pdfs/Hornberger_2003_Collisional_Decoherence.pdf",
                "sha256": "06d3ae4ad0af56fc114d65e532eb453be9dc59eb19c127d6643471e4466c6de5",
                "size_bytes": 100,
                "source_id": "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
            }
        ],
        "manifest_id": "PHI-GRADIENT-SOURCE-HASHES-v3_6",
    }
    (rs_dir / "source_hashes_v3_6.json").write_text(json.dumps(hashes), encoding="utf-8")
    (pdf_dir / "Hornberger_2003_Collisional_Decoherence.pdf").write_text("DUMMY_PDF_CONTENT", encoding="utf-8")

    # Mock rows
    rows = [
        {
            "benchmark_id": "BM-v4_0-001",
            "source_id": "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
            "extract_id": "VRX-001",
            "sha256": "06d3ae4ad0af56fc114d65e532eb453be9dc59eb19c127d6643471e4466c6de5",
            "page_number": 1,
            "observable_type": "BASELINE",
            "observable_text": "thermal decay rate gamma = 12.5 s^-1 is measured",
            "regime_text": "regime slot 1",
            "allowed_model_comparison": True,
            "gradient_claim_allowed": False,
        }
    ]
    (bm_dir / "phi_gradient_benchmark_rows_v4_0.json").write_text(
        json.dumps({"benchmark_rows": rows}), encoding="utf-8"
    )

    # v4.2 Outputs
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-v4_0-001",
            "source_id": "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
            "extract_id": "VRX-001",
            "observable_class": "DECOHERENCE_RATE",
            "observable_name": "decoherence rate",
            "source_observable_text": "thermal decay rate gamma = 12.5 s^-1 is measured",
            "normalized_variable_name": "decoherence_rate",
            "unit": "s^-1",
            "expected_dtype": "float",
            "measurement_context": "Baseline decoherence decay rate gamma",
            "regime_fields": {},
            "candidate_model_fields": ["decay_rate"],
            "baseline_model_fields": ["baseline_decay_rate"],
            "y_true_required": True,
            "y_true_status": "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION",
            "slot4_debt_status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
            "predictive_gain_allowed": False,
            "page_number": 1,
        }
    ]
    (obs_dir / "phi_gradient_observable_schema_v4_2.json").write_text(json.dumps({"schemas": []}), encoding="utf-8")
    (obs_dir / "phi_gradient_normalized_observable_targets_v4_2.json").write_text(
        json.dumps({"normalized_targets": targets}), encoding="utf-8"
    )
    (obs_dir / "phi_gradient_y_true_acquisition_plan_v4_2.json").write_text(json.dumps({"plan": []}), encoding="utf-8")
    (obs_dir / "phi_gradient_dataset_source_registry_v4_2.json").write_text(json.dumps({"registry": []}), encoding="utf-8")
    (obs_dir / "phi_gradient_measurement_readiness_matrix_v4_2.json").write_text(json.dumps({"readiness": []}), encoding="utf-8")
    (obs_dir / "phi_gradient_quality_control_rules_v4_2.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
    (obs_dir / "phi_gradient_v4_2_next_gate_inputs.json").write_text(json.dumps({"status": "PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY"}), encoding="utf-8")

    # Debt and Predictions
    (debt_dir / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json").write_text(json.dumps({"status": "OPEN"}), encoding="utf-8")
    (mc_dir / "phi_gradient_model_predictions_v4_1.json").write_text(
        json.dumps({
            "predictions": [
                {
                    "prediction_id": "PRED-001",
                    "target_id": "TGT-v4_2-001",
                    "model_id": "M_candidate_debt_bounded",
                    "predicted_value": 11.8,
                }
            ]
        }),
        encoding="utf-8"
    )
