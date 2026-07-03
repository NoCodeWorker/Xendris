from __future__ import annotations

import json
from pathlib import Path

from phyng.audit_remediation.campaign import run_phygn_audit_remediation_campaign
from phyng.audit_remediation.loader import REQUIRED_AUDIT_FILES


def test_no_ytrue_created(tmp_path: Path) -> None:
    write_minimal_audit(tmp_path)

    run_phygn_audit_remediation_campaign(tmp_path)

    assert not (tmp_path / "data/y_true").exists()


def test_no_predictive_gain_created(tmp_path: Path) -> None:
    write_minimal_audit(tmp_path)

    result = run_phygn_audit_remediation_campaign(tmp_path)

    assert result.continuation_gate is not None
    assert "Remediation creates PredictiveGain." in result.continuation_gate.blocked_claims


def test_slot4_debt_remains_open(tmp_path: Path) -> None:
    write_minimal_audit(tmp_path)

    result = run_phygn_audit_remediation_campaign(tmp_path)

    assert result.continuation_gate is not None
    assert "Remediation closes SLOT_4 debt." in result.continuation_gate.blocked_claims


def test_campaign_generates_remediation_outputs(tmp_path: Path) -> None:
    write_minimal_audit(tmp_path)

    result = run_phygn_audit_remediation_campaign(tmp_path)

    assert result.inputs_loaded is True
    assert result.output_paths["gate"] == "data/audits/remediation/phygn_v4_4_2_continuation_gate.json"
    assert (tmp_path / "reports/campaigns/PHYGN-AUDIT-REMEDIATION-v4_4_2.md").exists()


def write_minimal_audit(root: Path) -> None:
    payloads = {
        "full_suite": {"blocker_count": 0, "nonblocking_issue_count": 2},
        "status_permission": {
            "unmapped_statuses": ["PHI_GRADIENT_VALIDATED", "BENCHMARK_RANGE_CONTROL"],
            "issues": [
                {"evidence": "PHI_GRADIENT_VALIDATED"},
                {"evidence": "BENCHMARK_RANGE_CONTROL"},
            ],
        },
        "claim_leakage": {"issues": []},
        "test_logic": {
            "issues": [
                {
                    "path": "tests/test_model_comparison.py",
                    "message": "Test `test_status_only` appears to assert status.",
                    "category": "STATUS_ONLY_TEST",
                }
            ]
        },
        "debt_boundary": {"issues": [], "slot4_debt_open": True},
        "metric_integrity": {
            "predictive_gain_issues": [],
            "ytrue_issues": [],
            "source_support_issues": [],
            "negative_control_issues": [],
        },
        "remediation_plan": {"items": [], "gate_status": "CONDITIONAL_CONTINUE_AFTER_REVIEW"},
    }
    for key, rel_path in REQUIRED_AUDIT_FILES.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payloads[key]), encoding="utf-8")
