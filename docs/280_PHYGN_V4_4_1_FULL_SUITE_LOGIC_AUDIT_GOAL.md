# Phygn v4.4.1 — Full Suite Logic Audit & Epistemic Consistency Review Goal

## 0. Context

The latest generated document is:

```txt
docs/279_PHYGN_CODEX_V4_4_MANUAL_DATA_EXTRACTION_PROMPT.md
```

Therefore, v4.4.1 starts at:

```txt
280
```

v4.4 was prepared as:

```txt
Phygn v4.4 — Manual Data Extraction Sprint
```

Before continuing with v4.4 execution results or v4.5, the full suite logic must be audited.

---

## 1. Core thesis

```txt
A passing test suite can still protect a false logic.
Audit the permissions, not only the code.
```

The goal is not to increase test count.

The goal is to detect whether the suite permits epistemic laundering.

---

## 2. Scope

Audit the complete Phygn pipeline from:

```txt
v0.5 Boundary Atlas / CAMPAIGN-001
```

through:

```txt
v4.4 Manual Data Extraction Sprint
```

including:

```txt
status mapping
claim permission gates
source ingestion
extract validation
semantic triage
source pressure
scientific debt
benchmark construction
model comparison
observable normalization
y_true extraction
manual data extraction
tests and reports
```

---

## 3. Hard rule

```txt
No claim may inherit permission from an upstream artifact unless the permission path is explicit.
No benchmark score may become PredictiveGain.
No source pressure may become experimental validation.
No y_true plan may become y_true.
No accepted extraction may bypass provenance.
No SLOT_4 debt may be weakened by benchmark progress.
```

---

## 4. Audit objectives

Identify:

```txt
logical contradictions
status mapping inconsistencies
claim-permission leaks
test tautologies
overbroad allowed claims
silent debt bypasses
unsupported positive states
unreachable negative states
ambiguous canonical permissions
stale artifacts
misnamed files or misleading statuses
metric misuse
PredictiveGain misuse
source-support misuse
benchmark-support misuse
y_true misuse
SLOT_4 debt leakage
```

---

## 5. Inputs

Audit these areas:

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

## 6. Required outputs

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

## 7. Statuses

Add conservative statuses:

```txt
PHYGN_FULL_SUITE_LOGIC_AUDIT_COMPLETED
PHYGN_FULL_SUITE_LOGIC_AUDIT_PARTIAL
PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_BLOCKING_ISSUES
PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_NONBLOCKING_ISSUES
PHYGN_FULL_SUITE_LOGIC_AUDIT_BLOCKED_MISSING_ARTIFACTS
PHYGN_FULL_SUITE_LOGIC_AUDIT_REQUIRES_REMEDIATION
```

Expected active status depends on findings.

Do not force a clean result.

---

## 8. Severity levels

Use:

```txt
BLOCKER
HIGH
MEDIUM
LOW
INFO
```

Definitions:

```txt
BLOCKER:
  permits false scientific claim, false PredictiveGain, false validation or debt bypass

HIGH:
  could mislead roadmap or reporting but does not directly permit false validation

MEDIUM:
  inconsistency that may cause stale artifacts, wrong next gate or ambiguous status

LOW:
  naming/reporting/test clarity issue

INFO:
  observation or hardening recommendation
```

---

## 9. Acceptance criteria

v4.4.1 is complete when:

```txt
full suite logic traversed
status-permission matrix generated
claim leakage scan performed
test logic audit performed
debt boundary audit performed
metric integrity audit performed
remediation plan generated
reports generated
tests pass
audit is allowed to fail the suite logically
```

---

## 10. Final principle

```txt
The audit must be more loyal to truth than to continuity.
```
