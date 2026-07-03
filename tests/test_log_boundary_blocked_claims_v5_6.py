from phyng.frontera_c_disposition.blocked_claims import build_blocked_claims


def test_physical_claims_remain_blocked():
    claims = build_blocked_claims()

    assert claims.physical_claim_created is False
    assert "LOG_BOUNDARY is validated." in claims.blocked_claims
    assert "Frontera C is validated." in claims.blocked_claims


def test_frontera_c_remains_unvalidated():
    claims = build_blocked_claims()

    assert claims.frontera_c_validated is False
    assert claims.invariant_confirmed is False
