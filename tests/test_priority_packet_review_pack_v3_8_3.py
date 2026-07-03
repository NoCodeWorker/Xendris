from __future__ import annotations

from phyng.priority_packet_review.validation_ready_pack import build_validation_ready_pack


def test_ready_for_v3_9_requires_validation_ready_extract() -> None:
    pack = build_validation_ready_pack([], [], [], [], "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS", [])

    assert pack.validation_ready_count == 0
    assert pack.ready_for_v3_9 is False
