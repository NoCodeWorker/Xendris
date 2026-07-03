# Phygn v2.0 — Campaign, Report & Test Orchestration Audit

## 0. Purpose

Phygn campaigns produce reports and tests across many domains.

v2.0 must ensure that every campaign follows a comparable orchestration pattern.

---

## 1. Campaign audit

For every campaign runner, record:

```txt
campaign_id
input schemas
output schemas
reports generated
gatekeepers called
tests covering it
expected baseline count
failure behavior
CLI or programmatic entrypoint
```

---

## 2. Campaign contract

Each campaign should ideally produce:

```python
class CampaignResult(BaseModel):
    campaign_id: str
    version: str
    status: str
    inputs: dict
    outputs: dict
    reports: list[str]
    gate_results: list[dict]
    warnings: list[str]
    blocked_claims: list[str]
    next_actions: list[str]
```

---

## 3. Report audit

For every report:

```txt
Where is it written?
Which function writes it?
Which schema feeds it?
Does it include status?
Does it include blocked claims?
Does it include next actions?
Does it distinguish synthetic from predictive?
Does it include source support level?
Does it include generated timestamp?
```

---

## 4. Report contract proposal

Common sections:

```txt
Title
Date
Campaign ID
Inputs
Core Results
Gate Results
Allowed Claims
Blocked Claims
Failure Conditions
Reports Generated
Tests
Next Actions
Discipline Note
```

Domain-specific sections are allowed.

---

## 5. Test architecture audit

For tests, audit:

```txt
test count by module
contract tests vs implementation tests
regression tests for previous versions
campaign end-to-end tests
report existence tests
status canonicalization tests
negative tests
```

---

## 6. Required new meta-tests

v2.0 should add meta-tests if safe:

```txt
test_all_campaign_reports_include_blocked_claims_section
test_all_gate_results_have_permission_fields
test_no_core_imports_domain_modules
test_status_strings_are_declared_in_enums_or_registry
test_campaigns_return_or_write_expected_reports
```

If too invasive, generate audit warnings instead.

---

## 7. Final principle

```txt
A system that audits claims must also audit its own reporting chain.
```
