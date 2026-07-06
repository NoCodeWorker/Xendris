from xendris.core.calibration import (
    CalibrationAudit,
    ExecutionMode,
    InterventionLevel,
    ProgrammingCategory,
    ProgrammingInterventionPolicy,
)


def test_api_contracts_benchmark_mode_uses_minimal_intervention():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide(ProgrammingCategory.API_CONTRACTS, ExecutionMode.BENCHMARK_EXECUTION)

    assert decision.intervention_level == InterventionLevel.MINIMAL
    assert decision.prefer_minimal_patch is True


def test_api_contracts_preserve_signature():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide(ProgrammingCategory.API_CONTRACTS, ExecutionMode.CODE_SANDBOX)

    assert decision.preserve_signature is True


def test_api_contracts_disallow_extra_imports():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide("api_contracts", "code_sandbox")

    assert decision.allow_extra_imports is False
    assert decision.allow_runtime_type_checks is False


def test_unit_tests_code_sandbox_disallows_pytest_imports():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide(ProgrammingCategory.UNIT_TESTS, ExecutionMode.CODE_SANDBOX)

    assert decision.allow_test_framework_imports is False
    assert "plain assert" in " ".join([decision.rationale, *decision.warnings])


def test_edge_cases_allow_moderate_intervention_without_extra_imports_by_default():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide(ProgrammingCategory.EDGE_CASES, ExecutionMode.CODE_SANDBOX)

    assert decision.intervention_level == InterventionLevel.MODERATE
    assert decision.allow_extra_imports is False
    assert decision.allow_runtime_type_checks is True


def test_production_mode_allows_stronger_checks_than_benchmark_mode():
    policy = ProgrammingInterventionPolicy()

    benchmark = policy.decide(ProgrammingCategory.API_CONTRACTS, ExecutionMode.BENCHMARK_EXECUTION)
    production = policy.decide(ProgrammingCategory.API_CONTRACTS, ExecutionMode.PRODUCTION)

    assert benchmark.intervention_level == InterventionLevel.MINIMAL
    assert production.intervention_level == InterventionLevel.STRONG
    assert production.preserve_signature is True


def test_security_basics_requires_scan_but_warns_about_false_positives():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide(ProgrammingCategory.SECURITY_BASICS, ExecutionMode.CODE_SANDBOX)

    assert decision.require_security_scan is True
    assert any("false-positive" in warning for warning in decision.warnings)


def test_unknown_category_defaults_conservatively_without_overclaiming():
    policy = ProgrammingInterventionPolicy()

    decision = policy.decide("unknown_category", ExecutionMode.BENCHMARK_EXECUTION)

    assert decision.intervention_level == InterventionLevel.MINIMAL
    assert decision.allow_extra_imports is False
    assert decision.prefer_minimal_patch is True
    assert any("Unknown category" in warning for warning in decision.warnings)


def test_audit_object_records_rationale():
    policy = ProgrammingInterventionPolicy()

    audit = policy.audit(ProgrammingCategory.API_CONTRACTS, ExecutionMode.CODE_SANDBOX)

    assert isinstance(audit, CalibrationAudit)
    assert audit.rationale == audit.decision.rationale
    assert "No intervention without domain-calibrated benefit." in audit.notes


def test_policy_is_deterministic():
    policy = ProgrammingInterventionPolicy()

    first = policy.decide(ProgrammingCategory.EDGE_CASES, ExecutionMode.CODE_SANDBOX)
    second = policy.decide(ProgrammingCategory.EDGE_CASES, ExecutionMode.CODE_SANDBOX)

    assert first == second
