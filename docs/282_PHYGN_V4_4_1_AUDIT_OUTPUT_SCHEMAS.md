# Phygn v4.4.1 — Audit Output Schemas

## 0. Purpose

This document defines the full suite logic audit artifacts.

---

## 1. Full suite audit

Create:

```txt
data/audits/phygn_full_suite_logic_audit_v4_4_1.json
```

Schema:

```python
class FullSuiteLogicAudit(BaseModel):
    audit_id: str
    created_at: str
    audited_versions: list[str]
    audited_modules: list[str]
    audited_artifacts: list[str]
    issue_count: int
    blocker_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    final_status: str
    can_continue_pipeline: bool
    required_remediation_before_next_gate: list[str]
    notes: list[str]
```

---

## 2. Audit issue

```python
class AuditIssue(BaseModel):
    issue_id: str
    severity: str
    category: str
    location: str
    affected_versions: list[str]
    description: str
    why_it_matters: str
    evidence: list[str]
    recommended_fix: str
    blocks_next_gate: bool
```

Categories:

```txt
CLAIM_PERMISSION_LEAK
PREDICTIVE_GAIN_MISUSE
SOURCE_SUPPORT_MISUSE
YTRUE_MISUSE
SLOT4_DEBT_BYPASS
STATUS_MAPPING_INCONSISTENCY
TEST_TAUTOLOGY
NEGATIVE_CONTROL_WEAKNESS
STALE_ARTIFACT_RISK
METRIC_INTEGRITY_RISK
REPORTING_OVERCLAIM
NAMING_AMBIGUITY
```

---

## 3. Status permission matrix

Create:

```txt
data/audits/phygn_status_permission_matrix_v4_4_1.json
```

Fields:

```txt
status
canonical_permission
evidence_level
support_level
risk_level
allowed_claims
blocked_claims
required_next_gate
compatible_previous_statuses
incompatible_statuses
```

---

## 4. Claim leakage report

Create:

```txt
data/audits/phygn_claim_leakage_report_v4_4_1.json
```

Fields:

```txt
artifact_path
claim_text
claim_type
required_permission
actual_permission
leakage_status
severity
recommended_rewrite
```

Leakage statuses:

```txt
NO_LEAK
OVERCLAIM
AMBIGUOUS
BLOCKED_CLAIM_PRESENT
PERMISSION_NOT_TRACEABLE
```

---

## 5. Test logic audit

Create:

```txt
data/audits/phygn_test_logic_audit_v4_4_1.json
```

Fields:

```txt
test_file
test_name
tested_invariant
positive_fixture_present
negative_fixture_present
contradiction_fixture_present
debt_bypass_fixture_present
tautology_risk
coverage_gap
recommended_test
```

---

## 6. Debt boundary audit

Create:

```txt
data/audits/phygn_debt_boundary_audit_v4_4_1.json
```

Fields:

```txt
debt_id
status
blocking_claims
allowed_work
artifacts_checked
bypass_found
bypass_locations
required_fixes
```

---

## 7. Metric integrity audit

Create:

```txt
data/audits/phygn_metric_integrity_audit_v4_4_1.json
```

Fields:

```txt
metric_name
artifact_path
metric_type
required_inputs
actual_inputs
integrity_status
misuse_risk
recommended_fix
```

Metric types:

```txt
SYNTHETIC
SOURCE_PRESSURE
BENCHMARK_ALIGNMENT
MODEL_COMPARISON
YTRUE
PREDICTIVE_GAIN
```

---

## 8. Remediation plan

Create:

```txt
data/audits/phygn_remediation_plan_v4_4_1.json
```

Each remediation item:

```txt
remediation_id
linked_issue_id
severity
fix_type
target_file_or_module
required_change
required_test
blocks_next_gate
```

---

## 9. Final principle

```txt
The audit output must be machine-readable enough to block automation.
```
