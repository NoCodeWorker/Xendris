"""
Tests for phyng.candidates.admissibility
"""

from phyng.candidates.schemas import CandidatePredictionSpec
from phyng.candidates.admissibility import classify_candidate_admissibility

def test_missing_units_blocks_candidate():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="PRE_REGISTERED",
        # Missing units metadata
        term_units=None,
        alpha_units=None,
        dimensionless_core=None
    )
    status = classify_candidate_admissibility(spec, "B_SUPPRESSED")
    assert status == "BLOCKED_DIMENSIONAL_INCOMPLETE"

def test_free_parameters_underidentified():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="FREE_UNCONSTRAINED",
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B"
    )
    status = classify_candidate_admissibility(spec, "B_SUPPRESSED")
    assert status == "UNDERIDENTIFIED_CANDIDATE"

def test_ad_hoc_threshold_blocked():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="AD_HOC",
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B"
    )
    status = classify_candidate_admissibility(spec, "B_SUPPRESSED")
    assert status == "BLOCKED_AS_AD_HOC_CANDIDATE"

def test_admissible_negative_control():
    spec = CandidatePredictionSpec(
        candidate_id="CAND-FC-B-NEGCTRL-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameter_status="PRE_REGISTERED",
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B"
    )
    status = classify_candidate_admissibility(spec, "B_SUPPRESSED")
    assert status == "ADMISSIBLE_NEGATIVE_CONTROL"
