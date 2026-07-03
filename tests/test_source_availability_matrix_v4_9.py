from phyng.source_identity_preflight.availability import availability_for_identity
from phyng.source_identity_preflight.identity_resolution import resolve_inventory_ref


def test_candidate_fails_without_resolvable_sources():
    identity = resolve_inventory_ref("PHI_CURVATURE", "Phys. Rev. A 102, 022101")
    availability = availability_for_identity(identity)

    assert availability.identity_complete is False
    assert availability.availability_status == "IDENTITY_INCOMPLETE"
