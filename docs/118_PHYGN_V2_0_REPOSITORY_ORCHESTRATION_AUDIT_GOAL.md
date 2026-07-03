# Phygn v2.0 — Repository Orchestration, Consistency & Refactor Audit Goal

## 0. Context

The latest confirmed document is:

```txt
117_PHYGN_V1_9_BUSINESS_MODEL_VALIDATION_GATE_RESULTS.md
```

Therefore, v2.0 starts at:

```txt
118
```

Phygn has now accumulated several major subsystems:

```txt
candidate benchmarks
baseline/candidate comparison
detectability and failure modes
source audit and source-backed baseline attempts
epistemic modes
friction gradient
hypothesis incubation
idea-to-hypothesis UX
prediction accuracy ledger
model runtime
copilot truth-boundary UI
business model validation
```

This is the correct moment to stop adding features and audit the repository as a unified system.

---

## 1. Core problem

The risk is no longer lack of capability.

The risk is architectural drift:

```txt
duplicated schemas
overlapping enums
inconsistent gate outputs
state names that mean similar things but differ across modules
reports with incompatible formats
campaign runners with different orchestration logic
tests that validate islands but not system coherence
```

---

## 2. v2.0 thesis

```txt
No more features until the epistemic architecture is internally consistent.
```

v2.0 is not a feature release.

v2.0 is an architectural audit and refactor map.

---

## 3. Main objective

Ensure that every Phygn subsystem speaks the same epistemic language.

This includes:

```txt
EpistemicMode
RiskLevel
FrictionLevel
LadderLevel
TruthBoundaryStatus
PermissionLevel
ClaimStatus
ActionStatus
DetectabilityStatus
CandidateSurvivalStatus
BusinessValidationStatus
WTPLevel
ChannelValidationLevel
UnitEconomicsStatus
EvidenceLevel
SourceSupportLevel
BenchmarkSupportLevel
```

---

## 4. Required audit domains

v2.0 must audit:

```txt
repository structure
module boundaries
core ontology/state definitions
schema duplication
enum duplication
gatekeeper consistency
permission consistency
campaign orchestration
report contracts
test architecture
import dependencies
API/frontend readiness
```

---

## 5. Refactor principle

Do not refactor blindly.

First produce:

```txt
audit findings
duplication map
inconsistency map
risk ranking
safe refactor plan
migration order
backward compatibility notes
```

Then implement only low-risk consolidation if safe.

---

## 6. Proposed target architecture

Option A — minimal consolidation:

```txt
phyng/core/
  ontology.py
  states.py
  permissions.py
  evidence.py
  gates.py
  audit.py
```

Option B — domain separation:

```txt
phyng/core/
phyng/domains/physics/
phyng/domains/business/
phyng/domains/finance/
phyng/domains/copilot/
phyng/domains/prediction/
```

v2.0 should recommend which path is safer.

---

## 7. Acceptance criteria

v2.0 is complete when:

```txt
repository audit report exists
core ontology consistency report exists
module boundary/refactor map exists
campaign/report/test orchestration audit exists
safe refactor recommendations exist
tests pass
no existing behavior is silently changed
all proposed changes are traceable
```

---

## 8. Final principle

```txt
Before Phygn scales outward, Phygn must become internally legible.
```
