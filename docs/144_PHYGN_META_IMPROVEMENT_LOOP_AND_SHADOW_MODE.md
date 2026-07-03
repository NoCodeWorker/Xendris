# Phygn v2.4 — Meta-Improvement Loop & Shadow Mode

## 0. Purpose

This document defines the inner loop that proposes improvements to Phygn itself.

The meta-loop is useful but dangerous.

It must never allow the system to self-authorize critical changes.

---

## 1. Meta-loop states

```txt
META_OBSERVATION_RECORDED
META_CHANGE_PROPOSED
META_CHANGE_RISK_CLASSIFIED
META_CHANGE_SHADOW_TESTING
META_CHANGE_BENCHMARKED
META_CHANGE_APPROVED_LOW_RISK
META_CHANGE_REQUIRES_HUMAN_REVIEW
META_CHANGE_BLOCKED_REGRESSION
META_CHANGE_REJECTED
META_CHANGE_APPLIED_VERSIONED
META_CHANGE_ROLLED_BACK
```

---

## 2. Meta-change types

```txt
HEURISTIC_WEIGHT_CHANGE
QUESTION_PRIORITY_CHANGE
REPORT_TEMPLATE_CHANGE
WARNING_TEMPLATE_CHANGE
MODEL_ROUTING_CHANGE
CANONICAL_MAPPING_ADDITION
CANONICAL_MAPPING_CHANGE
GATE_THRESHOLD_CHANGE
CLAIM_PERMISSION_CHANGE
SOURCE_REQUIREMENT_CHANGE
BENCHMARK_REQUIREMENT_CHANGE
FINANCIAL_GATE_CHANGE
EXECUTION_GATE_CHANGE
```

---

## 3. Risk classification

Low risk:

```txt
warning template update
report wording update
question priority update
heuristic weight change within bounded range
new mapping for unknown status to REVIEW_REQUIRED
```

Medium risk:

```txt
canonical mapping addition for known domain status
model routing change for low-risk ideation
benchmark design heuristic change
```

High risk:

```txt
canonical permission change
blocked reason semantic change
source requirement change
benchmark requirement change
claim gate change
financial action gate change
execution gate change
```

---

## 4. Shadow mode

Every medium/high risk change must run in shadow mode.

Shadow mode means:

```txt
new rule runs alongside current rule
current rule remains authoritative
differences are logged
regression suite is run
impact report is generated
no user-facing permission changes occur
```

---

## 5. Auto-approval policy

Allowed for low-risk changes only if:

```txt
tests pass
no critical output changes
no permission elevation
rollback record exists
versioned config exists
```

Never auto-approve:

```txt
claim permission changes
financial action changes
execution changes
source/benchmark requirement reductions
canonical permission semantic changes
```

---

## 6. MetaChangeProposal schema

```python
class MetaChangeProposal(BaseModel):
    proposal_id: str
    change_type: str
    description: str
    affected_modules: list[str]
    current_behavior: str
    proposed_behavior: str
    risk_level: str
    requires_shadow_mode: bool
    requires_human_review: bool
    expected_behavior_change: bool
    canonical_status: CanonicalStatusRecord
```

---

## 7. Final principle

```txt
Self-improvement must run in shadow mode before it touches authority.
```
