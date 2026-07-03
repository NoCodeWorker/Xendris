"""
Tests v1.6 — Epistemic Modes Campaign

Tests:
    test_campaign_runs
    test_reports_generated
    test_early_ideas_allowed
    test_high_risk_claims_blocked
"""

import pytest
from pathlib import Path
import tempfile

from phyng.campaigns.epistemic_modes_friction_gradient import (
    run_epistemic_modes_friction_gradient_campaign,
)


def test_campaign_runs():
    """Campaign must complete without exceptions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    assert result is not None
    assert "ladder_result" in result
    assert "friction_decisions" in result
    assert "incubation_result" in result
    assert "dream_gate" in result
    assert "financial_gate" in result
    assert "report_paths" in result


def test_reports_generated():
    """All 5 required reports must be generated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
        paths = result["report_paths"]
        for key in ("ladder", "friction", "incubation", "gatekeeping", "campaign"):
            assert key in paths, f"Missing report key: {key}"
            assert Path(paths[key]).exists(), f"Missing report file: {key}"


def test_early_ideas_allowed():
    """Dream gate must allow idea_permission = IDEA_ALLOWED."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    dream_gate = result["dream_gate"]
    assert dream_gate.idea_permission == "IDEA_ALLOWED"


def test_high_risk_claims_blocked_in_dream_gate():
    """Dream gate without source must block claims."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    dream_gate = result["dream_gate"]
    assert dream_gate.claim_permission == "CLAIM_BLOCKED"


def test_financial_gate_blocks_incomplete_action():
    """Financial gate with incomplete fields must block action."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    fin_gate = result["financial_gate"]
    assert fin_gate.action_status == "ACTION_BLOCKED"
    assert fin_gate.intuition_status == "INTUITION_LOGGED"


def test_friction_decisions_cover_all_risk_levels():
    """Friction sweep must cover all 8 risk levels."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    assert len(result["friction_decisions"]) == 8


def test_campaign_report_mentions_ladder(tmp_path):
    """Campaign report must mention the ladder principle."""
    result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmp_path)
    campaign_md = Path(result["report_paths"]["campaign"]).read_text(encoding="utf-8")
    assert "ladder" in campaign_md.lower()


def test_incubation_result_has_seed_id():
    """Incubation result must reference the default seed ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = run_epistemic_modes_friction_gradient_campaign(reports_dir=tmpdir)
    assert result["incubation_result"].seed_id == "SEED-FRONTERA-C-001"
