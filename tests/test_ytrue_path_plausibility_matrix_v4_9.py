from phyng.source_identity_preflight.availability import availability_for_identity
from phyng.source_identity_preflight.identity_resolution import resolve_inventory_ref
from phyng.source_identity_preflight.observable_identity import build_observable_identity_matrix
from phyng.source_identity_preflight.ytrue_path import build_ytrue_path_plausibility_matrix


def test_ytrue_path_cannot_be_medium_without_source_identity():
    identity = resolve_inventory_ref("PHI_CURVATURE", "Phys. Rev. A 102, 022101")
    availability = availability_for_identity(identity)
    observables = build_observable_identity_matrix([identity])

    paths = build_ytrue_path_plausibility_matrix(observables, [availability])

    assert paths
    assert all(record.plausibility_level == "NONE" for record in paths)
