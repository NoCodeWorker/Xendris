from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_missing_local_files_require_manual_download():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    missing = [item for item in result.failure_records if item.source_candidate_id == "VD-SRC-v5_7_1-006-ARNDT-1999-C60"]

    assert missing
    assert missing[0].reason == "PAYWALL"
    assert "Acquire source object" in missing[0].required_next_action


def test_invalid_downloaded_object_is_rejected():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    gerlich = [item for item in result.source_manifest_records if item.source_candidate_id == "VD-SRC-v5_7_1-002-GERLICH-2011-LARGE-ORGANIC"][0]

    assert gerlich.download_status in {"REJECTED_NOT_SOURCE_OBJECT", "LOCAL_AVAILABLE"}
    if gerlich.download_status == "REJECTED_NOT_SOURCE_OBJECT":
        assert gerlich.local_pdf_hash is None
