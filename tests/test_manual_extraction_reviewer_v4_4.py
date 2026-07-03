from __future__ import annotations

from phyng.manual_data_extraction.loader import load_manual_extraction_inputs
from phyng.manual_data_extraction.reviewer import review_manual_queue

from tests.test_manual_data_extraction_loader_v4_4 import queue_item, write_minimal_v4_4_inputs


def test_accepted_ytrue_requires_prediction_match_for_gain(tmp_path) -> None:
    write_minimal_v4_4_inputs(tmp_path, [queue_item()])
    inputs = load_manual_extraction_inputs(tmp_path)

    _, accepted, rejected = review_manual_queue(inputs)

    assert len(accepted) == 1
    assert accepted[0].matched_prediction_ids
    assert rejected == []
