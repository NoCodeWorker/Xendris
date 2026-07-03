import json
from pathlib import Path

from phyng.candidates.heating_power_axis_expansion import run_heating_power_axis_expansion
from phyng.campaigns.frontera_c_heating_power_axis_expansion import run


def test_heating_power_expansion_preserves_existing_seed_records():
    payload = run_heating_power_axis_expansion(".")

    assert payload["axis_name"] == "heating_power_W"
    assert payload["record_count_before"] == 4
    assert payload["independent_source_count_before"] == 1
    assert all(record["record_status"] == "ACCEPTED_SEED_HEATING_POWER_YTRUE" for record in payload["existing_axis_records"])


def test_heating_power_expansion_does_not_promote_local_text_hits_to_ytrue():
    payload = run_heating_power_axis_expansion(".")

    assert payload["local_scan_records"]
    assert all(record["usable_as_new_ytrue"] is False for record in payload["local_scan_records"])
    assert "laser detection power reclassified as heating_power_W" in payload["forbidden_actions_avoided"]
    assert "local text hint accepted as y_true without strict QC" in payload["forbidden_actions_avoided"]


def test_heating_power_expansion_requires_independent_source_acquisition():
    payload = run_heating_power_axis_expansion(".")
    decision = payload["decision"]

    assert decision["final_status"] == "HEATING_POWER_AXIS_EXPANSION_REQUIRES_TARGETED_SOURCE_ACQUISITION"
    assert decision["new_accepted_ytrue_count"] == 0
    assert decision["accepted_heating_power_source_count"] == 1
    assert decision["v6_0_permitted"] is False
    assert decision["predictive_gain_permitted"] is False


def test_heating_power_expansion_creates_acquisition_task():
    payload = run_heating_power_axis_expansion(".")

    assert payload["acquisition_queue"]
    task = payload["acquisition_queue"][0]
    assert task["axis_name"] == "heating_power_W"
    assert task["status"] == "TARGETED_SOURCE_ACQUISITION_REQUIRED"
    assert "Must not be any of" in task["required_source_independence"]


def test_heating_power_campaign_writes_artifacts():
    result = run(".")

    assert result["status"] == "HEATING_POWER_AXIS_EXPANSION_REQUIRES_TARGETED_SOURCE_ACQUISITION"
    for path in result["output_paths"].values():
        assert Path(path).exists()
    decision = json.loads(Path("data/frontera_c/candidates/heating_power_axis_next_gate_v5_9_3.json").read_text(encoding="utf-8"))
    assert decision["v6_0_permitted"] is False
