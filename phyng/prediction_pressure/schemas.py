"""
Phygn v1.3/v1.4 — Prediction Pressure Schemas
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field
from phyng.candidates.schemas import CandidatePredictionSpec

GateStatus = Literal[
    "POSITIVE_PREDICTION_NOT_OPERATIONALIZED",
    "POSITIVE_PREDICTION_REQUIRES_EVIDENCE",
    "POSITIVE_PREDICTION_READY_FOR_BENCHMARK"
]

class PositivePredictionGateResult(BaseModel):
    status: GateStatus
    missing_fields: list[str] = Field(default_factory=list)
    message: str

KillPivotStatus = Literal[
    "CONTINUE_PREDICTIVE_TRACK",
    "NEGATIVE_FILTER_ONLY",
    "STRUCTURAL_FRAMEWORK_ONLY",
    "CLAIM_GATING_ARCHITECTURE",
    "NOT_PREDICTIVE_CURRENTLY"
]

class KillPivotResult(BaseModel):
    status: KillPivotStatus
    conclusion: str
    rationale: str
