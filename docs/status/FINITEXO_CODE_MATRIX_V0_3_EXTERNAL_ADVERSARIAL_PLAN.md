# Finitexo Code Matrix v0.3 - External Adversarial Plan

## Purpose

Finitexo Code Matrix v0.3 exists to test whether prior programming benchmark
signals survive a more adversarial design.

The main risk addressed by v0.3 is self-deception: a benchmark can accidentally
favor the system that created it through weak baselines, non-blind scoring,
task reuse, or interpretation that protects the preferred conclusion.

## v0.2 vs v0.3

v0.2 hardened the scoring contract and made verified success stricter.

v0.3 adds external-adversarial infrastructure:

- semi-external task origin;
- frozen dataset manifest;
- task and scoring hashes;
- blind scoring;
- strong non-system baseline requirement;
- explicit falsification policy;
- H0 preserved by default;
- runner defaults that avoid provider calls unless `--execute` is explicit.

## Dataset Origin

No verified third-party external dataset is currently bundled.

The current seed dataset is marked:

```txt
SEMI_EXTERNAL_SYNTHETIC
```

This is intentional and conservative. The infrastructure is ready for real
external data later, but the current dataset must not be described as fully
external.

## Null Hypothesis

```txt
H0: Xendris does not show a clear advantage over a strong non-Xendris baseline.
```

H0 remains live by default.

## Strong Baseline

v0.3 requires:

- `weak_base_agent`;
- `strong_base_agent`;
- `test_disciplined_base_agent`;
- `strong_non_xendris_agent`;
- `xendris_agent`;
- `xendris_calibrated_agent`.

A weak baseline is diagnostic only and cannot support advantage claims.

If `strong_non_xendris_agent` matches or outperforms system variants, that
result must be preserved and reported.

## Blind Scoring

The blind scorer must not receive:

- variant;
- provider;
- model;
- agent name;
- system labels;
- baseline labels.

If identity leaks into blind scoring, interpretation is blocked.

## Decisions

Allowed outcomes include:

- `XENDRIS_ADVANTAGE_OBSERVED_INTERNAL_ONLY`;
- `NO_CLEAR_XENDRIS_ADVANTAGE`;
- `BASELINE_MATCHED_XENDRIS`;
- `BASELINE_OUTPERFORMED_XENDRIS`;
- `BENCHMARK_INCONCLUSIVE`;
- `BLOCKED_FOR_INTERPRETATION`.

The benchmark is valid even when it reports no clear advantage.

## Forbidden Claims

v0.3 does not authorize:

- universal superiority;
- general coding superiority;
- production readiness;
- provider superiority;
- model superiority;
- positive claims from weak baselines;
- positive claims from non-blind scoring;
- positive claims from blocked evidence.

## Commands

Plan-only:

```powershell
.\.venv\Scripts\python.exe -m benchmarks.finitexo_code_matrix_v0_3.runners.run_external_matrix_v0_3 --plan-only --output-dir runs/finitexo_code_matrix_v0_3_plan
```

Dry-run:

```powershell
.\.venv\Scripts\python.exe -m benchmarks.finitexo_code_matrix_v0_3.runners.run_external_matrix_v0_3 --dry-run --output-dir runs/finitexo_code_matrix_v0_3_dry_run
```

Blind scoring dry-run:

```powershell
.\.venv\Scripts\python.exe -m benchmarks.finitexo_code_matrix_v0_3.runners.run_blind_scoring_v0_3
```

Baseline comparison dry-run:

```powershell
.\.venv\Scripts\python.exe -m benchmarks.finitexo_code_matrix_v0_3.runners.run_baseline_comparison_v0_3
```

## Pending For Real Execution

Before real provider execution:

- replace or supplement seed tasks with verified external tasks;
- review budget and model matrix;
- ensure blind scoring is active;
- ensure strong baseline variants are available;
- ensure no provider execution occurs without `--execute`;
- run the evidence/adversarial checks before interpreting results.

## Current Implementation Decision

```txt
IMPLEMENTED_SEMI_EXTERNAL_ADVERSARIAL_INFRASTRUCTURE
```

No provider execution has been performed by this plan.

