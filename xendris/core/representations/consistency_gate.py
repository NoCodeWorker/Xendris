"""Consistency gate and decision definitions for ClaimRepresentations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.algebra.claim_object import ClaimObject
from xendris.core.local.context import LocalContext
from xendris.core.boundary.contamination_guard import ContaminationGuard
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.sectors.transition_engine import SectorTransitionEngine
from xendris.core.representations.representation import ClaimRepresentation
from xendris.core.representations.equivalence import RepresentationRelation, RepresentationComparison
from xendris.core.representations.contradiction import compare_representations
from xendris.core.trust.types import ClaimStatus, ClaimType, RiskLevel


@dataclass(frozen=True)
class RepresentationConsistencyDecision:
    """The result of evaluating consistency across multiple representations."""

    decision: str  # ALLOW, ALLOW_WITH_LIMITATIONS, ALLOW_AS_HYPOTHESIS, HUMAN_REVIEW, BLOCK
    relation: RepresentationRelation
    allowed: bool
    reason: str
    recommended_claim: ClaimRepresentation | None = None
    rejected_claims: tuple[ClaimRepresentation, ...] = ()
    limitations: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    audit_tags: tuple[str, ...] = ()


class RepresentationConsistencyGate:
    """Validator ensuring consistency and safety across multiple claim representations."""

    def __init__(
        self,
        engine: SectorTransitionEngine | None = None,
        guard: ContaminationGuard | None = None,
    ) -> None:
        self.engine = engine or SectorTransitionEngine()
        self.guard = guard or ContaminationGuard()

    def check_consistency(
        self,
        representations: list[ClaimRepresentation],
        target_sector: EpistemicSector | None = None,
        target_context: LocalContext | None = None,
        strictness_level: str | None = None,
        requested_claim_type: ClaimType | None = None,
    ) -> tuple[RepresentationConsistencyDecision, list[RepresentationComparison]]:
        """Validate consistency and return the decision and pairwise comparisons."""
        if not representations:
            return RepresentationConsistencyDecision(
                decision="BLOCK",
                relation=RepresentationRelation.REQUIRES_HUMAN_REVIEW,
                allowed=False,
                reason="NO_REPRESENTATIONS_PROVIDED",
            ), []

        if len(representations) == 1:
            # Single representation: audit against sector transition if target is specified
            rep = representations[0]
            decision_val = "ALLOW"
            reason_str = "SINGLE_REPRESENTATION_PASSED"
            allowed_val = True
            
            # Map ClaimRepresentation to ClaimObject for composition
            claim_obj = ClaimObject(
                claim_id=rep.claim_id,
                content=rep.content,
                claim_type=ClaimType(rep.claim_type),
                claim_status=ClaimStatus.VERIFIED if rep.confidence >= 0.75 else ClaimStatus.UNSUPPORTED,
                risk_level=RiskLevel.MEDIUM,
                context=LocalContext(rep.source_context),
                metadata=rep.metadata,
                evidence_refs=rep.evidence_refs,
            )

            if target_sector is not None:
                final_req_type = requested_claim_type or ClaimType(rep.claim_type)
                sec_dec = self.engine.execute_transition(
                    claim=claim_obj,
                    source_sector=EpistemicSector(rep.epistemic_sector),
                    target_sector=target_sector,
                    local_context=target_context,
                    requested_claim_type=final_req_type,
                )
                decision_val = sec_dec.decision
                reason_str = sec_dec.reason
                allowed_val = sec_dec.allowed

            return RepresentationConsistencyDecision(
                decision=decision_val,
                relation=RepresentationRelation.EQUIVALENT,
                allowed=allowed_val,
                reason=reason_str,
                recommended_claim=rep,
            ), []

        # Perform pairwise comparisons
        comparisons: list[RepresentationComparison] = []
        for i in range(len(representations)):
            for j in range(i + 1, len(representations)):
                comp = compare_representations(representations[i], representations[j])
                comparisons.append(comp)

        # Aggregate relations and pick decision
        has_contradiction = any(c.relation == RepresentationRelation.CONTRADICTORY for c in comparisons)
        has_overgeneralization = any(c.relation == RepresentationRelation.OVERGENERALIZED for c in comparisons)
        has_evidence_mismatch = any(c.relation == RepresentationRelation.EVIDENCE_MISMATCH for c in comparisons)
        has_underspecified = any(c.relation == RepresentationRelation.UNDERSPECIFIED for c in comparisons)
        has_partial = any(c.relation == RepresentationRelation.PARTIALLY_EQUIVALENT for c in comparisons)
        has_disjoint = any(c.relation == RepresentationRelation.DISJOINT for c in comparisons)

        # Risk level determination based on comparisons
        max_risk = RiskLevel.LOW
        for c in comparisons:
            if c.risk_level == RiskLevel.CRITICAL:
                max_risk = RiskLevel.CRITICAL
                break
            elif c.risk_level == RiskLevel.HIGH:
                max_risk = RiskLevel.HIGH

        # Choice of recommended claim: pick the most cautious (the one with lowest confidence or most limitations)
        sorted_reps = sorted(
            representations,
            key=lambda r: (len(r.limitations), -r.confidence),
            reverse=True,
        )
        recommended = sorted_reps[0]
        rejected = tuple(sorted_reps[1:])

        # Evaluation order
        if has_contradiction:
            if max_risk == RiskLevel.CRITICAL:
                return RepresentationConsistencyDecision(
                    decision="HUMAN_REVIEW",
                    relation=RepresentationRelation.CONTRADICTORY,
                    allowed=False,
                    reason="CRITICAL_CONTRADICTION_DETECTED",
                    rejected_claims=tuple(representations),
                    audit_tags=("CONTRADICTION", "CRITICAL_RISK"),
                ), comparisons
            else:
                return RepresentationConsistencyDecision(
                    decision="BLOCK",
                    relation=RepresentationRelation.CONTRADICTORY,
                    allowed=False,
                    reason="HIGH_RISK_CONTRADICTION_DETECTED",
                    rejected_claims=tuple(representations),
                    audit_tags=("CONTRADICTION", "HIGH_RISK"),
                ), comparisons

        if has_overgeneralization:
            # Attempt to downgrade to safe scoped claim
            if max_risk == RiskLevel.CRITICAL:
                return RepresentationConsistencyDecision(
                    decision="BLOCK",
                    relation=RepresentationRelation.OVERGENERALIZED,
                    allowed=False,
                    reason="CRITICAL_OVERGENERALIZATION_BLOCKED",
                    rejected_claims=tuple(representations),
                    audit_tags=("OVERGENERALIZATION", "CRITICAL_RISK"),
                ), comparisons
            else:
                # Safe downgrade to limited claim
                return RepresentationConsistencyDecision(
                    decision="ALLOW_WITH_LIMITATIONS",
                    relation=RepresentationRelation.OVERGENERALIZED,
                    allowed=True,
                    reason="OVERGENERALIZATION_DOWNGRADED_TO_SCOPED_CLAIM",
                    recommended_claim=recommended,
                    rejected_claims=rejected,
                    limitations=("Claim downgraded and restricted to close benchmark parameters",),
                    audit_tags=("OVERGENERALIZATION", "DOWNGRADE"),
                ), comparisons

        if has_evidence_mismatch:
            return RepresentationConsistencyDecision(
                decision="BLOCK",
                relation=RepresentationRelation.EVIDENCE_MISMATCH,
                allowed=False,
                reason="EVIDENCE_MISMATCH_DETECTED",
                rejected_claims=tuple(representations),
                audit_tags=("EVIDENCE_MISMATCH",),
            ), comparisons

        if has_disjoint:
            return RepresentationConsistencyDecision(
                decision="ALLOW_WITH_LIMITATIONS",
                relation=RepresentationRelation.DISJOINT,
                allowed=True,
                reason="DISJOINT_REPRESENTATIONS_DO_NOT_FORCE_CONSENSUS",
                limitations=("Representations are logically disjoint, evaluated independently",),
                audit_tags=("DISJOINT",),
            ), comparisons

        if has_underspecified:
            return RepresentationConsistencyDecision(
                decision="ALLOW_WITH_LIMITATIONS",
                relation=RepresentationRelation.UNDERSPECIFIED,
                allowed=True,
                reason="UNDERSPECIFIED_REPRESENTATION_ADMITTED_WITH_LIMITATIONS",
                recommended_claim=recommended,
                limitations=("Lacks complete run configuration metadata",),
                audit_tags=("UNDERSPECIFIED",),
            ), comparisons

        # Check if exploratory (exploratory content gets ALLOW_AS_HYPOTHESIS)
        is_exploratory = any(
            "explore" in r.content.lower()
            or "hypothesis" in r.content.lower()
            or "may indicate" in r.content.lower()
            for r in representations
        )
        if is_exploratory:
            return RepresentationConsistencyDecision(
                decision="ALLOW_AS_HYPOTHESIS",
                relation=RepresentationRelation.PARTIALLY_EQUIVALENT if has_partial else RepresentationRelation.EQUIVALENT,
                allowed=True,
                reason="EXPLORATORY_REPRESENTATIONS_ALLOWED_AS_HYPOTHESIS",
                recommended_claim=recommended,
                limitations=("Exploratory speculative claim only, not verified factual knowledge",),
                audit_tags=("EXPLORATORY",),
            ), comparisons

        if has_partial:
            return RepresentationConsistencyDecision(
                decision="ALLOW_WITH_LIMITATIONS",
                relation=RepresentationRelation.PARTIALLY_EQUIVALENT,
                allowed=True,
                reason="PARTIALLY_EQUIVALENT_REPRESENTATIONS_ALLOWED_WITH_LIMITATIONS",
                recommended_claim=recommended,
                rejected_claims=rejected,
                limitations=recommended.limitations,
                audit_tags=("PARTIALLY_EQUIVALENT",),
            ), comparisons

        # Default Equivalent
        return RepresentationConsistencyDecision(
            decision="ALLOW",
            relation=RepresentationRelation.EQUIVALENT,
            allowed=True,
            reason="ALL_REPRESENTATIONS_LOGICALLY_EQUIVALENT",
            recommended_claim=recommended,
        ), comparisons
