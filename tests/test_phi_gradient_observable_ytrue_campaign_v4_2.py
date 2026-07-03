"""End-to-end campaign tests for v4.2."""

from __future__ import annotations

from pathlib import Path

from phyng.campaigns.phi_gradient_debt_bounded_model_comparison import (
    run_phi_gradient_debt_bounded_model_comparison_campaign,
)
from phyng.campaigns.phi_gradient_observable_ytrue_plan import (
    run_phi_gradient_observable_ytrue_plan_campaign,
)

from tests.test_model_comparison_loader_v4_1 import write_minimal_v4_1_inputs
from tests.test_observable_dataset_loader_v4_2 import write_minimal_v4_2_inputs



def test_missing_model_comparison_blocks_ytrue_plan(tmp_path: Path) -> None:
    res = run_phi_gradient_observable_ytrue_plan_campaign(tmp_path)
    assert res["status"] == "PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON"


def test_campaign_executes_successfully_and_blocks_claims(tmp_path: Path) -> None:
    write_minimal_v4_2_inputs(tmp_path)

    res = run_phi_gradient_observable_ytrue_plan_campaign(tmp_path)

    assert res["status"] == "PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY"
    assert res["next_gate_inputs_path"] is not None

    # Check that data files exist
    assert (tmp_path / "data/observables/phi_gradient_observable_schema_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_normalized_observable_targets_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_dataset_source_registry_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_quality_control_rules_v4_2.json").exists()
    assert (tmp_path / "data/observables/phi_gradient_v4_2_next_gate_inputs.json").exists()

    # Check report files exist and contain canonical status
    for key, path_str in res["report_paths"].items():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        assert report_path.exists(), f"Missing report: {path_str}"
        content = report_path.read_text(encoding="utf-8")
        assert "## Canonical Status" in content

    # Assert claim blocks are preserved
    gate_result = res["observable_dataset"]["gate_result"]
    assert "PHI_GRADIENT is predictively validated." in gate_result["blocked_claims"]
    assert gate_result["normalized_targets"][0]["slot4_debt_status"] == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"


def test_existing_v4_1_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v4_1_inputs(tmp_path)
    res_v4_1 = run_phi_gradient_debt_bounded_model_comparison_campaign(tmp_path)

    # v4.1 campaign runs unchanged
    assert res_v4_1["status"] == "PHI_GRADIENT_MODEL_COMPARISON_COMPLETED"
    assert res_v4_1["model_comparison"]["gate_result"]["claim_permission_update"]["physical_claim_permission"] == "BLOCKED"
