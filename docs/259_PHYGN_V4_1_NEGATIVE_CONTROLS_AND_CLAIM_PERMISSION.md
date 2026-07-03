# Phygn v4.1 — Negative Controls & Claim Permission

## 0. Purpose

This document defines negative-control evaluation and claim permission updates.

---

## 1. Negative controls input

Load:

```txt
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
```

Required control types:

```txt
BASELINE_ONLY_CONTROL
OBSERVABLE_ONLY_CONTROL
BENCHMARK_RANGE_CONTROL
PARAMETER_CONSTRAINT_CONTROL
LIMITATION_STRESS_CONTROL
NO_SLOT4_CONTROL
```

---

## 2. Negative control result

Create:

```txt
data/model_comparison/phi_gradient_negative_control_results_v4_1.json
```

Schema:

```python
class NegativeControlResult(BaseModel):
    control_id: str
    control_type: str
    tested_models: list[str]
    expected_result_if_candidate_is_only_analogy: str
    expected_result_if_candidate_has_signal: str
    observed_result: str
    survival_status: str
    failure_reason: str | None
    claim_impact: str
```

Survival statuses:

```txt
CONTROL_SURVIVED
CONTROL_FAILED
CONTROL_INCONCLUSIVE
CONTROL_NOT_RUN_NO_DATA
```

---

## 3. NO_SLOT4 control

This is mandatory.

If candidate advantage survives when SLOT_4 is zeroed:

```txt
claim_impact = ADVANTAGE_NOT_DEPENDENT_ON_GRADIENT_MECHANISM
```

If candidate advantage requires SLOT_4 despite open debt:

```txt
claim_impact = CLAIM_BLOCKED_BY_SLOT4_DEBT
```

If no real y_true exists:

```txt
CONTROL_INCONCLUSIVE
```

---

## 4. Claim permission update

Create:

```txt
data/model_comparison/phi_gradient_claim_permission_update_v4_1.json
```

Schema:

```python
class ClaimPermissionUpdate(BaseModel):
    update_id: str
    source_pressure_ref: str
    benchmark_ref: str
    debt_ref: str
    model_comparison_ref: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    conditional_claims: list[str]
    physical_claim_permission: str
    gradient_mechanism_claim_permission: str
    benchmark_claim_permission: str
    next_required_gate: str
```

---

## 5. Allowed claims after v4.1

Possible allowed claims:

```txt
A debt-bounded benchmark comparison was performed.
Candidate behavior was compared against source-pressure-derived benchmark rows.
SLOT_4 debt remained enforced during comparison.
Negative controls were applied or queued.
```

Blocked:

```txt
PHI_GRADIENT is validated.
PHI_GRADIENT has predictive gain.
Gradient mechanism is supported.
Frontera C is validated.
Invariant is empirically confirmed.
```

Conditional:

```txt
Candidate may be benchmark-actionable if comparison score survives negative controls.
```

---

## 6. Final principle

```txt
Claim permission is the output that matters.
```
