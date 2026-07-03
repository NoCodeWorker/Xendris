"""
Phygn v1.0 — Baseline Limited Upgrade Execution

Orchestrates the full BASELINE-SRC-PACK-001 pipeline:
  scan → register → audit → support matrix → upgrade attempt → report

The only valid limited upgrade is:
    FORMULA_SUPPORT + OBSERVABLE_SUPPORT + PASSED_LIMITED audit → BASELINE_SOURCE_BACKED_LIMITED

Candidate physical prediction remains BLOCKED under all outcomes.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from phyng.baselines.source_pack import evaluate_source_pack
from phyng.baselines.upgrade_attempt import run_baseline_upgrade_attempt_v0_9
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult, audit_citation_v0_9
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09
from phyng.evidence.local_source_scanner import scan_local_sources
from phyng.evidence.source_candidates import SourceCandidate
from phyng.evidence.source_records_v0_9 import SourceRecordV09

_STILL_BLOCKED: list[str] = [
    "Phygn predicts gravitational decoherence.",
    "Frontera C is validated.",
    "The boundary-aware candidate is validated.",
    "SyntheticGain is physical PredictiveGain.",
]

_REQUIREMENT_TO_SUPPORT: dict[str, str] = {
    "BSR-001": "FORMULA_SUPPORT",
    "BSR-003": "OBSERVABLE_SUPPORT",
    "BSR-002": "PARAMETER_SUPPORT",
    "BSR-004": "CONTEXT_SUPPORT",
}


class BaselineUpgradeExecutionResult(BaseModel):
    """Full result of the BASELINE-SRC-PACK-001 ingestion & upgrade campaign."""

    execution_id: str
    campaign_id: str = "BASELINE-SRC-PACK-001"
    linked_campaign_id: str = "CAMPAIGN-002"
    source_pack_status: str
    audited_sources_count: int = 0
    formula_support_count: int = 0
    observable_support_count: int = 0
    parameter_support_count: int = 0
    contradiction_count: int = 0
    baseline_before: str = "TOY_INTERNAL"
    baseline_after: str
    upgrade_success: bool
    max_claim_level: int = 3
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    report_paths: list[str] = Field(default_factory=list)


def _candidate_to_record(candidate: SourceCandidate, idx: int) -> SourceRecordV09:
    """Convert a SourceCandidate to a SourceRecordV09 for auditing."""
    has_local = False
    if candidate.local_path:
        p = Path(candidate.local_path)
        has_local = p.exists() and p.is_file()

    if has_local:
        ingestion_status = "INGESTED_WITH_EXTRACTS"
        metadata_status = (
            "COMPLETE"
            if (candidate.title and candidate.authors and candidate.year)
            else "PARTIAL"
        )
    else:
        ingestion_status = "NOT_INGESTED"
        metadata_status = "UNKNOWN"

    return SourceRecordV09(
        source_id=f"SRC-V10-{idx + 1:03d}",
        title=candidate.title,
        authors=candidate.authors,
        year=candidate.year,
        source_type=candidate.source_type,
        trust_level=candidate.trust_level,
        local_path=candidate.local_path,
        url=candidate.url,
        ingestion_status=ingestion_status,
        metadata_status=metadata_status,
        notes=candidate.notes,
    )


def _link_from_audit(
    record: SourceRecordV09,
    audit: CitationAuditResult,
    requirement_id: str,
    idx: int,
    candidate: SourceCandidate,
) -> ClaimSourceLinkV09 | None:
    """Create a ClaimSourceLinkV09 if the audit passed."""
    if not audit.passed:
        return None
    support_type = _REQUIREMENT_TO_SUPPORT.get(requirement_id, "CONTEXT_SUPPORT")
    return ClaimSourceLinkV09(
        link_id=f"LINK-V10-{idx + 1:03d}",
        claim_id="CLAIM-DECOH-001",
        source_id=record.source_id,
        support_type=support_type,
        support_strength="HIGH" if record.trust_level in {"PRIMARY", "HIGH"} else "MEDIUM",
        quote_or_excerpt=(
            candidate.notes
            if candidate.notes and len(candidate.notes) < 200
            else None
        ),
        local_reference="See local file",
        audit_status=audit.audit_status,
    )


def run_limited_upgrade_execution(
    project_root: Path,
    execution_id: str = "EXEC-V10-001",
) -> BaselineUpgradeExecutionResult:
    """
    Full BASELINE-SRC-PACK-001 execution:

    1. Scan sources/baseline/
    2. Convert to SourceRecordV09
    3. Run citation audits
    4. Build ClaimSourceLinks
    5. Build BaselineSourcePack
    6. Run upgrade attempt
    7. Generate all v1.0 reports
    """
    # Step 1 — Scan
    candidates = scan_local_sources(project_root)

    # Steps 2-4 — Convert, audit, link
    records: list[SourceRecordV09] = []
    audits: list[CitationAuditResult] = []
    links: list[ClaimSourceLinkV09] = []

    for idx, cand in enumerate(candidates):
        record = _candidate_to_record(cand, idx)
        records.append(record)
        audit = audit_citation_v0_9(record)
        audits.append(audit)
        link = _link_from_audit(record, audit, cand.requirement_id, idx, cand)
        if link:
            links.append(link)

    # Step 5 — Build pack
    pack = evaluate_source_pack(
        "BSP-V10-001", "CAMPAIGN-002", candidates, audits, links
    )

    # Step 6 — Upgrade attempt
    has_parameter = any(lnk.support_type == "PARAMETER_SUPPORT" for lnk in links)
    has_assumptions = len(candidates) > 0

    attempt = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-V10-001",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links,
        has_parameter=has_parameter,
        has_assumptions=has_assumptions,
    )

    # Count support types
    formula_count = sum(1 for lnk in links if lnk.support_type == "FORMULA_SUPPORT")
    obs_count = sum(1 for lnk in links if lnk.support_type == "OBSERVABLE_SUPPORT")
    param_count = sum(1 for lnk in links if lnk.support_type == "PARAMETER_SUPPORT")
    contra_count = sum(1 for lnk in links if lnk.support_type == "CONTRADICTION")

    # Step 7 — Reports
    report_paths = _write_v1_0_reports(
        project_root, pack, candidates, audits, links, attempt
    )

    return BaselineUpgradeExecutionResult(
        execution_id=execution_id,
        source_pack_status=pack.coverage_status,
        audited_sources_count=len([a for a in audits if a.passed]),
        formula_support_count=formula_count,
        observable_support_count=obs_count,
        parameter_support_count=param_count,
        contradiction_count=contra_count,
        baseline_after=attempt.baseline_after,
        upgrade_success=attempt.success,
        max_claim_level=attempt.max_claim_level,
        allowed_claims=attempt.allowed_claims,
        blocked_claims=list(_STILL_BLOCKED),
        report_paths=report_paths,
    )


def _write_v1_0_reports(
    project_root: Path,
    pack,
    candidates: list[SourceCandidate],
    audits: list[CitationAuditResult],
    links: list[ClaimSourceLinkV09],
    attempt,
) -> list[str]:
    rag_dir = project_root / "reports" / "rag"
    rag_dir.mkdir(parents=True, exist_ok=True)
    camp_dir = project_root / "reports" / "campaigns"
    camp_dir.mkdir(parents=True, exist_ok=True)
    comp_dir = project_root / "reports" / "model_comparison"
    comp_dir.mkdir(parents=True, exist_ok=True)

    paths: list[str] = []

    # 1. baseline_source_pack_v1_0.md
    p = rag_dir / "baseline_source_pack_v1_0.md"
    p.write_text(
        "\n".join([
            "# Baseline Source Pack — v1.0",
            "",
            f"- **Pack ID**: BSP-V10-001",
            f"- **Campaign**: CAMPAIGN-002",
            f"- **Coverage Status**: **{pack.coverage_status}**",
            f"- **Ready for Upgrade**: {pack.ready_for_upgrade_attempt}",
            f"- **Candidates Registered**: {len(candidates)}",
            "",
            "## Missing Requirements",
            *([f"- {m}" for m in pack.missing_requirements] or ["- None"]),
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    # 2. baseline_support_matrix_v1_0.md
    p = rag_dir / "baseline_support_matrix_v1_0.md"
    rows = [
        f"| {lnk.link_id} | {lnk.source_id} | {lnk.support_type} | {lnk.support_strength} | {lnk.audit_status} |"
        for lnk in links
    ] or ["| — | — | No support links registered. | — | — |"]
    p.write_text(
        "\n".join([
            "# Baseline Support Matrix — v1.0",
            "",
            "| Link ID | Source ID | Support Type | Strength | Audit Status |",
            "|---|---|---|---|---|",
            *rows,
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    # 3. citation_audit_v1_0.md
    p = rag_dir / "citation_audit_v1_0.md"
    audit_rows = [
        f"| {a.source_id} | {a.passed} | {a.audit_status} | {'; '.join(a.trust_issues + a.extraction_issues + a.missing_fields) or 'None'} |"
        for a in audits
    ] or ["| — | — | No audits performed. | — |"]
    p.write_text(
        "\n".join([
            "# Citation Audit Results — v1.0",
            "",
            "| Source ID | Passed | Audit Status | Issues |",
            "|---|---|---|---|",
            *audit_rows,
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    # 4. BASELINE-SRC-PACK-001_ingestion_result.md
    p = camp_dir / "BASELINE-SRC-PACK-001_ingestion_result.md"
    p.write_text(
        "\n".join([
            "# BASELINE-SRC-PACK-001 — Source Ingestion Result",
            "",
            f"- **Candidates Scanned**: {len(candidates)}",
            f"- **Audited (passed)**: {len([a for a in audits if a.passed])}",
            f"- **Pack Coverage**: **{pack.coverage_status}**",
            f"- **Baseline Before**: {attempt.baseline_before}",
            f"- **Baseline After**: **{attempt.baseline_after}**",
            f"- **Upgrade Success**: **{attempt.success}**",
            f"- **Reason**: {attempt.reason}",
            "",
            "## Allowed Claims",
            *([f"- {c}" for c in attempt.allowed_claims] or ["- None"]),
            "",
            "## Blocked Claims",
            *[f"- {c}" for c in _STILL_BLOCKED],
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    # 5. CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md
    p = camp_dir / "CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md"
    p.write_text(
        "\n".join([
            "# CAMPAIGN-002 — Baseline Upgrade Attempt (v1.0)",
            "",
            f"- **Baseline After**: **{attempt.baseline_after}**",
            f"- **Success**: {attempt.success}",
            f"- **Reason**: {attempt.reason}",
            f"- **Max Claim Level**: {attempt.max_claim_level}",
            "",
            "## Physical Prediction Status",
            "- candidate_status = HYPOTHETICAL_CANDIDATE (unchanged)",
            "- can_claim_physical_prediction = False (unchanged)",
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    # 6. CAMPAIGN-002_source_backed_baseline_status_v1_0.md
    p = comp_dir / "CAMPAIGN-002_source_backed_baseline_status_v1_0.md"
    p.write_text(
        "\n".join([
            "# Model Comparison — Source-Backed Baseline Status (v1.0)",
            "",
            f"- **Baseline Status**: **{attempt.baseline_after}**",
            f"- **Max Claim Level**: {attempt.max_claim_level}",
            "",
            "## Principle",
            "A source-backed limited baseline is a legitimate opponent.",
            "It does not validate the boundary-aware candidate.",
            "Physical prediction remains blocked until the candidate model",
            "is independently source-backed.",
        ]),
        encoding="utf-8",
    )
    paths.append(str(p))

    return paths
