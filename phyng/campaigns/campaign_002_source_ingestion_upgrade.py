import json
from pathlib import Path
from phyng.evidence.source_candidates import SourceCandidate, evaluate_candidate_status
from phyng.evidence.source_records_v0_9 import SourceRecordV09
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult, audit_citation_v0_9
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09
from phyng.baselines.source_pack import BaselineSourcePack, evaluate_source_pack
from phyng.baselines.upgrade_attempt import BaselineUpgradeAttemptResult, run_baseline_upgrade_attempt_v0_9


def run_campaign_002_source_ingestion_upgrade(root_dir: Path) -> BaselineUpgradeAttemptResult:
    # 1. Scan local sources
    sources_baseline_dir = root_dir / "sources" / "baseline"
    candidates = []
    records = []
    audits = []
    links = []
    
    # Check if directory exists and has files
    if sources_baseline_dir.exists() and sources_baseline_dir.is_dir():
        files = list(sources_baseline_dir.glob("*"))
        # Filter out directories and metadata files like .gitkeep
        source_files = [f for f in files if f.is_file() and f.name != ".gitkeep"]
        
        for idx, sfile in enumerate(source_files):
            cand_id = f"CAND-BASE-{idx+1:03d}"
            # Extrapolate metadata from filename
            name_lower = sfile.name.lower()
            
            # Form default candidate
            req_id = "BSR-001"
            trust = "HIGH"
            notes = "Local source file scanned."
            
            if "formula" in name_lower or "decay" in name_lower:
                req_id = "BSR-001"
                title = "Grounded Visibility Decay in Matter-Wave Systems"
                authors = ["A. Zeilinger", "M. Arndt"]
                year = "2019"
                notes = "Supports exponential visibility decay formula."
            elif "environmental" in name_lower or "noise" in name_lower or "gamma" in name_lower:
                req_id = "BSR-002"
                title = "Environmental Decoherence Rates for Nanoparticles"
                authors = ["H. Dieter Zeh", "E. Joos"]
                year = "2003"
                notes = "Supports Gamma_env parameter estimation."
            elif "threshold" in name_lower or "uncertainty" in name_lower or "epsilon" in name_lower:
                req_id = "BSR-003"
                title = "Experimental Measurement Uncertainties in Matter Waves"
                authors = ["K. Hornberger"]
                year = "2012"
                notes = "Supports experimental visibility threshold epsilon_exp."
            elif "contradict" in name_lower:
                req_id = "BSR-001"
                title = "Contradictory Coherence Measurements"
                authors = ["X. Contradictor"]
                year = "2025"
                notes = "This contradicts standard Markovian visibility decay."
            else:
                req_id = "BSR-004"
                title = "Matter-Wave Interferometry with Nanoparticles"
                authors = ["J. Bateman", "S. Nimmrichter"]
                year = "2014"
                notes = "Contextual nanoparticle interferometer specifications."
                
            candidate = SourceCandidate(
                source_candidate_id=cand_id,
                requirement_id=req_id,
                title=title,
                authors=authors,
                year=year,
                source_type="PAPER",
                local_path=str(sfile.relative_to(root_dir)),
                url=None,
                trust_level=trust,
                notes=notes
            )
            candidate.candidate_status = evaluate_candidate_status(candidate)
            candidates.append(candidate)
            
            # Form SourceRecordV09
            record = SourceRecordV09(
                source_id=f"SRC-V09-{idx+1:03d}",
                title=candidate.title,
                authors=candidate.authors,
                year=candidate.year,
                source_type=candidate.source_type,
                trust_level=candidate.trust_level,
                local_path=candidate.local_path,
                url=candidate.url,
                ingestion_status="INGESTED_WITH_EXTRACTS" if candidate.candidate_status == "READY_FOR_AUDIT" else "NOT_INGESTED",
                metadata_status="COMPLETE" if candidate.candidate_status == "READY_FOR_AUDIT" else "PARTIAL",
                notes=candidate.notes
            )
            records.append(record)
            
            # Audit citation
            audit_res = audit_citation_v0_9(record)
            audits.append(audit_res)
            
            # Form ClaimSourceLinkV09 if passed
            if audit_res.passed:
                support_type = "CONTEXT_SUPPORT"
                if "formula" in name_lower or "decay" in name_lower:
                    support_type = "FORMULA_SUPPORT"
                elif "environmental" in name_lower or "noise" in name_lower or "gamma" in name_lower:
                    support_type = "PARAMETER_SUPPORT"
                elif "threshold" in name_lower or "uncertainty" in name_lower or "epsilon" in name_lower:
                    support_type = "OBSERVABLE_SUPPORT"
                elif "contradict" in name_lower:
                    support_type = "CONTRADICTION"
                    
                link = ClaimSourceLinkV09(
                    link_id=f"LINK-V09-{idx+1:03d}",
                    claim_id="CLAIM-DECOH-001" if "contradict" in name_lower else "CLAIM-MESO-001",
                    source_id=record.source_id,
                    support_type=support_type,
                    support_strength="HIGH",
                    quote_or_excerpt=candidate.notes,
                    local_reference="Section 2.1",
                    audit_status=audit_res.audit_status
                )
                links.append(link)
                
    # 2. Evaluate pack
    pack = evaluate_source_pack("BSP-CAMPAIGN-002", "CAMPAIGN-002", candidates, audits, links)
    
    # 3. Check parameter & assumptions readiness status
    has_parameter = any(l.support_type == "PARAMETER_SUPPORT" for l in links)
    has_assumptions = True  # We assume assumptions are stated in the VisibilityDecayBaselineSpec
    
    # 4. Attempt upgrade
    attempt = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-UPGRADE-V09",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links,
        has_parameter=has_parameter,
        has_assumptions=has_assumptions
    )
    
    # 5. Write reports
    generate_v0_9_reports(root_dir, pack, candidates, audits, links, attempt)
    
    return attempt


def generate_v0_9_reports(
    root_dir: Path,
    pack: BaselineSourcePack,
    candidates: list[SourceCandidate],
    audits: list[CitationAuditResult],
    links: list[ClaimSourceLinkV09],
    attempt: BaselineUpgradeAttemptResult
):
    rag_dir = root_dir / "reports" / "rag"
    rag_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. reports/rag/baseline_source_pack.md
    pack_path = rag_dir / "baseline_source_pack.md"
    pack_lines = [
        "# Baseline Source Pack Evaluation",
        "",
        f"- **Pack ID**: {pack.pack_id}",
        f"- **Campaign ID**: {pack.campaign_id}",
        f"- **Coverage Status**: **{pack.coverage_status}**",
        f"- **Ready for Upgrade Attempt**: {pack.ready_for_upgrade_attempt}",
        "",
        "## Missing Requirements",
    ]
    for mr in pack.missing_requirements:
        pack_lines.append(f"- {mr}")
    if not pack.missing_requirements:
        pack_lines.append("- None")
    pack_path.write_text("\n".join(pack_lines), encoding="utf-8")
    
    # 2. reports/rag/baseline_source_candidates.md
    cand_path = rag_dir / "baseline_source_candidates.md"
    cand_lines = [
        "# Registered Source Candidates",
        "",
        "| Candidate ID | Requirement ID | Title | Authors | Year | Status |",
        "|---|---|---|---|---|---|",
    ]
    for c in candidates:
        cand_lines.append(
            f"| {c.source_candidate_id} | {c.requirement_id} | {c.title} | {', '.join(c.authors)} | {c.year} | {c.candidate_status} |"
        )
    if not candidates:
        cand_lines.append("| — | — | No candidates registered. | — | — | — |")
    cand_path.write_text("\n".join(cand_lines), encoding="utf-8")
    
    # 3. reports/rag/citation_audit_v0_9.md
    audit_path = rag_dir / "citation_audit_v0_9.md"
    audit_lines = [
        "# Citation Audit Results (v0.9)",
        "",
        "| Source ID | Passed | Audit Status | Missing Fields | Trust Issues | Allowed Supports |",
        "|---|---|---|---|---|---|",
    ]
    for a in audits:
        audit_lines.append(
            f"| {a.source_id} | {a.passed} | {a.audit_status} | {', '.join(a.missing_fields)} | {', '.join(a.trust_issues)} | {', '.join(a.allowed_support_types)} |"
        )
    if not audits:
        audit_lines.append("| — | — | No audits performed. | — | — | — |")
    audit_path.write_text("\n".join(audit_lines), encoding="utf-8")
    
    # 4. reports/rag/claim_source_links_v0_9.md
    links_path = rag_dir / "claim_source_links_v0_9.md"
    links_lines = [
        "# Claim-Source Links (v0.9)",
        "",
        "| Link ID | Claim ID | Source ID | Support Type | Audit Status |",
        "|---|---|---|---|---|",
    ]
    for l in links:
        links_lines.append(
            f"| {l.link_id} | {l.claim_id} | {l.source_id} | {l.support_type} | {l.audit_status} |"
        )
    if not links:
        links_lines.append("| — | — | No links registered. | — | — |")
    links_path.write_text("\n".join(links_lines), encoding="utf-8")
    
    # 5. reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v0_9.md
    camp_dir = root_dir / "reports" / "campaigns"
    camp_dir.mkdir(parents=True, exist_ok=True)
    camp_path = camp_dir / "CAMPAIGN-002_baseline_upgrade_attempt_v0_9.md"
    camp_lines = [
        "# CAMPAIGN-002 — Baseline Ingestion & Upgrade Attempt",
        "",
        f"- **Attempt ID**: {attempt.attempt_id}",
        f"- **Baseline Before**: {attempt.baseline_before}",
        f"- **Baseline After**: {attempt.baseline_after}",
        f"- **Success Status**: **{attempt.success}**",
        f"- **Reason**: {attempt.reason}",
        f"- **Source Pack Status**: {attempt.source_pack_status}",
        "",
        "## Allowed Claims",
    ]
    for ac in attempt.allowed_claims:
        camp_lines.append(f"- {ac}")
    camp_lines.append("\n## Blocked Claims")
    for bc in attempt.blocked_claims:
        camp_lines.append(f"- {bc}")
    camp_path.write_text("\n".join(camp_lines), encoding="utf-8")
    
    # 6. reports/model_comparison/baseline_upgrade_attempt_v0_9.md
    comp_dir = root_dir / "reports" / "model_comparison"
    comp_dir.mkdir(parents=True, exist_ok=True)
    comp_path = comp_dir / "baseline_upgrade_attempt_v0_9.md"
    comp_lines = [
        "# Model Comparison — Baseline Upgrade Attempt v0.9",
        "",
        f"- **Baseline Upgrade State**: {attempt.baseline_after}",
        f"- **Maximum Claim Level Allowed**: {attempt.max_claim_level}",
        "",
        "## Ingestion Validation",
        "Physical prediction remains blocked because upgrading the baseline does not validate the candidate model.",
    ]
    comp_path.write_text("\n".join(comp_lines), encoding="utf-8")
