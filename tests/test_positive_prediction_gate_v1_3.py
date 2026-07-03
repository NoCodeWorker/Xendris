"""
Tests for phyng.prediction_pressure.positive_gate
"""

from phyng.prediction_pressure import CandidatePredictionSpec, evaluate_positive_prediction_gate

def test_positive_gate_missing_fields_blocks():
    # Missing candidate_model and candidate_term
    spec = CandidatePredictionSpec(
        observable="visibility",
        baseline_model="exp(-Gamma t)",
        parameters=["Gamma"]
    )
    res = evaluate_positive_prediction_gate(spec)
    assert res.status == "POSITIVE_PREDICTION_NOT_OPERATIONALIZED"
    assert "candidate_model" in res.missing_fields
    assert "candidate_term" in res.missing_fields

def test_positive_gate_complete_requires_evidence():
    # All fields present, but no source support or benchmark
    spec = CandidatePredictionSpec(
        observable="visibility",
        baseline_model="exp(-Gamma t)",
        candidate_model="exp(-(Gamma+Delta)t)",
        candidate_term="Delta = Q*B/L",
        parameters=["Q", "B", "L"],
        data_target="Talbot-Lau",
        error_metric="RMSE",
        expected_pattern="Delta > 0",
        detectability_threshold=0.01,
        failure_condition="Gain <= 0",
        has_source_support=False,
        has_benchmark=False
    )
    res = evaluate_positive_prediction_gate(spec)
    assert res.status == "POSITIVE_PREDICTION_REQUIRES_EVIDENCE"

def test_positive_gate_ready_for_benchmark():
    # All fields + evidence + benchmark
    spec = CandidatePredictionSpec(
        observable="visibility",
        baseline_model="exp(-Gamma t)",
        candidate_model="exp(-(Gamma+Delta)t)",
        candidate_term="Delta = Q*B/L",
        parameters=["Q", "B", "L"],
        data_target="Talbot-Lau",
        error_metric="RMSE",
        expected_pattern="Delta > 0",
        detectability_threshold=0.01,
        failure_condition="Gain <= 0",
        has_source_support=True,
        has_benchmark=True
    )
    res = evaluate_positive_prediction_gate(spec)
    assert res.status == "POSITIVE_PREDICTION_READY_FOR_BENCHMARK"
