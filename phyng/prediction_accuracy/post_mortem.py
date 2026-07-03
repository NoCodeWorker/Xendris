"""
Phygn v1.7 — Prediction Accuracy: Post-Mortem Engine

generate_prediction_post_mortem: structured analysis of a resolved prediction.

Answers:
  - what was predicted
  - what happened
  - was baseline beaten
  - which evidence mattered
  - which gate was too strict / too loose
  - what should change
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome


class PostMortemReport(BaseModel):
    """Full post-mortem for a resolved prediction."""
    prediction_id: str
    what_was_predicted: str
    what_happened: str
    baseline_beaten: bool | None = None
    baseline_notes: str = ""
    evidence_that_mattered: list[str] = Field(default_factory=list)
    gate_assessment: str = ""
    gate_too_strict: bool | None = None
    gate_too_loose: bool | None = None
    recommended_changes: list[str] = Field(default_factory=list)
    verdict: str = "UNRESOLVED"
    # "CORRECT", "INCORRECT", "CORRECT_BEATS_BASELINE", "CORRECT_BELOW_BASELINE",
    # "INCORRECT_BASELINE_BETTER", "UNRESOLVED"


def generate_prediction_post_mortem(
    prediction_id: str,
    records: list[PredictionRecord],
    outcomes: list[PredictionOutcome],
) -> PostMortemReport:
    """
    Generate a structured post-mortem for a single resolved prediction.

    Args:
        prediction_id: ID of the prediction to analyze.
        records: Full ledger of prediction records.
        outcomes: Full list of resolved outcomes.

    Returns:
        PostMortemReport — if prediction or outcome not found, returns UNRESOLVED.
    """
    record = next((r for r in records if r.prediction_id == prediction_id), None)
    outcome = next((o for o in outcomes if o.prediction_id == prediction_id), None)

    if record is None:
        return PostMortemReport(
            prediction_id=prediction_id,
            what_was_predicted="RECORD NOT FOUND",
            what_happened="OUTCOME NOT AVAILABLE",
            verdict="UNRESOLVED",
        )
    if outcome is None or not outcome.resolved:
        return PostMortemReport(
            prediction_id=prediction_id,
            what_was_predicted=record.prediction_text,
            what_happened="Outcome not yet resolved.",
            verdict="UNRESOLVED",
        )

    # Build narrative
    what_predicted = (
        f"'{record.prediction_text}' — "
        f"target: {record.target_variable}, "
        f"direction: {record.predicted_direction or 'not specified'}, "
        f"horizon: {record.time_horizon}, "
        f"ladder: {record.ladder_level}, "
        f"gate: {record.gate_status}."
    )

    what_happened = (
        f"Actual direction: {outcome.actual_direction or 'unknown'}. "
        f"Actual value: {outcome.actual_value if outcome.actual_value is not None else 'unknown'}. "
        f"Success: {outcome.success}."
        + (f" Notes: {outcome.notes}" if outcome.notes else "")
    )

    # Baseline comparison
    baseline_beaten: bool | None = None
    baseline_notes = ""
    if outcome.benchmark_success is not None:
        baseline_beaten = outcome.benchmark_success
        if baseline_beaten:
            baseline_notes = "Candidate prediction beat the baseline benchmark."
        else:
            baseline_notes = "Baseline benchmark was NOT beaten by candidate prediction."

    # Verdict
    if outcome.success is True and (baseline_beaten is True or baseline_beaten is None):
        verdict = "CORRECT_BEATS_BASELINE" if baseline_beaten else "CORRECT"
    elif outcome.success is True and baseline_beaten is False:
        verdict = "CORRECT_BELOW_BASELINE"
    elif outcome.success is False and baseline_beaten is True:
        verdict = "INCORRECT_BASELINE_BETTER"
    elif outcome.success is False:
        verdict = "INCORRECT"
    else:
        verdict = "UNRESOLVED"

    # Evidence assessment
    evidence: list[str] = []
    level_val = record.evidence_level
    if record.ladder_level in ("SOURCE_BACKED_LIMITED", "BENCHMARK_SUPPORTED"):
        level_val = record.ladder_level
    if level_val in ("SOURCE_BACKED_LIMITED", "BENCHMARK_SUPPORTED"):
        evidence.append(f"Evidence level '{level_val}' was present at time of prediction.")
    if record.baseline_reference:
        evidence.append(f"Baseline reference used: {record.baseline_reference}.")
    if not evidence:
        evidence.append("No source-backed evidence was available at time of prediction.")

    # Gate assessment
    if verdict in ("CORRECT", "CORRECT_BEATS_BASELINE"):
        gate_assessment = "Gate was appropriate — prediction at this level succeeded."
        gate_too_strict = False
        gate_too_loose = False
        changes = ["No immediate gate change required. Continue monitoring."]
    elif verdict == "CORRECT_BELOW_BASELINE":
        gate_assessment = "Prediction succeeded but did not beat baseline. Gate may be too loose for this domain."
        gate_too_strict = False
        gate_too_loose = True
        changes = ["Consider requiring benchmark support before allowing this prediction type.", "Tighten evidence requirement."]
    elif verdict in ("INCORRECT", "INCORRECT_BASELINE_BETTER"):
        gate_assessment = "Prediction failed. Gate may have been too loose — insufficient evidence required."
        gate_too_strict = False
        gate_too_loose = True
        changes = ["Require higher ladder level before next similar prediction.", "Review source support criteria."]
    else:
        gate_assessment = "Insufficient data to assess gate."
        gate_too_strict = None
        gate_too_loose = None
        changes = ["Resolve prediction to enable post-mortem analysis."]

    return PostMortemReport(
        prediction_id=prediction_id,
        what_was_predicted=what_predicted,
        what_happened=what_happened,
        baseline_beaten=baseline_beaten,
        baseline_notes=baseline_notes,
        evidence_that_mattered=evidence,
        gate_assessment=gate_assessment,
        gate_too_strict=gate_too_strict,
        gate_too_loose=gate_too_loose,
        recommended_changes=changes,
        verdict=verdict,
    )
