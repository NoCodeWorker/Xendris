import tempfile
import math
from pathlib import Path
from phyng.campaigns.schemas import CampaignInput
from phyng.campaigns.mesoscopic_boundary_number import run_mesoscopic_boundary_campaign
from phyng.campaigns.campaign_runner import run_campaign
from phyng.campaigns.campaign_report import generate_campaign_reports
from phyng.rag.research_planner import list_research_tasks
from phyng.constants import planck_length


def test_mesoscopic_campaign_run_and_eval():
    campaign_in = CampaignInput(
        campaign_id="CAMPAIGN-001",
        system_id="SYS-MESO-TEST",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="separation scale",
        observer_channel="readout",
        justification="Verified by MAQRO proposal paper",
        allowed_range_m=(1e-8, 1e-6),
        arbitrariness_risk="LOW"
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        result = run_mesoscopic_boundary_campaign(campaign_in, tmp_path)
        
        # Verify result content
        assert result.campaign_id == "CAMPAIGN-001"
        assert result.atlas_region == "NEGATIVE_GRAVITY_BOUND"
        assert result.trace_type == "NEGATIVE_BOUND_TRACE"
        assert result.scale_status == "ACCEPTED"
        assert result.non_triviality_status == "NEGATIVE_NONTRIVIAL"
        
        # Required signature contract
        expected_keys = {
            "lambda_c",
            "r_g",
            "R_S",
            "Q",
            "B",
            "QB",
            "planck_ratio_squared",
            "delta_QB",
            "logQ",
            "logB",
            "u",
            "w",
        }
        assert expected_keys.issubset(result.signature)
        assert math.isclose(
            result.signature["QB"],
            (planck_length() / campaign_in.L_value_m) ** 2,
            rel_tol=1e-12,
        )
        assert abs(result.signature["delta_QB"]) < 1e-50
        
        # Blocked claim
        assert "Phygn predicts new gravitational decoherence." in result.blocked_claims
        
        # Allowed claim
        assert any("direct gravitational boundary ratio B = r_g/L is negligible." in c for c in result.allowed_claims)
        
        # Check generated research tasks
        tasks = list_research_tasks(tmp_path)
        assert len(tasks) > 0
        assert any(t.task_id == "RT-CAMPAIGN-001-SRC-CAT-001" for t in tasks)
        
        # Check report generation
        rep_path = generate_campaign_reports(campaign_in, result, tmp_path)
        assert rep_path.exists()
        assert (tmp_path / "reports" / "campaigns" / "CAMPAIGN-001_citation_audit.md").exists()


def test_campaign_runner_dispatches_campaign_001():
    campaign_in = CampaignInput(
        campaign_id="CAMPAIGN-001",
        system_id="SYS-MESO-RUNNER",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="interferometric path separation",
        observer_channel="matter-wave interference readout",
        justification="Campaign default scale.",
        allowed_range_m=(1e-8, 1e-6),
        arbitrariness_risk="LOW",
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = run_campaign("CAMPAIGN-001", campaign_in, Path(tmp_dir))

    assert result.system_id == "SYS-MESO-RUNNER"
    assert result.atlas_region == "NEGATIVE_GRAVITY_BOUND"


def test_campaign_report_uses_reviewed_scale_status():
    campaign_in = CampaignInput(
        campaign_id="CAMPAIGN-001",
        system_id="SYS-MESO-REJECTED-SCALE",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="interferometric path separation",
        observer_channel="matter-wave interference readout",
        justification="Outside the configured range by construction.",
        allowed_range_m=(1e-10, 1e-9),
        arbitrariness_risk="LOW",
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        result = run_mesoscopic_boundary_campaign(campaign_in, tmp_path)
        report_path = generate_campaign_reports(campaign_in, result, tmp_path)
        report = report_path.read_text(encoding="utf-8")

    assert result.scale_status == "REJECTED"
    assert "Review Status: **REJECTED**" in report
    assert "outside allowed range" in report
