from phyng.dataset_expansion.source_pool import build_source_pool


def test_log_boundary_remains_archived():
    pool = build_source_pool(".")

    assert len(pool) == 5
    assert all(record.source_status == "LOCAL_AVAILABLE" for record in pool)


def test_source_pool_contains_target_sources():
    pool = build_source_pool(".")
    source_ids = {record.source_id for record in pool}

    assert "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE" in source_ids
    assert "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE" in source_ids
