from phyng.source_pressure.phi_gradient_audit import (
    default_source_fixtures,
    run_phi_gradient_source_pressure_audit,
    source_gradient_component_support_fixture,
    source_negative_conflict_fixture,
    source_observable_support_fixture,
)


def test_negative_source_blocks_unaddressed_upgrade():
    result = run_phi_gradient_source_pressure_audit(default_source_fixtures(include_negative=True))

    assert result.status == "PHI_GRADIENT_CONTRADICTED_BY_SOURCE"
    assert result.negative_sources


def test_alpha_constraint_missing_remains_blocked():
    result = run_phi_gradient_source_pressure_audit([
        source_observable_support_fixture(),
        source_gradient_component_support_fixture(),
    ])

    assert "alpha_like_parameter_constraint" in result.missing_requirements
    assert "search alpha-like parameter constraints" in result.next_actions


def test_source_backed_limited_requires_minimum_slots():
    result = run_phi_gradient_source_pressure_audit(default_source_fixtures())

    assert result.status == "PHI_GRADIENT_SOURCE_BACKED_LIMITED"
    assert result.canonical_status.evidence_level.value == "SOURCE_BACKED_LIMITED"
