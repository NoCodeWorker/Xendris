from copy import deepcopy

from phyng.closed_loop.meta_loop import classify_meta_change_risk
from phyng.closed_loop.schemas import MetaChangeProposal
from phyng.closed_loop.shadow_mode import run_shadow_mode
from phyng.core.compatibility import normalize_status


def test_shadow_mode_does_not_mutate_authoritative_outputs():
    proposal = classify_meta_change_risk(
        MetaChangeProposal(
            proposal_id="META-SHADOW-001",
            change_type="REPORT_TEMPLATE_CHANGE",
            description="report wording",
            current_behavior="old",
            proposed_behavior="new",
            canonical_status=normalize_status("META_CHANGE_PROPOSED", domain="closed_loop"),
        )
    )
    sample = [{"current_output": {"canonical_permission": "TEST_DESIGN_ALLOWED", "blocked_reasons": ["MISSING_SOURCE_SUPPORT"]}}]
    before = deepcopy(sample)

    result = run_shadow_mode(proposal, sample)

    assert sample == before
    assert result.recommendation == "SHADOW_APPROVED_NO_MUTATION"
    assert not result.permission_differences
