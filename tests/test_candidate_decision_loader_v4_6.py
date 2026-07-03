"""Tests for v4.6 candidate decision loader."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from phyng.candidate_decision.loader import load_candidate_decision_inputs, MissingFreezeDecisionError


def test_missing_freeze_decision_blocks_review(tmp_path: Path) -> None:
    # No files written, so freeze decision is missing
    with pytest.raises(MissingFreezeDecisionError):
        load_candidate_decision_inputs(tmp_path)


def write_mock_v4_6_inputs(tmp_path: Path) -> None:
    # Create necessary subdirectories
    (tmp_path / "data/external_evidence").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/y_true").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/model_comparison").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/debts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/audits/remediation").mkdir(parents=True, exist_ok=True)

    # Write files
    with open(tmp_path / "data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json", "w", encoding="utf-8") as f:
        json.dump({"accepted_y_true_count": 0, "freeze_status": "FROZEN_NO_YTRUE_AVAILABLE", "decision_id": "FREEZE-v45-001"}, f)

    with open(tmp_path / "data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json", "w", encoding="utf-8") as f:
        json.dump({"predictive_gain_status": "UNDEFINED_INSUFFICIENT_YTRUE", "ready_for_predictive_gain": False}, f)

    with open(tmp_path / "data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json", "w", encoding="utf-8") as f:
        json.dump({"records": []}, f)

    with open(tmp_path / "data/external_evidence/phi_gradient_table_review_results_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json", "w", encoding="utf-8") as f:
        json.dump([], f)

    with open(tmp_path / "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json", "w", encoding="utf-8") as f:
        json.dump({"status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"}, f)

    with open(tmp_path / "data/audits/remediation/phygn_v4_4_2_continuation_gate.json", "w", encoding="utf-8") as f:
        json.dump({"gate_status": "RESUME_ALLOWED_WITH_RESIDUAL_DEBT"}, f)


def test_loader_loads_successfully_when_present(tmp_path: Path) -> None:
    write_mock_v4_6_inputs(tmp_path)
    inputs = load_candidate_decision_inputs(tmp_path)
    assert "assembled_dataset_v4_5" in inputs
    assert inputs["closed_loop_dir_exists"] is False
