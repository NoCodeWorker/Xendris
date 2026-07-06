"""
xendris.core.sectors — [EXPERIMENTAL] Epistemic Sectors.

WARNING: This module is EXPERIMENTAL. The types below are minimal stubs
to satisfy imports from other experimental packages (runtime, orchestrator).
The full implementation lives in the `experimental-trust-layers` branch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EpistemicSector(str, Enum):
    FACTUAL = "FACTUAL"
    INFERRED = "INFERRED"
    CALCULATED = "CALCULATED"
    HYPOTHETICAL = "HYPOTHETICAL"
    CREATIVE = "CREATIVE"
    CODE_STATE = "CODE_STATE"
    USER_PROVIDED = "USER_PROVIDED"
    BENCHMARK = "BENCHMARK"
    PRODUCTION = "PRODUCTION"
    EXPLORATORY = "EXPLORATORY"
    HYPOTHESIS = "HYPOTHESIS"
    LATENCY = "LATENCY"


@dataclass
class SectorTransition:
    source_sector: str = ""
    target_sector: str = ""
    evidence_bridge: str = ""


@dataclass
class SectorTransitionDecision:
    decision: str = "ALLOW"
    allowed: bool = True
    source_sector: str = ""
    target_sector: str = ""
    reason: str = "STUB"
    risk_level: str = "LOW"
    transition: SectorTransition | None = None
    required_evidence: tuple = field(default_factory=tuple)
    limitations: tuple = field(default_factory=tuple)
    audit_tags: tuple = field(default_factory=tuple)


class SectorTransitionEngine:
    def __init__(self, guard: Any = None) -> None:
        self.guard = guard

    @staticmethod
    def evaluate(source: EpistemicSector, target: EpistemicSector) -> dict:
        return {"decision": "ALLOW", "reason": "STUB", "risk_level": "LOW"}

    def execute_transition(
        self,
        claim: Any = None,
        source_sector: EpistemicSector | None = None,
        target_sector: EpistemicSector | None = None,
        evidence_bridge: Any = None,
        local_context: Any = None,
        requested_claim_type: Any = None,
    ) -> SectorTransitionDecision:
        source_value = source_sector.value if source_sector else ""
        target_value = target_sector.value if target_sector else ""
        context_value = getattr(local_context, "value", str(local_context))
        claim_type = getattr(claim, "claim_type", None)
        claim_type_value = getattr(claim_type, "value", str(claim_type))
        risk = getattr(claim, "risk_level", None)
        risk_value = getattr(risk, "value", str(risk))

        if source_value == "LATENCY" and target_value == "PRODUCTION":
            return SectorTransitionDecision(
                decision="BLOCK",
                allowed=False,
                source_sector=source_value,
                target_sector=target_value,
                reason="DRY_RUN_LATENCY_TO_PRODUCTION_LATENCY_BLOCKED",
                risk_level="HIGH",
                required_evidence=("production latency evidence",),
                audit_tags=("LATENCY", "PRODUCTION"),
            )

        if source_value == "LATENCY" and getattr(requested_claim_type, "value", str(requested_claim_type)) == "FACTUAL":
            return SectorTransitionDecision(
                decision="BLOCK",
                allowed=False,
                source_sector=source_value,
                target_sector=target_value,
                reason="LATENCY_TO_ACCURACY_BLOCKED",
                risk_level="HIGH",
                required_evidence=("accuracy evidence independent of latency",),
                audit_tags=("LATENCY", "ACCURACY_PROXY"),
            )

        if risk_value == "HIGH" and evidence_bridge is None:
            return SectorTransitionDecision(
                decision="HUMAN_REVIEW_REQUIRED",
                allowed=False,
                source_sector=source_value,
                target_sector=target_value,
                reason="HIGH_RISK_TRANSITION_REQUIRES_EVIDENCE",
                risk_level="HIGH",
                required_evidence=("explicit evidence bridge",),
                audit_tags=("HIGH_RISK",),
            )

        if claim_type_value == "CODE_STATE" and context_value == "PRODUCTION" and evidence_bridge is None:
            return SectorTransitionDecision(
                decision="BLOCK",
                allowed=False,
                source_sector=source_value,
                target_sector=target_value,
                reason="PRODUCTION_READINESS_NOT_ESTABLISHED",
                risk_level="MEDIUM",
                required_evidence=("deployment evidence", "test evidence"),
                audit_tags=("CODE_STATE", "PRODUCTION"),
            )

        return SectorTransitionDecision(
            decision="ALLOW",
            allowed=True,
            source_sector=source_value,
            target_sector=target_value,
            reason="STUB",
        )


__all__ = ["EpistemicSector", "SectorTransition", "SectorTransitionDecision", "SectorTransitionEngine"]
