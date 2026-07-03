"""
Phygn v1.7 — Prediction Accuracy: Core Metrics

compute_prediction_metrics: accuracy, calibration, lift metrics.
"""

from __future__ import annotations

import math
from phyng.prediction_accuracy.schemas import (
    PredictionRecord,
    PredictionOutcome,
    PredictionMetrics,
)

_MIN_OUTCOMES_FOR_METRICS = 3


def compute_prediction_metrics(
    records: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
    base_rate: float = 0.5,
) -> PredictionMetrics:
    """
    Compute accuracy and calibration metrics for a set of prediction/outcome pairs.

    Args:
        records: All PredictionRecord entries.
        outcomes: Resolved PredictionOutcome entries.
        base_rate: Prior correct rate (e.g. 0.5 for coin-flip baseline).

    Returns:
        PredictionMetrics — all None fields when insufficient data.
    """
    outcome_map = {o.prediction_id: o for o in outcomes}
    resolved = [o for o in outcomes if o.resolved and o.success is not None]
    n_resolved = len(resolved)
    n_total = len(records)

    if n_resolved < _MIN_OUTCOMES_FOR_METRICS:
        return PredictionMetrics(
            n_total=n_total,
            n_resolved=n_resolved,
            n_correct=0,
            n_incorrect=0,
        )

    n_correct = sum(1 for o in resolved if o.success is True)
    n_incorrect = n_resolved - n_correct
    hit_rate = n_correct / n_resolved
    accuracy_lift = hit_rate - base_rate

    # Precision / recall / FPR / FNR
    # Define TP: predicted UP or success, actual success
    tp = sum(1 for o in resolved if o.success and o.actual_direction != "DOWN")
    fp = sum(1 for o in resolved if not o.success and o.actual_direction != "UP")
    fn = sum(1 for o in resolved if o.success is False)
    tn = n_resolved - tp - fp - fn

    precision = tp / (tp + fp) if (tp + fp) > 0 else None
    recall = tp / (tp + fn) if (tp + fn) > 0 else None
    fpr = fp / (fp + tn) if (fp + tn) > 0 else None
    fnr = fn / (fn + tp) if (fn + tp) > 0 else None

    mae_items: list[float] = []
    for r in records:
        if r.prediction_id in outcome_map:
            actual = outcome_map[r.prediction_id].actual_value
            pred = r.predicted_value
            if actual is not None and pred is not None:
                mae_items.append(abs(actual - pred))
    mae = sum(mae_items) / len(mae_items) if mae_items else None

    # Benchmark relative error
    bm_errors = [
        abs(o.benchmark_value - o.actual_value) if o.benchmark_value is not None and o.actual_value is not None else None
        for o in resolved
    ]
    bm_errors_clean = [e for e in bm_errors if e is not None]
    bm_rel_err = (sum(bm_errors_clean) / len(bm_errors_clean)) if bm_errors_clean else None

    return PredictionMetrics(
        n_total=n_total,
        n_resolved=n_resolved,
        n_correct=n_correct,
        n_incorrect=n_incorrect,
        hit_rate=hit_rate,
        base_rate=base_rate,
        accuracy_lift=accuracy_lift,
        precision=precision,
        recall=recall,
        false_positive_rate=fpr,
        false_negative_rate=fnr,
        mean_absolute_error=mae,
        benchmark_relative_error=bm_rel_err,
    )
