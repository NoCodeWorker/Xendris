"""Generate Markdown reports for v4.0 scientific debt and resolution plan."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.scientific_debt.schemas import ScientificDebtObject, Slot4ResolutionPlan


def write_scientific_debt_reports(
    debt: ScientificDebtObject,
    plan: Slot4ResolutionPlan,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    debt_dir = root / "debts"
    debt_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "debt_object": debt_dir / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.md",
        "resolution_plan": debt_dir / "slot4_resolution_plan_v4_0.md",
    }

    paths["debt_object"].write_text(_canonical_debt(_render_debt(debt), debt), encoding="utf-8")
    paths["resolution_plan"].write_text(_canonical_plan(_render_plan(plan), plan), encoding="utf-8")

    return {key: str(path) for key, path in paths.items()}


def _canonical_debt(markdown: str, debt: ScientificDebtObject) -> str:
    contract = build_report_contract(
        title="Scientific Debt Object — SLOT_4 Gap",
        campaign_id="PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0",
        domain_status="PHI_GRADIENT_SLOT4_DEBT_OPEN_BLOCKING",
        domain="scientific_debt",
        reports_generated=[],
        next_actions=[
            "Pedernales manual review",
            "Targeted SLOT_4 source acquisition",
        ],
        discipline_note="Untracked scientific debt is fatal.",
    )
    return append_canonical_status_section(markdown, contract)


def _canonical_plan(markdown: str, plan: Slot4ResolutionPlan) -> str:
    contract = build_report_contract(
        title="SLOT_4 Debt Resolution Plan",
        campaign_id="PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0",
        domain_status="PHI_GRADIENT_SLOT4_DEBT_OPEN_BLOCKING",
        domain="scientific_debt",
        reports_generated=[],
        next_actions=[
            "Pedernales manual review",
            "Targeted SLOT_4 source acquisition",
        ],
        discipline_note="Do not let benchmark progress launder mechanism debt.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_debt(debt: ScientificDebtObject) -> str:
    return "\n".join([
        f"# Scientific Debt: `{debt.debt_id}`",
        "",
        f"- Title: **{debt.title}**",
        f"- Status: `{debt.status}`",
        f"- Severity: `{debt.severity}`",
        f"- Opened By: `{debt.opened_by}`",
        f"- Source Pressure Reference: `{debt.source_pressure_ref}`",
        f"- Review Frequency: `{debt.review_frequency}`",
        "",
        "## Evidence Gap",
        "",
        debt.evidence_gap,
        "",
        "## Current Findings",
        "",
        *[f"- {finding}" for finding in debt.current_findings],
        "",
        "## Prohibited Claims (BLOCKED)",
        "",
        *[f"- {claim}" for claim in debt.prohibited_claims],
        "",
        "## Allowed Work",
        "",
        *[f"- {work}" for work in debt.allowed_work],
        "",
        "## Resolution Conditions",
        "",
        *[f"- {cond}" for cond in debt.resolution_conditions],
    ]) + "\n"


def _render_plan(plan: Slot4ResolutionPlan) -> str:
    lines = [
        f"# Resolution Plan: `{plan.plan_id}`",
        "",
        f"- Target Debt: `{plan.debt_id}`",
        f"- Status: `{plan.status}`",
        "",
        "## Tasks",
        "",
    ]
    for t in plan.tasks:
        lines.extend([
            f"### {t.task_id}: {t.name}",
            "",
            f"- Description: {t.description}",
            f"- Status: `{t.status}`",
            f"- Owner: `{t.owner}`",
            "",
        ])
    return "\n".join(lines)
