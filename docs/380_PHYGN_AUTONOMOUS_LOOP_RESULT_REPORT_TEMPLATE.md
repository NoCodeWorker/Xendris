# Phygn Autonomous Validate-If-Possible Decision Report Template

## Required title

```txt
# Phygn Autonomous Validate-If-Possible Decision Report
```

## Required fields

```txt
Date:
Final terminal status:
Last completed gate:
First failed gate:
Blocker type:
Missing capability type:
Self-provisioning cycles used:
Capabilities built:
accepted_ytrue_count:
independent_source_count:
dataset version:
benchmark readiness:
candidate family selected:
candidate prediction rule:
baseline model:
candidate model:
PredictiveGain:
negative-control result:
leakage result:
C-structure ablation result:
scientific debt status:
claim permission:
```

## Required sections

```txt
## Executive Decision
## Gate Trace
## Self-Provisioning Audit Summary
## Dataset State
## Candidate State
## Benchmark State
## PredictiveGain State
## Controls State
## C-Ablation State
## Scientific Debt State
## Allowed Claims
## Blocked Claims
## Human Action Required
## Experiment Required
## Next Recommended Phase
```

## Terminal status vocabulary

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_NO_PREDICTIVE_GAIN
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
NO_CANDIDATE_WITH_REALITY_CONTACT_AFTER_CONSTRUCTION_LOOP
SELF_PROVISIONING_LOOP_EXHAUSTED
HUMAN_REVIEW_REQUIRED
EXTERNAL_SOURCE_REQUIRED
```

## Final principle

```txt
A final report is not a victory statement.
It is a permission ledger.
```
