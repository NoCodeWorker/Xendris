from phyng.real_source_ingestion.extract_validation import (
    real_source_analogy_only_double,
    real_source_component_extract_double,
    validate_real_source_extract,
)


def test_valid_extract_requires_supported_component():
    validation = validate_real_source_extract(real_source_component_extract_double())

    assert validation.status == "EXTRACT_VALID_SUPPORTS_COMPONENT"
    assert not validation.counts_as_real_support


def test_analogy_extract_is_rejected():
    validation = validate_real_source_extract(real_source_analogy_only_double())

    assert validation.status == "EXTRACT_REJECTED_ANALOGY_ONLY"
    assert not validation.counts_as_real_support
