"""
Tests for phyng.candidates.readiness
"""

from phyng.candidates.schemas import CandidatePredictionSpec
from phyng.candidates.readiness import evaluate_candidate_readiness

def test_default_candidate_passes_not_operationalized_to_requires_evidence():
    # If missing observable
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="",  # missing
        baseline_model="exp(-Gamma * t)",
        candidate_model="exp(-(Gamma+Delta)t)",
        candidate_term="Delta",
        expected_pattern="decay",
        detectability_threshold=0.01,
        parameter_status="PRE_REGISTERED"
    )
    status = evaluate_candidate_readiness(spec, "ADMISSIBLE_NEGATIVE_CONTROL", ["FAIL_NO_BENCHMARK"])
    assert status == "CANDIDATE_NOT_OPERATIONALIZED"

    # If complete but lacks evidence
    spec2 = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma * t)",
        candidate_model="exp(-(Gamma+Delta)t)",
        candidate_term="Delta",
        expected_pattern="decay",
        detectability_threshold=0.01,
        parameter_status="PRE_REGISTERED"
    )
    status2 = evaluate_candidate_readiness(spec2, "ADMISSIBLE_NEGATIVE_CONTROL", ["FAIL_NO_SOURCE_SUPPORT", "FAIL_NO_BENCHMARK"])
    assert status2 == "CANDIDATE_REQUIRES_EVIDENCE"
