"""
Phygn v1.9 — Unit economics profile evaluator

Verifies pricing, delivery cost, margins, and CAC relationship.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.business_validation.schemas import UnitEconomicsProfile, UnitEconomicsStatus


class UnitEconomicsGateResult(BaseModel):
    """Result of unit economics financial feasibility gate."""
    economics_status: UnitEconomicsStatus
    margin: float | None = None
    margin_percent: float | None = None
    is_scale_allowed: bool
    notes: list[str] = Field(default_factory=list)


def evaluate_unit_economics(profile: UnitEconomicsProfile) -> UnitEconomicsGateResult:
    """
    Evaluate unit economics parameters and margin health.

    Rules:
      - Unknown if price/delivery cost missing -> UNIT_ECONOMICS_UNKNOWN.
      - margin < 0 -> UNIT_ECONOMICS_NEGATIVE.
      - margin / price < 20% -> UNIT_ECONOMICS_FRAGILE.
      - plausible margin -> UNIT_ECONOMICS_PLAUSIBLE.
      - margin > CAC and repeatable -> UNIT_ECONOMICS_STRONG.
    """
    notes = []

    if profile.price is None or profile.cost_to_deliver is None:
        return UnitEconomicsGateResult(
            economics_status="UNIT_ECONOMICS_UNKNOWN",
            is_scale_allowed=False,
            notes=["Missing price or delivery cost in profile. Economics status remains unknown."]
        )

    margin = profile.price - profile.cost_to_deliver
    margin_percent = margin / profile.price if profile.price > 0 else 0.0

    if margin < 0:
        status: UnitEconomicsStatus = "UNIT_ECONOMICS_NEGATIVE"
        notes.append("Negative margin: cost to deliver exceeds sales price. Scale blocked.")
        is_scale_allowed = False
    elif margin_percent < 0.20:
        status = "UNIT_ECONOMICS_FRAGILE"
        notes.append("Fragile economics: gross margin is below 20%. Delivery or pricing is fragile.")
        is_scale_allowed = False
    else:
        # Check CAC relationship
        if profile.customer_acquisition_cost is not None:
            if margin > profile.customer_acquisition_cost:
                status = "UNIT_ECONOMICS_STRONG"
                notes.append("Strong economics: margin exceeds customer acquisition cost.")
                is_scale_allowed = True
            else:
                status = "UNIT_ECONOMICS_FRAGILE"
                notes.append("Fragile economics: customer acquisition cost (CAC) exceeds customer gross margin.")
                is_scale_allowed = False
        else:
            status = "UNIT_ECONOMICS_PLAUSIBLE"
            notes.append("Plausible economics: positive gross margin (> 20%), but CAC remains unmeasured.")
            is_scale_allowed = True  # Plausible allows limited scale / testing but warns

    return UnitEconomicsGateResult(
        economics_status=status,
        margin=margin,
        margin_percent=margin_percent,
        is_scale_allowed=is_scale_allowed,
        notes=notes
    )
