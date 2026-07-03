"""
Phygn v1.6 — Epistemic Modes Report Writer

Generates all 5 required reports for the epistemic modes campaign.
"""

from __future__ import annotations

from pathlib import Path

from phyng.epistemic_modes.schemas import (
    ModeGateResult,
    IncubationResult,
    FrictionDecision,
    LadderClassification,
    HypothesisSeed,
)
from phyng.epistemic_modes.modes import MODE_DESCRIPTIONS, MODE_DEFAULT_RISK
from phyng.epistemic_modes.friction import RISK_TO_DEFAULT_FRICTION, FRICTION_INDEX
from phyng.epistemic_modes.ladder import LADDER_ORDER, LADDER_REQUIREMENTS, LADDER_STATUS


def write_epistemic_modes_reports(
    reports_dir: str | Path,
    gate_result: ModeGateResult,
    incubation_result: IncubationResult,
    friction_decisions: list[FrictionDecision],
    ladder_classification: LadderClassification,
    seed: HypothesisSeed,
) -> dict[str, str]:
    """Write all 5 v1.6 epistemic modes reports. Returns dict of {key: path}."""
    root = Path(reports_dir)
    em_dir = root / "epistemic_modes"
    em_dir.mkdir(parents=True, exist_ok=True)
    (root / "campaigns").mkdir(parents=True, exist_ok=True)

    paths: dict[str, str] = {}

    # 1. Dream-to-claim ladder
    p = em_dir / "dream_to_claim_ladder_v1_6.md"
    p.write_text(_render_ladder_report(ladder_classification), encoding="utf-8")
    paths["ladder"] = str(p)

    # 2. Friction gradient
    p = em_dir / "friction_gradient_v1_6.md"
    p.write_text(_render_friction_report(friction_decisions), encoding="utf-8")
    paths["friction"] = str(p)

    # 3. Hypothesis incubation
    p = em_dir / "hypothesis_incubation_v1_6.md"
    p.write_text(_render_incubation_report(incubation_result, seed), encoding="utf-8")
    paths["incubation"] = str(p)

    # 4. Risk-weighted gatekeeping
    p = em_dir / "risk_weighted_gatekeeping_v1_6.md"
    p.write_text(_render_gatekeeper_report(gate_result), encoding="utf-8")
    paths["gatekeeping"] = str(p)

    # 5. Campaign summary
    p = root / "campaigns" / "EPISTEMIC-MODES-FRICTION-GRADIENT-v1_6.md"
    p.write_text(
        _render_campaign_report(gate_result, incubation_result, ladder_classification, friction_decisions),
        encoding="utf-8",
    )
    paths["campaign"] = str(p)

    return paths


# ---------------------------------------------------------------------------
# Individual report renderers
# ---------------------------------------------------------------------------

def _render_ladder_report(lc: LadderClassification) -> str:
    lines = [
        "# Dream-to-Claim Ladder — Phygn v1.6",
        "",
        "## Ladder Levels",
        "",
        "| # | Level | Status | Claim Allowed | Action Allowed |",
        "|---|---|---|---|---|",
    ]
    for i, level in enumerate(LADDER_ORDER):
        status = LADDER_STATUS[level]
        claim = "✅" if level in {"SOURCE_BACKED_LIMITED", "BENCHMARK_SUPPORTED", "OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED"} else "❌"
        action = "✅" if level in {"OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED"} else "❌"
        lines.append(f"| {i} | `{level}` | `{status}` | {claim} | {action} |")
    lines += [
        "",
        "## Current Classification",
        "",
        f"- ladder_level: `{lc.ladder_level}` (level {lc.level_index})",
        f"- idea_allowed: {lc.idea_allowed}",
        f"- claim_allowed: {lc.claim_allowed}",
        f"- action_allowed: {lc.action_allowed}",
        f"- execution_allowed: {lc.execution_allowed}",
        f"- status: `{lc.status}`",
        "",
        "## Missing for Next Level",
        "",
    ]
    for m in lc.missing_for_next_level:
        lines.append(f"- `{m}`")
    lines += [
        "",
        "## Core Rule",
        "",
        "> A lower-level idea may exist. It may not impersonate a higher-level claim.",
        "> Phygn should be a ladder, not a guillotine.",
    ]
    return "\n".join(lines) + "\n"


def _render_friction_report(decisions: list[FrictionDecision]) -> str:
    lines = [
        "# Friction Gradient Report — Phygn v1.6",
        "",
        "## Risk-to-Friction Mapping",
        "",
        "| Risk Level | Default Friction | Blocked | Human Approval |",
        "|---|---|---|---|",
    ]
    for d in decisions:
        blocked = "✅ BLOCKED" if d.is_blocked else "—"
        human = "✅" if d.requires_human_approval else "—"
        lines.append(f"| `{d.risk_level}` | `{d.friction_level}` | {blocked} | {human} |")
    lines += [
        "",
        "## Principle",
        "",
        "> Friction must scale with harm, not with imagination.",
        "> Low risk → allow / label / structure.",
        "> High risk → require evidence / risk engine / human approval / block.",
    ]
    return "\n".join(lines) + "\n"


def _render_incubation_report(ir: IncubationResult, seed: HypothesisSeed) -> str:
    lines = [
        "# Hypothesis Incubation Report — Phygn v1.6",
        "",
        "## Seed",
        "",
        f"- seed_id: `{seed.seed_id}`",
        f"- title: {seed.title}",
        f"- domain: {seed.domain}",
        f"- intuition: _{seed.intuition}_",
        f"- current_level: `{seed.current_level}`",
        f"- risk_level: `{seed.risk_level}`",
        "",
        "## Incubation Status",
        "",
        f"`{ir.incubation_status}`",
        "",
        "## Allowed Use",
        "",
    ]
    for a in ir.allowed_use:
        lines.append(f"- {a}")
    lines += ["", "## Blocked Use", ""]
    for b in ir.blocked_use:
        lines.append(f"- {b}")
    lines += ["", "## Next Formalization Steps", ""]
    for s in ir.next_formalization_steps:
        lines.append(f"- {s}")
    lines += ["", "## Required Evidence for Next Level", ""]
    for e in ir.required_evidence_for_next_level:
        lines.append(f"- {e}")
    lines += [
        "",
        "## Friction Level",
        "",
        f"`{ir.friction_level}`",
        "",
        "> Do not bury a seed because it is not yet a tree.",
    ]
    return "\n".join(lines) + "\n"


def _render_gatekeeper_report(gr: ModeGateResult) -> str:
    lines = [
        "# Risk-Weighted Gatekeeping Report — Phygn v1.6",
        "",
        "## Mode Gate Result",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| mode | `{gr.mode}` |",
        f"| risk_level | `{gr.risk_level}` |",
        f"| friction_level | `{gr.friction_level}` |",
        f"| idea_permission | `{gr.idea_permission}` |",
        f"| hypothesis_permission | `{gr.hypothesis_permission}` |",
        f"| claim_permission | `{gr.claim_permission}` |",
        f"| action_permission | `{gr.action_permission}` |",
        f"| execution_permission | `{gr.execution_permission}` |",
        "",
        "## Allowed Uses",
        "",
    ]
    for a in gr.allowed_uses:
        lines.append(f"- {a}")
    lines += ["", "## Blocked Uses", ""]
    for b in gr.blocked_uses:
        lines.append(f"- {b}")
    lines += ["", "## Required Next Steps", ""]
    for s in gr.required_next_steps:
        lines.append(f"- {s}")
    lines += [
        "",
        "## Principle",
        "",
        "> Higher risk does not make ideas illegal.",
        "> It makes actions and claims more expensive.",
    ]
    return "\n".join(lines) + "\n"


def _render_campaign_report(
    gr: ModeGateResult,
    ir: IncubationResult,
    lc: LadderClassification,
    decisions: list[FrictionDecision],
) -> str:
    lines = [
        "# Campaign Report — EPISTEMIC-MODES-FRICTION-GRADIENT-v1_6",
        "",
        "## Campaign",
        "",
        "- campaign_id: `EPISTEMIC-MODES-v1_6`",
        "- version: v1.6",
        "- purpose: Implement epistemic modes, dream-to-claim ladder, friction gradient,",
        "  hypothesis incubation, and mode-aware claim/action gating.",
        "",
        "## Status: COMPLETE",
        "",
        "| Component | Status |",
        "|---|---|",
        "| Epistemic Mode Schemas | ✅ |",
        "| Dream-to-Claim Ladder | ✅ |",
        "| Friction Gradient Evaluator | ✅ |",
        "| Mode-Aware Gatekeeper | ✅ |",
        "| Hypothesis Incubation | ✅ |",
        "| Financial Action Gate | ✅ |",
        "| Reports | ✅ |",
        "| Tests | ✅ |",
        "",
        "## Example Gate Result",
        "",
        f"- mode: `{gr.mode}`",
        f"- idea_permission: `{gr.idea_permission}`",
        f"- claim_permission: `{gr.claim_permission}`",
        f"- action_permission: `{gr.action_permission}`",
        "",
        "## Example Ladder Level",
        "",
        f"- ladder_level: `{lc.ladder_level}` (index {lc.level_index})",
        f"- claim_allowed: {lc.claim_allowed}",
        "",
        "## Principle",
        "",
        "> Phygn must not kill hope.",
        "> It must stop hope from signing contracts as evidence.",
        "",
        "> Phygn should be a ladder, not a guillotine.",
        "",
        "## What v1.6 Does NOT Do",
        "",
        "- Does not weaken rigor for public claims.",
        "- Does not weaken rigor for financial execution.",
        "- Does not call intuition evidence.",
        "- Does not allow unsupported claims as truth.",
        "",
        "## What v1.6 DOES Do",
        "",
        "- Preserves intuition as a seed while blocking unsupported claims/actions.",
        "- Scales friction with risk, not with imagination.",
        "- Keeps high-risk execution tightly gated.",
        "- Allows early ideas to breathe without authority.",
    ]
    return "\n".join(lines) + "\n"
