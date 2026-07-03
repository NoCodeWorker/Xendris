from __future__ import annotations

from pathlib import Path

from phyng.full_suite_logic_audit.artifact_scanner import scan_artifacts
from phyng.full_suite_logic_audit.debt_boundary_audit import audit_debt_boundary


def test_debt_boundary_detects_slot4_bypass(tmp_path: Path) -> None:
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "bad.md").write_text("The gradient mechanism is supported and SLOT4 is resolved.\n", encoding="utf-8")
    scan = scan_artifacts(tmp_path, scope=["reports"])

    issues = audit_debt_boundary(tmp_path, scan, slot4_open=True)

    assert any(issue.category == "SLOT4_DEBT_BYPASS" for issue in issues)


def test_debt_boundary_ignores_blocked_context(tmp_path: Path) -> None:
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "ok.md").write_text("Blocked claims: gradient mechanism is supported and SLOT4 is resolved.\n", encoding="utf-8")
    scan = scan_artifacts(tmp_path, scope=["reports"])

    issues = audit_debt_boundary(tmp_path, scan, slot4_open=True)

    assert issues == []
