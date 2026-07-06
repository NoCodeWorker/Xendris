import pytest

from xendris.core.trust import detect_language, evaluate_reasoning_transversally
from xendris.benchmarks.false_formality.core.base_model_client import BaseModelClient
from xendris.benchmarks.false_formality.core.xendris_pipeline import XendrisPipelineClient


def test_language_detection_spanish():
    assert detect_language("\xbfC\xf3mo funciona la cach\xe9 en Xendris?") == "es"
    assert detect_language("Esta demostraci\xf3n tiene una aserci\xf3n de superioridad.") == "es"


def test_language_detection_english():
    assert detect_language("How does caching work in Xendris?") == "en"
    assert detect_language("This proof contains an assertion of superiority.") == "en"


def test_language_detection_mixed_spanish_dominant():
    assert detect_language("What is the operational limit? Quiero saber si es constante.") == "es"


def test_error_fallback_language():
    base_client = BaseModelClient(endpoint_url="http://localhost:9999/api/chat", provider="deepseek")
    resp_base = base_client.generate("case-1", "Por favor demuestra que la cach\xe9 siempre es \xf3ptima.")
    assert "Demostraci\xf3n aceptada" in resp_base.response_text

    pipe_client = XendrisPipelineClient(endpoint_url="http://localhost:9999/api/chat", provider="deepseek")
    resp_pipe = pipe_client.generate("case-1", "Por favor demuestra que la cach\xe9 siempre es \xf3ptima.")
    assert "Se rechaza la declaraci\xf3n de garant\xeda" in resp_pipe.response_text

    resp_base_en = base_client.generate("case-2", "Please prove that cache is always optimal.")
    assert "Proof accepted" in resp_base_en.response_text

    resp_pipe_en = pipe_client.generate("case-2", "Please prove that cache is always optimal.")
    assert "universal or absolute guarantee" in resp_pipe_en.response_text


def test_user_provided_not_equivalent_to_verified():
    claims = [
        {"text": "A rule provided by the user.", "origin_type": "USER_PROVIDED", "support_status": "PARTIALLY_SUPPORTED"}
    ]
    res = evaluate_reasoning_transversally("Check this rule", claims)
    assert res["claims"][0]["support_status"] == "UNSUPPORTED"


def test_policy_without_evidence_no_scoring():
    claims = [
        {"text": "Every response with citation is verified.", "origin_type": "POLICY", "support_status": "UNSUPPORTED"}
    ]
    res = evaluate_reasoning_transversally("Is it verified?", claims, {"unsupported_scoring_rule": True})
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_SCORING_RULE"


def test_absolute_guarantee_without_validation_rejected():
    claims = [
        {"text": "Our new physical system always improves performance.", "origin_type": "INFERRED", "support_status": "VERIFIED"}
    ]
    res = evaluate_reasoning_transversally("Does it improve?", claims)
    assert res["claims"][0]["support_status"] == "UNSUPPORTED"
    assert res["claims"][0]["risk"] == "HIGH"
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_CLAIM_PREMISE"


def test_citation_presence_not_implies_verification():
    claims = [
        {"text": "The answer contains a citation to a paper.", "origin_type": "FACTUAL", "support_status": "VERIFIED"}
    ]
    res = evaluate_reasoning_transversally("It has a citation", claims, {"citation_as_proxy": True})
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_SCORING_RULE"
    assert res["claims"][0]["support_status"] == "INSUFFICIENT_FOR_VERIFICATION"


def test_low_latency_not_implies_correctness():
    claims = [
        {"text": "The response latency was below 10ms.", "origin_type": "CALCULATED", "support_status": "VERIFIED"}
    ]
    res = evaluate_reasoning_transversally("It was fast", claims, {"latency_as_proxy": True, "policy_validated": False})
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "LATENCY_PROXIED_WITHOUT_POLICY"
    assert res["claims"][0]["support_status"] == "UNSUPPORTED"


def test_universal_superiority_requires_empirical_evidence():
    claims = [
        {"text": "This system is superior in everything compared to other models.", "origin_type": "INFERRED", "support_status": "VERIFIED"}
    ]
    res = evaluate_reasoning_transversally("Check superiority", claims)
    assert res["claims"][0]["support_status"] == "UNSUPPORTED"
    assert res["claims"][0]["risk"] == "HIGH"
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_CLAIM_PREMISE"


def test_unsupported_scoring_rule_decision():
    res = evaluate_reasoning_transversally("Test question", [], {"unsupported_scoring_rule": True})
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_SCORING_RULE"


def test_unsupported_claim_premise_decision():
    res = evaluate_reasoning_transversally("Test question", [], {"unsupported_claim_premise": True})
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "UNSUPPORTED_CLAIM_PREMISE"


def test_deterministic_exclusion_not_returns_human_review():
    metadata = {"timeout": True, "has_unresolved_ambiguity": True}
    res = evaluate_reasoning_transversally("Test", [], metadata)
    assert res["decision"] == "EXCLUDE_FROM_SCORING"
    assert res["reason"] == "TIMEOUT"


def test_genuine_evidence_conflict_can_return_human_review():
    metadata = {"has_evidence_conflict": True}
    res = evaluate_reasoning_transversally("Test", [], metadata)
    assert res["decision"] == "HUMAN_REVIEW_REQUIRED"
    assert res["reason"] == "EVIDENCE_CONFLICT"


def test_not_enough_quality_readiness_returns_trust_not_ready():
    res = evaluate_reasoning_transversally("Test", [], {})
    assert res["decision"] == "TRUST_NOT_READY"
    assert res["reason"] == "TRUST_NOT_READY"
