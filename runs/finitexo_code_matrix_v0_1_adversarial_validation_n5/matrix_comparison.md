# Finitexo Code Matrix v0.1 - Adversarial Validation n=5

## Scope

This run is a controlled adversarial validation phase for the Finitexo Code
Matrix v0.1 benchmark. It intentionally uses five less favorable or more
failure-prone tasks than the previous budget validation subset.

This phase is designed to look for robustness limits and failure modes. It is
not a statistically conclusive benchmark. No superiority claim is authorized.

## Configuration

| Field | Value |
|---|---|
| Dataset | Derived adversarial subset of Xendris Agentic Programming v0.1 |
| Subset path | `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/adversarial_subset` |
| Canonical dataset modified | no |
| Samples per variant | 5 |
| Max iterations | 1 |
| Max concurrent | 1 |
| Transport | direct |
| DeepSeek model | deepseek-v4-flash |
| OpenAI model | gpt-4.1-nano |
| Budget cap per provider run | $0.50 |
| Hard target for this phase | <= $0.05 |
| Actual spend | $0.007409 |
| Budget compliance | PASS |

## Adversarial Task Coverage

| task_id | adversarial_type | reason_selected |
|---|---|---|
| AP-007 | false_success_trap | Requires both implementation fix and a unit test; easy to claim completion without preserving checks. |
| AP-014 | api_contract_trap | Deep merge can pass shallow visible cases while breaking the public contract for nested dictionaries. |
| AP-008 | minimal_patch_trap | Refactor touches multiple allowed files and can penalize over-editing or inconsistent API migration. |
| AP-006 | hidden_test_sensitivity | Visible behavior is simple but hidden edge cases cover None, zero divisor, and non-numeric inputs. |
| AP-017 | security_unsafe_change_trap | Unsafe eval replacement requires preserving arithmetic utility without introducing dangerous execution. |

## Matrix Results

| model | variant | total_score | pass_rate | estimated_cost | verified_successes | cost_per_verified_success | evidence_decision | benchmark_gate | limitations |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| DeepSeek V4 Flash | deepseek_base_agent | 0.7400 | 0.4000 | $0.001433 | 2 | $0.000716 | INTERPRETABLE | WARNINGS_PRESENT | Failed API-contract/edge/security-sensitive cases; retained as baseline comparison only. |
| DeepSeek V4 Flash | deepseek_xendris_agent | 0.9300 | 0.8000 | $0.002291 | 4 | $0.000573 | INTERPRETABLE | READY_FOR_INTERPRETATION | Failed hidden-test sensitivity on AP-006. |
| DeepSeek V4 Flash | deepseek_xendris_calibrated_agent | 0.8500 | 0.6000 | $0.002014 | 3 | $0.000671 | INTERPRETABLE | READY_FOR_INTERPRETATION | Failed AP-006 hidden-test sensitivity and AP-017 security-sensitive behavior. |
| GPT-4.1 nano | openai_base_agent | 0.3300 | 0.2000 | $0.000575 | 1 | $0.000575 | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION | Blocked baseline; includes AP-007 runner/API-contract failure and AP-017 security-sensitive failure. |
| GPT-4.1 nano | openai_xendris_agent | 0.8600 | 0.6000 | $0.000556 | 3 | $0.000185 | INTERPRETABLE | READY_FOR_INTERPRETATION | Failed AP-006 hidden-test sensitivity and AP-017 hidden behavior. |
| GPT-4.1 nano | openai_xendris_calibrated_agent | 0.9200 | 0.8000 | $0.000541 | 4 | $0.000135 | INTERPRETABLE | READY_FOR_INTERPRETATION | Failed AP-017 security-sensitive behavior. |
| DeepSeek Reasoner | SKIPPED_MODEL_NOT_AVAILABLE | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Model unavailable in current codebase for this phase. |
| GPT-5.5 | SKIPPED_BUDGET_CONSTRAINT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Reserved for a later single-task premium reference baseline. |

## Provider Totals

| model | actual_spend | verified_successes | cost_per_verified_success | evidence_decision | benchmark_level_decision |
|---|---:|---:|---:|---|---|
| DeepSeek V4 Flash | $0.005737 | 9 | $0.000637 | INTERPRETABLE | READY_FOR_INTERPRETATION |
| GPT-4.1 nano | $0.001672 | 8 | $0.000209 | INTERPRETABLE | WARNINGS_PRESENT |
| Total | $0.007409 | 17 | $0.000436 | INTERPRETABLE | WARNINGS_PRESENT |

## Trend: n=5 Budget Validation vs n=5 Adversarial Validation

| phase | samples | model | base_agent_score | xendris_agent_score | xendris_calibrated_score | total_cost | evidence_decision | benchmark_gate |
|---|---:|---|---:|---:|---:|---:|---|---|
| budget validation | 5 | DeepSeek V4 Flash | 0.4900 | 1.0000 | 1.0000 | $0.003995 | INTERPRETABLE | WARNINGS_PRESENT |
| budget validation | 5 | GPT-4.1 nano | 0.4900 | 1.0000 | 1.0000 | $0.000791 | INTERPRETABLE | WARNINGS_PRESENT |
| adversarial validation | 5 | DeepSeek V4 Flash | 0.7400 | 0.9300 | 0.8500 | $0.005737 | INTERPRETABLE | READY_FOR_INTERPRETATION |
| adversarial validation | 5 | GPT-4.1 nano | 0.3300 | 0.8600 | 0.9200 | $0.001672 | INTERPRETABLE | WARNINGS_PRESENT |

## Failure Mode Notes

| model | variant | observed failure types |
|---|---|---|
| DeepSeek V4 Flash | deepseek_base_agent | AP-014 API contract, AP-006 hidden-test sensitivity, AP-017 security-sensitive behavior. |
| DeepSeek V4 Flash | deepseek_xendris_agent | AP-006 hidden-test sensitivity. |
| DeepSeek V4 Flash | deepseek_xendris_calibrated_agent | AP-006 hidden-test sensitivity, AP-017 security-sensitive behavior. |
| GPT-4.1 nano | openai_base_agent | AP-007 runner/API-contract failure, AP-014 API contract, AP-006 hidden-test sensitivity, AP-017 security-sensitive behavior. |
| GPT-4.1 nano | openai_xendris_agent | AP-006 hidden-test sensitivity, AP-017 hidden behavior. |
| GPT-4.1 nano | openai_xendris_calibrated_agent | AP-017 security-sensitive behavior. |

## Interpretation

The previous n=5 budget validation signal survived only partially under
adversarial validation.

The Xendris variants remained ahead of their corresponding base variants in
this small adversarial subset, but they no longer scored perfectly. The drop is
important: it shows that the earlier perfect scores were not robust to this
more adversarial task selection.

This is a useful robustness signal, not a superiority claim. n=5 remains small,
the subset is manually selected, and broader adversarial coverage is required
before performance claims.

## Evidence Contract vs Benchmark Gate

The `evidence_contract.decision` is `INTERPRETABLE` for both provider runs.
That means execution identity, provider provenance, transport, model identity,
and scoring metadata are sufficient for bounded interpretation.

The benchmark-level decision differs by provider:

- DeepSeek V4 Flash: `READY_FOR_INTERPRETATION`, because no variant was fully
  blocked, though the baseline has warnings.
- GPT-4.1 nano: `WARNINGS_PRESENT`, because the base variant is
  `BLOCKED_FOR_INTERPRETATION`.

Blocked or warning variants are retained for comparison only. They are not
admitted as positive evidence.

## Budget

| Budget item | Value |
|---|---:|
| Hard target | $0.050000 |
| Absolute stop threshold | $0.500000 |
| Actual spend | $0.007409 |
| Remaining under hard target | $0.042591 |
| Budget stayed under hard target | yes |
| Budget risk exceeded | no |

## Artifacts

| Path | Purpose |
|---|---|
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/adversarial_subset/dataset.json` | Derived adversarial subset manifest |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/adversarial_task_selection.json` | Task selection metadata |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/adversarial_subset_README.md` | Human-readable task selection rationale |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/deepseek-v4-flash/summary.json` | DeepSeek V4 Flash summary |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/deepseek-v4-flash/results.jsonl` | DeepSeek V4 Flash per-sample results |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/deepseek-v4-flash/report.md` | DeepSeek V4 Flash benchmark report |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/deepseek-v4-flash/evidence_report.md` | DeepSeek V4 Flash evidence report |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/gpt-4.1-nano/summary.json` | GPT-4.1 nano summary |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/gpt-4.1-nano/results.jsonl` | GPT-4.1 nano per-sample results |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/gpt-4.1-nano/report.md` | GPT-4.1 nano benchmark report |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/gpt-4.1-nano/evidence_report.md` | GPT-4.1 nano evidence report |
| `runs/finitexo_code_matrix_v0_1_adversarial_validation_n5/matrix_comparison.md` | Consolidated adversarial matrix comparison |

## Conclusion

This phase completed as an adversarial validation run. The signal did not remain
perfect, but it did remain directionally positive for Xendris variants against
their base variants on the selected adversarial subset.

No universal, general coding, or production-readiness claim is made or implied.
Larger adversarial samples are required before performance claims.
