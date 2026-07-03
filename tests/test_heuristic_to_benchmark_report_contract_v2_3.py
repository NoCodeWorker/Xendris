from pathlib import Path

from phyng.campaigns.heuristic_candidate_synthetic_benchmark import (
    run_heuristic_candidate_synthetic_benchmark_campaign,
)


def test_reports_include_canonical_section(tmp_path):
    result = run_heuristic_candidate_synthetic_benchmark_campaign(tmp_path)
    for key in ("formalization", "design", "detectability", "contract", "campaign"):
        text = Path(result.report_paths[key]).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "Canonical Permission" in text


def test_reports_do_not_authorize_physical_claim(tmp_path):
    result = run_heuristic_candidate_synthetic_benchmark_campaign(tmp_path)
    campaign = Path(result.report_paths["campaign"]).read_text(encoding="utf-8")

    assert "LOG_BOUNDARY remains unsupported by sources/data" in campaign
    assert "LOG_BOUNDARY validates Frontera C" in campaign
