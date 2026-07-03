# Phygn v5.6 — Reporting & Next Gate

## 0. Purpose

This document defines reporting and next-gate decisions for LOG_BOUNDARY control failure review.

---

## 1. Required reports

Generate:

```txt
reports/frontera_c/disposition/log_boundary_control_failure_review_v5_6.md
reports/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.md
reports/frontera_c/disposition/log_boundary_allowed_future_roles_v5_6.md
reports/frontera_c/disposition/log_boundary_blocked_claims_v5_6.md
reports/frontera_c/disposition/frontera_c_roadmap_update_after_log_boundary_v5_6.md
reports/frontera_c/disposition/v5_6_next_research_direction.md
reports/campaigns/FRONTERA-C-LOG-BOUNDARY-CONTROL-FAILURE-REVIEW-v5_6.md
```

---

## 2. Next gate decision

Create:

```txt
data/frontera_c/disposition/v5_6_next_research_direction.json
```

Schema:

```python
class NextResearchDirection(BaseModel):
    final_status: str
    selected_next_direction: str
    allowed_next_phase: str | None
    blocked_next_phases: list[str]
    required_inputs: list[str]
    rationale: str
    blocked_claims: list[str]
    allowed_claims: list[str]
    notes: list[str]
```

Possible next phases:

```txt
v5.7 — Visibility/Decoherence Dataset Expansion
v5.7 — Candidate Family Reprioritization After Control Failure
v5.7 — New Experiment Design Feasibility Gate
v5.7 — Next Candidate Human Source Lookup
```

Recommended default:

```txt
v5.7 — Visibility/Decoherence Dataset Expansion
```

---

## 3. Canonical statuses

Add:

```txt
LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_COMPLETED
LOG_BOUNDARY_DISPOSITION_BLOCKED_MISSING_CONTROL_RESULTS
LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE
LOG_BOUNDARY_RETAINED_AS_BENCHMARK_FIXTURE
LOG_BOUNDARY_RETAINED_AS_NEGATIVE_CONTROL_FIXTURE
FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE
FRONTERA_C_REQUIRES_CANDIDATE_REPRIORITIZATION
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

Suggested mapping for archive:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: CONTROL_FAILURE
Support Level: UNSUPPORTED_AS_VALIDATION_CANDIDATE
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping for retained fixture:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: FIXTURE_ONLY
Support Level: METHOD_SUPPORT_ONLY
Risk Level: LOW_FOR_PIPELINE_TESTING_HIGH_FOR_CLAIMS
```

---

## 4. Allowed claims

Allowed:

```txt
LOG_BOUNDARY produced a positive single-source smoke test.
LOG_BOUNDARY failed negative controls because the gain was explained by simple controls.
LOG_BOUNDARY was archived as a Frontera C validation candidate if the disposition says so.
LOG_BOUNDARY may be retained as a benchmark/control fixture.
```

Blocked:

```txt
LOG_BOUNDARY is validated.
LOG_BOUNDARY validates Frontera C.
LOG_BOUNDARY supports the invariant.
LOG_BOUNDARY has robust PredictiveGain.
Negative-control failure can be bypassed by more architecture.
```

---

## 5. Final principle

```txt
The control gate is where beautiful candidates go to become honest.
```
