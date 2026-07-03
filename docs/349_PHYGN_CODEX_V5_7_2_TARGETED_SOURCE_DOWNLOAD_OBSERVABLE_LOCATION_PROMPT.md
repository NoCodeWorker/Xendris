# Codex Prompt — Phygn v5.7.2 Targeted Source Download & Observable Location Review

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
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
```

Therefore v5.7.2 starts at:

```txt
345
```

---

# 1. Read first

Read these v5.7.2 specs:

```txt
docs/345_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_docs/status/GOAL.md
docs/346_PHYGN_V5_7_2_SOURCE_DOWNLOAD_AND_HASH_PROTOCOL.md
docs/347_PHYGN_V5_7_2_OBSERVABLE_LOCATION_REVIEW_PROTOCOL.md
docs/348_PHYGN_V5_7_2_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v5.7.2 — Targeted Source Download & Observable Location Review
```

Convert the 6 resolved candidate sources from v5.7.1 into verified source objects if possible, and review them for observable locations.

---

# 3. Current verified state

v5.7.1 result:

```txt
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_DOWNLOAD
resolved_candidate_sources = 6
download_required = 6
allowed_next_phase = v5.7.2 - Targeted Source Download & Observable Location Review
```

---

# 4. Hard constraints

Do not extract y_true.

Do not create accepted y_true.

Do not compute PredictiveGain.

Do not build benchmark.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not create physical claim.

Do not reactivate LOG_BOUNDARY.

Do not treat downloaded sources as evidence.

Do not treat observable locations as y_true.

Do not fabricate local files, hashes, page numbers, figure IDs, table IDs, values or snippets.

---

# 5. Required inputs

Load:

```txt
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
data/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.json
data/frontera_c/source_acquisition/v5_7_1_next_gate_decision.json
data/real_sources/source_hashes_v3_6.json
```

Inspect local source directory:

```txt
data/real_sources/pdfs/
```

---

# 6. Create package

Create:

```txt
phyng/source_download/
  __init__.py
  schemas.py
  manifest.py
  hashing.py
  failures.py
  reports.py
  campaign.py
```

Create or extend:

```txt
phyng/observable_location/
  __init__.py
  schemas.py
  pdf_text_scan.py
  location_classifier.py
  observed_measurement_candidates.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_targeted_source_download_observable_location.py
```

Entrypoint:

```python
run_frontera_c_targeted_source_download_observable_location_campaign(root: str | Path = ".")
```

---

# 7. Required source-download outputs

Create:

```txt
data/frontera_c/source_download/source_download_manifest_v5_7_2.json
data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json
data/frontera_c/source_download/source_download_failures_v5_7_2.json
```

---

# 8. Required observable-location outputs

Create:

```txt
data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json
data/frontera_c/observable_location/v5_7_2_next_gate_decision.json
```

---

# 9. Required reports

Create:

```txt
reports/frontera_c/source_download/source_download_manifest_v5_7_2.md
reports/frontera_c/source_download/source_hash_registry_update_v5_7_2.md
reports/frontera_c/source_download/source_download_failures_v5_7_2.md
reports/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.md
reports/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.md
reports/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.md
reports/frontera_c/observable_location/v5_7_2_next_gate_decision.md
reports/campaigns/FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2.md
```

Create final result document:

```txt
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
```

---

# 10. Observable target classes

Search for:

```txt
VISIBILITY
FRINGE_VISIBILITY
INTERFERENCE_CONTRAST
CONTRAST_DECAY
COHERENCE_LOSS
DECOHERENCE_RATE
PHASE_DECAY
THERMAL_DECOHERENCE_VISIBILITY
MATTER_WAVE_VISIBILITY
COLLISIONAL_DECOHERENCE_RATE
```

---

# 11. Location classifications

Every candidate location must be exactly one of:

```txt
OBSERVED_MEASUREMENT_CANDIDATE
MODEL_PARAMETER
BOUND_OR_CONSTRAINT
REGIME_VALUE
THEORETICAL_EQUATION
QUALITATIVE_PROSE
SUPPLEMENTARY_POINTER
DATA_REPOSITORY_POINTER
NOT_YTRUE
```

Only OBSERVED_MEASUREMENT_CANDIDATE may enter v5.7.3.

---

# 12. Final statuses

Emit exactly one:

```txt
TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_COMPLETED
TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND
TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD
TARGETED_SOURCE_DOWNLOAD_REQUIRES_HUMAN_FIGURE_REVIEW
TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES
TARGETED_OBSERVABLE_LOCATION_BLOCKED_NO_OBSERVED_MEASUREMENTS
TARGETED_OBSERVABLE_LOCATION_REQUIRES_SUPPLEMENTARY_DATA
FRONTERA_C_BLOCKED_NO_OBSERVABLE_LOCATION
```

---

# 13. Gate rules

If:

```txt
observed_measurement_candidate_count >= 1
```

permit:

```txt
v5.7.3 — Targeted y_true Extraction
```

If:

```txt
verified_source_object_count == 0
```

stop with:

```txt
TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES
```

If sources are missing:

```txt
TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD
```

If only human figure review can resolve values:

```txt
TARGETED_SOURCE_DOWNLOAD_REQUIRES_HUMAN_FIGURE_REVIEW
```

---

# 14. Tests

Create:

```txt
tests/test_v5_7_2_source_download_manifest.py
tests/test_v5_7_2_source_hash_registry_update.py
tests/test_v5_7_2_source_download_failures.py
tests/test_v5_7_2_observable_location_candidates.py
tests/test_v5_7_2_observed_measurement_candidates.py
tests/test_v5_7_2_next_gate_decision.py
tests/test_frontera_c_targeted_source_download_observable_location_campaign.py
```

Minimum tests:

```txt
test_missing_local_files_require_manual_download
test_hash_computed_for_existing_local_file
test_no_ytrue_extracted
test_no_predictive_gain_computed
test_observable_location_is_not_ytrue
test_observed_measurement_candidate_permits_v573
test_no_local_sources_blocks_observable_review
test_no_fabricated_hashes_or_locations
test_reports_generated
```

---

# 15. Allowed claims

Allowed if true:

```txt
source objects were downloaded and hashed
source objects require manual download
observable location candidates were found
observed measurement candidates were found
v5.7.3 is permitted only if observed measurement candidates exist
```

Blocked:

```txt
Frontera C is validated
LOG_BOUNDARY is reactivated
downloaded sources are evidence
observable location equals y_true
source support equals PredictiveGain
physical claim
invariant confirmation
```

---

# 16. Acceptance criteria

Complete when:

```txt
v5.7.1 inputs loaded
source download manifest generated
source hash registry update generated
source failures generated
observable location candidates generated
observed measurement candidates generated
next gate decision generated
tests pass
reports generated
final doc 350 generated
no y_true extraction
no PredictiveGain
no Frontera C validation
```

---

# 17. Final discipline

```txt
No source object, no observable review.
No observable location, no y_true.
```
