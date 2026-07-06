"""FirstPrinciplesGuard — checks if scientific/technical claims are consistent with first principles."""
from __future__ import annotations

import re
from xendris.core.council.models import GuardResult, GuardOutput

# First-principles consistency violations
_PRINCIPLE_VIOLATIONS = [
    (r"\bperpetual motion\b", "Conservation of energy violation"),
    (r"\bfaster than light\b.*\b(?:information|communication|causality)\b", "Causality violation"),
    (r"\b(?:free energy|zero[-\s]?point energy)\b(?!\s*(?:hypothesis|proposed|theoretical))", "Energy conservation violation"),
    (r"\b(?:time travel|backward.*time)\b(?!\s*(?:fiction|hypothetical|thought experiment))", "Causality violation"),
    (r"\b(?:cold fusion|low[-\s]?energy.*fusion)\b(?!\s*(?:hypothesis|proposed|controversial|claimed))", "Known unverified claim"),
    (r"\b(?:prove|disprove)\s+(?:god|soul|afterlife|consciousness)\b", "Beyond scientific scope"),
]

_SCIENTIFIC_DOMAIN_KEYWORDS = [
    "physic", "chemist", "biolog", "quantum", "relativity",
    "thermodynamic", "conservation", "entropy", "energy",
    "scientific", "experiment", "theory", "law of",
    "natural law", "fundamental", "principle",
    "motion", "force", "gravity", "mass", "velocity",
    "temperature", "pressure", "volume", "density",
    "light", "wave", "particle", "field", "radiation",
    "molecular", "atomic", "nuclear", "genetic",
    "evolution", "species", "cell", "organism",
    "fusion", "fission", "plasma", "laser", "magnet",
]


class FirstPrinciplesGuard:
    """Evaluates whether a claim contradicts known first principles."""

    def evaluate(self, user_input: str, model_output: str) -> GuardOutput:
        lower = model_output.lower()

        # Check if this is a scientific/technical context
        input_lower = user_input.lower()
        is_scientific = any(kw in input_lower or kw in lower for kw in _SCIENTIFIC_DOMAIN_KEYWORDS)

        if not is_scientific:
            return GuardOutput(
                guard_name="FirstPrinciplesGuard",
                result=GuardResult.PASS,
                reason="Non-scientific context, first-principles check skipped",
            )

        violations = []
        for pattern, description in _PRINCIPLE_VIOLATIONS:
            if re.search(pattern, lower):
                violations.append(description)

        if violations:
            return GuardOutput(
                guard_name="FirstPrinciplesGuard",
                result=GuardResult.FLAG,
                reason="; ".join(violations),
                details={"violations": violations, "is_scientific_context": True},
            )

        return GuardOutput(
            guard_name="FirstPrinciplesGuard",
            result=GuardResult.PASS,
            reason="No first-principles violations detected",
            details={"is_scientific_context": True},
        )
