from xendris.core.response_contract import (
    ClaimType,
    ConfidenceLevel,
    DomainValidity,
    ResponseContractAssessment,
    ResponseMode,
    assess_response_contract,
    classify_claim_text,
    detect_domain_validity,
    estimate_confidence,
)


def test_response_contract_imports_are_pure():
    assert ClaimType.OBSERVED.value == "OBSERVED"
    assert ConfidenceLevel.MEDIUM.value == "MEDIUM"
    assert ResponseMode.PRACTICAL.value == "PRACTICAL"
    assert DomainValidity.GENERAL.value == "GENERAL"


def test_claim_text_classification_is_conservative():
    assert classify_claim_text("This was measured in the source data.") == ClaimType.OBSERVED
    assert classify_claim_text("This suggests a possible effect.") == ClaimType.INFERENCE
    assert classify_claim_text("") == ClaimType.UNVERIFIED


def test_domain_validity_detects_sensitive_domains():
    assert detect_domain_validity("general answer") == DomainValidity.GENERAL
    assert detect_domain_validity("medical advice requires current verification") == DomainValidity.SENSITIVE_DOMAIN
    assert detect_domain_validity("result holds under these assumptions") == DomainValidity.ASSUMPTION_BOUND


def test_assessment_marks_absolute_language_as_overclaiming_risk():
    assessment = assess_response_contract("This is always guaranteed and proven.")

    assert assessment.non_overclaiming is False
    assert assessment.has_overclaim_risk is True
    assert assessment.is_conservative() is False
    assert assessment.confidence_level == ConfidenceLevel.LOW
    assert "absolute_language_detected" in assessment.notes
    assert assessment.to_dict()["claim_type"] == ClaimType.UNVERIFIED.value


def test_assessment_keeps_response_content_unchanged_by_design():
    text = "Under these assumptions, this suggests a useful practical next step."
    assessment = assess_response_contract(text, domain="programming")

    assert assessment.claim_type == ClaimType.INFERENCE
    assert assessment.domain_validity == DomainValidity.ASSUMPTION_BOUND
    assert assessment.response_mode == ResponseMode.PRACTICAL


def test_speculation_with_high_confidence_is_not_conservative():
    assessment = ResponseContractAssessment(
        claim_type=ClaimType.SPECULATION,
        confidence_level=ConfidenceLevel.HIGH,
        response_mode=ResponseMode.RIGOROUS,
        domain_validity=DomainValidity.DOMAIN_SPECIFIC,
        non_overclaiming=True,
        limits_stated=True,
        uncertainty_marked=True,
    )

    assert assessment.is_conservative() is False


def test_unverified_with_high_confidence_is_not_conservative():
    assessment = ResponseContractAssessment(
        claim_type=ClaimType.UNVERIFIED,
        confidence_level=ConfidenceLevel.HIGH,
        response_mode=ResponseMode.DIRECT,
        domain_validity=DomainValidity.GENERAL,
        non_overclaiming=True,
        limits_stated=True,
        uncertainty_marked=True,
    )

    assert assessment.is_conservative() is False


def test_explicit_overclaim_risk_is_not_conservative():
    assessment = ResponseContractAssessment(
        claim_type=ClaimType.STANDARD_KNOWLEDGE,
        confidence_level=ConfidenceLevel.MEDIUM,
        response_mode=ResponseMode.PRACTICAL,
        domain_validity=DomainValidity.GENERAL,
        non_overclaiming=True,
        limits_stated=True,
        uncertainty_marked=True,
        has_overclaim_risk=True,
    )

    assert assessment.is_conservative() is False


def test_helpers_do_not_emit_high_confidence():
    samples = [
        "",
        "This is always guaranteed and proven.",
        "Under these assumptions, this suggests a limited conclusion.",
        "A plain practical response with several words but no evidence validation.",
    ]

    assert all(estimate_confidence(sample) != ConfidenceLevel.HIGH for sample in samples)
    assert assess_response_contract("Measured result under these assumptions.").confidence_level != ConfidenceLevel.HIGH
