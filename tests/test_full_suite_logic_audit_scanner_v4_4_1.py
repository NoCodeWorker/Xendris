from __future__ import annotations

from pathlib import Path

from phyng.full_suite_logic_audit.artifact_scanner import scan_artifacts


def test_scanner_collects_supported_artifacts(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.md").write_text("# Note\n", encoding="utf-8")
    (tmp_path / "docs" / "blob.pdf").write_text("pdf", encoding="utf-8")

    result = scan_artifacts(tmp_path, scope=["docs"])

    assert "docs/note.md" in result.scanned_paths
    assert "docs/blob.pdf" not in result.scanned_paths


def test_scanner_records_missing_scope(tmp_path: Path) -> None:
    result = scan_artifacts(tmp_path, scope=["missing_module"])

    assert result.missing_scope_paths == ["missing_module"]
