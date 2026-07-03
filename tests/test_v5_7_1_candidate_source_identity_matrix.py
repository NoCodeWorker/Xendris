from phyng.source_acquisition.candidate_sources import build_candidate_sources
from phyng.source_acquisition.identity_matrix import build_identity_matrix
from phyng.source_acquisition.schemas import SourceAcquisitionQueueItem


def test_raw_title_only_source_not_complete():
    raw = SourceAcquisitionQueueItem(
        acquisition_id="RAW",
        priority="LOW",
        source_title_candidate="Raw title only",
        reason_for_relevance="test",
        source_identity_status="RAW_REF_ONLY",
        availability_status="UNKNOWN",
        manual_action_required="lookup",
    )
    matrix = build_identity_matrix([raw])

    assert matrix[0].identity_complete is False
    assert "authors_or_publication_authority" in matrix[0].missing_identity_fields


def test_resolved_source_requires_stable_identity():
    matrix = build_identity_matrix(build_candidate_sources())

    assert len(matrix) >= 3
    assert all(item.identity_complete for item in matrix)
    assert all(item.doi or item.arxiv or item.url for item in matrix)
