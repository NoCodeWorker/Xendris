"""
Phygn v1.3 — Campaign: Real Source Selection & Positive Prediction Pressure

Runs the v1.3 campaign:
1. Selects real source candidates
2. Writes filled manifest draft
3. Generates extract targets
4. Evaluates positive prediction gate (current unoperationalized state)
5. Evaluates kill/pivot criteria
6. Generates all 6 reports
"""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.evidence.real_source_candidates import get_baseline_real_source_candidates
from phyng.evidence.manifest_draft_writer import write_filled_manifest_draft
from phyng.evidence.extract_target_generator import generate_extract_targets
from phyng.prediction_pressure import (
    CandidatePredictionSpec,
    evaluate_positive_prediction_gate,
    evaluate_kill_or_pivot,
    write_prediction_pressure_reports,
)


def main(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent.parent
    print(f"[REAL-SOURCE-SELECTION v1.3] project_root = {root}")

    # 1. Real source candidates
    candidates = get_baseline_real_source_candidates()
    _write_real_candidates_report(root, candidates)
    print(f"[1/5] Real source candidates defined: {len(candidates)}")

    # 2. Manifest draft
    draft_path = write_filled_manifest_draft(root)
    print(f"[2/5] Manifest draft written: {draft_path.name}")

    # 3. Extract targets
    targets_path = generate_extract_targets(root)
    print(f"[3/5] Extract targets generated: {targets_path.name}")

    # 4. Positive prediction gate (current unoperationalized state of Frontera C)
    # We define a default spec representing the current state (missing fields)
    current_spec = CandidatePredictionSpec(
        observable="visibility",
        baseline_model="V_base(t) = exp(-Gamma_env t)",
        # candidate_model is None/missing
        # candidate_term is None/missing
        parameters=["Q", "B", "L"],
        data_target="Talbot-Lau visibility loss",
        error_metric="Root-mean-square error (RMSE)",
        expected_pattern="DeltaGamma_C > 0",
        detectability_threshold=0.05,
        failure_condition="Gain_C <= 0"
    )
    gate_res = evaluate_positive_prediction_gate(current_spec)
    print(f"[4/5] Positive prediction gate evaluated: {gate_res.status}")

    # 5. Kill/pivot criteria
    # Evaluate under the current state: negative bounds only, no detectable candidate
    kp_res = evaluate_kill_or_pivot(
        has_detectable_candidate=False,
        has_benchmark_gain=False,
        negative_bounds_only=True,
        claim_blocking_useful=True,
        structural_atlas_useful=True
    )
    print(f"[5/5] Kill/pivot criteria evaluated: {kp_res.status}")

    # Write prediction pressure reports
    write_prediction_pressure_reports(root, gate_res, kp_res)

    # 6. Campaign report
    _write_campaign_report(root, gate_res, kp_res)

    print()
    print("=" * 60)
    print("  REAL-SOURCE-SELECTION v1.3 — Campaign Result")
    print("=" * 60)
    print(f"  Candidates Selected    : {len(candidates)}")
    print(f"  Positive Gate Status   : {gate_res.status}")
    print(f"  Kill/Pivot Status      : {kp_res.status}")
    print(f"  Conclusion             : {kp_res.conclusion}")
    print()
    print("  Blocked claims (ALL statuses):")
    print("    ✗ Phygn predicts gravitational decoherence.")
    print("    ✗ Frontera C is validated.")
    print("    ✗ The boundary-aware candidate is validated.")
    print("    ✗ SyntheticGain is physical PredictiveGain.")
    print("=" * 60)


def _write_real_candidates_report(project_root: Path, candidates: list) -> None:
    report_dir = project_root / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "real_source_candidates_v1_3.md"

    lines = [
        "# Real Source Candidates — v1.3",
        "",
        "Real source candidates selected for the baseline source pack.",
        "",
        "| ID | Slot | Title | Authors | Intended Support | Trust | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in candidates:
        title = c.title or "*Unknown*"
        authors = ", ".join(c.authors) if c.authors else "*None*"
        support = ", ".join(c.intended_support_types)
        lines.append(
            f"| {c.source_candidate_id} | {c.slot} | {title} | {authors} | {support} | {c.trust_level} | {c.verification_status} |"
        )
    lines.extend([
        "",
        "## Discipline Note",
        "These are candidates only. Ingestion requires local files and successful audit."
    ])
    report_path.write_text("\n".join(lines), encoding="utf-8")


def _write_campaign_report(project_root: Path, gate_res, kp_res) -> None:
    report_dir = project_root / "reports" / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "REAL-SOURCE-SELECTION-v1_3.md"

    lines = [
        "# REAL-SOURCE-SELECTION — v1.3 Campaign Report",
        "",
        f"- **Positive Prediction Gate**: **{gate_res.status}**",
        f"- **Kill/Pivot Status**: **{kp_res.status}**",
        f"- **Conclusion**: {kp_res.conclusion}",
        "",
        "## Blocked Claims",
        "- Phygn predicts gravitational decoherence. (BLOCKED)",
        "- Frontera C is validated. (BLOCKED)",
        "- The boundary-aware candidate is validated. (BLOCKED)",
        "- SyntheticGain is physical PredictiveGain. (BLOCKED)",
        "",
        "## Discipline Note",
        "A theory that cannot risk losing cannot earn the right to win."
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    root_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(root_arg)
