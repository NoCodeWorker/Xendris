"""Representations package for the Xendris Algebraic Trust layer."""

from __future__ import annotations

from .representation import ClaimRepresentation
from .equivalence import RepresentationRelation, RepresentationComparison
from .consistency_gate import RepresentationConsistencyDecision, RepresentationConsistencyGate
from .contradiction import compare_representations
from .representation_audit import RepresentationAudit

__all__ = [
    "ClaimRepresentation",
    "RepresentationRelation",
    "RepresentationComparison",
    "RepresentationConsistencyDecision",
    "RepresentationConsistencyGate",
    "compare_representations",
    "RepresentationAudit",
]
