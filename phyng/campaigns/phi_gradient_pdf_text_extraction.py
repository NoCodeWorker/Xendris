"""Campaign wrapper for PHI_GRADIENT PDF/text extraction v3.7."""

from phyng.pdf_text_extraction.campaign import run_phi_gradient_pdf_text_extraction_campaign

__all__ = ["run_phi_gradient_pdf_text_extraction_campaign"]


if __name__ == "__main__":
    result = run_phi_gradient_pdf_text_extraction_campaign()
    manifest = result.extraction_result.manifest
    print(
        {
            "status": result.status,
            "hashed_sources_seen": manifest.hashed_sources_seen,
            "sources_extracted": manifest.sources_extracted,
            "sources_blocked": manifest.sources_blocked,
            "total_candidates": manifest.total_candidates,
        }
    )
