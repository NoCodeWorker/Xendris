"""
Phygn v1.4 — Campaign: Candidate Model Operationalization

Coordinates:
1. Defining the default candidate CAND-FC-B-NEGCTRL-001
2. Classifying admissibility
3. Evaluating failure conditions
4. Evaluating readiness and prediction gate status
5. Generating v1.4 reports
"""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.candidates import (
    CandidatePredictionSpec,
    classify_candidate_admissibility,
    evaluate_candidate_failure_conditions,
    evaluate_candidate_readiness,
    write_v1_4_reports,
)
from phyng.prediction_pressure import (
    evaluate_positive_prediction_gate,
    evaluate_kill_or_pivot,
)


def main(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent.parent
    print(f"[CANDIDATE-MODEL-OPERATIONALIZATION v1.4] project_root = {root}")

    # 1. Define default candidate
    default_cand = CandidatePredictionSpec(
        candidate_id="CAND-FC-B-NEGCTRL-001",
        observable="visibility_loss",
        baseline_model="exp(-Gamma_env * t)",
        candidate_model="exp(-(Gamma_env + alpha * B)t)",
        candidate_term="alpha * B",
        parameters={"alpha": "pre_registered_constant"},
        parameter_status="PRE_REGISTERED",
        data_target=None,
        error_metric=None,
        expected_pattern="decreased visibility",
        detectability_threshold=0.01,
        failure_condition=["FAIL_GAIN_NONPOSITIVE", "FAIL_UNDETECTABLE_DELTA"],
        source_ids=[],
        benchmark_ids=[],
        claim_level_requested=0,
        term_units="1/s",
        alpha_units="1/s",
        dimensionless_core="B",
        has_source_support=False,
        has_benchmark=False,
    )

    # 2. Admissibility
    admissibility = classify_candidate_admissibility(default_cand, "B_SUPPRESSED")

    # 3. Failure conditions
    failures = evaluate_candidate_failure_conditions(default_cand)

    # 4. Readiness and gate status
    readiness = evaluate_candidate_readiness(default_cand, admissibility, failures)
    gate_res = evaluate_positive_prediction_gate(default_cand)

    # 5. Kill / pivot status
    # Candidate exists but no benchmark gain yet
    kp_res = evaluate_kill_or_pivot(
        has_detectable_candidate=True,
        has_benchmark_gain=False,
        negative_bounds_only=False,
        claim_blocking_useful=False,
        structural_atlas_useful=False,
    )

    # 6. Write reports
    write_v1_4_reports(
        root,
        default_cand,
        admissibility,
        failures,
        readiness,
        gate_res.status,
        kp_res.status,
    )

    print()
    print("=" * 60)
    print("  CANDIDATE-MODEL-OPERATIONALIZATION v1.4 — Campaign Result")
    print("=" * 60)
    print(f"  Candidate ID           : {default_cand.candidate_id}")
    print(f"  Admissibility          : {admissibility}")
    print(f"  Triggered Failures     : {', '.join(failures) if failures else 'None'}")
    print(f"  Readiness Status       : {readiness}")
    print(f"  Positive Gate Status   : {gate_res.status}")
    print(f"  Kill/Pivot Status      : {kp_res.status}")
    print()
    print("  Blocked claims (ALL statuses):")
    print("    ✗ Phygn predicts gravitational decoherence.")
    print("    ✗ Frontera C is validated.")
    print("    ✗ The boundary-aware candidate is validated.")
    print("    ✗ SyntheticGain is physical PredictiveGain.")
    print("=" * 60)


if __name__ == "__main__":
    root_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(root_arg)
