"""Phygn v2.1 canonical status mapping campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.evidence_levels import CanonicalEvidenceLevel
from phyng.core.permissions import CanonicalPermission
from phyng.core.report_contract import (
    append_canonical_status_section,
    build_report_contract,
    render_canonical_report_section,
)
from phyng.core.risk_levels import CanonicalRiskLevel
from phyng.core.status_mapping import STATUS_COMPATIBILITY_MAP
from phyng.core.support_levels import CanonicalSupportLevel


def run_canonical_status_mapping_campaign(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    reports_root = repo_root / "reports"
    core_dir = reports_root / "core"
    campaigns_dir = reports_root / "campaigns"
    core_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    report_paths = {
        "mapping": core_dir / "canonical_status_mapping_v2_1.md",
        "grammar": core_dir / "permission_grammar_v2_1.md",
        "aliases": core_dir / "compatibility_aliases_v2_1.md",
        "report_contract": core_dir / "report_contract_canonicalization_v2_1.md",
        "campaign": campaigns_dir / "CANONICAL-STATUS-MAPPING-v2_1.md",
    }

    report_paths["mapping"].write_text(_render_mapping_report(), encoding="utf-8")
    report_paths["grammar"].write_text(_render_grammar_report(), encoding="utf-8")
    report_paths["aliases"].write_text(_render_alias_report(), encoding="utf-8")
    report_paths["report_contract"].write_text(_render_report_contract_report(), encoding="utf-8")
    generated = {key: str(path) for key, path in report_paths.items()}
    report_paths["campaign"].write_text(_render_campaign_report(generated), encoding="utf-8")

    return {
        "campaign_id": "CANONICAL-STATUS-MAPPING-v2_1",
        "status": "COMPLETE_COMPATIBILITY_LAYER_NO_BEHAVIOR_CHANGE",
        "mapped_status_count": len(STATUS_COMPATIBILITY_MAP),
        "report_paths": generated,
    }


def _render_mapping_report() -> str:
    lines = [
        "# Canonical Status Mapping v2.1",
        "",
        "## Purpose",
        "",
        "Map domain-specific statuses to a shared permission grammar without replacing the original domain status.",
        "",
        "| Domain Status | Domain | Permission | Blocked Reasons | Evidence | Support | Risk |",
        "|---|---|---|---|---|---|---|",
    ]
    for status, record in sorted(STATUS_COMPATIBILITY_MAP.items()):
        reasons = ", ".join(reason.value for reason in record.blocked_reasons)
        risk = record.risk_level.value if record.risk_level else "None"
        lines.append(
            f"| `{status}` | `{record.domain}` | `{record.canonical_permission.value}` | `{reasons}` | "
            f"`{record.evidence_level.value}` | `{record.support_level.value}` | `{risk}` |"
        )
    lines.extend([
        "",
        "## Discipline Note",
        "",
        "Canonicalization must increase clarity without erasing domain meaning.",
    ])
    return "\n".join(lines) + "\n"


def _render_grammar_report() -> str:
    sections = [
        ("CanonicalPermission", [item.value for item in CanonicalPermission]),
        ("CanonicalBlockedReason", [item.value for item in CanonicalBlockedReason]),
        ("CanonicalEvidenceLevel", [item.value for item in CanonicalEvidenceLevel]),
        ("CanonicalSupportLevel", [item.value for item in CanonicalSupportLevel]),
        ("CanonicalRiskLevel", [item.value for item in CanonicalRiskLevel]),
    ]
    lines = [
        "# Permission Grammar v2.1",
        "",
        "## Core Rule",
        "",
        "A status can be domain-specific. A permission must be system-readable.",
        "",
    ]
    for title, values in sections:
        lines.extend([f"## {title}", ""])
        lines.extend(f"- `{value}`" for value in values)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_alias_report() -> str:
    lines = [
        "# Compatibility Aliases v2.1",
        "",
        "## Rule",
        "",
        "Compatibility first. Consolidation second. Renaming last.",
        "",
        "| Original Status | Canonical Permission | Alias Behavior |",
        "|---|---|---|",
    ]
    for status, record in sorted(STATUS_COMPATIBILITY_MAP.items()):
        lines.append(
            f"| `{status}` | `{record.canonical_permission.value}` | Original status is preserved and interpreted through `CanonicalStatusRecord`. |"
        )
    return "\n".join(lines) + "\n"


def _render_report_contract_report() -> str:
    contract = build_report_contract(
        title="Report Contract Canonicalization v2.1",
        campaign_id="CANONICAL-STATUS-MAPPING-v2_1",
        domain_status="COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE",
        tests_summary="v2.1 report contract tests verify canonical section rendering.",
        reports_generated=["reports/core/report_contract_canonicalization_v2_1.md"],
    )
    base = "\n".join([
        "# Report Contract Canonicalization v2.1",
        "",
        "## Purpose",
        "",
        "New reports can append a canonical status section without rewriting historical reports.",
        "",
        "## Required Canonical Fields",
        "",
        "- Domain Status",
        "- Canonical Permission",
        "- Blocked Reasons",
        "- Evidence Level",
        "- Support Level",
        "- Risk Level",
        "- Allowed Uses",
        "- Blocked Uses",
        "- Next Actions",
        "- Discipline Note",
    ])
    return append_canonical_status_section(base, contract)


def _render_campaign_report(report_paths: dict[str, str]) -> str:
    contract = build_report_contract(
        title="Canonical Status Mapping Campaign v2.1",
        campaign_id="CANONICAL-STATUS-MAPPING-v2_1",
        domain_status="COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE",
        reports_generated=list(report_paths.values()),
        tests_summary="tests/test_*_v2_1.py",
        next_actions=[
            "Use normalize_status for new gate reports.",
            "Add new domain statuses to STATUS_COMPATIBILITY_MAP before treating them as permissions.",
            "Do not rename public domain statuses without ADR and compatibility aliases.",
        ],
    )
    base = "\n".join([
        "# Campaign Report - CANONICAL-STATUS-MAPPING-v2_1",
        "",
        "- campaign_id: `CANONICAL-STATUS-MAPPING-v2_1`",
        "- status: `COMPLETE_COMPATIBILITY_LAYER_NO_BEHAVIOR_CHANGE`",
        f"- mapped_status_count: `{len(STATUS_COMPATIBILITY_MAP)}`",
        "",
        "## Core Results",
        "",
        "- Canonical permission grammar created.",
        "- Blocked reason registry created.",
        "- Evidence/support/risk levels created.",
        "- Status compatibility map created.",
        "- Normalization and report contract helpers created.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in report_paths.values()],
        "",
        "## Tests",
        "",
        "- `tests/test_canonical_permissions_v2_1.py`",
        "- `tests/test_status_compatibility_mapping_v2_1.py`",
        "- `tests/test_status_normalization_v2_1.py`",
        "- `tests/test_report_contract_canonicalization_v2_1.py`",
        "- `tests/test_canonical_status_mapping_campaign_v2_1.py`",
    ])
    return base + "\n\n" + render_canonical_report_section(contract)
