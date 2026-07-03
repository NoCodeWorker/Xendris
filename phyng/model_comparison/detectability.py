import math


def delta_series(y_base: list[float], y_candidate: list[float]) -> list[float]:
    if len(y_base) != len(y_candidate):
        raise ValueError("series must have the same length")
    if not y_base:
        raise ValueError("series must not be empty")
    values = [*y_base, *y_candidate]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("series must contain only finite numbers")
    return [candidate - base for base, candidate in zip(y_base, y_candidate)]


def max_abs_delta(y_base: list[float], y_candidate: list[float]) -> float:
    return max(abs(value) for value in delta_series(y_base, y_candidate))


def classify_detectability(max_delta: float, epsilon_exp: float | None) -> str:
    if epsilon_exp is None:
        return "DETECTABILITY_REQUIRES_EPSILON"
    if epsilon_exp <= 0:
        raise ValueError("epsilon_exp must be > 0")
    if max_delta <= epsilon_exp:
        return "UNDETECTABLE_DIFFERENCE"
    return "DETECTABLE_TOY_DIFFERENCE"
