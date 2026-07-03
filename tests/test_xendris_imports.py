import pytest

def test_xendris_frontera_c_imports():
    from xendris.frontera_c import (
        C, planck_length, ClaimType, Layer, TraceType,
        validate_compton_gravity_invariant, Claim, evaluate_claim
    )
    assert C == 299792458.0
    assert planck_length() > 0
    assert ClaimType.STRUCTURAL_LEMMA.value == "STRUCTURAL_LEMMA"
    assert Layer.COGNITIVE_EXTENSION.value == "COGNITIVE_EXTENSION"
    assert TraceType.STRUCTURAL_TRACE.value == "STRUCTURAL_TRACE"
    assert validate_compton_gravity_invariant is not None
    assert Claim is not None
    assert evaluate_claim is not None

def test_xendris_core_rag_imports():
    from xendris.core.rag import (
        SourceRecord, ClaimRecord, add_source, list_sources, audit_claim_support
    )
    assert SourceRecord is not None
    assert ClaimRecord is not None
    assert add_source is not None
    assert list_sources is not None
    assert audit_claim_support is not None

def test_xendris_core_campaigns_imports():
    from xendris.core.campaigns import (
        CampaignInput, run_mesoscopic_boundary_campaign, build_atlas
    )
    assert CampaignInput is not None
    assert run_mesoscopic_boundary_campaign is not None
    assert build_atlas is not None

def test_xendris_models_imports():
    from xendris.models import Claim, BenchmarkCase, ModelResponse, RubricScore
    assert Claim is not None
    assert BenchmarkCase is not None
    assert ModelResponse is not None
    assert RubricScore is not None
