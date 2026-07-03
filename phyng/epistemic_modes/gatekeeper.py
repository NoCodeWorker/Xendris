"""
Phygn v1.6 — Mode-Aware Gatekeeper

Evaluates idea / hypothesis / claim / action / execution permission
for a given (mode, risk_level, ladder_level) combination.

Also implements the Financial Action Gate.
"""

from __future__ import annotations

from phyng.epistemic_modes.schemas import (
    EpistemicMode,
    RiskLevel,
    FrictionLevel,
    GateStatus,
    ModeGateResult,
    FinancialActionGateResult,
)
from phyng.epistemic_modes.friction import evaluate_friction, FRICTION_INDEX
from phyng.epistemic_modes.modes import is_high_risk_mode

# ---------------------------------------------------------------------------
# Required fields for financial action gate (§10 of prompt)
# ---------------------------------------------------------------------------

FINANCIAL_ACTION_REQUIRED_FIELDS = [
    "asset",
    "time_horizon",
    "source_freshness",
    "entry_condition",
    "exit_condition",
    "invalidation",
    "risk_per_trade",
    "position_sizing",
    "benchmark",
    "post_mortem_plan",
]


def evaluate_mode_gate(
    mode: EpistemicMode,
    risk_level: RiskLevel,
    ladder_level: str = "DREAM",
    has_source: bool = False,
    has_benchmark: bool = False,
) -> ModeGateResult:
    """
    Evaluate permission for idea / hypothesis / claim / action / execution.

    The gate distinguishes five permission types:
        idea_permission
        hypothesis_permission
        claim_permission
        action_permission
        execution_permission

    Low-risk modes allow ideas freely. High-risk modes require evidence
    before claims or actions are permitted.
    """
    friction = evaluate_friction(risk_level, mode)
    friction_idx = FRICTION_INDEX[friction.friction_level]

    # ---------------------------------------------------------------------------
    # Idea permission: always allowed unless fully blocked
    # ---------------------------------------------------------------------------
    if friction.is_blocked:
        idea_perm: GateStatus = "EXECUTION_BLOCKED"
    else:
        idea_perm = "IDEA_ALLOWED"

    # ---------------------------------------------------------------------------
    # Hypothesis permission: allowed unless claim-level mode with no source
    # ---------------------------------------------------------------------------
    if is_high_risk_mode(mode) and not has_source:
        hyp_perm: GateStatus = "HYPOTHESIS_INCUBATING"
    elif is_high_risk_mode(mode) and has_source:
        hyp_perm = "HYPOTHESIS_TESTABLE"
    else:
        hyp_perm = "HYPOTHESIS_SEED"

    # ---------------------------------------------------------------------------
    # Claim permission: requires source (friction ≥ 4) and benchmark (friction ≥ 5)
    # ---------------------------------------------------------------------------
    if not has_source:
        claim_perm: GateStatus = "CLAIM_BLOCKED"
    elif not has_benchmark and friction_idx >= 5:
        claim_perm = "CLAIM_REQUIRES_EVIDENCE"
    elif has_source and has_benchmark:
        claim_perm = "CLAIM_ALLOWED_LIMITED"
    else:
        claim_perm = "CLAIM_REQUIRES_EVIDENCE"

    # ---------------------------------------------------------------------------
    # Action permission: requires friction ≥ 6 gates + human approval
    # ---------------------------------------------------------------------------
    if mode in ("FINANCIAL_ACTION_MODE", "AUTOMATED_EXECUTION_MODE"):
        if friction.requires_human_approval and (not has_source or not has_benchmark):
            action_perm: GateStatus = "ACTION_BLOCKED"
        elif friction.requires_human_approval:
            action_perm = "ACTION_REQUIRES_RISK_GATE"
        else:
            action_perm = "ACTION_BLOCKED"
    else:
        action_perm = "ACTION_REQUIRES_RISK_GATE" if has_source and has_benchmark else "ACTION_BLOCKED"

    # ---------------------------------------------------------------------------
    # Execution permission: only AUTOMATED_EXECUTION_MODE with full auth
    # ---------------------------------------------------------------------------
    if mode == "AUTOMATED_EXECUTION_MODE" and has_source and has_benchmark and not friction.is_blocked:
        exec_perm: GateStatus = "EXECUTION_ALLOWED_LIMITED"
    else:
        exec_perm = "EXECUTION_BLOCKED"

    # ---------------------------------------------------------------------------
    # Allowed / blocked uses
    # ---------------------------------------------------------------------------
    allowed_uses: list[str] = ["Record intuition.", "Add to incubation backlog."]
    blocked_uses: list[str] = []
    next_steps: list[str] = []

    if idea_perm == "IDEA_ALLOWED":
        allowed_uses.append("Explore freely as a hypothesis seed.")
    if claim_perm == "CLAIM_BLOCKED":
        blocked_uses.append("Public claim without source support.")
        next_steps.append("Obtain source backing before making claims.")
    if claim_perm == "CLAIM_REQUIRES_EVIDENCE":
        blocked_uses.append("Claim without benchmark.")
        next_steps.append("Run benchmark before claiming support.")
    if action_perm == "ACTION_BLOCKED":
        blocked_uses.append("Real-world or financial action.")
        next_steps.append("Complete risk gate and human review.")
    if exec_perm == "EXECUTION_BLOCKED":
        blocked_uses.append("Automated execution.")

    return ModeGateResult(
        mode=mode,
        risk_level=risk_level,
        friction_level=friction.friction_level,
        idea_permission=idea_perm,
        hypothesis_permission=hyp_perm,
        claim_permission=claim_perm,
        action_permission=action_perm,
        execution_permission=exec_perm,
        allowed_uses=allowed_uses,
        blocked_uses=blocked_uses,
        required_next_steps=next_steps,
    )


def evaluate_financial_action_gate(
    provided_fields: dict[str, str | None],
) -> FinancialActionGateResult:
    """
    Gate for financial action mode.

    Requires all 10 fields from FINANCIAL_ACTION_REQUIRED_FIELDS.
    If any are missing, ACTION_BLOCKED.
    The intuition may still be INTUITION_LOGGED.
    """
    missing = [
        field
        for field in FINANCIAL_ACTION_REQUIRED_FIELDS
        if not provided_fields.get(field)
    ]

    asset = provided_fields.get("asset")

    if missing:
        gate_notes = [
            "Financial action requires all 10 risk fields.",
            f"Missing: {', '.join(missing)}.",
            "Intuition may be logged privately but no action can proceed.",
        ]
        return FinancialActionGateResult(
            asset=asset,
            action_status="ACTION_BLOCKED",
            intuition_status="INTUITION_LOGGED",
            missing_fields=missing,
            gate_notes=gate_notes,
        )

    return FinancialActionGateResult(
        asset=asset,
        action_status="ACTION_REQUIRES_RISK_GATE",
        intuition_status="INTUITION_LOGGED",
        missing_fields=[],
        gate_notes=[
            "All required fields present.",
            "Proceed to human review before execution.",
        ],
    )
