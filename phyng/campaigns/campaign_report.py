from pathlib import Path
from phyng.campaigns.schemas import CampaignResult, CampaignInput


def generate_campaign_reports(
    campaign_input: CampaignInput, result: CampaignResult, root_dir: Path
) -> Path:
    campaigns_dir = root_dir / "reports" / "campaigns"
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Write CAMPAIGN-001_mesoscopic_boundary_number.md
    md_path = campaigns_dir / "CAMPAIGN-001_mesoscopic_boundary_number.md"
    sig = result.signature
    
    allowed_list_str = "\n".join([f"- {c}" for c in result.allowed_claims]) if result.allowed_claims else "- None"
    blocked_list_str = "\n".join([f"- {c}" for c in result.blocked_claims]) if result.blocked_claims else "- None"
    
    rag_status_str = f"Linked sources: {', '.join(result.required_sources)}" if result.required_sources else "AWAITING_SOURCE_INGESTION"
    
    md_lines = [
        "# Campaign Result: CAMPAIGN-001 Mesoscopic Boundary Number",
        "",
        "## Scientific Question",
        "For a mesoscopic matter-wave interferometry nanoparticle, what constraint does $QB = (\\ell_P/L)^2$ impose on the simultaneous relevance of quantum and gravitational boundaries?",
        "",
        "## Input System Details",
        f"- **System ID**: {campaign_input.system_id}",
        f"- **Mass (m)**: {campaign_input.m_kg:.2e} kg",
        f"- **Scale L**: {campaign_input.L_value_m:.2e} m",
        f"- **Scale Type**: {campaign_input.L_type}",
        f"- **Physical Role**: {campaign_input.physical_role}",
        f"- **Observer Channel**: {campaign_input.observer_channel}",
        f"- **Scale Justification**: {campaign_input.justification}",
        "",
        "## Operational Scale Review",
        f"Review Status: **{result.scale_status}**",
        f"Reason: {result.scale_reason}",
        "",
        "## Boundary Signature",
        f"- **Reduced Compton Wavelength ($\\lambda_C$)**: {sig.get('lambda_c', 0.0):.2e} m",
        f"- **Gravitational Radius ($r_g$)**: {sig.get('r_g', 0.0):.2e} m",
        f"- **Schwarzschild Radius ($R_S$)**: {sig.get('R_S', 0.0):.2e} m",
        f"- **Quantum localization ratio (Q)**: {sig.get('Q', 0.0):.2e}",
        f"- **Gravity boundary ratio (B)**: {sig.get('B', 0.0):.2e}",
        f"- **Log coordinates**: $u = {sig.get('u', 0.0):.2f}$, $w = {sig.get('w', 0.0):.2f}$",
        "",
        "## Invariant Check",
        f"- **Product QB**: {sig.get('QB', 0.0):.2e}",
        f"- **Planck ratio squared ($\\ell_P^2/L^2$)**: {sig.get('planck_ratio_squared', 0.0):.2e}",
        f"- **Delta QB**: {sig.get('delta_QB', 0.0):.2e}",
        "",
        "## Region Classification",
        f"Assigned Region: **{result.atlas_region}**",
        "",
        "## Non-Triviality Status",
        f"Status: **{result.non_triviality_status}**",
        "",
        "### Why",
        "It establishes a computable, reproducible negative bound on direct gravity boundary ratios and blocks overclaims regarding decoherence signals in the absence of dynamical models.",
        "",
        "### What would falsify/defeat this",
        "An experimental measurement showing a positive gravity-boundary effect or horizon-like decoherence at these scales, or a dynamical model demonstrating non-negligible trace values.",
        "",
        "### What is still missing",
        "Ingestion of primary bibliography sources for Compton and Schwarzschild coordinate definitions, and dynamic decoherence base model comparison (CAMPAIGN-002).",
        "",
        "## Allowed Claims",
        allowed_list_str,
        "",
        "## Blocked Claims",
        blocked_list_str,
        "",
        "## RAG Status",
        f"- **Status**: {rag_status_str}",
        f"- **Missing Sources Tasks**: {', '.join(result.next_tasks) if result.next_tasks else 'None'}",
        "",
        "## Benchmark Status",
        f"- **Status**: {result.benchmark_status}",
        "",
        "## Tests",
        "- `tests/test_campaign_mesoscopic_boundary_number.py`",
        "",
        "## Next Tasks",
        "- Ingest Compton and gravity primary bibliography sources",
        "- Implement CAMPAIGN-002 model comparison once sources are ready"
    ]
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    # 2. Write CAMPAIGN-001_citation_audit.md
    audit_path = campaigns_dir / "CAMPAIGN-001_citation_audit.md"
    audit_lines = [
        "# Campaign Citation Audit Report",
        "",
        "| Claim ID | Claim Text | Status | Required Source Category | Source IDs | Support Level | Trust Level | Action |",
        "|---|---|---|---|---|---|---|---|",
        f"| CLAIM-MESO-001 | {result.allowed_claims[0] if result.allowed_claims else 'Negative gravity bound.'} | {result.trace_type} | SRC-CAT-005 | {', '.join(result.required_sources) if result.required_sources else 'None'} | DIRECT_SUPPORT | HIGH | Ingest primary sources to upgrade |",
        f"| CLAIM-DECOH-001 | {result.blocked_claims[0] if result.blocked_claims else 'Predicts decoherence.'} | BLOCKED | SRC-CAT-006 | None | CONTRADICTS | LOW | Keep blocked until Caldeira-Leggett model comparison |",
    ]
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("\n".join(audit_lines))
        
    return md_path
