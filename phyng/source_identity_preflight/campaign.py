"""Campaign orchestration for v4.9 source identity preflight."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.source_identity_preflight.availability import build_source_availability_matrix
from phyng.source_identity_preflight.decision import BLOCKED_CLAIMS, build_candidate_preflight_decision_matrix, build_source_identity_preflight_gate
from phyng.source_identity_preflight.identity_resolution import build_source_identity_resolution_matrix
from phyng.source_identity_preflight.inventory import build_candidate_family_source_inventory
from phyng.source_identity_preflight.loader import load_source_identity_preflight_inputs, prior_results_available
from phyng.source_identity_preflight.observable_identity import build_observable_identity_matrix
from phyng.source_identity_preflight.reports import write_source_identity_preflight_reports
from phyng.source_identity_preflight.schemas import SourceIdentityPreflightCampaignResult, SourceIdentityPreflightGate
from phyng.source_identity_preflight.ytrue_path import build_ytrue_path_plausibility_matrix


def run_phygn_source_identity_preflight_campaign(root: str | Path = ".") -> SourceIdentityPreflightCampaignResult:
    repo_root = Path(root)
    inputs = load_source_identity_preflight_inputs(repo_root)
    if not prior_results_available(inputs):
        status = "PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS"
        gate = SourceIdentityPreflightGate(
            final_status=status,
            candidate_count=0,
            passed_candidate_count=0,
            partial_candidate_count=0,
            failed_candidate_count=0,
            blocked_next_phases=["Source identity preflight", "PredictiveGain evaluation", "Physical validation"],
            required_before_next_pipeline=["Restore required v4.8/v4.6/debt artifacts."],
            blocked_claims=BLOCKED_CLAIMS,
            allowed_claims=[],
            notes=inputs.missing_files,
        )
        result = SourceIdentityPreflightCampaignResult(
            status=status,
            canonical_status=normalize_status(status, domain="source_identity_preflight"),
            inputs_loaded=False,
            gate=gate,
        )
        result.output_paths = write_outputs(repo_root, result)
        result.report_paths = write_source_identity_preflight_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    inventory = build_candidate_family_source_inventory(repo_root, inputs)
    identities = build_source_identity_resolution_matrix(inventory, repo_root)
    availability = build_source_availability_matrix(identities)
    observables = build_observable_identity_matrix(identities)
    ytrue_paths = build_ytrue_path_plausibility_matrix(observables, availability)
    decisions = build_candidate_preflight_decision_matrix(inventory, identities, availability, observables, ytrue_paths)
    gate = build_source_identity_preflight_gate(decisions)
    result = SourceIdentityPreflightCampaignResult(
        status=gate.final_status,
        canonical_status=normalize_status(gate.final_status, domain="source_identity_preflight"),
        inputs_loaded=True,
        inventory=inventory,
        identity_matrix=identities,
        availability_matrix=availability,
        observable_matrix=observables,
        ytrue_path_matrix=ytrue_paths,
        decision_matrix=decisions,
        gate=gate,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_source_identity_preflight_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def write_outputs(root: Path, result: SourceIdentityPreflightCampaignResult) -> dict[str, str]:
    base = root / "data" / "preflight" / "source_identity"
    paths = {
        "inventory": base / "candidate_family_source_inventory_v4_9.json",
        "identity_matrix": base / "source_identity_resolution_matrix_v4_9.json",
        "availability_matrix": base / "source_availability_matrix_v4_9.json",
        "observable_matrix": base / "observable_identity_matrix_v4_9.json",
        "ytrue_path_matrix": base / "ytrue_path_plausibility_matrix_v4_9.json",
        "decision_matrix": base / "candidate_preflight_decision_matrix_v4_9.json",
        "gate": base / "source_identity_preflight_gate_v4_9.json",
    }
    payloads = {
        "inventory": result.inventory,
        "identity_matrix": result.identity_matrix,
        "availability_matrix": result.availability_matrix,
        "observable_matrix": result.observable_matrix,
        "ytrue_path_matrix": result.ytrue_path_matrix,
        "decision_matrix": result.decision_matrix,
        "gate": result.gate,
    }
    for key, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = payloads[key]
        dumped = [item.model_dump() for item in payload] if isinstance(payload, list) else payload.model_dump()
        path.write_text(json.dumps(dumped, indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: SourceIdentityPreflightCampaignResult) -> None:
    path = root / "docs" / "321_PHYGN_V4_9_SOURCE_IDENTITY_PREFLIGHT_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v4.9 - Candidate Source Identity Preflight Gate Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/320_PHYGN_CODEX_V4_9_SOURCE_IDENTITY_PREFLIGHT_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Candidate count: `{result.gate.candidate_count}`",
        f"Passed candidates: `{result.gate.passed_candidate_count}`",
        f"Partial candidates: `{result.gate.partial_candidate_count}`",
        f"Failed candidates: `{result.gate.failed_candidate_count}`",
        f"Selected candidate family: `{result.gate.selected_candidate_family}`",
        "",
        "No y_true was created. No PredictiveGain was computed. No physical claim was upgraded.",
        "",
        "PHI_GRADIENT remains METHOD_ONLY_EMPIRICALLY_UNGROUNDED.",
        "PHI_CURVATURE remains blocked unless source identity is newly resolved.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
