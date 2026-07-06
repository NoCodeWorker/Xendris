"""Validation contracts for Xendris Trust Kernel audit objects."""

from __future__ import annotations

from .audit import ReasoningAudit
from .types import AuditDecision, ClaimStatus, RiskLevel


def validate_reasoning_audit(audit: ReasoningAudit) -> bool:
    """Validate structural coherence of a reasoning audit.

    This does not validate factual truth. It only checks that the audit object
    is internally coherent.
    """

    if not audit.answer.strip():
        return False
    if not 0.0 <= audit.global_confidence <= 1.0:
        return False
    if not audit.claims and not audit.notes:
        return False

    unsupported = tuple(claim for claim in audit.claims if claim.status == ClaimStatus.UNSUPPORTED)
    if set(unsupported) - set(audit.unsupported_claims):
        return False

    has_contradiction = any(claim.status == ClaimStatus.CONTRADICTED for claim in audit.claims)
    if has_contradiction and audit.decision not in {
        AuditDecision.BLOCKED,
        AuditDecision.HUMAN_REVIEW_REQUIRED,
    }:
        return False

    if audit.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL} and audit.decision == AuditDecision.APPROVED:
        if not audit.notes:
            return False

    return True
