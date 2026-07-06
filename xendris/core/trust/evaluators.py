"""Deterministic evaluator for the Xendris Trust Kernel."""

from __future__ import annotations

from collections.abc import Sequence

from .audit import ReasoningAudit
from .claims import Claim
from .evidence import EvidenceBinding
from .types import AuditDecision, ClaimStatus, ClaimType, RiskLevel


_EVIDENCE_REQUIRED_TYPES = {
    ClaimType.FACTUAL,
    ClaimType.CALCULATED,
    ClaimType.CODE_STATE,
}


def _average_confidence(claims: Sequence[Claim]) -> float:
    if not claims:
        return 0.5
    return sum(claim.confidence for claim in claims) / len(claims)


class TrustKernelEvaluator:
    """Evaluate declared claims with deterministic structural rules."""

    def evaluate(
        self,
        answer: str,
        claims: Sequence[Claim],
        evidence_bindings: Sequence[EvidenceBinding] = (),
    ) -> ReasoningAudit:
        claims_tuple = tuple(claims)
        support_scores = {
            binding.claim: binding.support_score
            for binding in evidence_bindings
        }
        insufficient_evidence_claims = tuple(
            claim
            for claim in claims_tuple
            if claim.claim_type in _EVIDENCE_REQUIRED_TYPES
            and claim.status == ClaimStatus.VERIFIED
            and support_scores.get(claim, 0.0) < 0.75
        )
        global_confidence = min(max(_average_confidence(claims_tuple), 0.0), 1.0)
        unsupported_claims = tuple(
            claim
            for claim in claims_tuple
            if claim.status == ClaimStatus.UNSUPPORTED
            or claim in insufficient_evidence_claims
        )

        if not claims_tuple:
            return ReasoningAudit(
                answer=answer,
                claims=(),
                global_confidence=min(global_confidence, 0.5),
                risk_level=RiskLevel.MEDIUM,
                decision=AuditDecision.HUMAN_REVIEW_REQUIRED,
                unsupported_claims=(),
                notes="No claims were provided for structural audit.",
            )

        if any(claim.status == ClaimStatus.CONTRADICTED for claim in claims_tuple):
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.HIGH,
                decision=AuditDecision.BLOCKED,
                unsupported_claims=unsupported_claims,
                notes="At least one claim is contradicted.",
            )

        if insufficient_evidence_claims:
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.HIGH,
                decision=AuditDecision.HUMAN_REVIEW_REQUIRED,
                unsupported_claims=unsupported_claims,
                notes=(
                    "Factual, calculated, or code-state claims marked VERIFIED "
                    "require evidence support score >= 0.75. Contradictory "
                    "evidence detection is deferred."
                ),
            )

        high_confidence_unsupported = any(
            claim.status == ClaimStatus.UNSUPPORTED
            and support_scores.get(claim, 0.0) < 0.75
            and claim.confidence >= 0.70
            for claim in claims_tuple
        )
        if high_confidence_unsupported:
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.HIGH,
                decision=AuditDecision.HUMAN_REVIEW_REQUIRED,
                unsupported_claims=unsupported_claims,
                notes="High-confidence unsupported claim requires human review.",
            )

        if unsupported_claims:
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.MEDIUM,
                decision=AuditDecision.APPROVED_WITH_LIMITATIONS,
                unsupported_claims=unsupported_claims,
                notes="Unsupported claims are present.",
            )

        if all(claim.claim_type == ClaimType.USER_PROVIDED for claim in claims_tuple):
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.MEDIUM,
                decision=AuditDecision.APPROVED_WITH_LIMITATIONS,
                unsupported_claims=(),
                notes="User-provided claims are accepted as input with limitations.",
            )

        if all(
            claim.status == ClaimStatus.VERIFIED or claim.claim_type == ClaimType.USER_PROVIDED
            for claim in claims_tuple
        ):
            return ReasoningAudit(
                answer=answer,
                claims=claims_tuple,
                global_confidence=global_confidence,
                risk_level=RiskLevel.LOW,
                decision=AuditDecision.APPROVED,
                unsupported_claims=(),
            )

        return ReasoningAudit(
            answer=answer,
            claims=claims_tuple,
            global_confidence=global_confidence,
            risk_level=RiskLevel.MEDIUM,
            decision=AuditDecision.APPROVED_WITH_LIMITATIONS,
            unsupported_claims=unsupported_claims,
            notes="Mixed support statuses require limitations.",
        )


def evaluate_claims(
    answer: str,
    claims: Sequence[Claim],
    evidence_bindings: Sequence[EvidenceBinding] = (),
) -> ReasoningAudit:
    """Evaluate declared claims using the default deterministic evaluator."""

    return TrustKernelEvaluator().evaluate(
        answer=answer,
        claims=claims,
        evidence_bindings=evidence_bindings,
    )
