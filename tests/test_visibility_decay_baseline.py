"""
tests/test_visibility_decay_baseline.py

Tests for the V_base(t) = exp(-Gamma * t) baseline model.
"""

import math
import tempfile
from pathlib import Path

from phyng.baselines.visibility_decay import (
    build_visibility_decay_baseline,
    compute_visibility,
    compute_visibility_series,
)


def test_visibility_at_t_zero_is_one():
    assert math.isclose(compute_visibility(0.1, 0.0), 1.0)


def test_visibility_decays_over_time():
    v0 = compute_visibility(0.5, 0.0)
    v1 = compute_visibility(0.5, 1.0)
    assert v0 > v1 > 0.0


def test_visibility_series_length():
    times = [0.0, 1.0, 2.0, 5.0]
    series = compute_visibility_series(0.1, times)
    assert len(series) == len(times)


def test_baseline_without_sources_is_toy_internal():
    with tempfile.TemporaryDirectory() as tmp:
        spec = build_visibility_decay_baseline(Path(tmp))
        assert spec.support_status == "TOY_INTERNAL"
        assert spec.parameter_status == "PARAMETER_TOY"
        assert spec.gamma_value is None


def test_arbitrary_gamma_is_parameter_toy():
    with tempfile.TemporaryDirectory() as tmp:
        spec = build_visibility_decay_baseline(Path(tmp))
        assert spec.parameter_status == "PARAMETER_TOY"


def test_baseline_formula_string():
    with tempfile.TemporaryDirectory() as tmp:
        spec = build_visibility_decay_baseline(Path(tmp))
        assert "exp" in spec.formula.lower() or "Gamma" in spec.formula


def test_baseline_forbidden_uses_include_prediction():
    with tempfile.TemporaryDirectory() as tmp:
        spec = build_visibility_decay_baseline(Path(tmp))
        forbidden_text = " ".join(spec.forbidden_uses).lower()
        assert "prediction" in forbidden_text or "experimental" in forbidden_text
