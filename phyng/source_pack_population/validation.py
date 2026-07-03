"""Validation for v3.2 source-pack population."""

from __future__ import annotations

from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest, SourcePackPopulationValidationResult
from phyng.source_pressure.slots import build_phi_gradient_source_slots


VALID_SLOTS = {slot.slot_id for slot in build_phi_gradient_source_slots()}


def validate_seed_pack(manifest: SeedSourceManifest, extract_pack: SeedSourceExtractPack) -> SourcePackPopulationValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    traceable_count = 0
    valid_slot_count = 0
    benchmark_count = 0
    negative_count = 0

    for entry in manifest.entries:
        if entry.doi or entry.arxiv_id or entry.url or entry.local_path:
            traceable_count += 1
        else:
            errors.append(f"{entry.source_id}: missing traceable identifier")
        if set(entry.target_slots).intersection(VALID_SLOTS):
            valid_slot_count += 1
        else:
            errors.append(f"{entry.source_id}: missing valid target slot")
        if entry.evidence_status != "CANDIDATE_NOT_VALIDATED":
            errors.append(f"{entry.source_id}: seed evidence_status must remain CANDIDATE_NOT_VALIDATED")
        if "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS" in entry.target_slots:
            benchmark_count += 1
        if "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES" in entry.target_slots or entry.review_status == "REVIEWED_SOURCE_NEGATIVE_CANDIDATE":
            negative_count += 1

    manifest_ids = {entry.source_id for entry in manifest.entries}
    manual_review_count = 0
    for extract in extract_pack.extracts:
        if extract.source_id not in manifest_ids:
            errors.append(f"{extract.extract_id}: source_id not present in manifest")
        if extract.slot_id not in VALID_SLOTS:
            errors.append(f"{extract.extract_id}: invalid slot")
        if not extract.manual_review_required:
            errors.append(f"{extract.extract_id}: seed extract must require manual review")
        else:
            manual_review_count += 1
        if extract.initial_validation_status != "EXTRACT_CANDIDATE_REQUIRES_REVIEW":
            errors.append(f"{extract.extract_id}: seed extract cannot start as validated support")

    if benchmark_count == 0:
        warnings.append("No benchmark candidate sources found.")
    if negative_count == 0:
        warnings.append("No negative source candidates found.")

    status = "PHI_GRADIENT_SOURCE_PACK_BLOCKED" if errors else "PHI_GRADIENT_SOURCE_PACK_POPULATED"
    return SourcePackPopulationValidationResult(
        status=status,
        manifest_entry_count=len(manifest.entries),
        extract_count=len(extract_pack.extracts),
        traceable_entry_count=traceable_count,
        valid_slot_entry_count=valid_slot_count,
        benchmark_candidate_count=benchmark_count,
        negative_candidate_count=negative_count,
        manual_review_extract_count=manual_review_count,
        warnings=warnings,
        errors=errors,
    )
