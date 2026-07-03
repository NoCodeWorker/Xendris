from pathlib import Path

from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_reports_generated():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    expected = [
        "data/frontera_c/source_download/source_download_manifest_v5_7_2.json",
        "data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json",
        "data/frontera_c/source_download/source_download_failures_v5_7_2.json",
        "data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json",
        "data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json",
        "data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json",
        "data/frontera_c/observable_location/v5_7_2_next_gate_decision.json",
        "reports/frontera_c/source_download/source_download_manifest_v5_7_2.md",
        "reports/frontera_c/source_download/source_hash_registry_update_v5_7_2.md",
        "reports/frontera_c/source_download/source_download_failures_v5_7_2.md",
        "reports/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.md",
        "reports/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.md",
        "reports/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.md",
        "reports/frontera_c/observable_location/v5_7_2_next_gate_decision.md",
        "reports/campaigns/FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2.md",
        "docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md",
    ]

    assert result.status in {
        "TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_COMPLETED",
        "TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND",
        "TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD",
        "TARGETED_SOURCE_DOWNLOAD_REQUIRES_HUMAN_FIGURE_REVIEW",
        "TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES",
        "TARGETED_OBSERVABLE_LOCATION_BLOCKED_NO_OBSERVED_MEASUREMENTS",
        "TARGETED_OBSERVABLE_LOCATION_REQUIRES_SUPPLEMENTARY_DATA",
        "FRONTERA_C_BLOCKED_NO_OBSERVABLE_LOCATION",
    }
    assert all(Path(path).exists() for path in expected)


def test_no_ytrue_extracted():
    run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    assert not Path("data/frontera_c/ytrue/targeted_ytrue_v5_7_2.json").exists()
