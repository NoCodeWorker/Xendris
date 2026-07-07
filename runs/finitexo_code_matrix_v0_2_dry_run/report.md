# Finitexo Code Matrix v0.2 - Anti-Ad-Hoc Validation

## Scope

Infrastructure run for anti-ad-hoc validation. No superiority claim is authorized.

## Configuration

- Execution mode: dry-run
- Samples: 5
- Models: deepseek-v4-flash, gpt-4.1-nano
- Variants: base_agent, base_agent_with_contract_prompt, base_agent_with_scoring_awareness, xendris_agent, xendris_calibrated_agent
- Dataset hash: 18ea0b43b7febb43dfcb5411a652a8641699253c42d33d65c3bce991eb90b304
- Scoring contract hash: c92d9a7e07be6a00fbc21ec7546dec3f56d39af9e8be36dbc35dcf6f5a84da74

## Dataset Integrity

- Anti-ad-hoc decision: WARNINGS_PRESENT
- Warnings: ['sample_count_below_20_budget_validation_only']
- Blocking issues: []

## Matrix Results

| model | variant | execution_status | evidence_decision | benchmark_gate | limitations |
|---|---|---|---|---|---|
| deepseek-v4-flash | base_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| deepseek-v4-flash | base_agent_with_contract_prompt | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| deepseek-v4-flash | base_agent_with_scoring_awareness | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| deepseek-v4-flash | xendris_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| deepseek-v4-flash | xendris_calibrated_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| gpt-4.1-nano | base_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| gpt-4.1-nano | base_agent_with_contract_prompt | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| gpt-4.1-nano | base_agent_with_scoring_awareness | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| gpt-4.1-nano | xendris_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |
| gpt-4.1-nano | xendris_calibrated_agent | DRY_RUN_ONLY | INSUFFICIENT | BUDGET_VALIDATION_ONLY | No provider execution was performed; no performance metric is generated. |

## Claims Explicitly Not Authorized

- Universal superiority.
- General coding superiority.
- Production readiness.
- Transfer to unmeasured models or providers.

## Conclusion

This artifact validates benchmark plumbing and anti-ad-hoc controls only. It does not contain live provider performance results.
