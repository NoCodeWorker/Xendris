"""
xendris.core.boundary — [EXPERIMENTAL] Algebraic Trust Boundary.

WARNING: This module is EXPERIMENTAL. The types below are minimal stubs
to satisfy imports from other experimental packages (runtime, orchestrator).
The full implementation lives in the `experimental-trust-layers` branch.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class EvidenceBridgeType(str, Enum):
    EXACT = "EXACT"
    DERIVED = "DERIVED"
    CROSS_DOMAIN = "CROSS_DOMAIN"
    BENCHMARK_ARTIFACT = "BENCHMARK_ARTIFACT"
    DEPLOYMENT_LOG = "DEPLOYMENT_LOG"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    TEST_RESULT = "TEST_RESULT"


class EvidenceBridge:
    def __init__(self, bridge_type: EvidenceBridgeType = EvidenceBridgeType.EXACT, **kwargs: Any) -> None:
        self.bridge_type = bridge_type
        for k, v in kwargs.items():
            setattr(self, k, v)


class ContaminationGuard:
    @staticmethod
    def check(source_claim: Any, target_context: Any) -> Any:
        from xendris.core.boundary.evidence_bridge import BoundaryDecision
        return ContaminationGuard().assess_transition(source_claim, target_context)

    def assess_transition(
        self,
        source_claim: Any = None,
        target_context: Any = None,
        requested_target_claim_type: Any = None,
        evidence_bridge: Any = None,
    ) -> Any:
        from xendris.core.boundary.evidence_bridge import BoundaryDecision

        content = str(getattr(source_claim, "content", "")).lower()
        source_context = getattr(source_claim, "context", None)
        claim_type = getattr(source_claim, "claim_type", None)
        source_context_value = getattr(source_context, "value", str(source_context))
        target_context_value = getattr(target_context, "value", str(target_context))
        requested_type_value = getattr(requested_target_claim_type, "value", str(requested_target_claim_type))
        claim_type_value = getattr(claim_type, "value", str(claim_type))

        base = {
            "source_context": source_context,
            "target_context": target_context,
            "requested_target_claim_type": requested_target_claim_type,
        }

        if (source_context_value == "LATENCY" or "dry-run latency" in content) and target_context_value == "PRODUCTION":
            return BoundaryDecision(
                decision="BLOCK",
                reason="DRY_RUN_LATENCY_TO_PRODUCTION_LATENCY_BLOCKED",
                allowed=False,
                required_evidence=("production latency evidence",),
                audit_tags=("LATENCY", "PRODUCTION"),
                **base,
            )

        if source_context_value == "LATENCY" and requested_type_value == "FACTUAL":
            return BoundaryDecision(
                decision="BLOCK",
                reason="LATENCY_TO_ACCURACY_BLOCKED",
                allowed=False,
                required_evidence=("accuracy evidence independent of latency",),
                audit_tags=("LATENCY", "ACCURACY_PROXY"),
                **base,
            )

        if claim_type_value == "CODE_STATE" and target_context_value == "PRODUCTION" and evidence_bridge is None:
            return BoundaryDecision(
                decision="BLOCK",
                reason="PRODUCTION_READINESS_NOT_ESTABLISHED",
                allowed=False,
                required_evidence=("deployment evidence", "test evidence"),
                audit_tags=("CODE_STATE", "PRODUCTION"),
                **base,
            )

        if "superior" in content and evidence_bridge is None:
            return BoundaryDecision(
                decision="ALLOW_WITH_LIMITATIONS",
                reason="UNIVERSAL_SUPERIORITY_DOWNGRADED",
                allowed=True,
                limitations=("Only state that the system outperformed DeepSeek within the scoped benchmark, if measured.",),
                required_evidence=("external validation for broader superiority",),
                audit_tags=("OVERCLAIM", "DOWNGRADE"),
                **base,
            )

        return BoundaryDecision(decision="ALLOW", reason="STUB", **base)


__all__ = ["EvidenceBridgeType", "EvidenceBridge", "ContaminationGuard"]
