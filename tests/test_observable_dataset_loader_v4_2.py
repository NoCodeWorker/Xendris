"""Tests for v4.2 observable dataset loader."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.observable_dataset.loader import load_observable_ytrue_inputs


def test_missing_model_comparison_blocks_ytrue_plan(tmp_path: Path) -> None:
    inputs = load_observable_ytrue_inputs(tmp_path)
    assert inputs.blocked_reason == "PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON"


def test_loader_loads_all_inputs(tmp_path: Path) -> None:
    write_minimal_v4_2_inputs(tmp_path)
    inputs = load_observable_ytrue_inputs(tmp_path)
    assert inputs.blocked_reason is None
    assert "benchmark_rows" in inputs.benchmark_rows


def write_minimal_v4_2_inputs(tmp_path: Path) -> None:
    mc_dir = tmp_path / "data" / "model_comparison"
    bm_dir = tmp_path / "data" / "benchmarks"
    debt_dir = tmp_path / "data" / "debts"

    mc_dir.mkdir(parents=True, exist_ok=True)
    bm_dir.mkdir(parents=True, exist_ok=True)
    debt_dir.mkdir(parents=True, exist_ok=True)

    # Mock rows
    rows = [
        {
            "benchmark_id": "BM-v4_0-001",
            "source_id": "SRC-TEST",
            "extract_id": "VRX-001",
            "sha256": "abc123",
            "page_number": 1,
            "observable_type": "BASELINE",
            "observable_text": "thermal emission causes decoherence",
            "regime_text": "regime slot 1",
            "allowed_model_comparison": True,
            "gradient_claim_allowed": False,
        },
        {
            "benchmark_id": "BM-v4_0-002",
            "source_id": "SRC-TEST",
            "extract_id": "VRX-002",
            "sha256": "def456",
            "page_number": 2,
            "observable_type": "OBSERVABLE",
            "observable_text": "measured visibility value is 0.45",
            "regime_text": "regime slot 2",
            "allowed_model_comparison": True,
            "gradient_claim_allowed": False,
        },
    ]

    # Write files
    (mc_dir / "phi_gradient_model_registry_v4_1.json").write_text(
        json.dumps({"models": []}), encoding="utf-8"
    )
    (mc_dir / "phi_gradient_model_predictions_v4_1.json").write_text(
        json.dumps({"predictions": []}), encoding="utf-8"
    )
    (mc_dir / "phi_gradient_benchmark_comparison_scores_v4_1.json").write_text(
        json.dumps({"scores": []}), encoding="utf-8"
    )
    (mc_dir / "phi_gradient_negative_control_results_v4_1.json").write_text(
        json.dumps({"negative_control_results": []}), encoding="utf-8"
    )
    (mc_dir / "phi_gradient_claim_permission_update_v4_1.json").write_text(
        json.dumps({"physical_claim_permission": "BLOCKED"}), encoding="utf-8"
    )
    (mc_dir / "phi_gradient_v4_1_next_gate_inputs.json").write_text(
        json.dumps({"status": "PHI_GRADIENT_MODEL_COMPARISON_COMPLETED"}), encoding="utf-8"
    )

    (bm_dir / "phi_gradient_benchmark_rows_v4_0.json").write_text(
        json.dumps({"benchmark_rows": rows, "row_count": len(rows)}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_observable_alignment_v4_0.json").write_text(
        json.dumps({"observable_alignments": []}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_negative_control_plan_v4_0.json").write_text(
        json.dumps({"controls": []}), encoding="utf-8"
    )
    (debt_dir / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json").write_text(
        json.dumps({"debt_id": "DEBT-SLOT4-GRADIENT-COMPONENT-GAP", "status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}), encoding="utf-8"
    )
