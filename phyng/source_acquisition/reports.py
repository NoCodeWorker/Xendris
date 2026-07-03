"""Reports for v5.7.1 targeted source acquisition."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_acquisition.schemas import SourceAcquisitionCampaignResult


def write_source_acquisition_reports(result: SourceAcquisitionCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "source_acquisition"
    campaign_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "queue": report_dir / "visibility_decoherence_source_acquisition_queue_v5_7_1.md",
        "identity": report_dir / "visibility_decoherence_candidate_source_identity_matrix_v5_7_1.md",
        "observable": report_dir / "visibility_decoherence_observable_target_matrix_v5_7_1.md",
        "download": report_dir / "visibility_decoherence_download_priority_queue_v5_7_1.md",
        "rejection": report_dir / "visibility_decoherence_source_rejection_log_v5_7_1.md",
        "campaign": campaign_dir / "FRONTERA-C-TARGETED-VISIBILITY-DECOHERENCE-LITERATURE-ACQUISITION-v5_7_1.md",
    }
    renderers = {
        "queue": _render_queue,
        "identity": _render_identity,
        "observable": _render_observable,
        "download": _render_download,
        "rejection": _render_rejection,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    result.report_paths = {key: str(path) for key, path in paths.items()}
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(result.report_paths.values())), encoding="utf-8")
    return result.report_paths


def _canonical(markdown: str, result: SourceAcquisitionCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Targeted Visibility/Decoherence Literature Acquisition v5.7.1",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="targeted_visibility_decoherence_source_acquisition",
        reports_generated=reports_generated or [],
        next_actions=["Download resolved sources and perform observable location review."],
        discipline_note="A source queue is not evidence. It is a map toward possible evidence.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_queue(result: SourceAcquisitionCampaignResult) -> str:
    lines = ["# Source Acquisition Queue v5.7.1", "", f"- queue_count: `{len(result.acquisition_queue)}`", ""]
    for item in result.acquisition_queue:
        lines.append(f"- `{item.acquisition_id}`: priority=`{item.priority}`, identity=`{item.source_identity_status}`")
    return "\n".join(lines) + "\n"


def _render_identity(result: SourceAcquisitionCampaignResult) -> str:
    lines = ["# Candidate Source Identity Matrix v5.7.1", "", f"- record_count: `{len(result.identity_matrix)}`", ""]
    for item in result.identity_matrix:
        lines.append(f"- `{item.source_candidate_id}`: complete=`{item.identity_complete}`, score=`{item.identity_completeness_score}`")
    return "\n".join(lines) + "\n"


def _render_observable(result: SourceAcquisitionCampaignResult) -> str:
    lines = ["# Observable Target Matrix v5.7.1", "", f"- target_count: `{len(result.observable_matrix)}`", ""]
    for item in result.observable_matrix:
        lines.append(f"- `{item.source_candidate_id}`: `{item.target_observable_class}` via `{item.expected_location_type}`")
    return "\n".join(lines) + "\n"


def _render_download(result: SourceAcquisitionCampaignResult) -> str:
    lines = ["# Download Priority Queue v5.7.1", "", f"- download_count: `{len(result.download_queue)}`", ""]
    for item in result.download_queue:
        lines.append(f"- `{item.source_candidate_id}`: target=`{item.target_local_path}`, paywall=`{item.requires_paywall_access}`")
    return "\n".join(lines) + "\n"


def _render_rejection(result: SourceAcquisitionCampaignResult) -> str:
    lines = ["# Source Rejection Log v5.7.1", "", f"- rejection_count: `{len(result.rejection_log)}`", ""]
    for item in result.rejection_log:
        lines.append(f"- `{item.source_candidate_id}`: reason=`{item.rejection_reason}`")
    return "\n".join(lines) + "\n"


def _render_campaign(result: SourceAcquisitionCampaignResult) -> str:
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-TARGETED-VISIBILITY-DECOHERENCE-LITERATURE-ACQUISITION-v5_7_1",
            "",
            f"- status: `{result.status}`",
            f"- inputs_loaded: `{result.inputs_loaded}`",
            f"- resolved_candidate_source_count: `{result.next_gate_decision.get('resolved_candidate_source_count')}`",
            f"- download_required_count: `{result.next_gate_decision.get('download_required_count')}`",
            f"- no_ytrue_extracted: `{result.next_gate_decision.get('no_ytrue_extracted')}`",
            f"- no_predictive_gain_computed: `{result.next_gate_decision.get('no_predictive_gain_computed')}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"
