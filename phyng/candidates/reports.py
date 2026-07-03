"""Reports for v5.9 reality-contact candidate-family screening."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.candidates.schemas import CandidateSelectionDecision


def write_candidate_reports(result: dict, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "candidates"
    campaign_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    decision: CandidateSelectionDecision = result["decision"]
    paths = {
        "registry": report_dir / "candidate_family_registry_v5_9.md",
        "features": report_dir / "candidate_feature_schema_v5_9.md",
        "rules": report_dir / "candidate_prediction_rules_v5_9.md",
        "reality": report_dir / "candidate_reality_contact_screen_v5_9.md",
        "leakage": report_dir / "candidate_leakage_screen_v5_9.md",
        "decision": report_dir / "candidate_selection_decision_v5_9.md",
        "campaign": campaign_dir / "FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9.md",
    }
    paths["registry"].write_text(_canonical(_render_registry(result), decision), encoding="utf-8")
    paths["features"].write_text(_canonical(_render_features(result), decision), encoding="utf-8")
    paths["rules"].write_text(_canonical(_render_rules(result), decision), encoding="utf-8")
    paths["reality"].write_text(_canonical(_render_reality(result), decision), encoding="utf-8")
    paths["leakage"].write_text(_canonical(_render_leakage(result), decision), encoding="utf-8")
    paths["decision"].write_text(_canonical(_render_decision(decision), decision), encoding="utf-8")
    paths["campaign"].write_text(_canonical(_render_campaign(result), decision), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _canonical(markdown: str, decision: CandidateSelectionDecision) -> str:
    contract = build_report_contract(
        title="Reality-Contact Candidate Family Construction v5.9",
        campaign_id="FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9",
        domain_status=decision.final_status,
        domain="candidate_family_selection",
        next_actions=[decision.allowed_next_phase or "Resolve candidate feature/theory blockers."],
        discipline_note="Selection is permission to test. Nothing more.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_registry(result: dict) -> str:
    lines = ["# Candidate Family Registry v5.9", "", f"- candidate_count: `{len(result['families'])}`", ""]
    for item in result["families"]:
        lines.append(f"- `{item.candidate_family_id}`: type=`{item.candidate_type}`, role=`{item.allowed_role}`")
    return "\n".join(lines) + "\n"


def _render_features(result: dict) -> str:
    schema = result["feature_schema"]
    lines = ["# Candidate Feature Schema v5.9", "", f"- dataset_id: `{schema.dataset_id}`", f"- target_variable: `{schema.target_variable}`", ""]
    lines.append(f"- allowed_feature_columns: `{', '.join(schema.allowed_feature_columns)}`")
    lines.append(f"- forbidden_feature_columns: `{', '.join(schema.forbidden_feature_columns)}`")
    return "\n".join(lines) + "\n"


def _render_rules(result: dict) -> str:
    lines = ["# Candidate Prediction Rules v5.9", "", f"- rule_count: `{len(result['rules'])}`", ""]
    for item in result["rules"]:
        lines.append(f"- `{item.rule_id}`: status=`{item.rule_status}`, leakage=`{item.leakage_risk}`")
    return "\n".join(lines) + "\n"


def _render_reality(result: dict) -> str:
    lines = ["# Candidate Reality Contact Screen v5.9", "", f"- screen_count: `{len(result['screen'])}`", ""]
    for item in result["screen"]:
        lines.append(f"- `{item.candidate_family_id}`: passed=`{item.reality_contact_passed}`, failures=`{', '.join(item.failure_reasons)}`")
    return "\n".join(lines) + "\n"


def _render_leakage(result: dict) -> str:
    lines = ["# Candidate Leakage Screen v5.9", "", f"- leakage_record_count: `{len(result['leakage'])}`", ""]
    for item in result["leakage"]:
        lines.append(f"- `{item.candidate_family_id}`: status=`{item.leakage_status}`, posthoc=`{item.posthoc_fit_flagged}`, ad_hoc_scale=`{item.ad_hoc_scale_flagged}`")
    return "\n".join(lines) + "\n"


def _render_decision(decision: CandidateSelectionDecision) -> str:
    return "\n".join(
        [
            "# Candidate Selection Decision v5.9",
            "",
            f"- final_status: `{decision.final_status}`",
            f"- selected_candidate_family: `{decision.selected_candidate_family}`",
            f"- selected_rule_id: `{decision.selected_rule_id}`",
            f"- passed_candidate_count: `{decision.passed_candidate_count}`",
            f"- blocked_by_missing_features_count: `{decision.blocked_by_missing_features_count}`",
            f"- blocked_by_leakage_count: `{decision.blocked_by_leakage_count}`",
            f"- allowed_next_phase: `{decision.allowed_next_phase}`",
            f"- rationale: {decision.rationale}",
        ]
    ) + "\n"


def _render_campaign(result: dict) -> str:
    decision = result["decision"]
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9",
            "",
            f"- status: `{decision.final_status}`",
            f"- candidate_count: `{decision.candidate_count}`",
            f"- passed_candidate_count: `{decision.passed_candidate_count}`",
            f"- selected_candidate_family: `{decision.selected_candidate_family}`",
            f"- no_predictive_gain_computed: `True`",
            f"- physical_claim_created: `False`",
            f"- frontera_c_validated: `False`",
        ]
    ) + "\n"
