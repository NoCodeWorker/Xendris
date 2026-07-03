import json

from phyng.dataset_expansion.observable_location_scan import scan_observable_locations
from phyng.dataset_expansion.source_pool import build_source_pool
from phyng.dataset_expansion.ytrue_extraction import build_ytrue_candidates, split_accepted_rejected


def test_context_conditions_are_not_ytrue():
    prior = json.load(open("data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json", encoding="utf-8"))["records"]
    candidates = build_ytrue_candidates(scan_observable_locations(build_source_pool(".")), build_source_pool("."), prior)
    accepted, _ = split_accepted_rejected(candidates)

    assert accepted
    assert all(item.variable_name == "visibility_fraction" for item in accepted)
    assert all("heating_power_W" in item.conditions for item in accepted)


def test_accepted_ytrue_requires_provenance():
    prior = json.load(open("data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json", encoding="utf-8"))["records"]
    accepted, _ = split_accepted_rejected(build_ytrue_candidates(scan_observable_locations(build_source_pool(".")), build_source_pool("."), prior))

    assert all(item.local_pdf_hash for item in accepted)
    assert all(item.page_number is not None for item in accepted)
    assert all(item.qc_status in {"PASS", "PASS_WITH_LIMITATIONS"} for item in accepted)
