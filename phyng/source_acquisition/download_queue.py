"""Download queue construction."""

from __future__ import annotations

from phyng.source_acquisition.schemas import DownloadQueueItem, SourceAcquisitionQueueItem


def _filename(item: SourceAcquisitionQueueItem) -> str:
    token = item.acquisition_id.split("-", 4)[-1].replace("-", "_")
    return f"{token}.pdf"


def build_download_queue(queue: list[SourceAcquisitionQueueItem]) -> list[DownloadQueueItem]:
    items = []
    for source in queue:
        if source.source_identity_status != "RESOLVED_COMPLETE":
            continue
        filename = _filename(source)
        items.append(
            DownloadQueueItem(
                source_candidate_id=source.acquisition_id,
                download_priority=source.priority,
                preferred_url=source.url_candidate or (f"https://arxiv.org/abs/{source.arxiv_candidate}" if source.arxiv_candidate else None),
                expected_filename=filename,
                target_local_path=f"data/real_sources/pdfs/{filename}",
                requires_manual_download=True,
                requires_paywall_access=source.availability_status == "PAYWALL_LIKELY",
                requires_supplementary_download=source.priority in {"CRITICAL", "HIGH"},
                notes=["Download does not create evidence; y_true extraction remains a later gate."],
            )
        )
    return items
