from pathlib import Path

from phyng.campaigns.log_boundary_sensitivity_ablation import run_log_boundary_sensitivity_ablation_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_log_boundary_sensitivity_ablation_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "Ablation may change synthetic priority" in text
