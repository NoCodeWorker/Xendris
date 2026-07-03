"""Heuristic candidate generation."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.heuristic_discovery.schemas import HeuristicCandidate


PHYSICAL_FAMILIES = [
    "B_SUPPRESSED",
    "QB_STRUCTURAL",
    "LOG_BOUNDARY",
    "THRESHOLD_SATURATION",
    "OBSERVABLE_DEPENDENT_BOUNDARY",
    "DIMENSIONLESS_INVARIANT",
    "REGIME_TRANSITION",
    "NOISE_COUPLING_MODULATION",
]

BUSINESS_FAMILIES = [
    "CUSTOMER_HYPOTHESIS",
    "PROBLEM_HYPOTHESIS",
    "WTP_HYPOTHESIS",
    "CHANNEL_HYPOTHESIS",
    "UNIT_ECONOMICS_HYPOTHESIS",
]

COPILOT_FAMILIES = [
    "CLARIFY_TERM",
    "DEFINE_OBSERVABLE",
    "DEFINE_FAILURE_CONDITION",
    "CHOOSE_BENCHMARK",
    "REQUEST_SOURCE",
]


def generate_heuristic_candidates(raw_problem: str, domain: str) -> list[HeuristicCandidate]:
    normalized_domain = domain.lower()
    if normalized_domain in {"physical", "physics", "physical_candidate"}:
        return [_physical_candidate(raw_problem, family, index) for index, family in enumerate(PHYSICAL_FAMILIES, 1)]
    if normalized_domain in {"business", "business_hypothesis"}:
        return [_business_candidate(raw_problem, family, index) for index, family in enumerate(BUSINESS_FAMILIES, 1)]
    if normalized_domain in {"copilot", "question", "copilot_question"}:
        return [_copilot_candidate(raw_problem, family, index) for index, family in enumerate(COPILOT_FAMILIES, 1)]
    return [_generic_candidate(raw_problem, domain)]


def _physical_candidate(raw_problem: str, family: str, index: int) -> HeuristicCandidate:
    base_scores = {
        "detectability_potential": 0.55,
        "non_ad_hoc_score": 0.75,
        "dimensional_consistency": 0.8,
        "falsifiability": 0.75,
        "benchmarkability": 0.7,
        "source_searchability": 0.65,
        "simplicity": 0.6,
        "novelty": 0.65,
        "cost_to_test_inverse": 0.55,
        "risk_penalty": 0.25,
    }
    if family == "B_SUPPRESSED":
        base_scores.update({
            "detectability_potential": 0.15,
            "novelty": 0.35,
            "risk_penalty": 0.35,
        })
    if family == "LOG_BOUNDARY":
        base_scores.update({
            "detectability_potential": 0.7,
            "source_searchability": 0.75,
            "simplicity": 0.7,
        })

    return HeuristicCandidate(
        candidate_id=f"HEUR-PHY-{index:03d}",
        domain="physical_candidate",
        raw_idea=raw_problem,
        proposed_hypothesis=f"{family} may identify a testable boundary behavior in: {raw_problem}",
        candidate_family=family,
        suggested_observables=["visibility_decay", "boundary_ratio_shift"],
        suggested_proxies=["max_abs_delta", "log_coordinate_shift"],
        required_sources=["canonical physical model source", "measurement protocol source"],
        required_benchmarks=["baseline environment-only model", "detectability threshold benchmark"],
        failure_conditions=["No measurable delta above epsilon threshold", "Requires unphysical parameter scale"],
        assumptions=["heuristic candidate only", "priority score is not evidence"],
        heuristic_scores=base_scores,
        canonical_status=normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    )


def _business_candidate(raw_problem: str, family: str, index: int) -> HeuristicCandidate:
    return HeuristicCandidate(
        candidate_id=f"HEUR-BUS-{index:03d}",
        domain="business_hypothesis",
        raw_idea=raw_problem,
        proposed_hypothesis=f"{family} should be tested for: {raw_problem}",
        candidate_family=family,
        suggested_observables=["qualified_response_rate", "paid_commitment_signal"],
        suggested_proxies=["interview_count", "preorder_or_pilot_count"],
        required_sources=["customer discovery notes", "pricing evidence"],
        required_benchmarks=["minimum viable channel conversion baseline"],
        failure_conditions=["No qualified customer signal", "No payment signal after declared outreach"],
        assumptions=["heuristic business decomposition only"],
        heuristic_scores=_default_scores(),
        canonical_status=normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    )


def _copilot_candidate(raw_problem: str, family: str, index: int) -> HeuristicCandidate:
    return HeuristicCandidate(
        candidate_id=f"HEUR-COP-{index:03d}",
        domain="copilot_question",
        raw_idea=raw_problem,
        proposed_hypothesis=f"Next copilot move: {family} for: {raw_problem}",
        candidate_family=family,
        suggested_observables=["answered_question", "missing_field_resolved"],
        suggested_proxies=["field_completion_delta"],
        required_sources=["workspace state"],
        required_benchmarks=["question usefulness baseline"],
        failure_conditions=["Question does not reduce missing fields"],
        assumptions=["heuristic question selection only"],
        heuristic_scores=_default_scores(),
        canonical_status=normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    )


def _generic_candidate(raw_problem: str, domain: str) -> HeuristicCandidate:
    return HeuristicCandidate(
        candidate_id="HEUR-GEN-001",
        domain=domain,
        raw_idea=raw_problem,
        proposed_hypothesis=f"Heuristic seed for {domain}: {raw_problem}",
        candidate_family="GENERIC_HEURISTIC",
        suggested_observables=[],
        suggested_proxies=[],
        required_sources=[],
        required_benchmarks=[],
        failure_conditions=[],
        assumptions=["generic heuristic seed requires review"],
        heuristic_scores=_default_scores(),
        canonical_status=normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    )


def _default_scores() -> dict[str, float]:
    return {
        "detectability_potential": 0.5,
        "non_ad_hoc_score": 0.7,
        "dimensional_consistency": 0.7,
        "falsifiability": 0.7,
        "benchmarkability": 0.6,
        "source_searchability": 0.6,
        "simplicity": 0.6,
        "novelty": 0.5,
        "cost_to_test_inverse": 0.6,
        "risk_penalty": 0.2,
    }
