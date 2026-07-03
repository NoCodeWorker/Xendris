from __future__ import annotations

from pathlib import Path

from phyng.full_suite_logic_audit.campaign import run_phygn_full_suite_logic_audit_campaign
from phyng.full_suite_logic_audit.remediation import build_remediation_plan
from phyng.full_suite_logic_audit.schemas import AuditIssue


def test_remediation_plan_created_for_blockers() -> None:
    issue = AuditIssue(
        issue_id="B-1",
        severity="BLOCKER",
        category="CLAIM_LEAKAGE",
        path="x",
        message="blocked",
        remediation="fix it",
    )

    plan = build_remediation_plan([issue])

    assert plan.can_continue_pipeline is False
    assert plan.items[0].gate_effect == "STOP_PIPELINE"


def test_clean_fixture_can_continue_pipeline() -> None:
    plan = build_remediation_plan([])

    assert plan.can_continue_pipeline is True
    assert plan.gate_status == "CONTINUE"


def test_blocker_fixture_stops_pipeline() -> None:
    issue = AuditIssue(issue_id="B-1", severity="BLOCKER", category="X", path="x", message="m", remediation="r")

    plan = build_remediation_plan([issue])

    assert plan.can_continue_pipeline is False


def test_campaign_generates_required_outputs(tmp_path: Path) -> None:
    for rel in ("docs", "reports", "data", "tests", "phyng/core", "phyng/campaigns"):
        (tmp_path / rel).mkdir(parents=True)
    (tmp_path / "docs" / "ok.md").write_text("Allowed: audit performed.\n", encoding="utf-8")
    (tmp_path / "tests" / "test_ok.py").write_text(
        "def test_gate():\n    result = run()\n    assert result.status == 'OK'\n    assert result.blocked_claims\n",
        encoding="utf-8",
    )

    result = run_phygn_full_suite_logic_audit_campaign(tmp_path)

    assert result.output_paths["full_suite"] == "data/audits/phygn_full_suite_logic_audit_v4_4_1.json"
    assert (tmp_path / "reports/campaigns/PHYGN-FULL-SUITE-LOGIC-AUDIT-v4_4_1.md").exists()
    assert "Audit creates PredictiveGain." in result.blocked_claims


def test_physical_claims_remain_blocked() -> None:
    issue = AuditIssue(issue_id="B-1", severity="BLOCKER", category="X", path="x", message="m", remediation="r")
    plan = build_remediation_plan([issue])

    assert plan.can_continue_pipeline is False
