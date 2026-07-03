"""
tests/test_baseline_source_support_matrix.py

Tests for the source support matrix builder.
"""

import tempfile
from pathlib import Path

from phyng.baselines.schemas import BaselineSourceSupport
from phyng.baselines.source_support import build_source_support_matrix
from phyng.baselines.readiness import classify_baseline_readiness
from phyng.baselines.visibility_decay import build_visibility_decay_baseline


def test_empty_matrix_when_no_sources():
    with tempfile.TemporaryDirectory() as tmp:
        matrix = build_source_support_matrix(Path(tmp))
        assert matrix == []


def test_background_only_does_not_source_back_baseline():
    """CONTEXT_SUPPORT only → baseline cannot be source-backed."""
    spec_no_src = build_visibility_decay_baseline.__wrapped__(Path(".")) if hasattr(
        build_visibility_decay_baseline, "__wrapped__"
    ) else None

    from phyng.baselines.schemas import VisibilityDecayBaselineSpec
    spec = VisibilityDecayBaselineSpec(
        model_id="TEST-BASE",
        source_ids=[],
    )
    context_only = [
        BaselineSourceSupport(
            source_id="SRC-999",
            support_level="CONTEXT_SUPPORT",
            trust_level="MEDIUM",
        )
    ]
    readiness = classify_baseline_readiness(spec, context_only)
    assert readiness.support_status == "BACKGROUND_SUPPORTED"
    assert readiness.can_be_used_as_baseline is False


def test_contradicting_source_blocks_baseline():
    from phyng.baselines.schemas import VisibilityDecayBaselineSpec
    spec = VisibilityDecayBaselineSpec(model_id="TEST-CONTRA")
    contra = [
        BaselineSourceSupport(
            source_id="SRC-CONTRA",
            support_level="CONTRADICTS",
            trust_level="HIGH",
        )
    ]
    readiness = classify_baseline_readiness(spec, contra)
    assert readiness.support_status == "CONTRADICTED"
    assert readiness.can_be_used_as_baseline is False
    assert readiness.max_claim_level == 0


def test_high_trust_formula_and_observable_support_allows_limited_baseline():
    from phyng.baselines.schemas import VisibilityDecayBaselineSpec
    spec = VisibilityDecayBaselineSpec(
        model_id="TEST-LIMITED",
        assumptions=["Markovian noise"],
    )
    support = [
        BaselineSourceSupport(
            source_id="SRC-F",
            support_level="FORMULA_SUPPORT",
            trust_level="HIGH",
        ),
        BaselineSourceSupport(
            source_id="SRC-O",
            support_level="OBSERVABLE_SUPPORT",
            trust_level="HIGH",
        ),
    ]
    readiness = classify_baseline_readiness(spec, support)
    assert readiness.support_status in {"SOURCE_BACKED_LIMITED", "SOURCE_BACKED_READY"}
    assert readiness.can_be_used_as_baseline is True
    assert readiness.max_claim_level >= 4
