"""Reports for v4.9 source identity preflight."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_identity_preflight.schemas import SourceIdentityPreflightCampaignResult


def write_source_identity_preflight_reports(result: SourceIdentityPreflightCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    preflight_dir = root / "preflight" / "source_identity"
    campaign_dir = root / "campaigns"
    preflight_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "inventory": preflight_dir / "candidate_family_source_inventory_v4_9.md",
        "identity_matrix": preflight_dir / "source_identity_resolution_matrix_v4_9.md",
        "availability_matrix": preflight_dir / "source_availability_matrix_v4_9.md",
        "observable_matrix": preflight_dir / "observable_identity_matrix_v4_9.md",
        "ytrue_path_matrix": preflight_dir / "ytrue_path_plausibility_matrix_v4_9.md",
        "decision_matrix": preflight_dir / "candidate_preflight_decision_matrix_v4_9.md",
        "gate": preflight_dir / "source_identity_preflight_gate_v4_9.md",
        "campaign": campaign_dir / "PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9.md",
    }
    renderers = {
        "inventory": _render_inventory,
        "identity_matrix": _render_identity,
        "availability_matrix": _render_availability,
        "observable_matrix": _render_observable,
        "ytrue_path_matrix": _render_ytrue,
        "decision_matrix": _render_decision,
        "gate": _render_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: SourceIdentityPreflightCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Source Identity Preflight Gate v4.9",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="source_identity_preflight",
        reports_generated=reports_generated or [],
        next_actions=result.gate.required_before_next_pipeline,
        discipline_note="No source identity, no science pipeline. Source identity does not create evidence.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_inventory(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# Candidate Family Source Inventory v4.9", "", f"- candidate_count: `{len(result.inventory)}`", ""]
    for record in result.inventory:
        lines.append(f"- `{record.family_id}`: status=`{record.inventory_status}`, raw_refs=`{len(record.raw_source_refs)}`, local_pdfs=`{len(record.local_pdf_refs)}`")
    return "\n".join(lines) + "\n"


def _render_identity(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# Source Identity Resolution Matrix v4.9", "", f"- record_count: `{len(result.identity_matrix)}`", ""]
    for record in result.identity_matrix:
        lines.append(f"- `{record.family_id}` / `{record.source_ref_raw or 'NO_REF'}`: status=`{record.resolution_status}`, complete=`{record.identity_complete}`")
    return "\n".join(lines) + "\n"


def _render_availability(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# Source Availability Matrix v4.9", "", f"- record_count: `{len(result.availability_matrix)}`", ""]
    for record in result.availability_matrix:
        lines.append(f"- `{record.family_id}` / `{record.source_id or 'NO_SOURCE'}`: status=`{record.availability_status}`, local_pdf=`{record.local_pdf_available}`")
    return "\n".join(lines) + "\n"


def _render_observable(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# Observable Identity Matrix v4.9", "", f"- record_count: `{len(result.observable_matrix)}`", ""]
    for record in result.observable_matrix:
        lines.append(f"- `{record.family_id}`: class=`{record.observable_class}`, status=`{record.observable_status}`")
    return "\n".join(lines) + "\n"


def _render_ytrue(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# y_true Path Plausibility Matrix v4.9", "", f"- record_count: `{len(result.ytrue_path_matrix)}`", ""]
    for record in result.ytrue_path_matrix:
        lines.append(f"- `{record.family_id}`: class=`{record.observable_class}`, plausibility=`{record.plausibility_level}`")
    return "\n".join(lines) + "\n"


def _render_decision(result: SourceIdentityPreflightCampaignResult) -> str:
    lines = ["# Candidate Preflight Decision Matrix v4.9", "", f"- candidate_count: `{len(result.decision_matrix)}`", ""]
    for record in result.decision_matrix:
        lines.append(f"- `{record.family_id}`: status=`{record.preflight_status}`, resolvable_sources=`{record.resolvable_source_count}`")
    return "\n".join(lines) + "\n"


def _render_gate(result: SourceIdentityPreflightCampaignResult) -> str:
    gate = result.gate
    lines = [
        "# Source Identity Preflight Gate v4.9",
        "",
        f"- final_status: `{gate.final_status}`",
        f"- candidate_count: `{gate.candidate_count}`",
        f"- passed_candidate_count: `{gate.passed_candidate_count}`",
        f"- partial_candidate_count: `{gate.partial_candidate_count}`",
        f"- failed_candidate_count: `{gate.failed_candidate_count}`",
        f"- selected_candidate_family: `{gate.selected_candidate_family}`",
        f"- allowed_next_phase: `{gate.allowed_next_phase}`",
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
    ]
    return "\n".join(lines) + "\n"


def _render_campaign(result: SourceIdentityPreflightCampaignResult) -> str:
    return "\n".join(
        [
            "# Campaign Report - PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9",
            "",
            f"- status: `{result.status}`",
            f"- inputs_loaded: `{result.inputs_loaded}`",
            f"- candidate_count: `{len(result.inventory)}`",
            f"- passed_candidate_count: `{result.gate.passed_candidate_count}`",
            f"- partial_candidate_count: `{result.gate.partial_candidate_count}`",
            f"- failed_candidate_count: `{result.gate.failed_candidate_count}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"
