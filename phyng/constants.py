"""
Physical constants and derived Planck quantities.

All values in SI units.
Sources: CODATA 2018 recommended values.
"""

import math

# ── Fundamental constants ──────────────────────────────────────────────

C: float = 299_792_458.0
"""Speed of light in vacuum [m/s]."""

HBAR: float = 1.054571817e-34
"""Reduced Planck constant ħ [J·s]."""

G: float = 6.67430e-11
"""Newtonian gravitational constant [m³/(kg·s²)]."""

KB: float = 1.380649e-23
"""Boltzmann constant [J/K]."""


# ── Derived Planck quantities ──────────────────────────────────────────

def planck_length() -> float:
    """
    Planck length:
        ℓ_P = √(ħG / c³)

    Returns:
        Planck length in meters.
    """
    return math.sqrt(HBAR * G / C**3)


def planck_mass() -> float:
    """
    Planck mass:
        m_P = √(ħc / G)

    Returns:
        Planck mass in kilograms.
    """
    return math.sqrt(HBAR * C / G)


def planck_area() -> float:
    """
    Planck area:
        A_P = ℓ_P²

    Returns:
        Planck area in m².
    """
    lp = planck_length()
    return lp * lp
