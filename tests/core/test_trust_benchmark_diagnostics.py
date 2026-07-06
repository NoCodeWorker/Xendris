from xendris.core.trust import (
    BenchmarkExclusionReason,
    BenchmarkGateDecision,
    BenchmarkGateResult,
    BenchmarkSuiteReadiness,
    diagnose_benchmark_suite,
)


def _gate_result(
    *,
    decision: BenchmarkGateDecision = BenchmarkGateDecision.INCLUDE,
    reason: BenchmarkExclusionReason = BenchmarkExclusionReason.NONE,
    include_in_scoring: bool = True,
    requires_limitation_note: bool = False,
    quality_score: float = 0.95,
) -> BenchmarkGateResult:
    return BenchmarkGateResult(
        decision=decision,
        reason=reason,
        include_in_scoring=include_in_scoring,
        requires_limitation_note=requires_limitation_note,
        quality_score=quality_score,
        notes="test result",
    )


def test_diagnostics_mark_all_clean_high_quality_outputs_as_excellent():
    diagnostics = diagnose_benchmark_suite(
        (
            _gate_result(quality_score=0.95),
            _gate_result(quality_score=0.90),
        )
    )

    assert diagnostics.total_outputs == 2
    assert diagnostics.included_outputs == 2
    assert diagnostics.excluded_outputs == 0
    assert diagnostics.inclusion_rate == 1.0
    assert diagnostics.average_quality_score == 0.925
    assert diagnostics.readiness == BenchmarkSuiteReadiness.EXCELLENT
    assert "reproducibility" in diagnostics.improvement_actions[-1]


def test_diagnostics_mark_limited_outputs_as_usable_with_limitations():
    diagnostics = diagnose_benchmark_suite(
        (
            _gate_result(),
            _gate_result(
                decision=BenchmarkGateDecision.INCLUDE_WITH_LIMITATIONS,
                reason=BenchmarkExclusionReason.LIMITED_READINESS,
                requires_limitation_note=True,
                quality_score=0.72,
            ),
        )
    )

    assert diagnostics.readiness == BenchmarkSuiteReadiness.USABLE_WITH_LIMITATIONS
    assert diagnostics.limited_outputs == 1
    assert diagnostics.included_outputs == 2
    assert any("limitation notes" in action for action in diagnostics.improvement_actions)


def test_diagnostics_mark_degraded_runtime_as_needing_remediation():
    diagnostics = diagnose_benchmark_suite(
        (
            _gate_result(),
            _gate_result(
                decision=BenchmarkGateDecision.EXCLUDE,
                reason=BenchmarkExclusionReason.TIMEOUT,
                include_in_scoring=False,
                requires_limitation_note=True,
                quality_score=0.0,
            ),
        )
    )

    assert diagnostics.readiness == BenchmarkSuiteReadiness.NEEDS_REMEDIATION
    assert diagnostics.excluded_outputs == 1
    assert diagnostics.inclusion_rate == 0.5
    assert any("fallback outputs" in action for action in diagnostics.improvement_actions)


def test_diagnostics_block_empty_or_fully_excluded_runs():
    empty = diagnose_benchmark_suite(())
    fully_excluded = diagnose_benchmark_suite(
        (
            _gate_result(
                decision=BenchmarkGateDecision.EXCLUDE,
                reason=BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED,
                include_in_scoring=False,
                requires_limitation_note=True,
                quality_score=0.2,
            ),
        )
    )

    assert empty.readiness == BenchmarkSuiteReadiness.BLOCKED
    assert empty.inclusion_rate == 0.0
    assert fully_excluded.readiness == BenchmarkSuiteReadiness.BLOCKED
    assert fully_excluded.excluded_outputs == 1


def test_diagnostics_payload_is_json_safe():
    diagnostics = diagnose_benchmark_suite((_gate_result(),))
    payload = diagnostics.to_dict()

    assert payload["readiness"] == BenchmarkSuiteReadiness.EXCELLENT.value
    assert payload["total_outputs"] == 1
    assert isinstance(payload["improvement_actions"], list)


def test_public_imports_are_available_from_trust_namespace():
    diagnostics = diagnose_benchmark_suite((_gate_result(),))

    assert diagnostics.readiness == BenchmarkSuiteReadiness.EXCELLENT
