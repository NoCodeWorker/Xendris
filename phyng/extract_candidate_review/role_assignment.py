"""Conservative component-role assignment for extraction candidates."""

from __future__ import annotations

from phyng.extract_candidate_review.schemas import RawExtractionCandidate


def assign_component_role(candidate: RawExtractionCandidate) -> str:
    text = f"{candidate.candidate_type} {candidate.extracted_text} {candidate.normalized_text or ''}".lower()
    if any(term in text for term in ("negligible", "excluded", "ruled out", "dominates", "background", "mismatch")):
        return "NEGATIVE_CONSTRAINT"
    if any(term in text for term in ("limitation", "limited")):
        return "LIMITATION"
    if "gradient" in text or "transition" in text or "effective operator" in text or "effective dynamics" in text:
        if any(term in text for term in ("decoherence", "rate", "visibility", "interferometer", "interferometry", "dynamics")):
            return "GRADIENT_COMPONENT"
        return "ANALOGY_ONLY"
    if any(term in text for term in ("csl", "collapse", "bound", "constraint", "exclusion", "lambda", "bayesian", "hypothesis")):
        return "PARAMETER_CONSTRAINT"
    if any(term in text for term in ("mass", "amu", "separation", "distance", "temperature", "pressure", "matter-wave", "interferometry constraints", "benchmark")):
        return "BENCHMARK_MODEL"
    if any(term in text for term in ("fringe visibility", "contrast", "interference visibility", "loss of coherence", "observed decoherence", "visibility")):
        return "VISIBILITY_DECAY_OBSERVABLE"
    if any(term in text for term in ("decoherence rate", "environmental decoherence", "collisional decoherence", "thermal emission", "scattering", "decoherence")):
        return "DECOHERENCE_BASELINE"
    return "REQUIRES_MANUAL_REVIEW"
