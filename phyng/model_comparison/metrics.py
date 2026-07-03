import math


def _validate_same_length(a: list[float], b: list[float]) -> None:
    if len(a) != len(b):
        raise ValueError("series must have the same length")
    if not a:
        raise ValueError("series must not be empty")
    values = [*a, *b]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("series must contain only finite numbers")


def mse(y_true: list[float], y_pred: list[float]) -> float:
    _validate_same_length(y_true, y_pred)
    return sum((truth - pred) ** 2 for truth, pred in zip(y_true, y_pred)) / len(y_true)


def mae(y_true: list[float], y_pred: list[float]) -> float:
    _validate_same_length(y_true, y_pred)
    return sum(abs(truth - pred) for truth, pred in zip(y_true, y_pred)) / len(y_true)


def rmse(y_true: list[float], y_pred: list[float]) -> float:
    return math.sqrt(mse(y_true, y_pred))


def compute_error(metric: str, y_true: list[float], y_pred: list[float]) -> float:
    normalized = metric.upper()
    if normalized == "MSE":
        return mse(y_true, y_pred)
    if normalized == "MAE":
        return mae(y_true, y_pred)
    if normalized == "RMSE":
        return rmse(y_true, y_pred)
    raise ValueError(f"Unsupported error metric: {metric}")


def compute_predictive_gain(error_base: float, error_candidate: float) -> float:
    if error_base <= 0:
        raise ValueError("error_base must be > 0")
    if error_candidate < 0:
        raise ValueError("error_candidate must be >= 0")
    return (error_base - error_candidate) / error_base
