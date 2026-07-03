"""
Phygn v1.6 — Epistemic Modes & Friction Gradient Campaign

Orchestrates the full v1.6 epistemic modes demonstration:
    - Runs ladder classification on example inputs
    - Evaluates friction for all risk levels × modes
    - Incubates a default hypothesis seed
    - Evaluates mode gate for dream and claim modes
    - Evaluates financial action gate
    - Generates all 5 reports
"""

from __future__ import annotations

from pathlib import Path

from phyng.epistemic_modes.schemas import HypothesisSeed
from phyng.epistemic_modes.ladder import classify_ladder_level
from phyng.epistemic_modes.friction import evaluate_friction, RISK_TO_DEFAULT_FRICTION
from phyng.epistemic_modes.incubation import incubate_hypothesis
from phyng.epistemic_modes.gatekeeper import evaluate_mode_gate, evaluate_financial_action_gate
from phyng.epistemic_modes.report import write_epistemic_modes_reports

# Default example seed for the campaign
DEFAULT_SEED = HypothesisSeed(
    seed_id="SEED-FRONTERA-C-001",
    title="Frontera C modulates decoherence at boundary scale",
    intuition="Maybe C is a causal seam that appears as decoherence at the boundary length.",
    domain="quantum_decoherence",
    possible_observable="visibility_loss",
    analogy="Like surface tension at a phase boundary — invisible until measured at the right scale.",
    current_level="HYPOTHESIS_SEED",
    risk_level="RISK_1_INTERNAL_NOTE",
    known_unknowns=[
        "coupling constant alpha has no prior",
        "boundary scale L not uniquely defined",
        "no experimental dataset available",
    ],
    next_formalization_steps=[
        "Define candidate observable (visibility_loss).",
        "Set baseline model (exp decay).",
        "Declare failure condition.",
    ],
    forbidden_claims=[
        "Frontera C predicts decoherence.",
        "This is a validated physical effect.",
    ],
)


def run_epistemic_modes_friction_gradient_campaign(
    reports_dir: str | Path = "reports",
) -> dict:
    """
    Full v1.6 campaign:
        ladder → friction sweep → incubation → mode gate → financial gate → reports.

    Returns dict with all results and report_paths.
    """
    # 1. Ladder classification (example: early-stage dream input)
    ladder_result = classify_ladder_level(
        input_text="Maybe Frontera C modulates decoherence at boundary scale.",
        requested_use="dream",
        available_evidence=["candidate_phenomenon", "domain", "uncertainty_acknowledged"],
    )

    # 2. Friction decisions for all risk levels (using DREAM_MODE as example mode)
    friction_decisions = [
        evaluate_friction(risk, "DREAM_MODE")
        for risk in RISK_TO_DEFAULT_FRICTION.keys()
    ]

    # 3. Hypothesis incubation
    incubation_result = incubate_hypothesis(DEFAULT_SEED)

    # 4. Mode gate — DREAM_MODE (no source, no benchmark → idea allowed, claim blocked)
    dream_gate = evaluate_mode_gate(
        mode="DREAM_MODE",
        risk_level="RISK_0_PRIVATE_THOUGHT",
        ladder_level="DREAM",
        has_source=False,
        has_benchmark=False,
    )

    # 5. Financial action gate — example with missing fields
    financial_gate = evaluate_financial_action_gate(
        provided_fields={"asset": "BTC", "time_horizon": "1w"}  # intentionally incomplete
    )

    # 6. Write reports
    report_paths = write_epistemic_modes_reports(
        reports_dir=reports_dir,
        gate_result=dream_gate,
        incubation_result=incubation_result,
        friction_decisions=friction_decisions,
        ladder_classification=ladder_result,
        seed=DEFAULT_SEED,
    )

    return {
        "ladder_result": ladder_result,
        "friction_decisions": friction_decisions,
        "incubation_result": incubation_result,
        "dream_gate": dream_gate,
        "financial_gate": financial_gate,
        "report_paths": report_paths,
    }
