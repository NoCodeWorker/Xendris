"""Status-to-permission matrix audit."""

from __future__ import annotations

import re
from pathlib import Path

from phyng.core.status_mapping import STATUS_COMPATIBILITY_MAP, CanonicalStatusRecord
from phyng.full_suite_logic_audit.schemas import AuditIssue, StatusPermissionAuditResult, StatusPermissionMatrixEntry


STATUS_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+){2,}\b")


def build_status_permission_matrix(status_map: dict[str, CanonicalStatusRecord] | None = None) -> list[StatusPermissionMatrixEntry]:
    records = status_map or STATUS_COMPATIBILITY_MAP
    return [
        StatusPermissionMatrixEntry(
            domain_status=status,
            domain=record.domain,
            canonical_permission=record.canonical_permission.value,
            evidence_level=record.evidence_level.value,
            support_level=record.support_level.value,
            risk_level=record.risk_level.value if record.risk_level else None,
            mapped=True,
        )
        for status, record in sorted(records.items())
    ]


def audit_status_permission_matrix(
    observed_statuses: set[str] | None = None,
    status_map: dict[str, CanonicalStatusRecord] | None = None,
) -> StatusPermissionAuditResult:
    records = status_map or STATUS_COMPATIBILITY_MAP
    matrix = build_status_permission_matrix(records)
    unmapped = sorted((observed_statuses or set()) - set(records))
    issues = [
        AuditIssue(
            issue_id=f"UNMAPPED-STATUS-{status}",
            severity="HIGH",
            category="UNMAPPED_STATUS",
            path="status_permission_matrix",
            message=f"Observed status `{status}` has no canonical permission mapping.",
            evidence=status,
            remediation="Add a conservative canonical status mapping before using this status in reports.",
        )
        for status in unmapped
    ]
    return StatusPermissionAuditResult(entries=matrix, unmapped_statuses=unmapped, issues=issues)


def extract_observed_statuses(root: str | Path, paths: list[str]) -> set[str]:
    repo_root = Path(root)
    tokens: set[str] = set()
    prefixes = (
        "PHI_",
        "PHYGN_",
        "LOG_",
        "HEURISTIC_",
        "SYNTHETIC_",
        "BUSINESS_",
        "SOURCE_",
        "BENCHMARK_",
        "FAIL_",
        "DETECTABLE_",
        "UNDETECTABLE_",
        "ACTION_",
        "UNIT_",
        "WTP_",
    )
    for rel in paths:
        path = repo_root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except FileNotFoundError:
            continue
        for token in STATUS_TOKEN_RE.findall(text):
            if token.startswith(prefixes):
                tokens.add(token)
    return tokens
