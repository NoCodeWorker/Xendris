"""SLOT_4 debt boundary audit."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.full_suite_logic_audit.claim_leakage_scanner import _is_blocking_context
from phyng.full_suite_logic_audit.schemas import ArtifactScanResult, AuditIssue


def is_slot4_debt_open(root: str | Path = ".") -> bool:
    repo_root = Path(root)
    candidates = [
        repo_root / "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        repo_root / "data/y_true/manual_extraction/phi_gradient_updated_y_true_dataset_v4_4.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        text = json.dumps(payload).lower()
        if "open_blocking" in text or "open_blocking_for_gradient_claims" in text or '"status": "open"' in text:
            return True
    return True


def audit_debt_boundary(root: str | Path, artifact_scan: ArtifactScanResult, slot4_open: bool | None = None) -> list[AuditIssue]:
    if slot4_open is None:
        slot4_open = is_slot4_debt_open(root)
    if not slot4_open:
        return []
    repo_root = Path(root)
    issues: list[AuditIssue] = []
    for artifact in artifact_scan.artifacts:
        if artifact.path.startswith("tests/"):
            continue
        path = repo_root / artifact.path
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line_number, line in enumerate(lines, start=1):
            lowered = line.lower()
            context = "\n".join(lines[max(0, line_number - 9): min(len(lines), line_number + 8)])
            if _is_blocking_context(context):
                continue
            if ("gradient mechanism" in lowered or "slot_4" in lowered or "slot4" in lowered) and any(term in lowered for term in ("supported", "resolved", "validated")):
                issues.append(slot4_bypass_issue(artifact.path, line_number, line))
    return issues


def slot4_bypass_issue(path: str, line_number: int, line: str) -> AuditIssue:
    return AuditIssue(
        issue_id=f"SLOT4-BYPASS-{abs(hash((path, line_number, line))) % 100000}",
        severity="BLOCKER",
        category="SLOT4_DEBT_BYPASS",
        path=path,
        message=f"SLOT_4 debt appears bypassed at line {line_number}.",
        evidence=line.strip()[:300],
        remediation="Keep gradient mechanism claims blocked until SLOT_4 debt is explicitly resolved by source-supported evidence.",
    )
