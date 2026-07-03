"""
Tests for reporting engine.
"""

import os
import tempfile

from phyng.reporting import (
    generate_mesoscopic_report,
    generate_quantum_channel_report,
    export_mesoscopic_json,
    export_mesoscopic_latex,
    export_quantum_channel_json,
    export_quantum_channel_latex,
)


def test_mesoscopic_report_generates_markdown(tmp_path):
    """Report generates valid Markdown with all required sections."""
    path = str(tmp_path / "test_report.md")
    report = generate_mesoscopic_report(output_path=path)

    assert isinstance(report, str)
    assert len(report) > 100

    # Required sections
    assert "## Inputs" in report
    assert "## Results" in report
    assert "## Classification" in report
    assert "## Interpretation" in report
    assert "## Limitations" in report
    assert "NEGATIVE_BOUND_TRACE" in report
    assert "Forbidden" in report


def test_mesoscopic_report_writes_file(tmp_path):
    """Report is written to disk."""
    path = str(tmp_path / "reports" / "mesoscopic.md")
    generate_mesoscopic_report(output_path=path)
    assert os.path.isfile(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "MESO-INT-001" in content


def test_mesoscopic_report_contains_case_id(tmp_path):
    path = str(tmp_path / "r.md")
    report = generate_mesoscopic_report(output_path=path)
    assert "MESO-INT-001" in report


def test_mesoscopic_report_contains_qb_values(tmp_path):
    path = str(tmp_path / "r.md")
    report = generate_mesoscopic_report(output_path=path)
    assert "Q (quantum weight)" in report
    assert "B (gravitational weight)" in report


def test_quantum_channel_report_generates_markdown(tmp_path):
    path = str(tmp_path / "qc_report.md")
    report = generate_quantum_channel_report(p=0.1, output_path=path)

    assert isinstance(report, str)
    assert "## Inputs" in report
    assert "## Distributions" in report
    assert "## Results" in report
    assert "DETECTABLE_TRACE" in report


def test_quantum_channel_report_null_trace(tmp_path):
    """p=0 → NULL_TRACE in report."""
    path = str(tmp_path / "qc_null.md")
    report = generate_quantum_channel_report(p=0.0, output_path=path)
    assert "NULL_TRACE" in report


def test_quantum_channel_report_writes_file(tmp_path):
    path = str(tmp_path / "reports" / "qc.md")
    generate_quantum_channel_report(p=0.5, output_path=path)
    assert os.path.isfile(path)


def test_quantum_channel_report_contains_limitations(tmp_path):
    path = str(tmp_path / "r.md")
    report = generate_quantum_channel_report(p=0.1, output_path=path)
    assert "## Limitations" in report


def test_export_mesoscopic_json(tmp_path):
    path = str(tmp_path / "reports" / "mesoscopic.json")
    json_str = export_mesoscopic_json(output_path=path)
    assert os.path.isfile(path)
    assert '"case_id": "MESO-INT-001"' in json_str


def test_export_mesoscopic_latex(tmp_path):
    path = str(tmp_path / "reports" / "mesoscopic.tex")
    latex_str = export_mesoscopic_latex(output_path=path)
    assert os.path.isfile(path)
    assert "\\begin{table}" in latex_str
    assert "mesoscopic" in latex_str


def test_export_quantum_channel_json(tmp_path):
    path = str(tmp_path / "reports" / "qc.json")
    json_str = export_quantum_channel_json(p=0.2, epsilon_exp=1e-5, output_path=path)
    assert os.path.isfile(path)
    assert '"p": 0.2' in json_str


def test_export_quantum_channel_latex(tmp_path):
    path = str(tmp_path / "reports" / "qc.tex")
    latex_str = export_quantum_channel_latex(p=0.2, epsilon_exp=1e-5, output_path=path)
    assert os.path.isfile(path)
    assert "\\begin{table}" in latex_str
    assert "0.2" in latex_str

