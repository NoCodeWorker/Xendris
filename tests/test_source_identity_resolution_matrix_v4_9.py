from phyng.source_identity_preflight.identity_resolution import resolve_inventory_ref


def test_raw_citation_string_cannot_pass_candidate():
    record = resolve_inventory_ref("PHI_CURVATURE", "Phys. Rev. A 102, 022101")

    assert record.resolution_status == "RAW_REF_ONLY"
    assert record.identity_complete is False


def test_identity_requires_locator_or_local_hash():
    record = resolve_inventory_ref("PHI_CURVATURE", "Nature Physics 15, 890")

    assert record.local_hash is None
    assert "IDENTITY_REQUIRES_DOI_ARXIV_URL_OR_LOCAL_HASH" in record.blockers
