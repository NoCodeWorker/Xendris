import json

from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_source_hash_registry_update_records_real_hashes_only():
    run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    payload = json.loads(open("data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json", encoding="utf-8").read())

    assert payload["hash_count"] >= 1
    for record in payload["records"]:
        if record["hash_status"] == "NO_LOCAL_FILE":
            assert record["sha256"] is None
        else:
            assert len(record["sha256"]) == 64
            assert record["file_size_bytes"] > 0
