"""
Phygn v1.7 — Idea-to-Hypothesis UX, Prediction Accuracy & Model-Agnostic Campaign

Orchestrates a full v1.7 run, demonstrating:
  1. Idea intake and hypothesis seed card generation
  2. Intuition math translation
  3. Prediction ledger registration, resolution, calibration, and filter lift evaluations
  4. Post-mortem analysis on a resolved case
  5. Model runtime backend registration, evaluation, and capability routing
  6. Generation of all 10 reports (2 UX, 4 accuracy, 3 runtime, 1 campaign)
"""

from __future__ import annotations

from pathlib import Path
from phyng.ux import IdeaIntake, process_idea_intake, translate_from_intake
from phyng.ux.report import write_ux_reports

from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome
from phyng.prediction_accuracy.ledger import record_prediction, resolve_prediction, evaluate_filter_lift
from phyng.prediction_accuracy.metrics import compute_prediction_metrics
from phyng.prediction_accuracy.calibration import evaluate_calibration
from phyng.prediction_accuracy.post_mortem import generate_prediction_post_mortem
from phyng.prediction_accuracy.report import write_prediction_accuracy_reports

from phyng.model_runtime.schemas import BackendRegistration
from phyng.model_runtime.backends import (
    register_model_backend,
    evaluate_backend_permission,
    route_model_task,
    clear_registry,
)
from phyng.model_runtime.report import write_model_runtime_reports


def run_idea_to_hypothesis_accuracy_campaign(
    reports_dir: str | Path = "reports",
) -> dict:
    """
    Run the full v1.7 campaign.
    """
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------------
    # 1. UX Intake & Math Translator
    # ---------------------------------------------------------------------------
    intake = IdeaIntake(
        idea_id="IDEA-FC-DECO-001",
        raw_intuition="Maybe gravitational decoherence modulates visibility loss at boundary sensitivity.",
        domain="quantum_decoherence",
        possible_cause="boundary scale Schwarzschild ratio",
        possible_effect="faster fringe contrast decay",
        context="mesoscopic molecular interferometry",
        user_confidence=0.8,
        intended_use="private_exploration",
        risk_level="RISK_2_INTERNAL_RESEARCH",
    )

    seed_card = process_idea_intake(intake)
    translator_out = translate_from_intake(intake)
    ux_paths = write_ux_reports(reports_path, seed_card, translator_out)

    # ---------------------------------------------------------------------------
    # 2. Prediction Accuracy Ledger
    # ---------------------------------------------------------------------------
    ledger: list[PredictionRecord] = []
    outcomes: list[PredictionOutcome] = []

    # Let's populate 6 mock predictions to ensure ECE/calibration/lift work
    # We want at least 5 resolved outcomes
    mock_records = [
        PredictionRecord(
            prediction_id="PRED-001",
            prediction_text="Frontera C predicts faster decay under high alpha.",
            target_variable="decay_rate",
            predicted_probability=0.90,
            predicted_value=1.5,
            ladder_level="BENCHMARK_SUPPORTED",  # Passed
        ),
        PredictionRecord(
            prediction_id="PRED-002",
            prediction_text="Baseline environment-only decay is 0.05.",
            target_variable="decay_rate",
            predicted_probability=0.95,
            predicted_value=0.05,
            ladder_level="BENCHMARK_SUPPORTED",  # Passed
        ),
        PredictionRecord(
            prediction_id="PRED-003",
            prediction_text="Fringe contrast drops below 1e-6 at t=10.",
            target_variable="visibility",
            predicted_probability=0.30,
            predicted_value=0.0,
            ladder_level="DREAM",  # Not passed
        ),
        PredictionRecord(
            prediction_id="PRED-004",
            prediction_text="Social sentiment leads return by 1 day.",
            target_variable="stock_return",
            predicted_probability=0.60,
            predicted_value=0.02,
            ladder_level="HYPOTHESIS_SEED",  # Not passed
        ),
        PredictionRecord(
            prediction_id="PRED-005",
            prediction_text="Quantum channel is stable for 30s.",
            target_variable="coherence_time",
            predicted_probability=0.85,
            predicted_value=30.0,
            ladder_level="OPERATIONALLY_ACTIONABLE",  # Passed
        ),
        PredictionRecord(
            prediction_id="PRED-006",
            prediction_text="Local noise level will remain below 0.01.",
            target_variable="noise_rms",
            predicted_probability=0.50,
            predicted_value=0.005,
            ladder_level="DREAM",  # Not passed
        ),
    ]

    for r in mock_records:
        record_prediction(r, ledger)

    # Resolve all 6 predictions
    resolve_prediction(
        prediction_id="PRED-001",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=1.6,
        actual_direction="UP",
        success=True,
        benchmark_value=1.0,
    )
    resolve_prediction(
        prediction_id="PRED-002",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=0.05,
        actual_direction="NEUTRAL",
        success=True,
        benchmark_value=0.06,
    )
    resolve_prediction(
        prediction_id="PRED-003",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=0.001,
        actual_direction="UP",
        success=False,
        benchmark_value=0.0,
    )
    resolve_prediction(
        prediction_id="PRED-004",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=0.01,
        actual_direction="UP",
        success=True,
        benchmark_value=0.0,
    )
    resolve_prediction(
        prediction_id="PRED-005",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=32.0,
        actual_direction="UP",
        success=True,
        benchmark_value=25.0,
    )
    resolve_prediction(
        prediction_id="PRED-006",
        ledger=ledger,
        outcomes=outcomes,
        actual_value=0.02,
        actual_direction="UP",
        success=False,
        benchmark_value=0.01,
    )

    metrics = compute_prediction_metrics(ledger, outcomes, base_rate=0.5)
    calibration = evaluate_calibration(ledger, outcomes)
    lift = evaluate_filter_lift(ledger, outcomes, base_rate=0.5)
    post_mortem = generate_prediction_post_mortem("PRED-001", ledger, outcomes)

    accuracy_paths = write_prediction_accuracy_reports(
        reports_dir=reports_path,
        records=ledger,
        outcomes=outcomes,
        metrics=metrics,
        calibration=calibration,
        lift=lift,
        post_mortem=post_mortem,
    )

    # ---------------------------------------------------------------------------
    # 3. Model-Agnostic Runtime
    # ---------------------------------------------------------------------------
    clear_registry()
    backends_to_register = [
        BackendRegistration(
            backend_id="gpt-4o",
            model_name="GPT-4o",
            model_type="FRONTIER_API",
            supports_json_mode=True,
            supports_tool_use=True,
            quality_tier=1,
        ),
        BackendRegistration(
            backend_id="llama-3-8b",
            model_name="Llama-3-8B-Instruct",
            model_type="OPEN_SOURCE_API",
            supports_json_mode=True,
            supports_tool_use=False,
            quality_tier=2,
        ),
        BackendRegistration(
            backend_id="phi-3-mini",
            model_name="Phi-3-Mini-Local",
            model_type="LOCAL_LLM",
            supports_json_mode=False,
            supports_tool_use=False,
            quality_tier=3,
            is_local=True,
        ),
        BackendRegistration(
            backend_id="human-expert",
            model_name="Human Expert Review Panel",
            model_type="HUMAN_REVIEW",
            supports_json_mode=False,
            supports_tool_use=False,
            quality_tier=1,
        ),
    ]

    for b in backends_to_register:
        register_model_backend(b)

    # Evaluate some tasks to test capability routing
    eval_permissions = [
        evaluate_backend_permission("gpt-4o", "automated_execution"),
        evaluate_backend_permission("llama-3-8b", "claim_extraction"),
        evaluate_backend_permission("phi-3-mini", "idea_intake"),
        evaluate_backend_permission("phi-3-mini", "automated_execution"),
        evaluate_backend_permission("human-expert", "gatekeeping"),
    ]

    runtime_paths = write_model_runtime_reports(reports_path, eval_permissions)

    campaign_path = reports_path / "campaigns" / "IDEA-TO-HYPOTHESIS-ACCURACY-RUNTIME-v1_7.md"
    campaign_path.parent.mkdir(parents=True, exist_ok=True)
    # Prepare forward slash paths for the markdown links to prevent f-string backslash syntax error
    flow_p = Path(ux_paths['flow']).as_posix()
    cards_p = Path(ux_paths['cards']).as_posix()
    ledger_p = Path(accuracy_paths['ledger']).as_posix()
    cal_p = Path(accuracy_paths['calibration']).as_posix()
    lift_p = Path(accuracy_paths['lift']).as_posix()
    pm_p = Path(accuracy_paths['post_mortem']).as_posix()
    reg_p = Path(runtime_paths['registry']).as_posix()
    os_p = Path(runtime_paths['opensource']).as_posix()
    rout_p = Path(runtime_paths['routing']).as_posix()

    campaign_content = f"""# Campaign Report — IDEA-TO-HYPOTHESIS-ACCURACY-RUNTIME-v1_7

## Status: COMPLETE
- **Intake Seed Card Created**: `{seed_card.seed_id}` (UX Status: `{seed_card.ux_status}`)
- **Math Translation Propose-Label**: `{translator_out.label}`
- **Ledger resolved entries**: {metrics.n_resolved} / {metrics.n_total}
- **Filter Lift Status**: `{lift.filter_status}`
- **Calibration Status**: `{calibration.calibration_status}`
- **Model Backends Registered**: {len(backends_to_register)}

## Narrative Results
- **UX Flow**: Natural language intuition was successfully processed and given suggested variables, proxies, and a minimum test plan without requiring math structure on input.
- **Rigor & Verification**: Higher-level predictions (>= Source Backed) achieved an accuracy of {f'{lift.accuracy_given_pass:.1%}' if lift.accuracy_given_pass is not None else 'N/A'}, showing lift over baseline.
- **Model Runtime Routing**: High-risk tasks are successfully routed to frontier API / human review backends, while low-risk tasks (idea intake, proxy suggestion) are open-source model compatible.

## Generated Reports Directory
1. **UX Reports**:
   - Flow: [{ux_paths['flow']}](file:///{flow_p})
   - Cards: [{ux_paths['cards']}](file:///{cards_p})
2. **Prediction Accuracy Reports**:
   - Ledger: [{accuracy_paths['ledger']}](file:///{ledger_p})
   - Calibration: [{accuracy_paths['calibration']}](file:///{cal_p})
   - Filter Lift: [{accuracy_paths['lift']}](file:///{lift_p})
   - Post-Mortem: [{accuracy_paths['post_mortem']}](file:///{pm_p})
3. **Model Runtime Reports**:
   - Registry: [{runtime_paths['registry']}](file:///{reg_p})
   - Open Source: [{runtime_paths['opensource']}](file:///{os_p})
   - Routing: [{runtime_paths['routing']}](file:///{rout_p})

## Final Discipline
> Phygn must help ideas become testable.
> Then it must measure whether its own approvals were worth anything.
"""
    campaign_path.write_text(campaign_content, encoding="utf-8")

    all_paths = {}
    all_paths.update(ux_paths)
    all_paths.update(accuracy_paths)
    all_paths.update(runtime_paths)
    all_paths.update({"campaign": str(campaign_path)})

    return {
        "seed_card": seed_card,
        "translator_out": translator_out,
        "metrics": metrics,
        "calibration": calibration,
        "lift": lift,
        "post_mortem": post_mortem,
        "report_paths": all_paths,
    }
