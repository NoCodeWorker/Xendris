from phyng.source_acquisition.rejection_log import build_rejection_log


def test_rejection_log_records_review_only_sources():
    log = build_rejection_log()

    assert log
    assert log[0].rejection_reason == "REVIEW_ONLY"
