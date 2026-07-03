"""
Phygn v1.7 — Prediction Accuracy Reports Writer
"""

from __future__ import annotations

from pathlib import Path
from phyng.prediction_accuracy.schemas import (
    PredictionRecord,
    PredictionOutcome,
    PredictionMetrics,
    CalibrationReport,
    FilterLiftReport,
)
from phyng.prediction_accuracy.post_mortem import PostMortemReport


def write_prediction_accuracy_reports(
    reports_dir: str | Path,
    records: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
    metrics: PredictionMetrics,
    calibration: CalibrationReport,
    lift: FilterLiftReport,
    post_mortem: PostMortemReport,
) -> dict[str, str]:
    """
    Write the 4 prediction accuracy reports:
    - reports/prediction_accuracy/prediction_ledger_v1_7.md
    - reports/prediction_accuracy/calibration_report_v1_7.md
    - reports/prediction_accuracy/filter_lift_report_v1_7.md
    - reports/prediction_accuracy/post_mortem_report_v1_7.md
    """
    base_path = Path(reports_dir) / "prediction_accuracy"
    base_path.mkdir(parents=True, exist_ok=True)

    ledger_path = base_path / "prediction_ledger_v1_7.md"
    calibration_path = base_path / "calibration_report_v1_7.md"
    lift_path = base_path / "filter_lift_report_v1_7.md"
    post_mortem_path = base_path / "post_mortem_report_v1_7.md"

    # Ledger report
    outcome_map = {o.prediction_id: o for o in outcomes}
    ledger_rows = []
    for r in records:
        outc = outcome_map.get(r.prediction_id)
        resolved_str = "✅ Resolved" if outc and outc.resolved else "⏳ Pending"
        success_str = str(outc.success) if outc and outc.success is not None else "—"
        val_str = str(r.predicted_value) if r.predicted_value is not None else "—"
        prob_str = f"{r.predicted_probability:.2f}" if r.predicted_probability is not None else "—"
        ledger_rows.append(
            f"| `{r.prediction_id}` | `{r.ladder_level}` | {r.prediction_text[:40]}... | {val_str} | {prob_str} | {resolved_str} | {success_str} |"
        )

    ledger_content = f"""# Prediction Ledger — Phygn v1.7

## Registered Predictions ({len(records)} total)

| Prediction ID | Ladder Level | Text Snippet | Pred Value | Pred Prob | Status | Success |
|---|---|---|---|---|---|---|
{chr(10).join(ledger_rows)}

## Overall Performance
- **Resolved**: {metrics.n_resolved} / {metrics.n_total}
- **Correct**: {metrics.n_correct}
- **Incorrect**: {metrics.n_incorrect}
- **Hit Rate**: {f'{metrics.hit_rate:.2%}' if metrics.hit_rate is not None else 'N/A'}
- **Base Rate**: {f'{metrics.base_rate:.2%}' if metrics.base_rate is not None else 'N/A'}
- **Accuracy Lift**: {f'{metrics.accuracy_lift:+.2%}' if metrics.accuracy_lift is not None else 'N/A'}
- **Mean Absolute Error (MAE)**: {f'{metrics.mean_absolute_error:.4f}' if metrics.mean_absolute_error is not None else 'N/A'}
"""

    # Calibration report
    bin_rows = []
    for b in calibration.calibration_bins:
        bin_rows.append(
            f"| {b['bin_low']:.1f} - {b['bin_high']:.1f} | {b['n']} | {b['mean_p']:.1%} | {b['actual_rate']:.1%} | {abs(b['mean_p'] - b['actual_rate']):.1%} |"
        )

    notes_str = "\n".join([f"- {note}" for note in calibration.notes])

    calibration_content = f"""# Prediction Calibration Report — Phygn v1.7

## Metadata
- **Resolved probabilistic predictions**: {calibration.n_predictions_with_probability}
- **Brier Score**: `{calibration.brier_score if calibration.brier_score is not None else 'N/A'}` (lower is better, range [0, 1])
- **Expected Calibration Error (ECE)**: `{calibration.expected_calibration_error if calibration.expected_calibration_error is not None else 'N/A'}`
- **Calibration Status**: `{calibration.calibration_status}`

## Calibration Bins
| Bin Range | Sample Size | Mean Predicted Probability | Actual Success Rate | Absolute Gap |
|---|---|---|---|---|
{chr(10).join(bin_rows) if bin_rows else "| No data | - | - | - | - |"}

## Analysis Notes
{notes_str if notes_str else "No additional notes."}
"""

    # Filter Lift report
    ladder_rows = []
    for level, acc_val in lift.ladder_accuracy_by_level.items():
        ladder_rows.append(f"| `{level}` | {acc_val:.1%} |")

    lift_notes = "\n".join([f"- {note}" for note in lift.notes])

    lift_content = f"""# Filter Lift Report — Phygn v1.7

## Filter Effectiveness Summary
- **Passed Predictions (>= Source Backed)**: {lift.n_passed} (Accuracy: {f'{lift.accuracy_given_pass:.1%}' if lift.accuracy_given_pass is not None else 'N/A'})
- **Low Level Predictions (< Source Backed)**: {lift.n_not_passed} (Accuracy: {f'{lift.accuracy_given_low_level:.1%}' if lift.accuracy_given_low_level is not None else 'N/A'})
- **Base Rate Baseline**: {lift.base_rate:.1%}
- **Filter Lift over Baseline**: {f'{lift.lift_over_baseline:+.1%}' if lift.lift_over_baseline is not None else 'N/A'}
- **Filter Usefulness Status**: `{lift.filter_status}`

## Accuracy by Ladder Level
| Ladder Level | Success Rate |
|---|---|
{chr(10).join(ladder_rows) if ladder_rows else "| No resolved levels | - |"}

## Warnings and Recommendations
{lift_notes if lift_notes else "Phygn filters are functioning within normal operational parameters."}
"""

    # Post-mortem report
    pm_evidence = "\n".join([f"- {e}" for e in post_mortem.evidence_that_mattered])
    pm_changes = "\n".join([f"- {c}" for c in post_mortem.recommended_changes])

    post_mortem_content = f"""# Post-Mortem Analysis — {post_mortem.prediction_id}

## Core Case
- **Prediction ID**: `{post_mortem.prediction_id}`
- **What Was Predicted**: {post_mortem.what_was_predicted}
- **What Actually Happened**: {post_mortem.what_happened}
- **Verdict**: `{post_mortem.verdict}`

## Baseline Comparison
- **Baseline Beaten**: {post_mortem.baseline_beaten}
- **Notes**: {post_mortem.baseline_notes}

## Evidence and Audit
### Evidence that Mattered
{pm_evidence}

### Gate Assessment
- **Assessment**: {post_mortem.gate_assessment}
- **Gate Too Strict**: {post_mortem.gate_too_strict}
- **Gate Too Loose**: {post_mortem.gate_too_loose}

## Recommended Changes
{pm_changes}
"""

    ledger_path.write_text(ledger_content, encoding="utf-8")
    calibration_path.write_text(calibration_content, encoding="utf-8")
    lift_path.write_text(lift_content, encoding="utf-8")
    post_mortem_path.write_text(post_mortem_content, encoding="utf-8")

    return {
        "ledger": str(ledger_path),
        "calibration": str(calibration_path),
        "lift": str(lift_path),
        "post_mortem": str(post_mortem_path),
    }
