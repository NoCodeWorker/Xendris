# Finitexo Code Matrix v0.2

Anti-ad-hoc validation benchmark for small agentic programming tasks.

This benchmark exists to test whether the signal observed in v0.1 survives
stronger reproducibility controls. It is not designed to prove superiority.

## Status

- Benchmark version: `v0.2`
- Dataset size: 20 tasks
- Dataset state: frozen by manifest hash
- Default interpretation for small runs: budget validation only

## Design

The benchmark separates:

1. task definitions;
2. generation/execution;
3. scoring;
4. anti-ad-hoc integrity checks;
5. interpretation policy.

The benchmark must not be cited as evidence of universal programming quality,
production readiness, or provider superiority.

## Minimal Dry Run

```powershell
.\.venv\Scripts\python.exe benchmarks\finitexo_code_matrix_v0_2\runners\run_matrix_v0_2.py --dry-run --samples 5
```

## Ablation Dry Run

```powershell
.\.venv\Scripts\python.exe benchmarks\finitexo_code_matrix_v0_2\runners\run_ablation_v0_2.py --dry-run --samples 5
```

Live provider execution is intentionally not implemented in this first
infrastructure pass. Provider adapters must be wired explicitly in a later
step, after dry-run integrity checks are stable.
