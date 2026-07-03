from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_observable_location_is_not_ytrue():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    assert result.location_candidates
    assert result.next_gate_decision["no_ytrue_extracted"] is True
    assert not any("y_true" in candidate.model_dump() for candidate in result.location_candidates)


def test_no_local_sources_blocks_observable_review(tmp_path):
    # This assertion checks the campaign gate output shape without fabricating a
    # source object in tests.
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    if result.verified_source_object_count == 0:
        assert result.status in {"TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES", "TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD"}
    else:
        assert all(candidate.local_pdf_path for candidate in result.location_candidates)
