from __future__ import annotations

from phyng.audit_remediation.metric_remediation import build_metric_remediation_records, predictive_gain_metric_labels_remain_distinct


def test_predictive_gain_metric_labels_remain_distinct() -> None:
    records = build_metric_remediation_records({})

    assert predictive_gain_metric_labels_remain_distinct(records)


def test_benchmark_score_not_labeled_predictive_gain() -> None:
    records = build_metric_remediation_records({})
    benchmark = next(record for record in records if record.metric_name == "BenchmarkComparisonScore")

    assert benchmark.forbidden_label == "PredictiveGain"
    assert benchmark.required_label == "Benchmark comparison only"
