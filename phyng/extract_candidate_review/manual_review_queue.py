"""Manual review queue helpers."""

from __future__ import annotations

from phyng.extract_candidate_review.schemas import ManualReviewQueueItem


PEDERNALES_SOURCE_ID = "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING"


def build_pedernales_manual_review_item(extraction_manifest: dict) -> ManualReviewQueueItem | None:
    for summary in extraction_manifest.get("source_summaries", []):
        if summary.get("source_id") != PEDERNALES_SOURCE_ID:
            continue
        if summary.get("extraction_status") == "EXTRACTION_REQUIRES_PDF_READER_OR_MANUAL_REVIEW":
            return ManualReviewQueueItem(
                candidate_id="MANUAL-PEDERNALES-SLOT-4-GRADIENT-COMPONENT",
                source_id=PEDERNALES_SOURCE_ID,
                page_number=None,
                candidate_type="SOURCE_EXTRACTION_BLOCKED",
                text_preview="PDF extraction blocked for Pedernales source.",
                reason="PDF extraction blocked; SLOT_4 gradient-component bottleneck.",
                priority="HIGH",
                suggested_action="Install pypdf/pdfplumber or manually extract relevant gradient/transition passages.",
            )
    return None
