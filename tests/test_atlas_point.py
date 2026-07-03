import math
from phyng.constants import planck_length
from phyng.atlas.schemas import PhysicalSystemSpec
from phyng.atlas.atlas_builder import build_atlas
from phyng.atlas.region_classifier import classify_region
from phyng.atlas.schemas import AtlasThresholds


def test_atlas_point_qb_identity():
    spec = PhysicalSystemSpec(
        system_id="SYS-1",
        label="Test system",
        description="A test system spec",
        m_kg=1e-12,
        L_value_m=1e-8,
        L_type="L_SYS",
        physical_role="Size",
        observer_channel="None",
        justification="Verified size",
        allowed_range_m=(1e-9, 1e-7),
        arbitrariness_risk="LOW"
    )
    
    thresholds = AtlasThresholds()
    atlas = build_atlas([spec], thresholds)
    p = atlas.points[0]
    
    # Verify QB identity
    lp = planck_length()
    expected_qb = (lp ** 2) / (p.L_value_m ** 2)
    assert abs(p.QB - expected_qb) < 1e-30
    assert abs(p.delta_QB) < 1e-30


def test_log_coordinates_valid():
    spec = PhysicalSystemSpec(
        system_id="SYS-2",
        label="Test system 2",
        description="A test system spec 2",
        m_kg=1e-12,
        L_value_m=1e-8,
        L_type="L_SYS",
        physical_role="Size",
        observer_channel="None",
        justification="Verified size",
        allowed_range_m=(1e-9, 1e-7),
        arbitrariness_risk="LOW"
    )
    
    thresholds = AtlasThresholds()
    atlas = build_atlas([spec], thresholds)
    p = atlas.points[0]
    
    # log10 checks
    assert math.isclose(p.logQ, math.log10(p.Q))
    assert math.isclose(p.logB, math.log10(p.B))
    assert math.isclose(p.u, (p.logQ + p.logB) / 2.0)
    assert math.isclose(p.w, (p.logB - p.logQ) / 2.0)
