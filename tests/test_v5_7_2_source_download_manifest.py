import json

from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_hash_computed_for_existing_local_file():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    verified = [record for record in result.source_manifest_records if record.file_verified]

    assert verified
    assert all(record.local_pdf_hash for record in verified)
    assert all(record.local_pdf_path for record in verified)


def test_no_fabricated_hashes_or_locations():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    unverified = [record for record in result.source_manifest_records if not record.file_verified]

    assert unverified
    assert all(record.local_pdf_hash is None for record in unverified)
    assert all(candidate.local_pdf_hash for candidate in result.location_candidates)
    assert all(candidate.page_number is not None for candidate in result.location_candidates)


def test_manifest_file_generated():
    run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    payload = json.loads(open("data/frontera_c/source_download/source_download_manifest_v5_7_2.json", encoding="utf-8").read())

    assert payload["source_count"] == 6
    assert payload["verified_source_object_count"] >= 1
