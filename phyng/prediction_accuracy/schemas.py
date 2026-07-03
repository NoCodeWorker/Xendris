"""
Phygn v1.7 — Prediction Accuracy: Schemas

PredictionRecord, PredictionOutcome, PredictionMetrics,
CalibrationReport, FilterLiftReport — all defined here.
"""

from __future__ import annotations

import uuid
from pydantic import BaseModel, Field


class PredictionRecord(BaseModel):
    """A logged prediction before resolution."""
    prediction_id: str = Field(default_factory=lambda: f"PRED-{uuid.uuid4().hex[:8].upper()}")
    hypothesis_id: str | None = None
    claim_id: str | None = None
    mode: str = "HYPOTHESIS_MODE"
    ladder_level: str = "HYPOTHESIS_SEED"
    domain: str = "general"
    prediction_text: str
    target_variable: str
    predicted_direction: str | None = None     # "UP", "DOWN", "NEUTRAL"
    predicted_value: float | None = None
    predicted_probability: float | None = None  # 0.0–1.0
    time_horizon: str = "unspecified"
    baseline_reference: str | None = None
    evidence_level: str = "HYPOTHESIS_SEED"
    gate_status: str = "HYPOTHESIS_SEED"
    confidence_score: float | None = None
    created_at: str = ""
    resolution_due_at: str | None = None


class PredictionOutcome(BaseModel):
    """Actual outcome after a prediction resolves."""
    prediction_id: str
    resolved: bool = False
    actual_value: float | None = None
    actual_direction: str | None = None
    success: bool | None = None             # True if prediction was correct
    error_value: float | None = None        # |predicted - actual|
    benchmark_value: float | None = None
    benchmark_success: bool | None = None
    resolved_at: str | None = None
    notes: str | None = None


class PredictionMetrics(BaseModel):
    """Computed accuracy and calibration metrics over a set of predictions."""
    n_total: int = 0
    n_resolved: int = 0
    n_correct: int = 0
    n_incorrect: int = 0
    hit_rate: float | None = None           # n_correct / n_resolved
    base_rate: float | None = None          # prior/baseline correct rate
    accuracy_lift: float | None = None      # hit_rate - base_rate
    precision: float | None = None
    recall: float | None = None
    false_positive_rate: float | None = None
    false_negative_rate: float | None = None
    brier_score: float | None = None        # mean((p - outcome)^2), lower = better
    mean_absolute_error: float | None = None
    expected_calibration_error: float | None = None
    benchmark_relative_error: float | None = None
    overconfidence_index: float | None = None


class CalibrationReport(BaseModel):
    """Calibration analysis of probabilistic predictions."""
    n_predictions_with_probability: int = 0
    brier_score: float | None = None
    expected_calibration_error: float | None = None
    calibration_status: str = "INSUFFICIENT_DATA"
    # "WELL_CALIBRATED", "OVERCONFIDENT_GATE", "UNDERCONFIDENT_GATE", "INSUFFICIENT_DATA"
    calibration_bins: list[dict] = Field(default_factory=list)
    # Each bin: {"bin_low": 0.0, "bin_high": 0.2, "n": 5, "mean_p": 0.1, "actual_rate": 0.12}
    notes: list[str] = Field(default_factory=list)


class FilterLiftReport(BaseModel):
    """Report on whether Phygn filters improve prediction accuracy."""
    n_passed: int = 0
    n_not_passed: int = 0
    accuracy_given_pass: float | None = None
    accuracy_given_low_level: float | None = None
    base_rate: float | None = None
    lift_over_baseline: float | None = None
    filter_status: str = "INSUFFICIENT_OUTCOMES"
    # "FILTER_SHOWS_PREDICTIVE_LIFT", "FILTER_NOT_PREDICTIVELY_USEFUL_YET",
    # "INSUFFICIENT_OUTCOMES", "LADDER_NOT_PREDICTIVELY_ORDERED"
    ladder_accuracy_by_level: dict[str, float] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)
