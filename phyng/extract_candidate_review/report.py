"""Reports for PHI_GRADIENT extract candidate review v3.8."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.extract_candidate_review.schemas import PhiGradientExtractCandidateReviewCampaignResult


def write_extract_candidate_review_reports(
    result: PhiGradientExtractCandidateReviewCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "extract_candidate_review"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "summary": report_dir / "phi_gradient_candidate_review_summary_v3_8.md",
        "validation_ready_pack": report_dir / "phi_gradient_validation_ready_pack_v3_8.md",
        "rejected_candidates": report_dir / "phi_gradient_rejected_candidates_v3_8.md",
        "manual_review_queue": report_dir / "phi_gradient_manual_review_queue_v3_8.md",
        "component_role_map": report_dir / "phi_gradient_component_role_map_v3_8.md",
        "next_pressure_gate": report_dir / "phi_gradient_next_pressure_gate_v3_8.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8.md",
    }
    renderers = {
        "summary": _render_summary,
        "validation_ready_pack": _render_pack,
        "rejected_candidates": _render_rejected,
        "manual_review_queue": _render_manual_queue,
        "component_role_map": _render_role_map,
        "next_pressure_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientExtractCandidateReviewCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Extract Candidate Review v3.8",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="extract_candidate_review",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="A validation-ready extract is not support. It is an object ready to be judged.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_summary(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Candidate Review Summary v3.8",
            "",
            f"- status: `{gate.status}`",
            f"- input_candidate_count: `{gate.input_candidate_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- rejected_count: `{gate.rejected_count}`",
            f"- manual_review_count: `{gate.manual_review_count}`",
            f"- pedernales_blocked: `{gate.pedernales_blocked}`",
            "",
            "## Component Role Counts",
            "",
            *_or_none([f"- `{role}`: `{count}`" for role, count in sorted(gate.component_role_counts.items())]),
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_pack(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    pack = result.gate_result.validation_ready_pack
    return "\n".join(
        [
            "# PHI_GRADIENT Validation-Ready Pack v3.8",
            "",
            f"- validation_ready_count: `{pack.validation_ready_count}`",
            f"- rejected_count: `{pack.rejected_count}`",
            f"- manual_review_count: `{pack.manual_review_count}`",
            "",
            *_or_none([f"- `{item.extract_id}`: source=`{item.source_id}`, role=`{item.component_role}`, page=`{item.page_number}`" for item in pack.extracts]),
        ]
    ) + "\n"


def _render_rejected(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    rejected = result.gate_result.rejected_candidates
    return "\n".join(
        [
            "# PHI_GRADIENT Rejected Candidates v3.8",
            "",
            f"- rejected_count: `{len(rejected)}`",
            "",
            *_or_none([f"- `{item.candidate_id}`: `{item.review_status}` - {item.reason}" for item in rejected[:60]]),
        ]
    ) + "\n"


def _render_manual_queue(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    queue = result.gate_result.manual_review_queue
    return "\n".join(
        [
            "# PHI_GRADIENT Manual Review Queue v3.8",
            "",
            f"- manual_review_count: `{len(queue)}`",
            "",
            *_or_none([f"- `{item.candidate_id}`: priority=`{item.priority}`, source=`{item.source_id}`, reason={item.reason}" for item in queue[:80]]),
        ]
    ) + "\n"


def _render_role_map(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    entries = result.gate_result.reviewed_candidate_map
    return "\n".join(
        [
            "# PHI_GRADIENT Component Role Map v3.8",
            "",
            *_or_none([f"- `{item.candidate_id}`: decision=`{item.review_decision}`, role=`{item.component_role}`" for item in entries[:80]]),
        ]
    ) + "\n"


def _render_next_gate(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Next Pressure Gate v3.8",
            "",
            f"- status: `{gate.status}`",
            f"- next_phase: `v3.9 - Validation-Ready Extract Gate & First Source-Pressure Decision`",
            "",
            "## Allowed Claims",
            "",
            *[f"- {claim}" for claim in gate.allowed_claims],
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
            "",
            "## Next Actions",
            "",
            *[f"- {action}" for action in gate.next_actions],
        ]
    ) + "\n"


def _render_campaign(result: PhiGradientExtractCandidateReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- input_candidate_count: `{gate.input_candidate_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- rejected_count: `{gate.rejected_count}`",
            f"- manual_review_count: `{gate.manual_review_count}`",
            f"- pedernales_blocked: `{gate.pedernales_blocked}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
