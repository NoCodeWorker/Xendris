"""
Tests v1.8 — Copilot Truth Boundary Campaign Integration
"""

import pytest
import tempfile
from pathlib import Path
from phyng.campaigns.copilot_truth_boundary_ui import (
    run_copilot_truth_boundary_campaign,
)


def test_reports_generated():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_copilot_truth_boundary_campaign(reports_dir=tmpdir)

        # Verify output keys
        assert "workspace" in result
        assert "next_question" in result
        assert "tb_eval" in result
        assert "orch_result" in result
        assert "response_contract" in result
        assert "report_paths" in result

        paths = result["report_paths"]
        # Verify 5 reports were generated
        expected_keys = [
            "ui", "socratic", "workspace", "orchestration", "campaign"
        ]
        for key in expected_keys:
            assert key in paths, f"Missing report path key: {key}"
            assert Path(paths[key]).exists(), f"Report file does not exist: {paths[key]}"
