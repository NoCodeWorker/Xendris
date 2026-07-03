"""Campaign gate for PHI_GRADIENT reviewed local manifests."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.reviewed_manifest.benchmark_comparability import assess_reviewed_benchmark_comparability
from phyng.reviewed_manifest.extract_validation_bridge import validate_reviewed_extract_pack
from phyng.reviewed_manifest.manifest_loader import load_or_create_reviewed_manifest_inputs
from phyng.reviewed_manifest.manifest_validation import validate_reviewed_manifest
from phyng.reviewed_manifest.schemas import (
    PhiGradientReviewedManifestGateResult,
    ReviewedSourceExtractPack,
    ReviewedSourceManifest,
)
from phyng.reviewed_manifest.slot_coverage import build_reviewed_slot_coverage_matrix


def run_phi_gradient_reviewed_manifest_gate(
    root: str = ".",
    manifest: ReviewedSourceManifest | None = None,
    extract_pack: ReviewedSourceExtractPack | None = None,
) -> PhiGradientReviewedManifestGateResult:
    manifest_created = False
    extract_pack_created = False
    if manifest is None or extract_pack is None:
        loaded_manifest, loaded_pack, manifest_created, extract_pack_created = load_or_create_reviewed_manifest_inputs(root)
        manifest = manifest or loaded_manifest
        extract_pack = extract_pack or loaded_pack

    manifest_validation = validate_reviewed_manifest(manifest)
    extract_validations = validate_reviewed_extract_pack(manifest, extract_pack)
    slot_coverage = build_reviewed_slot_coverage_matrix(manifest, extract_validations)
    benchmark = assess_reviewed_benchmark_comparability(slot_coverage)
    negative_source_ids = [
        validation.source_id
        for validation in extract_validations
        if validation.status == "EXTRACT_VALID_CONTRADICTS_CANDIDATE"
    ]
    status = _determine_status(
        manifest_created,
        manifest_validation.status,
        extract_validations,
        slot_coverage,
        benchmark.status,
        negative_source_ids,
    )
    return PhiGradientReviewedManifestGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="reviewed_manifest"),
        manifest=manifest,
        manifest_validation=manifest_validation,
        extract_pack=extract_pack,
        extract_validations=extract_validations,
        slot_coverage=slot_coverage,
        negative_source_ids=negative_source_ids,
        benchmark_comparability=benchmark,
        manifest_created=manifest_created,
        extract_pack_created=extract_pack_created,
        validated_extract_count=sum(1 for result in extract_validations if result.counts_as_real_support),
        rejected_analogy_count=sum(1 for result in extract_validations if result.status == "EXTRACT_REJECTED_ANALOGY_ONLY"),
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(status),
        next_actions=_next_actions(status),
    )


def _determine_status(
    manifest_created: bool,
    manifest_status: str,
    validations: list,
    slot_coverage,
    benchmark_status: str,
    negative_source_ids: list[str],
) -> str:
    if manifest_created or manifest_status == "REVIEWED_MANIFEST_EMPTY":
        return "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED"
    if manifest_status in {
        "REVIEWED_MANIFEST_INVALID_SCHEMA",
        "REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES",
        "REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES",
    }:
        return "PHI_GRADIENT_REVIEWED_MANIFEST_INVALID"
    if negative_source_ids:
        return "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    if not validations:
        return "PHI_GRADIENT_REVIEWED_MANIFEST_LOADED"
    if benchmark_status == "BENCHMARK_COMPARABLE_REAL_RECORD_FOUND":
        return "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    if _has_source_backed_minimum(slot_coverage):
        return "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    if any(validation.counts_as_real_support for validation in validations):
        return "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    if validations and all(validation.status == "EXTRACT_REJECTED_ANALOGY_ONLY" for validation in validations):
        return "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY"
    return "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"


def _has_source_backed_minimum(slot_coverage) -> bool:
    by_slot = {record.slot_id: record for record in slot_coverage.records}
    observable_or_baseline = any(
        by_slot.get(slot_id) and by_slot[slot_id].accepted_support_count > 0
        for slot_id in {
            "SLOT_1_DECOHERENCE_BASELINE_MODELS",
            "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
        }
    )
    component = (
        by_slot.get("SLOT_4_GRADIENT_TRANSITION_OPERATORS") is not None
        and by_slot["SLOT_4_GRADIENT_TRANSITION_OPERATORS"].accepted_support_count > 0
    )
    return observable_or_baseline and component


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED":
        return ["Reviewed manifest and extract-pack templates were created."]
    if status == "PHI_GRADIENT_REVIEWED_MANIFEST_LOADED":
        return ["A reviewed local manifest was loaded for extract review."]
    if status in {"PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED", "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"}:
        return ["Limited source-pressure statements tied to validated reviewed extracts."]
    return ["Reviewed-manifest campaign executed under conservative claim controls."]


def _blocked_claims(status: str) -> list[str]:
    claims = [
        "A reviewed manifest proves PHI_GRADIENT.",
        "A source candidate is evidence.",
        "A benchmark candidate is benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT validates Frontera C.",
    ]
    if status != "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        claims.append("PHI_GRADIENT has benchmark-comparable real support.")
    return claims


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED":
        return ["Populate the reviewed local manifest with traceable sources.", "Add extract pack entries before claiming source pressure."]
    if status == "PHI_GRADIENT_REVIEWED_MANIFEST_LOADED":
        return ["Extract slot-specific text, equations, observables and benchmark ranges.", "Validate extracts before counting support."]
    if status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED":
        return ["Review the contradiction and down-rank or narrow the candidate claim."]
    if status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        return ["Schedule benchmark comparison pressure.", "Keep physical claims blocked."]
    if status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        return ["Schedule parameter alignment and numerical benchmark comparison.", "Keep experimental validation blocked."]
    return ["Improve manifest coverage and target missing slots."]
