import xendris.core.response_contract as rc


def test_public_imports_are_exposed():
    assert rc.ClaimType.OBSERVED.value == "OBSERVED"
    assert rc.ConfidenceLevel.CALIBRATED.value == "CALIBRATED"
    assert rc.ResponseMode.RIGOROUS.value == "RIGOROUS"
    assert rc.DomainValidity.CONTEXT_DEPENDENT.value == "CONTEXT_DEPENDENT"
    assert rc.ClaimAssessment is not None
    assert rc.ResponseContractAssessment is not None
    assert rc.make_claim is not None


def test_enum_values_match_response_contract_v0_2_0():
    assert [item.value for item in rc.ClaimType] == [
        "OBSERVED",
        "DERIVED",
        "STANDARD_KNOWLEDGE",
        "INFERENCE",
        "SPECULATION",
        "UNVERIFIED",
    ]
    assert [item.value for item in rc.ConfidenceLevel] == [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CALIBRATED",
        "UNKNOWN",
    ]
    assert [item.value for item in rc.ResponseMode] == [
        "FAST",
        "STANDARD",
        "RIGOROUS",
        "AUDIT",
    ]
    assert [item.value for item in rc.DomainValidity] == [
        "GENERAL",
        "LOCAL",
        "CONTEXT_DEPENDENT",
        "EXPERIMENTAL",
        "UNKNOWN",
    ]


def test_make_claim_creates_claim_assessment():
    claim = rc.make_claim(
        text="E = mc² is the rest-energy relation.",
        claim_type=rc.ClaimType.STANDARD_KNOWLEDGE,
        confidence=rc.ConfidenceLevel.CALIBRATED,
        domain_validity=rc.DomainValidity.CONTEXT_DEPENDENT,
    )

    assert isinstance(claim, rc.ClaimAssessment)
    assert claim.text == "E = mc² is the rest-energy relation."
    assert claim.claim_type == rc.ClaimType.STANDARD_KNOWLEDGE
    assert claim.confidence == rc.ConfidenceLevel.CALIBRATED
    assert claim.domain_validity == rc.DomainValidity.CONTEXT_DEPENDENT


def test_required_usage_example_is_conservative():
    claim = rc.make_claim(
        text="E = mc² is the rest-energy relation.",
        claim_type=rc.ClaimType.STANDARD_KNOWLEDGE,
        confidence=rc.ConfidenceLevel.CALIBRATED,
        domain_validity=rc.DomainValidity.CONTEXT_DEPENDENT,
    )

    assessment = rc.ResponseContractAssessment(
        mode=rc.ResponseMode.RIGOROUS,
        claims=(claim,),
        has_domain_limits=True,
        has_uncertainty_marker=True,
        has_overclaim_risk=False,
    )

    assert assessment.is_conservative() is True


def test_has_overclaim_risk_is_not_conservative():
    assessment = rc.ResponseContractAssessment(
        mode=rc.ResponseMode.STANDARD,
        has_overclaim_risk=True,
    )

    assert assessment.is_conservative() is False


def test_speculation_with_high_confidence_is_not_conservative():
    claim = rc.make_claim(
        text="This speculative statement is certain.",
        claim_type=rc.ClaimType.SPECULATION,
        confidence=rc.ConfidenceLevel.HIGH,
    )
    assessment = rc.ResponseContractAssessment(
        mode=rc.ResponseMode.AUDIT,
        claims=(claim,),
    )

    assert assessment.is_conservative() is False


def test_unverified_with_high_confidence_is_not_conservative():
    claim = rc.make_claim(
        text="This unverified statement is certain.",
        claim_type=rc.ClaimType.UNVERIFIED,
        confidence=rc.ConfidenceLevel.HIGH,
    )
    assessment = rc.ResponseContractAssessment(
        mode=rc.ResponseMode.FAST,
        claims=(claim,),
    )

    assert assessment.is_conservative() is False


def test_surface_helpers_are_conservative_and_do_not_validate_truth():
    assert rc.classify_claim_text("This was measured locally.") == rc.ClaimType.OBSERVED
    assert rc.classify_claim_text("This suggests a limited next step.") == rc.ClaimType.INFERENCE
    assert rc.classify_claim_text("") == rc.ClaimType.UNVERIFIED
    assert rc.detect_domain_validity("under these assumptions") == rc.DomainValidity.CONTEXT_DEPENDENT
    assert rc.detect_domain_validity("experimental pilot") == rc.DomainValidity.EXPERIMENTAL


def test_helpers_do_not_emit_high_confidence_aggressively():
    samples = [
        "",
        "This is always guaranteed and proven.",
        "Under these assumptions, this suggests a limited conclusion.",
        "A plain practical response without evidence validation.",
    ]

    assert all(rc.estimate_confidence(sample) != rc.ConfidenceLevel.HIGH for sample in samples)
    assert rc.assess_response_contract("Measured result under these assumptions.").claims[0].confidence != rc.ConfidenceLevel.HIGH


def test_assess_response_contract_reports_surface_signals_only():
    assessment = rc.assess_response_contract(
        "Under these assumptions, this suggests a context dependent answer.",
        mode=rc.ResponseMode.RIGOROUS,
    )

    assert assessment.mode == rc.ResponseMode.RIGOROUS
    assert assessment.has_uncertainty_marker is True
    assert assessment.has_domain_limits is True
    assert assessment.has_overclaim_risk is False
    assert assessment.is_conservative() is True
    assert assessment.claims[0].claim_type == rc.ClaimType.INFERENCE
