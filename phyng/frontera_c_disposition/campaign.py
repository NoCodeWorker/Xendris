"""Campaign orchestration for v5.6 LOG_BOUNDARY control failure review."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.frontera_c_disposition.allowed_future_roles import build_allowed_future_roles
from phyng.frontera_c_disposition.blocked_claims import build_blocked_claims
from phyng.frontera_c_disposition.candidate_disposition import build_candidate_disposition
from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs
from phyng.frontera_c_disposition.next_research_direction import build_next_research_direction
from phyng.frontera_c_disposition.reports import write_disposition_reports
from phyng.frontera_c_disposition.roadmap_update import build_roadmap_update
from phyng.frontera_c_disposition.schemas import LogBoundaryControlFailureCampaignResult


def run_frontera_c_log_boundary_control_failure_review_campaign(root: str | Path = ".") -> LogBoundaryControlFailureCampaignResult:
    repo_root = Path(root)
    inputs = load_control_failure_inputs(repo_root)
    if inputs.missing_files:
        result = LogBoundaryControlFailureCampaignResult(
            status="LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS",
            inputs_loaded=False,
            missing_files=inputs.missing_files,
        )
        result.output_paths = write_outputs(repo_root, result)
        result.report_paths = write_disposition_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    review = build_control_failure_review(inputs)
    disposition = build_candidate_disposition(review)
    future_roles = build_allowed_future_roles(disposition)
    blocked_claims = build_blocked_claims(disposition.candidate_family)
    roadmap = build_roadmap_update(disposition)
    next_direction = build_next_research_direction(roadmap, blocked_claims)
    result = LogBoundaryControlFailureCampaignResult(
        status="LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE",
        inputs_loaded=True,
        review=review,
        disposition=disposition,
        future_roles=future_roles,
        blocked_claims=blocked_claims,
        roadmap_update=roadmap,
        next_direction=next_direction,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_disposition_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def write_outputs(root: Path, result: LogBoundaryControlFailureCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "disposition"
    paths = {
        "review": base / "log_boundary_control_failure_review_v5_6.json",
        "disposition": base / "log_boundary_candidate_disposition_v5_6.json",
        "future_roles": base / "log_boundary_allowed_future_roles_v5_6.json",
        "blocked_claims": base / "log_boundary_blocked_claims_v5_6.json",
        "roadmap_update": base / "frontera_c_roadmap_update_after_log_boundary_v5_6.json",
        "next_direction": base / "v5_6_next_research_direction.json",
    }
    payloads = {
        "review": result.review,
        "disposition": result.disposition,
        "future_roles": result.future_roles,
        "blocked_claims": result.blocked_claims,
        "roadmap_update": result.roadmap_update,
        "next_direction": result.next_direction,
    }
    base.mkdir(parents=True, exist_ok=True)
    for key, path in paths.items():
        payload = payloads[key]
        dumped = payload.model_dump() if payload is not None else {"status": result.status, "missing_files": result.missing_files}
        path.write_text(json.dumps(dumped, indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: LogBoundaryControlFailureCampaignResult) -> None:
    path = root / "docs" / "332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v5.6 - LOG_BOUNDARY Control Failure Review Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/331_PHYGN_CODEX_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Inputs loaded: `{result.inputs_loaded}`",
        "",
        "## Disposition",
        "",
        f"Primary disposition: `{result.disposition.primary_disposition if result.disposition else None}`",
        f"Can proceed to C-structure ablation: `{result.review.can_proceed_to_c_structure_ablation if result.review else False}`",
        f"Can support Frontera C validation: `{result.review.can_support_frontera_c_validation if result.review else False}`",
        "",
        "## Next Direction",
        "",
        f"Allowed next phase: `{result.next_direction.allowed_next_phase if result.next_direction else None}`",
        "",
        "No PredictiveGain was recomputed. No C-structure ablation was executed. No physical claim was created. Frontera C remains unvalidated.",
    ]
    contract = build_report_contract(
        title="LOG_BOUNDARY Control Failure Review Results v5.6",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="frontera_c_disposition",
        next_actions=["Expand visibility/decoherence dataset without restoring LOG_BOUNDARY as an active validation candidate."],
        discipline_note="A positive smoke test is a suspect, not a proof. A control failure is a verdict.",
    )
    path.write_text(append_canonical_status_section("\n".join(lines) + "\n", contract), encoding="utf-8")
