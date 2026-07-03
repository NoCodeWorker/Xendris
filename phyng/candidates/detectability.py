"""
Phygn v1.5 — Detectability Classifier

Classifies synthetic delta detectability and estimates alpha_min.
"""

from __future__ import annotations

import math

DetectabilityStatus = str  # DETECTABLE_SYNTHETIC_DELTA | UNDETECTABLE_SYNTHETIC_DELTA | NO_THRESHOLD_DECLARED

AlphaReasonablenessStatus = str  # ALPHA_REASONABLE_TOY | ALPHA_LARGE | ALPHA_EXTREME | ALPHA_UNPHYSICAL_OR_UNCONSTRAINED


def classify_detectability(
    max_abs_delta: float,
    epsilon_exp: float | None,
) -> DetectabilityStatus:
    """
    Classify whether the synthetic delta is detectable.

    Statuses:
        DETECTABLE_SYNTHETIC_DELTA
        UNDETECTABLE_SYNTHETIC_DELTA
        NO_THRESHOLD_DECLARED
    """
    if epsilon_exp is None:
        return "NO_THRESHOLD_DECLARED"
    if max_abs_delta > epsilon_exp:
        return "DETECTABLE_SYNTHETIC_DELTA"
    return "UNDETECTABLE_SYNTHETIC_DELTA"


def classify_alpha_reasonableness(alpha: float) -> AlphaReasonablenessStatus:
    """
    Classify whether alpha is physically reasonable (toy heuristic).

    Thresholds (heuristic, toy classification only):
        alpha <= 1e6  → ALPHA_REASONABLE_TOY
        1e6 < alpha <= 1e20 → ALPHA_LARGE
        1e20 < alpha <= 1e35 → ALPHA_EXTREME
        alpha > 1e35  → ALPHA_UNPHYSICAL_OR_UNCONSTRAINED
    """
    if alpha <= 1e6:
        return "ALPHA_REASONABLE_TOY"
    if alpha <= 1e20:
        return "ALPHA_LARGE"
    if alpha <= 1e35:
        return "ALPHA_EXTREME"
    return "ALPHA_UNPHYSICAL_OR_UNCONSTRAINED"


def estimate_alpha_min_for_detectability(
    B: float,
    gamma_env: float,
    t_grid: list[float],
    epsilon_exp: float | None,
) -> float | None:
    """
    First-order estimate:
        alpha_min ≈ epsilon_exp / (B * max(t * exp(-gamma_env * t)))

    Returns None if denominator is zero or epsilon_exp is None.
    """
    if epsilon_exp is None:
        return None

    # max over t of  t * exp(-gamma_env * t)
    values = [t * math.exp(-gamma_env * t) for t in t_grid]
    max_val = max(values) if values else 0.0

    denom = B * max_val
    if denom == 0.0 or not math.isfinite(denom):
        return None

    alpha_min = epsilon_exp / denom
    return alpha_min
