"""
Claim Gatekeeper.

Anti-self-deception engine. Evaluates claims against strict rules
and blocks anything that uses structural lemmas, analogies, or
algebraic identities as proof of new physics.

If a claim doesn't leave a trace, it's blocked.
If a scale L is arbitrary, it's blocked.
If a lemma is used as empirical proof, it's blocked.
If a model doesn't improve or bound anything, it's registered without makeup.
"""

import re
from typing import Optional

from pydantic import BaseModel

from phyng.enums import ClaimType, Layer, TraceType


class Claim(BaseModel):
    """A typed epistemic claim to be evaluated by the gatekeeper."""

    text: str
    claim_type: ClaimType
    layer: Layer
    trace_type: TraceType | None = None
    predictive_gain: float | None = None
    requires_L: bool = False
    L_status: str | None = None


# ── Blocked text patterns ──────────────────────────────────────────────

_PATTERN_INVARIANT_NEW_PHYSICS = re.compile(
    r"invariante?\s+demuestra\s+nueva\s+f[ií]sica"
    r"|invariant\s+proves?\s+new\s+physics"
    r"|invariant\s+demonstrates?\s+new\s+physics",
    re.IGNORECASE,
)

_PATTERN_MINKOWSKI_OVERCLAIM = re.compile(
    r"Minkowski\s+demuestra\s+Frontera\s+C\s+completa"
    r"|Minkowski\s+proves?\s+(?:complete\s+)?(?:Frontera\s+C|C[- ]?Boundary)",
    re.IGNORECASE,
)

_PATTERN_NEW_PHYSICS = re.compile(
    r"nueva\s+f[ií]sica"
    r"|new\s+physics"
    r"|nueva\s+ley"
    r"|new\s+law"
    r"|teor[ií]a\s+(?:est[aá]\s+)?validada"
    r"|theory\s+(?:is\s+)?validated",
    re.IGNORECASE,
)

_PATTERN_MASS_CANCELLATION = re.compile(
    r"cancelaci[oó]n\s+de\s+masa\s+prueba"
    r"|mass\s+cancellation\s+proves?",
    re.IGNORECASE,
)

_PATTERN_PLANCK_AREA_VALIDATION = re.compile(
    r"[aá]rea\s+de\s+Planck\s+aparece.*(?:validada|validado)"
    r"|Planck\s+area\s+appears.*validated"
    r"|[aá]rea\s+de\s+Planck\s+aparece.*teor[ií]a",
    re.IGNORECASE,
)


def evaluate_claim(claim: Claim) -> dict:
    """
    Evaluate a claim against the gatekeeper rules.

    Rules (applied in order):
        1. Text matches "invariant proves new physics" → BLOCKED_INVALID_LEMMA_USE
        2. Text matches "Minkowski proves complete Frontera C" → BLOCKED_OVERCLAIM
        3. COGNITIVE_EXTENSION layer validating physics → BLOCKED_LAYER_CONTAMINATION
        4. HYPOTHESIS with NULL_TRACE or no trace → REQUIRES_TRACE
        5. requires_L but L_status != ACCEPTED → BLOCKED_AS_AD_HOC_SCALE
        6. STRUCTURAL_LEMMA with STRUCTURAL_TRACE → ALLOWED_LIMITED
        7. Claims new physics without empirical/predictive trace → BLOCKED

    Args:
        claim: The claim to evaluate.

    Returns:
        Dict with decision, reason, safe_rewrite, layer, claim_type,
        and trace_type.
    """
    text = claim.text

    # Rule 1: Invariant proves new physics
    if _PATTERN_INVARIANT_NEW_PHYSICS.search(text):
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_INVALID_LEMMA_USE: A structural lemma (algebraic identity) "
                   "cannot be used as proof of new physics.",
            safe_rewrite="The invariant λ_C·r_g=ℓ_P² is a consistency check, "
                         "not evidence for new physics.",
        )

    # Rule 2: Minkowski overclaim
    if _PATTERN_MINKOWSKI_OVERCLAIM.search(text):
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_OVERCLAIM: Minkowski spacetime consistency does not "
                   "validate the complete Frontera C framework.",
            safe_rewrite="Minkowski spacetime provides a necessary consistency check "
                         "for the structural layer only.",
        )

    # Rule 2b: Mass cancellation overclaim
    if _PATTERN_MASS_CANCELLATION.search(text):
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_OVERCLAIM: Mass cancellation in the invariant is "
                   "algebraic, not evidence for a new physical law.",
            safe_rewrite="The mass cancellation is a structural property of "
                         "the λ_C·r_g identity, not a new law.",
        )

    # Rule 2c: Planck area appearance overclaim
    if _PATTERN_PLANCK_AREA_VALIDATION.search(text):
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_OVERCLAIM: The appearance of Planck area in an "
                   "algebraic identity does not validate the theory.",
            safe_rewrite="Planck area appears because the identity is built from "
                         "ħ, G, and c — it is not independent confirmation.",
        )

    # Rule 3: Cognitive extension validating physics
    if claim.layer == Layer.COGNITIVE_EXTENSION and _claims_physics_validation(text):
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_LAYER_CONTAMINATION: Cognitive extensions cannot "
                   "validate physical claims.",
            safe_rewrite="Cognitive models may inspire hypotheses but cannot "
                         "serve as physical validation.",
        )

    # Rule 4: Hypothesis without trace
    if claim.claim_type == ClaimType.HYPOTHESIS:
        if claim.trace_type is None or claim.trace_type == TraceType.NULL_TRACE:
            return _result(
                claim,
                decision="REQUIRES_TRACE",
                reason="REQUIRES_TRACE: Hypothesis requires at least a non-null "
                       "epistemic trace to proceed.",
                safe_rewrite="This hypothesis needs an epistemic trace "
                             "(τ > 0) before it can be evaluated.",
            )

    # Rule 5: Requires L but L not accepted
    if claim.requires_L and claim.L_status != "ACCEPTED":
        return _blocked(
            claim,
            decision="BLOCKED",
            reason="BLOCKED_AS_AD_HOC_SCALE: Claim requires an accepted operational "
                   f"scale L, but L_status is '{claim.L_status}'.",
            safe_rewrite="Re-evaluate the claim with a justified and accepted "
                         "operational scale L.",
        )

    # Rule 6: Structural lemma with structural trace → limited
    if (
        claim.claim_type == ClaimType.STRUCTURAL_LEMMA
        and claim.trace_type == TraceType.STRUCTURAL_TRACE
    ):
        return _result(
            claim,
            decision="ALLOWED_LIMITED",
            reason="Structural lemma with structural trace. "
                   "Allowed for consistency checking only.",
            safe_rewrite=None,
        )

    # Rule 7: Claims new physics without empirical trace
    if _PATTERN_NEW_PHYSICS.search(text):
        empirical_traces = {
            TraceType.PREDICTIVE_TRACE,
            TraceType.DETECTABLE_TRACE,
            TraceType.NEGATIVE_BOUND_TRACE,
        }
        if claim.trace_type not in empirical_traces:
            return _blocked(
                claim,
                decision="BLOCKED",
                reason="BLOCKED_NO_EMPIRICAL_OR_PREDICTIVE_TRACE: Claim asserts "
                       "new physics but lacks a predictive, detectable, or "
                       "negative-bound trace.",
                safe_rewrite="Remove the new-physics assertion or provide "
                             "empirical/predictive evidence.",
            )

    # Default: allowed
    return _result(
        claim,
        decision="ALLOWED",
        reason="Claim passes all gatekeeper rules.",
        safe_rewrite=None,
    )


# ── Internal helpers ───────────────────────────────────────────────────

def _claims_physics_validation(text: str) -> bool:
    """Check if text attempts to validate physics."""
    patterns = [
        r"valida\s+(?:la\s+)?f[ií]sica",
        r"validates?\s+physics",
        r"prueba\s+(?:la\s+)?f[ií]sica",
        r"proves?\s+(?:the\s+)?physics",
        r"demuestra\s+(?:la\s+)?f[ií]sica",
        r"confirms?\s+(?:the\s+)?physics",
        r"verifica\s+(?:la\s+)?f[ií]sica",
    ]
    combined = re.compile("|".join(patterns), re.IGNORECASE)
    return bool(combined.search(text))


def _blocked(
    claim: Claim,
    decision: str,
    reason: str,
    safe_rewrite: Optional[str],
) -> dict:
    return _result(claim, decision, reason, safe_rewrite)


def _result(
    claim: Claim,
    decision: str,
    reason: str,
    safe_rewrite: Optional[str],
) -> dict:
    return {
        "decision": decision,
        "reason": reason,
        "safe_rewrite": safe_rewrite,
        "layer": claim.layer.value,
        "claim_type": claim.claim_type.value,
        "trace_type": claim.trace_type.value if claim.trace_type else None,
    }
