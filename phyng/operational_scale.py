"""
Operational scale L selection and review.

Fundamental rule:
    If L is not accepted, the Q/B signature can be computed
    but CANNOT support predictive claims.

Every scale must be justified — no free parameters.
"""

from typing import Literal

from pydantic import BaseModel, Field


class OperationalScale(BaseModel):
    """
    Typed operational scale for Frontera C calculations.

    L must have a physical role, an observer channel, and a justification.
    Without these, no predictive claim can be supported.
    """

    L_value_m: float = Field(gt=0, description="Scale value in meters")
    L_type: Literal[
        "L_SYS",
        "L_DET",
        "L_INT",
        "L_COH",
        "L_WAVELENGTH",
        "L_CURV",
        "L_HORIZON",
        "L_BOX",
        "L_CHANNEL",
    ]
    physical_role: str
    observer_channel: str
    justification: str
    allowed_range_m: tuple[float, float] | None = None
    arbitrariness_risk: Literal["LOW", "MEDIUM", "HIGH"]


def review_operational_scale(scale: OperationalScale) -> dict:
    """
    Review an operational scale for acceptability.

    Rules:
        - Empty justification → REJECTED
        - Empty physical_role → REJECTED
        - Empty observer_channel → REJECTED
        - HIGH arbitrariness_risk → REQUIRES_JUSTIFICATION
        - L_value_m outside allowed_range_m → REJECTED
        - Otherwise → ACCEPTED

    Args:
        scale: The operational scale to review.

    Returns:
        Dict with status, reason, and whether the scale can
        support predictive claims.
    """
    if not scale.justification.strip():
        return {
            "status": "REJECTED",
            "reason": "Justification is empty",
            "can_support_predictive_claims": False,
        }

    if not scale.physical_role.strip():
        return {
            "status": "REJECTED",
            "reason": "Physical role is empty",
            "can_support_predictive_claims": False,
        }

    if not scale.observer_channel.strip():
        return {
            "status": "REJECTED",
            "reason": "Observer channel is empty",
            "can_support_predictive_claims": False,
        }

    if scale.allowed_range_m is not None:
        lo, hi = scale.allowed_range_m
        if not (lo <= scale.L_value_m <= hi):
            return {
                "status": "REJECTED",
                "reason": (
                    f"L_value_m={scale.L_value_m} is outside allowed range "
                    f"[{lo}, {hi}]"
                ),
                "can_support_predictive_claims": False,
            }

    if scale.arbitrariness_risk == "HIGH":
        return {
            "status": "REQUIRES_JUSTIFICATION",
            "reason": "Arbitrariness risk is HIGH — additional justification required",
            "can_support_predictive_claims": False,
        }

    return {
        "status": "ACCEPTED",
        "reason": "Scale is justified and within bounds",
        "can_support_predictive_claims": True,
    }
