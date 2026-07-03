"""
Phygn v1.3 — Positive Prediction Gate

Evaluates whether a candidate model has operationalized its positive prediction.
"""

from __future__ import annotations

from phyng.prediction_pressure.schemas import CandidatePredictionSpec, PositivePredictionGateResult

REQUIRED_FIELDS = [
    "observable",
    "baseline_model",
    "candidate_model",
    "candidate_term",
    "parameters",
    "data_target",
    "error_metric",
    "expected_pattern",
    "detectability_threshold",
    "failure_condition",
]

def evaluate_positive_prediction_gate(
    candidate: CandidatePredictionSpec
) -> PositivePredictionGateResult:
    """
    Evaluates the positive prediction gate for a candidate model.
    """
    missing_fields = []
    
    for field in REQUIRED_FIELDS:
        val = getattr(candidate, field)
        if val is None or val == "" or (isinstance(val, list) and not val):
            missing_fields.append(field)
            
    if missing_fields:
        return PositivePredictionGateResult(
            status="POSITIVE_PREDICTION_NOT_OPERATIONALIZED",
            missing_fields=sorted(missing_fields),
            message=f"Missing operationalization fields: {', '.join(missing_fields)}"
        )
        
    if not candidate.has_source_support or not candidate.has_benchmark:
        return PositivePredictionGateResult(
            status="POSITIVE_PREDICTION_REQUIRES_EVIDENCE",
            message="Model is operationalized but lacks verified source support or benchmark implementation."
        )
        
    return PositivePredictionGateResult(
        status="POSITIVE_PREDICTION_READY_FOR_BENCHMARK",
        message="Model has positive prediction operationalized and is ready for benchmark evaluation."
    )
