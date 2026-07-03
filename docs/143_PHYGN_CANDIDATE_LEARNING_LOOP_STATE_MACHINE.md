# Phygn v2.4 — Candidate Learning Loop State Machine

## 0. Purpose

This document defines the outer loop: the Candidate Learning Loop.

It converts results into structured updates to candidate family priorities without allowing self-confirmation.

---

## 1. Candidate loop states

```txt
LOOP_INPUT_RECEIVED
HEURISTIC_DISCOVERY_RUN
CANDIDATES_PRIORITIZED
CANDIDATE_FORMALIZATION_ATTEMPTED
SYNTHETIC_BENCHMARK_DESIGNED
SYNTHETIC_BENCHMARK_EXECUTED
SOURCE_PRESSURE_ATTEMPTED
BENCHMARK_PRESSURE_ATTEMPTED
RESULT_CLASSIFIED
PREDICTION_LEDGER_UPDATED
POST_MORTEM_COMPLETED
UPDATE_PROPOSAL_CREATED
NEXT_CANDIDATE_SELECTED
LOOP_BLOCKED_REQUIRES_REVIEW
```

---

## 2. Candidate loop input types

```txt
RAW_IDEA
HEURISTIC_RESULT
SYNTHETIC_BENCHMARK_RESULT
SOURCE_AUDIT_RESULT
BENCHMARK_RESULT
PREDICTION_OUTCOME
BUSINESS_EXPERIMENT_RESULT
COPILOT_FEEDBACK
HUMAN_REVIEW_NOTE
```

---

## 3. Candidate loop output

```python
class CandidateLoopResult(BaseModel):
    loop_id: str
    input_type: str
    domain: str
    candidate_id: str | None
    candidate_family: str | None
    previous_status: str | None
    new_status: str
    canonical_status: CanonicalStatusRecord
    ledger_event_id: str | None
    post_mortem_id: str | None
    update_proposals: list[CandidateUpdateProposal]
    next_actions: list[str]
    blocked_reasons: list[str]
```

---

## 4. Update proposal types

```txt
HEURISTIC_WEIGHT_UPDATE
CANDIDATE_FAMILY_PRIORITY_UPDATE
NEXT_BEST_QUESTION_PRIORITY_UPDATE
SOURCE_SEARCH_PRIORITY_UPDATE
BENCHMARK_DESIGN_UPDATE
WARNING_TEMPLATE_UPDATE
REPORT_CONTRACT_UPDATE
```

---

## 5. Allowed updates

The candidate loop may propose:

```txt
down-rank candidate families that repeatedly fail detectability
up-rank families that survive benchmark design
increase source-search priority for promising candidates
add warning templates for repeated failure modes
adjust non-critical heuristic weights in shadow mode
```

---

## 6. Forbidden updates

The candidate loop may not directly modify:

```txt
CanonicalPermission semantics
CanonicalBlockedReason semantics
source support gates
benchmark support gates
experimental evidence gates
financial action gates
claim authorization rules
truth-boundary critical gates
```

---

## 7. Example: LOG_BOUNDARY

If LOG_BOUNDARY synthetic execution returns:

```txt
DETECTABLE_SYNTHETIC_DELTA
```

Then loop may propose:

```txt
increase source-search priority
increase benchmark-pressure priority
mark as source-pressure candidate
```

It may not propose:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
```

If LOG_BOUNDARY returns:

```txt
UNDETECTABLE_SYNTHETIC_DELTA
```

Then loop may propose:

```txt
down-rank LOG_BOUNDARY
record failure reason
search variant or choose next family
```

---

## 8. Loop anti-debt requirement

Every loop iteration must produce:

```txt
loop event
canonical status
post-mortem or skip reason
update proposal or no-update reason
next action
report
```

No silent iteration is allowed.

---

## 9. Final principle

```txt
A failed candidate should not disappear.
It should become structured information for the next candidate.
```
