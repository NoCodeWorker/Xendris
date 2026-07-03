"""End-to-end campaign tests for v4.1."""

from __future__ import annotations

from pathlib import Path

from phyng.benchmark_construction.campaign import run_phi_gradient_benchmark_construction_campaign
from phyng.campaigns.phi_gradient_debt_aware_benchmark import run_phi_gradient_debt_aware_benchmark_campaign
from phyng.campaigns.phi_gradient_debt_bounded_model_comparison import (
    run_phi_gradient_debt_bounded_model_comparison_campaign,
)

from tests.test_debt_aware_benchmark_loader_v4_0 import write_minimal_v4_0_inputs
from tests.test_model_comparison_loader_v4_1 import write_minimal_v4_1_inputs


def test_missing_benchmark_blocks_model_comparison(tmp_path: Path) -> None:
    res = run_phi_gradient_debt_bounded_model_comparison_campaign(tmp_path)
    assert res["status"] == "PHI_GRADIENT_MODEL_COMPARISON_BLOCKED_MISSING_BENCHMARK"


def test_campaign_executes_successfully_and_blocks_claims(tmp_path: Path) -> None:
    write_minimal_v4_1_inputs(tmp_path)
    res = run_phi_gradient_debt_bounded_model_comparison_campaign(tmp_path)

    assert res["status"] == "PHI_GRADIENT_MODEL_COMPARISON_COMPLETED"
    assert res["next_gate_inputs_path"] is not None

    # Check that data files exist
    assert (tmp_path / "data/model_comparison/phi_gradient_model_registry_v4_1.json").exists()
    assert (tmp_path / "data/model_comparison/phi_gradient_model_predictions_v4_1.json").exists()
    assert (tmp_path / "data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json").exists()
    assert (tmp_path / "data/model_comparison/phi_gradient_negative_control_results_v4_1.json").exists()
    assert (tmp_path / "data/model_comparison/phi_gradient_claim_permission_update_v4_1.json").exists()
    assert (tmp_path / "data/model_comparison/phi_gradient_v4_1_next_gate_inputs.json").exists()

    # Check report files exist and contain canonical status
    for key, path_str in res["report_paths"].items():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        assert report_path.exists(), f"Missing report: {path_str}"
        content = report_path.read_text(encoding="utf-8")
        assert "## Canonical Status" in content

    # Assert claim blocks are preserved
    gate_result = res["model_comparison"]["gate_result"]
    assert "PHI_GRADIENT is validated." in gate_result["blocked_claims"]
    assert gate_result["claim_permission_update"]["physical_claim_permission"] == "BLOCKED"
    assert gate_result["claim_permission_update"]["gradient_mechanism_claim_permission"] == "BLOCKED_BY_SLOT4_DEBT"


def test_existing_v4_0_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v4_0_inputs(tmp_path)
    res_v4_0 = run_phi_gradient_debt_aware_benchmark_campaign(tmp_path)

    # v4.0 campaign runs unchanged
    assert res_v4_0["status"] == "PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY"
    assert res_v4_0["debt_object"]["status"] == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
