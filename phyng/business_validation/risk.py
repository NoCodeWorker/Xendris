"""
Phygn v1.9 — Business risk gate evaluator

Classifies legal, regulatory, reputational, or financial risks.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.business_validation.schemas import BusinessRiskAssessment, BusinessRiskStatus


class BusinessRiskGateResult(BaseModel):
    """Result of risk evaluation gate."""
    risk_status: BusinessRiskStatus
    is_blocking: bool
    notes: list[str] = Field(default_factory=list)


def evaluate_business_risk(assessment: BusinessRiskAssessment) -> BusinessRiskGateResult:
    """
    Evaluate identified business risks.
    If any risk value is 'BLOCKING' or 'RISK_BLOCKING', status becomes RISK_BLOCKING.
    """
    notes = []
    is_blocking = False
    status: BusinessRiskStatus = "RISK_UNASSESSED"

    if not assessment.risks:
        notes.append("No risks have been assessed yet. Risk status remains unassessed.")
        return BusinessRiskGateResult(
            risk_status="RISK_UNASSESSED",
            is_blocking=False,
            notes=notes
        )

    # Classify overall status
    risk_values = set(assessment.risks.values())

    if "RISK_BLOCKING" in risk_values or "BLOCKING" in risk_values:
        status = "RISK_BLOCKING"
        is_blocking = True
        notes.append("Blocking risk identified! Regulatory or operational constraints block scaling.")
    elif "RISK_HIGH_REQUIRES_REVIEW" in risk_values or "HIGH" in risk_values:
        status = "RISK_HIGH_REQUIRES_REVIEW"
        notes.append("High risk identified. Action requires expert compliance review.")
    elif "RISK_MEDIUM" in risk_values or "MEDIUM" in risk_values:
        status = "RISK_MEDIUM"
        notes.append("Medium risks logged. Ongoing monitoring required.")
    else:
        status = "RISK_LOW"
        notes.append("All logged risks are low.")

    return BusinessRiskGateResult(
        risk_status=status,
        is_blocking=is_blocking,
        notes=notes
    )
