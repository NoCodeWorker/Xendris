"""
xendris.core.trust — [EXPERIMENTAL] Trust Kernel.

WARNING: This module is EXPERIMENTAL. The types below are minimal stubs
to satisfy imports from other experimental packages (runtime, router,
fingerprints, representations).
The full implementation lives in the `experimental-trust-layers` branch.
"""

from __future__ import annotations

from enum import Enum


class ClaimType(str, Enum):
    FACTUAL = "FACTUAL"
    INFERRED = "INFERRED"
    CALCULATED = "CALCULATED"
    HYPOTHETICAL = "HYPOTHETICAL"
    USER_PROVIDED = "USER_PROVIDED"
    CODE_STATE = "CODE_STATE"
    POLICY = "POLICY"
    CREATIVE = "CREATIVE"


class ClaimStatus(str, Enum):
    APPROVED = "APPROVED"
    APPROVED_WITH_LIMITATIONS = "APPROVED_WITH_LIMITATIONS"
    BLOCKED = "BLOCKED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


__all__ = ["ClaimType", "ClaimStatus", "RiskLevel"]
