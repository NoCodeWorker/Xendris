from phyng.frontera_c_disposition.candidate_disposition import build_candidate_disposition
from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs


def test_log_boundary_archived_as_validation_candidate():
    review = build_control_failure_review(load_control_failure_inputs("."))
    disposition = build_candidate_disposition(review)

    assert disposition.primary_disposition == "ARCHIVE_AS_VALIDATION_CANDIDATE"
    assert disposition.archived_as_validation_candidate is True


def test_reopen_requires_independent_sources_and_more_ytrue():
    review = build_control_failure_review(load_control_failure_inputs("."))
    disposition = build_candidate_disposition(review)

    assert "at least 2 independent sources" in disposition.required_to_reopen_as_candidate
    assert "at least 10 accepted y_true records" in disposition.required_to_reopen_as_candidate
    assert "negative controls survive" in disposition.required_to_reopen_as_candidate
