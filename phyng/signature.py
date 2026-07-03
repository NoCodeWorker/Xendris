"""
Minimal Q/B frontier signature.

Computes:
    Q  = λ_C / L       (quantum weight)
    B  = r_g / L        (gravitational weight)
    QB = (ℓ_P / L)²     (Planck ratio squared — must equal Q·B)

The signature requires a justified operational scale L.
If L is not accepted, the signature is computed but claims are blocked.
"""

from phyng.constants import planck_length, planck_area
from phyng.frontier_lengths import (
    compton_reduced,
    gravitational_radius,
    schwarzschild_radius,
)
from phyng.operational_scale import OperationalScale, review_operational_scale


def frontier_signature(
    m_kg: float,
    scale: OperationalScale,
    qb_tolerance: float = 1e-12,
    gravity_threshold: float = 1e-20,
) -> dict:
    """
    Compute the frontier signature Q/B for a given mass and scale.

    Args:
        m_kg: Mass in kilograms. Must be > 0.
        scale: Justified operational scale.
        qb_tolerance: Maximum relative error for QB consistency check.
        gravity_threshold: If B < this threshold, trace is NEGATIVE_BOUND.

    Returns:
        Dict with Q, B, QB, scale review, trace type, and claim status.
    """
    lambda_c = compton_reduced(m_kg)
    r_g = gravitational_radius(m_kg)
    r_s = schwarzschild_radius(m_kg)
    lp = planck_length()

    L = scale.L_value_m
    Q = lambda_c / L
    B = r_g / L
    QB = Q * B
    planck_ratio_sq = (lp / L) ** 2
    delta_QB = abs(QB - planck_ratio_sq)

    qb_relative = delta_QB / planck_ratio_sq if planck_ratio_sq > 0 else float("inf")
    qb_valid = qb_relative <= qb_tolerance

    # Review the scale
    scale_review = review_operational_scale(scale)
    scale_status = scale_review["status"]

    # Determine trace type and claim status
    if scale_status != "ACCEPTED":
        claim_status = "BLOCKED_AS_AD_HOC_SCALE"
        trace_type = "STRUCTURAL_TRACE"
        interpretation = (
            "Scale L is not accepted. Signature computed for reference only. "
            "No predictive claims supported."
        )
    elif B < gravity_threshold:
        trace_type = "NEGATIVE_BOUND_TRACE"
        claim_status = "ALLOWED_LIMITED"
        interpretation = (
            f"Gravitational weight B={B:.2e} is below threshold {gravity_threshold:.0e}. "
            "Direct gravitational frontier is negligible at this regime."
        )
    else:
        trace_type = "STRUCTURAL_TRACE"
        claim_status = "ALLOWED_LIMITED"
        interpretation = (
            "Signature computed with accepted scale. "
            "Claims limited to structural consistency."
        )

    return {
        "m_kg": m_kg,
        "L_value_m": L,
        "L_type": scale.L_type,
        "lambda_c_m": lambda_c,
        "r_g_m": r_g,
        "schwarzschild_radius_m": r_s,
        "Q": Q,
        "B": B,
        "QB": QB,
        "planck_ratio_squared": planck_ratio_sq,
        "delta_QB": delta_QB,
        "qb_valid": qb_valid,
        "scale_review_status": scale_status,
        "trace_type": trace_type,
        "claim_status": claim_status,
        "interpretation": interpretation,
    }
