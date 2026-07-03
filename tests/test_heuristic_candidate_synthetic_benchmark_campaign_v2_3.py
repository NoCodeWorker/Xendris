from pathlib import Path

from phyng.campaigns.heuristic_candidate_synthetic_benchmark import (
    run_heuristic_candidate_synthetic_benchmark_campaign,
)


def test_campaign_generates_reports(tmp_path):
    result = run_heuristic_candidate_synthetic_benchmark_campaign(tmp_path)

    assert result.status == "SYNTHETIC_BENCHMARK_DESIGNED"
    assert result.candidate_spec.candidate_id == "HEUR-PHY-003"
    assert len(result.report_paths) == 5
    for path in result.report_paths.values():
        assert Path(path).exists()
