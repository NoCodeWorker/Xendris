"""
Tests for claim gatekeeper.
"""

from phyng.claim_gatekeeper import Claim, evaluate_claim
from phyng.enums import ClaimType, Layer, TraceType


def test_gatekeeper_blocks_invariant_new_physics_claim():
    """Rule 1: 'invariant proves new physics' → BLOCKED."""
    claim = Claim(
        text="El invariante demuestra nueva física",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_INVALID_LEMMA_USE" in result["reason"]


def test_gatekeeper_blocks_invariant_english():
    """Rule 1 also works in English."""
    claim = Claim(
        text="The invariant proves new physics",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"


def test_gatekeeper_blocks_minkowski_overclaim():
    """Rule 2: 'Minkowski proves complete Frontera C' → BLOCKED."""
    claim = Claim(
        text="Minkowski demuestra Frontera C completa",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_OVERCLAIM" in result["reason"]


def test_gatekeeper_blocks_cognitive_validation_of_physics():
    """Rule 3: COGNITIVE_EXTENSION validating physics → BLOCKED."""
    claim = Claim(
        text="La conciencia valida la física de Frontera C",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.COGNITIVE_EXTENSION,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_LAYER_CONTAMINATION" in result["reason"]


def test_gatekeeper_requires_trace_for_hypothesis():
    """Rule 4: HYPOTHESIS without trace → REQUIRES_TRACE."""
    claim = Claim(
        text="The model predicts gravitational decoherence",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
        trace_type=None,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "REQUIRES_TRACE"


def test_gatekeeper_requires_trace_for_null_trace():
    """Rule 4: HYPOTHESIS with NULL_TRACE → REQUIRES_TRACE."""
    claim = Claim(
        text="The model predicts decoherence effects",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
        trace_type=TraceType.NULL_TRACE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "REQUIRES_TRACE"


def test_gatekeeper_blocks_ad_hoc_L_claim():
    """Rule 5: requires_L but L not accepted → BLOCKED."""
    claim = Claim(
        text="Signature shows quantum-gravity crossover",
        claim_type=ClaimType.MODEL,
        layer=Layer.PHYSICAL_CORE,
        trace_type=TraceType.STRUCTURAL_TRACE,
        requires_L=True,
        L_status="REJECTED",
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_AS_AD_HOC_SCALE" in result["reason"]


def test_gatekeeper_allows_structural_lemma():
    """Rule 6: STRUCTURAL_LEMMA + STRUCTURAL_TRACE → ALLOWED_LIMITED."""
    claim = Claim(
        text="λ_C · r_g = ℓ_P² holds for all masses",
        claim_type=ClaimType.STRUCTURAL_LEMMA,
        layer=Layer.PHYSICAL_CORE,
        trace_type=TraceType.STRUCTURAL_TRACE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "ALLOWED_LIMITED"


def test_gatekeeper_blocks_new_physics_without_trace():
    """Rule 7: 'new physics' without empirical trace → BLOCKED."""
    claim = Claim(
        text="This proves new physics beyond the Standard Model",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
        trace_type=TraceType.STRUCTURAL_TRACE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_NO_EMPIRICAL_OR_PREDICTIVE_TRACE" in result["reason"]


def test_gatekeeper_allows_hypothesis_with_detectable_trace():
    """HYPOTHESIS + DETECTABLE_TRACE → ALLOWED (no blocked patterns)."""
    claim = Claim(
        text="The depolarizing channel case shows measurable effect",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.QUANTUM_CHANNEL_CORE,
        trace_type=TraceType.DETECTABLE_TRACE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "ALLOWED"


def test_gatekeeper_blocks_mass_cancellation_overclaim():
    """Rule 2b: 'mass cancellation proves new law' → BLOCKED."""
    claim = Claim(
        text="La cancelación de masa prueba una nueva ley",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_OVERCLAIM" in result["reason"]


def test_gatekeeper_blocks_planck_area_validation():
    """Rule 2c: 'Planck area appears, theory validated' → BLOCKED."""
    claim = Claim(
        text="El área de Planck aparece, por tanto la teoría está validada",
        claim_type=ClaimType.HYPOTHESIS,
        layer=Layer.PHYSICAL_CORE,
    )
    result = evaluate_claim(claim)
    assert result["decision"] == "BLOCKED"
    assert "BLOCKED_OVERCLAIM" in result["reason"]

