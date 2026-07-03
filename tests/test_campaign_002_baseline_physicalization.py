"""
tests/test_campaign_002_baseline_physicalization.py

Tests for run_campaign_002_baseline_physicalization().
"""

import tempfile
from pathlib import Path

from phyng.campaigns.campaign_002_baseline_upgrade import (
    run_campaign_002_baseline_physicalization,
)


def test_campaign_002_baseline_requires_source_if_no_sources():
    """Without ingested sources, baseline should be BASELINE_REQUIRES_SOURCE."""
    with tempfile.TemporaryDirectory() as tmp:
        result = run_campaign_002_baseline_physicalization(Path(tmp))
        assert result.baseline_before == "TOY_INTERNAL"
        assert result.baseline_after == "BASELINE_REQUIRES_SOURCE"
        assert result.baseline_readiness["can_be_used_as_baseline"] is False


def test_baseline_upgrade_does_not_unlock_candidate_prediction():
    """candidate_status and physical prediction must remain blocked."""
    with tempfile.TemporaryDirectory() as tmp:
        result = run_campaign_002_baseline_physicalization(Path(tmp))
        blocked = " ".join(result.still_blocked_claims).lower()
        assert "predicts" in blocked or "boundary" in blocked or "candidate" in blocked


def test_source_backed_baseline_updates_readiness_report():
    """Reports must be written after physicalization."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_campaign_002_baseline_physicalization(root)
        assert (root / "reports" / "model_comparison" / "visibility_decay_baseline_readiness.md").exists()
        assert (root / "reports" / "campaigns" / "CAMPAIGN-002_baseline_physicalization.md").exists()
        assert (root / "reports" / "rag" / "baseline_source_requirements.md").exists()
        assert (root / "reports" / "rag" / "baseline_source_support_matrix.md").exists()
        assert (root / "reports" / "rag" / "baseline_literature_ingestion.md").exists()


def test_source_requirements_created():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_campaign_002_baseline_physicalization(Path(tmp))
        assert len(result.source_requirements) >= 4


def test_next_steps_are_non_empty():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_campaign_002_baseline_physicalization(Path(tmp))
        assert len(result.next_required_steps) > 0
