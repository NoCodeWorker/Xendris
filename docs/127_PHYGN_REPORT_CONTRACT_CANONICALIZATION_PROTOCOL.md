# Phygn v2.1 — Report Contract Canonicalization Protocol

## 0. Purpose

v2.0 found that reports exist across many domains but their sections are uneven.

v2.1 should add canonical report helpers without rewriting all historical reports.

---

## 1. Common report sections

New reports should include where possible:

```txt
Title
Date
Campaign ID
Input Summary
Core Results
Domain Status
Canonical Permission
Blocked Reasons
Evidence Level
Support Level
Risk Level
Allowed Claims / Uses
Blocked Claims / Uses
Failure Conditions
Tests
Reports Generated
Next Actions
Discipline Note
```

---

## 2. ReportContract model

```python
class CanonicalReportContract(BaseModel):
    title: str
    date: str
    campaign_id: str | None
    domain_status: str
    canonical_permission: str
    blocked_reasons: list[str]
    evidence_level: str
    support_level: str
    risk_level: str | None
    allowed_uses: list[str]
    blocked_uses: list[str]
    failure_conditions: list[str]
    tests_summary: str | None
    reports_generated: list[str]
    next_actions: list[str]
    discipline_note: str
```

---

## 3. Helper functions

Implement:

```python
build_report_contract(...)
```

```python
render_canonical_report_section(contract: CanonicalReportContract) -> str
```

```python
append_canonical_status_section(markdown: str, contract: CanonicalReportContract) -> str
```

---

## 4. Progressive adoption

Do not rewrite every historical report in v2.1.

Instead:

```txt
new reports include canonical sections
selected active reports may append canonical status sections
historical reports remain unchanged
audit warnings track missing canonical sections
```

---

## 5. Snapshot/contract tests

Add tests ensuring that:

```txt
canonical report section contains domain status
canonical report section contains canonical permission
canonical report section contains blocked reasons
unknown status is marked review required
```

---

## 6. Report safety

Reports must not make stronger claims than the gate result permits.

If canonical permission is:

```txt
CLAIM_BLOCKED
```

the report must include blocked claims or blocked uses.

---

## 7. Final principle

```txt
Reports are not documentation after the fact.
Reports are part of the epistemic chain of custody.
```
