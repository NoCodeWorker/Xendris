"""
Tests for operational scale review.
"""

from phyng.operational_scale import OperationalScale, review_operational_scale


def _make_scale(**overrides) -> OperationalScale:
    """Helper to create a valid scale with overrides."""
    defaults = {
        "L_value_m": 1e-7,
        "L_type": "L_INT",
        "physical_role": "interferometer branch separation",
        "observer_channel": "position/interference measurement",
        "justification": "direct experimental control scale",
        "arbitrariness_risk": "LOW",
    }
    defaults.update(overrides)
    return OperationalScale(**defaults)


def test_operational_scale_rejects_empty_justification():
    scale = _make_scale(justification="")
    result = review_operational_scale(scale)
    assert result["status"] == "REJECTED"
    assert result["can_support_predictive_claims"] is False


def test_operational_scale_rejects_whitespace_justification():
    scale = _make_scale(justification="   ")
    result = review_operational_scale(scale)
    assert result["status"] == "REJECTED"


def test_operational_scale_rejects_empty_physical_role():
    scale = _make_scale(physical_role="")
    result = review_operational_scale(scale)
    assert result["status"] == "REJECTED"
    assert result["can_support_predictive_claims"] is False


def test_operational_scale_rejects_empty_observer_channel():
    scale = _make_scale(observer_channel="")
    result = review_operational_scale(scale)
    assert result["status"] == "REJECTED"


def test_operational_scale_requires_justification_when_high_risk():
    scale = _make_scale(arbitrariness_risk="HIGH")
    result = review_operational_scale(scale)
    assert result["status"] == "REQUIRES_JUSTIFICATION"
    assert result["can_support_predictive_claims"] is False


def test_operational_scale_accepts_valid_scale():
    scale = _make_scale()
    result = review_operational_scale(scale)
    assert result["status"] == "ACCEPTED"
    assert result["can_support_predictive_claims"] is True


def test_operational_scale_rejects_out_of_range():
    scale = _make_scale(
        L_value_m=1.0,  # way outside allowed range
        allowed_range_m=(1e-9, 1e-3),
    )
    result = review_operational_scale(scale)
    assert result["status"] == "REJECTED"


def test_operational_scale_accepts_within_range():
    scale = _make_scale(allowed_range_m=(1e-9, 1e-3))
    result = review_operational_scale(scale)
    assert result["status"] == "ACCEPTED"
