"""Claim risk screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import ClaimRiskScreen

def screen_claim_risk(inputs: dict[str, Any]) -> ClaimRiskScreen:
    # Check selection matrix record or defaults
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    # Allow test overrides
    physical_risk = str(inputs.get("override_physical_claim_risk") or record.get("claim_risk_level") or "LOW")
    slot4_dep = str(inputs.get("override_slot4_independence") or record.get("slot4_independence") or "INDEPENDENT")

    
    slot4_risk = "LOW" if slot4_dep == "INDEPENDENT" else ("HIGH" if slot4_dep == "DEPENDENT_BLOCKING" else "MEDIUM")
    
    if physical_risk == "HIGH" or slot4_risk == "HIGH":
        score = 0.8
    elif physical_risk == "MEDIUM":
        score = 0.5
    else:
        score = 0.2

    mitigation_rules = [
        "Do not overclaim physical validity based on simulations alone.",
        "Ensure slot4 independence remains active unless explicitly resolved."
    ]

    return ClaimRiskScreen(
        candidate_family="PHI_CURVATURE",
        physical_claim_risk=physical_risk,
        source_overclaim_risk="MEDIUM" if physical_risk == "HIGH" else "LOW",
        benchmark_laundering_risk="LOW",
        slot4_dependency_risk=slot4_risk,
        predictive_gain_misuse_risk="LOW",
        mitigation_rules=mitigation_rules,
        claim_risk_score=score,
    )
