from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.compatibility import normalize_status
from phyng.core.permissions import CanonicalPermission
from phyng.heuristic_discovery.permissions import evaluate_heuristic_permission
from phyng.heuristic_discovery.schemas import HeuristicCandidate


def _candidate(**overrides):
    data = {
        "candidate_id": "HEUR-GATE-001",
        "domain": "physical_candidate",
        "raw_idea": "Boundary signal",
        "proposed_hypothesis": "A boundary signal may be measurable.",
        "candidate_family": "LOG_BOUNDARY",
        "suggested_observables": ["visibility_decay"],
        "suggested_proxies": ["max_abs_delta"],
        "required_sources": ["source"],
        "required_benchmarks": ["baseline"],
        "failure_conditions": ["delta below epsilon"],
        "assumptions": ["heuristic only"],
        "heuristic_scores": {
            "dimensional_consistency": 0.9,
            "non_ad_hoc_score": 0.9,
        },
        "canonical_status": normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    }
    data.update(overrides)
    return HeuristicCandidate(**data)


def test_heuristic_seed_maps_to_explore_allowed():
    record = normalize_status("HEURISTIC_SEED", domain="heuristic_discovery")

    assert record.canonical_permission == CanonicalPermission.EXPLORE_ALLOWED
    assert CanonicalBlockedReason.MISSING_SOURCE_SUPPORT in record.blocked_reasons


def test_heuristic_output_cannot_authorize_claim():
    result = evaluate_heuristic_permission(_candidate())

    assert result.is_claim_authorized is False
    assert result.canonical_status.canonical_permission == CanonicalPermission.TEST_DESIGN_ALLOWED


def test_missing_observable_blocks_test_design():
    result = evaluate_heuristic_permission(_candidate(suggested_observables=[]))

    assert result.domain_status == "HEURISTIC_REJECTED_NO_OBSERVABLE"
    assert result.is_test_design_allowed is False
    assert "suggested_observables" in result.missing_fields


def test_missing_failure_condition_blocks_test_design():
    result = evaluate_heuristic_permission(_candidate(failure_conditions=[]))

    assert result.domain_status == "HEURISTIC_REVIEW_REQUIRED"
    assert result.is_test_design_allowed is False
    assert "failure_conditions" in result.missing_fields
