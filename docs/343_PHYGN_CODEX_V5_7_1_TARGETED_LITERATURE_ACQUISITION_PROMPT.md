# Codex Prompt — Phygn v5.7.1 Targeted Visibility/Decoherence Literature Acquisition

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current latest result document:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
```

Therefore v5.7.1 starts at:

```txt
339
```

---

# 1. Read first

Read these v5.7.1 specs:

```txt
docs/339_PHYGN_V5_7_1_TARGETED_LITERATURE_ACQUISITION_docs/status/GOAL.md
docs/340_PHYGN_V5_7_1_SOURCE_ACQUISITION_PROTOCOL.md
docs/341_PHYGN_V5_7_1_SEARCH_STRATEGY_AND_SEED_QUERIES.md
docs/342_PHYGN_V5_7_1_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v5.7.1 — Targeted Visibility/Decoherence Literature Acquisition
```

The goal is to create a targeted, prioritized source acquisition queue for additional independent visibility/decoherence experimental sources.

This phase does not extract y_true.

This phase does not compute PredictiveGain.

This phase does not reactivate LOG_BOUNDARY.

---

# 3. Current verified state

v5.7 result:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL
accepted_y_true_total = 4
independent_source_count = 1
```

Current blocker:

```txt
MISSING_EXPERIMENTAL_DATA
MISSING_BENCHMARK
SOURCE_LIMITED
```

LOG_BOUNDARY:

```txt
ARCHIVED_AS_VALIDATION_CANDIDATE
```

---

# 4. Hard constraints

Do not extract y_true.

Do not compute PredictiveGain.

Do not build benchmark.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not create physical claim.

Do not claim invariant confirmation.

Do not reactivate LOG_BOUNDARY as candidate.

Do not treat source acquisition as evidence.

Do not allow raw title-only sources to pass.

---

# 5. Required inputs

Load:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json
data/frontera_c/dataset_expansion/v5_7_next_gate_decision.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json
data/real_sources/source_hashes_v3_6.json
```

---

# 6. Create package

Create:

```txt
phyng/source_acquisition/
  __init__.py
  schemas.py
  seed_queries.py
  candidate_sources.py
  identity_matrix.py
  observable_target_matrix.py
  download_queue.py
  rejection_log.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_targeted_visibility_decoherence_literature_acquisition.py
```

Entrypoint:

```python
run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(root: str | Path = ".")
```

---

# 7. Source targets

Target experimental literature likely to contain:

```txt
visibility / fringe visibility / contrast / decoherence rate / contrast decay
```

Prioritize:

```txt
matter-wave interferometry
molecular interferometry
thermal emission decoherence
collisional decoherence
gas collision decoherence
Talbot-Lau interferometry
KDTLI visibility measurements
```

---

# 8. Seed queries

Use and extend:

```txt
"matter wave interferometry visibility decoherence figure"
"molecular interferometry visibility thermal decoherence"
"Talbot Lau interferometer visibility decoherence measurement"
"KDTLI molecular interference visibility data"
"collisional decoherence matter wave interferometry visibility gas pressure"
"thermal emission decoherence visibility molecule interferometer"
"interference fringe visibility decoherence rate atom interferometer"
"visibility loss decoherence matter wave experiment"
"macroscopicity test visibility matter wave interferometry"
"decoherence by thermal emission of radiation visibility figure"
```

---

# 9. Required outputs

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_source_rejection_log_v5_7_1.json
data/frontera_c/source_acquisition/v5_7_1_next_gate_decision.json
```

---

# 10. Required reports

Create:

```txt
reports/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.md
reports/frontera_c/source_acquisition/visibility_decoherence_source_rejection_log_v5_7_1.md
reports/campaigns/FRONTERA-C-TARGETED-VISIBILITY-DECOHERENCE-LITERATURE-ACQUISITION-v5_7_1.md
```

Create final result document:

```txt
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
```

---

# 11. Final statuses

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

# 12. Gate logic

If:

```txt
resolved_candidate_source_count >= 3
```

permit:

```txt
v5.7.2 — Targeted Source Download & Observable Location Review
```

If fewer than 3 candidate sources are resolved:

```txt
continue targeted human lookup
```

---

# 13. Tests

Create:

```txt
tests/test_v5_7_1_source_acquisition_queue.py
tests/test_v5_7_1_candidate_source_identity_matrix.py
tests/test_v5_7_1_observable_target_matrix.py
tests/test_v5_7_1_download_priority_queue.py
tests/test_v5_7_1_source_rejection_log.py
tests/test_v5_7_1_next_gate_decision.py
tests/test_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign.py
```

Minimum tests:

```txt
test_log_boundary_remains_archived
test_no_ytrue_extracted
test_no_predictive_gain_computed
test_raw_title_only_source_not_complete
test_resolved_source_requires_stable_identity
test_download_queue_created_for_resolved_sources
test_next_gate_requires_three_resolved_sources
test_source_acquisition_is_not_evidence
test_reports_generated
```

---

# 14. Allowed claims

Allowed if true:

```txt
targeted acquisition queue was created
candidate sources were resolved
candidate sources require download
candidate sources require human lookup
observable targets were prioritized
```

Blocked:

```txt
Frontera C is validated
LOG_BOUNDARY is reactivated
literature acquisition equals evidence
source identity equals y_true
source relevance equals benchmark readiness
```

---

# 15. Acceptance criteria

Complete when:

```txt
v5.7 status loaded
source acquisition queue generated
source identity matrix generated
observable target matrix generated
download queue generated
rejection log generated
next gate decision generated
tests pass
reports generated
final doc 344 generated
no y_true extraction
no PredictiveGain
no Frontera C validation
```

---

# 16. Final discipline

```txt
A source queue is not evidence.
It is a map toward possible evidence.
```
