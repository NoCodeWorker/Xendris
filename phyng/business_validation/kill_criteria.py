"""
Phygn v1.9 — Kill criteria gate evaluator

Verifies that the validation attempt defines clear failure thresholds to prevent burning capital.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.business_validation.schemas import KillCriteria


class KillCriteriaGateResult(BaseModel):
    """Result of verifying kill criteria completeness."""
    is_valid: bool
    notes: list[str] = Field(default_factory=list)


def evaluate_kill_criteria(criteria: KillCriteria | None) -> KillCriteriaGateResult:
    """
    Ensure kill criteria exists and defines a failure threshold.
    """
    notes = []

    if criteria is None:
        notes.append("No kill criteria defined. Scaling is blocked. You must define failure conditions.")
        return KillCriteriaGateResult(is_valid=False, notes=notes)

    # Verify that failure conditions are present
    if not criteria.kill_trigger or not criteria.pivot_trigger:
        notes.append("Kill or pivot triggers are empty.")
        return KillCriteriaGateResult(is_valid=False, notes=notes)

    if not criteria.has_failure_threshold:
        notes.append("No explicit failure threshold defined. Scale blocked.")
        return KillCriteriaGateResult(is_valid=False, notes=notes)

    notes.append("Kill criteria defined with explicit failure thresholds.")
    return KillCriteriaGateResult(is_valid=True, notes=notes)
