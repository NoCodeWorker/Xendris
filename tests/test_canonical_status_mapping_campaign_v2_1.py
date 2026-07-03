from pathlib import Path

from phyng.campaigns.canonical_status_mapping import run_canonical_status_mapping_campaign


def test_campaign_generates_reports(tmp_path):
    result = run_canonical_status_mapping_campaign(tmp_path)

    assert result["status"] == "COMPLETE_COMPATIBILITY_LAYER_NO_BEHAVIOR_CHANGE"
    assert result["mapped_status_count"] >= 19
    for path in result["report_paths"].values():
        assert Path(path).exists()

    campaign_text = Path(result["report_paths"]["campaign"]).read_text(encoding="utf-8")
    assert "Canonical Permission" in campaign_text
    assert "COMPLETE_COMPATIBILITY_LAYER_NO_BEHAVIOR_CHANGE" in campaign_text
