"""Council data models: escalation reasons, guard results, council decisions."""
from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class GuardResult(str, Enum):
    PASS = "PASS"
    FLAG = "FLAG"
    BLOCK = "BLOCK"


class EscalationReason(str, Enum):
    SYCOPHANCY_DETECTED = "SYCOPHANCY_DETECTED"
    STRONG_CONTRADICTION = "STRONG_CONTRADICTION"
    HIGH_RISK_CLAIM = "HIGH_RISK_CLAIM"
    INSUFFICIENT_EVIDENCE_HIGH_IMPACT = "INSUFFICIENT_EVIDENCE_HIGH_IMPACT"
    HIGH_IMPACT_SYCOPHANCY = "HIGH_IMPACT_SYCOPHANCY"
    IRREVERSIBLE_ACTION = "IRREVERSIBLE_ACTION"
    MODEL_CONFLICT = "MODEL_CONFLICT"
    USER_REQUESTED = "USER_REQUESTED"
    BUDGET_ALLOWS = "BUDGET_ALLOWS"


class GuardOutput(BaseModel):
    guard_name: str
    result: GuardResult
    reason: str = ""
    details: dict[str, Any] = Field(default_factory=dict)


class CouncilDecision(BaseModel):
    requires_council: bool = False
    escalation_reason: EscalationReason | None = None
    guard_results: list[GuardOutput] = Field(default_factory=list)
    selected_models: list[str] = Field(default_factory=list)
    marginal_certainty_gain: Decimal = Field(default=Decimal("0.00"))
    tokens_used: int = 0
    cost: Decimal = Field(default=Decimal("0.00"))
    tokens_avoided: int = 0
    cost_saved: Decimal = Field(default=Decimal("0.00"))
    verdict: str = "SINGLE_MODEL_OK"
