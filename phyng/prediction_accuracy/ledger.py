"""
Phygn v1.7 — Prediction Accuracy: Ledger & Filter Lift

record_prediction, resolve_prediction, evaluate_filter_lift.

The ledger answers: does passing Phygn filters improve predictions?
"""

from __future__ import annotations

from phyng.prediction_accuracy.schemas import (
    PredictionRecord,
    PredictionOutcome,
    FilterLiftReport,
)

# Minimum resolved outcomes to compute lift
_MIN_FOR_LIFT = 5
# Ladder levels considered "passed" (≥ SOURCE_BACKED_LIMITED)
_PASSED_LEVELS = {
    "SOURCE_BACKED_LIMITED",
    "BENCHMARK_SUPPORTED",
    "OPERATIONALLY_ACTIONABLE",
    "AUTOMATED_EXECUTION_ALLOWED",
}
_LOW_LEVELS = {
    "DREAM",
    "HYPOTHESIS_SEED",
    "FORMALIZING_HYPOTHESIS",
    "TESTABLE_HYPOTHESIS",
    "SYNTHETIC_SUPPORT",
}


def record_prediction(record: PredictionRecord, ledger: list[PredictionRecord]) -> None:
    """Append a prediction to the ledger (in-place)."""
    ledger.append(record)


def resolve_prediction(
    prediction_id: str,
    ledger: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
    actual_value: float | None = None,
    actual_direction: str | None = None,
    success: bool | None = None,
    benchmark_value: float | None = None,
    notes: str | None = None,
    resolved_at: str | None = None,
) -> PredictionOutcome:
    """
    Resolve a prediction by matching its ID and creating a PredictionOutcome.

    Returns the created outcome (caller must append to outcomes list).
    """
    record = next((r for r in ledger if r.prediction_id == prediction_id), None)
    error_value: float | None = None
    if record and record.predicted_value is not None and actual_value is not None:
        error_value = abs(record.predicted_value - actual_value)

    outcome = PredictionOutcome(
        prediction_id=prediction_id,
        resolved=True,
        actual_value=actual_value,
        actual_direction=actual_direction,
        success=success,
        error_value=error_value,
        benchmark_value=benchmark_value,
        benchmark_success=(
            (actual_value is not None and benchmark_value is not None and actual_value > benchmark_value)
            if (actual_value is not None and benchmark_value is not None)
            else None
        ),
        resolved_at=resolved_at,
        notes=notes,
    )
    outcomes.append(outcome)
    return outcome


def evaluate_filter_lift(
    records: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
    base_rate: float = 0.5,
) -> FilterLiftReport:
    """
    Evaluate whether Phygn filters (higher ladder levels) improve accuracy.

    Statuses:
        FILTER_SHOWS_PREDICTIVE_LIFT      — passed predictions outperform baseline
        FILTER_NOT_PREDICTIVELY_USEFUL_YET — passed predictions ≤ baseline accuracy
        INSUFFICIENT_OUTCOMES             — not enough resolved outcomes
        LADDER_NOT_PREDICTIVELY_ORDERED   — higher rungs do NOT outperform lower
    """
    outcome_map = {o.prediction_id: o for o in outcomes if o.resolved and o.success is not None}
    resolved_records = [r for r in records if r.prediction_id in outcome_map]

    if len(resolved_records) < _MIN_FOR_LIFT:
        return FilterLiftReport(
            n_passed=0,
            n_not_passed=0,
            base_rate=base_rate,
            filter_status="INSUFFICIENT_OUTCOMES",
            notes=[f"Need at least {_MIN_FOR_LIFT} resolved outcomes. Have {len(resolved_records)}."],
        )

    passed = [r for r in resolved_records if r.ladder_level in _PASSED_LEVELS]
    low = [r for r in resolved_records if r.ladder_level in _LOW_LEVELS]

    def acc(subset: list[PredictionRecord]) -> float | None:
        if not subset:
            return None
        return sum(1 for r in subset if outcome_map[r.prediction_id].success) / len(subset)

    acc_pass = acc(passed)
    acc_low = acc(low)
    lift = (acc_pass - base_rate) if acc_pass is not None else None

    # Ladder accuracy by level
    levels = set(r.ladder_level for r in resolved_records)
    ladder_acc: dict[str, float] = {}
    for level in levels:
        subset = [r for r in resolved_records if r.ladder_level == level]
        a = acc(subset)
        if a is not None:
            ladder_acc[level] = round(a, 3)

    # Check if ladder is predictively ordered
    level_order = [
        "DREAM", "HYPOTHESIS_SEED", "FORMALIZING_HYPOTHESIS", "TESTABLE_HYPOTHESIS",
        "SYNTHETIC_SUPPORT", "SOURCE_BACKED_LIMITED", "BENCHMARK_SUPPORTED",
        "OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED",
    ]
    ordered_acc = [ladder_acc[lv] for lv in level_order if lv in ladder_acc]
    is_ordered = True
    for i in range(len(ordered_acc) - 1):
        val1 = ordered_acc[i]
        val2 = ordered_acc[i + 1]
        if val1 > val2:
            is_ordered = False
            break

    if len(ordered_acc) >= 2 and not is_ordered:
        status = "LADDER_NOT_PREDICTIVELY_ORDERED"
    elif lift is not None and lift > 0:
        status = "FILTER_SHOWS_PREDICTIVE_LIFT"
    elif lift is not None and lift <= 0:
        status = "FILTER_NOT_PREDICTIVELY_USEFUL_YET"
    else:
        status = "INSUFFICIENT_OUTCOMES"

    notes: list[str] = []
    if status == "FILTER_NOT_PREDICTIVELY_USEFUL_YET":
        notes.append(
            "Phygn filters are not yet improving prediction accuracy. "
            "This is allowed and important — continue collecting data."
        )
    if status == "LADDER_NOT_PREDICTIVELY_ORDERED":
        notes.append(
            "SERIOUS WARNING: Higher ladder levels are not producing better accuracy. "
            "Review gate criteria."
        )

    return FilterLiftReport(
        n_passed=len(passed),
        n_not_passed=len(low),
        accuracy_given_pass=acc_pass,
        accuracy_given_low_level=acc_low,
        base_rate=base_rate,
        lift_over_baseline=lift,
        filter_status=status,
        ladder_accuracy_by_level=ladder_acc,
        notes=notes,
    )
