# Phygn v2.5 — LOG_BOUNDARY Loop Feedback Protocol

## 0. Purpose

This document defines how v2.5 feeds synthetic execution results into the v2.4 closed loop.

The loop may learn priorities.

The loop may not learn truth.

---

## 1. Input to Candidate Learning Loop

After execution, send:

```txt
input_type: SYNTHETIC_BENCHMARK_RESULT
domain: physical_candidate
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
previous_status: SYNTHETIC_BENCHMARK_DESIGNED
result_status: <detectability_status>
best_max_abs_delta: <value>
failure_conditions: <list>
```

---

## 2. Feedback rules

If status is:

```txt
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
```

Then propose:

```txt
increase source-search priority
increase benchmark-pressure priority
schedule source support audit
schedule benchmark data search
keep physical claims blocked
```

If status is:

```txt
LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
```

Then propose:

```txt
down-rank LOG_BOUNDARY
record as synthetic negative result
select next heuristic family
keep physical claims blocked
```

If status is:

```txt
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
```

Then propose:

```txt
mark as toy-extreme
require parameter justification
block priority elevation unless source-backed
```

If status is:

```txt
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
```

Then propose:

```txt
block promotion
record post-hoc tuning failure
require pre-registration
```

---

## 3. Meta-loop feedback

The meta-loop may propose low-risk improvements:

```txt
report warning templates
candidate priority update
next-best-question ordering
source search priority
benchmark pressure routing
```

The meta-loop may not auto-apply:

```txt
claim gate relaxation
source requirement reduction
benchmark requirement reduction
experimental evidence requirement reduction
canonical permission semantic changes
```

---

## 4. Required loop report fields

```txt
loop_event_id
candidate_id
result_status
canonical_status
update_proposals
blocked_updates
shadow_mode_required
human_review_required
next_actions
rollbackable_config_changes
```

---

## 5. Final principle

```txt
The loop may change where Phygn looks next.
It may not change what Phygn is allowed to claim.
```
