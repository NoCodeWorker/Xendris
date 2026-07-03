import datetime
import math
from phyng.constants import C, HBAR, G, planck_length, planck_mass
from phyng.operational_scale import OperationalScale, review_operational_scale
from phyng.atlas.schemas import PhysicalSystemSpec, BoundaryAtlasPoint, BoundaryAtlas, AtlasThresholds
from phyng.atlas.region_classifier import classify_region
from phyng.atlas.exclusion_rules import generate_exclusion_claims


def build_atlas(
    systems: list[PhysicalSystemSpec],
    thresholds: AtlasThresholds,
    atlas_id: str = "ATLAS-v0.5",
    version: str = "0.5.0"
) -> BoundaryAtlas:
    lp = planck_length()
    points = []
    
    for spec in systems:
        # Physical calculations
        m = spec.m_kg
        L = spec.L_value_m
        
        lambda_c = HBAR / (m * C)
        rg = G * m / (C ** 2)
        rs = 2.0 * rg
        
        Q = lambda_c / L
        B = rg / L
        QB = Q * B
        
        planck_ratio_sq = (lp ** 2) / (L ** 2)
        delta_QB = QB - planck_ratio_sq
        
        logQ = math.log10(Q)
        logB = math.log10(B)
        
        u = (logQ + logB) / 2.0
        w = (logB - logQ) / 2.0
        
        # Operational scale review
        op_scale = OperationalScale(
            L_value_m=L,
            L_type=spec.L_type, # type: ignore
            physical_role=spec.physical_role,
            observer_channel=spec.observer_channel,
            justification=spec.justification,
            allowed_range_m=spec.allowed_range_m,
            arbitrariness_risk=spec.arbitrariness_risk # type: ignore
        )
        review = review_operational_scale(op_scale)
        scale_status = review["status"]
        
        # Region classification
        region = classify_region(Q, B, scale_status, thresholds)
        
        # Exclusion rules
        allowed_claims, blocked_claims = generate_exclusion_claims(region, scale_status, delta_QB)
        
        # Trace type mapping
        if region == "NEGATIVE_GRAVITY_BOUND" or region == "NEGATIVE_QUANTUM_BOUND":
            trace_type = "NEGATIVE_BOUND_TRACE"
        elif region in ["PLANCK_CROSSING", "QUANTUM_BOUNDARY", "GRAVITATIONAL_BOUNDARY"]:
            trace_type = "PREDICTIVE_TRACE"
        else:
            trace_type = "STRUCTURAL_TRACE"
            
        # Claim status mapping
        if scale_status != "ACCEPTED":
            claim_status = "REQUIRES_SCALE_JUSTIFICATION"
        elif region == "AD_HOC_SCALE_BLOCKED":
            claim_status = "BLOCKED"
        elif region == "NEGATIVE_GRAVITY_BOUND":
            claim_status = "ALLOWED_LIMITED"
        else:
            claim_status = "ALLOWED"
            
        point = BoundaryAtlasPoint(
            system_id=spec.system_id,
            label=spec.label,
            m_kg=m,
            L_value_m=L,
            L_type=spec.L_type,
            lambda_c_m=lambda_c,
            r_g_m=rg,
            schwarzschild_radius_m=rs,
            Q=Q,
            B=B,
            QB=QB,
            planck_ratio_squared=planck_ratio_sq,
            delta_QB=delta_QB,
            logQ=logQ,
            logB=logB,
            u=u,
            w=w,
            scale_status=scale_status,
            region=region,
            trace_type=trace_type,
            claim_status=claim_status,
            allowed_claims=allowed_claims,
            blocked_claims=blocked_claims,
            source_ids=spec.source_ids,
            test_ids=[]
        )
        points.append(point)
        
    # Build summary stats
    summary = {
        "total_points": len(points),
        "region_breakdown": {}
    }
    for p in points:
        summary["region_breakdown"][p.region] = summary["region_breakdown"].get(p.region, 0) + 1
        
    # Aggregate claims
    all_allowed = []
    all_blocked = []
    all_sources = []
    
    for p in points:
        all_allowed.extend(p.allowed_claims)
        all_blocked.extend(p.blocked_claims)
        all_sources.extend(p.source_ids)
        
    atlas = BoundaryAtlas(
        atlas_id=atlas_id,
        version=version,
        points=points,
        summary=summary,
        allowed_claims=list(set(all_allowed)),
        blocked_claims=list(set(all_blocked)),
        required_sources=list(set(all_sources)),
        generated_at=datetime.datetime.utcnow().isoformat() + "Z"
    )
    return atlas
