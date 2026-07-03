"""Y_true accessibility screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import YTrueAccessibilityScreen

def screen_ytrue_accessibility(inputs: dict[str, Any]) -> YTrueAccessibilityScreen:
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    feasibility = str(inputs.get("override_ytrue_accessibility") or record.get("y_true_accessibility") or "MEDIUM")

    if feasibility == "HIGH":
        score = 0.8
        experiment = False
    elif feasibility == "MEDIUM":
        score = 0.4
        experiment = False
    elif feasibility == "LOW":
        score = 0.2
        experiment = True
    else:
        score = 0.0
        experiment = True

    return YTrueAccessibilityScreen(
        candidate_family="PHI_CURVATURE",
        target_observables=["curvature_coefficient"],
        plausible_ytrue_sources=["literature_tables", "supplementary_data"],
        manual_extraction_likelihood="MEDIUM" if feasibility == "MEDIUM" else feasibility,
        public_dataset_likelihood="LOW",
        experiment_required=experiment,
        minimum_ytrue_feasibility=feasibility,
        ytrue_accessibility_score=score,
        blockers=[] if score > 0.0 else ["No plausible y_true path available"]
    )
