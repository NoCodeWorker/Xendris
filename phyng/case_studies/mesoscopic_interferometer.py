"""
Case study: Mesoscopic interferometer — negative bound.

Parameters:
    m = 1e-17 kg
    L = 1e-7 m  (L_INT: interferometer branch separation)

Expected results:
    Q  ≈ 3.5e-19
    B  ≈ 7.4e-38
    QB ≈ 2.6e-56

Classification: NEGATIVE_BOUND_TRACE

Allowed interpretation:
    For this mass/scale regime, a direct gravitational frontier
    based on B = r_g/L is negligible.

Forbidden interpretation:
    Phyng predicts new gravitational decoherence.
"""

from phyng.operational_scale import OperationalScale
from phyng.signature import frontier_signature


def mesoscopic_interferometer_case() -> dict:
    """
    Run the mesoscopic interferometer negative-bound case study.

    Uses m = 1e-17 kg with interferometer branch separation L = 1e-7 m.
    Gravitational weight B is negligible → NEGATIVE_BOUND_TRACE.

    Returns:
        Dict with full signature, trace type, and interpretations.
    """
    m_kg = 1e-17
    scale = OperationalScale(
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="interferometer branch separation",
        observer_channel="position/interference measurement",
        justification="direct experimental control scale",
        arbitrariness_risk="LOW",
    )

    sig = frontier_signature(m_kg, scale)

    return {
        "case_id": "MESO-INT-001",
        "m_kg": m_kg,
        "L_value_m": scale.L_value_m,
        "L_type": scale.L_type,
        "Q": sig["Q"],
        "B": sig["B"],
        "QB": sig["QB"],
        "qb_valid": sig["qb_valid"],
        "scale_review_status": sig["scale_review_status"],
        "trace_type": sig["trace_type"],
        "claim_status": sig["claim_status"],
        "allowed_interpretation": (
            "For this regime of mass and scale, a direct gravitational "
            "frontier based on B = rg/L is negligible."
        ),
        "forbidden_interpretation": (
            "Phyng predicts new measurable gravitational decoherence."
        ),
    }
