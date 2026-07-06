# Trust Traps v0.1 Run v2 - Xendris Trust Reasoning Refinement v0.3.5

Date: 2026-07-04

## Status

```txt
DRY_RUN_COMPLETED
```

This run used deterministic mock providers. It did not call real DeepSeek APIs
and must not be treated as a real provider performance measurement.

## Purpose

Validate that the v0.3.5 trust-reasoning refinement improves weak Trust Traps
v0.1 categories without altering the dataset, changing the scoring rubric,
degrading `normal_control`, or increasing false-positive contamination.

## Historical Rejected Artifacts

These artifacts are historical dry-run outputs and are not admitted as current
benchmark evidence by `runs/benchmark_evidence_registry.json` because the
summary metadata is incomplete.

```txt
runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_v2.jsonl
runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_v2_summary.json
```

## Results

| Metric | Value |
|---|---:|
| Total samples | 100 |
| DeepSeek average score | 0.100 |
| Xendris average score | 0.985 |
| Average delta | +0.885 |
| Xendris wins | 90 |
| DeepSeek wins | 0 |
| Ties | 10 |
| Xendris exclusion rate | 90.0% |
| Xendris human review rate | 15.0% |

## Category Breakdown

| Category | DeepSeek score | Xendris score | Delta | Xendris exclusion rate |
|---|---:|---:|---:|---:|
| `false_truth_proxy` | 0.000 | 1.000 | +1.000 | 100.0% |
| `universal_superiority` | 0.000 | 1.000 | +1.000 | 100.0% |
| `user_provided_without_evidence` | 0.000 | 0.900 | +0.900 | 100.0% |
| `evidence_conflict` | 0.000 | 1.000 | +1.000 | 100.0% |
| `code_and_production_claims` | 0.000 | 1.000 | +1.000 | 100.0% |
| `fallback_runtime_timeout` | 0.000 | 1.000 | +1.000 | 100.0% |
| `normal_control` | 1.000 | 1.000 | 0.000 | 0.0% |

## Comparison Against Previous Reported Baseline

| Metric | Previous | v2 dry-run |
|---|---:|---:|
| Global Xendris score | 0.865 | 0.985 |
| `evidence_conflict` | 0.500 | 1.000 |
| `user_provided_without_evidence` | 0.800 | 0.900 |
| `code_and_production_claims` | 0.800 | 1.000 |
| `normal_control` | 1.000 | 1.000 |

## Interpretation

The v0.3.5 deterministic refinement improves Trust Traps v0.1 dry-run scores by:

- preserving operational decisions expected by the dataset;
- separating user-provided origin from verified support;
- distinguishing real evidence conflicts from deterministic exclusions;
- mapping code and production overclaims to unsupported scoring criteria;
- keeping `normal_control` unrestricted.

## Limits

- This is a dry-run with mock providers.
- It validates deterministic classification and gate behavior, not real model
  quality.
- It does not prove universal superiority over DeepSeek or any frontier model.
- It does not generalize to datasets outside Trust Traps v0.1.
- It does not modify historical results.

## No Benchmark Inflation Statement

The dataset and scoring function were not changed for this run. The improvement
comes from reasoning, classification, and provider adapter decision mapping.

## Next Step

Run the same v0.3.5 configuration with a real provider call when API access,
cost controls, and run logging are ready.
