"""
Phygn v1.4 — Candidate Term Families

Defines candidate families for Frontera C.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

class CandidateFamily(BaseModel):
    candidate_family_id: str
    formula: str
    dimensionless_core: str
    required_parameters: list[str] = Field(default_factory=list)
    parameter_status: str
    default_admissibility: str
    failure_risks: list[str] = Field(default_factory=list)

CANDIDATE_FAMILIES = {
    "B_SUPPRESSED": CandidateFamily(
        candidate_family_id="B_SUPPRESSED",
        formula="DeltaGamma_C = alpha * B",
        dimensionless_core="B",
        required_parameters=["alpha"],
        parameter_status="PRE_REGISTERED",
        default_admissibility="ADMISSIBLE_NEGATIVE_CONTROL",
        failure_risks=["FAIL_UNDETECTABLE_DELTA", "FAIL_PARAMETER_UNDERIDENTIFIED"]
    ),
    "QB_STRUCTURAL": CandidateFamily(
        candidate_family_id="QB_STRUCTURAL",
        formula="DeltaGamma_C = alpha * Q * B",
        dimensionless_core="Q * B",
        required_parameters=["alpha"],
        parameter_status="PRE_REGISTERED",
        default_admissibility="ADMISSIBLE_NEGATIVE_CONTROL",
        failure_risks=["FAIL_UNDETECTABLE_DELTA", "FAIL_PARAMETER_UNDERIDENTIFIED"]
    ),
    "LOG_BOUNDARY": CandidateFamily(
        candidate_family_id="LOG_BOUNDARY",
        formula="DeltaGamma_C = alpha * sigma(a * u + b * w + c)",
        dimensionless_core="sigma(a * u + b * w + c)",
        required_parameters=["alpha", "a", "b", "c"],
        parameter_status="FREE_UNCONSTRAINED",
        default_admissibility="UNDERCONSTRAINED_UNLESS_PRIOR_DEFINED",
        failure_risks=["FAIL_PARAMETER_UNDERIDENTIFIED", "FAIL_GAIN_NONPOSITIVE"]
    ),
    "THRESHOLD_SATURATION": CandidateFamily(
        candidate_family_id="THRESHOLD_SATURATION",
        formula="DeltaGamma_C = alpha * B / (B + B_star)",
        dimensionless_core="B / (B + B_star)",
        required_parameters=["alpha", "B_star"],
        parameter_status="AD_HOC",
        default_admissibility="BLOCKED_IF_THRESHOLD_AD_HOC",
        failure_risks=["FAIL_AD_HOC_TERM", "FAIL_PARAMETER_UNDERIDENTIFIED"]
    )
}

def get_candidate_term_families() -> dict[str, CandidateFamily]:
    """Returns the registered candidate families."""
    return CANDIDATE_FAMILIES
