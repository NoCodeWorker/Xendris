# Phygn v4.4.2 — Audit Remediation & Status/Test Hardening Sprint Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
```

Therefore, v4.4.2 starts at:

```txt
286
```

v4.4.1 produced:

```txt
PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_NONBLOCKING_ISSUES
blocker_count = 0
nonblocking_issue_count = 255
unmapped_status_count = 160
status_only_test_issue_count = 95
can_continue_pipeline = True
remediation_gate = CONDITIONAL_CONTINUE_AFTER_REVIEW
```

v4.4.2 must not continue the scientific pipeline by ignoring this debt.

It must classify, remediate, reduce, or explicitly accept audit debt.

---

## 1. Core thesis

```txt
Do not grow the pipeline over unmapped permissions.
```

A nonblocking issue is still debt.

Debt may continue only if it is:

```txt
named
bounded
assigned
tested
accepted or remediated
```

---

## 2. Mission

Implement:

```txt
v4.4.2 — Audit Remediation & Status/Test Hardening Sprint
```

The sprint targets:

```txt
160 unmapped statuses
95 status-only tests
255 nonblocking audit issues
```

Priority:

```txt
1. status mapping hardening
2. status-only test hardening
3. claim leakage ambiguity reduction
4. metric integrity warnings
5. stale artifact/count mismatch handling
6. accepted residual audit debt register
```

---

## 3. Hard rule

```txt
A status without a permission mapping cannot govern a claim.
A test that cannot fail the claim is not a scientific test.
A nonblocking issue cannot disappear because it is inconvenient.
```

---

## 4. Required behavior

v4.4.2 must:

```txt
load v4.4.1 audit artifacts
classify all nonblocking issues
map or quarantine unmapped statuses
identify status-only tests
add negative/debt-bypass/contradiction fixtures where appropriate
create accepted residual debt register
create remediation summary
compute post-remediation audit deltas
generate reports
```

---

## 5. Inputs

Load:

```txt
data/audits/phygn_full_suite_logic_audit_v4_4_1.json
data/audits/phygn_status_permission_matrix_v4_4_1.json
data/audits/phygn_claim_leakage_report_v4_4_1.json
data/audits/phygn_test_logic_audit_v4_4_1.json
data/audits/phygn_debt_boundary_audit_v4_4_1.json
data/audits/phygn_metric_integrity_audit_v4_4_1.json
data/audits/phygn_remediation_plan_v4_4_1.json
```

Inspect:

```txt
phyng/core/status_mapping.py
phyng/core/support_levels.py
tests/
reports/
docs/
data/
```

If v4.4.1 artifacts are missing:

```txt
PHYGN_AUDIT_REMEDIATION_BLOCKED_MISSING_AUDIT
```

---

## 6. Outputs

Create:

```txt
data/audits/remediation/phygn_status_mapping_remediation_v4_4_2.json
data/audits/remediation/phygn_status_quarantine_register_v4_4_2.json
data/audits/remediation/phygn_test_hardening_plan_v4_4_2.json
data/audits/remediation/phygn_test_hardening_results_v4_4_2.json
data/audits/remediation/phygn_claim_leakage_remediation_v4_4_2.json
data/audits/remediation/phygn_metric_integrity_remediation_v4_4_2.json
data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json
data/audits/remediation/phygn_post_remediation_audit_delta_v4_4_2.json
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
```

---

## 7. Statuses

Add:

```txt
PHYGN_AUDIT_REMEDIATION_COMPLETED
PHYGN_AUDIT_REMEDIATION_PARTIAL
PHYGN_AUDIT_REMEDIATION_REQUIRES_MORE_HARDENING
PHYGN_AUDIT_REMEDIATION_BLOCKED_MISSING_AUDIT
PHYGN_AUDIT_REMEDIATION_BLOCKED_UNRESOLVED_PERMISSIONS
PHYGN_AUDIT_REMEDIATION_READY_TO_RESUME_PIPELINE
```

Expected conservative status:

```txt
PHYGN_AUDIT_REMEDIATION_PARTIAL
```

unless deltas are strong enough to resume.

---

## 8. Continuation gate

The pipeline may resume only if:

```txt
blocker_count = 0
critical_unmapped_status_count = 0
open_claim_leakage_blocker_count = 0
accepted_residual_debt has explicit owner/category/risk/next_review
```

Recommended gate result values:

```txt
RESUME_ALLOWED
RESUME_ALLOWED_WITH_RESIDUAL_DEBT
RESUME_BLOCKED_PENDING_STATUS_MAPPING
RESUME_BLOCKED_PENDING_TEST_HARDENING
RESUME_BLOCKED_PENDING_CLAIM_LEAKAGE_FIX
```

---

## 9. Acceptance criteria

v4.4.2 is complete when:

```txt
v4.4.1 audit artifacts loaded
unmapped statuses classified
critical statuses mapped or quarantined
status-only tests classified
test hardening plan created
claim leakage issues remediated or accepted
metric integrity issues remediated or accepted
accepted residual debt register created
post-remediation delta computed
continuation gate generated
reports generated
tests pass
no physical claim upgraded
no y_true created
no PredictiveGain created
SLOT_4 debt remains open
```

---

## 10. Final principle

```txt
Remediation is not cosmetic cleanup.
It is permission infrastructure.
```
