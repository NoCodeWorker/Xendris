"""Candidate learning loop."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal


def run_candidate_learning_loop(input: CandidateLoopInput) -> CandidateLoopResult:
    canonical = normalize_status(input.result_status, domain="closed_loop")
    post_mortem_id = None
    skip_reason = None
    proposals: list[CandidateUpdateProposal] = []
    next_actions: list[str] = []

    if input.result_status == "SYNTHETIC_BENCHMARK_DESIGNED":
        skip_reason = "No synthetic execution outcome exists yet; post-mortem deferred."
        next_actions = [
            "execute synthetic benchmark",
            "source search pressure",
            "benchmark data search",
            "priority update proposal",
        ]
        proposals.append(
            CandidateUpdateProposal(
                proposal_id=f"{input.loop_id}-PROP-001",
                proposal_type="SOURCE_SEARCH_PRIORITY_UPDATE",
                candidate_id=input.candidate_id,
                candidate_family=input.candidate_family,
                description="Increase source and benchmark pressure for LOG_BOUNDARY before any claim promotion.",
                proposed_change={"source_search_priority": "increase", "benchmark_pressure": "increase"},
                risk_level="LOW",
                requires_shadow_mode=False,
                requires_human_review=False,
                forbidden_actions=["authorize physical claim", "validate Frontera C", "experimental confirmation"],
                canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
            )
        )
    else:
        post_mortem_id = f"{input.loop_id}-PM-001"
        next_actions = ["record result classification", "review candidate family priority"]

    return CandidateLoopResult(
        loop_id=input.loop_id,
        input_type=input.input_type,
        domain=input.domain,
        candidate_id=input.candidate_id,
        candidate_family=input.candidate_family,
        previous_status=input.previous_status,
        new_status="LOOP_UPDATE_PROPOSED",
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
        ledger_event_id=f"{input.loop_id}-LEDGER-001",
        post_mortem_id=post_mortem_id,
        post_mortem_skip_reason=skip_reason,
        update_proposals=proposals,
        next_actions=next_actions,
        blocked_reasons=[reason.value for reason in canonical.blocked_reasons],
        blocked_claims=[
            "authorize physical claim",
            "validate Frontera C",
            "experimental confirmation",
        ],
        audit_event_id=f"{input.loop_id}-AUDIT-001",
    )
