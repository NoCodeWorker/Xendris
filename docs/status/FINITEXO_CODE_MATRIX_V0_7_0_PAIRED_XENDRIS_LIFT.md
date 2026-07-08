# Finitexo Code Matrix v0.7.0 — Paired Xendris Lift

## Why v0.6.0 Was Infrastructure/Provider Baseline Only

v0.6.0 established the controlled-run infrastructure with a real-provider baseline (DeepSeek V4 Flash and GPT-4.1 nano, 30 tasks each, no wrappers). It verified the preflight gate, output isolation, dataset hash checks, scorer range, and artifact pipeline. It did not test any intervention.

## Why v0.7.0 Is the Actual Paired Xendris-Lift Experiment

v0.7.0 measures whether the Xendris admissibility wrapper improves diagnostic scores over the same provider's base model on the same 30 tasks. Each task is executed four times:

| Variant | Provider | Xendris Wrapper |
|---|---|---|
| deepseek_base | DeepSeek V4 Flash | No |
| deepseek_xendris | DeepSeek V4 Flash | Yes |
| openai_base | GPT-4.1 nano | No |
| openai_xendris | GPT-4.1 nano | Yes |

## Dataset

- Source: `benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30/`
- Size: 30 tasks
- Dataset hash: `04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010`
- Manifest hash: `073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519`
- Not modified by v0.7.0

## Expected Attempts

30 tasks × 4 variants = 120 attempts

## Budget

Default cap: $0.75

## Claims Authorized

- Real providers executed under controlled paired conditions
- Xendris wrapper was applied consistently to paired variants
- Diagnostic scores computed using the documented scorer
- Paired lift measured on this n=30 controlled dataset
- Budget tracked per variant
- Provider failures observed or not observed

## Claims Prohibited

- Universal model superiority
- Statistically significant superiority (not authorized without separate statistical gate)
- Production readiness
- General coding ability
- External benchmark performance
- Xendris universal improvement outside this controlled diagnostic run
- Provider ranking (diagnostic-only)

## Safe Execution with Suffix

```bash
set FINITEXO_PAIRED_LIFT_RUN_ID_SUFFIX=live_20260708_01
```

This produces:
- run_id: `finitexo_v0_7_0_paired_xendris_lift_n30_live_20260708_01`
- output_dir: `runs/finitexo_code_matrix_v0_7_0_paired_xendris_lift_n30_live_20260708_01/`

The canonical output directory (`runs/finitexo_code_matrix_v0_7_0_paired_xendris_lift_n30/`) is untouched. If the suffixed directory already exists and is non-empty, the run is blocked.

## Output Artifacts

- summary.json
- report.md
- responses.jsonl
- scores.jsonl
- metadata.jsonl
- costs.json
- errors.jsonl
- preflight.json
- gate.json
- paired_lift.json
- task_level_lift.jsonl
- evidence_integrity.json

## Preflight Checks

- FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM=true
- DEEPSEEK_API_KEY present (env or frontend/.env.local)
- OPENAI_API_KEY present (env or frontend/.env.local)
- Dataset path exists
- Dataset count == 30
- Dataset hash matches
- Manifest hash matches
- Output directory empty or nonexistent
- Expected attempts == 120
- Budget cap present
- Temperature == 0.0
- Provider mode == real
