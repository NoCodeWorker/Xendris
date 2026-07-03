"""
Tests for phyng.campaigns.candidate_model_operationalization
"""

from pathlib import Path
from phyng.campaigns.candidate_model_operationalization import main as campaign_main

def test_reports_generated(tmp_path: Path):
    campaign_main(tmp_path)
    
    expected_reports = [
        "reports/candidates/candidate_term_families_v1_4.md",
        "reports/candidates/candidate_admissibility_v1_4.md",
        "reports/prediction_pressure/candidate_failure_conditions_v1_4.md",
        "reports/prediction_pressure/candidate_model_readiness_v1_4.md",
        "reports/campaigns/CANDIDATE-MODEL-OPERATIONALIZATION-v1_4.md",
    ]
    
    for r in expected_reports:
        p = tmp_path / r
        assert p.exists()
