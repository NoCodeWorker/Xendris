from phyng.dataset_expansion.observable_location_scan import scan_observable_locations
from phyng.dataset_expansion.source_pool import build_source_pool


def test_location_scan_finds_observable_candidates():
    locations = scan_observable_locations(build_source_pool("."))

    assert locations
    assert any(item.classification == "OBSERVED_MEASUREMENT_CANDIDATE" for item in locations)
    assert any("REQUIRES_VISUAL_FIGURE_REVIEW" in item.extraction_blockers for item in locations)
