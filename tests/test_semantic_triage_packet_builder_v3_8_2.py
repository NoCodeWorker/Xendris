from __future__ import annotations

from phyng.extract_candidate_review.schemas import RawExtractionCandidate
from phyng.semantic_triage.packet_builder import build_low_value_exclusions, build_priority_packet
from phyng.semantic_triage.prioritizer import triage_candidates


def test_packet_size_is_capped() -> None:
    records = triage_candidates([_candidate(index) for index in range(80)])

    packet = build_priority_packet(records, limit=60)

    assert len(packet) == 60


def test_low_value_candidates_excluded() -> None:
    candidate = RawExtractionCandidate(
        candidate_id="LOW-1",
        source_id="SRC-TEST",
        sha256="abc123",
        page_number=1,
        location_type="PAGE_TEXT",
        location_value="page=1",
        candidate_type="QUOTE_CANDIDATE",
        extracted_text="x y z",
        normalized_text="x y z",
    )
    records = triage_candidates([candidate])

    exclusions = build_low_value_exclusions(records)

    assert exclusions
    assert exclusions[0].candidate_id == "LOW-1"


def test_priority_packet_does_not_grant_support() -> None:
    records = triage_candidates([_candidate(1)])
    packet = build_priority_packet(records)

    assert packet
    assert "support" not in packet[0].next_gate_impact.lower()
    assert "v3.8.3" in packet[0].next_gate_impact


def _candidate(index: int) -> RawExtractionCandidate:
    return RawExtractionCandidate(
        candidate_id=f"CAND-{index}",
        source_id="SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
        sha256="h5",
        page_number=index,
        location_type="PAGE_TEXT",
        location_value=f"page={index}",
        candidate_type="QUOTE_CANDIDATE",
        extracted_text="The magnetic field gradient produces spin-motion coupling and effective dynamics in the motional state.",
        normalized_text="the magnetic field gradient produces spin-motion coupling and effective dynamics in the motional state.",
    )
