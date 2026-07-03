"""
Phygn v1.8 — Truth Boundary Evaluator

Checks the truth boundary status of any user input / model action.
Ensures we do not claim truth without epistemic support,
and distinguishes between lack of evidence, overclaim, and falsehood.
"""

from __future__ import annotations

from phyng.copilot.schemas import TruthBoundaryEvaluation, TruthBoundaryStatus


# Map ladder levels to inside boundaries
LADDER_BOUNDARY_MAP: dict[str, TruthBoundaryStatus] = {
    "DREAM":                        "INSIDE_DREAM_BOUNDARY",
    "HYPOTHESIS_SEED":              "INSIDE_HYPOTHESIS_BOUNDARY",
    "FORMALIZING_HYPOTHESIS":       "INSIDE_EXPLORATION_BOUNDARY",
    "TESTABLE_HYPOTHESIS":          "INSIDE_TESTABILITY_BOUNDARY",
    "SYNTHETIC_SUPPORT":            "INSIDE_SYNTHETIC_SUPPORT_BOUNDARY",
    "SOURCE_BACKED_LIMITED":        "INSIDE_SOURCE_BACKED_LIMITED_BOUNDARY",
    "BENCHMARK_SUPPORTED":          "INSIDE_BENCHMARK_SUPPORTED_BOUNDARY",
    "OPERATIONALLY_ACTIONABLE":     "INSIDE_BENCHMARK_SUPPORTED_BOUNDARY",
    "AUTOMATED_EXECUTION_ALLOWED":  "INSIDE_BENCHMARK_SUPPORTED_BOUNDARY",
}


def evaluate_truth_boundary(
    ladder_level: str,
    mode: str,
    risk_level: str,
    has_sources: bool = False,
    has_benchmark: bool = False,
    has_contradiction: bool = False,
    has_overclaim: bool = False,
    requests_action: bool = False,
    requests_execution: bool = False,
) -> TruthBoundaryEvaluation:
    """
    Check if the current state crosses any truth, action, or execution boundaries.
    """
    notes: list[str] = []
    is_valid = True

    # 1. Contradiction with evidence or internal constraints
    if has_contradiction:
        notes.append("Falsity detected: contradiction with evidence or constraints.")
        return TruthBoundaryEvaluation(
            status="CROSSED_FALSEHOOD_BOUNDARY",
            is_valid=False,
            allowed_uses=["Refine hypothesis", "Log failure in ledger"],
            blocked_uses=["Public claim", "Action", "Execution", "Validation"],
            evaluation_notes=notes
        )

    # 2. Claim stronger than evidence (overclaim)
    if has_overclaim:
        notes.append("Overclaim detected: statements go beyond available evidence.")
        return TruthBoundaryEvaluation(
            status="CROSSED_OVERCLAIM_BOUNDARY",
            is_valid=False,
            allowed_uses=["Internal research", "Hypothesis testing"],
            blocked_uses=["Public publication", "Action recommendation"],
            evaluation_notes=notes
        )

    # 3. Execution without full authorization
    if requests_execution and (ladder_level != "AUTOMATED_EXECUTION_ALLOWED" or not has_benchmark):
        notes.append("Execution blocked: automated execution requires complete authorization and benchmark support.")
        return TruthBoundaryEvaluation(
            status="OUTSIDE_EXECUTION_BOUNDARY",
            is_valid=False,
            allowed_uses=["Simulation", "Test run"],
            blocked_uses=["Automated trading", "Live execution"],
            evaluation_notes=notes
        )

    # 4. Action without operational authorization
    if requests_action and (ladder_level not in ("OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED") or not has_benchmark):
        notes.append("Action blocked: operational decisions require benchmark-supported or actionable status.")
        return TruthBoundaryEvaluation(
            status="OUTSIDE_ACTION_BOUNDARY",
            is_valid=False,
            allowed_uses=["Paper trading", "Risk assessment"],
            blocked_uses=["Real-world allocation", "Client recommendation"],
            evaluation_notes=notes
        )

    # 5. Unsupported public claim (lack of evidence != falsehood)
    if mode in ("CLAIM_MODE", "PUBLICATION_MODE") and not has_sources:
        notes.append("Claim blocked: public claims require source documentation.")
        return TruthBoundaryEvaluation(
            status="OUTSIDE_CLAIM_BOUNDARY",
            is_valid=False,
            allowed_uses=["Private exploration", "Hypothesis builder"],
            blocked_uses=["Scientific claim", "Fact statement"],
            evaluation_notes=notes
        )

    # 6. Default boundaries based on ladder levels
    status = LADDER_BOUNDARY_MAP.get(ladder_level, "INSIDE_DREAM_BOUNDARY")
    notes.append(f"State is inside the {status} boundary.")

    # Determine allowed/blocked uses based on standard ladder level mapping
    allowed = ["Private recording", "Hypothesis refinement"]
    blocked = ["Public publication", "Automated execution"]

    if ladder_level in ("BENCHMARK_SUPPORTED", "OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED"):
        allowed.extend(["Limited claim", "Operational recommendation"])
        blocked.remove("Public publication")

    if ladder_level == "AUTOMATED_EXECUTION_ALLOWED":
        allowed.append("Automated execution")
        blocked.remove("Automated execution")

    return TruthBoundaryEvaluation(
        status=status,
        is_valid=is_valid,
        allowed_uses=allowed,
        blocked_uses=blocked,
        evaluation_notes=notes
    )
