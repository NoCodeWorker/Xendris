"""Report writers for v2.4 closed-loop meta-improvement."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.closed_loop.schemas import ClosedLoopCampaignResult


def write_closed_loop_reports(result: ClosedLoopCampaignResult, reports_dir: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_dir)
    loop_dir = root / "closed_loop"
    campaigns_dir = root / "campaigns"
    loop_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidate_loop": loop_dir / "candidate_learning_loop_v2_4.md",
        "meta_loop": loop_dir / "meta_improvement_loop_v2_4.md",
        "shadow_mode": loop_dir / "shadow_mode_v2_4.md",
        "guards": loop_dir / "self_confirmation_guards_v2_4.md",
        "versioning": loop_dir / "versioned_update_records_v2_4.md",
        "campaign": campaigns_dir / "CLOSED-LOOP-META-IMPROVEMENT-v2_4.md",
    }
    paths["candidate_loop"].write_text(_canonical(_candidate(result), "LOOP_UPDATE_PROPOSED", result.campaign_id), encoding="utf-8")
    paths["meta_loop"].write_text(_canonical(_meta(result), result.meta_improvement_result.proposal.canonical_status.domain_status, result.campaign_id), encoding="utf-8")
    paths["shadow_mode"].write_text(_canonical(_shadow(result), result.shadow_mode_result.canonical_status.domain_status, result.campaign_id), encoding="utf-8")
    paths["guards"].write_text(_canonical(_guards(result), result.status, result.campaign_id), encoding="utf-8")
    paths["versioning"].write_text(_canonical(_versioning(result), result.versioned_record.canonical_status.domain_status, result.campaign_id), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_campaign(result), result.status, result.campaign_id, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, status: str, campaign_id: str, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Closed Loop Meta Improvement v2.4",
        campaign_id=campaign_id,
        domain_status=status,
        reports_generated=reports_generated or [],
        discipline_note="Phygn can improve itself. It cannot give itself permission to be right.",
    )
    return append_canonical_status_section(markdown, contract)


def _candidate(result: ClosedLoopCampaignResult) -> str:
    loop = result.candidate_loop_result
    return "\n".join([
        "# Candidate Learning Loop v2.4",
        "",
        f"- loop_id: `{loop.loop_id}`",
        f"- input_type: `{loop.input_type}`",
        f"- candidate_id: `{loop.candidate_id}`",
        f"- new_status: `{loop.new_status}`",
        f"- audit_event_id: `{loop.audit_event_id}`",
        "",
        "## Next Actions",
        "",
        *[f"- {item}" for item in loop.next_actions],
        "",
        "## Blocked Claims",
        "",
        *[f"- {item}" for item in loop.blocked_claims],
    ]) + "\n"


def _meta(result: ClosedLoopCampaignResult) -> str:
    proposal = result.meta_improvement_result.proposal
    return "\n".join([
        "# Meta Improvement Loop v2.4",
        "",
        f"- proposal_id: `{proposal.proposal_id}`",
        f"- change_type: `{proposal.change_type}`",
        f"- risk_level: `{proposal.risk_level}`",
        f"- requires_shadow_mode: `{proposal.requires_shadow_mode}`",
        f"- requires_human_review: `{proposal.requires_human_review}`",
        "",
        "## Blocked Actions",
        "",
        "- Critical gate changes cannot be auto-applied.",
        "- Evidence requirements cannot be relaxed without review.",
    ]) + "\n"


def _shadow(result: ClosedLoopCampaignResult) -> str:
    shadow = result.shadow_mode_result
    return "\n".join([
        "# Shadow Mode v2.4",
        "",
        f"- proposal_id: `{shadow.proposal_id}`",
        f"- recommendation: `{shadow.recommendation}`",
        f"- differences: `{len(shadow.differences)}`",
        f"- permission_differences: `{len(shadow.permission_differences)}`",
        "",
        "## Blocked Actions",
        "",
        "- Shadow mode cannot mutate authoritative behavior.",
    ]) + "\n"


def _guards(result: ClosedLoopCampaignResult) -> str:
    lines = [
        "# Self-Confirmation Guards v2.4",
        "",
        "| Guard | Passed | Severity | Message |",
        "|---|---|---|---|",
    ]
    for guard in result.guard_results:
        lines.append(f"| `{guard.guard_name}` | {guard.passed} | `{guard.severity}` | {guard.message} |")
    lines.extend(["", "## Blocked Claims", "", "- Self-confirming promotion without source/benchmark evidence."])
    return "\n".join(lines) + "\n"


def _versioning(result: ClosedLoopCampaignResult) -> str:
    record = result.versioned_record
    return "\n".join([
        "# Versioned Update Records v2.4",
        "",
        f"- version_id: `{record.version_id}`",
        f"- proposal_id: `{record.proposal_id}`",
        f"- rollback_path: `{record.rollback_path}`",
        f"- impact_summary: {record.impact_summary}",
        "",
        "## Tests Required",
        "",
        *[f"- `{item}`" for item in record.tests_required],
        "",
        "## Blocked Actions",
        "",
        "- High-risk updates are not applied automatically.",
    ]) + "\n"


def _campaign(result: ClosedLoopCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - CLOSED-LOOP-META-IMPROVEMENT-v2_4",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        "",
        "## Core Results",
        "",
        "- Candidate learning loop created update proposals without authorizing physical claims.",
        "- Meta-improvement loop classified risk and used shadow mode.",
        "- Guards block self-confirming promotion.",
        "",
        "## Blocked Claims",
        "",
        "- Phygn improves its truth automatically.",
        "- The loop validates hypotheses.",
        "- Self-improvement can relax evidence gates.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
