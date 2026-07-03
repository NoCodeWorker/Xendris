"""Tests for v4.1 model comparison loader."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.model_comparison.loader import load_model_comparison_inputs


def test_missing_benchmark_blocks_model_comparison(tmp_path: Path) -> None:
    inputs = load_model_comparison_inputs(tmp_path)
    assert inputs.blocked_reason == "PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK"


def test_loader_loads_all_inputs(tmp_path: Path) -> None:
    write_minimal_v4_1_inputs(tmp_path)
    inputs = load_model_comparison_inputs(tmp_path)
    assert inputs.blocked_reason is None
    assert "benchmark_rows" in inputs.benchmark_rows


def write_minimal_v4_1_inputs(tmp_path: Path) -> None:
    bm_dir = tmp_path / "data" / "benchmarks"
    debt_dir = tmp_path / "data" / "debts"

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
        }
    ]

    # Write files
    (bm_dir / "phi_gradient_benchmark_dataset_manifest_v4_0.json").write_text(
        json.dumps({"dataset_id": "MOCK-MANIFEST", "benchmark_row_count": len(rows)}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_observable_alignment_v4_0.json").write_text(
        json.dumps({"observable_alignments": []}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_benchmark_rows_v4_0.json").write_text(
        json.dumps({"benchmark_rows": rows, "row_count": len(rows)}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_negative_control_plan_v4_0.json").write_text(
        json.dumps({"controls": [{"control_id": "CTRL-1", "control_type": "NO_SLOT4_CONTROL"}]}), encoding="utf-8"
    )
    (debt_dir / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json").write_text(
        json.dumps({"debt_id": "DEBT-SLOT4-GRADIENT-COMPONENT-GAP", "status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}), encoding="utf-8"
    )
    (debt_dir / "slot4_resolution_plan_v4_0.json").write_text(
        json.dumps({"plan_id": "RESOLUTION-PLAN"}), encoding="utf-8"
    )
    (bm_dir / "phi_gradient_v4_0_next_gate_inputs.json").write_text(
        json.dumps({"ready_for_next_phase": True}), encoding="utf-8"
    )
