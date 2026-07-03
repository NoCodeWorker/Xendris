from phyng.core.compatibility import normalize_status
from phyng.core.permissions import CanonicalPermission
from phyng.heuristic_discovery.schemas import HeuristicCandidate


def test_heuristic_candidate_has_canonical_status():
    candidate = HeuristicCandidate(
        candidate_id="HEUR-TEST-001",
        domain="physical_candidate",
        raw_idea="Test boundary signal",
        proposed_hypothesis="A boundary signal may be testable.",
        candidate_family="LOG_BOUNDARY",
        canonical_status=normalize_status("HEURISTIC_SEED", domain="heuristic_discovery"),
    )

    assert candidate.canonical_status.domain_status == "HEURISTIC_SEED"
    assert candidate.canonical_status.canonical_permission == CanonicalPermission.EXPLORE_ALLOWED
