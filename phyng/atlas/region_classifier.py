import math
from phyng.atlas.schemas import AtlasThresholds


def classify_region(
    Q: float, B: float, scale_status: str, thresholds: AtlasThresholds
) -> str:
    if scale_status == "REJECTED" or scale_status == "REJECTED_HIGH_RISK":
        return "AD_HOC_SCALE_BLOCKED"
        
    # Check if Q and B are order of magnitude near 1
    # We can use the window of [0.1, 10.0] (which is log10 between -1 and 1)
    q_near = 0.1 <= Q <= 10.0
    b_near = 0.1 <= B <= 10.0
    
    if q_near and b_near:
        return "PLANCK_CROSSING"
    elif q_near:
        return "QUANTUM_BOUNDARY"
    elif b_near:
        return "GRAVITATIONAL_BOUNDARY"
    elif B < thresholds.small_threshold:
        return "NEGATIVE_GRAVITY_BOUND"
    elif Q < thresholds.small_threshold:
        return "NEGATIVE_QUANTUM_BOUND"
    elif Q < 0.1 and B < 0.1:
        return "CLASSICAL_ACCESSIBLE"
    else:
        return "UNCLASSIFIED"
