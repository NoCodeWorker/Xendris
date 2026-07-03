# Phygn v5.7.1 — Reporting & Next Gate

## 0. Purpose

This document defines reporting and next-gate decisions for targeted literature acquisition.

---

## 1. Required reports

Generate:

```txt
reports/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_source_rejection_log_v5_7_1.md
reports/campaigns/FRONTERA-C-TARGETED-VISIBILITY-DECOHERENCE-LITERATURE-ACQUISITION-v5_7_1.md
```

---

## 2. Final result doc

Create:

```txt
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
```

Note:

```txt
Spec pack occupies 339-343.
Campaign result should occupy 344.
```

---

## 3. Final status options

Emit exactly one:

```txt
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_COMPLETED
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_PARTIAL
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_HUMAN_LOOKUP
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_DOWNLOAD
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_BLOCKED_NO_CANDIDATE_SOURCES
FRONTERA_C_REQUIRES_TARGETED_DATASET_EXPANSION
```

---

## 4. Gate readiness

Create:

```txt
data/frontera_c/source_acquisition/v5_7_1_next_gate_decision.json
```

Fields:

```txt
final_status
resolved_candidate_source_count
high_priority_source_count
likely_observable_source_count
download_required_count
human_lookup_required_count
allowed_next_phase
blocked_next_phases
rationale
```

Gate rule:

```txt
if resolved_candidate_source_count >= 3:
    allowed_next_phase = v5.7.2 - Targeted Source Download & Observable Location Review
else:
    allowed_next_phase = None
```

---

## 5. Blocked claims

Always blocked:

```txt
Frontera C is validated
LOG_BOUNDARY is reactivated
literature acquisition equals evidence
source identity equals y_true
source relevance equals benchmark readiness
```

---

## 6. Allowed claims

Allowed if true:

```txt
targeted acquisition queue was created
candidate sources were resolved
candidate sources require download
candidate sources require human lookup
observable targets were prioritized
```

---

## 7. Final principle

```txt
A source queue is not evidence.
It is a map toward possible evidence.
```
