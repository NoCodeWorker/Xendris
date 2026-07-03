# Phygn v4.0 — SLOT_4 Debt Object & Resolution Plan

## 0. Purpose

This document formalizes the unresolved gradient-component gap as a claim-blocking debt.

---

## 1. Debt object

Create:

```txt
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Schema:

```python
class ScientificDebtObject(BaseModel):
    debt_id: str
    title: str
    status: str
    severity: str
    opened_by: str
    source_pressure_ref: str
    blocks: list[str]
    does_not_block: list[str]
    evidence_gap: str
    current_findings: list[str]
    resolution_conditions: list[str]
    prohibited_claims: list[str]
    allowed_work: list[str]
    review_frequency: str
    notes: list[str]
```

Recommended values:

```txt
debt_id = DEBT-SLOT4-GRADIENT-COMPONENT-GAP
status = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
severity = HIGH
opened_by = v3.9 source pressure decision
```

---

## 2. Resolution conditions

The debt may close only if one of these occurs:

```txt
1. New validation-ready SLOT_4 extracts are found and v3.9-style gate grants pressure.
2. Existing Pedernales manual review yields clean SLOT_4 extract and source-pressure gate upgrades status.
3. Source pressure contradicts SLOT_4 and PHI_GRADIENT pivots away from gradient mechanism.
4. PHI_GRADIENT is redefined explicitly as benchmark/observable model without gradient-mechanism claim.
```

---

## 3. Prohibited claims while open

```txt
PHI_GRADIENT is source-backed as a gradient mechanism.
Pedernales supports the gradient component.
Gradient-transition-effective dynamics are literature-backed.
Frontera C is empirically validated.
The invariant has empirical confirmation.
```

---

## 4. Allowed work while open

```txt
benchmark construction
observable alignment
baseline model comparison
negative-control design
SLOT_4 source acquisition
Pedernales manual review
candidate revision
kill/pivot analysis
```

---

## 5. SLOT_4 resolution plan

Create:

```txt
data/debts/slot4_resolution_plan_v4_0.json
```

Plan tasks:

```txt
manual review of Pedernales SLOT_4 queue
targeted source search for gradient/transition/effective dynamics
extract exact equations/passages from candidate SLOT_4 sources
run v3.8.3-style promotion on new SLOT_4 extracts
rerun source pressure decision
decide keep/revise/kill gradient mechanism
```

---

## 6. Resolution statuses

```txt
SLOT4_DEBT_OPEN
SLOT4_DEBT_UNDER_REVIEW
SLOT4_DEBT_PARTIALLY_RESOLVED
SLOT4_DEBT_RESOLVED_AS_SUPPORTED
SLOT4_DEBT_RESOLVED_AS_CONTRADICTED
SLOT4_DEBT_RESOLVED_BY_PIVOT
```

---

## 7. Final principle

```txt
Scientific debt is not shameful.
Untracked scientific debt is fatal.
```
