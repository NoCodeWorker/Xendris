"""Audit tests for status-only assertions that miss behavioral gates."""

from __future__ import annotations

import ast
from pathlib import Path

from phyng.full_suite_logic_audit.schemas import AuditIssue


BEHAVIOR_TERMS = (
    "blocked_claims",
    "allowed_claims",
    "ready_for_predictive_gain",
    "accepted",
    "rejected",
    "slot4",
    "slot_4",
    "predictive_gain",
    "source_hash",
    "provenance",
    "claim_impact",
    "canonical",
)


def audit_test_logic(root: str | Path = ".", test_paths: list[str] | None = None) -> tuple[list[AuditIssue], int]:
    repo_root = Path(root)
    paths = [repo_root / path for path in test_paths] if test_paths is not None else list((repo_root / "tests").glob("test_*.py"))
    issues: list[AuditIssue] = []
    scanned = 0
    for path in paths:
        if not path.exists():
            continue
        scanned += 1
        issues.extend(audit_test_file(path.read_text(encoding="utf-8"), path.relative_to(repo_root).as_posix() if path.is_absolute() else str(path)))
    return issues, scanned


def audit_test_file(source: str, path: str = "inline") -> list[AuditIssue]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    issues: list[AuditIssue] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        body_source = "\n".join(_node_text(stmt, source) for stmt in node.body).lower()
        status_asserts = body_source.count(".status") + body_source.count("['status']") + body_source.count('"status"')
        has_behavior_assert = any(term in body_source for term in BEHAVIOR_TERMS)
        if status_asserts and not has_behavior_assert:
            issues.append(
                AuditIssue(
                    issue_id=f"STATUS-ONLY-TEST-{node.name}",
                    severity="MEDIUM",
                    category="STATUS_ONLY_TEST",
                    path=path,
                    message=f"Test `{node.name}` appears to assert status without a behavioral or epistemic invariant.",
                    evidence=node.name,
                    remediation="Add assertions for blocked claims, provenance, counts, or gate behavior.",
                )
            )
    return issues


def _node_text(node: ast.AST, source: str) -> str:
    return ast.get_source_segment(source, node) or ""
