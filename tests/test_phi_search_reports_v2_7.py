from pathlib import Path

from phyng.campaigns.log_boundary_non_saturating_phi_search import run_log_boundary_non_saturating_phi_search_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_log_boundary_non_saturating_phi_search_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "neither earns truth" in text
