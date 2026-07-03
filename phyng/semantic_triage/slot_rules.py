"""Slot assignment rules for v3.8.2 semantic triage."""

from __future__ import annotations

SLOT_1_DECOHERENCE_BASELINE = "SLOT_1_DECOHERENCE_BASELINE"
SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE = "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE"
SLOT_3_BENCHMARK_RANGES = "SLOT_3_BENCHMARK_RANGES"
SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS = "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"
SLOT_5_PARAMETER_CONSTRAINTS = "SLOT_5_PARAMETER_CONSTRAINTS"
SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS = "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS"
SLOT_7_EXPERIMENTAL_CONTEXT = "SLOT_7_EXPERIMENTAL_CONTEXT"
SLOT_8_ANALOGY_ONLY_OR_BACKGROUND = "SLOT_8_ANALOGY_ONLY_OR_BACKGROUND"

ALL_SLOTS = [
    SLOT_1_DECOHERENCE_BASELINE,
    SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE,
    SLOT_3_BENCHMARK_RANGES,
    SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS,
    SLOT_5_PARAMETER_CONSTRAINTS,
    SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS,
    SLOT_7_EXPERIMENTAL_CONTEXT,
    SLOT_8_ANALOGY_ONLY_OR_BACKGROUND,
]

SLOT_KEYWORDS = {
    SLOT_1_DECOHERENCE_BASELINE: [
        "decoherence",
        "collisional decoherence",
        "thermal emission",
        "environmental decoherence",
        "scattering",
        "decoherence rate",
        "loss of coherence",
    ],
    SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE: [
        "visibility",
        "fringe visibility",
        "contrast",
        "interference visibility",
        "coherence loss",
        "interferometer signal",
    ],
    SLOT_3_BENCHMARK_RANGES: [
        "mass",
        "amu",
        "molecule",
        "cluster",
        "nanoparticle",
        "time",
        "separation",
        "distance",
        "temperature",
        "pressure",
        "mbar",
        " k",
        "seconds",
    ],
    SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS: [
        "gradient",
        "field gradient",
        "magnetic field gradient",
        "transition",
        "effective dynamics",
        "hamiltonian",
        "operator",
        "motional dynamical decoupling",
        "spin-motion coupling",
        "motional state",
    ],
    SLOT_5_PARAMETER_CONSTRAINTS: [
        "csl",
        "collapse",
        "lambda",
        "r_c",
        "parameter",
        "constraint",
        "bound",
        "exclusion",
        "bayesian",
        "hypothesis test",
        "macrorealistic modification",
        "mmm",
    ],
    SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS: [
        "negligible",
        "dominates",
        "excluded",
        "ruled out",
        "limitation",
        "noise",
        "background",
        "thermal",
        "environmental",
        "incompatible",
        "falsify",
    ],
    SLOT_7_EXPERIMENTAL_CONTEXT: [
        "setup",
        "experiment",
        "interferometer",
        "kdtli",
        "lumi",
        "talbot",
        "kapitza-dirac",
        "nanodiamond",
        "matter-wave",
    ],
}


def assign_slot(text: str, source_id: str = "") -> str:
    lowered = f"{source_id} {text}".lower()
    weighted_hits = {slot: _keyword_hits(lowered, keywords) for slot, keywords in SLOT_KEYWORDS.items()}
    if source_id == "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING" and weighted_hits[SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS]:
        return SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
    if source_id == "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS" and weighted_hits[SLOT_5_PARAMETER_CONSTRAINTS]:
        return SLOT_5_PARAMETER_CONSTRAINTS
    if source_id == "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST" and weighted_hits[SLOT_5_PARAMETER_CONSTRAINTS]:
        return SLOT_5_PARAMETER_CONSTRAINTS
    slot, hits = max(weighted_hits.items(), key=lambda item: item[1])
    if hits <= 0:
        return SLOT_8_ANALOGY_ONLY_OR_BACKGROUND
    return slot


def slot_keyword_hit_ratio(text: str, slot: str) -> float:
    keywords = SLOT_KEYWORDS.get(slot, [])
    if not keywords:
        return 0.4
    hits = _keyword_hits(text.lower(), keywords)
    return min(1.0, hits / 2.0)


def _keyword_hits(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)
