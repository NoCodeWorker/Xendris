"""
Tests for Q/B frontier signature.
"""

import math

from phyng.constants import planck_length
from phyng.operational_scale import OperationalScale
from phyng.signature import frontier_signature


def _justified_scale(L_value_m: float = 1e-7) -> OperationalScale:
    return OperationalScale(
        L_value_m=L_value_m,
        L_type="L_INT",
        physical_role="interferometer branch separation",
        observer_channel="position/interference measurement",
        justification="direct experimental control scale",
        arbitrariness_risk="LOW",
    )


def _ad_hoc_scale(L_value_m: float = 1e-7) -> OperationalScale:
    return OperationalScale(
        L_value_m=L_value_m,
        L_type="L_INT",
        physical_role="",
        observer_channel="position measurement",
        justification="no reason",
        arbitrariness_risk="LOW",
    )


def test_QB_constraint():
    """Q·B must equal (ℓ_P/L)² within tolerance."""
    m = 1e-17
    scale = _justified_scale()
    sig = frontier_signature(m, scale)

    assert sig["qb_valid"] is True
    assert math.isclose(sig["QB"], sig["planck_ratio_squared"], rel_tol=1e-12)


def test_signature_blocks_ad_hoc_L():
    """Signature with unjustified L → BLOCKED_AS_AD_HOC_SCALE."""
    m = 1e-17
    scale = _ad_hoc_scale()
    sig = frontier_signature(m, scale)

    assert sig["scale_review_status"] == "REJECTED"
    assert sig["claim_status"] == "BLOCKED_AS_AD_HOC_SCALE"


def test_signature_accepts_justified_L():
    """Signature with justified L → ACCEPTED, not blocked."""
    m = 1e-17
    scale = _justified_scale()
    sig = frontier_signature(m, scale)

    assert sig["scale_review_status"] == "ACCEPTED"
    assert sig["claim_status"] != "BLOCKED_AS_AD_HOC_SCALE"


def test_signature_Q_B_values():
    """Check Q and B orders of magnitude for mesoscopic regime."""
    m = 1e-17
    scale = _justified_scale(1e-7)
    sig = frontier_signature(m, scale)

    # Q = λ_C / L ≈ 3.5e-19
    assert 1e-20 < sig["Q"] < 1e-17
    # B = r_g / L ≈ 7.4e-38
    assert 1e-39 < sig["B"] < 1e-36


def test_mesoscopic_negative_bound():
    """Mesoscopic regime with tiny B → NEGATIVE_BOUND_TRACE."""
    m = 1e-17
    scale = _justified_scale(1e-7)
    sig = frontier_signature(m, scale)

    assert sig["trace_type"] == "NEGATIVE_BOUND_TRACE"
    assert sig["B"] < 1e-20
