"""
xendris.core.boundary.evidence_bridge — [EXPERIMENTAL] Evidence bridge types.

WARNING: This module is EXPERIMENTAL. Minimal stubs for import compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from xendris.core.boundary import EvidenceBridge, EvidenceBridgeType  # noqa: F401


@dataclass
class BoundaryDecision:
    decision: str = "ALLOW"
    reason: str = "STUB"
    allowed: bool = True
    source_context: Any = None
    target_context: Any = None
    requested_target_claim_type: Any = None
    required_evidence: tuple = field(default_factory=tuple)
    limitations: tuple = field(default_factory=tuple)
    audit_tags: tuple = field(default_factory=tuple)
    risk_level: str = "LOW"


__all__ = ["EvidenceBridge", "EvidenceBridgeType", "BoundaryDecision"]
