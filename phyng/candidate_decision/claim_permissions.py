"""Claim permissions module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import FinalClaimPermissions

def establish_claim_permissions(inputs: dict[str, Any], freeze_review_ref: str) -> FinalClaimPermissions:
    allowed_claims = [
        "PHI_GRADIENT was evaluated as a benchmark candidate.",
        "PHI_GRADIENT failed to obtain accepted y_true from available sources.",
        "PHI_GRADIENT is frozen as empirically ungrounded under current artifacts.",
        "PHI_GRADIENT may remain useful as a methodological stress-test if redefined."
    ]

    blocked_claims = [
        "PHI_GRADIENT is predictively validated.",
        "PHI_GRADIENT has PredictiveGain.",
        "PHI_GRADIENT is empirically supported.",
        "PHI_GRADIENT is a source-backed physical mechanism.",
        "PHI_GRADIENT validates Frontera C.",
        "PHI_GRADIENT confirms the invariant."
    ]

    required_to_unblock = [
        "at least 3 accepted y_true records",
        "matched predictions",
        "source provenance",
        "QC pass",
        "either SLOT_4 debt resolution or explicit non-SLOT_4 claim scope"
    ]

    return FinalClaimPermissions(
        candidate_id="PHI_GRADIENT",
        decision_ref=freeze_review_ref,
        predictive_gain_permission="BLOCKED_NO_YTRUE",
        physical_claim_permission="BLOCKED",
        gradient_mechanism_claim_permission="BLOCKED_BY_SLOT4_DEBT",
        benchmark_method_permission="ALLOWED",
        method_only_permission="ALLOWED",
        allowed_claims=allowed_claims,
        blocked_claims=blocked_claims,
        archived_claims=[],
        required_to_unblock=required_to_unblock,
    )
