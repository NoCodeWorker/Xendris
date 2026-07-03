"""
Tests for phyng.prediction_pressure.kill_criteria
"""

from phyng.prediction_pressure.kill_criteria import evaluate_kill_or_pivot

def test_kill_criteria_negative_only_not_predictive():
    # negative_bounds_only=True, no detectable candidate, no structural/blocking use
    res = evaluate_kill_or_pivot(
        has_detectable_candidate=False,
        has_benchmark_gain=False,
        negative_bounds_only=True,
        claim_blocking_useful=False,
        structural_atlas_useful=False
    )
    assert res.status == "NOT_PREDICTIVE_CURRENTLY"
    assert "not a predictive physical theory" in res.conclusion

def test_kill_criteria_claim_gating():
    # negative_bounds_only=True, no detectable candidate, but blocking is useful
    res = evaluate_kill_or_pivot(
        has_detectable_candidate=False,
        has_benchmark_gain=False,
        negative_bounds_only=True,
        claim_blocking_useful=True,
        structural_atlas_useful=True
    )
    assert res.status == "CLAIM_GATING_ARCHITECTURE"

def test_kill_criteria_structural_framework():
    # negative_bounds_only=True, no detectable candidate, blocking not useful, structural atlas useful
    res = evaluate_kill_or_pivot(
        has_detectable_candidate=False,
        has_benchmark_gain=False,
        negative_bounds_only=True,
        claim_blocking_useful=False,
        structural_atlas_useful=True
    )
    assert res.status == "STRUCTURAL_FRAMEWORK_ONLY"

def test_kill_criteria_detectable_candidate_continues():
    res = evaluate_kill_or_pivot(
        has_detectable_candidate=True,
        has_benchmark_gain=False,
        negative_bounds_only=False,
        claim_blocking_useful=False,
        structural_atlas_useful=False
    )
    assert res.status == "CONTINUE_PREDICTIVE_TRACK"
