from __future__ import annotations

from phyng.extract_candidate_review.role_assignment import assign_component_role
from phyng.extract_candidate_review.schemas import RawExtractionCandidate

from tests.test_extract_candidate_review_loader_v3_8 import raw_candidate


def test_component_role_assigned_conservatively() -> None:
    gradient = RawExtractionCandidate(
        **raw_candidate(
            extracted_text="The effective gradient transition modifies decoherence rate in interferometry dynamics.",
            normalized_text="the effective gradient transition modifies decoherence rate in interferometry dynamics.",
        )
    )
    analogy = RawExtractionCandidate(
        **raw_candidate(
            extracted_text="A magnetic field gradient is present in the apparatus.",
            normalized_text="a magnetic field gradient is present in the apparatus.",
        )
    )

    assert assign_component_role(gradient) == "GRADIENT_COMPONENT"
    assert assign_component_role(analogy) == "ANALOGY_ONLY"
