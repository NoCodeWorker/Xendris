"""PresentationBoundary for Xendris Epistemic Frame Layer.

Distinguishes between what a model output *presents* (interface utility)
and what it *asserts* (cognitive certainty). A useful presentation is not
the same as a verified claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class PresentationBoundaryDecision(Enum):
    CLEAR_BOUNDARY = "CLEAR_BOUNDARY"
    BOUNDARY_VIOLATION = "BOUNDARY_VIOLATION"
    UNCLEAR = "UNCLEAR"


@dataclass(frozen=True)
class PresentationBoundaryVerdict:
    decision: PresentationBoundaryDecision
    reason: str
    violations: tuple[str, ...] = ()


_INTERFACE_INDICATORS = {
    "demonstration", "example", "illustration", "visualization",
    "interface", "widget", "component", "layout", "format",
    "diagram", "table", "chart", "figure", "screenshot",
    "demo", "preview", "overview", "summary", "template",
}

_ASSERTION_INDICATORS = {
    "proves", "confirms", "guarantees", "establishes", "demonstrates that",
    "therefore", "conclusively", "undoubtedly", "certainly", "absolutely",
    "siempre", "nunca", "garantiza", "demuestra que", "concluyentemente",
    "prueba", "confirmación definitiva", "sin duda",
}

_FALSE_BRIDGE_PATTERNS = [
    ("interface_as_proof", "demostración", "prueba"),
    ("interface_as_proof", "demo", "proof"),
    ("interface_as_certainty", "interfaz", "garantiza"),
    ("interface_as_certainty", "ui", "guarantees"),
    ("presentation_as_validation", "visualization", "validates"),
    ("presentation_as_validation", "ejemplo", "confirma"),
]


def evaluate_presentation_boundary(
    output_text: str,
    metadata: Mapping[str, Any] | None = None,
) -> PresentationBoundaryVerdict:
    """Evaluate whether the output respects the presentation boundary.

    Checks if interface/demonstration language is conflated with
    certainty/assertion language.
    """
    text_lower = output_text.lower()

    interface_count = sum(1 for word in _INTERFACE_INDICATORS if word in text_lower)
    assertion_count = sum(1 for word in _ASSERTION_INDICATORS if word in text_lower)

    violations = []
    for category, term1, term2 in _FALSE_BRIDGE_PATTERNS:
        if term1 in text_lower and term2 in text_lower:
            violations.append(
                f"False bridge detected ({category}): '{term1}' paired with '{term2}' "
                f"suggests interface utility equals cognitive certainty."
            )

    if violations:
        return PresentationBoundaryVerdict(
            decision=PresentationBoundaryDecision.BOUNDARY_VIOLATION,
            reason=f"Presentation boundary violated: {len(violations)} false bridge(s) detected.",
            violations=tuple(violations),
        )

    if assertion_count > interface_count * 2 and assertion_count > 2:
        return PresentationBoundaryVerdict(
            decision=PresentationBoundaryDecision.UNCLEAR,
            reason=f"Assertion language ({assertion_count}) dominates interface language ({interface_count}). "
                   "The output may be conflating presented content with asserted certainty.",
        )

    return PresentationBoundaryVerdict(
        decision=PresentationBoundaryDecision.CLEAR_BOUNDARY,
        reason="Presentation boundary respected. Interface utility is not conflated with cognitive certainty.",
    )
