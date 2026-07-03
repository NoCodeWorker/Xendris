"""Tests for v4.3 assembled dataset quality report."""

from __future__ import annotations

from phyng.ytrue_extraction.quality_report import build_quality_report
from phyng.ytrue_extraction.schemas import QueueItem


def test_quality_report_summarises_accurately() -> None:
    targets = [{"target_id": "TGT-1"}]
    candidates = [
        {
            "target_id": "TGT-1",
            "can_enter_dataset": False,
            "qc_status": "FAIL",
        }
    ]
    blocked_list = [{"target_id": "TGT-1"}]
    table_q: list[QueueItem] = []
    fig_q: list[QueueItem] = []
    pub_q: list[QueueItem] = []
    supp_q: list[QueueItem] = []

    q = build_quality_report(
        targets,
        candidates,
        blocked_list,
        table_q,
        fig_q,
        pub_q,
        supp_q,
        accepted_count=0,
        ready_for_predictive_gain=False,
    )
    assert q.target_count == 1
    assert q.candidate_count == 1
    assert q.accepted_y_true_count == 0
    assert q.blocked_count == 1
    assert q.readiness_status == "YTRUE_DATASET_EMPTY_NEEDS_EXTRACTION"
