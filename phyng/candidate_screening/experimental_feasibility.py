"""Experimental feasibility screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import ExperimentalFeasibilityScreen

def screen_experimental_feasibility(inputs: dict[str, Any]) -> ExperimentalFeasibilityScreen:
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    feasibility = str(inputs.get("override_feasibility_level") or record.get("experimental_feasibility") or "HIGH")

    if feasibility == "HIGH":
        score = 0.8
    elif feasibility == "MEDIUM":
        score = 0.5
    elif feasibility == "LOW":
        score = 0.2
    else:
        score = 0.0

    return ExperimentalFeasibilityScreen(
        candidate_family="PHI_CURVATURE",
        required_observables=["curvature_coefficient"],
        possible_experiment_classes=["INTERFEROMETER_SWEEP"],
        required_apparatus=["Phase shifter", "Interferometer"],
        required_sensitivity="1e-5",
        feasibility_level=feasibility,
        cost_risk="MEDIUM" if feasibility == "HIGH" else "HIGH",
        timeline_risk="LOW" if feasibility == "HIGH" else "MEDIUM",
        experiment_accessibility_score=score,
        notes=["Local interferometer apparatus can be easily adapted to sweep phase curvature."]
    )
