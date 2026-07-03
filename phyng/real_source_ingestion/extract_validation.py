"""Validation for real source extracts."""

from __future__ import annotations

from phyng.real_source_ingestion.schemas import RealSourceExtract, RealSourceExtractValidationResult


def validate_real_source_extract(extract: RealSourceExtract) -> RealSourceExtractValidationResult:
    status = _status_for_extract(extract)
    counts = (
        status.startswith("EXTRACT_VALID_")
        and not extract.is_fixture
        and not extract.is_test_double
    )
    reasons = []
    if extract.is_fixture:
        reasons.append("Fixture extract cannot count as real support.")
    if extract.is_test_double:
        reasons.append("Test double validates format only and cannot count as real support.")
    if status == "EXTRACT_REJECTED_ANALOGY_ONLY":
        reasons.append("Extract contains analogy language without concrete component support.")
    if status == "EXTRACT_REQUIRES_MANUAL_REVIEW":
        reasons.append("Extract lacks enough structured evidence for automatic classification.")
    return RealSourceExtractValidationResult(
        extract_id=extract.extract_id,
        source_id=extract.source_id,
        status=status,
        counts_as_real_support=counts,
        slot_id=extract.slot_id,
        supported_components=list(extract.supported_components),
        contradicted_components=list(extract.contradicted_components),
        reasons=reasons,
    )


def _status_for_extract(extract: RealSourceExtract) -> str:
    if extract.contradicted_components:
        return "EXTRACT_VALID_CONTRADICTS_CANDIDATE"
    if extract.benchmark_data_text:
        required = bool(extract.observable_text and extract.parameter_constraint_text and extract.supported_components)
        return "EXTRACT_VALID_PROVIDES_BENCHMARK_DATA" if required else "EXTRACT_REJECTED_NOT_COMPARABLE"
    if extract.parameter_constraint_text:
        return "EXTRACT_VALID_CONSTRAINS_PARAMETER"
    if "gradient_transition_operator" in extract.supported_components and extract.equation_text:
        return "EXTRACT_VALID_SUPPORTS_COMPONENT"
    if "environmental_decoherence_baseline" in extract.supported_components and extract.equation_text:
        return "EXTRACT_VALID_SUPPORTS_BASELINE"
    if extract.observable_text and "visibility_decay_observable" in extract.supported_components:
        return "EXTRACT_VALID_SUPPORTS_OBSERVABLE"
    if extract.extracted_text_or_paraphrase and not extract.supported_components:
        return "EXTRACT_REJECTED_ANALOGY_ONLY"
    return "EXTRACT_REQUIRES_MANUAL_REVIEW"


def real_source_observable_extract_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-DOUBLE-OBS",
        source_id="RS-DOUBLE-OBS",
        slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
        extracted_text_or_paraphrase="Defines visibility decay observable in test-double format.",
        observable_text="visibility V(t)",
        supported_components=["visibility_decay_observable"],
        is_test_double=True,
    )


def real_source_component_extract_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-DOUBLE-COMP",
        source_id="RS-DOUBLE-COMP",
        slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
        extracted_text_or_paraphrase="Provides gradient transition operator in test-double format.",
        equation_text="rate += |d phi / du|",
        supported_components=["gradient_transition_operator"],
        is_test_double=True,
    )


def real_source_benchmark_extract_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-DOUBLE-BENCH",
        source_id="RS-DOUBLE-BENCH",
        slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
        extracted_text_or_paraphrase="Provides comparable benchmark range in test-double format.",
        observable_text="visibility decay",
        parameter_constraint_text="m_kg, L_m, t_s ranges",
        benchmark_data_text="table: m_kg/L_m/t_s/V",
        supported_components=["benchmark_dataset_or_table"],
        is_test_double=True,
    )


def real_source_analogy_only_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-DOUBLE-ANALOGY",
        source_id="RS-DOUBLE-ANALOGY",
        slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
        extracted_text_or_paraphrase="Mentions gradients and boundaries with no observable, equation or component.",
        is_test_double=True,
    )


def real_source_negative_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-DOUBLE-NEG",
        source_id="RS-DOUBLE-NEG",
        slot_id="SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES",
        extracted_text_or_paraphrase="Contradicts candidate mechanism in test-double format.",
        contradicted_components=["gradient_transition_operator"],
        is_test_double=True,
    )


def fixture_source_from_v2_8_extract_double() -> RealSourceExtract:
    return RealSourceExtract(
        extract_id="EXT-FIX-V2-8",
        source_id="SRC-FIX-V2-8",
        slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
        extracted_text_or_paraphrase="v2.8 fixture component support must not count as real support.",
        equation_text="fixture equation",
        supported_components=["gradient_transition_operator"],
        is_fixture=True,
    )


def default_extract_doubles() -> list[RealSourceExtract]:
    return [
        real_source_observable_extract_double(),
        real_source_component_extract_double(),
        real_source_benchmark_extract_double(),
        real_source_analogy_only_double(),
        fixture_source_from_v2_8_extract_double(),
    ]
