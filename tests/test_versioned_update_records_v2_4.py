from phyng.closed_loop.meta_loop import classify_meta_change_risk
from phyng.closed_loop.schemas import MetaChangeProposal
from phyng.closed_loop.versioning import create_versioned_update_record
from phyng.core.compatibility import normalize_status


def test_versioned_update_record_has_rollback_path():
    proposal = classify_meta_change_risk(
        MetaChangeProposal(
            proposal_id="META-VERSION-001",
            change_type="REPORT_TEMPLATE_CHANGE",
            description="report template update",
            current_behavior="old",
            proposed_behavior="new",
            canonical_status=normalize_status("META_CHANGE_PROPOSED", domain="closed_loop"),
        )
    )
    record = create_versioned_update_record(
        proposal,
        previous_config={"template": "old"},
        new_config={"template": "new"},
        reason="Improve blocked claims section.",
        tests_required=["pytest -q"],
        rollback_path="Restore previous report template.",
        impact_summary="No gate behavior change.",
    )

    assert record.rollback_path
    assert record.previous_config["template"] == "old"
    assert record.new_config["template"] == "new"
