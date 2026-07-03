"""E2E and campaign integration tests for v4.5."""

from __future__ import annotations

import json
from pathlib import Path
from phyng.external_evidence.campaign import run_phi_gradient_external_evidence_sprint_campaign
from tests.test_external_evidence_loader_v4_5 import write_mock_v4_5_inputs


def test_only_three_acquisition_tracks_allowed(tmp_path: Path) -> None:
    # Set up mock inputs
    write_mock_v4_5_inputs(tmp_path)
    res = run_phi_gradient_external_evidence_sprint_campaign(tmp_path)
    assert res["status"] in {
        "PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE",
        "PHI_GRADIENT_EXTERNAL_EVIDENCE_NO_YTRUE_FOUND",
        "PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL",
    }

    # Verify that only three track result files were written
    assert (tmp_path / "data/external_evidence/phi_gradient_table_review_results_v4_5.json").exists()
    assert (tmp_path / "data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json").exists()
    assert (tmp_path / "data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json").exists()

    # Verify that no fourth governance track results file exists
    assert not (tmp_path / "data/external_evidence/phi_gradient_governance_search_results_v4_5.json").exists()


def test_no_predictive_gain_created(tmp_path: Path) -> None:
    write_mock_v4_5_inputs(tmp_path)
    res = run_phi_gradient_external_evidence_sprint_campaign(tmp_path)
    assert res["ready_for_predictive_gain"] is False

    # Check assembled dataset json directly
    with open(tmp_path / "data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json", "r") as f:
        ds = json.load(f)
    assert ds["ready_for_predictive_gain"] is False
    assert ds["predictive_gain_status"] == "UNDEFINED_INSUFFICIENT_YTRUE"


def test_slot4_debt_remains_open(tmp_path: Path) -> None:
    write_mock_v4_5_inputs(tmp_path)
    run_phi_gradient_external_evidence_sprint_campaign(tmp_path)

    with open(tmp_path / "data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json", "r") as f:
        ds = json.load(f)
    assert ds["slot4_debt_status"] == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_mock_v4_5_inputs(tmp_path)
    res = run_phi_gradient_external_evidence_sprint_campaign(tmp_path)

    # Verify report files block physical claims
    campaign_report_path = tmp_path / res["report_paths"]["campaign"]
    report_content = campaign_report_path.read_text(encoding="utf-8")
    assert "### Blocked Claims:" in report_content
    assert "PHI_GRADIENT is validated." in report_content
