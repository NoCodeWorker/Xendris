"""
Phygn v1.3 — Real Source Candidates

Defines the RealSourceCandidate schema and registry.
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

VerificationStatus = Literal[
    "CANDIDATE_ONLY",
    "NEEDS_LOCAL_FILE",
    "NEEDS_METADATA_VERIFICATION",
    "READY_FOR_MANIFEST_DRAFT",
    "READY_FOR_EXTRACTION",
]

LocalFileStatus = Literal["MISSING", "PRESENT"]

class RealSourceCandidate(BaseModel):
    source_candidate_id: str
    slot: str
    title: str | None
    authors: list[str]
    year: str | None
    url: str | None
    intended_support_types: list[str]
    trust_level: str
    verification_status: VerificationStatus = "CANDIDATE_ONLY"
    local_file_status: LocalFileStatus = "MISSING"
    notes: str

# Defined based on docs/75_PHYGN_BASELINE_REAL_SOURCE_CANDIDATES.md
CANDIDATE_DATA = [
    {
        "source_candidate_id": "SRC-BASE-DECOH-001",
        "slot": "SRC-BASE-DECOH-001",
        "title": "Decoherence, the measurement problem, and interpretations of quantum mechanics",
        "authors": ["Maximilian Schlosshauer"],
        "year": "2003",
        "url": "https://arxiv.org/abs/quant-ph/0312059",
        "intended_support_types": ["CONTEXT_SUPPORT", "ASSUMPTION_SUPPORT", "FORMULA_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "READY_FOR_MANIFEST_DRAFT",
        "local_file_status": "MISSING",
        "notes": "Candidate. Verify local file and extract exact support before audit."
    },
    {
        "source_candidate_id": "SRC-BASE-DECOH-002",
        "slot": "SRC-BASE-DECOH-001",
        "title": "Environment--Induced Decoherence, Classicality and Consistency of Quantum Histories",
        "authors": ["Juan Pablo Paz", "Wojciech Hubert Zurek"],
        "year": "1993",
        "url": "https://arxiv.org/abs/gr-qc/9304031",
        "intended_support_types": ["CONTEXT_SUPPORT", "ASSUMPTION_SUPPORT", "PARAMETER_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "READY_FOR_MANIFEST_DRAFT",
        "local_file_status": "MISSING",
        "notes": "Candidate. Use only for claims explicitly supported by extract."
    },
    {
        "source_candidate_id": "SRC-BASE-MWI-001",
        "slot": "SRC-BASE-MWI-001",
        "title": "Macroscopic quantum resonators (MAQRO)",
        "authors": ["Rainer Kaltenbaek", "Gerald Hechenblaikner", "Nikolai Kiesel", "Oriol Romero-Isart", "Keith C. Schwab", "Ulrich Johann", "Markus Aspelmeyer"],
        "year": "2012",
        "url": "https://arxiv.org/abs/1201.4756",
        "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "READY_FOR_MANIFEST_DRAFT",
        "local_file_status": "MISSING",
        "notes": "Candidate for MAQRO/mesoscopic context and visibility-decoherence connection."
    },
    {
        "source_candidate_id": "SRC-BASE-MWI-002",
        "slot": "SRC-BASE-MWI-001",
        "title": "Macroscopic Quantum Resonators (MAQRO): 2015 update",
        "authors": [],
        "year": "2015",
        "url": "https://arxiv.org/abs/1503.02640",
        "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "NEEDS_METADATA_VERIFICATION",
        "local_file_status": "MISSING",
        "notes": "Candidate. Verify full authors and support locally before audit."
    },
    {
        "source_candidate_id": "SRC-BASE-VIS-001",
        "slot": "SRC-BASE-VIS-001",
        "title": None,
        "authors": [],
        "year": "2024",
        "url": "https://arxiv.org/pdf/2410.20910",
        "intended_support_types": ["OBSERVABLE_SUPPORT", "CONTEXT_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "NEEDS_METADATA_VERIFICATION",
        "local_file_status": "MISSING",
        "notes": "Candidate for visibility loss/contrast from matter-wave decoherence/dephasing. Verify metadata."
    },
    {
        "source_candidate_id": "SRC-BASE-VIS-002",
        "slot": "SRC-BASE-VIS-001",
        "title": "Decoherence in a Talbot-Lau interferometer: the influence of molecular scattering",
        "authors": [],
        "year": None,
        "url": None,
        "intended_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT", "BENCHMARK_SUPPORT"],
        "trust_level": "HIGH",
        "verification_status": "NEEDS_METADATA_VERIFICATION",
        "local_file_status": "MISSING",
        "notes": "Candidate for exponential decrease of fringe visibility. Verify bibliographic metadata and source URL."
    },
    {
        "source_candidate_id": "SRC-BASE-EXP-001",
        "slot": "SRC-BASE-MWI-001",
        "title": "Experimental decoherence in molecule interferometry",
        "authors": ["Markus Arndt"],
        "year": "2021",
        "url": "https://arxiv.org/abs/2101.08216",
        "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT", "EXPERIMENTAL_CONTEXT"],
        "trust_level": "HIGH",
        "verification_status": "READY_FOR_MANIFEST_DRAFT",
        "local_file_status": "MISSING",
        "notes": "Candidate. Verify full authors and explicit support."
    }
]

def get_baseline_real_source_candidates() -> list[RealSourceCandidate]:
    """
    Returns the list of real source candidates defined in the protocol.
    """
    return [RealSourceCandidate(**data) for data in CANDIDATE_DATA]
