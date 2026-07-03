"""Candidate family source inventory construction."""

from __future__ import annotations

from pathlib import Path

from phyng.source_identity_preflight.schemas import CandidateFamilySourceInventory, SourceIdentityPreflightInputs


REQUIRED_FAMILIES = [
    "PHI_CURVATURE",
    "PHI_LOCALIZED_WINDOW",
    "PHI_BANDPASS",
    "PHI_GRADIENT",
    "B_SUPPRESSED",
    "QB_STRUCTURAL",
    "LOG_BOUNDARY",
    "THRESHOLD_SATURATION",
]


def build_candidate_family_source_inventory(root: str | Path, inputs: SourceIdentityPreflightInputs) -> list[CandidateFamilySourceInventory]:
    local_registry = _load_local_registry(Path(root))
    matrix_by_family = {row.get("family_id"): row for row in inputs.candidate_matrix}
    inventory: list[CandidateFamilySourceInventory] = []
    for family in REQUIRED_FAMILIES:
        matrix = matrix_by_family.get(family, {})
        raw_refs = _raw_refs_for_family(family, inputs)
        local_pdf_refs = _local_pdf_refs_for_family(family, local_registry)
        resolved = _known_resolved_sources_for_family(family, inputs)
        notes = list(matrix.get("notes", []))
        if family == "PHI_GRADIENT":
            notes.append("Preserved as METHOD_ONLY_EMPIRICALLY_UNGROUNDED.")
        if family == "PHI_CURVATURE" and inputs.v48_gate.get("final_status"):
            notes.append(f"v4.8 status: {inputs.v48_gate.get('final_status')}.")
        inventory.append(
            CandidateFamilySourceInventory(
                family_id=family,
                previous_status=_previous_status(family, matrix, inputs),
                raw_source_refs=raw_refs,
                known_resolved_sources=resolved,
                local_pdf_refs=local_pdf_refs,
                supplementary_refs=[],
                dataset_refs=[],
                inventory_status=_inventory_status(raw_refs, resolved, local_pdf_refs),
                notes=notes,
            )
        )
    return inventory


def _raw_refs_for_family(family: str, inputs: SourceIdentityPreflightInputs) -> list[str]:
    if family == "PHI_CURVATURE":
        return [record.get("source_ref_raw", "") for record in inputs.v48_resolution if record.get("source_ref_raw")]
    return []


def _known_resolved_sources_for_family(family: str, inputs: SourceIdentityPreflightInputs) -> list[str]:
    if family != "PHI_CURVATURE":
        return []
    return [
        record.get("source_id", "")
        for record in inputs.v48_resolution
        if record.get("identity_complete") is True or record.get("resolution_status") in {"RESOLVED_LOCAL", "RESOLVED_EXTERNAL_IDENTITY"}
    ]


def _previous_status(family: str, matrix: dict, inputs: SourceIdentityPreflightInputs) -> str | None:
    if family == "PHI_GRADIENT":
        return inputs.phi_gradient_method_only.get("required_label") or "METHOD_ONLY_EMPIRICALLY_UNGROUNDED"
    if family == "PHI_CURVATURE":
        return inputs.v48_gate.get("final_status") or matrix.get("previous_status")
    return matrix.get("previous_status")


def _inventory_status(raw_refs: list[str], resolved: list[str], local_pdf_refs: list[str]) -> str:
    if resolved:
        return "HAS_RESOLVED_SOURCES"
    if local_pdf_refs:
        return "HAS_LOCAL_ARTIFACTS"
    if raw_refs:
        return "HAS_RAW_REFS_ONLY"
    return "NO_SOURCE_REFS"


def _local_pdf_refs_for_family(family: str, local_registry: dict) -> list[str]:
    if family not in {local_registry.get("candidate_family"), local_registry.get("phi_family")}:
        return []
    refs: list[str] = []
    for record in local_registry.get("source_records", []):
        if record.get("exists") and record.get("local_path"):
            refs.append(record["local_path"])
    return refs


def _load_local_registry(root: Path) -> dict:
    path = root / "data" / "real_sources" / "local_text_registry_v3_6.json"
    if not path.exists():
        return {}
    import json

    return json.loads(path.read_text(encoding="utf-8"))
