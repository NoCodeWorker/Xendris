"""Tests for v4.6 candidate experiment requirement."""

from __future__ import annotations

from phyng.candidate_decision.experiment_requirement import evaluate_experiment_requirement


def test_experiment_requirement_details() -> None:
    inputs = {}
    exp = evaluate_experiment_requirement(inputs)
    assert exp.candidate_id == "PHI_GRADIENT"
    assert exp.requirement_status == "REQUIRED_BUT_NOT_CURRENTLY_FEASIBLE"
    assert "visibility_loss" in exp.required_observables
    assert exp.minimum_measurements == 10
    assert exp.feasibility_risk == "HIGH"
    assert exp.recommended_action == "REQUIRES_EXPERIMENT_DESIGN"
