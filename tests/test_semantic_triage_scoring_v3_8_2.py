from __future__ import annotations

from phyng.extract_candidate_review.schemas import RawExtractionCandidate
from phyng.semantic_triage.prioritizer import triage_candidate


def test_pedernales_slot4_gets_minimum_high_priority() -> None:
    candidate = RawExtractionCandidate(
        candidate_id="PED-1",
        source_id="SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
        sha256="h5",
        page_number=3,
        location_type="PAGE_TEXT",
        location_value="page=3",
        candidate_type="QUOTE_CANDIDATE",
        extracted_text="A magnetic field gradient couples the spin and motional state in the Hamiltonian.",
        normalized_text="a magnetic field gradient couples the spin and motional state in the hamiltonian.",
    )

    record = triage_candidate(candidate)

    assert record.assigned_slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"
    assert record.priority in {"HIGH", "CRITICAL"}
    assert record.include_in_priority_packet is True
