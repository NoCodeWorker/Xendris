"""
Tests for frontier lengths and structural lemma.
"""

import math

import pytest

from phyng.constants import planck_length, planck_mass, planck_area
from phyng.errors import InvalidMassError
from phyng.frontier_lengths import (
    compton_reduced,
    gravitational_radius,
    schwarzschild_radius,
    validate_compton_gravity_invariant,
)


def test_planck_length_positive():
    lp = planck_length()
    assert lp > 0
    # Order of magnitude: ~1.6e-35 m
    assert 1e-36 < lp < 1e-34


def test_planck_mass_positive():
    mp = planck_mass()
    assert mp > 0
    # Order of magnitude: ~2.2e-8 kg
    assert 1e-9 < mp < 1e-7


def test_compton_reduced_positive():
    # Electron mass ≈ 9.109e-31 kg
    lc = compton_reduced(9.109e-31)
    assert lc > 0
    # Reduced Compton wavelength of electron ≈ 3.86e-13 m
    assert 3e-13 < lc < 5e-13


def test_compton_reduced_rejects_negative_mass():
    with pytest.raises(InvalidMassError):
        compton_reduced(-1.0)


def test_compton_reduced_rejects_zero_mass():
    with pytest.raises(InvalidMassError):
        compton_reduced(0.0)


def test_gravitational_radius_positive():
    # Solar mass ≈ 1.989e30 kg → r_g ≈ 1.48 km
    rg = gravitational_radius(1.989e30)
    assert rg > 0
    assert 1000 < rg < 2000


def test_gravitational_radius_rejects_negative_mass():
    with pytest.raises(InvalidMassError):
        gravitational_radius(-1.0)


def test_schwarzschild_is_twice_rg():
    m = 1.0  # 1 kg
    rg = gravitational_radius(m)
    rs = schwarzschild_radius(m)
    assert math.isclose(rs, 2.0 * rg, rel_tol=1e-15)


def test_compton_gravity_invariant():
    """λ_C · r_g = ℓ_P² for any mass."""
    result = validate_compton_gravity_invariant(1.0)
    assert result["valid"] is True
    assert result["claim_type"] == "STRUCTURAL_LEMMA"
    assert result["trace_type"] == "STRUCTURAL_TRACE"
    assert result["predictive_gain"] is None
    assert result["forbidden_interpretation"] == "Proof of new physics"


def test_compton_gravity_invariant_electron_mass():
    """Invariant holds for electron mass too."""
    m_e = 9.10938e-31
    result = validate_compton_gravity_invariant(m_e)
    assert result["valid"] is True


def test_compton_gravity_invariant_planck_mass():
    """Invariant holds for Planck mass."""
    mp = planck_mass()
    result = validate_compton_gravity_invariant(mp)
    assert result["valid"] is True
