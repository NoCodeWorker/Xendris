"""v5.9 reality-contact candidate-family construction campaign."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.candidates.dataset_introspection import load_canonical_dataset
from phyng.candidates.family_registry import build_candidate_family_registry
from phyng.candidates.feature_schema import build_feature_schema
from phyng.candidates.leakage_screen import build_leakage_screen
from phyng.candidates.prediction_rules import build_prediction_rules
from phyng.candidates.reality_contact_screen import build_reality_contact_screen
from phyng.candidates.reports import write_candidate_reports
from phyng.candidates.selection_decision import build_selection_decision
from phyng.candidates.schemas import CandidateSelectionDecision


def run_frontera_c_reality_contact_candidate_family_campaign(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    dataset = load_canonical_dataset(repo_root)
    families = build_candidate_family_registry()
    feature_schema = build_feature_schema(dataset, families)
    rules = build_prediction_rules(families, feature_schema.missing_required_features_by_candidate)
    leakage = build_leakage_screen(families, rules)
    screen = build_reality_contact_screen(families, rules, leakage, feature_schema.missing_required_features_by_candidate)
    decision = build_selection_decision(screen, leakage)
    next_gate = _next_gate(decision)
    result = {
        "dataset": dataset,
        "families": families,
        "feature_schema": feature_schema,
        "rules": rules,
        "leakage": leakage,
        "screen": screen,
        "decision": decision,
        "next_gate": next_gate,
    }
    output_paths = write_outputs(repo_root, result)
    report_paths = write_candidate_reports(result, repo_root / "reports")
    final_doc = write_final_doc(repo_root, result, output_paths, report_paths)
    return {
        "status": decision.final_status,
        "selected_candidate_family": decision.selected_candidate_family,
        "passed_candidate_count": decision.passed_candidate_count,
        "allowed_next_phase": decision.allowed_next_phase,
        "output_paths": output_paths,
        "report_paths": report_paths,
        "final_doc": final_doc,
    }


def write_outputs(root: Path, result: dict) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "candidates"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "registry": base / "candidate_family_registry_v5_9.json",
        "features": base / "candidate_feature_schema_v5_9.json",
        "rules": base / "candidate_prediction_rules_v5_9.json",
        "reality": base / "candidate_reality_contact_screen_v5_9.json",
        "leakage": base / "candidate_leakage_screen_v5_9.json",
        "decision": base / "candidate_selection_decision_v5_9.json",
        "next_gate": base / "v5_9_next_gate_decision.json",
    }
    payloads = {
        "registry": {"candidate_count": len(result["families"]), "records": [item.model_dump() for item in result["families"]]},
        "features": result["feature_schema"].model_dump(),
        "rules": {"rule_count": len(result["rules"]), "records": [item.model_dump() for item in result["rules"]]},
        "reality": {"screen_count": len(result["screen"]), "records": [item.model_dump() for item in result["screen"]]},
        "leakage": {"leakage_record_count": len(result["leakage"]), "records": [item.model_dump() for item in result["leakage"]]},
        "decision": result["decision"].model_dump(),
        "next_gate": result["next_gate"],
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_final_doc(root: Path, result: dict, output_paths: dict[str, str], report_paths: dict[str, str]) -> str:
    from phyng.core.report_contract import append_canonical_status_section, build_report_contract

    decision: CandidateSelectionDecision = result["decision"]
    path = root / "docs" / "374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md"
    lines = [
        "# Phygn v5.9 - Reality-Contact Candidate Family Construction Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/373_PHYGN_CODEX_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{decision.final_status}`",
        f"Candidate families screened: `{decision.candidate_count}`",
        f"Passed candidates: `{decision.passed_candidate_count}`",
        f"Selected candidate family: `{decision.selected_candidate_family}`",
        f"Allowed next phase: `{decision.allowed_next_phase}`",
        "",
        "No PredictiveGain was computed. No benchmark scoring was run. No negative controls or C-structure ablation were run. Frontera C was not validated.",
        "",
        "## Created Artifacts",
        "",
        *[f"- `{value}`" for value in output_paths.values()],
        *[f"- `{value}`" for value in report_paths.values()],
        "",
        "## Blocked Claims",
        "",
        "- Candidate validated.",
        "- Frontera C validated.",
        "- PredictiveGain exists.",
        "- Physical mechanism confirmed.",
        "- LOG_BOUNDARY reactivated.",
        "",
        "Final discipline:",
        "",
        "```txt",
        "A candidate is not a name.",
        "A candidate is a leak-free rule that can be wrong.",
        "```",
    ]
    contract = build_report_contract(
        title="Reality-Contact Candidate Family Construction Results v5.9",
        campaign_id="FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9",
        domain_status=decision.final_status,
        domain="candidate_family_selection",
        reports_generated=list(report_paths.values()),
        next_actions=[decision.allowed_next_phase or "Resolve missing features or reformulate candidate theory."],
        discipline_note="Selection is permission to test. Nothing more.",
    )
    path.write_text(append_canonical_status_section("\n".join(lines) + "\n", contract), encoding="utf-8")
    return path.relative_to(root).as_posix()


def _next_gate(decision: CandidateSelectionDecision) -> dict:
    return {
        "final_status": decision.final_status,
        "selected_candidate_family": decision.selected_candidate_family,
        "selected_rule_id": decision.selected_rule_id,
        "allowed_next_phase": decision.allowed_next_phase,
        "blocked_next_phases": decision.blocked_next_phases,
        "no_predictive_gain_computed": True,
        "benchmark_scoring_run": False,
        "negative_controls_run": False,
        "c_structure_ablation_run": False,
        "frontera_c_validated": False,
        "physical_claim_created": False,
        "rationale": decision.rationale,
    }
