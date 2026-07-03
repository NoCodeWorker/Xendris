"""
Phygn v1.7 — Prediction Accuracy: Calibration

Brier score, expected calibration error, and calibration status.
"""

from __future__ import annotations

from phyng.prediction_accuracy.schemas import (
    PredictionRecord,
    PredictionOutcome,
    CalibrationReport,
)

_N_BINS = 5
_MIN_FOR_CALIBRATION = 5


def compute_brier_score(
    probabilities: list[float],
    outcomes_binary: list[int],  # 1 = correct, 0 = incorrect
) -> float:
    """Brier score = mean((p - outcome)^2). Lower is better."""
    if not probabilities or len(probabilities) != len(outcomes_binary):
        return float("nan")
    return sum((p - o) ** 2 for p, o in zip(probabilities, outcomes_binary)) / len(probabilities)


def compute_expected_calibration_error(
    probabilities: list[float],
    outcomes_binary: list[int],
    n_bins: int = _N_BINS,
) -> float:
    """ECE: weighted mean |mean_prob - actual_rate| over bins."""
    if not probabilities or len(probabilities) != len(outcomes_binary):
        return float("nan")
    n = len(probabilities)
    bins: list[list[tuple[float, int]]] = [[] for _ in range(n_bins)]
    for p, o in zip(probabilities, outcomes_binary):
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append((p, o))
    ece = 0.0
    for b in bins:
        if b:
            mean_p = sum(x[0] for x in b) / len(b)
            actual_rate = sum(x[1] for x in b) / len(b)
            ece += (len(b) / n) * abs(mean_p - actual_rate)
    return ece


def evaluate_calibration(
    records: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
) -> CalibrationReport:
    """
    Evaluate calibration for all predictions that have a predicted_probability.

    Calibration status:
        WELL_CALIBRATED      — ECE < 0.10
        OVERCONFIDENT_GATE   — high confidence but low accuracy
        UNDERCONFIDENT_GATE  — low confidence but high accuracy
        INSUFFICIENT_DATA    — < MIN_FOR_CALIBRATION resolved with probability
    """
    outcome_map = {o.prediction_id: o for o in outcomes if o.resolved and o.success is not None}

    pairs = [
        (r.predicted_probability, 1 if outcome_map[r.prediction_id].success else 0)
        for r in records
        if r.predicted_probability is not None and r.prediction_id in outcome_map
    ]

    n = len(pairs)
    if n < _MIN_FOR_CALIBRATION:
        return CalibrationReport(
            n_predictions_with_probability=n,
            calibration_status="INSUFFICIENT_DATA",
            notes=["Not enough resolved probabilistic predictions to calibrate."],
        )

    probs = [p for p, _ in pairs]
    outc = [o for _, o in pairs]

    brier = compute_brier_score(probs, outc)
    ece = compute_expected_calibration_error(probs, outc)
    mean_p = sum(probs) / n
    actual_rate = sum(outc) / n
    overconf_index = mean_p - actual_rate

    if ece < 0.10:
        status = "WELL_CALIBRATED"
    elif overconf_index > 0.15:
        status = "OVERCONFIDENT_GATE"
    elif overconf_index < -0.15:
        status = "UNDERCONFIDENT_GATE"
    else:
        status = "WELL_CALIBRATED"

    # Build calibration bins for report
    bins_data: list[dict] = []
    for i in range(_N_BINS):
        low = i / _N_BINS
        high = (i + 1) / _N_BINS
        bin_pairs = [(p, o) for p, o in zip(probs, outc) if low <= p < high]
        if bin_pairs:
            bins_data.append({
                "bin_low": low,
                "bin_high": high,
                "n": len(bin_pairs),
                "mean_p": round(sum(b[0] for b in bin_pairs) / len(bin_pairs), 3),
                "actual_rate": round(sum(b[1] for b in bin_pairs) / len(bin_pairs), 3),
            })

    return CalibrationReport(
        n_predictions_with_probability=n,
        brier_score=round(brier, 4),
        expected_calibration_error=round(ece, 4),
        calibration_status=status,
        calibration_bins=bins_data,
        notes=[f"Overconfidence index: {overconf_index:.3f}"],
    )
