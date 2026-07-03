from phyng.source_identity_preflight.identity_resolution import resolve_inventory_ref
from phyng.source_identity_preflight.observable_identity import build_observable_identity_matrix


def test_observable_not_locatable_without_source_identity():
    identity = resolve_inventory_ref("PHI_CURVATURE", "Phys. Rev. A 102, 022101")

    observables = build_observable_identity_matrix([identity])

    assert observables
    assert all(record.source_locatable is False for record in observables)
    assert all(record.observable_status == "SOURCE_NOT_LOCATABLE" for record in observables)
