# Codex Prompt — Phygn v4.4.1 Full Suite Logic Audit & Epistemic Consistency Review

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current latest generated document:

```txt
docs/279_PHYGN_CODEX_V4_4_MANUAL_DATA_EXTRACTION_PROMPT.md
```

Therefore v4.4.1 starts at:

```txt
280
```

---

# 1. Read first

Read these v4.4.1 specs:

```txt
docs/280_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_docs/status/GOAL.md
docs/281_PHYGN_V4_4_1_AUDIT_RULES_AND_INVARIANTS.md
docs/282_PHYGN_V4_4_1_AUDIT_OUTPUT_SCHEMAS.md
docs/283_PHYGN_V4_4_1_REPORTING_AND_REMEDIATION_GATE.md
```

Also read the latest result docs if present:

```txt
docs/274_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_RESULTS.md
docs/268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
docs/262_PHYGN_V4_1_DEBT_BOUNDED_MODEL_COMPARISON_RESULTS.md
docs/256_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_RESULTS.md
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
docs/244_PHYGN_V3_8_3_PRIORITY_PACKET_REVIEW_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v4.4.1 — Full Suite Logic Audit & Epistemic Consistency Review
```

Audit the logic of the entire suite.

Do not merely run pytest.

Do not assume passing tests imply correct epistemic logic.

---

# 3. Audit scope

Inspect:

```txt
docs/
reports/
data/
tests/
phyng/core/
phyng/source_pressure/
phyng/real_source_ingestion/
phyng/exact_extract_review/
phyng/priority_exact_fill/
phyng/pdf_text_extraction/
phyng/extract_candidate_review/
phyng/semantic_triage/
phyng/priority_packet_review/
phyng/source_pressure_decision/
phyng/benchmark_construction/
phyng/scientific_debt/
phyng/model_comparison/
phyng/observable_dataset/
phyng/ytrue_extraction/
phyng/manual_data_extraction/
phyng/campaigns/
```

---

# 4. Create package

Create:

```txt
phyng/full_suite_logic_audit/
  __init__.py
  schemas.py
  artifact_scanner.py
  status_permission_audit.py
  claim_leakage_scanner.py
  test_logic_audit.py
  debt_boundary_audit.py
  metric_integrity_audit.py
  remediation.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phygn_full_suite_logic_audit.py
```

Entrypoint:

```python
run_phygn_full_suite_logic_audit_campaign(root: str | Path = ".")
```

---

# 5. Required audits

Perform:

```txt
status-permission matrix audit
claim leakage scan
test logic audit
SLOT_4 debt boundary audit
PredictiveGain metric integrity audit
y_true integrity audit
source-support integrity audit
negative-control integrity audit
stale artifact audit
```

---

# 6. Blocking conditions

Mark as BLOCKER if any artifact:

```txt
claims PHI_GRADIENT is validated
claims PredictiveGain exists without y_true
claims gradient mechanism support while SLOT_4 debt is open
treats source pressure as experimental proof
treats benchmark score as predictive truth
treats extraction candidate as source support
admits y_true without provenance
```

---

# 7. Required outputs

Create:

```txt
data/audits/phygn_full_suite_logic_audit_v4_4_1.json
data/audits/phygn_status_permission_matrix_v4_4_1.json
data/audits/phygn_claim_leakage_report_v4_4_1.json
data/audits/phygn_test_logic_audit_v4_4_1.json
data/audits/phygn_debt_boundary_audit_v4_4_1.json
data/audits/phygn_metric_integrity_audit_v4_4_1.json
data/audits/phygn_remediation_plan_v4_4_1.json
```

---

# 8. Reports

Generate:

```txt
reports/audits/phygn_full_suite_logic_audit_v4_4_1.md
reports/audits/phygn_status_permission_matrix_v4_4_1.md
reports/audits/phygn_claim_leakage_report_v4_4_1.md
reports/audits/phygn_test_logic_audit_v4_4_1.md
reports/audits/phygn_debt_boundary_audit_v4_4_1.md
reports/audits/phygn_metric_integrity_audit_v4_4_1.md
reports/audits/phygn_remediation_plan_v4_4_1.md
reports/campaigns/PHYGN-FULL-SUITE-LOGIC-AUDIT-v4_4_1.md
```

---

# 9. Statuses

Add:

```txt
PHYGN_FULL_SUITE_LOGIC_AUDIT_COMPLETED
PHYGN_FULL_SUITE_LOGIC_AUDIT_PARTIAL
PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_BLOCKING_ISSUES
PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_NONBLOCKING_ISSUES
PHYGN_FULL_SUITE_LOGIC_AUDIT_BLOCKED_MISSING_ARTIFACTS
PHYGN_FULL_SUITE_LOGIC_AUDIT_REQUIRES_REMEDIATION
```

---

# 10. Tests

Create:

```txt
tests/test_full_suite_logic_audit_scanner_v4_4_1.py
tests/test_status_permission_audit_v4_4_1.py
tests/test_claim_leakage_scanner_v4_4_1.py
tests/test_test_logic_audit_v4_4_1.py
tests/test_debt_boundary_audit_v4_4_1.py
tests/test_metric_integrity_audit_v4_4_1.py
tests/test_phygn_full_suite_logic_audit_campaign_v4_4_1.py
```

Minimum tests:

```txt
test_claim_leakage_detects_predictive_gain_without_ytrue
test_claim_leakage_detects_gradient_support_with_open_slot4_debt
test_metric_audit_blocks_benchmark_score_as_predictive_gain
test_ytrue_audit_blocks_value_without_provenance
test_debt_boundary_detects_slot4_bypass
test_negative_control_audit_requires_claim_impact
test_test_logic_audit_flags_status_only_test
test_status_permission_matrix_has_no_unmapped_statuses
test_remediation_plan_created_for_blockers
test_clean_fixture_can_continue_pipeline
test_blocker_fixture_stops_pipeline
```

---

# 11. Do not overclaim

Do not write:

```txt
Tests passed, therefore science is valid.
Audit passed, therefore PHI_GRADIENT is valid.
Audit resolves SLOT_4 debt.
Audit creates y_true.
Audit creates PredictiveGain.
```

Allowed:

```txt
A full suite logic audit was performed.
The audit found blocking/nonblocking issues.
The pipeline may continue only according to the remediation gate.
```

---

# 12. Acceptance criteria

Complete when:

```txt
audit package created
audit campaign created
audit tests pass
all required audit artifacts generated
all required reports generated
pipeline continuation gate computed
BLOCKER issues stop continuation
reports include canonical status
```

---

# 13. Final discipline

```txt
The audit must be more loyal to truth than to continuity.
```
