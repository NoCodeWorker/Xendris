# Phygn v2.0 — Module Boundaries & Refactor Map

## 0. Purpose

This document defines how to audit module boundaries and produce a safe refactor map.

The goal is not cosmetic cleanup.

The goal is to prevent architectural drift.

---

## 1. Current module families

Audit at minimum:

```txt
phyng/campaigns/
phyng/boundary_atlas/
phyng/model_comparison/
phyng/evidence/
phyng/source_audit/
phyng/candidates/
phyng/epistemic_modes/
phyng/ux/
phyng/prediction_accuracy/
phyng/model_runtime/
phyng/copilot/
phyng/business_validation/
```

Actual module names must be discovered from the repository.

---

## 2. Boundary questions

For each module:

```txt
What is its responsibility?
What does it import?
What imports it?
What schemas does it define?
What reports does it generate?
What tests cover it?
Does it duplicate logic from another module?
Should it depend on core?
Should it be domain-specific?
```

---

## 3. Dependency audit

Produce:

```txt
dependency graph
import direction map
cycle detection
high coupling warnings
shared schema candidates
domain boundary violations
```

Hard rule:

```txt
domain modules may depend on core;
core must not depend on domain modules.
```

---

## 4. Refactor categories

Each recommendation must be classified:

```txt
NO_CHANGE
DOCUMENT_ONLY
LOW_RISK_EXTRACT_CONSTANTS
LOW_RISK_EXTRACT_ENUM
MEDIUM_RISK_SCHEMA_UNIFICATION
MEDIUM_RISK_REPORT_CONTRACT_UNIFICATION
HIGH_RISK_MODULE_MOVE
HIGH_RISK_PUBLIC_API_CHANGE
BLOCKED_NEEDS_HUMAN_REVIEW
```

---

## 5. Refactor order

Recommended order:

```txt
1. document current architecture
2. canonicalize naming tables
3. extract shared enums/constants only when duplicates are proven
4. add compatibility aliases
5. update reports to use canonical labels
6. update tests around public contracts
7. remove duplicate logic only after behavior parity tests
```

---

## 6. Behavior preservation

v2.0 must not silently change:

```txt
gate decisions
candidate survival results
detectability results
business validation outcomes
financial action blocks
truth boundary statuses
prediction ledger metrics
```

All changes must be behavior-preserving unless explicitly marked.

---

## 7. Final principle

```txt
Refactor is allowed only when it reduces ambiguity without erasing evidence history.
```
