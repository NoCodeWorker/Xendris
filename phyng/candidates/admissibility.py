"""
Phygn v1.4 — Candidate Admissibility Classifier

Classifies a candidate model's admissibility based on dimensional analysis,
parameter status, and family characteristics.
"""

from __future__ import annotations

from phyng.candidates.schemas import CandidatePredictionSpec, AdmissibilityStatus

def classify_candidate_admissibility(
    candidate: CandidatePredictionSpec,
    family_id: str | None = None,
) -> AdmissibilityStatus:
    """
    Classifies the admissibility of a candidate model spec.
    """
    # 1. Missing units check
    if not candidate.term_units or not candidate.alpha_units or not candidate.dimensionless_core:
        return "BLOCKED_DIMENSIONAL_INCOMPLETE"
        
    # 2. Parameter status checks
    if candidate.parameter_status == "FREE_UNCONSTRAINED":
        return "UNDERIDENTIFIED_CANDIDATE"
        
    if candidate.parameter_status == "AD_HOC":
        return "BLOCKED_AS_AD_HOC_CANDIDATE"
        
    if candidate.parameter_status == "SOURCE_BACKED":
        return "REQUIRES_SOURCE_BACKING"
        
    # 3. Family-specific checks
    if family_id in ("B_SUPPRESSED", "QB_STRUCTURAL"):
        if candidate.parameter_status == "PRE_REGISTERED":
            return "ADMISSIBLE_NEGATIVE_CONTROL"
            
    if family_id == "LOG_BOUNDARY":
        if candidate.parameter_status == "PRE_REGISTERED":
            return "ADMISSIBLE_TOY_CANDIDATE"
        else:
            return "REQUIRES_PARAMETER_PRIOR"
            
    # Default fallback
    return "REQUIRES_PARAMETER_PRIOR"
