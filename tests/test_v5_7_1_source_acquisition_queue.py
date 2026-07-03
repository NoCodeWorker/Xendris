from phyng.source_acquisition.candidate_sources import build_candidate_sources


def test_log_boundary_remains_archived():
    queue = build_candidate_sources()

    assert queue
    assert all(item.acquisition_id.startswith("VD-SRC-v5_7_1") for item in queue)


def test_no_ytrue_extracted():
    queue = build_candidate_sources()

    assert all("y_true" not in item.model_dump() for item in queue)


def test_source_acquisition_is_not_evidence():
    queue = build_candidate_sources()

    assert all("evidence" not in item.reason_for_relevance.lower() for item in queue)
