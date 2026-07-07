"""Contamination risk helpers for acquisition records."""

from __future__ import annotations

from .acquisition_types import ContaminationRisk

FORBIDDEN_TERMS = (
    "xendris",
    "benchmark gate",
    "trust gate",
    "internal gate",
    "response contract",
)


def assess_text_contamination(text: str) -> ContaminationRisk:
    normalized = text.lower()
    if any(term in normalized for term in FORBIDDEN_TERMS):
        return ContaminationRisk.BLOCKED
    return ContaminationRisk.LOW

