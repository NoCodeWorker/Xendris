# Phygn v4.4.2 — Claim, Metric & Residual Debt Remediation

## 0. Purpose

This document defines remediation of nonblocking claim leakage, metric integrity and residual audit debt.

---

## 1. Claim leakage remediation

Create:

```txt
data/audits/remediation/phygn_claim_leakage_remediation_v4_4_2.json
```

Schema:

```python
class ClaimLeakageRemediationRecord(BaseModel):
    leakage_id: str
    artifact_path: str
    claim_text: str
    leakage_status: str
    severity: str
    remediation_action: str
    rewritten_claim: str | None
    final_status: str
    blocks_next_gate: bool
```

Actions:

```txt
REWRITE_CLAIM
ADD_PERMISSION_QUALIFIER
MOVE_TO_BLOCKED_CLAIMS
MARK_HISTORICAL_ONLY
ACCEPT_AS_NONBLOCKING_WITH_NOTE
```

---

## 2. Metric integrity remediation

Create:

```txt
data/audits/remediation/phygn_metric_integrity_remediation_v4_4_2.json
```

Schema:

```python
class MetricIntegrityRemediationRecord(BaseModel):
    metric_name: str
    artifact_path: str
    misuse_risk: str
    remediation_action: str
    required_label: str
    forbidden_label: str | None
    final_status: str
```

Critical metric labels:

```txt
BenchmarkComparisonScore != PredictiveGain
SyntheticGain != PredictiveGain
SourcePressureScore != validation
ObservableAlignmentScore != observed truth
```

---

## 3. Accepted residual audit debt

Create:

```txt
data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json
```

Schema:

```python
class AcceptedResidualAuditDebt(BaseModel):
    debt_id: str
    source_issue_id: str
    category: str
    severity: str
    reason_accepted: str
    owner: str
    next_review_phase: str
    may_continue_pipeline: bool
    blocks_claims: list[str]
    does_not_block: list[str]
    notes: list[str]
```

Accepted debt must never block silently.

---

## 4. Post-remediation delta

Create:

```txt
data/audits/remediation/phygn_post_remediation_audit_delta_v4_4_2.json
```

Fields:

```txt
initial_nonblocking_issue_count
remaining_nonblocking_issue_count
initial_unmapped_status_count
remaining_unmapped_status_count
critical_unmapped_status_count
initial_status_only_test_issue_count
remaining_status_only_test_issue_count
blocker_count_before
blocker_count_after
claims_rewritten_count
metrics_relabelled_count
debt_items_accepted_count
continuation_gate
```

---

## 5. Continuation gate

Create:

```txt
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
```

Fields:

```txt
gate_status
can_continue_pipeline
recommended_next_phase
required_before_v4_5
accepted_residual_debt_ref
blocked_claims
allowed_claims
notes
```

---

## 6. Recommended next phase options

If remediation permits continuation:

```txt
v4.5 — Public Dataset Acquisition & Table/Figure Review Continuation
```

If remediation remains high:

```txt
v4.4.3 — Remaining Status Mapping & Test Hardening
```

If blockers emerge:

```txt
v4.4.3 — Blocking Logic Remediation Sprint
```

---

## 7. Final principle

```txt
Accepted debt is not forgotten debt.
It is scheduled epistemic risk.
```
