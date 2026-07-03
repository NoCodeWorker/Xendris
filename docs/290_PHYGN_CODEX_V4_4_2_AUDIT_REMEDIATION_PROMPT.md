# Codex Prompt — Phygn v4.4.2 Audit Remediation & Status/Test Hardening Sprint

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current latest result document:

```txt
docs/285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
```

Therefore v4.4.2 starts at:

```txt
286
```

---

# 1. Read first

Read these v4.4.2 specs:

```txt
docs/286_PHYGN_V4_4_2_AUDIT_REMEDIATION_docs/status/GOAL.md
docs/287_PHYGN_V4_4_2_STATUS_MAPPING_AND_QUARANTINE_PROTOCOL.md
docs/288_PHYGN_V4_4_2_TEST_HARDENING_AND_NEGATIVE_FIXTURES.md
docs/289_PHYGN_V4_4_2_CLAIM_METRIC_DEBT_REMEDIATION.md
```

Also read:

```txt
docs/285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
```

---

# 2. First action

Run focused audit validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_full_suite_logic_audit_scanner_v4_4_1.py tests/test_status_permission_audit_v4_4_1.py tests/test_claim_leakage_scanner_v4_4_1.py tests/test_test_logic_audit_v4_4_1.py tests/test_debt_boundary_audit_v4_4_1.py tests/test_metric_integrity_audit_v4_4_1.py tests/test_phygn_full_suite_logic_audit_campaign_v4_4_1.py
```

Expected recent result:

```txt
19 passed
```

---

# 3. Mission

Implement:

```txt
v4.4.2 — Audit Remediation & Status/Test Hardening Sprint
```

Do not proceed to scientific acquisition.

Do not create y_true.

Do not create PredictiveGain.

Do not close SLOT_4 debt.

---

# 4. Load v4.4.1 audit artifacts

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

If missing:

```txt
PHYGN_AUDIT_REMEDIATION_BLOCKED_MISSING_AUDIT
```

---

# 5. Create package

Create:

```txt
phyng/audit_remediation/
  __init__.py
  schemas.py
  loader.py
  status_remediation.py
  status_quarantine.py
  test_hardening.py
  claim_remediation.py
  metric_remediation.py
  residual_debt.py
  delta.py
  continuation_gate.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phygn_audit_remediation.py
```

Entrypoint:

```python
run_phygn_audit_remediation_campaign(root: str | Path = ".")
```

---

# 6. Status remediation

Classify all unmapped statuses.

For critical statuses, do one of:

```txt
map
deprecated
quarantine
```

No critical status may remain silently unmapped.

Generate:

```txt
data/audits/remediation/phygn_status_mapping_remediation_v4_4_2.json
data/audits/remediation/phygn_status_quarantine_register_v4_4_2.json
```

Update status mapping only when safe and conservative.

---

# 7. Test hardening

Use audit output to classify weak tests.

Do not need to fix all 95 in one sprint, but must create:

```txt
plan
results
negative fixture strategy
remaining risk summary
```

Where possible, add tests for:

```txt
PredictiveGain without y_true must fail
SLOT_4 debt bypass must fail
benchmark score as PredictiveGain must fail
y_true without provenance must fail
status-only tests should be flagged
```

---

# 8. Claim and metric remediation

Generate:

```txt
data/audits/remediation/phygn_claim_leakage_remediation_v4_4_2.json
data/audits/remediation/phygn_metric_integrity_remediation_v4_4_2.json
```

Ensure:

```txt
BenchmarkComparisonScore != PredictiveGain
SyntheticGain != PredictiveGain
SourcePressureScore != validation
ObservableAlignmentScore != observed truth
```

---

# 9. Accepted residual debt

Generate:

```txt
data/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.json
```

Every accepted debt item needs:

```txt
category
severity
reason accepted
owner
next_review_phase
may_continue_pipeline
blocked claims
does_not_block
```

---

# 10. Delta and continuation gate

Generate:

```txt
data/audits/remediation/phygn_post_remediation_audit_delta_v4_4_2.json
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
```

Continuation may only be:

```txt
RESUME_ALLOWED
RESUME_ALLOWED_WITH_RESIDUAL_DEBT
RESUME_BLOCKED_PENDING_STATUS_MAPPING
RESUME_BLOCKED_PENDING_TEST_HARDENING
RESUME_BLOCKED_PENDING_CLAIM_LEAKAGE_FIX
```

---

# 11. Reports

Generate:

```txt
reports/audits/remediation/phygn_status_mapping_remediation_v4_4_2.md
reports/audits/remediation/phygn_status_quarantine_register_v4_4_2.md
reports/audits/remediation/phygn_test_hardening_plan_v4_4_2.md
reports/audits/remediation/phygn_test_hardening_results_v4_4_2.md
reports/audits/remediation/phygn_claim_leakage_remediation_v4_4_2.md
reports/audits/remediation/phygn_metric_integrity_remediation_v4_4_2.md
reports/audits/remediation/phygn_accepted_residual_audit_debt_v4_4_2.md
reports/audits/remediation/phygn_post_remediation_audit_delta_v4_4_2.md
reports/audits/remediation/phygn_v4_4_2_continuation_gate.md
reports/campaigns/PHYGN-AUDIT-REMEDIATION-v4_4_2.md
```

---

# 12. Statuses

Add mappings:

```txt
PHYGN_AUDIT_REMEDIATION_COMPLETED
PHYGN_AUDIT_REMEDIATION_PARTIAL
PHYGN_AUDIT_REMEDIATION_REQUIRES_MORE_HARDENING
PHYGN_AUDIT_REMEDIATION_BLOCKED_MISSING_AUDIT
PHYGN_AUDIT_REMEDIATION_BLOCKED_UNRESOLVED_PERMISSIONS
PHYGN_AUDIT_REMEDIATION_READY_TO_RESUME_PIPELINE
```

---

# 13. Tests

Create:

```txt
tests/test_audit_remediation_loader_v4_4_2.py
tests/test_status_remediation_v4_4_2.py
tests/test_status_quarantine_v4_4_2.py
tests/test_test_hardening_v4_4_2.py
tests/test_claim_metric_remediation_v4_4_2.py
tests/test_residual_debt_v4_4_2.py
tests/test_audit_remediation_continuation_gate_v4_4_2.py
tests/test_phygn_audit_remediation_campaign_v4_4_2.py
```

Minimum tests:

```txt
test_missing_audit_blocks_remediation
test_critical_unmapped_status_cannot_unlock_claim
test_quarantined_status_cannot_gate_claim
test_deprecated_status_cannot_be_active_campaign_status
test_status_hardening_reduces_or_classifies_unmapped_statuses
test_status_only_tests_are_classified
test_predictive_gain_metric_labels_remain_distinct
test_benchmark_score_not_labeled_predictive_gain
test_accepted_residual_debt_requires_next_review
test_continuation_gate_blocks_critical_unmapped_statuses
test_continuation_gate_allows_residual_debt_when_bounded
test_no_ytrue_created
test_no_predictive_gain_created
test_slot4_debt_remains_open
```

---

# 14. Behavior preservation

Do not alter:

```txt
v4.4 manual extraction results
v4.3 y_true extraction
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure
historical reports
```

Only harden mappings, tests and remediation artifacts.

---

# 15. Do not overclaim

Do not write:

```txt
Remediation validates PHI_GRADIENT.
Remediation creates y_true.
Remediation creates PredictiveGain.
Remediation closes SLOT_4 debt.
All debt is gone unless proven by delta.
```

Allowed:

```txt
Audit remediation was performed.
Some statuses were mapped, quarantined, deprecated or accepted as residual debt.
Some tests were hardened or flagged for future hardening.
Pipeline continuation was computed by gate.
```

---

# 16. Acceptance criteria

Complete when:

```txt
v4.4.1 audit artifacts loaded
v4.4.2 tests pass
status mapping remediation generated
status quarantine generated
test hardening plan/results generated
claim/metric remediation generated
accepted residual debt register generated
post-remediation delta generated
continuation gate generated
reports generated
no y_true created
no PredictiveGain created
SLOT_4 debt remains open
```

---

# 17. Final discipline

```txt
Remediation is permission infrastructure.
```
