"""
Strict classification enums for Frontera C v0.3.

Every claim, trace, and layer must be explicitly typed.
No ambiguity. No mixing categories.
"""

from enum import Enum


class ClaimType(str, Enum):
    """Classification of epistemic claims."""
    DEFINITION = "DEFINITION"
    AXIOM = "AXIOM"
    STRUCTURAL_LEMMA = "STRUCTURAL_LEMMA"
    HYPOTHESIS = "HYPOTHESIS"
    MODEL = "MODEL"
    BENCHMARK = "BENCHMARK"
    NEGATIVE_BOUND = "NEGATIVE_BOUND"
    SPECULATIVE_EXTENSION = "SPECULATIVE_EXTENSION"


class TraceType(str, Enum):
    """Classification of epistemic traces."""
    NULL_TRACE = "NULL_TRACE"
    STRUCTURAL_TRACE = "STRUCTURAL_TRACE"
    THEORETICAL_TRACE = "THEORETICAL_TRACE"
    DETECTABLE_TRACE = "DETECTABLE_TRACE"
    PREDICTIVE_TRACE = "PREDICTIVE_TRACE"
    NEGATIVE_BOUND_TRACE = "NEGATIVE_BOUND_TRACE"
    BLOCKED = "BLOCKED"


class Layer(str, Enum):
    """Architectural layers of the Frontera C framework."""
    PHYSICAL_CORE = "PHYSICAL_CORE"
    ONTO_EPISTEMIC_CORE = "ONTO_EPISTEMIC_CORE"
    QUANTUM_CHANNEL_CORE = "QUANTUM_CHANNEL_CORE"
    APPLICATION_TRACK = "APPLICATION_TRACK"
    COGNITIVE_EXTENSION = "COGNITIVE_EXTENSION"
    SPECULATIVE_ONLY = "SPECULATIVE_ONLY"
