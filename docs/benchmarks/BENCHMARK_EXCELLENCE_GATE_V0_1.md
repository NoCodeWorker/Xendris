# Benchmark Excellence Gate v0.1

## Purpose

Benchmark Excellence Gate v0.1 is a conservative interpretation gate for
Xendris benchmark artifacts.

It reviews summary JSON objects and optional Markdown reports before they are
used as evidence in comparisons, roadmap decisions, or public claims.

The gate does not:

- improve outputs;
- change scores;
- call providers;
- modify datasets;
- validate universal superiority;
- inflate benchmarks.

It only evaluates whether the benchmark artifact is structurally prepared for
careful interpretation.

## What It Checks

The gate checks whether an artifact contains enough structural evidence to be
interpreted responsibly:

- dataset hash;
- execution mode;
- dataset name or version;
- model name or comparable system names;
- total sample count;
- comparable score pair;
- average delta;
- no-universal-superiority warning;
- limitations section;
- provider disclosure for real-provider runs;
- temperature;
- max token limit;
- Xendris version;
- Python version;
- latency metrics;
- cost metrics;
- dataset hash algorithm;
- run date;
- external data disclosure;
- pricing assumptions.

## Decisions

| Decision | Meaning |
|---|---|
| `READY_FOR_INTERPRETATION` | No blockers or warnings were found. |
| `WARNINGS_PRESENT` | No blockers were found, but the artifact has non-blocking weaknesses. |
| `BLOCKED_FOR_INTERPRETATION` | Required evidence is missing, invalid, or contradicted by the report. |

## Blockers

The following findings block interpretation:

- `missing_dataset_hash`
- `missing_execution_mode`
- `missing_dataset_version_or_name`
- `missing_model_name_or_system_names`
- `missing_total_sample_count`
- `invalid_total_sample_count`
- `missing_comparable_score_pair`
- `missing_average_delta`
- `missing_no_universal_superiority_warning`
- `missing_limitations_section`
- `dry_run_report_claims_real_provider_performance`
- `real_provider_run_missing_provider_name`

Cost or latency gaps are warnings by default, but become blockers if the report
makes cost or latency claims without the corresponding metrics.

## Warnings

The following findings are warnings unless escalated by a related report claim:

- `missing_temperature`
- `missing_max_tokens`
- `missing_xendris_version`
- `missing_python_version`
- `missing_latency_metrics`
- `missing_cost_metrics`
- `missing_dataset_hash_algorithm`
- `missing_run_date`
- `missing_provider_disclosure`
- `missing_external_data_disclosure`
- `missing_pricing_assumptions`

## Notes

The gate may add notes to clarify interpretation:

- `dry_run_result`
- `benchmark_local_only`
- `closed_dataset`
- `synthetic_dataset`
- `frontier_gap_not_applicable`

Notes do not block interpretation.

## Examples

### Ready Artifact

An artifact is ready when it includes complete metadata, comparable scores,
average delta, cost and latency metrics, a clear no-universal-superiority
warning, and limitations.

```python
from xendris.benchmarking import assess_benchmark_excellence

assessment = assess_benchmark_excellence(summary, report_text=report)
assert assessment.decision.value == "READY_FOR_INTERPRETATION"
```

### Blocked Artifact

An artifact is blocked when it lacks a dataset hash:

```python
assessment = assess_benchmark_excellence(summary_without_hash, report_text=report)
assert assessment.has_blockers
```

### CLI Usage

```powershell
.\.venv\Scripts\python.exe scripts\validate_benchmark_excellence.py `
  runs\deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json `
  --report docs\benchmarks\RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md `
  --output runs\deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_excellence.json
```

## Correct Interpretation

Passing the gate means only that the artifact is structurally ready for careful
benchmark interpretation.

It does not mean:

- Xendris is universally superior;
- the model is production-ready;
- the dataset generalizes;
- factual claims are validated;
- benchmark scores are scientific proof.

## Limitations

- The gate checks structure and reporting discipline, not truth.
- It cannot detect all benchmark leakage or dataset bias.
- It cannot prove that the measured improvement generalizes.
- It cannot replace external review.

## No Universal Superiority Warning

Benchmark Excellence Gate v0.1 explicitly rejects using benchmark artifacts as
universal superiority evidence. It exists to make benchmark usage more
reproducible, calibrated, and resistant to overclaiming.
