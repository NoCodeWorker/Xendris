"""
Epistemic trace τ_O(H).

Measures distinguishability between hypothesis H and null hypothesis ¬H
using Jensen-Shannon divergence over discrete probability distributions.

τ = 0        → NULL_TRACE     (no information)
0 < τ ≤ ε   → NOT_DETECTABLE (below experimental resolution)
τ > ε        → DETECTABLE_TRACE
"""

import numpy as np


def normalize_distribution(p: np.ndarray) -> np.ndarray:
    """
    Normalize a non-negative array to a probability distribution.

    Args:
        p: Non-negative array.

    Returns:
        Normalized array summing to 1.

    Raises:
        ValueError: If any element is negative or sum is zero.
    """
    p = np.asarray(p, dtype=np.float64)
    if np.any(p < 0):
        raise ValueError(f"Distribution has negative values: {p}")
    total = p.sum()
    if total == 0:
        raise ValueError("Distribution sums to zero — cannot normalize")
    return p / total


def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """
    Kullback-Leibler divergence D_KL(P || Q).

    Args:
        p: Reference distribution (will be normalized).
        q: Comparison distribution (will be normalized).
        eps: Small constant to avoid log(0).

    Returns:
        KL divergence (non-negative float).
    """
    p = normalize_distribution(p)
    q = normalize_distribution(q)
    # Clip to avoid log(0)
    q_safe = np.clip(q, eps, None)
    p_safe = np.clip(p, eps, None)
    return float(np.sum(p_safe * np.log(p_safe / q_safe)))


def jensen_shannon_divergence(
    p: np.ndarray,
    q: np.ndarray,
    eps: float = 1e-12,
) -> float:
    """
    Jensen-Shannon divergence JSD(P || Q).

    Symmetric, bounded [0, ln(2)].

    Args:
        p: First distribution (will be normalized).
        q: Second distribution (will be normalized).
        eps: Small constant to avoid log(0).

    Returns:
        JSD value (non-negative float).
    """
    p = normalize_distribution(p)
    q = normalize_distribution(q)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m, eps) + 0.5 * kl_divergence(q, m, eps)


def epistemic_trace(
    p_h: np.ndarray,
    p_not_h: np.ndarray,
    epsilon_exp: float = 1e-6,
) -> dict:
    """
    Compute the epistemic trace τ_O(H).

    τ = JSD(P(Y|H), P(Y|¬H))

    Args:
        p_h: Distribution under hypothesis H.
        p_not_h: Distribution under null hypothesis ¬H.
        epsilon_exp: Experimental resolution threshold.

    Returns:
        Dict with τ, divergence type, trace classification,
        and operational status.
    """
    p_h = np.asarray(p_h, dtype=np.float64)
    p_not_h = np.asarray(p_not_h, dtype=np.float64)

    tau = jensen_shannon_divergence(p_h, p_not_h)

    if tau == 0.0:
        trace_type = "NULL_TRACE"
        operational_status = "EMPTY"
    elif tau > epsilon_exp:
        trace_type = "DETECTABLE_TRACE"
        operational_status = "DETECTABLE"
    else:
        trace_type = "NOT_DETECTABLE"
        operational_status = "NOT_DETECTABLE"

    return {
        "tau": tau,
        "divergence": "JENSEN_SHANNON",
        "epsilon_exp": epsilon_exp,
        "trace_type": trace_type,
        "operational_status": operational_status,
    }
