"""
Tests v1.5 — Candidate vs Baseline Synthetic Benchmark Campaign

Tests:
    test_campaign_runs
    test_reports_generated
    test_candidate_physically_blocked_after_campaign
    test_campaign_returns_survival_status
"""

import pytest
from pathlib import Path
import tempfile

from phyng.campaigns.candidate_baseline_synthetic_benchmark import (
    run_candidate_baseline_synthetic_benchmark_campaign,
)


def test_campaign_runs():
    """Campaign must complete without exceptions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
    assert result is not None
    assert "benchmark_result" in result
    assert "alpha_sweep_rows" in result
    assert "candidate_survival" in result
    assert "report_paths" in result


def test_reports_generated():
    """All 5 required report files must be generated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
        report_paths = result["report_paths"]
        for key in ("benchmark", "candidate_benchmark", "alpha_sweep", "failure_report", "campaign"):
            assert key in report_paths
            assert Path(report_paths[key]).exists(), f"Missing report: {key}"


def test_campaign_returns_survival_status():
    """Campaign must return a non-empty candidate survival status."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
    assert isinstance(result["candidate_survival"], str)
    assert len(result["candidate_survival"]) > 0


def test_candidate_physically_blocked_after_campaign():
    """Blocked claims must include physical prediction language."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
    bench = result["benchmark_result"]
    blocked = " ".join(bench.blocked_claims)
    assert "Frontera C is validated" in blocked
    assert "PredictiveGain" in blocked


def test_campaign_alpha_sweep_rows_not_empty():
    """Alpha sweep must produce rows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
    assert len(result["alpha_sweep_rows"]) > 0


def test_campaign_default_undetectable():
    """Default candidate (alpha=1) must be undetectable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmpdir)
    bench = result["benchmark_result"]
    assert bench.detectability_status == "UNDETECTABLE_SYNTHETIC_DELTA"


def test_campaign_report_contains_blocked_claims(tmp_path):
    """Campaign markdown report must mention physical claims blocked."""
    result = run_candidate_baseline_synthetic_benchmark_campaign(reports_dir=tmp_path)
    campaign_md = Path(result["report_paths"]["campaign"]).read_text(encoding="utf-8")
    assert "BLOCKED" in campaign_md
