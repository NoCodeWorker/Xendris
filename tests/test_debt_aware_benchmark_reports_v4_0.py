"""Tests for v4.0 debt-aware benchmark reports."""

from __future__ import annotations

from pathlib import Path

from phyng.campaigns.phi_gradient_debt_aware_benchmark import run_phi_gradient_debt_aware_benchmark_campaign

from tests.test_debt_aware_benchmark_loader_v4_0 import write_minimal_v4_0_inputs


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    write_minimal_v4_0_inputs(tmp_path)
    res = run_phi_gradient_debt_aware_benchmark_campaign(tmp_path)

    report_paths = res["report_paths"]
    assert len(report_paths) >= 6

    for key, path_str in report_paths.items():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        content = report_path.read_text(encoding="utf-8")
        assert "## Canonical Status" in content, f"Missing canonical section in {key} report: {path_str}"
