"""Seed source-pack generation for PHI_GRADIENT v3.2."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_pack_population.schemas import SeedSourceExtract, SeedSourceExtractPack, SeedSourceManifest, SeedSourceManifestEntry


MANIFEST_SEED_PATH = Path("data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json")
EXTRACT_SEED_PATH = Path("data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json")


def build_seed_manifest() -> SeedSourceManifest:
    return SeedSourceManifest(
        entries=[
            _entry("SRC-PHI-V32-001", "Collisional decoherence observed in matter-wave interferometry", ["Hornberger", "Sipe"], 2003, "quant-ph/0303093", ["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"], ["environmental_decoherence_baseline", "visibility_decay_observable", "Gamma_env_rate"], ["RISK_REVIEW_REQUIRED"]),
            _entry("SRC-PHI-V32-002", "Decoherence of matter waves by thermal emission of radiation", ["Hackermuller", "Hornberger", "Brezger", "Zeilinger"], 2004, "quant-ph/0402146", ["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"], ["visibility_decay_observable", "environmental_decoherence_baseline"], ["RISK_OBSERVABLE_MISMATCH", "RISK_REVIEW_REQUIRED"]),
            _entry("SRC-PHI-V32-003", "Decoherence in a Talbot-Lau interferometer: the influence of molecular scattering", ["Hornberger", "Uttenthaler", "Brezger", "Hackermuller", "Arndt", "Zeilinger"], 2004, "quant-ph/0407245", ["SLOT_1_DECOHERENCE_BASELINE_MODELS"], ["environmental_decoherence_baseline", "Gamma_env_rate"], ["RISK_REVIEW_REQUIRED"]),
            _entry("SRC-PHI-V32-004", "Matter-wave interference of particles selected from a molecular library with masses exceeding 10000 amu", ["Eibenberger", "Gerstmayr", "Juffmann", "Nimmrichter", "Arndt"], 2013, "1310.8343", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"], ["mesoscopic_mass_length_time_range", "visibility_decay_observable", "benchmark_dataset_or_table"], ["RISK_BENCHMARK_NOT_COMPARABLE", "RISK_REVIEW_REQUIRED"], review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE"),
            _entry("SRC-PHI-V32-005", "Macroscopicity of mechanical quantum superposition states", ["Nimmrichter", "Hornberger"], 2012, "1205.3447", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS"], ["mesoscopic_mass_length_time_range", "alpha_like_parameter_constraint"], ["RISK_NO_ALPHA_CONSTRAINT", "RISK_REVIEW_REQUIRED"], review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE"),
            _entry("SRC-PHI-V32-006", "MAQRO: a test of macroscopic quantumness in space", ["Kaltenbaek", "Aspelmeyer", "Barker", "Bassi", "Bateman", "Bose", "Ulbricht"], 2012, "1201.4756", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS"], ["benchmark_dataset_or_table", "alpha_like_parameter_constraint"], ["RISK_BENCHMARK_NOT_COMPARABLE", "RISK_REVIEW_REQUIRED"], review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE"),
            _entry("SRC-PHI-V32-007", "Testing the limits of quantum mechanical superpositions", ["Nimmrichter", "Hornberger", "Haslinger", "Arndt"], 2014, "1410.0270", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS"], ["benchmark_dataset_or_table", "alpha_like_parameter_constraint"], ["RISK_NO_ALPHA_CONSTRAINT", "RISK_REVIEW_REQUIRED"], review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE"),
            _entry("SRC-PHI-V32-008", "Models of wave-function collapse, underlying theories, and experimental tests", ["Bassi", "Lochan", "Satin", "Singh", "Ulbricht"], 2012, "1204.4325", ["SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"], ["alpha_like_parameter_constraint", "negative_or_exclusion_constraint"], ["RISK_SOURCE_MAY_BE_NEGATIVE", "RISK_NOT_DIRECTLY_PHI_GRADIENT"], review_status="REVIEWED_SOURCE_NEGATIVE_CANDIDATE"),
            _entry("SRC-PHI-V32-009", "Quantum-classical hypothesis tests in macroscopic matter-wave interferometry", ["Nimmrichter", "Hornberger"], 2020, "2004.03392", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"], ["benchmark_dataset_or_table", "negative_or_exclusion_constraint"], ["RISK_SOURCE_MAY_BE_NEGATIVE", "RISK_BENCHMARK_NOT_COMPARABLE"], review_status="REVIEWED_SOURCE_NEGATIVE_CANDIDATE"),
            _entry("SRC-PHI-V32-010", "Motional dynamical decoupling with matter-wave interferometry", ["Russo", "Murch", "et al."], 2019, "1906.00835", ["SLOT_4_GRADIENT_TRANSITION_OPERATORS", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"], ["gradient_transition_operator", "visibility_decay_observable"], ["RISK_NOT_DIRECTLY_PHI_GRADIENT", "RISK_REVIEW_REQUIRED"]),
            _entry("SRC-PHI-V32-011", "Air molecule scattering in matter-wave interferometry", ["Source-pack seed candidate"], 2024, "2410.20910", ["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"], ["environmental_decoherence_baseline", "negative_or_exclusion_constraint"], ["RISK_SOURCE_MAY_BE_NEGATIVE", "RISK_REVIEW_REQUIRED"], review_status="REVIEWED_SOURCE_NEGATIVE_CANDIDATE"),
            _entry("SRC-PHI-V32-012", "Thermal decoherence of a levitated dielectric particle", ["Source-pack seed candidate"], 2024, "2407.01215", ["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS"], ["environmental_decoherence_baseline", "Gamma_env_rate"], ["RISK_OBSERVABLE_MISMATCH", "RISK_REVIEW_REQUIRED"]),
            _entry("SRC-PHI-V32-013", "Decoherence and the quantum-to-classical transition", ["Schlosshauer"], 2007, None, ["SLOT_1_DECOHERENCE_BASELINE_MODELS", "SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS"], ["environmental_decoherence_baseline", "log_or_scale_coordinate_formulation"], ["RISK_ANALOGY_ONLY", "RISK_NOT_DIRECTLY_PHI_GRADIENT"], url="https://link.springer.com/book/10.1007/978-3-540-35775-9"),
        ],
        notes=[
            "v3.2 seed pack: candidate sources only.",
            "Every source starts as CANDIDATE_NOT_VALIDATED and requires manual extract validation.",
        ],
    )


def build_seed_extract_pack(manifest: SeedSourceManifest) -> SeedSourceExtractPack:
    extracts = [
        _extract("EXT-PHI-V32-001", "SRC-PHI-V32-001", "SLOT_1_DECOHERENCE_BASELINE_MODELS", "Candidate extract should review collisional-decoherence rate modeling and visibility loss.", ["environmental_decoherence_baseline", "Gamma_env_rate"]),
        _extract("EXT-PHI-V32-002", "SRC-PHI-V32-002", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT", "Candidate extract should review thermal-emission visibility degradation and observable contrast loss.", ["visibility_decay_observable"]),
        _extract("EXT-PHI-V32-003", "SRC-PHI-V32-004", "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "Candidate extract should review molecular mass ranges and measured interference visibility.", ["mesoscopic_mass_length_time_range", "benchmark_dataset_or_table"], benchmark_data_text="Candidate benchmark ranges require manual extraction."),
        _extract("EXT-PHI-V32-004", "SRC-PHI-V32-005", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS", "Candidate extract should review macroscopicity measures as possible alpha-like constraint pressure.", ["alpha_like_parameter_constraint"]),
        _extract("EXT-PHI-V32-005", "SRC-PHI-V32-008", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES", "Candidate extract should review collapse-model constraints that may bound or wound PHI_GRADIENT.", [], contradicted_components=["unbounded_gradient_transition_claim"]),
        _extract("EXT-PHI-V32-006", "SRC-PHI-V32-009", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES", "Candidate extract should review hypothesis-test exclusions and benchmark stress conditions.", [], contradicted_components=["unconstrained_phi_gradient_effect"]),
        _extract("EXT-PHI-V32-007", "SRC-PHI-V32-010", "SLOT_4_GRADIENT_TRANSITION_OPERATORS", "Candidate extract should review whether gradient-related motional control maps to a concrete transition operator.", ["gradient_transition_operator"]),
        _extract("EXT-PHI-V32-008", "SRC-PHI-V32-013", "SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS", "Candidate extract should review whether scale-space language is concrete or analogy-only.", ["log_or_scale_coordinate_formulation"]),
    ]
    return SeedSourceExtractPack(
        manifest_id=manifest.manifest_id,
        extracts=extracts,
        notes=["All v3.2 extracts are review candidates and are not validated support."],
    )


def write_seed_pack(root: str | Path = ".") -> tuple[SeedSourceManifest, SeedSourceExtractPack, str, str]:
    repo_root = Path(root)
    manifest = build_seed_manifest()
    extract_pack = build_seed_extract_pack(manifest)
    manifest_path = repo_root / MANIFEST_SEED_PATH
    extract_path = repo_root / EXTRACT_SEED_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    extract_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(_json(manifest.model_dump()), encoding="utf-8")
    extract_path.write_text(_json(extract_pack.model_dump()), encoding="utf-8")
    return manifest, extract_pack, str(MANIFEST_SEED_PATH), str(EXTRACT_SEED_PATH)


def _entry(
    source_id: str,
    title: str,
    authors: list[str],
    year: int,
    arxiv_id: str | None,
    target_slots: list[str],
    expected_components: list[str],
    risk_flags: list[str],
    review_status: str = "REVIEWED_SOURCE_CANDIDATE",
    url: str | None = None,
) -> SeedSourceManifestEntry:
    return SeedSourceManifestEntry(
        source_id=source_id,
        title=title,
        authors=authors,
        year=year,
        arxiv_id=arxiv_id,
        url=url or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None),
        source_type="paper",
        target_slots=target_slots,
        expected_components=expected_components,
        review_status=review_status,
        reviewer_notes=["Seed candidate; review exact source text before validation."],
        risk_flags=risk_flags,
        evidence_status="CANDIDATE_NOT_VALIDATED",
    )


def _extract(
    extract_id: str,
    source_id: str,
    slot_id: str,
    text: str,
    supported_components: list[str],
    contradicted_components: list[str] | None = None,
    benchmark_data_text: str | None = None,
) -> SeedSourceExtract:
    return SeedSourceExtract(
        extract_id=extract_id,
        source_id=source_id,
        slot_id=slot_id,
        extract_text_or_paraphrase=text,
        benchmark_data_text=benchmark_data_text,
        supported_components=supported_components,
        contradicted_components=contradicted_components or [],
        limitations=["Seed paraphrase only; requires manual source review."],
        manual_review_required=True,
        extraction_notes=["Initial v3.2 seed extract. Not validated support."],
        initial_validation_status="EXTRACT_CANDIDATE_REQUIRES_REVIEW",
    )


def _json(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
