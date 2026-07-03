"""Tests for v4.7 candidate screening loader."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from phyng.candidate_screening.loader import load_screening_inputs, MissingPivotDecisionError


def test_missing_pivot_decision_blocks_screen(tmp_path: Path) -> None:
    # No files written, so pivot decision is missing
    with pytest.raises(MissingPivotDecisionError):
        load_screening_inputs(tmp_path)


def write_mock_v4_7_inputs(tmp_path: Path) -> None:
    # Create necessary subdirectories
    (tmp_path / "data/candidate_decisions").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/debts").mkdir(parents=True, exist_ok=True)

    # Write files
    with open(tmp_path / "data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json", "w", encoding="utf-8") as f:
        json.dump([
            {
                "family_id": "PHI_CURVATURE",
                "previous_status": "PHI_CANDIDATE_SURVIVES_CONTROLS",
                "source_support_availability": "HIGH",
                "y_true_accessibility": "MEDIUM",
                "public_dataset_availability": "PLAUSIBLE",
                "observable_clarity": "HIGH",
                "slot4_independence": "INDEPENDENT",
                "experimental_feasibility": "HIGH",
                "claim_risk_level": "LOW",
                "selection_score": 0.85,
                "recommended_action": "SELECT_FOR_SOURCE_AND_YTRUE_SCREENING"
            }
        ], f)

    with open(tmp_path / "data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json", "w", encoding="utf-8") as f:
        json.dump({"decision_ref": "PIVOT-v46-001", "next_candidate_family": "PHI_CURVATURE"}, f)

    with open(tmp_path / "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json", "w", encoding="utf-8") as f:
        json.dump({"redefinition_status": "PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY"}, f)

    with open(tmp_path / "data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json", "w", encoding="utf-8") as f:
        json.dump({"predictive_gain_permission": "BLOCKED_NO_YTRUE"}, f)

    with open(tmp_path / "data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json", "w", encoding="utf-8") as f:
        json.dump({"requirement_status": "REQUIRED_BUT_NOT_CURRENTLY_FEASIBLE"}, f)

    with open(tmp_path / "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json", "w", encoding="utf-8") as f:
        json.dump({"status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}, f)


def test_loader_loads_successfully_when_present(tmp_path: Path) -> None:
    write_mock_v4_7_inputs(tmp_path)
    inputs = load_screening_inputs(tmp_path)
    assert "pivot_decision_v4_6" in inputs
    assert inputs["closed_loop_dir_exists"] is False
