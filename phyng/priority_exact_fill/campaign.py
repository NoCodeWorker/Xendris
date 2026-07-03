"""Campaign orchestration for PHI_GRADIENT priority exact fill v3.5."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.priority_exact_fill.report import write_priority_exact_fill_reports
from phyng.priority_exact_fill.review_gate import run_phi_gradient_priority_exact_fill_gate
from phyng.priority_exact_fill.schemas import PhiGradientPriorityExactFillCampaignResult, PriorityExactFillRecord


def run_phi_gradient_priority_exact_fill_campaign(
    root: str | Path = ".",
    priority_records: list[PriorityExactFillRecord] | None = None,
) -> PhiGradientPriorityExactFillCampaignResult:
    repo_root = Path(root)
    gate = run_phi_gradient_priority_exact_fill_gate(str(repo_root), priority_records=priority_records)
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5",
        input_type="PRIORITY_EXACT_FILL_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_EXACT_EXTRACT_REVIEW_COMPLETED",
        result_status=gate.status,
        payload={
            "priority_source_count": gate.priority_source_count,
            "validation_ready_count": gate.validation_ready_count,
            "unresolved_count": gate.unresolved_count,
            "source_text_required_count": gate.source_text_required_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5-{gate.status}",
        proposal_type="PRIORITY_EXACT_FILL_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Priority exact fill executed; unavailable local source text remains outside source support.",
        proposed_change={
            "status": gate.status,
            "validation_ready_count": gate.validation_ready_count,
            "unresolved_count": gate.unresolved_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "treat URL as exact source text",
            "count unresolved priority source as support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientPriorityExactFillCampaignResult(
        campaign_id="PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5",
        status=gate.status,
        gate_result=gate,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_priority_exact_fill_reports(result, repo_root / "reports")
    return result
