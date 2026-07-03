"""End-to-end campaign tests for v4.0."""

from __future__ import annotations

from pathlib import Path

from phyng.campaigns.phi_gradient_debt_aware_benchmark import run_phi_gradient_debt_aware_benchmark_campaign
from phyng.source_pressure_decision.campaign import run_phi_gradient_source_pressure_decision_campaign

from tests.test_debt_aware_benchmark_loader_v4_0 import write_minimal_v4_0_inputs
from tests.test_source_pressure_loader_v3_9 import write_minimal_v3_9_inputs


def test_missing_source_pressure_blocks_benchmark(tmp_path: Path) -> None:
    res = run_phi_gradient_debt_aware_benchmark_campaign(tmp_path)
    assert res["status"] == "PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE"


def test_campaign_executes_successfully_and_blocks_claims(tmp_path: Path) -> None:
    write_minimal_v4_0_inputs(tmp_path)
    res = run_phi_gradient_debt_aware_benchmark_campaign(tmp_path)

    assert res["status"] == "PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY"
    assert res["debt_object"]["status"] == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"

    # Verify output JSONs exist
    assert (tmp_path / "data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json").exists()
    assert (tmp_path / "data/benchmarks/phi_gradient_observable_alignment_v4_0.json").exists()
    assert (tmp_path / "data/benchmarks/phi_gradient_benchmark_rows_v4_0.json").exists()
    assert (tmp_path / "data/benchmarks/phi_gradient_negative_control_plan_v4_0.json").exists()
    assert (tmp_path / "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json").exists()
    assert (tmp_path / "data/debts/slot4_resolution_plan_v4_0.json").exists()
    assert (tmp_path / "data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json").exists()

    # Physical claims remain blocked
    blocked = res["benchmark_construction"]["gate_result"]["blocked_claims"]
    assert "PHI_GRADIENT is validated." in blocked
    assert "Frontera C is validated." in blocked


def test_existing_v3_9_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)
    res_v3_9 = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    # v3.9 decision should still run perfectly
    assert res_v3_9.status != "PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK"
    assert res_v3_9.gate_result.decision.primary_decision == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
