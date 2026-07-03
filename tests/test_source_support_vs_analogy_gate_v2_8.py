from phyng.source_pressure.phi_gradient_audit import (
    source_analogy_only_fixture,
    source_gradient_component_support_fixture,
    source_observable_support_fixture,
)
from phyng.source_pressure.source_gate import assess_source_support


def test_analogy_only_source_does_not_count_as_support():
    assessment = assess_source_support(source_analogy_only_fixture())

    assert assessment.status == "SOURCE_ANALOGY_ONLY"
    assert not assessment.counts_as_support


def test_source_support_requires_component_or_observable():
    observable = assess_source_support(source_observable_support_fixture())
    component = assess_source_support(source_gradient_component_support_fixture())

    assert observable.counts_as_support
    assert component.counts_as_support
    assert component.status == "SOURCE_SUPPORTS_COMPONENT"
