"""Tests for v4.6 candidate freeze review campaign orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from phyng.candidate_decision.campaign import run_candidate_decision_campaign
from tests.test_candidate_decision_loader_v4_6 import write_mock_v4_6_inputs


def test_campaign_executes_successfully_and_saves_files(tmp_path: Path) -> None:
    write_mock_v4_6_inputs(tmp_path)
    
    result = run_candidate_decision_campaign(tmp_path)
    from phyng.candidate_decision.schemas import CampaignResultv46
    assert isinstance(result, CampaignResultv46)
    
    assert result.status == "PHI_GRADIENT_FREEZE_REVIEW_COMPLETED"
    assert result.permissions.predictive_gain_permission == "BLOCKED_NO_YTRUE"
    assert result.permissions.physical_claim_permission == "BLOCKED"
    assert result.pivot.next_candidate_family == "PHI_CURVATURE"


    # Verify JSON files are written
    assert (tmp_path / "data/candidate_decisions/phi_gradient_freeze_review_v4_6.json").exists()
    assert (tmp_path / "data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json").exists()
    assert (tmp_path / "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json").exists()
    assert (tmp_path / "data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json").exists()
    assert (tmp_path / "data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json").exists()
    assert (tmp_path / "data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json").exists()

    # Verify report files are generated
    assert (tmp_path / "reports/candidate_decisions/phi_gradient_freeze_review_v4_6.md").exists()
    assert (tmp_path / "reports/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.md").exists()
    assert (tmp_path / "reports/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.md").exists()
    assert (tmp_path / "reports/candidate_decisions/phi_gradient_experiment_requirement_v4_6.md").exists()
    assert (tmp_path / "reports/candidate_decisions/next_candidate_family_selection_matrix_v4_6.md").exists()
    assert (tmp_path / "reports/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.md").exists()
    assert (tmp_path / "reports/campaigns/PHI-GRADIENT-CANDIDATE-FREEZE-REVIEW-v4_6.md").exists()


def test_missing_freeze_decision_blocks_campaign(tmp_path: Path) -> None:
    # No files written, so freeze decision is missing
    result = run_candidate_decision_campaign(tmp_path)
    assert isinstance(result, dict)
    assert result["status"] == "PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION"
