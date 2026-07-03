"""
Phygn v1.9 — Business post-mortem retrospect evaluator

Audits completed business model experiments and gate appropriateness.
"""

from __future__ import annotations

import uuid
from phyng.business_validation.schemas import BusinessPostMortem


def create_business_post_mortem(
    hypothesis_id: str,
    test_summary: str,
    expected_result: str,
    actual_result: str,
    gate_decision: str,
    was_gate_too_strict: bool = False,
    was_gate_too_loose: bool = False,
    next_decision: str = "Pivot",
) -> BusinessPostMortem:
    """
    Construct a validated BusinessPostMortem instance.
    """
    return BusinessPostMortem(
        post_mortem_id=f"PM-BUS-{uuid.uuid4().hex[:8].upper()}",
        hypothesis_id=hypothesis_id,
        test_summary=test_summary,
        expected_result=expected_result,
        actual_result=actual_result,
        gate_decision=gate_decision,
        was_gate_too_strict=was_gate_too_strict,
        was_gate_too_loose=was_gate_too_loose,
        next_decision=next_decision
    )
