# Finitexo Code Matrix v0.8.1 — Hard Paired Xendris Lift (n=30)

**Status:** IN PROGRESS — module files written, tests not yet executed.

## Objective

Apply the v0.7.0 paired Xendris lift methodology to the hard v0.8.0 dataset (n=30, 5 families × 6) to reduce ceiling effects observed in v0.7.0.

## Key Differences from v0.7.0

| Aspect | v0.7.0 (easy) | v0.8.1 (hard) |
|--------|---------------|----------------|
| Dataset | Controlled run n=30 (easy) | Hard programming n=30 |
| Mean scores | ~0.89 (DS), ~0.88 (OA) | Expected lower ceiling |
| Budget | $0.75 | $1.00 |
| Family tracking | No | Yes (`task_family` in records) |
| Family lift artifact | No | `family_lift.json` |
| Config suffix env | `FINITEXO_CONTROLLED_RUN_ID_SUFFIX` | `FINITEXO_HARD_LIFT_RUN_ID_SUFFIX` |

## Module Files (6)

| File | Purpose |
|------|---------|
| `hard_lift_config.py` | Config with v0.8.0 hashes, $1.00 budget, 4 variants |
| `hard_lift_gate.py` | Preflight gate (HARD_LIFT_PREFLIGHT_READY / BLOCKED) |
| `hard_lift_scoring.py` | Scorer + `task_family` + `aggregate_by_family_variant()` + `compute_family_lift()` |
| `hard_lift_runner.py` | Runner with 120-count integrity check + family_lift.json |
| `hard_lift_report.py` | Report with family lift table |
| `__init__.py` | Public API |

## Variants

1. `deepseek_base` — deepseek-v4-flash, no Xendris
2. `deepseek_xendris` — deepseek-v4-flash, with Xendris wrapper
3. `openai_base` — gpt-4.1-nano, no Xendris
4. `openai_xendris` — gpt-4.1-nano, with Xendris wrapper

Expected attempts: 4 × 30 = 120.

## Hard Rules (inherited from v0.4.3+)

- No live provider execution without confirmation env var
- No modification of v0.4.3 / v0.6.0 / v0.7.0 / v0.8.0 artifacts
- No superiority claims
- No `runs/` in staging

## Artifacts (output dir)

- `summary.json`, `report.md`, `responses.jsonl`, `scores.jsonl`, `costs.json`
- `paired_lift.json`, `task_level_lift.jsonl`
- `family_lift.json` ✨ new
- `evidence_integrity.json`, `gate.json`, `preflight.json`, `errors.jsonl`, `metadata.jsonl`

## Test Plan

- 35 tests covering: config defaults, suffix, preflight gate, Xendris wrapper, scorer, family-aware scoring, paired lift, runner, artifacts, evidence integrity, budget, claims, report.

## Next Steps

1. Run tests (`pytest tests/benchmarking/test_finitexo_code_matrix_v0_8_hard_paired_xendris_lift.py -v`)
2. Run all regression tests (v0.6 + v0.7 + v0.8 + v0.8.1)
3. Stage and commit
