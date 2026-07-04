"""Equivalence and comparison definitions for ClaimRepresentations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from xendris.core.trust.types import RiskLevel


class RepresentationRelation(str, Enum):
    """Logical relations between multiple claim representations."""

    EQUIVALENT = "EQUIVALENT"
    PARTIALLY_EQUIVALENT = "PARTIALLY_EQUIVALENT"
    CONTRADICTORY = "CONTRADICTORY"
    DISJOINT = "DISJOINT"
    OVERGENERALIZED = "OVERGENERALIZED"
    UNDERSPECIFIED = "UNDERSPECIFIED"
    EVIDENCE_MISMATCH = "EVIDENCE_MISMATCH"
    REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"


@dataclass(frozen=True)
class RepresentationComparison:
    """An immutable record of comparing two representations of a claim."""

    left_representation_id: str
    right_representation_id: str
    relation: RepresentationRelation
    reason: str
    shared_claim_id: str
    shared_terms: tuple[str, ...] = ()
    conflict_terms: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.LOW
