"""Source accessibility screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import SourceAccessibilityScreen

def screen_source_accessibility(inputs: dict[str, Any]) -> SourceAccessibilityScreen:
    # Use selection matrix to find PHI_CURVATURE or defaults
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    # Allow test overrides
    source_quality = str(inputs.get("override_source_location_quality") or record.get("source_support_availability") or "MEDIUM")

    
    if source_quality == "HIGH":
        score = 0.9
        action = "Integrate existing local references"
    elif source_quality == "MEDIUM":
        score = 0.6
        action = "Perform targeted literature search for curvature coefficients"
    elif source_quality == "LOW":
        score = 0.2
        action = "Manual review of unindexed references required"
    else:
        score = 0.0
        action = "Source acquisition blocked"

    return SourceAccessibilityScreen(
        candidate_family="PHI_CURVATURE",
        likely_source_domains=["quantum_optics", "decoherence_physics"],
        known_source_refs=["Phys. Rev. A 102, 022101", "Nature Physics 15, 890"],
        local_source_refs=[],
        source_location_quality=source_quality,
        source_accessibility_score=score,
        blockers=[] if score > 0.2 else ["No local or known indexed literature found"],
        recommended_next_action=action,
    )
