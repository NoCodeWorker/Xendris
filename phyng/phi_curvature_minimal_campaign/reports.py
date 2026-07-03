"""Reports for PHI_CURVATURE minimal campaign v4.8."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.phi_curvature_minimal_campaign.schemas import PhiCurvatureMinimalCampaignResult


def write_phi_curvature_reports(result: PhiCurvatureMinimalCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    source_dir = root / "phi_curvature" / "sources"
    evidence_dir = root / "phi_curvature" / "evidence"
    dataset_dir = root / "phi_curvature" / "datasets"
    next_dir = root / "phi_curvature" / "next"
    campaign_dir = root / "campaigns"
    for directory in (source_dir, evidence_dir, dataset_dir, next_dir, campaign_dir):
        directory.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_resolution": source_dir / "phi_curvature_source_resolution_v4_8.md",
        "source_availability": source_dir / "phi_curvature_source_availability_v4_8.md",
        "candidate_observables": evidence_dir / "phi_curvature_candidate_observables_v4_8.md",
        "ytrue_candidates": evidence_dir / "phi_curvature_ytrue_candidates_v4_8.md",
        "accepted_ytrue": evidence_dir / "phi_curvature_accepted_ytrue_v4_8.md",
        "rejected_ytrue": evidence_dir / "phi_curvature_rejected_ytrue_v4_8.md",
        "audit_trail": evidence_dir / "phi_curvature_evidence_audit_trail_v4_8.md",
        "dataset": dataset_dir / "phi_curvature_minimal_ytrue_dataset_v4_8.md",
        "next_gate": next_dir / "phi_curvature_v4_8_next_gate_decision.md",
        "campaign": campaign_dir / "PHI-CURVATURE-MINIMAL-SOURCE-YTRUE-CAMPAIGN-v4_8.md",
    }
    renderers = {
        "source_resolution": _render_resolution,
        "source_availability": _render_availability,
        "candidate_observables": _render_observables,
        "ytrue_candidates": _render_ytrue_candidates,
        "accepted_ytrue": _render_accepted,
        "rejected_ytrue": _render_rejected,
        "audit_trail": _render_audit,
        "dataset": _render_dataset,
        "next_gate": _render_next,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiCurvatureMinimalCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="PHI_CURVATURE Minimal Source/y_true Campaign v4.8",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="phi_curvature_minimal_campaign",
        reports_generated=reports_generated or [],
        next_actions=result.next_gate.required_before_predictive_gain,
        discipline_note="Accepted y_true is not PredictiveGain. The minimal campaign does not validate PHI_CURVATURE or Frontera C.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_resolution(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Source Resolution v4.8", "", f"- record_count: `{len(result.source_resolution)}`", ""]
    for record in result.source_resolution:
        lines.append(f"- `{record.source_ref_raw}`: status=`{record.resolution_status}`, source_id=`{record.source_id}`")
    return "\n".join(lines) + "\n"


def _render_availability(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Source Availability v4.8", "", f"- record_count: `{len(result.source_availability)}`", ""]
    for record in result.source_availability:
        lines.append(f"- `{record.source_id}`: status=`{record.availability_status}`, local_pdf=`{record.local_pdf_available}`")
    return "\n".join(lines) + "\n"


def _render_observables(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Candidate Observables v4.8", "", f"- observable_count: `{len(result.candidate_observables)}`", ""]
    for record in result.candidate_observables:
        lines.append(f"- `{record.observable_id}`: class=`{record.observable_class}`, status=`{record.extraction_status}`")
    return "\n".join(lines) + "\n"


def _render_ytrue_candidates(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE y_true Candidates v4.8", "", f"- candidate_count: `{len(result.ytrue_candidates)}`", ""]
    for record in result.ytrue_candidates:
        lines.append(f"- `{record.candidate_id}`: qc=`{record.qc_status}`, can_enter=`{record.can_enter_dataset}`, rejection=`{record.rejection_reason}`")
    return "\n".join(lines) + "\n"


def _render_accepted(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Accepted y_true v4.8", "", f"- accepted_count: `{len(result.accepted_ytrue)}`", ""]
    if not result.accepted_ytrue:
        lines.append("No candidate met strict y_true QC.")
    for record in result.accepted_ytrue:
        lines.append(f"- `{record.y_true_id}`: value=`{record.value}` `{record.unit}`")
    return "\n".join(lines) + "\n"


def _render_rejected(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Rejected y_true v4.8", "", f"- rejected_count: `{len(result.rejected_ytrue)}`", ""]
    for record in result.rejected_ytrue:
        lines.append(f"- `{record.candidate_id}`: `{record.rejection_reason}`")
    return "\n".join(lines) + "\n"


def _render_audit(result: PhiCurvatureMinimalCampaignResult) -> str:
    lines = ["# PHI_CURVATURE Evidence Audit Trail v4.8", "", f"- audit_event_count: `{len(result.audit_trail)}`", ""]
    for event in result.audit_trail:
        lines.append(f"- `{event.audit_id}`: `{event.event_type}`, decision=`{event.decision}`")
    return "\n".join(lines) + "\n"


def _render_dataset(result: PhiCurvatureMinimalCampaignResult) -> str:
    dataset = result.dataset
    return "\n".join([
        "# PHI_CURVATURE Minimal y_true Dataset v4.8",
        "",
        f"- accepted_ytrue_count: `{dataset.accepted_ytrue_count}`",
        f"- minimum_threshold: `{dataset.minimum_threshold}`",
        f"- threshold_reached: `{dataset.threshold_reached}`",
        f"- predictive_gain_status: `{dataset.predictive_gain_status}`",
        f"- physical_claim_permission: `{dataset.physical_claim_permission}`",
    ]) + "\n"


def _render_next(result: PhiCurvatureMinimalCampaignResult) -> str:
    gate = result.next_gate
    return "\n".join([
        "# PHI_CURVATURE v4.8 Next Gate Decision",
        "",
        f"- final_status: `{gate.final_status}`",
        f"- accepted_ytrue_count: `{gate.accepted_ytrue_count}`",
        f"- threshold_reached: `{gate.threshold_reached}`",
        f"- allowed_next_phase: `{gate.allowed_next_phase}`",
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
    ]) + "\n"


def _render_campaign(result: PhiCurvatureMinimalCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - PHI-CURVATURE-MINIMAL-SOURCE-YTRUE-CAMPAIGN-v4_8",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- inputs_loaded: `{result.inputs_loaded}`",
        f"- source_resolution_count: `{len(result.source_resolution)}`",
        f"- accepted_ytrue_count: `{len(result.accepted_ytrue)}`",
        f"- rejected_ytrue_count: `{len(result.rejected_ytrue)}`",
        f"- next_gate: `{result.next_gate.final_status}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
