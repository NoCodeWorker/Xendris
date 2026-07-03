"""Markdown report contract audit."""

from __future__ import annotations

from pathlib import Path

from phyng.repository_audit.schemas import ReportAuditRecord


SECTION_PATTERNS = {
    "title": ["# "],
    "date": ["date", "generated"],
    "campaign_id": ["campaign_id", "campaign id", "campaign"],
    "inputs": ["input", "parameters"],
    "core_results": ["result", "summary", "status"],
    "gate_results": ["gate"],
    "allowed_claims": ["allowed claims"],
    "blocked_claims": ["blocked claims", "blocked"],
    "failure_conditions": ["failure condition", "kill criteria"],
    "next_actions": ["next action", "next task", "next steps"],
    "tests": ["tests", "pytest"],
}


def audit_reports(root: Path) -> list[ReportAuditRecord]:
    root = Path(root)
    records: list[ReportAuditRecord] = []
    for path in sorted((root / "reports").rglob("*.md")):
        rel = str(path.relative_to(root)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        values = {key: _has_pattern(text, lower, patterns) for key, patterns in SECTION_PATTERNS.items()}
        warnings = [
            f"Missing or unmapped report field: {key}"
            for key, present in values.items()
            if not present and key in {"title", "core_results", "blocked_claims", "next_actions"}
        ]
        records.append(ReportAuditRecord(path=rel, warnings=warnings, **values))
    return records


def _has_pattern(text: str, lower: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern == "# " and text.lstrip().startswith("# "):
            return True
        if pattern in lower:
            return True
    return False
