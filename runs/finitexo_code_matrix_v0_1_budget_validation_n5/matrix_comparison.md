# Finitexo Code Matrix v0.1 - Budget Validation n=5

## Scope

This run is a controlled budget validation phase for the Finitexo Code Matrix
v0.1 benchmark. It repeats the n=1 smoke and n=3 mini-validation pattern on
five samples per variant.

This is not a statistically conclusive benchmark. It is a budget validation
run only. No superiority claim is authorized.

## Configuration

| Field | Value |
|---|---|
| Dataset | Xendris Agentic Programming v0.1 |
| Samples per variant | 5 |
| Max iterations | 1 |
| Max concurrent | 1 |
| Transport | direct |
| DeepSeek model | deepseek-v4-flash |
| OpenAI model | gpt-4.1-nano |
| Budget cap per provider run | $0.50 |
| Hard target for this phase | <= $0.05 |
| Actual spend | $0.004786 |
| Budget compliance | PASS |

## Matrix Results

| model | variant | total_score | pass_rate | estimated_cost | verified_successes | cost_per_verified_success | evidence_decision | benchmark_gate | limitations |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| DeepSeek V4 Flash | deepseek_base_agent | 0.4900 | 0.0000 | $0.001250 | 0 | N/A | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION | Blocked variant retained for comparison only; not admitted as positive evidence. |
| DeepSeek V4 Flash | deepseek_xendris_agent | 1.0000 | 1.0000 | $0.001502 | 5 | $0.000300 | INTERPRETABLE | READY_FOR_INTERPRETATION | n=5 budget validation only; not statistically conclusive. |
| DeepSeek V4 Flash | deepseek_xendris_calibrated_agent | 1.0000 | 1.0000 | $0.001244 | 5 | $0.000249 | INTERPRETABLE | READY_FOR_INTERPRETATION | n=5 budget validation only; not statistically conclusive. |
| GPT-4.1 nano | openai_base_agent | 0.4900 | 0.0000 | $0.000212 | 0 | N/A | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION | Blocked variant retained for comparison only; not admitted as positive evidence. |
| GPT-4.1 nano | openai_xendris_agent | 1.0000 | 1.0000 | $0.000291 | 5 | $0.000058 | INTERPRETABLE | READY_FOR_INTERPRETATION | n=5 budget validation only; not statistically conclusive. |
| GPT-4.1 nano | openai_xendris_calibrated_agent | 1.0000 | 1.0000 | $0.000288 | 5 | $0.000058 | INTERPRETABLE | READY_FOR_INTERPRETATION | n=5 budget validation only; not statistically conclusive. |
| DeepSeek Reasoner | SKIPPED_MODEL_NOT_AVAILABLE | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Model unavailable in current codebase for this phase. |
| GPT-5.5 | SKIPPED_BUDGET_CONSTRAINT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Reserved for a later single-task premium reference baseline. |

## Provider Totals

| model | actual_spend | verified_successes | cost_per_verified_success | evidence_decision | benchmark_level_decision |
|---|---:|---:|---:|---|---|
| DeepSeek V4 Flash | $0.003995 | 10 | $0.000400 | INTERPRETABLE | WARNINGS_PRESENT |
| GPT-4.1 nano | $0.000791 | 10 | $0.000079 | INTERPRETABLE | WARNINGS_PRESENT |
| Total | $0.004786 | 20 | $0.000239 | INTERPRETABLE | WARNINGS_PRESENT |

## Trend: n=1 -> n=3 -> n=5

| phase | samples | model | base_agent_score | xendris_agent_score | xendris_calibrated_score | total_cost | evidence_decision | benchmark_gate |
|---|---:|---|---:|---:|---:|---:|---|---|
| smoke | 1 | DeepSeek V4 Flash | 0.6500 | 1.0000 | 1.0000 | $0.000943 | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION |
| smoke | 1 | GPT-4.1 nano | 0.6500 | 1.0000 | 1.0000 | $0.000227 | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION |
| mini | 3 | DeepSeek V4 Flash | 0.5167 | 1.0000 | 1.0000 | $0.001698 | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION |
| mini | 3 | GPT-4.1 nano | 0.5167 | 1.0000 | 1.0000 | $0.000431 | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION |
| validation | 5 | DeepSeek V4 Flash | 0.4900 | 1.0000 | 1.0000 | $0.003995 | INTERPRETABLE | WARNINGS_PRESENT |
| validation | 5 | GPT-4.1 nano | 0.4900 | 1.0000 | 1.0000 | $0.000791 | INTERPRETABLE | WARNINGS_PRESENT |

## Interpretation

The signal repeated from n=1 and n=3 in this n=5 budget validation run: both
Xendris variants scored 1.0000 on both measured models, while the base variants
remained below the benchmark gate threshold.

This does not authorize a superiority claim. The sample size is still small,
the dataset is closed, and the result is not statistically conclusive. A larger
sample is required before performance claims.

## Evidence Contract vs Benchmark Gate

The `evidence_contract.decision` is `INTERPRETABLE` for both provider runs.
That means the evidence layer has sufficient identity, provenance, model,
transport and scoring metadata for bounded interpretation.

The benchmark-level decision is `WARNINGS_PRESENT` for n=5 because the base
variants are blocked by the variant-level benchmark gate. Those blocked
variants are retained for comparison only and must not be treated as admitted
positive evidence.

Earlier n=1 and n=3 artifacts report `BLOCKED_FOR_INTERPRETATION` at benchmark
level because they predate the comparison-mode gate semantics used in this n=5
validation.

## Budget

| Budget item | Value |
|---|---:|
| Hard target | $0.050000 |
| Absolute stop threshold | $0.500000 |
| Actual spend | $0.004786 |
| Remaining under hard target | $0.045214 |
| Budget stayed under hard target | yes |
| Budget risk exceeded | no |

## Artifacts

| Path | Purpose |
|---|---|
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/deepseek-v4-flash/summary.json` | DeepSeek V4 Flash summary |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/deepseek-v4-flash/results.jsonl` | DeepSeek V4 Flash per-sample results |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/deepseek-v4-flash/report.md` | DeepSeek V4 Flash benchmark report |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/deepseek-v4-flash/evidence_report.md` | DeepSeek V4 Flash evidence report |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/gpt-4.1-nano/summary.json` | GPT-4.1 nano summary |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/gpt-4.1-nano/results.jsonl` | GPT-4.1 nano per-sample results |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/gpt-4.1-nano/report.md` | GPT-4.1 nano benchmark report |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/gpt-4.1-nano/evidence_report.md` | GPT-4.1 nano evidence report |
| `runs/finitexo_code_matrix_v0_1_budget_validation_n5/matrix_comparison.md` | Consolidated matrix comparison |

## Conclusion

This phase completed as a budget validation run. The n=1 and n=3 signal
repeated at n=5 for the measured DeepSeek V4 Flash and GPT-4.1 nano variants.

No universal, general coding, or production-readiness claim is made or implied.
Larger samples and broader model coverage are required before performance
claims.
