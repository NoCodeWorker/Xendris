"""Validate-if-possible loop audit and terminal report."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.self_provisioning.feature_recovery import run_feature_recovery_attempt
from phyng.self_provisioning.schemas import SelfProvisioningAuditRecord


TEST_COMMAND = (
    ".\\.venv\\Scripts\\python.exe -m pytest -q "
    "tests/test_master_goal_frontera_c_decision.py "
    "tests/test_v5_9_candidate_family_registry.py "
    "tests/test_v5_9_candidate_feature_schema.py "
    "tests/test_v5_9_candidate_prediction_rules.py "
    "tests/test_v5_9_reality_contact_screen.py "
    "tests/test_v5_9_leakage_screen.py "
    "tests/test_v5_9_candidate_selection_decision.py "
    "tests/test_frontera_c_reality_contact_candidate_family_campaign.py"
)
TEST_COMMAND_WITH_FEATURE_RECOVERY = (
    TEST_COMMAND
    + " tests/test_self_provisioning_feature_recovery.py "
    + "tests/test_validate_if_possible_self_provisioning_loop.py"
)


def run_validate_if_possible_loop_campaign(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    decision = _load_json(repo_root / "data/frontera_c/candidates/candidate_selection_decision_v5_9.json")
    next_gate = _load_json(repo_root / "data/frontera_c/candidates/v5_9_next_gate_decision.json")
    quality = _load_json(repo_root / "data/frontera_c/master_goal/quality_v5_7_4_master.json")
    recovery = run_feature_recovery_attempt(repo_root)
    audit_records = [_build_candidate_construction_cycle(decision), _build_feature_recovery_cycle(decision, recovery)]
    terminal_status = _terminal_status(audit_records)
    outputs = _write_outputs(repo_root, audit_records, terminal_status)
    report = _write_report(repo_root, audit_records, decision, next_gate, quality, recovery, terminal_status)
    return {
        "terminal_status": terminal_status,
        "audit_records": len(audit_records),
        "accepted_ytrue_count": quality.get("total_accepted_ytrue_count"),
        "independent_source_count": quality.get("independent_source_count"),
        "benchmark_readiness": quality.get("benchmark_readiness"),
        "selected_candidate": decision.get("selected_candidate_family"),
        "outputs": outputs,
        "final_report": report,
    }


def _build_candidate_construction_cycle(decision: dict) -> SelfProvisioningAuditRecord:
    return SelfProvisioningAuditRecord(
        cycle_id="SELF-PROVISION-v5_9-001-CANDIDATE-CONSTRUCTION",
        phase="v5.9 reality-contact candidate-family construction",
        gate_name="candidate_family_selection",
        gate_status_before="NO_CANDIDATE_WITH_REALITY_CONTACT",
        blocker_id="MODEL_BLOCKER_CANDIDATE_FAMILY_SELECTION",
        blocker_type="MODEL_BLOCKER",
        missing_capability_type="MISSING_CANDIDATE_FORMALIZATION",
        proposed_improvement=(
            "Build candidate family registry, dataset introspection, feature schema, "
            "prediction-rule formalization, leakage screen, baseline/control/ablation "
            "screening, and selection decision."
        ),
        why_minimal=(
            "The blocker was not missing y_true or benchmark readiness; it was the lack "
            "of a formal candidate object that could be tested without leakage."
        ),
        files_created=[
            "phyng/candidates/dataset_introspection.py",
            "phyng/candidates/family_registry.py",
            "phyng/candidates/feature_schema.py",
            "phyng/candidates/prediction_rules.py",
            "phyng/candidates/leakage_screen.py",
            "phyng/candidates/reality_contact_screen.py",
            "phyng/candidates/selection_decision.py",
            "phyng/candidates/reports.py",
            "phyng/candidates/campaign.py",
            "phyng/campaigns/frontera_c_reality_contact_candidate_family.py",
            "docs/374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md",
        ],
        files_modified=["phyng/candidates/schemas.py", "phyng/core/status_mapping.py"],
        tests_added=[
            "tests/test_v5_9_candidate_family_registry.py",
            "tests/test_v5_9_candidate_feature_schema.py",
            "tests/test_v5_9_candidate_prediction_rules.py",
            "tests/test_v5_9_reality_contact_screen.py",
            "tests/test_v5_9_leakage_screen.py",
            "tests/test_v5_9_candidate_selection_decision.py",
            "tests/test_frontera_c_reality_contact_candidate_family_campaign.py",
        ],
        tests_run=[TEST_COMMAND],
        tests_passed=True,
        gate_retried=True,
        gate_status_after=decision.get("final_status", "UNKNOWN"),
        blocker_removed=bool(decision.get("passed_candidate_count", 0) > 0),
        next_action=(
            "Provide or derive non-leaking candidate features and a candidate-family "
            "prediction rule, or acquire new observable/source data. Do not compute "
            "PredictiveGain until a candidate passes v5.9."
        ),
        forbidden_actions_avoided=[
            "PredictiveGain computation",
            "benchmark scoring",
            "negative controls before candidate permission",
            "C-structure ablation before candidate permission",
            "LOG_BOUNDARY reactivation",
            "Frontera C validation claim",
        ],
        notes=[
            "Candidate construction capability was provisioned and the gate was retried.",
            "No candidate passed because required non-target features and debt-free C-structure rules are absent.",
            "This blocker is not internally removable without fabricating physical variables or theory.",
        ],
    )


def _build_feature_recovery_cycle(decision: dict, recovery: dict) -> SelfProvisioningAuditRecord:
    summary = recovery.get("summary", {})
    return SelfProvisioningAuditRecord(
        cycle_id="SELF-PROVISION-v5_9_1-002-FEATURE-RECOVERY",
        phase="v5.9.1 local source feature recovery attempt",
        gate_name="candidate_family_selection",
        gate_status_before=decision.get("final_status", "UNKNOWN"),
        blocker_id="MODEL_BLOCKER_MISSING_NON_LEAKING_FEATURES",
        blocker_type="MODEL_BLOCKER",
        missing_capability_type="MISSING_THEORY_FEATURES_OR_SHARED_CONDITION_AXIS",
        proposed_improvement=(
            "Search hash-verified local PDFs and accepted y_true condition fields for "
            "mass, operational scale, mechanism labels, and shared condition axes."
        ),
        why_minimal=(
            "This is the next internal step after candidate construction: recover only "
            "source-local feature hints before requesting human theory reformulation or "
            "new source acquisition."
        ),
        files_created=[
            "phyng/self_provisioning/feature_recovery.py",
            "data/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.json",
            "reports/frontera_c/self_provisioning/feature_recovery_attempt_v5_9_1.md",
        ],
        files_modified=[
            "phyng/self_provisioning/campaign.py",
            "docs/PHYGN_AUTONOMOUS_VALIDATE_IF_POSSIBLE_DECISION_REPORT.md",
        ],
        tests_added=["tests/test_self_provisioning_feature_recovery.py"],
        tests_run=[TEST_COMMAND_WITH_FEATURE_RECOVERY],
        tests_passed=True,
        gate_retried=True,
        gate_status_after=decision.get("final_status", "UNKNOWN"),
        blocker_removed=False,
        next_action=(
            "Human/theory input is now required: provide a non-ad-hoc operational scale "
            "rule, complete physical features, or a source-independent condition axis "
            "before v6.0/PredictiveGain can run."
        ),
        forbidden_actions_avoided=[
            "mass or scale fabrication",
            "text hint promotion to selected feature",
            "PredictiveGain computation",
            "benchmark scoring",
            "Frontera C validation claim",
        ],
        notes=[
            f"Mass text hints found: {summary.get('mass_feature_hints')}.",
            f"Operational-scale text hints found: {summary.get('operational_scale_hints')}.",
            f"Shared numeric condition axis available: {summary.get('shared_numeric_condition_axis_available')}.",
            "Recovered hints are not complete leak-free candidate features.",
            "The remaining blocker is not removable internally without fabricating a candidate rule or physical variables.",
        ],
    )


def _terminal_status(audit_records: list[SelfProvisioningAuditRecord]) -> str:
    if any(record.blocker_removed for record in audit_records):
        return "CANDIDATE_SELECTION_SELF_PROVISIONING_ADVANCED"
    return "HUMAN_REVIEW_REQUIRED"


def _write_outputs(root: Path, audit_records: list[SelfProvisioningAuditRecord], terminal_status: str) -> dict[str, str]:
    data_dir = root / "data" / "frontera_c" / "self_provisioning"
    report_dir = root / "reports" / "frontera_c" / "self_provisioning"
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = data_dir / "self_provisioning_audit_log.json"
    md_path = report_dir / "self_provisioning_audit_log.md"
    payload = {
        "terminal_status": terminal_status,
        "cycle_count": len(audit_records),
        "records": [record.model_dump() for record in audit_records],
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(_render_audit_markdown(audit_records, terminal_status), encoding="utf-8")
    return {
        "audit_json": json_path.relative_to(root).as_posix(),
        "audit_report": md_path.relative_to(root).as_posix(),
    }


def _render_audit_markdown(records: list[SelfProvisioningAuditRecord], terminal_status: str) -> str:
    lines = [
        "# Self-Provisioning Audit Log",
        "",
        f"Terminal status: `{terminal_status}`",
        f"Cycle count: `{len(records)}`",
        "",
    ]
    for record in records:
        lines.extend(
            [
                f"## {record.cycle_id}",
                "",
                f"- gate: `{record.gate_name}`",
                f"- blocker: `{record.blocker_type}`",
                f"- missing capability: `{record.missing_capability_type}`",
                f"- proposed improvement: {record.proposed_improvement}",
                f"- gate status before: `{record.gate_status_before}`",
                f"- gate status after: `{record.gate_status_after}`",
                f"- blocker removed: `{record.blocker_removed}`",
                f"- tests passed: `{record.tests_passed}`",
                f"- next action: {record.next_action}",
                "",
            ]
        )
    return "\n".join(lines)


def _write_report(
    root: Path,
    audit_records: list[SelfProvisioningAuditRecord],
    decision: dict,
    next_gate: dict,
    quality: dict,
    recovery: dict,
    terminal_status: str,
) -> str:
    path = root / "docs" / "PHYGN_AUTONOMOUS_VALIDATE_IF_POSSIBLE_DECISION_REPORT.md"
    capabilities = [
        "dataset introspection",
        "candidate family registry",
        "feature availability analysis",
        "candidate prediction rule formalization",
        "leakage screen",
        "baseline comparator screen",
        "control plan screen",
        "C-structure ablation plan screen",
        "candidate selection decision",
    ]
    lines = [
        "# Phygn Autonomous Validate-If-Possible Decision Report",
        "",
        "Date: 2026-07-02",
        "",
        f"Final terminal status: `{terminal_status}`",
        "Last completed gate: `v5.9.1 - local source feature recovery attempt`",
        "First failed gate: `candidate_family_selection`",
        f"Self-provisioning cycles used: `{len(audit_records)}`",
        f"Capabilities built: `{', '.join(capabilities)}`",
        f"accepted_ytrue_count: `{quality.get('total_accepted_ytrue_count')}`",
        f"independent_source_count: `{quality.get('independent_source_count')}`",
        f"benchmark readiness: `{quality.get('benchmark_readiness')}`",
        f"selected candidate: `{decision.get('selected_candidate_family')}`",
        f"prediction rule: `{decision.get('selected_rule_id')}`",
        "PredictiveGain: `NOT_COMPUTED`",
        "negative controls result: `NOT_RUN`",
        "leakage result: `SCREEN_RUN_NO_SELECTED_CANDIDATE`",
        "C-ablation result: `PLAN_SCREEN_RUN_NO_SELECTED_CANDIDATE`",
        "scientific debt status: `BLOCKS_CANDIDATE_SELECTION`",
        "",
        "## Gate Retry Result",
        "",
        f"- v5.9 final status: `{decision.get('final_status')}`",
        f"- passed candidate count: `{decision.get('passed_candidate_count')}`",
        f"- blocked by missing features: `{decision.get('blocked_by_missing_features_count')}`",
        f"- blocked by leakage: `{decision.get('blocked_by_leakage_count')}`",
        f"- blocked by scientific debt: `{decision.get('blocked_by_scientific_debt_count')}`",
        f"- allowed next phase: `{decision.get('allowed_next_phase')}`",
        f"- next gate flags: PredictiveGain computed=`{not next_gate.get('no_predictive_gain_computed', True)}`",
        "",
        "## Feature Recovery Cycle",
        "",
        f"- feature recovery status: `{recovery.get('status')}`",
        f"- total y_true records reviewed: `{recovery.get('summary', {}).get('total_records')}`",
        f"- mass text hints: `{recovery.get('summary', {}).get('mass_feature_hints')}`",
        f"- operational scale text hints: `{recovery.get('summary', {}).get('operational_scale_hints')}`",
        f"- shared numeric condition axis available: `{recovery.get('summary', {}).get('shared_numeric_condition_axis_available')}`",
        f"- C-coordinate candidate permitted: `{recovery.get('summary', {}).get('c_coordinate_candidate_permitted')}`",
        f"- source-agnostic candidate permitted: `{recovery.get('summary', {}).get('source_agnostic_candidate_permitted')}`",
        "",
        "## Allowed Claims",
        "",
        "- Candidate construction/self-provisioning was attempted.",
        "- Local source feature recovery was attempted.",
        "- Dataset threshold remains reached.",
        "- Candidate feature, leakage and selection screens were run.",
        "- No active candidate currently has reality contact under v5.9.",
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- PredictiveGain exists.",
        "- Any candidate family has physical support.",
        "- LOG_BOUNDARY is reactivated.",
        "- C-structure ablation survived.",
        "",
        "## Human Action Required",
        "",
        "Provide a non-leaking candidate-family prediction rule with required physical features, especially a non-ad-hoc operational scale rule and/or a shared source-independent condition axis. The current local PDFs can provide hints, but not a complete candidate feature set under the gate.",
        "",
        "## Experiment Required",
        "",
        "No new experiment is strictly designed here, but current candidate selection cannot advance without externally supplied theory/features or additional empirical observables.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path.relative_to(root).as_posix()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
