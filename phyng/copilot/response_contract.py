"""
Phygn v1.8 — Copilot Response Contract

Verifies that any response returned to the user conforms to the strict Response Contract.
"""

from __future__ import annotations

import datetime
from typing import Any
from phyng.copilot.schemas import CopilotResponseContract, NextBestQuestion, HypothesisCardState


def create_copilot_response(
    user_facing_message: str,
    epistemic_mode: str,
    ladder_level: str,
    risk_level: str,
    friction_level: str,
    truth_boundary_status: str,
    allowed_uses: list[str],
    blocked_uses: list[str],
    next_best_question: NextBestQuestion | None = None,
    hypothesis_card: HypothesisCardState | None = None,
    additional_audit_notes: list[str] | None = None,
) -> CopilotResponseContract:
    """
    Construct a validated CopilotResponseContract instance.
    Includes an automatic audit log event for compliance.
    """
    card_dict = hypothesis_card.model_dump() if hypothesis_card is not None else None

    audit_event = {
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
        "epistemic_mode": epistemic_mode,
        "ladder_level": ladder_level,
        "risk_level": risk_level,
        "friction_level": friction_level,
        "truth_boundary_status": truth_boundary_status,
        "notes": additional_audit_notes or [],
    }

    return CopilotResponseContract(
        user_facing_message=user_facing_message,
        epistemic_mode=epistemic_mode,
        ladder_level=ladder_level,
        risk_level=risk_level,
        friction_level=friction_level,
        truth_boundary_status=truth_boundary_status,
        allowed_uses=allowed_uses,
        blocked_uses=blocked_uses,
        next_best_question=next_best_question,
        hypothesis_card=card_dict,
        audit_log_event=audit_event,
    )
