# Finitexo Code Matrix v0.9.1 — Runtime Evidence Gate

## Purpose

This is an offline evidence integrity and statistical robustness gate over the v0.9.0 live_20260708_02 runtime paired lift run.

No providers are called.
No scores are changed.
No superiority claim authorized.
The goal is integrity verification + robustness analysis + claim authorization.

## Source Run

- **Run ID:** finitexo_v0_9_0_runtime_paired_lift_n30_live_20260708_02
- **Directory:** `runs/finitexo_code_matrix_v0_9_0_runtime_paired_lift_n30_live_20260708_02/`
- **Provider mode:** real
- **Final decision:** RUNTIME_LIFT_COMPLETED_DIAGNOSTIC_ONLY
- **Total expected:** 240
- **Total completed:** 240
- **Total failed:** 0
- **Runtime traces:** 120 / 120
- **Calibration traces:** 60 / 60
- **Errors:** 0
- **Evidence integrity:** ready
- **Total cost:** $0.0894

## Gate Operations

### Evidence Integrity

The gate verifies:
- Source run directory exists and all required artifacts are present
- Source run decision, provider mode, hashes, counts, and variant distributions match expectations
- All 8 variants have exactly 30 scores each
- All scores are in [0, 1]
- Task IDs are identical across variants
- All 5 expected families are present

### Statistical Robustness

The gate computes pairwise paired statistics (mean lift, median lift, wins/losses/ties, bootstrap CI, sign test, outlier sensitivity) for all 12 comparisons across DeepSeek and OpenAI.

Signal classification is diagnostic-only:
- STRONG_DIAGNOSTIC_SIGNAL
- MODERATE_DIAGNOSTIC_SIGNAL
- WEAK_OR_INCONCLUSIVE_SIGNAL
- NEGATIVE_SIGNAL

These classifications do not authorize universal or statistical superiority claims.

### Claim Authorization

The gate explicitly lists:
- **Authorized claims** — facts the source run supports
- **Conditional claims** — per-comparison diagnostic signals
- **Blocked claims** — claims that cannot be made from this run

## Output Directory

Results are written to:

```
runs/finitexo_code_matrix_v0_9_1_runtime_evidence_gate_live_20260708_02/
```

Artifacts:
- `summary.json` — gate summary with final decision
- `integrity.json` — full integrity check results
- `statistics.json` — all paired comparison statistics
- `cost_robustness.json` — cost metrics
- `claim_authorization.json` — authorized/blocked claims
- `report.md` — human-readable report

## Constraints

- No providers are called
- No scores are changed
- No source run artifacts are modified
- No superiority claim is authorized
- No production readiness claim is authorized
- Results are diagnostic-only for this controlled n=30 dataset
