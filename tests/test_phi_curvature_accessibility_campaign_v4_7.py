"""Tests for v4.7 candidate screening campaign orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from phyng.candidate_screening.campaign import run_phi_curvature_accessibility_screen_campaign
from phyng.candidate_screening.schemas import CampaignResultv47
from tests.test_phi_curvature_screen_loader_v4_7 import write_mock_v4_7_inputs


def test_campaign_executes_successfully_and_saves_files(tmp_path: Path) -> None:
    write_mock_v4_7_inputs(tmp_path)
    
    result = run_phi_curvature_accessibility_screen_campaign(tmp_path)
    assert isinstance(result, CampaignResultv47)
    assert result.status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED"
    
    # Standard mock config has 6 met criteria -> Passed (or Partial depending on default parameters, here it evaluates to PASSED because matrix record had PLAUSIBLE, HIGH, etc)
    assert result.decision.final_status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED"

    # Verify JSON files are written
    screening_dir = tmp_path / "data/candidate_screening"
    assert (screening_dir / "phi_curvature_screening_inputs_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_source_accessibility_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_observable_accessibility_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_ytrue_accessibility_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_public_dataset_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_experimental_feasibility_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_claim_risk_screen_v4_7.json").exists()
    assert (screening_dir / "phi_curvature_screening_decision_v4_7.json").exists()

    # Verify report files are generated
    assert (tmp_path / "reports/candidate_screening/phi_curvature_screening_inputs_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_public_dataset_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_claim_risk_screen_v4_7.md").exists()
    assert (tmp_path / "reports/candidate_screening/phi_curvature_screening_decision_v4_7.md").exists()
    assert (tmp_path / "reports/campaigns/PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7.md").exists()


def test_missing_pivot_decision_blocks_campaign(tmp_path: Path) -> None:
    # No files written, so pivot decision is missing
    result = run_phi_curvature_accessibility_screen_campaign(tmp_path)
    assert isinstance(result, dict)
    assert result["status"] == "PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION"


def test_no_ytrue_or_predictive_gain_created(tmp_path: Path) -> None:
    write_mock_v4_7_inputs(tmp_path)
    run_phi_curvature_accessibility_screen_campaign(tmp_path)
    # Check that no new y_true file or predictive gain inputs were created
    assert not (tmp_path / "data/y_true/phi_curvature_assembled_y_true_dataset_v4_7.json").exists()
    assert not (tmp_path / "data/y_true/phi_curvature_v4_7_next_predictive_gain_inputs.json").exists()


def test_phi_gradient_remains_method_only(tmp_path: Path) -> None:
    write_mock_v4_7_inputs(tmp_path)
    run_phi_curvature_accessibility_screen_campaign(tmp_path)
    # Check redefinition from loaded inputs
    with open(tmp_path / "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["redefinition_status"] == "PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY"
