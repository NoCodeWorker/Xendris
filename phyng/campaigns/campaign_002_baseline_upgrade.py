"""
Phygn v0.8 — CAMPAIGN-002 Baseline Physicalization

Upgrades CAMPAIGN-002 baseline from TOY_INTERNAL toward SOURCE_BACKED_LIMITED
or marks it BASELINE_REQUIRES_SOURCE if evidence is absent.

Candidate physical prediction remains BLOCKED regardless of baseline status.
"""

from __future__ import annotations

from pathlib import Path

from phyng.baselines.readiness import classify_baseline_readiness
from phyng.baselines.report import (
    write_baseline_literature_ingestion,
    write_baseline_source_requirements,
    write_baseline_source_support_matrix,
    write_visibility_decay_readiness_report,
)
from phyng.baselines.schemas import Campaign002BaselineUpgradeResult
from phyng.baselines.source_support import (
    build_baseline_source_requirements,
    build_source_support_matrix,
)
from phyng.baselines.visibility_decay import (
    build_visibility_decay_baseline,
    ensure_baseline_research_tasks,
)

_STILL_BLOCKED = [
    "Phygn predicts gravitational decoherence.",
    "Boundary C causes decoherence.",
    "SyntheticGain proves physical gain.",
    "The source-backed baseline validates the boundary-aware candidate.",
]

_NEXT_STEPS_TEMPLATE = [
    "Ingest a PRIMARY or HIGH trust source for the exponential visibility-decay formula.",
    "Provide a sourced value for Gamma_env to upgrade parameter status.",
    "Provide OBSERVABLE_SUPPORT and PARAMETER_SUPPORT to reach SOURCE_BACKED_READY.",
    "Implement CAMPAIGN-002 candidate source-backed hypothesis (not yet unlocked).",
    "Provide y_true from literature or experiment for PredictiveGain evaluation.",
]


def run_campaign_002_baseline_physicalization(
    root_dir: Path,
) -> Campaign002BaselineUpgradeResult:
    """
    Evaluate and upgrade the CAMPAIGN-002 baseline status.

    Steps:
      1. Build visibility-decay baseline spec (checks existing sources).
      2. Build source support matrix.
      3. Classify baseline readiness.
      4. Ensure ResearchTasks exist for missing categories.
      5. Generate all reports.
      6. Return upgrade result (candidate prediction remains blocked).
    """
    # 1. Build baseline spec from current source registry
    spec = build_visibility_decay_baseline(root_dir)

    # 2. Build source support matrix
    support_matrix = build_source_support_matrix(root_dir)

    # 3. Classify readiness
    readiness = classify_baseline_readiness(spec, support_matrix)

    # 4. Ensure research tasks exist for missing sources
    task_ids = ensure_baseline_research_tasks(root_dir)

    # 5. Write reports
    requirements = build_baseline_source_requirements()

    write_baseline_source_requirements(requirements, root_dir)
    write_baseline_literature_ingestion(requirements, root_dir)
    write_baseline_source_support_matrix(support_matrix, root_dir)
    readiness_report_path = write_visibility_decay_readiness_report(spec, readiness, root_dir)

    _write_physicalization_report(readiness, task_ids, root_dir)
    _write_source_backed_readiness_report(readiness, root_dir)

    # 6. Determine new baseline status and allowed new claims
    baseline_after = readiness.support_status
    allowed_new: list[str] = list(readiness.allowed_claims)

    return Campaign002BaselineUpgradeResult(
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        baseline_after=baseline_after,
        baseline_readiness=readiness.model_dump(),
        source_requirements=task_ids,
        source_support_matrix_path=str(
            root_dir / "reports" / "rag" / "baseline_source_support_matrix.md"
        ),
        updated_max_claim_level=readiness.max_claim_level,
        allowed_new_claims=allowed_new,
        still_blocked_claims=_STILL_BLOCKED,
        next_required_steps=_NEXT_STEPS_TEMPLATE,
    )


def _write_physicalization_report(readiness, task_ids: list[str], root_dir: Path) -> Path:
    report_dir = root_dir / "reports" / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "CAMPAIGN-002_baseline_physicalization.md"

    allowed_str = "\n".join(f"- {c}" for c in readiness.allowed_claims) or "- None"
    blocked_str = "\n".join(f"- {c}" for c in _STILL_BLOCKED)
    missing_str = "\n".join(f"- {m}" for m in readiness.missing_requirements) or "- None"

    lines = [
        "# CAMPAIGN-002 — Baseline Physicalization",
        "",
        "## Objective",
        "Upgrade baseline_status from TOY_INTERNAL to SOURCE_BACKED_LIMITED or mark BASELINE_REQUIRES_SOURCE.",
        "",
        "## Before v0.8",
        "- baseline_status = TOY_INTERNAL",
        "- candidate_status = HYPOTHETICAL_CANDIDATE",
        "- benchmark_status = SYNTHETIC_READY",
        "- can_claim_physical_prediction = False",
        "",
        "## Baseline After v0.8",
        f"- baseline_status = **{readiness.support_status}**",
        f"- max_claim_level = {readiness.max_claim_level}",
        f"- can_be_used_as_baseline = {readiness.can_be_used_as_baseline}",
        "",
        "## Baseline Readiness",
        f"- support_status: {readiness.support_status}",
        f"- parameter_status: {readiness.parameter_status}",
        "",
        "## Missing Requirements",
        missing_str,
        "",
        "## Allowed New Claims",
        allowed_str,
        "",
        "## Still Blocked",
        blocked_str,
        "",
        "## Next Required Steps",
        "- Ingest PRIMARY/HIGH trust source for V(t)=exp(-Gamma*t) formula.",
        "- Provide sourced Gamma_env value.",
        "- Complete OBSERVABLE_SUPPORT and PARAMETER_SUPPORT for SOURCE_BACKED_READY.",
        "- Provide y_true from experiment for PredictiveGain.",
        "",
        "## Open Research Tasks",
        *[f"- {tid}" for tid in task_ids],
        "",
        "## Final Principle",
        "Upgrading the baseline does not upgrade the candidate.",
        "Physical prediction remains blocked.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_source_backed_readiness_report(readiness, root_dir: Path) -> Path:
    report_dir = root_dir / "reports" / "model_comparison"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "source_backed_readiness.md"

    lines = [
        "# Source-Backed Readiness Report",
        "",
        f"- Baseline support status: **{readiness.support_status}**",
        f"- Parameter status: **{readiness.parameter_status}**",
        f"- Can be used as baseline: **{readiness.can_be_used_as_baseline}**",
        f"- Maximum claim level: **{readiness.max_claim_level}**",
        "",
        "## Candidate Status",
        "- candidate_status = HYPOTHETICAL_CANDIDATE (unchanged)",
        "- can_claim_physical_prediction = False (unchanged)",
        "",
        "## Why physical prediction remains blocked",
        "A source-backed baseline is a worthy opponent — not a validation of the candidate.",
        "PredictiveGain requires y_true, error metric, and a sourced candidate hypothesis.",
        "None of these have been provided. Physical prediction remains blocked.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
