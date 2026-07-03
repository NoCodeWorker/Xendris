"""Campaign orchestration for PHI_GRADIENT PDF/text extraction v3.7."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.pdf_text_extraction.candidate_detection import detect_observable_candidates, detect_quote_candidates
from phyng.pdf_text_extraction.equation_detection import detect_equation_candidates
from phyng.pdf_text_extraction.extraction_manifest import build_extraction_manifest, write_extraction_outputs
from phyng.pdf_text_extraction.negative_detection import detect_negative_candidates
from phyng.pdf_text_extraction.page_extraction import extract_pages_for_sources
from phyng.pdf_text_extraction.range_detection import detect_caption_candidates, detect_range_candidates
from phyng.pdf_text_extraction.registry_loader import load_hashed_pdf_sources
from phyng.pdf_text_extraction.report import write_pdf_text_extraction_reports
from phyng.pdf_text_extraction.schemas import PhiGradientPDFTextExtractionCampaignResult, PhiGradientPDFTextExtractionResult


def run_phi_gradient_pdf_text_extraction_campaign(root: str | Path = ".") -> PhiGradientPDFTextExtractionCampaignResult:
    repo_root = Path(root)
    sources, input_registry_id, blocked_reason = load_hashed_pdf_sources(repo_root)
    pages = []
    summaries = []
    if blocked_reason is None:
        pages, summaries = extract_pages_for_sources(sources, repo_root)
    quote_candidates = detect_quote_candidates(pages) + detect_observable_candidates(pages)
    equation_candidates = detect_equation_candidates(pages)
    table_range_candidates = detect_range_candidates(pages) + detect_caption_candidates(pages)
    negative_candidates = detect_negative_candidates(pages)
    candidate_count_by_source: dict[str, int] = {}
    for candidate in quote_candidates + equation_candidates + table_range_candidates + negative_candidates:
        candidate_count_by_source[candidate.source_id] = candidate_count_by_source.get(candidate.source_id, 0) + 1
    for summary in summaries:
        summary.candidate_count = candidate_count_by_source.get(summary.source_id, 0)

    manifest = build_extraction_manifest(
        input_registry_id=input_registry_id,
        sources=sources,
        pages=pages,
        summaries=summaries,
        quote_candidates=quote_candidates,
        equation_candidates=equation_candidates,
        table_range_candidates=table_range_candidates,
        negative_candidates=negative_candidates,
        blocked_reason=blocked_reason,
    )
    output_paths = write_extraction_outputs(repo_root, manifest, pages, quote_candidates, equation_candidates, table_range_candidates, negative_candidates)
    status = manifest.status
    extraction_result = PhiGradientPDFTextExtractionResult(
        status=status,
        canonical_status=normalize_status(status, domain="pdf_text_extraction"),
        registered_sources=sources,
        pages=pages,
        quote_candidates=quote_candidates,
        equation_candidates=equation_candidates,
        table_range_candidates=table_range_candidates,
        negative_candidates=negative_candidates,
        manifest=manifest,
        output_paths=output_paths,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=_next_actions(status),
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7",
        input_type="PDF_TEXT_EXTRACTION_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_LOCAL_SOURCE_FILES_READY",
        result_status=status,
        payload={
            "hashed_sources_seen": manifest.hashed_sources_seen,
            "sources_extracted": manifest.sources_extracted,
            "total_candidates": manifest.total_candidates,
            "manual_review_count": manifest.manual_review_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7-{status}",
        proposal_type="PDF_TEXT_EXTRACTION_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="PDF/text extraction ran under hashed-source boundaries; candidates require review before source pressure.",
        proposed_change={
            "status": status,
            "hashed_sources_seen": manifest.hashed_sources_seen,
            "sources_extracted": manifest.sources_extracted,
            "total_candidates": manifest.total_candidates,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "treat extracted candidate as source support",
            "treat extracted range as benchmark support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientPDFTextExtractionCampaignResult(
        campaign_id="PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7",
        status=status,
        extraction_result=extraction_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_pdf_text_extraction_reports(result, repo_root / "reports")
    return result


def _allowed_claims(status: str) -> list[str]:
    if status in {"PHI_GRADIENT_PDF_EXTRACTION_COMPLETED", "PHI_GRADIENT_PDF_EXTRACTION_PARTIAL"}:
        return [
            "PDF/text extraction was performed on hashed local sources.",
            "Candidate quotes/equations/ranges were generated.",
            "Candidates require review before validation.",
        ]
    if status == "PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW":
        return ["Hashed local PDFs were queued, but extraction requires manual review or a PDF reader."]
    return ["PDF/text extraction boundary checks were performed."]


def _blocked_claims() -> list[str]:
    return [
        "PDF extraction validates PHI_GRADIENT.",
        "Extracted quote candidate is source support.",
        "Equation candidate is physical support.",
        "Benchmark candidate is benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
    ]


def _next_actions(status: str) -> list[str]:
    if status in {"PHI_GRADIENT_PDF_EXTRACTION_COMPLETED", "PHI_GRADIENT_PDF_EXTRACTION_PARTIAL"}:
        return ["Run v3.8 extract candidate review and validation-ready pack assembly."]
    if status == "PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW":
        return ["Install or provide a lightweight PDF text reader, or manually review the local PDFs without promoting claims."]
    if status == "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING":
        return ["Restore v3.6 local source registry artifacts before extraction."]
    if status == "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES":
        return ["Run v3.6 until local source files are hashed."]
    return ["Review extraction artifacts before v3.8."]
