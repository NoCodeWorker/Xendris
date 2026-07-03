"""Observable accessibility screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import ObservableAccessibilityScreen

def screen_observable_accessibility(inputs: dict[str, Any]) -> ObservableAccessibilityScreen:
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    # Allow overrides
    clarity = inputs.get("override_observable_clarity", record.get("observable_clarity", "HIGH"))

    if clarity == "HIGH":
        score = 0.8
    elif clarity == "MEDIUM":
        score = 0.5
    else:
        score = 0.1

    return ObservableAccessibilityScreen(
        candidate_family="PHI_CURVATURE",
        proposed_observables=["curvature_coefficient", "phase_decay_rate"],
        observable_classes=["CURVATURE_PROXY", "DECOHERENCE_RATE"],
        directly_measurable=["phase_decay_rate"],
        proxy_observables=["curvature_coefficient"],
        blocked_observables=[],
        observable_clarity=clarity,
        observable_accessibility_score=score,
        notes=["Curvature requires a second-order derivative proxy from raw signal."]
    )
