"""Campaign orchestration for PHI_CURVATURE minimal source/y_true v4.8."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.phi_curvature_minimal_campaign.dataset import build_minimal_dataset
from phyng.phi_curvature_minimal_campaign.loader import load_phi_curvature_minimal_inputs, v47_screen_passed
from phyng.phi_curvature_minimal_campaign.next_gate import BLOCKED_CLAIMS, ALLOWED_CLAIMS, decide_next_gate
from phyng.phi_curvature_minimal_campaign.observable_extraction import extract_candidate_observables
from phyng.phi_curvature_minimal_campaign.reports import write_phi_curvature_reports
from phyng.phi_curvature_minimal_campaign.schemas import (
    EvidenceAuditEvent,
    PhiCurvatureMinimalCampaignResult,
    PhiCurvatureMinimalYTrueDataset,
    PhiCurvatureNextGateDecision,
)
from phyng.phi_curvature_minimal_campaign.source_availability import assess_source_availability
from phyng.phi_curvature_minimal_campaign.source_resolution import resolve_seed_references
from phyng.phi_curvature_minimal_campaign.ytrue_qc import build_ytrue_candidates, split_ytrue


def run_phi_curvature_minimal_source_ytrue_campaign(root: str | Path = ".") -> PhiCurvatureMinimalCampaignResult:
    repo_root = Path(root)
    inputs = load_phi_curvature_minimal_inputs(repo_root)
    if inputs.missing_files or not v47_screen_passed(inputs):
        status = "PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN"
        dataset = PhiCurvatureMinimalYTrueDataset(notes=["v4.7 passed screen missing or unavailable."])
        gate = PhiCurvatureNextGateDecision(
            final_status=status,
            accepted_ytrue_count=0,
            threshold_reached=False,
            blocked_claims=BLOCKED_CLAIMS,
            allowed_claims=[],
            allowed_next_phase=None,
            blocked_next_phases=["v4.8 minimal campaign", "PredictiveGain evaluation"],
            required_before_predictive_gain=["Restore v4.7 passed screen."],
            notes=inputs.missing_files,
        )
        result = PhiCurvatureMinimalCampaignResult(
            status=status,
            canonical_status=normalize_status(status, domain="phi_curvature_minimal_campaign"),
            inputs_loaded=False,
            dataset=dataset,
            next_gate=gate,
        )
        result.output_paths = write_outputs(repo_root, result)
        result.report_paths = write_phi_curvature_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    refs = inputs.source_screen.get("known_source_refs", [])
    resolutions = resolve_seed_references(repo_root, refs)
    availability = assess_source_availability(repo_root, resolutions)
    observables = extract_candidate_observables(resolutions, availability, inputs.observable_screen)
    source_hashes = {record.source_id: record.local_pdf_hash for record in availability}
    ytrue_candidates = build_ytrue_candidates(observables, source_hashes)
    accepted, rejected = split_ytrue(ytrue_candidates)
    dataset = build_minimal_dataset(accepted)
    gate = decide_next_gate(dataset, resolutions, availability)
    status = gate.final_status
    audit = build_audit_trail(resolutions, observables, ytrue_candidates)
    result = PhiCurvatureMinimalCampaignResult(
        status=status,
        canonical_status=normalize_status(status, domain="phi_curvature_minimal_campaign"),
        inputs_loaded=True,
        source_resolution=resolutions,
        source_availability=availability,
        candidate_observables=observables,
        ytrue_candidates=ytrue_candidates,
        accepted_ytrue=accepted,
        rejected_ytrue=rejected,
        audit_trail=audit,
        dataset=dataset,
        next_gate=gate,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_phi_curvature_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def build_audit_trail(resolutions, observables, ytrue_candidates) -> list[EvidenceAuditEvent]:
    events: list[EvidenceAuditEvent] = []
    for index, record in enumerate(resolutions, start=1):
        events.append(EvidenceAuditEvent(audit_id=f"PHICURV-AUDIT-v4_8-{index:03d}", object_id=record.source_id or record.source_ref_raw, event_type="SOURCE_RESOLUTION", decision=record.resolution_status, reason="Raw citation was checked against local artifacts.", claim_impact="No source support unless identity and local provenance are complete."))
    offset = len(events)
    for index, record in enumerate(observables, start=1):
        events.append(EvidenceAuditEvent(audit_id=f"PHICURV-AUDIT-v4_8-{offset+index:03d}", object_id=record.observable_id, event_type="OBSERVABLE_EXTRACTION", decision=record.extraction_status, reason=", ".join(record.blockers), claim_impact="No y_true unless numeric value and provenance pass QC."))
    offset = len(events)
    for index, record in enumerate(ytrue_candidates, start=1):
        events.append(EvidenceAuditEvent(audit_id=f"PHICURV-AUDIT-v4_8-{offset+index:03d}", object_id=record.candidate_id, event_type="YTRUE_QC", decision=record.qc_status, reason=record.rejection_reason or "PASS", claim_impact="Accepted y_true does not create PredictiveGain in v4.8."))
    return events


def write_outputs(root: Path, result: PhiCurvatureMinimalCampaignResult) -> dict[str, str]:
    paths = {
        "source_resolution": root / "data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json",
        "source_availability": root / "data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json",
        "candidate_observables": root / "data/phi_curvature/evidence/phi_curvature_candidate_observables_v4_8.json",
        "ytrue_candidates": root / "data/phi_curvature/evidence/phi_curvature_ytrue_candidates_v4_8.json",
        "accepted_ytrue": root / "data/phi_curvature/evidence/phi_curvature_accepted_ytrue_v4_8.json",
        "rejected_ytrue": root / "data/phi_curvature/evidence/phi_curvature_rejected_ytrue_v4_8.json",
        "audit_trail": root / "data/phi_curvature/evidence/phi_curvature_evidence_audit_trail_v4_8.json",
        "dataset": root / "data/phi_curvature/datasets/phi_curvature_minimal_ytrue_dataset_v4_8.json",
        "next_gate": root / "data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json",
    }
    payloads = {
        "source_resolution": result.source_resolution,
        "source_availability": result.source_availability,
        "candidate_observables": result.candidate_observables,
        "ytrue_candidates": result.ytrue_candidates,
        "accepted_ytrue": result.accepted_ytrue,
        "rejected_ytrue": result.rejected_ytrue,
        "audit_trail": result.audit_trail,
        "dataset": result.dataset,
        "next_gate": result.next_gate,
    }
    for key, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = payloads[key]
        dumped = [item.model_dump() for item in payload] if isinstance(payload, list) else payload.model_dump()
        path.write_text(json.dumps(dumped, indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: PhiCurvatureMinimalCampaignResult) -> None:
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v4.8 - PHI_CURVATURE Minimal Source/y_true Campaign Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/314_PHYGN_CODEX_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Accepted y_true count: `{len(result.accepted_ytrue)}`",
        f"Rejected y_true count: `{len(result.rejected_ytrue)}`",
        f"Threshold reached: `{result.dataset.threshold_reached}`",
        f"PredictiveGain status: `{result.dataset.predictive_gain_status}`",
        f"Physical claim permission: `{result.dataset.physical_claim_permission}`",
        "",
        "No PredictiveGain was computed. No physical claim was upgraded. PHI_GRADIENT remains method-only and SLOT_4 remains open.",
    ]
    (docs_dir / "315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
