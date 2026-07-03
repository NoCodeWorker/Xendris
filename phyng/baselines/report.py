"""
Phygn v0.8 — Baseline Report Generator

Generates:
  reports/rag/baseline_source_requirements.md
  reports/rag/baseline_literature_ingestion.md
  reports/rag/baseline_source_support_matrix.md
  reports/model_comparison/visibility_decay_baseline_readiness.md
"""

from __future__ import annotations

from pathlib import Path

from phyng.baselines.schemas import (
    BaselineReadinessResult,
    BaselineSourceRequirement,
    BaselineSourceSupport,
    VisibilityDecayBaselineSpec,
)


def write_baseline_source_requirements(
    requirements: list[BaselineSourceRequirement], root_dir: Path
) -> Path:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "baseline_source_requirements.md"

    lines = [
        "# Baseline Source Requirements",
        "",
        "Status: these requirements must be satisfied before the baseline can be upgraded from TOY_INTERNAL.",
        "",
        "| ID | Topic | Role | Trust Required | Status |",
        "|---|---|---|---|---|",
    ]
    for r in requirements:
        lines.append(
            f"| {r.requirement_id} | {r.topic} | {r.baseline_role} "
            f"| {r.required_trust_level} | {r.status} |"
        )
    lines += [
        "",
        "## Suggested Search Queries",
        "",
    ]
    for r in requirements:
        lines.append(f"### {r.requirement_id} — {r.topic}")
        for q in r.suggested_queries:
            lines.append(f"- {q}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_baseline_literature_ingestion(
    requirements: list[BaselineSourceRequirement], root_dir: Path
) -> Path:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "baseline_literature_ingestion.md"

    n_awaiting = sum(1 for r in requirements if r.status == "AWAITING_SOURCE_INGESTION")
    n_sourced = sum(1 for r in requirements if r.status == "SOURCED")

    lines = [
        "# Baseline Literature Ingestion Report",
        "",
        f"- Requirements awaiting source: {n_awaiting}",
        f"- Requirements sourced: {n_sourced}",
        "- No invented citations are present in this report.",
        "",
        "## Ingestion Rule",
        "Do not create a SourceRecord unless actual source data exists.",
        "Do not cherry-pick supporting evidence — contradicting evidence must also be reported.",
        "",
        "## Open Requirements",
        "",
    ]
    for r in requirements:
        if r.status == "AWAITING_SOURCE_INGESTION":
            lines.append(f"- **{r.requirement_id}** ({r.topic}): {r.reason}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_baseline_source_support_matrix(
    support_matrix: list[BaselineSourceSupport], root_dir: Path
) -> Path:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "baseline_source_support_matrix.md"

    lines = [
        "# Baseline Source Support Matrix",
        "",
        "| Source ID | Support Level | Trust Level | Note |",
        "|---|---|---|---|",
    ]
    if support_matrix:
        for s in support_matrix:
            lines.append(f"| {s.source_id} | {s.support_level} | {s.trust_level} | {s.note} |")
    else:
        lines.append("| — | AWAITING_SOURCE_INGESTION | — | No sources ingested yet. |")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_visibility_decay_readiness_report(
    spec: VisibilityDecayBaselineSpec,
    readiness: BaselineReadinessResult,
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "model_comparison"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "visibility_decay_baseline_readiness.md"

    allowed_str = "\n".join(f"- {c}" for c in readiness.allowed_claims) or "- None"
    blocked_str = "\n".join(f"- {c}" for c in readiness.blocked_claims) or "- None"
    missing_str = "\n".join(f"- {m}" for m in readiness.missing_requirements) or "- None"

    lines = [
        "# Visibility Decay Baseline — Readiness Report",
        "",
        "## Formula",
        f"$$\n{spec.formula}\n$$",
        "",
        "## Observable",
        f"- {spec.observable}",
        "",
        "## Parameter Status",
        f"- Gamma parameter: `{spec.gamma_parameter_name}`",
        f"- Gamma value: `{spec.gamma_value if spec.gamma_value is not None else 'UNDEFINED (PARAMETER_TOY)'}`",
        f"- Parameter status: **{readiness.parameter_status}**",
        "",
        "## Source Support",
        f"- Support status: **{readiness.support_status}**",
        f"- Sources linked: {len(spec.source_ids)}",
        "",
        "## Baseline Readiness",
        f"- Can be used as baseline: **{readiness.can_be_used_as_baseline}**",
        f"- Maximum claim level: **{readiness.max_claim_level}**",
        "",
        "## Missing Requirements",
        missing_str,
        "",
        "## Allowed Uses",
        "\n".join(f"- {u}" for u in spec.allowed_uses),
        "",
        "## Forbidden Uses",
        "\n".join(f"- {u}" for u in spec.forbidden_uses),
        "",
        "## Allowed Claims",
        allowed_str,
        "",
        "## Blocked Claims",
        blocked_str,
        "",
        "## Assumptions",
        "\n".join(f"- {a}" for a in spec.assumptions) if spec.assumptions else "- None",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
