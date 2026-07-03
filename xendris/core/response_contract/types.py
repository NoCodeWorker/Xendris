"""Pure enum types for the Xendris Response Contract v0.2.0.

These enums are representation primitives. They do not perform model calls,
retrieval, response rewriting, factual validation, scientific validation, or
deep semantic reasoning.
"""

from __future__ import annotations

from enum import Enum


class ClaimType(str, Enum):
    """Conservative posture for an important statement in a response."""

    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    STANDARD_KNOWLEDGE = "STANDARD_KNOWLEDGE"
    INFERENCE = "INFERENCE"
    SPECULATION = "SPECULATION"
    UNVERIFIED = "UNVERIFIED"


class ConfidenceLevel(str, Enum):
    """Calibrated confidence bucket for a claim or response posture."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CALIBRATED = "CALIBRATED"
    UNKNOWN = "UNKNOWN"


class ResponseMode(str, Enum):
    """Intended response mode."""

    FAST = "FAST"
    STANDARD = "STANDARD"
    RIGOROUS = "RIGOROUS"
    AUDIT = "AUDIT"


class DomainValidity(str, Enum):
    """Declared domain-of-validity posture."""

    GENERAL = "GENERAL"
    LOCAL = "LOCAL"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"
    EXPERIMENTAL = "EXPERIMENTAL"
    UNKNOWN = "UNKNOWN"
