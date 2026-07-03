"""
Predictive Gain.

    Gain_C = (Error(M_base) - Error(M_C)) / Error(M_base)

A model earns its place only by reducing error.
No gain, no claim.
"""


def predictive_gain(
    error_base: float,
    error_model: float,
) -> dict:
    """
    Compute the predictive gain of model M_C over baseline M_base.

    Args:
        error_base: Error of the baseline model. Must be > 0.
        error_model: Error of the Frontera C model. Must be >= 0.

    Returns:
        Dict with errors, gain value, and status classification.

    Raises:
        ValueError: If error_base <= 0 or error_model < 0.
    """
    if error_base <= 0:
        raise ValueError(f"error_base must be > 0, got {error_base}")
    if error_model < 0:
        raise ValueError(f"error_model must be >= 0, got {error_model}")

    gain = (error_base - error_model) / error_base

    if gain > 0:
        status = "POSITIVE_GAIN"
    elif gain == 0:
        status = "ZERO_GAIN"
    else:
        status = "NEGATIVE_GAIN"

    return {
        "error_base": error_base,
        "error_model": error_model,
        "gain": gain,
        "status": status,
    }
