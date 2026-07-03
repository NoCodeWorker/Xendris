"""Versioned update records for closed-loop changes."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.closed_loop.schemas import MetaChangeProposal, VersionedUpdateRecord


def create_versioned_update_record(
    proposal: MetaChangeProposal,
    previous_config: dict,
    new_config: dict,
    reason: str,
    tests_required: list[str],
    rollback_path: str,
    impact_summary: str,
) -> VersionedUpdateRecord:
    status = "META_CHANGE_REQUIRES_HUMAN_REVIEW" if proposal.requires_human_review else "META_CHANGE_APPROVED_LOW_RISK"
    return VersionedUpdateRecord(
        version_id=f"VER-{proposal.proposal_id}",
        proposal_id=proposal.proposal_id,
        previous_config=previous_config,
        new_config=new_config,
        reason=reason,
        tests_required=tests_required,
        rollback_path=rollback_path,
        impact_summary=impact_summary,
        canonical_status=normalize_status(status, domain="closed_loop"),
    )
