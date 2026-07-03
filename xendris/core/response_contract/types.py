"""Pure response contract types for Xendris.

These types describe response quality and claim posture. They do not perform
model calls, retrieval, rewriting, factual validation, scientific validation,
or deep semantic reasoning. They are representation primitives for conservative
contract checks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ClaimType(str, Enum):
    """Internal posture for an important statement in a response."""

    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    STANDARD_KNOWLEDGE = "STANDARD_KNOWLEDGE"
    INFERENCE = "INFERENCE"
    SPECULATION = "SPECULATION"
    UNVERIFIED = "UNVERIFIED"


class ConfidenceLevel(str, Enum):
    """Calibrated confidence bucket for a response or statement."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class ResponseMode(str, Enum):
    """Intended response style."""

    DIRECT = "DIRECT"
    PRACTICAL = "PRACTICAL"
    RIGOROUS = "RIGOROUS"
    CAUTIONARY = "CAUTIONARY"


class DomainValidity(str, Enum):
    """Declared domain-of-validity posture for a response."""

    GENERAL = "GENERAL"
    DOMAIN_SPECIFIC = "DOMAIN_SPECIFIC"
    ASSUMPTION_BOUND = "ASSUMPTION_BOUND"
    SENSITIVE_DOMAIN = "SENSITIVE_DOMAIN"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ResponseContractAssessment:
    """Immutable result of a pure response-contract assessment.

    The assessment is a contract posture, not a truth judgment. A conservative
    assessment must not pair high confidence with speculative or unverified
    claims, and must not carry explicit overclaim risk.
    """

    claim_type: ClaimType
    confidence_level: ConfidenceLevel
    response_mode: ResponseMode
    domain_validity: DomainValidity
    non_overclaiming: bool
    limits_stated: bool
    uncertainty_marked: bool
    has_overclaim_risk: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)

    def is_conservative(self) -> bool:
        """Return whether this assessment satisfies conservative posture rules."""

        if self.has_overclaim_risk or not self.non_overclaiming:
            return False
        if self.confidence_level == ConfidenceLevel.HIGH and self.claim_type in {
            ClaimType.SPECULATION,
            ClaimType.UNVERIFIED,
        }:
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation without external dependencies."""

        return {
            "claim_type": self.claim_type.value,
            "confidence_level": self.confidence_level.value,
            "response_mode": self.response_mode.value,
            "domain_validity": self.domain_validity.value,
            "non_overclaiming": self.non_overclaiming,
            "limits_stated": self.limits_stated,
            "uncertainty_marked": self.uncertainty_marked,
            "has_overclaim_risk": self.has_overclaim_risk,
            "is_conservative": self.is_conservative(),
            "notes": list(self.notes),
        }
