import json
from pathlib import Path

from phyng.self_provisioning.feature_recovery import run_feature_recovery_attempt


def test_feature_recovery_attempt_writes_artifacts_without_selecting_candidate():
    payload = run_feature_recovery_attempt(".")

    assert payload["status"] == "FEATURE_RECOVERY_ATTEMPTED_SELECTION_STILL_BLOCKED"
    assert Path("data/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.json").exists()
    assert Path("reports/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.md").exists()
    assert payload["summary"]["c_coordinate_candidate_permitted"] is False
    assert payload["summary"]["source_agnostic_candidate_permitted"] is False


def test_feature_recovery_keeps_operational_scale_and_mass_non_promoted():
    run_feature_recovery_attempt(".")
    payload = json.loads(Path("data/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.json").read_text(encoding="utf-8"))

    assert payload["summary"]["mass_feature_complete"] is False
    assert payload["summary"]["operational_scale_complete"] is False
    assert payload["summary"]["observable_mechanism_class_complete"] is False
    assert "text hint promotion to selected feature" in payload["forbidden_promotions_avoided"]


def test_feature_recovery_records_exact_blockers_for_main_families():
    payload = run_feature_recovery_attempt(".")

    assert "C_COORDINATE_RESPONSE" in payload["blocked_candidate_families"]
    assert "SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE" in payload["blocked_candidate_families"]
    assert any("operational_scale_L_m" in item for item in payload["blocked_candidate_families"]["C_COORDINATE_RESPONSE"])
