# Phygn v4.6 — Final Claim Permission & Method-Only Redefinition

## 0. Purpose

This document defines the final permitted and blocked claims for PHI_GRADIENT after empirical freeze.

---

## 1. Final claim permissions

Create:

```txt
data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json
```

Schema:

```python
class FinalClaimPermissions(BaseModel):
    candidate_id: str
    decision_ref: str
    predictive_gain_permission: str
    physical_claim_permission: str
    gradient_mechanism_claim_permission: str
    benchmark_method_permission: str
    method_only_permission: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    archived_claims: list[str]
    required_to_unblock: list[str]
```

Required values:

```txt
predictive_gain_permission = BLOCKED_NO_YTRUE
physical_claim_permission = BLOCKED
gradient_mechanism_claim_permission = BLOCKED_BY_SLOT4_DEBT
```

---

## 2. Allowed claims

Allowed:

```txt
PHI_GRADIENT was evaluated as a benchmark candidate.
PHI_GRADIENT failed to obtain accepted y_true from available sources.
PHI_GRADIENT is frozen as empirically ungrounded under current artifacts.
PHI_GRADIENT may remain useful as a methodological stress-test if redefined.
```

---

## 3. Blocked claims

Blocked:

```txt
PHI_GRADIENT is predictively validated.
PHI_GRADIENT has PredictiveGain.
PHI_GRADIENT is empirically supported.
PHI_GRADIENT is a source-backed physical mechanism.
PHI_GRADIENT validates Frontera C.
PHI_GRADIENT confirms the invariant.
```

---

## 4. Method-only redefinition

Create:

```txt
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
```

Schema:

```python
class MethodOnlyRedefinition(BaseModel):
    candidate_id: str
    redefinition_status: str
    allowed_method_roles: list[str]
    prohibited_scientific_roles: list[str]
    allowed_future_use: list[str]
    required_label: str
    notes: list[str]
```

Allowed method roles:

```txt
negative-control generator
benchmark-shaping heuristic
candidate-stress-test fixture
source-pressure pipeline test case
claim-gating regression fixture
```

Prohibited scientific roles:

```txt
physical model
validated mechanism
predictive model
Frontera C evidence
invariant confirmation
```

Required label:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

---

## 5. Required to unblock

To reopen PHI_GRADIENT as active predictive candidate, require:

```txt
at least 3 accepted y_true records
matched predictions
source provenance
QC pass
and either SLOT_4 debt resolution or explicit non-SLOT_4 claim scope
```

---

## 6. Final principle

```txt
A method-only object must not masquerade as a physical model.
```
