from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09


def test_no_fake_excerpt_allowed():
    # If quote_or_excerpt is present, it is tracked as provided
    link = ClaimSourceLinkV09(
        link_id="L-1",
        claim_id="C-1",
        source_id="S-1",
        support_type="FORMULA_SUPPORT",
        support_strength="HIGH",
        quote_or_excerpt="V_base(t) = exp(-Gamma * t)",
        local_reference="Eq 4.1",
        audit_status="PASSED_LIMITED"
    )
    assert link.quote_or_excerpt == "V_base(t) = exp(-Gamma * t)"


def test_claim_source_link_properties():
    link = ClaimSourceLinkV09(
        link_id="L-2",
        claim_id="C-2",
        source_id="S-2",
        support_type="CONTEXT_SUPPORT",
        support_strength="MEDIUM",
        quote_or_excerpt=None,
        local_reference="Introduction",
        audit_status="PASSED_METADATA_ONLY"
    )
    assert link.quote_or_excerpt is None
    assert link.support_type == "CONTEXT_SUPPORT"
