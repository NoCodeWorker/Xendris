"""
Phygn v0.8 — Baseline Readiness Classifier

Rules (from doc 45/47):
  no source           → TOY_INTERNAL  (or BASELINE_REQUIRES_SOURCE)
  background only     → BACKGROUND_SUPPORTED  (not ready)
  formula + obs       → SOURCE_BACKED_LIMITED  (max_claim_level=4)
  formula+obs+param+assumptions → SOURCE_BACKED_READY  (max_claim_level=5)
  contradiction       → CONTRADICTED

Candidate physical prediction remains blocked regardless of baseline status.
"""

from __future__ import annotations

from phyng.baselines.schemas import (
    BaselineReadinessResult,
    BaselineSourceSupport,
    VisibilityDecayBaselineSpec,
)

_CANDIDATE_BLOCKED = [
    "Phygn predicts gravitational decoherence.",
    "Boundary C causes decoherence.",
    "The source-backed baseline validates the boundary-aware candidate.",
    "SyntheticGain proves physical gain.",
]


def classify_baseline_readiness(
    spec: VisibilityDecayBaselineSpec,
    support_matrix: list[BaselineSourceSupport],
) -> BaselineReadinessResult:
    """
    Classify the readiness of the visibility-decay baseline model.

    Args:
        spec: The baseline specification (formula, parameters, assumptions).
        support_matrix: List of source-support records for this baseline.

    Returns:
        BaselineReadinessResult with status, claim level, and claim lists.
    """
    has_formula_support = any(
        s.support_level == "FORMULA_SUPPORT" and s.trust_level in {"PRIMARY", "HIGH"}
        for s in support_matrix
    )
    has_observable_support = any(
        s.support_level == "OBSERVABLE_SUPPORT" and s.trust_level in {"PRIMARY", "HIGH"}
        for s in support_matrix
    )
    has_parameter_support = any(
        s.support_level == "PARAMETER_SUPPORT" and s.trust_level in {"PRIMARY", "HIGH"}
        for s in support_matrix
    )
    has_contradiction = any(s.support_level == "CONTRADICTS" for s in support_matrix)
    has_background_only = (
        len(support_matrix) > 0
        and not has_formula_support
        and not has_observable_support
        and not has_parameter_support
        and not has_contradiction
    )

    # --- Contradiction is terminal -----------------------------------------
    if has_contradiction:
        return BaselineReadinessResult(
            model_id=spec.model_id,
            support_status="CONTRADICTED",
            parameter_status=spec.parameter_status,
            can_be_used_as_baseline=False,
            max_claim_level=0,
            missing_requirements=["Contradiction found in source matrix."],
            allowed_claims=[],
            blocked_claims=_CANDIDATE_BLOCKED + ["Baseline is contradicted by source evidence."],
        )

    # --- No sources at all --------------------------------------------------
    if not support_matrix:
        return BaselineReadinessResult(
            model_id=spec.model_id,
            support_status="BASELINE_REQUIRES_SOURCE",
            parameter_status=spec.parameter_status,
            can_be_used_as_baseline=False,
            max_claim_level=3,
            missing_requirements=[
                "FORMULA_SUPPORT at HIGH trust",
                "OBSERVABLE_SUPPORT at HIGH trust",
                "PARAMETER_SUPPORT or sourced Gamma_env",
                "Stated assumptions",
            ],
            allowed_claims=["Baseline is classified as TOY_INTERNAL pending source ingestion."],
            blocked_claims=_CANDIDATE_BLOCKED,
        )

    # --- Background only ---------------------------------------------------
    if has_background_only:
        return BaselineReadinessResult(
            model_id=spec.model_id,
            support_status="BACKGROUND_SUPPORTED",
            parameter_status=spec.parameter_status,
            can_be_used_as_baseline=False,
            max_claim_level=3,
            missing_requirements=[
                "FORMULA_SUPPORT at HIGH trust",
                "OBSERVABLE_SUPPORT at HIGH trust",
            ],
            allowed_claims=["Background literature found. Baseline remains TOY_INTERNAL."],
            blocked_claims=_CANDIDATE_BLOCKED,
        )

    # --- Source-backed limited (formula + observable) ----------------------
    has_assumptions = len(spec.assumptions) > 0
    if has_formula_support and has_observable_support:
        if has_parameter_support and has_assumptions:
            status = "SOURCE_BACKED_READY"
            level = 5
            allowed = [
                "CAMPAIGN-002 now uses a source-backed ready baseline for visibility decay.",
                "The candidate remains hypothetical and no physical prediction is claimed.",
            ]
            missing: list[str] = []
        else:
            status = "SOURCE_BACKED_LIMITED"
            level = 4
            allowed = [
                "CAMPAIGN-002 now uses a source-backed limited baseline for visibility decay.",
                "The candidate remains hypothetical and no physical prediction is claimed.",
            ]
            missing = []
            if not has_parameter_support:
                missing.append("PARAMETER_SUPPORT for Gamma_env")
            if not has_assumptions:
                missing.append("Explicit model assumptions required for READY status")
    elif has_formula_support and not has_observable_support:
        status = "SOURCE_BACKED_LIMITED"
        level = 4
        allowed = ["Formula has source support. Observable support still required for READY status."]
        missing = ["OBSERVABLE_SUPPORT at HIGH trust"]
    else:
        # Observable without formula — still limited
        status = "BACKGROUND_SUPPORTED"
        level = 3
        allowed = ["Partial support found. Baseline not yet source-backed."]
        missing = ["FORMULA_SUPPORT at HIGH trust"]

    return BaselineReadinessResult(
        model_id=spec.model_id,
        support_status=status,
        parameter_status=spec.parameter_status,
        can_be_used_as_baseline=(level >= 4),
        max_claim_level=level,
        missing_requirements=missing,
        allowed_claims=allowed,
        blocked_claims=_CANDIDATE_BLOCKED,
    )
