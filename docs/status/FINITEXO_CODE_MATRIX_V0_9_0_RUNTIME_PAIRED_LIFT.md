# Finitexo Code Matrix v0.9.0 — Runtime Paired Lift (n=30)

**Status:** IN PROGRESS — module files written, tests not yet executed.

## Objective

Restore foundational Xendris runtime methodology after the wrapper-only deviation in v0.7.0 and v0.8.1.
v0.9.0 includes Calibrated Runtime as a first-class variant.
v0.9.0 may not be executed unless the methodology guard passes.

## Key Differences from v0.8.1

| Aspect | v0.8.1 (wrapper) | v0.9.0 (runtime) |
|--------|-------------------|-------------------|
| Methodology | Prompt wrapper | Full runtime loop |
| Variants | 4 (2 base, 2 wrapper) | 8 (2 base, 2 wrapper, 2 runtime, 2 calibrated runtime) |
| Expected top-level executions | 120 | 240 |
| Budget | $1.00 | $2.00 |
| Audit | Scorer only | 12-component deterministic audit + decision |
| Repair loop | No | Yes (conditional) |
| Calibrated runtime | No | First-class variant |
| Traces | No | runtime_traces.jsonl, calibration_traces.jsonl, audit_decisions.jsonl, repair_attempts.jsonl |
| Suffix env | FINITEXO_HARD_LIFT_RUN_ID_SUFFIX | FINITEXO_RUNTIME_LIFT_RUN_ID_SUFFIX |
| Lift comparisons | Wrapper vs base | Wrapper vs base, Runtime vs base, Runtime vs wrapper, Calibrated vs all |

## Module Files (9)

| File | Purpose |
|------|---------|
| `runtime_lift_config.py` | Config with 6 variants, v0.8.0 hashes, $2.00 budget |
| `runtime_lift_types.py` | Enums, dataclasses (Trace, AuditResult, ScoredRecord, etc.) |
| `runtime_lift_gate.py` | Preflight gate |
| `runtime_lift_audit.py` | Deterministic audit engine + repair prompt builder |
| `runtime_lift_scoring.py` | Scorer + all lift computations + repair/audit metrics |
| `runtime_lift_runner.py` | Full runtime loop runner |
| `runtime_lift_report.py` | Report with all lift tables |
| `__init__.py` | Public API |

## Methodology Guard (new)

- `xendris/core/methodology/` — foundational contract types and validation
- `benchmarks/finitexo_code_matrix_v0_9/methodology_guard/` — v0.9-specific gate

## Variants (8)

1. `deepseek_base` — deepseek-v4-flash, direct
2. `deepseek_wrapper` — deepseek-v4-flash, Xendris wrapper
3. `deepseek_runtime` — deepseek-v4-flash, Xendris runtime loop
4. `deepseek_calibrated_runtime` — deepseek-v4-flash, Xendris runtime + calibration
5. `openai_base` — gpt-4.1-nano, direct
6. `openai_wrapper` — gpt-4.1-nano, Xendris wrapper
7. `openai_runtime` — gpt-4.1-nano, Xendris runtime loop
8. `openai_calibrated_runtime` — gpt-4.1-nano, Xendris runtime + calibration

Expected top-level executions: 8 × 30 = 240.
Provider call count may exceed 240 due to repair passes.

## Runtime Loop

For each runtime variant task:
1. Provider initial call
2. Deterministic audit (12 components)
3. Audit decision: ALLOW / ALLOW_WITH_LIMITATIONS / REPAIR_REQUIRED / BLOCK / HUMAN_REVIEW_REQUIRED
4. If REPAIR_REQUIRED: repair call, final audit, use best response
5. If BLOCK: return controlled limitation response
6. Otherwise: use initial response directly

## Calibrated Runtime Loop

All runtime phases plus:
7. Claim classification
8. Evidence status resolution
9. Confidence banding
10. Allowed/blocked language selection
11. Final calibrated response

## Methodology Guard Requirements

- All 8 variants must be present
- Runtime traces artifact must be configured
- Calibration traces artifact must be configured
- Audit decisions artifact must be configured
- Repair attempts artifact must be configured
- Expected top-level executions must be 240
- No provider execution without passing guard

## Hard Rules

- No live provider execution without confirmation env var
- No modification of v0.4.3 / v0.6.0 / v0.7.0 / v0.8.0 / v0.8.1 artifacts
- No superiority claims
- No runs/ in staging
- No live provider execution during implementation

## Artifacts (output dir)

- `summary.json`, `report.md`, `responses.jsonl`, `scores.jsonl`, `costs.json`
- `paired_lift.json`, `family_lift.json`
- `runtime_traces.jsonl`, `calibration_traces.jsonl`, `audit_decisions.jsonl`, `repair_attempts.jsonl`
- `evidence_integrity.json`, `gate.json`, `preflight.json`, `errors.jsonl`, `metadata.jsonl`

## Next Steps

1. Run tests
2. Report results
