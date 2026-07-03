"""Reports for PHI_GRADIENT PDF/text extraction v3.7."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.pdf_text_extraction.schemas import PhiGradientPDFTextExtractionCampaignResult, PDFExtractionCandidate


def write_pdf_text_extraction_reports(
    result: PhiGradientPDFTextExtractionCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "pdf_text_extraction"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": report_dir / "phi_gradient_pdf_extraction_manifest_v3_7.md",
        "source_coverage": report_dir / "phi_gradient_pdf_source_coverage_v3_7.md",
        "quote_candidates": report_dir / "phi_gradient_pdf_quote_candidates_v3_7.md",
        "equation_candidates": report_dir / "phi_gradient_pdf_equation_candidates_v3_7.md",
        "table_range_candidates": report_dir / "phi_gradient_pdf_table_range_candidates_v3_7.md",
        "negative_constraint_candidates": report_dir / "phi_gradient_pdf_negative_constraint_candidates_v3_7.md",
        "next_gate": report_dir / "phi_gradient_pdf_extraction_next_gate_v3_7.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7.md",
    }
    renderers = {
        "manifest": _render_manifest,
        "source_coverage": _render_source_coverage,
        "quote_candidates": lambda item: _render_candidates("PHI_GRADIENT Quote Candidates v3.7", item.extraction_result.quote_candidates),
        "equation_candidates": lambda item: _render_candidates("PHI_GRADIENT Equation Candidates v3.7", item.extraction_result.equation_candidates),
        "table_range_candidates": lambda item: _render_candidates("PHI_GRADIENT Table and Range Candidates v3.7", item.extraction_result.table_range_candidates),
        "negative_constraint_candidates": lambda item: _render_candidates("PHI_GRADIENT Negative Constraint Candidates v3.7", item.extraction_result.negative_candidates),
        "next_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientPDFTextExtractionCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    extraction = result.extraction_result
    contract = build_report_contract(
        title="PHI_GRADIENT PDF/Text Extraction v3.7",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="pdf_text_extraction",
        reports_generated=reports_generated or [],
        next_actions=extraction.next_actions,
        discipline_note="Extraction is contact, not belief.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: PhiGradientPDFTextExtractionCampaignResult) -> str:
    manifest = result.extraction_result.manifest
    return "\n".join(
        [
            "# PHI_GRADIENT PDF Extraction Manifest v3.7",
            "",
            f"- status: `{manifest.status}`",
            f"- hashed_input_sources: `{manifest.hashed_sources_seen}`",
            f"- extracted_sources: `{manifest.sources_extracted}`",
            f"- blocked_sources: `{manifest.sources_blocked}`",
            f"- pages_extracted: `{manifest.total_pages_extracted}`",
            f"- total_candidates: `{manifest.total_candidates}`",
            f"- quote_candidate_count: `{manifest.quote_candidate_count}`",
            f"- equation_candidate_count: `{manifest.equation_candidate_count}`",
            f"- range_table_candidate_count: `{manifest.table_range_candidate_count}`",
            f"- negative_candidate_count: `{manifest.negative_candidate_count}`",
            f"- manual_review_count: `{manifest.manual_review_count}`",
            f"- reader_availability: `{manifest.reader_availability}`",
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in result.extraction_result.blocked_claims],
        ]
    ) + "\n"


def _render_source_coverage(result: PhiGradientPDFTextExtractionCampaignResult) -> str:
    summaries = result.extraction_result.manifest.source_summaries
    return "\n".join(
        [
            "# PHI_GRADIENT PDF Source Coverage v3.7",
            "",
            *_or_none(
                [
                    f"- `{item.source_id}`: status=`{item.extraction_status}`, reader=`{item.reader_used}`, pages=`{item.pages_extracted}`, candidates=`{item.candidate_count}`, manual_review=`{item.requires_manual_review}`"
                    for item in summaries
                ]
            ),
        ]
    ) + "\n"


def _render_candidates(title: str, candidates: list[PDFExtractionCandidate]) -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            f"- candidate_count: `{len(candidates)}`",
            "",
            *_or_none(
                [
                    f"- `{item.candidate_id}`: source=`{item.source_id}`, page=`{item.page_number}`, type=`{item.candidate_type}`, review=`{item.requires_manual_review}`"
                    for item in candidates[:40]
                ]
            ),
            "",
            "Reports summarize candidate metadata only; full extracted text is in JSON artifacts.",
        ]
    ) + "\n"


def _render_next_gate(result: PhiGradientPDFTextExtractionCampaignResult) -> str:
    extraction = result.extraction_result
    return "\n".join(
        [
            "# PHI_GRADIENT PDF Extraction Next Gate v3.7",
            "",
            f"- status: `{extraction.status}`",
            "",
            "## Allowed Claims",
            "",
            *[f"- {claim}" for claim in extraction.allowed_claims],
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in extraction.blocked_claims],
            "",
            "## Next Actions",
            "",
            *[f"- {action}" for action in extraction.next_actions],
        ]
    ) + "\n"


def _render_campaign(result: PhiGradientPDFTextExtractionCampaignResult) -> str:
    manifest = result.extraction_result.manifest
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- hashed_input_sources: `{manifest.hashed_sources_seen}`",
            f"- extracted_sources: `{manifest.sources_extracted}`",
            f"- blocked_sources: `{manifest.sources_blocked}`",
            f"- total_candidates: `{manifest.total_candidates}`",
            f"- manual_review_count: `{manifest.manual_review_count}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
