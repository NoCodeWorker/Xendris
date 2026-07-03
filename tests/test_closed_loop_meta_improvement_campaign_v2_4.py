from pathlib import Path

from phyng.campaigns.closed_loop_meta_improvement import run_closed_loop_meta_improvement_campaign
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec, design_synthetic_benchmark


def test_reports_include_canonical_section(tmp_path):
    result = run_closed_loop_meta_improvement_campaign(tmp_path)
    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text


def test_reports_include_blocked_claims_or_actions(tmp_path):
    result = run_closed_loop_meta_improvement_campaign(tmp_path)
    combined = "\n".join(Path(path).read_text(encoding="utf-8") for path in result.report_paths.values())

    assert "Blocked Claims" in combined
    assert "Blocked Actions" in combined


def test_campaign_generates_reports(tmp_path):
    result = run_closed_loop_meta_improvement_campaign(tmp_path)

    assert result.status == "META_CHANGE_APPROVED_LOW_RISK"
    assert len(result.report_paths) == 6
    for path in result.report_paths.values():
        assert Path(path).exists()


def test_existing_v2_3_behavior_preserved():
    spec = create_log_boundary_candidate_spec()
    result = design_synthetic_benchmark(spec)

    assert result.status == "SYNTHETIC_BENCHMARK_DESIGNED"
    assert "Physical prediction" in " ".join(result.blocked_claims)
