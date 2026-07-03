"""Experiment requirement module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import ExperimentRequirement

def evaluate_experiment_requirement(inputs: dict[str, Any]) -> ExperimentRequirement:
    return ExperimentRequirement(
        candidate_id="PHI_GRADIENT",
        requirement_status="REQUIRED_BUT_NOT_CURRENTLY_FEASIBLE",
        required_observables=["visibility_loss", "decoherence_rate"],
        minimum_measurements=10,
        required_sensitivity="1e-6",
        required_apparatus=["Interferometer apparatus", "Vacuum chamber"],
        feasibility_risk="HIGH",
        cost_risk="HIGH",
        timeline_risk="HIGH",
        reason="No literature or supplementary files exist for PHI_GRADIENT observed y_true. Only a custom experimental setup can produce these data.",
        recommended_action="REQUIRES_EXPERIMENT_DESIGN",
    )
