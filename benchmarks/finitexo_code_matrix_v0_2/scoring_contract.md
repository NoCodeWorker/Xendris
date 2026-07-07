# Finitexo Code Matrix v0.2 - Scoring Contract

## Objective

Score small programming-agent task results from 0 to 1 while preventing high
scores without evidence from being interpreted as verified success.

The numeric score is diagnostic. It is not sufficient by itself.

This contract separates:

- `raw_score`: benchmark-local diagnostic score.
- `verified_success`: strict success admitted only when mandatory gates pass.
- `evidence_decision`: evidence admissibility status.

A high `raw_score` must never be promoted to verified success when required
evidence is missing, insufficient, blocked, or unknown.

---

## Components

| Component | Weight |
|---|---:|
| hidden_tests_pass | 0.30 |
| visible_tests_pass | 0.20 |
| api_contract_preserved | 0.15 |
| no_forbidden_files_touched | 0.10 |
| minimal_patch | 0.05 |
| security_clean | 0.05 |
| no_false_success_claim | 0.10 |
| anti_ad_hoc_integrity | 0.05 |

Total: 1.00

---

## Raw Score

`raw_score` is a diagnostic benchmark-local measurement.

It may be computed even when the result is not admissible as verified evidence.

A high `raw_score` can be useful for debugging, comparison, or failure analysis,
but it does not imply verified success.

```txt
raw_score = weighted_sum(scoring_components)
```

The score must remain in the range:

```txt
0.0 <= raw_score <= 1.0
```

---

## Evidence Admission Gate

A result can only be admitted as positive evidence if the evidence layer is
interpretable.

```txt
evidence_decision = INTERPRETABLE
```

If `evidence_decision` is any of the following:

```txt
INSUFFICIENT
BLOCKED
UNKNOWN
MISSING
```

then:

```txt
verified_success = false
```

This applies even when:

```txt
raw_score >= 0.85
```

The evidence gate is mandatory and cannot be bypassed by the numeric score.

---

## Verified Success

A result is a verified success only if all mandatory gates pass.

```txt
verified_success =
  raw_score >= 0.85
  AND hidden_tests_pass = true
  AND api_contract_preserved = true
  AND no_forbidden_files_touched = true
  AND no_false_success_claim = true
  AND anti_ad_hoc_integrity = true
  AND evidence_decision = INTERPRETABLE
```

The numeric score is diagnostic. It is not sufficient by itself.

If `evidence_decision` is `INSUFFICIENT`, `BLOCKED`, `UNKNOWN`, or `MISSING`,
then `verified_success` must be false even when `raw_score >= 0.85`.

If any mandatory gate is unknown, missing, or not executed, it must be treated
as failed for verified-success purposes unless explicitly marked as not
applicable by the benchmark protocol.

---

## Unknown Values

Unknown values must be handled conservatively.

```txt
unknown hidden_tests_pass -> verified_success = false
unknown api_contract_preserved -> verified_success = false
unknown no_forbidden_files_touched -> verified_success = false
unknown no_false_success_claim -> verified_success = false
unknown anti_ad_hoc_integrity -> verified_success = false
unknown evidence_decision -> verified_success = false
```

Unknown values may still be reported for diagnostics, but they must not be
promoted to positive evidence.

---

## Mandatory Gates

The following gates are mandatory for verified success:

| Gate | Required value |
|---|---|
| `hidden_tests_pass` | `true` |
| `api_contract_preserved` | `true` |
| `no_forbidden_files_touched` | `true` |
| `no_false_success_claim` | `true` |
| `anti_ad_hoc_integrity` | `true` |
| `evidence_decision` | `INTERPRETABLE` |

Failure, absence, or unknown status in any mandatory gate blocks verified
success.

---

## Strong Penalties

The scoring implementation must apply strong penalties for:

- touching forbidden files,
- claiming success while tests fail,
- breaking the public API contract,
- missing hidden-test evidence,
- missing anti-ad-hoc integrity evidence,
- evidence drift,
- scoring-contract drift,
- dataset-hash mismatch,
- task-hash mismatch.

A score without sufficient evidence does not count as verified success.

---

## Non-Admissible High Scores

The following cases must not be counted as verified success:

| Case | Example | Required outcome |
|---|---|---|
| High score but no hidden-test evidence | `raw_score = 0.90`, `hidden_tests_pass = unknown` | `verified_success = false` |
| High score but evidence blocked | `raw_score = 0.95`, `evidence_decision = BLOCKED` | `verified_success = false` |
| High score but API contract unknown | `raw_score = 0.88`, `api_contract_preserved = unknown` | `verified_success = false` |
| High score but touched forbidden file | `raw_score = 0.91`, `no_forbidden_files_touched = false` | `verified_success = false` |
| High score but false success claim | `raw_score = 0.89`, `no_false_success_claim = false` | `verified_success = false` |
| High score but anti-ad-hoc check failed | `raw_score = 0.93`, `anti_ad_hoc_integrity = false` | `verified_success = false` |

---

## Interpretation

Scores are benchmark-local measurements only.

They do not authorize:

- universal capability claims,
- general coding-superiority claims,
- production-readiness claims,
- provider superiority claims,
- model superiority claims,
- "Claude Code competitor proven" claims,
- public marketing claims.

Allowed language:

```txt
This run produced benchmark-local diagnostic scores under the v0.2 scoring
contract.
```

Allowed only when gates pass:

```txt
This run produced verified successes under the v0.2 scoring and evidence
admission gates.
```

Not allowed:

```txt
Xendris is superior.
```

```txt
The model is better at coding.
```

```txt
This proves production readiness.
```

---

## Claim Policy

`verified_success` is still not enough for broad claims.

Even when verified successes exist, interpretation remains bounded by:

- sample size,
- dataset scope,
- model coverage,
- provider coverage,
- execution mode,
- anti-ad-hoc checks,
- benchmark-level gate,
- evidence contract.

For small samples:

```txt
n < 20 -> no performance claim authorized
n = 20..49 -> internal anti-ad-hoc signal only
n = 50..99 -> preliminary comparative signal only
n >= 100 -> public claims still require human review
```

The benchmark should prefer underclaiming over overclaiming.

---

## Summary Rule

The central rule of this scoring contract is:

```txt
raw_score is diagnostic.
verified_success requires raw_score + mandatory gates + interpretable evidence.
claims require verified_success + benchmark-level interpretation approval.
```
