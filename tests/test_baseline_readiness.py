"""
tests/test_baseline_readiness.py

Tests for classify_baseline_readiness().
"""

from phyng.baselines.readiness import classify_baseline_readiness
from phyng.baselines.schemas import BaselineSourceSupport, VisibilityDecayBaselineSpec


def _spec(assumptions: list[str] | None = None) -> VisibilityDecayBaselineSpec:
    return VisibilityDecayBaselineSpec(
        model_id="TEST-READINESS",
        assumptions=assumptions or [],
        source_ids=[],
    )


def test_baseline_without_sources_requires_source():
    readiness = classify_baseline_readiness(_spec(), [])
    assert readiness.support_status == "BASELINE_REQUIRES_SOURCE"
    assert readiness.can_be_used_as_baseline is False
    assert readiness.max_claim_level == 3


def test_background_only_not_source_backed():
    matrix = [
        BaselineSourceSupport(source_id="S1", support_level="CONTEXT_SUPPORT", trust_level="MEDIUM")
    ]
    readiness = classify_baseline_readiness(_spec(), matrix)
    assert readiness.support_status == "BACKGROUND_SUPPORTED"
    assert readiness.can_be_used_as_baseline is False


def test_formula_support_without_observable_not_ready():
    matrix = [
        BaselineSourceSupport(source_id="S1", support_level="FORMULA_SUPPORT", trust_level="HIGH")
    ]
    readiness = classify_baseline_readiness(_spec(["Markovian noise"]), matrix)
    # Formula without observable → SOURCE_BACKED_LIMITED but still not READY
    assert readiness.support_status == "SOURCE_BACKED_LIMITED"
    assert readiness.max_claim_level == 4


def test_source_backed_formula_allows_limited_baseline():
    matrix = [
        BaselineSourceSupport(source_id="S1", support_level="FORMULA_SUPPORT", trust_level="HIGH"),
        BaselineSourceSupport(source_id="S2", support_level="OBSERVABLE_SUPPORT", trust_level="HIGH"),
    ]
    readiness = classify_baseline_readiness(_spec(["Markovian noise"]), matrix)
    assert readiness.can_be_used_as_baseline is True
    assert readiness.support_status in {"SOURCE_BACKED_LIMITED", "SOURCE_BACKED_READY"}


def test_missing_assumptions_blocks_ready_status():
    matrix = [
        BaselineSourceSupport(source_id="S1", support_level="FORMULA_SUPPORT", trust_level="HIGH"),
        BaselineSourceSupport(source_id="S2", support_level="OBSERVABLE_SUPPORT", trust_level="HIGH"),
        BaselineSourceSupport(source_id="S3", support_level="PARAMETER_SUPPORT", trust_level="HIGH"),
    ]
    # No assumptions → cannot reach READY
    readiness = classify_baseline_readiness(_spec(assumptions=[]), matrix)
    assert readiness.support_status != "SOURCE_BACKED_READY"


def test_candidate_prediction_always_blocked():
    """Regardless of baseline readiness, candidate physical prediction must stay blocked."""
    matrix = [
        BaselineSourceSupport(source_id="S1", support_level="FORMULA_SUPPORT", trust_level="PRIMARY"),
        BaselineSourceSupport(source_id="S2", support_level="OBSERVABLE_SUPPORT", trust_level="HIGH"),
        BaselineSourceSupport(source_id="S3", support_level="PARAMETER_SUPPORT", trust_level="HIGH"),
    ]
    spec = _spec(assumptions=["Markovian noise", "single channel"])
    readiness = classify_baseline_readiness(spec, matrix)
    blocked_text = " ".join(readiness.blocked_claims).lower()
    assert "predicts" in blocked_text or "validates" in blocked_text or "boundary" in blocked_text
