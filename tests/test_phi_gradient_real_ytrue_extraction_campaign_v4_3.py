"""End-to-end campaign tests for v4.3."""

from __future__ import annotations

from pathlib import Path

from phyng.campaigns.phi_gradient_observable_ytrue_plan import (
    run_phi_gradient_observable_ytrue_plan_campaign,
)
from phyng.campaigns.phi_gradient_real_ytrue_extraction import (
    run_phi_gradient_real_ytrue_extraction_campaign,
)

from tests.test_observable_dataset_loader_v4_2 import write_minimal_v4_2_inputs
from tests.test_ytrue_extraction_loader_v4_3 import write_minimal_v4_3_inputs


def test_missing_ytrue_plan_blocks_extraction(tmp_path: Path) -> None:
    res = run_phi_gradient_real_ytrue_extraction_campaign(tmp_path)
    assert res["status"] == "PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN"


def test_campaign_executes_successfully_and_blocks_claims(tmp_path: Path) -> None:
    write_minimal_v4_3_inputs(tmp_path)
    res = run_phi_gradient_real_ytrue_extraction_campaign(tmp_path)

    # Since it contains 1 valid numeric extract target in baseline (which is DECOHERENCE_RATE),
    # it extracts it successfully! So accepted_y_true_records is 1.
    # Therefore, status is PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL.
    assert res["status"] == "PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL"

    # Check that data files exist
    assert (tmp_path / "data/y_true/phi_gradient_source_coverage_audit_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_figure_digitization_queue_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_dataset_quality_report_v4_3.json").exists()
    assert (tmp_path / "data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json").exists()

    # Check report files exist and contain canonical status
    for key, path_str in res["report_paths"].items():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        assert report_path.exists(), f"Missing report: {path_str}"
        content = report_path.read_text(encoding="utf-8")
        assert "## Canonical Status" in content

    # Assert claim blocks are preserved
    gate_result = res["ytrue_extraction"]["gate_result"]
    assert "PHI_GRADIENT is predictively validated." in gate_result["blocked_claims"]
    assert gate_result["assembled_y_true_dataset"]["slot4_debt_status"] == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
    assert gate_result["assembled_y_true_dataset"]["physical_claim_permission"] == "BLOCKED"


def test_existing_v4_2_behavior_preserved(tmp_path: Path) -> None:
    write_minimal_v4_2_inputs(tmp_path)
    res_v4_2 = run_phi_gradient_observable_ytrue_plan_campaign(tmp_path)

    # v4.2 campaign runs unchanged
    assert res_v4_2["status"] == "PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY"
