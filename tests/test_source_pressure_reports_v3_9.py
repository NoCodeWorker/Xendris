"""Tests for v3.9 source pressure reports."""

from __future__ import annotations

from pathlib import Path

from phyng.source_pressure_decision.campaign import run_phi_gradient_source_pressure_decision_campaign

from tests.test_source_pressure_loader_v3_9 import write_minimal_v3_9_inputs


def test_reports_include_canonical_section(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    for path_str in result.report_paths.values():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        content = report_path.read_text(encoding="utf-8")
        assert "## Canonical Status" in content, f"Missing canonical section in {path_str}"


def test_reports_generated_for_all_artifacts(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    expected_keys = ["decision", "extract_pressure_map", "slot_pressure_summary",
                     "benchmark_alignment", "contradiction_map", "recommendations", "campaign"]
    for key in expected_keys:
        assert key in result.report_paths, f"Missing report key: {key}"

    for path_str in result.report_paths.values():
        report_path = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        assert report_path.exists(), f"Missing report file: {path_str}"
