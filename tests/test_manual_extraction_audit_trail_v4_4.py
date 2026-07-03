from __future__ import annotations

from phyng.manual_data_extraction.audit_trail import build_audit_trail
from phyng.manual_data_extraction.loader import load_manual_extraction_inputs
from phyng.manual_data_extraction.reviewer import review_manual_queue

from tests.test_manual_data_extraction_loader_v4_4 import queue_item, write_minimal_v4_4_inputs


def test_audit_trail_records_every_decision(tmp_path) -> None:
    write_minimal_v4_4_inputs(tmp_path, [queue_item(), queue_item(target_id="TGT-2")])
    inputs = load_manual_extraction_inputs(tmp_path)
    inputs.normalized_targets["normalized_targets"].append({**inputs.normalized_targets["normalized_targets"][0], "target_id": "TGT-2"})
    reviews, accepted, rejected = review_manual_queue(inputs)

    audit = build_audit_trail(reviews, accepted, rejected)

    assert len(audit) == len(reviews)
