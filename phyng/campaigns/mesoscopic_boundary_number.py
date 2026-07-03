import math
from pathlib import Path
from phyng.constants import C, HBAR, G, planck_length
from phyng.operational_scale import OperationalScale, review_operational_scale
from phyng.atlas.region_classifier import classify_region
from phyng.atlas.exclusion_rules import generate_exclusion_claims
from phyng.atlas.schemas import AtlasThresholds
from phyng.campaigns.schemas import CampaignInput, CampaignResult
from phyng.campaigns.non_triviality import classify_non_triviality
from phyng.rag.schemas import ResearchTask
from phyng.rag.research_planner import save_research_task, list_research_tasks
from phyng.rag.source_registry import list_sources


def run_mesoscopic_boundary_campaign(
    campaign_input: CampaignInput, root_dir: Path
) -> CampaignResult:
    # 1. Physical calculations
    m = campaign_input.m_kg
    L = campaign_input.L_value_m
    lp = planck_length()
    
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
    
    # 2. Scale review
    op_scale = OperationalScale(
        L_value_m=L,
        L_type=campaign_input.L_type, # type: ignore
        physical_role=campaign_input.physical_role,
        observer_channel=campaign_input.observer_channel,
        justification=campaign_input.justification,
        allowed_range_m=campaign_input.allowed_range_m,
        arbitrariness_risk=campaign_input.arbitrariness_risk # type: ignore
    )
    review = review_operational_scale(op_scale)
    scale_status = review["status"]
    scale_reason = review["reason"]
    
    # 3. Region classification
    thresholds = AtlasThresholds()
    region = classify_region(Q, B, scale_status, thresholds)
    
    # 4. Allowed & blocked claims
    allowed, blocked = generate_exclusion_claims(region, scale_status, delta_QB)
    
    # Hard rule for Campaign 001: decoherence overclaim must be blocked
    deco_overclaim = "Phygn predicts new gravitational decoherence."
    if deco_overclaim not in blocked:
        blocked.append(deco_overclaim)
        
    allowed_meso = f"For the selected m and L, Phygn computes a negative bound showing that the direct gravitational boundary ratio B = r_g/L is negligible."
    if allowed_meso not in allowed and region == "NEGATIVE_GRAVITY_BOUND":
        allowed.append(allowed_meso)
        
    # 5. Check RAG sources & create research tasks if missing
    existing_sources = list_sources(root_dir)
    existing_tasks = list_research_tasks(root_dir)
    existing_task_ids = {t.task_id for t in existing_tasks}
    
    # Define needed categories and see if we have sources matching them
    categories = {
        "SRC-CAT-001": ("Compton Wavelength", ["compton", "quantum"]),
        "SRC-CAT-002": ("Schwarzschild Radius", ["schwarzschild", "gravity", "gravitational"]),
        "SRC-CAT-003": ("Planck Scale", ["planck"]),
        "SRC-CAT-004": ("Compton-Schwarzschild Diagram", ["diagram", "adler", "santiago"]),
        "SRC-CAT-005": ("Mesoscopic Interferometry", ["maqro", "interferometer", "mesoscopic"])
    }
    
    required_sources = []
    next_tasks = []
    
    for cat_id, (cat_name, keywords) in categories.items():
        found = False
        for src in existing_sources:
            src_str = f"{src.title} {src.notes or ''} {' '.join(src.topics)}".lower()
            if any(kw in src_str for kw in keywords):
                found = True
                required_sources.append(src.source_id)
                break
                
        if not found:
            # Create a ResearchTask in registry
            task_id = f"RT-CAMPAIGN-001-{cat_id}"
            if task_id not in existing_task_ids:
                task = ResearchTask(
                    task_id=task_id,
                    question=f"What is the physical grounding for the {cat_name} category?",
                    reason=f"Campaign requires support for {cat_name}.",
                    linked_gap_id=f"GAP_RAG_{cat_id}",
                    required_source_types=["PAPER", "BOOK"],
                    priority="P1",
                    expected_output="SOURCE_RECORDS",
                    status="AWAITING_SOURCE_INGESTION"
                )
                save_research_task(task, root_dir)
            next_tasks.append(task_id)
            
    # Trace type
    if region == "NEGATIVE_GRAVITY_BOUND" or region == "NEGATIVE_QUANTUM_BOUND":
        trace_type = "NEGATIVE_BOUND_TRACE"
    elif region in ["PLANCK_CROSSING", "QUANTUM_BOUNDARY", "GRAVITATIONAL_BOUNDARY"]:
        trace_type = "PREDICTIVE_TRACE"
    else:
        trace_type = "STRUCTURAL_TRACE"
        
    signature = {
        "lambda_c": lambda_c,
        "r_g": rg,
        "R_S": rs,
        "Q": Q,
        "B": B,
        "QB": QB,
        "planck_ratio_squared": planck_ratio_sq,
        "delta_QB": delta_QB,
        "logQ": logQ,
        "logB": logB,
        "u": u,
        "w": w
    }
    
    # 6. Non-triviality check
    nt_status = classify_non_triviality(
        has_negative_bound=(region == "NEGATIVE_GRAVITY_BOUND"),
        has_predictive_model=False, # We don't have dynamic models yet
        has_empirical_threshold=True, # L is justified
        has_gain=False
    )
    
    result = CampaignResult(
        campaign_id=campaign_input.campaign_id,
        system_id=campaign_input.system_id,
        signature=signature,
        atlas_region=region,
        trace_type=trace_type,
        scale_status=scale_status,
        scale_reason=scale_reason,
        non_triviality_status=nt_status,
        allowed_claims=allowed,
        blocked_claims=blocked,
        required_sources=required_sources,
        required_models=["Decoherence dynamic comparison model (Caldeira-Leggett or Diosi-Penrose)"],
        required_tests=["test_campaign_mesoscopic_boundary_number"],
        benchmark_status="No active benchmark model comparison (Gain_C is not computed)",
        next_tasks=next_tasks
    )
    
    return result
