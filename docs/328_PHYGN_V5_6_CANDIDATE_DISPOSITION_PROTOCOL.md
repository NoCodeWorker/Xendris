# Phygn v5.6 — Candidate Disposition Protocol

## 0. Purpose

This document defines the candidate disposition protocol after LOG_BOUNDARY control failure.

---

## 1. Control failure review

Create:

```txt
data/frontera_c/disposition/log_boundary_control_failure_review_v5_6.json
```

Schema:

```python
class ControlFailureReview(BaseModel):
    candidate_family: str
    previous_status: str
    positive_smoke_test_ref: str
    negative_control_ref: str
    failure_summary: str
    primary_failure_reason: str
    supporting_control_results: list[dict]
    can_proceed_to_c_structure_ablation: bool
    can_support_frontera_c_validation: bool
    notes: list[str]
```

Required values:

```txt
can_proceed_to_c_structure_ablation = false
can_support_frontera_c_validation = false
```

Primary failure reason:

```txt
GAIN_EXPLAINED_BY_SIMPLE_CONTROL
```

---

## 2. Candidate disposition

Create:

```txt
data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json
```

Schema:

```python
class CandidateDisposition(BaseModel):
    candidate_family: str
    primary_disposition: str
    secondary_roles: list[str]
    archived_as_validation_candidate: bool
    retained_as_fixture: bool
    reason: str
    required_to_reopen_as_candidate: list[str]
    prohibited_actions: list[str]
    notes: list[str]
```

Allowed primary dispositions:

```txt
ARCHIVE_AS_VALIDATION_CANDIDATE
EXPAND_VISIBILITY_DATASET_BEFORE_RECONSIDERATION
REPRIORITIZE_CANDIDATE_FAMILIES
DESIGN_NEW_EXPERIMENT
```

Recommended:

```txt
ARCHIVE_AS_VALIDATION_CANDIDATE
```

Secondary roles may include:

```txt
BENCHMARK_FIXTURE
NEGATIVE_CONTROL_FIXTURE
YTRUE_PIPELINE_REGRESSION_FIXTURE
SOURCE_IDENTITY_REGRESSION_FIXTURE
```

---

## 3. Allowed future roles

Create:

```txt
data/frontera_c/disposition/log_boundary_allowed_future_roles_v5_6.json
```

Allowed:

```txt
benchmark fixture
negative-control fixture
pipeline regression test
single-source y_true smoke-test example
control-failure teaching case
```

Blocked:

```txt
active Frontera C validation candidate
physical mechanism
PredictiveGain evidence
invariant confirmation
generalized decoherence model
```

---

## 4. Reopen criteria

LOG_BOUNDARY may be reopened only if:

```txt
new independent sources are added
accepted_ytrue_count increases beyond single-source N=4
controls are rerun
simple controls no longer explain gain
candidate has out-of-sample predictive advantage
```

Minimum reopen criteria:

```txt
at least 2 independent sources
at least 10 accepted y_true records
out-of-sample or leave-one-source-out evaluation
negative controls survive
```

---

## 5. Final principle

```txt
A failed candidate may become a useful instrument.
It must not remain a hidden claim.
```
