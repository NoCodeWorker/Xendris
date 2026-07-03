from phyng.core.report_contract import (
    append_canonical_status_section,
    build_report_contract,
    render_canonical_report_section,
)


def test_report_contract_renders_canonical_section():
    contract = build_report_contract(
        title="Canonical Section Test",
        campaign_id="TEST-CAMPAIGN",
        domain_status="OUTSIDE_CLAIM_BOUNDARY",
        generated_date="2026-06-30",
    )
    rendered = render_canonical_report_section(contract)

    assert "Domain Status: `OUTSIDE_CLAIM_BOUNDARY`" in rendered
    assert "Canonical Permission: `CLAIM_BLOCKED`" in rendered
    assert "Blocked Reasons: `OUTSIDE_CLAIM_BOUNDARY`" in rendered
    assert "Evidence Level: `NO_EVIDENCE`" in rendered


def test_append_canonical_status_section_preserves_original_markdown():
    contract = build_report_contract(
        title="Canonical Section Test",
        domain_status="BUSINESS_VALIDATED_LIMITED",
        generated_date="2026-06-30",
    )
    original = "# Existing Report\n\nOriginal content."

    combined = append_canonical_status_section(original, contract)

    assert combined.startswith(original)
    assert "## Canonical Status" in combined
    assert "BUSINESS_VALIDATED_LIMITED" in combined
