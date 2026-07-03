from __future__ import annotations

from phyng.manual_data_extraction.dataset_update import build_updated_dataset
from phyng.manual_data_extraction.loader import load_manual_extraction_inputs
from phyng.manual_data_extraction.reviewer import review_manual_queue

from tests.test_manual_data_extraction_loader_v4_4 import queue_item, write_minimal_v4_4_inputs


def test_predictive_gain_ready_requires_three_records(tmp_path) -> None:
    queue = [queue_item(target_id=f"TGT-{i}") for i in range(1, 4)]
    write_minimal_v4_4_inputs(tmp_path, queue)
    inputs = load_manual_extraction_inputs(tmp_path)
    base_target = inputs.normalized_targets["normalized_targets"][0]
    inputs.normalized_targets["normalized_targets"] = [
        {**base_target, "target_id": f"TGT-{i}", "benchmark_id": "BM-1"} for i in range(1, 4)
    ]

    _, accepted, _ = review_manual_queue(inputs)
    dataset = build_updated_dataset(inputs, accepted)

    assert len(accepted) == 3
    assert dataset.ready_for_predictive_gain is True
