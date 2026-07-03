"""Heuristic-to-testable-hypothesis pipeline."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.core.permissions import CanonicalPermission
from phyng.heuristic_discovery.generator import generate_heuristic_candidates
from phyng.heuristic_discovery.permissions import evaluate_heuristic_permission
from phyng.heuristic_discovery.prioritizer import rank_heuristic_candidates
from phyng.heuristic_discovery.schemas import HeuristicPipelineResult


def run_heuristic_to_testable_pipeline(raw_problem: str, domain: str) -> HeuristicPipelineResult:
    candidates = generate_heuristic_candidates(raw_problem, domain)
    ranking = rank_heuristic_candidates(candidates)
    permission_results = [evaluate_heuristic_permission(candidate) for candidate in ranking.candidates]
    top_candidate = ranking.candidates[0] if ranking.candidates else None
    top_permission = permission_results[0] if permission_results else None
    missing_fields = top_permission.missing_fields if top_permission else []

    if "suggested_observables" in missing_fields:
        question = "What observable would make this heuristic candidate measurable?"
    elif "failure_conditions" in missing_fields:
        question = "What result would falsify or kill this heuristic candidate?"
    elif "required_benchmarks" in missing_fields:
        question = "Which baseline or benchmark should this candidate be compared against?"
    elif top_permission and top_permission.canonical_status.canonical_permission == CanonicalPermission.TEST_DESIGN_ALLOWED:
        question = "What synthetic benchmark should be run first?"
    else:
        question = "What missing evidence would prevent overclaiming this heuristic output?"

    canonical_status = (
        top_permission.canonical_status
        if top_permission is not None
        else normalize_status("HEURISTIC_REVIEW_REQUIRED", domain="heuristic_discovery")
    )
    return HeuristicPipelineResult(
        raw_problem=raw_problem,
        domain=domain,
        candidates=ranking.candidates,
        ranking=ranking,
        permission_results=permission_results,
        top_candidate=top_candidate,
        missing_fields=missing_fields,
        next_best_question=question,
        canonical_status=canonical_status,
    )
