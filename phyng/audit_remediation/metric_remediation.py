"""Metric label remediation."""

from __future__ import annotations

from phyng.audit_remediation.schemas import MetricIntegrityRemediationRecord


CRITICAL_METRIC_RULES = [
    ("BenchmarkComparisonScore", "Benchmark comparison only", "PredictiveGain"),
    ("SyntheticGain", "Synthetic-only delta", "PredictiveGain"),
    ("SourcePressureScore", "Source pressure review score", "validation"),
    ("ObservableAlignmentScore", "Observable alignment score", "observed truth"),
]


def build_metric_remediation_records(metric_payload: dict) -> list[MetricIntegrityRemediationRecord]:
    records = [
        MetricIntegrityRemediationRecord(
            metric_name=name,
            artifact_path="global_metric_contract",
            misuse_risk=f"{name} must not be relabelled as {forbidden}.",
            remediation_action="DECLARE_LABEL_BOUNDARY",
            required_label=required,
            forbidden_label=forbidden,
            final_status="LABEL_BOUNDARY_RESTATED",
        )
        for name, required, forbidden in CRITICAL_METRIC_RULES
    ]
    for bucket in ("predictive_gain_issues", "ytrue_issues", "source_support_issues", "negative_control_issues"):
        for issue in metric_payload.get(bucket, []):
            records.append(
                MetricIntegrityRemediationRecord(
                    metric_name=issue.get("category", "metric_integrity_issue"),
                    artifact_path=issue.get("path", ""),
                    misuse_risk=issue.get("message", ""),
                    remediation_action="KEEP_BLOCKED_UNTIL_SOURCE_AND_YTRUE_GATE",
                    required_label="Audit debt or blocked metric input",
                    forbidden_label="PredictiveGain",
                    final_status="ACCEPTED_RESIDUAL" if issue.get("severity") != "BLOCKER" else "BLOCKS_NEXT_GATE",
                )
            )
    return records


def predictive_gain_metric_labels_remain_distinct(records: list[MetricIntegrityRemediationRecord]) -> bool:
    forbidden_pairs = {(record.metric_name, record.forbidden_label) for record in records}
    return ("BenchmarkComparisonScore", "PredictiveGain") in forbidden_pairs and ("SyntheticGain", "PredictiveGain") in forbidden_pairs
