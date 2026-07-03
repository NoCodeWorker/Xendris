"""Reports for v5.6 LOG_BOUNDARY disposition."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.frontera_c_disposition.schemas import LogBoundaryControlFailureCampaignResult


def write_disposition_reports(result: LogBoundaryControlFailureCampaignResult, root: str | Path = "reports") -> dict[str, str]:
    reports_root = Path(root)
    disp_dir = reports_root / "frontera_c" / "disposition"
    campaign_dir = reports_root / "campaigns"
    disp_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "review": disp_dir / "log_boundary_control_failure_review_v5_6.md",
        "disposition": disp_dir / "log_boundary_candidate_disposition_v5_6.md",
        "future_roles": disp_dir / "log_boundary_allowed_future_roles_v5_6.md",
        "blocked_claims": disp_dir / "log_boundary_blocked_claims_v5_6.md",
        "roadmap_update": disp_dir / "frontera_c_roadmap_update_after_log_boundary_v5_6.md",
        "next_direction": disp_dir / "v5_6_next_research_direction.md",
        "campaign": campaign_dir / "FRONTERA-C-LOG-BOUNDARY-CONTROL-FAILURE-REVIEW-v5_6.md",
    }
    renderers = {
        "review": _render_review,
        "disposition": _render_disposition,
        "future_roles": _render_future_roles,
        "blocked_claims": _render_blocked_claims,
        "roadmap_update": _render_roadmap,
        "next_direction": _render_next,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    result.report_paths = {key: str(path) for key, path in paths.items()}
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(result.report_paths.values())), encoding="utf-8")
    return result.report_paths


def _canonical(markdown: str, result: LogBoundaryControlFailureCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="LOG_BOUNDARY Control Failure Review v5.6",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="frontera_c_disposition",
        reports_generated=reports_generated or [],
        next_actions=["Expand visibility/decoherence dataset without rescuing LOG_BOUNDARY."],
        discipline_note="A positive smoke test is a suspect, not a proof. A control failure is a verdict.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_review(result: LogBoundaryControlFailureCampaignResult) -> str:
    review = result.review
    return "\n".join(
        [
            "# LOG_BOUNDARY Control Failure Review v5.6",
            "",
            f"- status: `{result.status}`",
            f"- previous_status: `{review.previous_status if review else None}`",
            f"- primary_failure_reason: `{review.primary_failure_reason if review else None}`",
            f"- can_proceed_to_c_structure_ablation: `{review.can_proceed_to_c_structure_ablation if review else False}`",
            f"- can_support_frontera_c_validation: `{review.can_support_frontera_c_validation if review else False}`",
            "",
            review.failure_summary if review else "Missing inputs blocked review.",
        ]
    ) + "\n"


def _render_disposition(result: LogBoundaryControlFailureCampaignResult) -> str:
    disp = result.disposition
    lines = ["# LOG_BOUNDARY Candidate Disposition v5.6", "", f"- status: `{result.status}`"]
    if disp:
        lines += [
            f"- primary_disposition: `{disp.primary_disposition}`",
            f"- archived_as_validation_candidate: `{disp.archived_as_validation_candidate}`",
            f"- retained_as_fixture: `{disp.retained_as_fixture}`",
            "",
            "## Reopen Criteria",
            "",
            *[f"- {item}" for item in disp.required_to_reopen_as_candidate],
        ]
    return "\n".join(lines) + "\n"


def _render_future_roles(result: LogBoundaryControlFailureCampaignResult) -> str:
    roles = result.future_roles
    return "\n".join(
        [
            "# LOG_BOUNDARY Allowed Future Roles v5.6",
            "",
            "## Allowed",
            "",
            *[f"- {item}" for item in (roles.allowed_roles if roles else [])],
            "",
            "## Blocked",
            "",
            *[f"- {item}" for item in (roles.blocked_roles if roles else [])],
        ]
    ) + "\n"


def _render_blocked_claims(result: LogBoundaryControlFailureCampaignResult) -> str:
    claims = result.blocked_claims
    return "\n".join(
        [
            "# LOG_BOUNDARY Blocked Claims v5.6",
            "",
            f"- claim_permission: `{claims.claim_permission if claims else 'CLAIM_BLOCKED'}`",
            f"- frontera_c_validated: `{claims.frontera_c_validated if claims else False}`",
            f"- physical_claim_created: `{claims.physical_claim_created if claims else False}`",
            "",
            "## Blocked Claims",
            "",
            *[f"- {item}" for item in (claims.blocked_claims if claims else [])],
        ]
    ) + "\n"


def _render_roadmap(result: LogBoundaryControlFailureCampaignResult) -> str:
    roadmap = result.roadmap_update
    return "\n".join(
        [
            "# Frontera C Roadmap Update After LOG_BOUNDARY v5.6",
            "",
            f"- new_blocker: `{roadmap.new_blocker if roadmap else None}`",
            f"- current_validation_status: `{roadmap.current_validation_status if roadmap else 'NOT_VALIDATED'}`",
            f"- recommended_path: `{roadmap.recommended_path if roadmap else None}`",
            "",
            roadmap.rationale if roadmap else "",
        ]
    ) + "\n"


def _render_next(result: LogBoundaryControlFailureCampaignResult) -> str:
    next_direction = result.next_direction
    return "\n".join(
        [
            "# v5.6 Next Research Direction",
            "",
            f"- final_status: `{next_direction.final_status if next_direction else result.status}`",
            f"- selected_next_direction: `{next_direction.selected_next_direction if next_direction else None}`",
            f"- allowed_next_phase: `{next_direction.allowed_next_phase if next_direction else None}`",
            "",
            next_direction.rationale if next_direction else "",
        ]
    ) + "\n"


def _render_campaign(result: LogBoundaryControlFailureCampaignResult) -> str:
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-LOG-BOUNDARY-CONTROL-FAILURE-REVIEW-v5_6",
            "",
            f"- status: `{result.status}`",
            f"- inputs_loaded: `{result.inputs_loaded}`",
            f"- frontera_c_validated: `{result.blocked_claims.frontera_c_validated if result.blocked_claims else False}`",
            f"- physical_claim_created: `{result.blocked_claims.physical_claim_created if result.blocked_claims else False}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"
