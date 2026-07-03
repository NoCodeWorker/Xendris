"""
Frontier lengths and structural lemma validation.

Implements:
    - Reduced Compton wavelength:  λ_C = ħ / (m c)
    - Gravitational radius:        r_g = G m / c²
    - Schwarzschild radius:        R_S = 2 G m / c²
    - Structural lemma:            λ_C · r_g = ℓ_P²

The lemma λ_C · r_g = ℓ_P² is classified as STRUCTURAL_LEMMA.
It is NOT a hypothesis, NOT proof of new physics.
"""

from phyng.constants import C, HBAR, G, planck_area
from phyng.errors import InvalidMassError


def compton_reduced(m_kg: float) -> float:
    """
    Reduced Compton wavelength:
        λ_C = ħ / (m c)

    Args:
        m_kg: Mass in kilograms. Must be > 0.

    Returns:
        Reduced Compton wavelength in meters.

    Raises:
        InvalidMassError: If m_kg <= 0.
    """
    if m_kg <= 0:
        raise InvalidMassError(f"Mass must be positive, got {m_kg}")
    return HBAR / (m_kg * C)


def gravitational_radius(m_kg: float) -> float:
    """
    Gravitational radius:
        r_g = G m / c²

    Args:
        m_kg: Mass in kilograms. Must be > 0.

    Returns:
        Gravitational radius in meters.

    Raises:
        InvalidMassError: If m_kg <= 0.
    """
    if m_kg <= 0:
        raise InvalidMassError(f"Mass must be positive, got {m_kg}")
    return G * m_kg / (C * C)


def schwarzschild_radius(m_kg: float) -> float:
    """
    Schwarzschild radius:
        R_S = 2 G m / c²

    Args:
        m_kg: Mass in kilograms. Must be > 0.

    Returns:
        Schwarzschild radius in meters.

    Raises:
        InvalidMassError: If m_kg <= 0.
    """
    return 2.0 * gravitational_radius(m_kg)


def validate_compton_gravity_invariant(
    m_kg: float,
    relative_tolerance: float = 1e-12,
) -> dict:
    """
    Validate the structural lemma:
        λ_C · r_g = ℓ_P²

    This is a STRUCTURAL_LEMMA — an algebraic identity derivable from
    the definitions of λ_C, r_g, and ℓ_P. It does NOT prove new physics.

    Args:
        m_kg: Mass in kilograms. Must be > 0.
        relative_tolerance: Maximum relative error for validation.

    Returns:
        Dict with validation results, claim classification, and
        allowed/forbidden interpretations.
    """
    lambda_c = compton_reduced(m_kg)
    r_g = gravitational_radius(m_kg)
    product = lambda_c * r_g
    lp2 = planck_area()

    relative_error = abs(product - lp2) / lp2 if lp2 > 0 else float("inf")
    valid = relative_error <= relative_tolerance

    return {
        "lambda_c_m": lambda_c,
        "r_g_m": r_g,
        "product_m2": product,
        "planck_area_m2": lp2,
        "relative_error": relative_error,
        "valid": valid,
        "claim_type": "STRUCTURAL_LEMMA",
        "trace_type": "STRUCTURAL_TRACE",
        "predictive_gain": None,
        "allowed_interpretation": "Consistency lemma only",
        "forbidden_interpretation": "Proof of new physics",
    }
