"""Report writers for the v2.0 repository audit."""

from __future__ import annotations

from pathlib import Path

from phyng.repository_audit.schemas import RepositoryAuditCampaignResult


def write_repository_audit_reports(result: RepositoryAuditCampaignResult, reports_dir: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_dir)
    audit_dir = root / "audit"
    campaigns_dir = root / "campaigns"
    audit_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "structure": audit_dir / "repository_structure_audit_v2_0.md",
        "ontology": audit_dir / "core_ontology_consistency_v2_0.md",
        "modules": audit_dir / "module_boundary_refactor_map_v2_0.md",
        "orchestration": audit_dir / "campaign_report_test_orchestration_v2_0.md",
        "recommendations": audit_dir / "refactor_recommendations_v2_0.md",
        "campaign": campaigns_dir / "REPOSITORY-ORCHESTRATION-AUDIT-v2_0.md",
    }

    paths["structure"].write_text(_render_structure(result), encoding="utf-8")
    paths["ontology"].write_text(_render_ontology(result), encoding="utf-8")
    paths["modules"].write_text(_render_modules(result), encoding="utf-8")
    paths["orchestration"].write_text(_render_orchestration(result), encoding="utf-8")
    paths["recommendations"].write_text(_render_recommendations(result), encoding="utf-8")
    result.report_paths = {key: str(path) for key, path in paths.items()}
    paths["campaign"].write_text(_render_campaign(result), encoding="utf-8")
    return result.report_paths


def _render_structure(result: RepositoryAuditCampaignResult) -> str:
    audit = result.repository_audit
    lines = [
        "# Repository Structure Audit v2.0",
        "",
        f"- root: `{audit.root}`",
        f"- packages: `{len(audit.packages)}`",
        f"- modules: `{len(audit.modules)}`",
        f"- tests: `{len(audit.tests)}`",
        f"- reports: `{len(audit.reports)}`",
        f"- campaigns: `{len(audit.campaigns)}`",
        f"- schemas: `{len(audit.schemas)}`",
        f"- enums_or_literals: `{len(audit.enums)}`",
        f"- status_strings: `{len(audit.status_strings)}`",
        "",
        "## Campaign Modules",
        "",
        *_bullets(audit.campaigns),
        "",
        "## Status Strings",
        "",
        *_bullets(audit.status_strings[:120]),
        "",
        "## Warnings",
        "",
        *_bullets(audit.warnings),
    ]
    return "\n".join(lines) + "\n"


def _render_ontology(result: RepositoryAuditCampaignResult) -> str:
    lines = [
        "# Core Ontology Consistency Audit v2.0",
        "",
        "| State family | Representation | Definitions | Tests | Warnings |",
        "|---|---|---|---|---|",
    ]
    for record in result.ontology_records:
        lines.append(
            f"| `{record.state_family}` | `{record.representation}` | {len(record.definitions)} | {len(record.tests)} | {_join(record.warnings)} |"
        )
    lines.extend([
        "",
        "## Mapping Table Candidates",
        "",
        "| Domain status | Canonical permission | Notes |",
        "|---|---|---|",
    ])
    for status in result.repository_audit.status_strings[:80]:
        permission = _permission_for_status(status)
        lines.append(f"| `{status}` | `{permission}` | Heuristic v2.0 audit mapping; review before canonicalization. |")
    return "\n".join(lines) + "\n"


def _render_modules(result: RepositoryAuditCampaignResult) -> str:
    lines = [
        "# Module Boundary and Refactor Map v2.0",
        "",
        "## Module Boundary Records",
        "",
        "| Module | Responsibility | Imports | Imported by | Schemas | Warnings |",
        "|---|---|---:|---:|---:|---|",
    ]
    for record in result.module_records:
        lines.append(
            f"| `{record.module}` | {record.responsibility_guess} | {len(record.imports)} | {len(record.imported_by)} | {len(record.defined_schemas)} | {_join(record.boundary_warnings)} |"
        )
    lines.extend([
        "",
        "## Dependency Warnings",
        "",
    ])
    warnings = []
    for dep in result.dependency_records:
        for warning in dep.cycle_warnings + dep.coupling_warnings + dep.boundary_warnings:
            warnings.append(f"`{dep.module}`: {warning}")
    lines.extend(_bullets(warnings))
    return "\n".join(lines) + "\n"


def _render_orchestration(result: RepositoryAuditCampaignResult) -> str:
    lines = [
        "# Campaign, Report and Test Orchestration Audit v2.0",
        "",
        "## Campaigns",
        "",
        "| Campaign ID | Entrypoint | Reports | Tests | Warnings |",
        "|---|---|---:|---:|---|",
    ]
    for record in result.campaign_records:
        lines.append(
            f"| `{record.campaign_id}` | `{record.entrypoint}` | {len(record.reports)} | {len(record.tests)} | {_join(record.warnings)} |"
        )
    lines.extend([
        "",
        "## Reports",
        "",
        "| Report | Title | Gate | Blocked claims | Next actions | Warnings |",
        "|---|---|---|---|---|---|",
    ])
    for record in result.report_records:
        lines.append(
            f"| `{record.path}` | {record.title} | {record.gate_results} | {record.blocked_claims} | {record.next_actions} | {_join(record.warnings)} |"
        )
    lines.extend([
        "",
        "## Tests",
        "",
        "| Test file | Count | Campaign | Contract | Report | Negative |",
        "|---|---:|---|---|---|---|",
    ])
    for record in result.test_records:
        lines.append(
            f"| `{record.path}` | {record.test_count_estimate} | {record.campaign_tests} | {record.contract_tests} | {record.report_tests} | {record.negative_tests} |"
        )
    return "\n".join(lines) + "\n"


def _render_recommendations(result: RepositoryAuditCampaignResult) -> str:
    lines = [
        "# Refactor Recommendations v2.0",
        "",
        "| Order | Risk | Human review | Behavior change | Title |",
        "|---:|---|---|---|---|",
    ]
    for rec in result.recommendations:
        lines.append(
            f"| {rec.suggested_order} | `{rec.risk_level}` | {rec.requires_human_review} | {rec.behavior_change_expected} | {rec.title} |"
        )
    lines.extend(["", "## Details", ""])
    for rec in result.recommendations:
        lines.extend([
            f"### {rec.suggested_order}. {rec.title}",
            "",
            rec.description,
            "",
            f"- affected_modules: `{', '.join(rec.affected_modules)}`",
            f"- expected_benefit: {rec.expected_benefit}",
            "",
        ])
    return "\n".join(lines) + "\n"


def _render_campaign(result: RepositoryAuditCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - REPOSITORY-ORCHESTRATION-AUDIT-v2_0",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- version: `{result.version}`",
        f"- status: `{result.status}`",
        "",
        "## Inputs",
        "",
        "- Repository root audit over `phyng/`, `tests/`, `reports/`, and `docs/`.",
        "",
        "## Core Results",
        "",
        f"- modules audited: `{len(result.module_records)}`",
        f"- state families audited: `{len(result.ontology_records)}`",
        f"- campaigns audited: `{len(result.campaign_records)}`",
        f"- reports audited: `{len(result.report_records)}`",
        f"- tests audited: `{len(result.test_records)}`",
        "",
        "## Gate Results",
        "",
        "- v2.0 made no behavior-changing refactors.",
        "- High-risk module moves and public API changes are blocked pending human review.",
        "",
        "## Allowed Claims",
        "",
        "- The repository now has a generated audit map for structure, ontology, module boundaries, orchestration, and refactor risk.",
        "",
        "## Blocked Claims",
        "",
        "- The audit does not prove semantic equivalence between duplicated statuses.",
        "- The audit does not authorize high-risk module moves.",
        "",
        "## Failure Conditions",
        "",
        "- Any future canonicalization that changes gate outputs must be treated as a separate reviewed migration.",
        "",
        "## Reports Generated",
        "",
        *_bullets(result.report_paths.values()),
        "",
        "## Tests",
        "",
        "- `tests/test_repository_structure_audit_v2_0.py`",
        "- `tests/test_core_ontology_audit_v2_0.py`",
        "- `tests/test_module_boundary_audit_v2_0.py`",
        "- `tests/test_campaign_report_test_audit_v2_0.py`",
        "- `tests/test_refactor_map_v2_0.py`",
        "- `tests/test_repository_orchestration_audit_campaign_v2_0.py`",
        "",
        "## Next Actions",
        "",
        "- Review canonical status mapping candidates.",
        "- Add compatibility aliases only after duplicate meaning is proven.",
        "- Create an ADR before any public API or module topology change.",
    ]) + "\n"


def _bullets(items) -> list[str]:
    values = list(items)
    if not values:
        return ["- None"]
    return [f"- `{item}`" for item in values]


def _join(items: list[str]) -> str:
    return "<br>".join(items) if items else "None"


def _permission_for_status(status: str) -> str:
    if "BLOCK" in status or "FAIL" in status or "UNDETECTABLE" in status:
        return "BLOCKED_OR_REVIEW_REQUIRED"
    if "ALLOW" in status or "PASS" in status or "VALIDATED" in status:
        return "LIMITED_ALLOWED"
    return "REVIEW_REQUIRED"
