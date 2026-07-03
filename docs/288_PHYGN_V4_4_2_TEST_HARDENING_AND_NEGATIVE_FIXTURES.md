# Phygn v4.4.2 — Test Hardening & Negative Fixtures

## 0. Purpose

This document defines how to reduce `status_only_test_issue_count = 95`.

---

## 1. Test hardening plan

Create:

```txt
data/audits/remediation/phygn_test_hardening_plan_v4_4_2.json
```

Schema:

```python
class TestHardeningPlanItem(BaseModel):
    test_file: str
    test_name: str
    issue_type: str
    current_weakness: str
    required_negative_fixture: str
    required_assertion_upgrade: str
    priority: str
    remediation_status: str
```

---

## 2. Test hardening results

Create:

```txt
data/audits/remediation/phygn_test_hardening_results_v4_4_2.json
```

Fields:

```txt
initial_status_only_count
hardened_test_count
remaining_status_only_count
negative_fixture_count_added
contradiction_fixture_count_added
debt_bypass_fixture_count_added
metric_misuse_fixture_count_added
recommendations
```

---

## 3. Weak tests to flag

Flag tests that only assert:

```txt
status == EXPECTED_STATUS
file exists
count > 0
report contains heading
function returns object
```

without checking:

```txt
blocked claims
permission propagation
negative fixture behavior
debt bypass
metric misuse
y_true provenance failure
PredictiveGain failure without y_true
source-pressure failure without validation-ready extracts
```

---

## 4. Required hardening fixture classes

Add fixture classes:

```txt
claim_leakage_fixture
predictive_gain_without_ytrue_fixture
slot4_bypass_fixture
source_pressure_without_extract_fixture
benchmark_score_as_predictive_gain_fixture
ytrue_without_provenance_fixture
negative_control_no_claim_impact_fixture
stale_artifact_count_mismatch_fixture
```

---

## 5. Priority targets

Prioritize tests around:

```txt
status_mapping
claim_permission
source_pressure_decision
scientific_debt
model_comparison
observable_dataset
ytrue_extraction
manual_data_extraction
full_suite_logic_audit
```

---

## 6. Minimum upgraded assertions

Every critical pipeline test should include at least one assertion that a false claim remains blocked.

Examples:

```python
assert "PHI_GRADIENT is validated" in blocked_claims
assert predictive_gain is None
assert gradient_mechanism_claim_permission == "BLOCKED_BY_SLOT4_DEBT"
assert ready_for_predictive_gain is False when accepted_y_true_count < 3
```

---

## 7. Final principle

```txt
A test must protect a boundary, not merely confirm a ceremony.
```
