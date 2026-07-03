from phyng.source_acquisition.candidate_sources import build_candidate_sources
from phyng.source_acquisition.download_queue import build_download_queue


def test_download_queue_created_for_resolved_sources():
    queue = build_download_queue(build_candidate_sources())

    assert len(queue) >= 3
    assert all(item.requires_manual_download for item in queue)
    assert all(item.target_local_path.startswith("data/real_sources/pdfs/") for item in queue)
