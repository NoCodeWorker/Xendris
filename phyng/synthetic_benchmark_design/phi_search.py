"""Phi candidate search, ranking and loop feedback."""

from __future__ import annotations

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.phi_candidates import generate_phi_candidate_families
from phyng.synthetic_benchmark_design.phi_evaluation import evaluate_phi_candidate
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryCandidateSpec,
    PhiCandidateEvaluationResult,
    PhiCandidateRankingResult,
    PhiSearchLoopFeedbackResult,
)


def run_phi_candidate_search(spec: LogBoundaryCandidateSpec) -> tuple[list[PhiCandidateEvaluationResult], PhiCandidateRankingResult]:
    evaluations = [evaluate_phi_candidate(spec, candidate) for candidate in generate_phi_candidate_families()]
    ranked = sorted(evaluations, key=lambda result: result.metrics.control_resistance_score, reverse=True)
    survivors = [result for result in ranked if result.classification == "PHI_CANDIDATE_SURVIVES_CONTROLS"]
    status = "PHI_CANDIDATE_SURVIVES_CONTROLS" if survivors else "PHI_SEARCH_NO_SURVIVOR"
    best_candidate = survivors[0] if survivors else ranked[0] if ranked else None
    ranking = PhiCandidateRankingResult(
        status=status,
        canonical_status=normalize_status(status, domain="phi_search"),
        ranked_candidates=ranked,
        survivor_count=len(survivors),
        best_candidate_family=best_candidate.candidate.family if best_candidate else None,
    )
    return evaluations, ranking


def generate_phi_search_loop_feedback(ranking: PhiCandidateRankingResult) -> PhiSearchLoopFeedbackResult:
    loop_input = CandidateLoopInput(
        loop_id="LOG-BOUNDARY-PHI-SEARCH-v2_7",
        input_type="PHI_SEARCH_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="LOG_BOUNDARY",
        previous_status="LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT",
        result_status=ranking.status,
        payload={
            "survivor_count": ranking.survivor_count,
            "best_candidate_family": ranking.best_candidate_family,
            "ranking_note": ranking.ranking_note,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    allowed_updates, next_actions = _feedback_actions(ranking)
    proposal = CandidateUpdateProposal(
        proposal_id=f"LOG-BOUNDARY-PHI-SEARCH-v2_7-{ranking.status}",
        proposal_type="PHI_SEARCH_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="LOG_BOUNDARY",
        description=_proposal_description(ranking),
        proposed_change={"allowed_updates": allowed_updates, "next_actions": next_actions},
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=ranking.status != "PHI_CANDIDATE_SURVIVES_CONTROLS",
        forbidden_actions=["authorize physical claim", "validate Frontera C", "relax source requirement"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    return PhiSearchLoopFeedbackResult(
        loop_event_id=loop_result.audit_event_id,
        result_status=ranking.status,
        canonical_status=ranking.canonical_status,
        candidate_loop_input=loop_input,
        candidate_loop_result=loop_result,
        update_proposals=[proposal],
        allowed_updates=allowed_updates,
        blocked_updates=[
            "physical claim authorization",
            "Frontera C validation",
            "experimental confirmation",
            "source requirement reduction",
            "benchmark requirement reduction",
            "canonical permission semantic changes",
            "claim gate relaxation",
        ],
        next_actions=next_actions,
        blocked_claims=[
            "A surviving phi validates LOG_BOUNDARY.",
            "A non-saturating phi proves Frontera C.",
            "Synthetic control resistance proves a physical effect.",
        ],
    )


def _feedback_actions(ranking: PhiCandidateRankingResult) -> tuple[list[str], list[str]]:
    if ranking.status == "PHI_CANDIDATE_SURVIVES_CONTROLS":
        return (
            ["increase source-search priority for surviving phi formulation", "increase benchmark-pressure priority"],
            ["schedule source-support audit", "schedule benchmark-data search", "keep physical claims blocked"],
        )
    return (
        ["reject/down-rank saturating or constant-control formulations"],
        ["down-rank LOG_BOUNDARY family", "select next heuristic family", "retain results as negative control"],
    )


def _proposal_description(ranking: PhiCandidateRankingResult) -> str:
    if ranking.status == "PHI_CANDIDATE_SURVIVES_CONTROLS":
        return f"Promote synthetic pressure for surviving phi family {ranking.best_candidate_family}; physical claims remain blocked."
    return "No phi candidate survived controls; down-rank current LOG_BOUNDARY phi search and retain failure memory."
