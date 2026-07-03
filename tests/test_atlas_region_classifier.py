from phyng.atlas.schemas import AtlasThresholds
from phyng.atlas.region_classifier import classify_region


def test_region_classifier_logic():
    thresholds = AtlasThresholds()
    
    # Planck crossing
    region = classify_region(Q=1.0, B=1.0, scale_status="ACCEPTED", thresholds=thresholds)
    assert region == "PLANCK_CROSSING"
    
    # Quantum boundary
    region = classify_region(Q=1.0, B=1e-25, scale_status="ACCEPTED", thresholds=thresholds)
    assert region == "QUANTUM_BOUNDARY"
    
    # Gravitational boundary
    region = classify_region(Q=1e-25, B=1.0, scale_status="ACCEPTED", thresholds=thresholds)
    assert region == "GRAVITATIONAL_BOUNDARY"
    
    # Negative gravity bound
    region = classify_region(Q=1e-5, B=1e-25, scale_status="ACCEPTED", thresholds=thresholds)
    assert region == "NEGATIVE_GRAVITY_BOUND"
    
    # Ad-hoc scale blocked
    region = classify_region(Q=1.0, B=1.0, scale_status="REJECTED", thresholds=thresholds)
    assert region == "AD_HOC_SCALE_BLOCKED"
