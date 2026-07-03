from phyng.core.compatibility import get_canonical_permission
from phyng.core.permissions import CanonicalPermission
from phyng.heuristic_discovery.pipeline import run_heuristic_to_testable_pipeline


def test_pipeline_returns_next_best_question():
    result = run_heuristic_to_testable_pipeline("Boundary behavior", "physical_candidate")

    assert result.top_candidate is not None
    assert result.next_best_question
    assert "benchmark" in result.next_best_question.lower()


def test_existing_canonical_mapping_still_passes():
    assert get_canonical_permission("BUSINESS_BLOCKED_NO_WTP") == CanonicalPermission.SCALE_BLOCKED
    assert get_canonical_permission("OUTSIDE_CLAIM_BOUNDARY") == CanonicalPermission.CLAIM_BLOCKED
