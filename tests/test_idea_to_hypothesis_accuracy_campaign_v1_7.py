"""
Tests v1.7 — Idea-to-Hypothesis Accuracy & Model Campaign
"""

import pytest
import tempfile
from pathlib import Path
from phyng.campaigns.idea_to_hypothesis_accuracy_runtime import (
    run_idea_to_hypothesis_accuracy_campaign,
)


def test_campaign_runs_and_generates_reports():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_idea_to_hypothesis_accuracy_campaign(reports_dir=tmpdir)

        # Verify output keys
        assert "seed_card" in result
        assert "translator_out" in result
        assert "metrics" in result
        assert "calibration" in result
        assert "lift" in result
        assert "post_mortem" in result
        assert "report_paths" in result

        paths = result["report_paths"]
        # Verify 10 reports were generated
        expected_keys = [
            "flow", "cards",
            "ledger", "calibration", "lift", "post_mortem",
            "registry", "opensource", "routing",
            "campaign"
        ]
        for key in expected_keys:
            assert key in paths, f"Missing report path key: {key}"
            assert Path(paths[key]).exists(), f"Report file does not exist: {paths[key]}"
