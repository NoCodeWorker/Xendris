import json

from xendris.benchmarking.frontier_gap import (
    FrontierGapSystemResult,
    compute_frontier_gap,
    write_frontier_gap_summary_json,
)


def _system(
    role: str,
    score: float,
    cost: float,
    latency: float,
    allowed: int = 10,
    exclusion_rate: float = 0.0,
    human_review_rate: float = 0.0,
) -> FrontierGapSystemResult:
    return FrontierGapSystemResult(
        system_name=role,
        model_name=f"{role}-model",
        provider="fake-provider",
        role=role,  # type: ignore[arg-type]
        average_score=score,
        total_cost_usd=cost,
        average_latency_ms=latency,
        scoring_allowed_count=allowed,
        exclusion_rate=exclusion_rate,
        human_review_rate=human_review_rate,
        cost_per_valid_answer=cost / allowed if allowed else None,
    )


def test_1_calculates_gap_closed_correctly():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.865, 1.2, 101.0),
        _system("frontier_base", 0.89, 10.0, 500.0),
    )

    assert comparison.gap_closed_ratio == round((0.865 - 0.10) / (0.89 - 0.10), 8)
    assert comparison.gap_closed_percent == round(((0.865 - 0.10) / (0.89 - 0.10)) * 100, 8)


def test_2_gap_closed_is_100_percent_when_cheap_xendris_reaches_frontier():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.20, 1.0, 100.0),
        _system("cheap_xendris", 0.80, 1.3, 110.0),
        _system("frontier_base", 0.80, 9.0, 450.0),
    )

    assert comparison.gap_closed_ratio == 1.0
    assert comparison.gap_closed_percent == 100.0


def test_3_gap_above_100_percent_is_allowed_with_warning():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.20, 1.0, 100.0),
        _system("cheap_xendris", 0.90, 1.4, 110.0),
        _system("frontier_base", 0.80, 9.0, 450.0),
    )

    assert comparison.gap_closed_percent == round((0.70 / 0.60) * 100, 8)
    assert "Frontier exceeded on this benchmark only" in comparison.interpretation
    assert "universal superiority" in comparison.interpretation


def test_4_gap_is_not_applicable_when_frontier_does_not_exceed_cheap_base():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.80, 1.0, 100.0),
        _system("cheap_xendris", 0.85, 1.2, 110.0),
        _system("frontier_base", 0.75, 8.0, 450.0),
    )

    assert comparison.gap_closed_ratio is None
    assert comparison.gap_closed_percent is None
    assert "Gap not applicable" in comparison.interpretation


def test_5_calculates_cost_multipliers():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 2.0, 100.0),
        _system("cheap_xendris", 0.60, 3.0, 120.0),
        _system("frontier_base", 0.80, 20.0, 500.0),
    )

    assert comparison.cost_multiplier_xendris_vs_cheap == 1.5
    assert comparison.cost_multiplier_frontier_vs_cheap == 10.0


def test_6_calculates_cost_per_gap_point():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.60, 1.5, 120.0),
        _system("frontier_base", 0.80, 8.0, 500.0),
    )

    assert comparison.cost_per_gap_point_xendris == 1.0
    assert comparison.cost_per_gap_point_frontier == 10.0


def test_7_calculates_latency_overhead():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.60, 1.5, 125.0),
        _system("frontier_base", 0.80, 8.0, 540.0),
    )

    assert comparison.latency_overhead_xendris == 25.0
    assert comparison.latency_overhead_frontier == 440.0


def test_8_zero_cost_or_zero_gap_does_not_divide_by_zero():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.50, 0.0, 100.0),
        _system("cheap_xendris", 0.50, 0.0, 100.0),
        _system("frontier_base", 0.50, 10.0, 300.0),
    )

    assert comparison.cost_multiplier_xendris_vs_cheap is None
    assert comparison.cost_multiplier_frontier_vs_cheap is None
    assert comparison.cost_per_gap_point_xendris is None
    assert comparison.cost_per_gap_point_frontier is None
    assert comparison.gap_closed_percent is None


def test_9_interpretation_is_prudent():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.70, 1.5, 120.0),
        _system("frontier_base", 0.90, 8.0, 500.0),
    )

    assert "Benchmark-local" in comparison.interpretation
    assert "does not imply universal superiority" in comparison.interpretation


def test_10_no_real_apis_are_used():
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.70, 1.5, 120.0),
        _system("frontier_base", 0.90, 8.0, 500.0),
    )

    assert comparison.cheap_base.provider == "fake-provider"
    assert comparison.frontier_base.provider == "fake-provider"


def test_11_exports_summary_json(tmp_path):
    comparison = compute_frontier_gap(
        _system("cheap_base", 0.10, 1.0, 100.0),
        _system("cheap_xendris", 0.70, 1.5, 120.0),
        _system("frontier_base", 0.90, 8.0, 500.0),
    )
    output_path = tmp_path / "frontier-gap.json"

    write_frontier_gap_summary_json(comparison, output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["gap_closed_percent"] == comparison.gap_closed_percent
    assert payload["cheap_base"]["role"] == "cheap_base"


def test_12_documentation_warning_text_exists():
    doc_path = "docs/benchmarks/CHEAP_TO_FRONTIER_GAP_BENCHMARK_V0_1.md"
    with open(doc_path, "r", encoding="utf-8") as handle:
        text = handle.read()

    assert "No Universal Superiority Warning" in text
    assert "does not imply universal superiority" in text
