# Phygn v2.4 — Loop Guards Against Self-Confirmation

## 0. Purpose

Closed loops can make systems smarter.

They can also make systems self-confirming.

This document defines the guards that prevent Phygn from rewarding its own biases.

---

## 1. Core failure mode

```txt
self-confirming epistemic loop
```

Example:

```txt
Heuristic raises LOG_BOUNDARY.
LOG_BOUNDARY produces toy detectability.
Loop increases LOG_BOUNDARY priority.
System searches variants that maximize detectability.
Reports begin to look increasingly positive.
No external evidence was added.
```

This is prohibited.

---

## 2. Required guards

```txt
NO_SELF_AUTHORIZATION
NO_PERMISSION_ELEVATION_FROM_HEURISTIC_ONLY
NO_HIDDEN_PARAMETER_OPTIMIZATION
NO_POST_HOC_SCALE_SELECTION
NO_CLAIM_WITHOUT_SOURCE_OR_BENCHMARK
NO_SYNTHETIC_TO_PHYSICAL_PROMOTION
NO_CRITICAL_CHANGE_WITHOUT_SHADOW_MODE
NO_GATE_RELAXATION_WITHOUT_HUMAN_REVIEW
NO_REPORT_WITHOUT_BLOCKED_CLAIMS_SECTION
NO_LOOP_ITERATION_WITHOUT_AUDIT_EVENT
```

---

## 3. Parameter search guard

Any parameter sweep must record:

```txt
pre_registered_ranges
out_of_range_values
extreme_values
post_hoc_changes
detectability_source
```

If detectability appears only after post-hoc tuning:

```txt
FAIL_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
```

---

## 4. Evidence boundary guard

Synthetic support may update:

```txt
candidate priority
source search priority
benchmark pressure priority
```

It may not update:

```txt
physical truth status
experimental support
source support
claim authorization
```

---

## 5. Regression guard

Before applying any meta-change:

```txt
run full test suite
run relevant focused tests
compare canonical permissions before/after
compare blocked reasons before/after
compare report blocked-claims sections
generate impact report
```

If critical permission changes occur unexpectedly:

```txt
META_CHANGE_BLOCKED_REGRESSION
```

---

## 6. Rollback guard

Every applied meta-change must have:

```txt
version id
previous config
new config
reason
tests passed
rollback path
impact report
```

---

## 7. Final principle

```txt
The loop may improve the search.
It may not move the finish line.
```
