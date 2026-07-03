"""Test architecture audit."""

from __future__ import annotations

import ast
from pathlib import Path

from phyng.repository_audit.schemas import TestAuditRecord


def audit_tests(root: Path) -> list[TestAuditRecord]:
    root = Path(root)
    records: list[TestAuditRecord] = []
    for path in sorted((root / "tests").glob("test_*.py")):
        rel = str(path.relative_to(root)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(text)
        count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
        imports = _phyng_imports(tree)
        lower = text.lower()
        records.append(
            TestAuditRecord(
                path=rel,
                test_count_estimate=count,
                modules_covered=imports,
                campaign_tests="campaign" in lower,
                negative_tests=any(word in lower for word in ("blocked", "fail", "negative", "reject")),
                contract_tests=any(word in lower for word in ("contract", "schema", "status", "permission")),
                report_tests="report" in lower or ".md" in lower,
            )
        )
    return records


def _phyng_imports(tree: ast.Module) -> list[str]:
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("phyng."):
                    imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("phyng."):
            imports.add(node.module)
    return sorted(imports)
