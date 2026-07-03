


def generate_exclusion_claims(
    region: str, scale_status: str, delta_QB: float
) -> tuple[list[str], list[str]]:
    allowed = []
    blocked = []
    
    # 1. Scale check
    if scale_status != "ACCEPTED":
        blocked.append("Any predictive claim using this scale is arbitrary and blocked.")
        
    # 2. Invariant consistency check
    if abs(delta_QB) > 1e-5:
        blocked.append("Atlas point calculation has dimensional inconsistency and is blocked.")
        return allowed, blocked
        
    # 3. Region specific rules
    if region == "NEGATIVE_GRAVITY_BOUND":
        allowed.extend([
            "B is negligible under the selected operational scale.",
            "Direct gravitational boundary claims are not supported by this signature."
        ])
        blocked.extend([
            "Phygn predicts gravitational decoherence.",
            "The system is near a gravitational horizon."
        ])
    elif region == "QUANTUM_BOUNDARY":
        allowed.append("Q is order unity, indicating quantum-localization boundary relevance.")
        blocked.append("Quantum boundary proves consciousness/measurement collapse.")
    elif region == "PLANCK_CROSSING":
        allowed.extend([
            "Q and B are simultaneously order unity.",
            "The point is structurally near Planck crossing."
        ])
        blocked.append("This proves quantum gravity.")
    elif region == "GRAVITATIONAL_BOUNDARY":
        allowed.append("B is order unity, indicating relativistic gravity / horizon boundary relevance.")
        blocked.append("Proves singular collapse without general relativity corrections.")
    elif region == "CLASSICAL_ACCESSIBLE":
        allowed.append("System is in the classical accessible region where both Q and B are small.")
        blocked.append("Claim quantum or gravitational boundary signatures are relevant.")
    elif region == "AD_HOC_SCALE_BLOCKED":
        blocked.append("Scale status is rejected. No claims permitted.")
    else:
        allowed.append("System is unclassified.")
        
    return allowed, blocked
