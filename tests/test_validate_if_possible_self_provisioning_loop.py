import json
from pathlib import Path

from phyng.campaigns.frontera_c_validate_if_possible_loop import run


def test_validate_if_possible_loop_writes_required_audit_artifacts():
    result = run(".")

    assert result["terminal_status"] == "HUMAN_REVIEW_REQUIRED"
    assert result["audit_records"] == 2
    assert Path("data/frontera_c/self_provisioning/self_provisioning_audit_log.json").exists()
    assert Path("data/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.json").exists()
    assert Path("reports/frontera_c/self_provisioning/self_provisioning_audit_log.md").exists()
    assert Path("docs/PHYGN_AUTONOMOUS_VALIDATE_IF_POSSIBLE_DECISION_REPORT.md").exists()


def test_self_provisioning_audit_records_candidate_construction_cycle():
    run(".")
    payload = json.loads(Path("data/frontera_c/self_provisioning/self_provisioning_audit_log.json").read_text(encoding="utf-8"))
    record = payload["records"][0]

    assert record["gate_name"] == "candidate_family_selection"
    assert record["missing_capability_type"] == "MISSING_CANDIDATE_FORMALIZATION"
    assert record["gate_retried"] is True
    assert record["tests_passed"] is True
    assert record["gate_status_after"] == "CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES"


def test_self_provisioning_audit_records_feature_recovery_cycle():
    run(".")
    payload = json.loads(Path("data/frontera_c/self_provisioning/self_provisioning_audit_log.json").read_text(encoding="utf-8"))
    record = payload["records"][1]

    assert record["cycle_id"] == "SELF-PROVISION-v5_9_1-002-FEATURE-RECOVERY"
    assert record["missing_capability_type"] == "MISSING_THEORY_FEATURES_OR_SHARED_CONDITION_AXIS"
    assert record["gate_retried"] is True
    assert record["blocker_removed"] is False
    assert record["gate_status_after"] == "CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES"


def test_validate_if_possible_loop_does_not_compute_forbidden_gates():
    run(".")
    report = Path("docs/PHYGN_AUTONOMOUS_VALIDATE_IF_POSSIBLE_DECISION_REPORT.md").read_text(encoding="utf-8")

    assert "PredictiveGain: `NOT_COMPUTED`" in report
    assert "negative controls result: `NOT_RUN`" in report
    assert "C-ablation result: `PLAN_SCREEN_RUN_NO_SELECTED_CANDIDATE`" in report
    assert "Frontera C is validated." in report
