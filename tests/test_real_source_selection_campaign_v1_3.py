"""
Tests for phyng.campaigns.real_source_selection
"""

from pathlib import Path
from phyng.campaigns.real_source_selection import main as campaign_main

def test_reports_generated(tmp_path: Path):
    campaign_main(tmp_path)
    
    expected_reports = [
        "reports/rag/real_source_candidates_v1_3.md",
        "reports/rag/filled_manifest_draft_v1_3.md",
        "reports/rag/extract_targets_v1_3.md",
        "reports/prediction_pressure/positive_prediction_gate_v1_3.md",
        "reports/prediction_pressure/kill_pivot_criteria_v1_3.md",
        "reports/campaigns/REAL-SOURCE-SELECTION-v1_3.md",
    ]
    
    for r in expected_reports:
        p = tmp_path / r
        assert p.exists()
        
    # Check that sources/baseline/notes/extract_targets_v1_3.md was created
    assert (tmp_path / "sources" / "baseline" / "notes" / "extract_targets_v1_3.md").exists()
    # Check that sources/baseline/source_manifest_draft_v1_3.json was created
    assert (tmp_path / "sources" / "baseline" / "source_manifest_draft_v1_3.json").exists()
