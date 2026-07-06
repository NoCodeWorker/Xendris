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


class EvidenceBridge:
    def __init__(self, bridge_type: EvidenceBridgeType = EvidenceBridgeType.EXACT, **kwargs: Any) -> None:
        self.bridge_type = bridge_type
        for k, v in kwargs.items():
            setattr(self, k, v)


class ContaminationGuard:
    @staticmethod
    def check(source_claim: Any, target_context: Any) -> Any:
        from xendris.core.boundary.evidence_bridge import BoundaryDecision
        return BoundaryDecision(decision="ALLOW", reason="STUB")


__all__ = ["EvidenceBridgeType", "EvidenceBridge", "ContaminationGuard"]
