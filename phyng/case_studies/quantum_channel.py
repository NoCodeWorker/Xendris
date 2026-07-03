"""
Case study: Depolarizing quantum channel.

Minimal case for epistemic trace computation.

Null hypothesis ¬H:  p = 0 (no depolarization, identity channel)
Hypothesis H:        p > 0 (depolarization present)

For initial state |0⟩ measured in computational basis:

    P(Y=0 | ¬H) = 1,    P(Y=1 | ¬H) = 0
    P(Y=0 | H)  = 1-p/2, P(Y=1 | H)  = p/2

When p = 0: τ = 0 (NULL_TRACE)
When p > 0: τ > 0 (DETECTABLE_TRACE, if above ε_exp)
"""

import numpy as np

from phyng.epistemic_trace import epistemic_trace
from phyng.errors import InvalidProbabilityError


def depolarizing_distribution(p: float) -> np.ndarray:
    """
    Output distribution for depolarizing channel on |0⟩.

    Args:
        p: Depolarizing parameter, 0 ≤ p ≤ 1.

    Returns:
        Array [P(Y=0|H), P(Y=1|H)] = [1 - p/2, p/2].

    Raises:
        InvalidProbabilityError: If p is outside [0, 1].
    """
    if not (0.0 <= p <= 1.0):
        raise InvalidProbabilityError(
            f"Depolarizing parameter p must be in [0, 1], got {p}"
        )
    return np.array([1.0 - p / 2.0, p / 2.0])


def quantum_channel_trace_case(
    p: float,
    epsilon_exp: float = 1e-6,
) -> dict:
    """
    Run the depolarizing channel case study.

    Computes τ = JSD(P(Y|H), P(Y|¬H)) and classifies the trace.

    Args:
        p: Depolarizing parameter, 0 ≤ p ≤ 1.
        epsilon_exp: Experimental resolution threshold.

    Returns:
        Dict with case ID, distributions, τ, trace type,
        claim status, and interpretation.
    """
    p_h = depolarizing_distribution(p)
    p_not_h = np.array([1.0, 0.0])  # identity channel: no depolarization

    trace = epistemic_trace(p_h, p_not_h, epsilon_exp)

    tau = trace["tau"]
    trace_type = trace["trace_type"]

    if trace_type == "NULL_TRACE":
        claim_status = "NOT_DETECTABLE"
        interpretation = (
            "Depolarizing parameter p=0. Channel is identity. "
            "No epistemic trace. No claim possible."
        )
    elif trace_type == "DETECTABLE_TRACE":
        claim_status = "ALLOWED"
        interpretation = (
            f"Depolarizing parameter p={p}. "
            f"Epistemic trace τ={tau:.6e} exceeds ε_exp={epsilon_exp:.0e}. "
            "Trace is detectable."
        )
    else:
        # NOT_DETECTABLE: 0 < τ ≤ ε_exp
        claim_status = "NOT_DETECTABLE"
        interpretation = (
            f"Depolarizing parameter p={p}. "
            f"Epistemic trace τ={tau:.6e} is below ε_exp={epsilon_exp:.0e}. "
            "Trace exists but is not experimentally resolvable."
        )

    return {
        "case_id": "QC-DEPOLARIZING-001",
        "p": p,
        "p_h": p_h.tolist(),
        "p_not_h": p_not_h.tolist(),
        "tau": tau,
        "trace_type": trace_type,
        "claim_status": claim_status,
        "interpretation": interpretation,
    }
