"""Classify validation-ready extracts into pressure classes for v3.9."""

from __future__ import annotations

import re

from phyng.source_pressure_decision.schemas import (
    ExtractPressureRecord,
    SOURCE_WEIGHTS,
)


def classify_extract(extract: dict, source_hashes: dict) -> ExtractPressureRecord:
    """Classify a single validation-ready extract into a pressure class."""
    slot = extract.get("assigned_slot", "")
    role = extract.get("component_role", "")
    text = extract.get("exact_text", "").lower()
    source_id = extract.get("source_id", "")
    direction = extract.get("possible_pressure_direction", "SUPPORT_CANDIDATE")
    weight = SOURCE_WEIGHTS.get(source_id, 0.5)

    pressure_class, reasoning, can_support, can_contradict = _classify(slot, role, text, direction)
    score = _score(pressure_class, weight)
    confidence = _confidence(pressure_class, text, slot)

    return ExtractPressureRecord(
        extract_id=extract.get("extract_id", ""),
        source_id=source_id,
        sha256=extract.get("sha256", ""),
        page_number=extract.get("page_number"),
        assigned_slot=slot,
        component_role=role,
        exact_text=extract.get("exact_text", ""),
        pressure_class=pressure_class,
        pressure_direction=direction,
        pressure_score=score,
        confidence=confidence,
        reasoning=reasoning,
        limitations=extract.get("limitations", []),
        can_support_claim=can_support,
        can_contradict_claim=can_contradict,
    )


def _classify(slot: str, role: str, text: str, direction: str) -> tuple[str, str, bool, bool]:
    """Return (pressure_class, reasoning, can_support, can_contradict)."""
    # Negative/contradiction slots take priority per rule 6.
    if slot == "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS":
        if any(term in text for term in ["incompatible", "excluded", "falsif", "dominates"]):
            return "CONTRADICTS_COMPONENT", "extract contains direct negative constraint", False, True
        if any(term in text for term in ["negligible", "limitation", "noise", "background"]):
            return "LIMITS_COMPONENT", "extract contains limitation language", False, True
        return "LIMITS_COMPONENT", "slot is negative-constraints/limitations", False, True

    if role == "ANALOGY_ONLY":
        return "ANALOGY_ONLY", "role is analogy-only", False, False

    if slot == "SLOT_1_DECOHERENCE_BASELINE":
        return "SUPPORTS_BASELINE_ONLY", "extract aligns with decoherence baseline", True, False

    if slot == "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE":
        return "SUPPORTS_OBSERVABLE_ONLY", "extract aligns with visibility/coherence observable", True, False

    if slot == "SLOT_3_BENCHMARK_RANGES":
        return "SUPPORTS_BENCHMARK_ALIGNMENT", "extract provides benchmark range data", True, False

    if slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS":
        if any(term in text for term in ["gradient", "transition", "effective dynamics", "spin-motion", "hamiltonian"]):
            return "SUPPORTS_GRADIENT_COMPONENT", "extract provides gradient-component dynamics", True, False
        return "INCONCLUSIVE", "slot 4 extract lacks gradient-specific dynamics language", False, False

    if slot == "SLOT_5_PARAMETER_CONSTRAINTS":
        return "SUPPORTS_PARAMETER_CONSTRAINT", "extract constrains model parameters", True, False

    if slot == "SLOT_7_EXPERIMENTAL_CONTEXT":
        if _has_benchmark_data(text):
            return "SUPPORTS_BENCHMARK_ALIGNMENT", "experimental context with benchmark-relevant data", True, False
        return "INCONCLUSIVE", "experimental context without clear pressure direction", False, False

    return "INCONCLUSIVE", "extract could not be cleanly classified", False, False


def _score(pressure_class: str, weight: float) -> float:
    """Compute a pressure score: positive for support, negative for contradiction/limitation."""
    base_scores = {
        "SUPPORTS_BASELINE_ONLY": 0.3,
        "SUPPORTS_OBSERVABLE_ONLY": 0.4,
        "SUPPORTS_BENCHMARK_ALIGNMENT": 0.5,
        "SUPPORTS_PARAMETER_CONSTRAINT": 0.4,
        "SUPPORTS_GRADIENT_COMPONENT": 0.8,
        "CONTRADICTS_COMPONENT": -0.9,
        "LIMITS_COMPONENT": -0.5,
        "ANALOGY_ONLY": 0.0,
        "INCONCLUSIVE": 0.0,
        "IRRELEVANT_AFTER_REVIEW": 0.0,
    }
    return round(base_scores.get(pressure_class, 0.0) * weight, 4)


def _confidence(pressure_class: str, text: str, slot: str) -> str:
    """Default LOW unless the alignment is direct and slot coverage is strong."""
    if pressure_class in ("INCONCLUSIVE", "ANALOGY_ONLY", "IRRELEVANT_AFTER_REVIEW"):
        return "LOW"
    if pressure_class in ("CONTRADICTS_COMPONENT", "LIMITS_COMPONENT"):
        return "MEDIUM"
    word_count = len(text.split())
    if word_count > 20 and pressure_class.startswith("SUPPORTS_"):
        return "MEDIUM"
    return "LOW"


def _has_benchmark_data(text: str) -> bool:
    return bool(re.search(r"\d", text)) and any(
        term in text for term in ["mass", "time", "temperature", "pressure", "mbar", "amu", "nm", "setup"]
    )
