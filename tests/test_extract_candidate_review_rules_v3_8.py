from __future__ import annotations

from phyng.extract_candidate_review.review_rules import review_candidate
from phyng.extract_candidate_review.schemas import RawExtractionCandidate

from tests.test_extract_candidate_review_loader_v3_8 import raw_candidate


def test_empty_or_noise_candidate_rejected() -> None:
    candidate = RawExtractionCandidate(**raw_candidate(candidate_id="NOISE", extracted_text="\x01\x02\x03", normalized_text="\x01\x02\x03"))

    reviewed, rejected, queue, _ = review_candidate(candidate)

    assert reviewed is None
    assert rejected is not None
    assert rejected.review_status == "REVIEWED_CANDIDATE_REJECTED_GARBAGE"
    assert queue is None


def test_candidate_with_source_hash_and_location_can_be_validation_ready() -> None:
    candidate = RawExtractionCandidate(**raw_candidate(requires_manual_review=False))

    reviewed, rejected, queue, _ = review_candidate(candidate)

    assert reviewed is not None
    assert reviewed.validation_ready is True
    assert reviewed.sha256 == "abc123"
    assert rejected is None
    assert queue is None


def test_ambiguous_equation_candidate_requires_manual_review() -> None:
    candidate = RawExtractionCandidate(
        **raw_candidate(
            candidate_id="EQ-1",
            candidate_type="EQUATION_CANDIDATE",
            extracted_text="Gamma = lambda times mass controls decoherence rate.",
            normalized_text="gamma = lambda times mass controls decoherence rate.",
            requires_manual_review=True,
        )
    )

    reviewed, rejected, queue, _ = review_candidate(candidate)

    assert reviewed is not None
    assert reviewed.validation_ready is False
    assert rejected is None
    assert queue is not None
    assert "equation formatting" in queue.reason
