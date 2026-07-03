from pathlib import Path

from phyng.campaigns.heuristic_discovery_layer import run_heuristic_discovery_layer_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_heuristic_discovery_layer_campaign(tmp_path)
    pipeline_report = Path(result.report_paths["pipeline"]).read_text(encoding="utf-8")

    assert "## Canonical Status" in pipeline_report
    assert "Canonical Permission" in pipeline_report
    assert "Heuristics may guide search" in pipeline_report


def test_campaign_generates_reports(tmp_path):
    result = run_heuristic_discovery_layer_campaign(tmp_path)

    assert result.status == "HEURISTIC_TEST_DESIGN_READY"
    assert len(result.report_paths) == 6
    for path in result.report_paths.values():
        assert Path(path).exists()
