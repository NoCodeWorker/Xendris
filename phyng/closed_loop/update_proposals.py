"""Helpers for closed-loop update proposals."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.closed_loop.schemas import CandidateUpdateProposal


def create_candidate_update_proposal(
    proposal_id: str,
    proposal_type: str,
    description: str,
    candidate_id: str | None = None,
    candidate_family: str | None = None,
    risk_level: str = "LOW",
) -> CandidateUpdateProposal:
    return CandidateUpdateProposal(
        proposal_id=proposal_id,
        proposal_type=proposal_type,
        candidate_id=candidate_id,
        candidate_family=candidate_family,
        description=description,
        risk_level=risk_level,
        requires_shadow_mode=risk_level in {"MEDIUM", "HIGH"},
        requires_human_review=risk_level == "HIGH",
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
