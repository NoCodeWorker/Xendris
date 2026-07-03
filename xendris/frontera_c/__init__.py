"""
xendris.frontera_c — Canonical re-export layer for Frontera C physical rules.

This package exposes the Frontera C epistemic framework under the clean
xendris namespace. All logic lives in phyng/; these are stable re-exports.

Usage:
    from xendris.frontera_c import (
        Claim, evaluate_claim,
        planck_length, planck_area,
        predictive_gain,
        ClaimType, Layer, TraceType,
    )
"""

# --- Constants ---
from phyng.constants import (  # noqa: F401
    C, HBAR, G,
    planck_length, planck_mass, planck_area,
)

# --- Enums ---
from phyng.enums import ClaimType, Layer, TraceType  # noqa: F401

# --- Errors ---
from phyng.errors import InvalidMassError  # noqa: F401

# --- Core physics ---
from phyng.frontier_lengths import (  # noqa: F401
    validate_compton_gravity_invariant,
    compton_reduced,
    gravitational_radius,
    schwarzschild_radius,
)
# Compatibility alias for cleaner public API
compton_wavelength = compton_reduced
from phyng.operational_scale import (  # noqa: F401
    OperationalScale,
    review_operational_scale,
)
from phyng.signature import frontier_signature  # noqa: F401
from phyng.predictive_gain import predictive_gain  # noqa: F401
from phyng.epistemic_trace import epistemic_trace  # noqa: F401

# --- Claim gatekeeper ---
from phyng.claim_gatekeeper import Claim, evaluate_claim  # noqa: F401

__all__ = [
    # Constants
    "C", "HBAR", "G",
    "planck_length", "planck_mass", "planck_area",
    # Enums
    "ClaimType", "Layer", "TraceType",
    # Errors
    "InvalidMassError",
    # Physics
    "validate_compton_gravity_invariant",
    "compton_wavelength",
    "gravitational_radius",
    "OperationalScale",
    "review_operational_scale",
    "frontier_signature",
    "predictive_gain",
    "epistemic_trace",
    # Gatekeeper
    "Claim",
    "evaluate_claim",
]
