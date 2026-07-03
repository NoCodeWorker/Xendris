"""Rejection log for targeted literature acquisition."""

from __future__ import annotations

from phyng.source_acquisition.schemas import SourceRejectionRecord


def build_rejection_log() -> list[SourceRejectionRecord]:
    return [
        SourceRejectionRecord(
            source_candidate_id="VD-SRC-v5_7_1-REJECT-001-HORNBERGER-GERLICH-COLLOQUIUM",
            source_title_candidate="Colloquium: Quantum interference of clusters and molecules",
            rejection_reason="REVIEW_ONLY",
            notes=["Useful background review, but not prioritized as a source of new observed y_true."],
        )
    ]
