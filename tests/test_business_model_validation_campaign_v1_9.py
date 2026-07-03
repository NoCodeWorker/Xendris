"""
Tests v1.9 — Business Model Validation Campaign Integration
"""

import pytest
import tempfile
from pathlib import Path
from phyng.campaigns.business_model_validation_gate import (
    run_business_model_validation_campaign,
)


def test_campaign_runs_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_business_model_validation_campaign(reports_dir=tmpdir)

        # Verify output keys
        assert "canvas" in result
        assert "wtp_test" in result
        assert "channel_test" in result
        assert "economics" in result
        assert "risk" in result
        assert "gate_result" in result
        assert "post_mortem" in result
        assert "report_paths" in result

        paths = result["report_paths"]
        # Verify 6 reports were generated (5 validation + 1 campaign)
        expected_keys = [
            "canvas", "wtp", "channel", "economics", "gate", "campaign"
        ]
        for key in expected_keys:
            assert key in paths, f"Missing report path key: {key}"
            assert Path(paths[key]).exists(), f"Report file does not exist: {paths[key]}"
