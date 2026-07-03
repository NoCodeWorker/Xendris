"""Build and write the PHI_GRADIENT local source text registry."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.local_source_text.availability import build_source_availability_manifest
from phyng.local_source_text.file_discovery import discover_local_source_files
from phyng.local_source_text.manual_download_tasks import build_manual_download_tasks
from phyng.local_source_text.schemas import (
    LocalSourceTextRegistry,
    PriorityLocalSourceSpec,
    SourceFileManifest,
    SourceHashManifest,
    SourceHashRecord,
)
from phyng.priority_exact_fill.loader import MANIFEST_V3_2_PATH
from phyng.priority_exact_fill.source_availability import PRIORITY_SOURCE_MAP
from phyng.source_pack_population.schemas import SeedSourceManifest

LOCAL_REGISTRY_PATH = Path("data/real_sources/local_text_registry_v3_6.json")
SOURCE_FILE_MANIFEST_PATH = Path("data/real_sources/source_file_manifest_v3_6.json")
SOURCE_HASHES_PATH = Path("data/real_sources/source_hashes_v3_6.json")
SOURCE_AVAILABILITY_PATH = Path("data/real_sources/source_availability_v3_6.json")
MANUAL_DOWNLOAD_TASKS_PATH = Path("data/real_sources/manual_download_tasks_v3_6.json")

PREFERRED_FILENAMES: dict[str, str] = {
    "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE": "Hornberger_2003_Collisional_Decoherence.pdf",
    "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE": "Hackermueller_2004_Thermal_Emission_Decoherence.pdf",
    "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST": "Nimmrichter_2011_CSL_Matter_Wave_Test.pdf",
    "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS": "Schrinski_2020_QC_Hypothesis_Tests.pdf",
    "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING": "Pedernales_2019_Motional_Dynamical_Decoupling.pdf",
}


def load_reviewed_seed_manifest(root: str | Path = ".") -> tuple[SeedSourceManifest | None, str | None]:
    path = Path(root) / MANIFEST_V3_2_PATH
    if not path.exists():
        return None, f"Missing reviewed seed manifest: {MANIFEST_V3_2_PATH}"
    return SeedSourceManifest.model_validate(json.loads(path.read_text(encoding="utf-8"))), None


def build_priority_local_source_specs(manifest: SeedSourceManifest) -> list[PriorityLocalSourceSpec]:
    entries_by_id = {entry.source_id: entry for entry in manifest.entries}
    specs: list[PriorityLocalSourceSpec] = []
    for priority, (priority_source_id, seed_source_id) in enumerate(PRIORITY_SOURCE_MAP.items(), start=1):
        entry = entries_by_id.get(seed_source_id)
        preferred_filename = PREFERRED_FILENAMES[priority_source_id]
        specs.append(
            PriorityLocalSourceSpec(
                source_id=priority_source_id,
                matched_seed_source_id=seed_source_id if entry else None,
                title=entry.title if entry else priority_source_id,
                preferred_filename=preferred_filename,
                target_path=str(Path("data/real_sources/pdfs") / preferred_filename),
                known_identifiers={
                    "seed_source_id": seed_source_id,
                    "doi": entry.doi if entry else None,
                    "arxiv_id": entry.arxiv_id if entry else None,
                    "url": entry.url if entry else None,
                },
                priority=priority,
            )
        )
    return specs


def build_local_source_text_registry(
    root: str | Path = ".",
) -> tuple[
    list[PriorityLocalSourceSpec],
    LocalSourceTextRegistry,
    SourceFileManifest,
    SourceHashManifest,
    object,
    object,
    str | None,
]:
    manifest, blocked_reason = load_reviewed_seed_manifest(root)
    if blocked_reason or manifest is None:
        empty_registry = LocalSourceTextRegistry(registry_status="PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED")
        return [], empty_registry, SourceFileManifest(), SourceHashManifest(), build_source_availability_manifest([]), build_manual_download_tasks([], []), blocked_reason
    specs = build_priority_local_source_specs(manifest)
    records = discover_local_source_files(specs, root)
    available_count = sum(1 for record in records if record.exists and bool(record.sha256))
    missing_count = sum(1 for record in records if not record.exists)
    hash_count = sum(1 for record in records if record.sha256)
    unsupported_count = sum(1 for record in records if record.registry_status == "LOCAL_SOURCE_FILE_UNSUPPORTED_TYPE")
    status = _campaign_status(len(records), available_count, missing_count)
    registry = LocalSourceTextRegistry(
        source_records=records,
        available_count=available_count,
        missing_count=missing_count,
        hash_count=hash_count,
        unsupported_file_count=unsupported_count,
        registry_status=status,
    )
    file_manifest = SourceFileManifest(source_files=records)
    hash_manifest = SourceHashManifest(
        hashes=[
            SourceHashRecord(
                source_id=record.source_id,
                local_path=record.local_path,
                sha256=record.sha256,
                size_bytes=record.size_bytes or 0,
                file_type=record.file_type,
            )
            for record in records
            if record.sha256
        ]
    )
    availability_manifest = build_source_availability_manifest(records)
    download_tasks = build_manual_download_tasks(specs, records)
    return specs, registry, file_manifest, hash_manifest, availability_manifest, download_tasks, None


def write_local_source_text_outputs(
    root: str | Path,
    registry: LocalSourceTextRegistry,
    file_manifest: SourceFileManifest,
    hash_manifest: SourceHashManifest,
    availability_manifest,
    download_tasks,
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {
        "local_text_registry": repo_root / LOCAL_REGISTRY_PATH,
        "source_file_manifest": repo_root / SOURCE_FILE_MANIFEST_PATH,
        "source_hashes": repo_root / SOURCE_HASHES_PATH,
        "source_availability": repo_root / SOURCE_AVAILABILITY_PATH,
        "manual_download_tasks": repo_root / MANUAL_DOWNLOAD_TASKS_PATH,
    }
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    paths["local_text_registry"].write_text(json.dumps(registry.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    paths["source_file_manifest"].write_text(json.dumps(file_manifest.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    paths["source_hashes"].write_text(json.dumps(hash_manifest.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    paths["source_availability"].write_text(json.dumps(availability_manifest.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    paths["manual_download_tasks"].write_text(json.dumps(download_tasks.model_dump(mode="json"), indent=2, sort_keys=True), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _campaign_status(record_count: int, available_count: int, missing_count: int) -> str:
    if record_count == 0:
        return "PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED"
    if available_count == 0 and missing_count == record_count:
        return "PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING"
    if available_count == record_count:
        return "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY"
    if available_count:
        return "PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL"
    return "PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED"
