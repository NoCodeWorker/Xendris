"""Conservative promotion rules for v3.8.3."""

from __future__ import annotations

import re

from phyng.priority_packet_review.schemas import ReviewTarget

SLOT_TO_ROLE = {
    "SLOT_1_DECOHERENCE_BASELINE": "DECOHERENCE_BASELINE",
    "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE": "VISIBILITY_COHERENCE_OBSERVABLE",
    "SLOT_3_BENCHMARK_RANGES": "BENCHMARK_RANGE",
    "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS": "GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
    "SLOT_5_PARAMETER_CONSTRAINTS": "PARAMETER_CONSTRAINT",
    "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS": "NEGATIVE_CONSTRAINT_LIMITATION",
    "SLOT_7_EXPERIMENTAL_CONTEXT": "EXPERIMENTAL_CONTEXT",
}


def evaluate_promotion(target: ReviewTarget, valid_hashes: dict[str, str]) -> tuple[str, str, str | None, list[str]]:
    record = target.triage_record
    text = exact_text(target)
    if not target.source_id:
        return "REJECT_TOO_AMBIGUOUS", "missing source_id", None, []
    if record is None or not record.sha256 or valid_hashes.get(target.source_id) != record.sha256:
        return "REJECT_UNSUPPORTED_ROLE", "missing or mismatched v3.6 source hash", None, []
    if target.page_number is None:
        return "SEND_TO_MANUAL_REVIEW", "page number or exact location is missing", None, []
    if not text.strip():
        return "REJECT_GARBAGE", "empty exact text", None, []
    if _needs_manual_review(text):
        return "SEND_TO_MANUAL_REVIEW", "promising item needs nearby context or repaired formatting", None, []
    if not _legible(text):
        return "REJECT_GARBAGE", "text is not legible enough for promotion", None, []
    if target.assigned_slot == "SLOT_8_ANALOGY_ONLY_OR_BACKGROUND":
        return "CLASSIFY_ANALOGY_ONLY", "slot is analogy/background only", "ANALOGY_ONLY", ["Analogy-only material is context, not pressure."]
    role = SLOT_TO_ROLE.get(target.assigned_slot)
    if role is None:
        return "REJECT_UNSUPPORTED_ROLE", "assigned slot has no promoted component role", None, []
    if not _slot_rule_passes(target.assigned_slot, text):
        if target.assigned_slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS" and "gradient" in text.lower():
            return "CLASSIFY_ANALOGY_ONLY", "gradient appears without clear pressure-relevant dynamics", "ANALOGY_ONLY", ["Gradient reference may be apparatus-level only."]
        return "REJECT_TOO_AMBIGUOUS", "text does not cleanly answer the slot decision question", None, []
    limitations = [
        "Validation-ready only; v3.8.3 does not grant source support.",
        "Requires v3.9 source-pressure judgment against PHI_GRADIENT.",
    ]
    return "PROMOTE_VALIDATION_READY", f"clean traceable extract for {role}", role, limitations


def exact_text(target: ReviewTarget) -> str:
    if target.triage_record is not None:
        return target.triage_record.extracted_text
    return target.exact_text_or_preview


def pressure_direction(slot: str) -> str:
    if slot == "SLOT_1_DECOHERENCE_BASELINE":
        return "BASELINE_CANDIDATE"
    if slot == "SLOT_3_BENCHMARK_RANGES":
        return "BENCHMARK_CANDIDATE"
    if slot == "SLOT_5_PARAMETER_CONSTRAINTS":
        return "PARAMETER_CONSTRAINT_CANDIDATE"
    if slot == "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS":
        return "CONTRADICTION_CANDIDATE"
    if slot == "SLOT_8_ANALOGY_ONLY_OR_BACKGROUND":
        return "ANALOGY_ONLY"
    return "SUPPORT_CANDIDATE"


def _legible(text: str) -> bool:
    normalized = " ".join(text.split())
    if len(normalized) < 35:
        return False
    alpha = sum(char.isalpha() for char in normalized)
    return alpha / max(len(normalized), 1) > 0.45


def _needs_manual_review(text: str) -> bool:
    normalized = " ".join(text.split())
    if len(normalized) < 50 and any(symbol in normalized for symbol in ["=", "<", ">", "λ", "^"]):
        return True
    if normalized.count("(") != normalized.count(")"):
        return True
    return False


def _slot_rule_passes(slot: str, text: str) -> bool:
    lowered = text.lower()
    if slot == "SLOT_1_DECOHERENCE_BASELINE":
        return any(term in lowered for term in ["decoherence", "thermal emission", "scattering", "loss of coherence"])
    if slot == "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE":
        return any(term in lowered for term in ["visibility", "contrast", "coherence loss", "interference"])
    if slot == "SLOT_3_BENCHMARK_RANGES":
        return bool(re.search(r"\d", lowered)) and any(term in lowered for term in ["mass", "time", "temperature", "pressure", "mbar", "amu", "nm", " k", "setup", "regime"])
    if slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS":
        return "gradient" in lowered and any(term in lowered for term in ["motional", "spin-motion", "hamiltonian", "operator", "effective dynamics", "transition"])
    if slot == "SLOT_5_PARAMETER_CONSTRAINTS":
        return any(term in lowered for term in ["csl", "mmm", "collapse", "lambda", "r_c", "bound", "constraint", "hypothesis"])
    if slot == "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS":
        return any(term in lowered for term in ["negligible", "dominates", "limitation", "noise", "background", "excluded", "incompatible", "falsify"])
    if slot == "SLOT_7_EXPERIMENTAL_CONTEXT":
        return any(term in lowered for term in ["experiment", "setup", "interferometer", "talbot", "matter-wave", "nanodiamond"])
    return False
