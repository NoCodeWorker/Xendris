# Finitexo Code Matrix v0.3 - Scoring Contract

## Objective

Score small programming-agent task submissions from 0 to 1 while preventing
high scores without evidence from being interpreted as verified success.

This contract is adversarial by design. It separates diagnostic scoring from
verified success and requires blind scoring plus interpretable evidence.

## Components

| Component | Weight |
|---|---:|
| hidden_tests_pass | 0.30 |
| visible_tests_pass | 0.15 |
| api_contract_preserved | 0.15 |
| minimal_patch | 0.10 |
| no_forbidden_files_touched | 0.10 |
| security_clean | 0.05 |
| no_false_success_claim | 0.10 |
| external_validity_integrity | 0.05 |

Total: 1.00

## Raw Score

`raw_score` is a benchmark-local diagnostic score.

It may be computed even when the result is not admissible as verified evidence.
It must never be treated as verified success by itself.

## Verified Success

A result is a verified success only if all conditions hold:

```txt
raw_score >= 0.85
hidden_tests_pass = true
api_contract_preserved = true
no_forbidden_files_touched = true
no_false_success_claim = true
external_validity_integrity = true
evidence_decision = INTERPRETABLE
```

Unknown, missing, or not-executed mandatory values block verified success.

## Blind Scoring

The scorer must not receive:

- variant;
- provider;
- model;
- agent_name;
- xendris_label;
- baseline_label.

If any identity field reaches the blind scoring payload:

```txt
blind_scoring_decision = FAILED
verified_success = false
```

## Interpretation

Scores are benchmark-local measurements only. They do not authorize universal,
general coding, production-readiness, provider, or model superiority claims.

