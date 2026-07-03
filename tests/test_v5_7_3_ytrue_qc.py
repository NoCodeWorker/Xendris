from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def test_accept_requires_verified_source_object_and_hash():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    assert result.accepted
    assert all(item.local_pdf_path for item in result.accepted)
    assert all(len(item.local_pdf_hash) == 64 for item in result.accepted)


def test_no_physical_claim_created():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    assert result.next_gate_decision["physical_claim_created"] is False
    assert result.next_gate_decision["frontera_c_validated"] is False
