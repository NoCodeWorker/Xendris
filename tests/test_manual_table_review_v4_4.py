from __future__ import annotations

from phyng.manual_data_extraction.table_review import can_accept, review_queue_item

from tests.test_manual_data_extraction_loader_v4_4 import queue_item, target


def test_manual_review_requires_source_hash() -> None:
    review = review_queue_item(queue_item(), 1, {"TGT-1": target()}, {}, extracted_value_text="0.4")

    assert review.reviewer_decision == "SEND_TO_HUMAN_REVIEW"
    assert "MISSING_SOURCE_HASH" in review.blockers


def test_manual_review_requires_location() -> None:
    review = review_queue_item(queue_item(source_location_hint="Page unknown of local PDF."), 1, {"TGT-1": target()}, _hashes(), extracted_value_text="0.4")

    assert review.reviewer_decision == "REJECT_MISSING_LOCATION"


def test_manual_review_rejects_prose_only_visibility() -> None:
    review = review_queue_item(queue_item(), 1, {"TGT-1": target()}, _hashes(), extracted_value_text="and thus halve the interference visibility")

    assert review.reviewer_decision == "REJECT_PROSE_ONLY"


def test_manual_review_rejects_missing_unit_for_rate() -> None:
    item = queue_item(observable_class="DECOHERENCE_RATE")
    review = review_queue_item(item, 1, {"TGT-1": target(observable_class="DECOHERENCE_RATE")}, _hashes(), extracted_value_text="rate 2.4")

    assert review.reviewer_decision == "REJECT_MISSING_UNIT"


def test_manual_review_accepts_valid_dimensionless_visibility() -> None:
    review = review_queue_item(queue_item(), 1, {"TGT-1": target()}, _hashes(), extracted_value_text="visibility 0.42")

    assert can_accept(review)
    assert review.unit == "dimensionless"


def test_manual_review_accepts_valid_decoherence_rate() -> None:
    item = queue_item(observable_class="DECOHERENCE_RATE")
    review = review_queue_item(item, 1, {"TGT-1": target(observable_class="DECOHERENCE_RATE")}, _hashes(), extracted_value_text="decoherence rate 2.4 s^-1")

    assert can_accept(review)
    assert review.unit == "s^-1"


def _hashes() -> dict[str, dict]:
    return {"SRC-TEST": {"sha256": "abc123", "local_path": "data/real_sources/pdfs/test.pdf"}}
