"""Candidate source identity matrix construction."""

from __future__ import annotations

from phyng.source_acquisition.schemas import CandidateSourceIdentityRecord, SourceAcquisitionQueueItem


def build_identity_matrix(queue: list[SourceAcquisitionQueueItem]) -> list[CandidateSourceIdentityRecord]:
    records = []
    for item in queue:
        missing = []
        if not item.source_title_candidate:
            missing.append("title")
        if not item.authors_candidate and not item.publication_candidate:
            missing.append("authors_or_publication_authority")
        if item.year_candidate is None:
            missing.append("year")
        if not (item.doi_candidate or item.arxiv_candidate or item.url_candidate):
            missing.append("doi_or_arxiv_or_url")
        complete = not missing and item.source_identity_status == "RESOLVED_COMPLETE"
        score = (4 - len(missing)) / 4
        records.append(
            CandidateSourceIdentityRecord(
                source_candidate_id=item.acquisition_id,
                title=item.source_title_candidate,
                authors=item.authors_candidate,
                year=item.year_candidate,
                publication=item.publication_candidate,
                doi=item.doi_candidate,
                arxiv=item.arxiv_candidate,
                url=item.url_candidate,
                identity_completeness_score=score,
                identity_complete=complete,
                missing_identity_fields=missing,
            )
        )
    return records
