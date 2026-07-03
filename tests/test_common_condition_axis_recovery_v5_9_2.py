import json
from pathlib import Path

from phyng.candidates.common_axis_recovery import run_common_condition_axis_recovery
from phyng.campaigns.frontera_c_common_condition_axis_recovery import run


def test_common_axis_recovery_detects_single_source_heating_axis():
    payload = run_common_condition_axis_recovery(".")
    axes = {axis["axis_name"]: axis for axis in payload["axis_records"]}
    groups = {group["axis_name"]: group for group in payload["candidate_groups"]}

    assert axes["heating_power_W"]["record_count"] == 4
    assert axes["heating_power_W"]["source_count"] == 1
    assert axes["heating_power_W"]["passes_common_numeric_axis_threshold"] is False
    assert groups["heating_power_W"]["axis_status"] == "AXIS_PROMISING_BUT_SINGLE_SOURCE"


def test_common_axis_recovery_blocks_v6_when_no_multi_source_numeric_axis():
    payload = run_common_condition_axis_recovery(".")
    decision = payload["decision"]

    assert decision["final_status"] == "COMMON_CONDITION_AXIS_BLOCKED_SINGLE_SOURCE_ONLY"
    assert decision["selected_axis"] is None
    assert decision["selected_candidate_family"] is None
    assert decision["v6_0_permitted"] is False
    assert decision["predictive_gain_permitted"] is False


def test_common_axis_recovery_does_not_use_forbidden_columns():
    payload = run_common_condition_axis_recovery(".")

    assert "target value used as feature" in payload["forbidden_actions_avoided"]
    for axis in payload["axis_records"]:
        assert axis["axis_name"] not in {"value_numeric", "original_value_text", "source_id", "local_pdf_hash"}
        assert axis["leakage_status"] == "PASS"


def test_common_axis_campaign_writes_artifacts():
    result = run(".")

    assert result["status"] == "COMMON_CONDITION_AXIS_BLOCKED_SINGLE_SOURCE_ONLY"
    for path in result["output_paths"].values():
        assert Path(path).exists()
    decision = json.loads(Path("data/frontera_c/candidates/common_condition_axis_next_gate_v5_9_2.json").read_text(encoding="utf-8"))
    assert decision["v6_0_permitted"] is False
