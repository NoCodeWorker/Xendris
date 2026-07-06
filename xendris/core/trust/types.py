"""Core enum types for the Xendris Trust Kernel.

These types are deterministic representation primitives. They do not call
models, retrieve sources, or validate factual truth.
"""

from __future__ import annotations

from enum import Enum


class ClaimType(str, Enum):
    """Structural category for an auditable claim."""

    FACTUAL = "FACTUAL"
    INFERRED = "INFERRED"
    CALCULATED = "CALCULATED"
    CODE_STATE = "CODE_STATE"
    USER_PROVIDED = "USER_PROVIDED"
    USER_PROVIDED_FACT = "USER_PROVIDED_FACT"
    USER_PROVIDED_RULE = "USER_PROVIDED_RULE"
    USER_PROVIDED_POLICY = "USER_PROVIDED_POLICY"
    USER_PROVIDED_CLAIM = "USER_PROVIDED_CLAIM"
    USER_PROVIDED_EVIDENCE_REFERENCE = "USER_PROVIDED_EVIDENCE_REFERENCE"
    POLICY = "POLICY"
    UNSUPPORTED = "UNSUPPORTED"


class ClaimStatus(str, Enum):
    """Support status assigned to an auditable claim."""

    VERIFIED = "VERIFIED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


class RiskLevel(str, Enum):
    """Global structural risk for an audited answer."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AuditDecision(str, Enum):
    """Decision produced by the deterministic trust kernel."""

    APPROVED = "APPROVED"
    APPROVED_WITH_LIMITATIONS = "APPROVED_WITH_LIMITATIONS"
    BLOCKED = "BLOCKED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
