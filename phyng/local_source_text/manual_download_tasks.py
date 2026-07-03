"""Manual download task generation for missing local source files."""

from __future__ import annotations

from phyng.local_source_text.schemas import (
    LocalSourceFileRecord,
    ManualSourceDownloadTask,
    ManualSourceDownloadTaskManifest,
    PriorityLocalSourceSpec,
)


def build_manual_download_tasks(
    specs: list[PriorityLocalSourceSpec],
    records: list[LocalSourceFileRecord],
) -> ManualSourceDownloadTaskManifest:
    records_by_source = {record.source_id: record for record in records}
    tasks: list[ManualSourceDownloadTask] = []
    for spec in sorted(specs, key=lambda item: item.priority):
        record = records_by_source.get(spec.source_id)
        if record is not None and record.exists and record.sha256:
            continue
        tasks.append(
            ManualSourceDownloadTask(
                task_id=f"DOWNLOAD-{spec.priority:02d}-{spec.source_id}",
                source_id=spec.source_id,
                title=spec.title,
                preferred_filename=spec.preferred_filename,
                target_path=spec.target_path,
                known_identifiers=dict(spec.known_identifiers),
                priority=spec.priority,
                reason="Local source file is missing or not hashable; exact extraction cannot proceed for this source.",
            )
        )
    return ManualSourceDownloadTaskManifest(tasks=tasks)
