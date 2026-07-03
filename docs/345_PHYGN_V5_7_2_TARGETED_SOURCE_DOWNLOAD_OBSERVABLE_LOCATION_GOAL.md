# Phygn v5.7.2 — Targeted Source Download & Observable Location Review Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
```

Therefore v5.7.2 starts at:

```txt
345
```

v5.7.1 status:

```txt
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_DOWNLOAD
resolved_candidate_sources = 6
download_required = 6
allowed_next_phase = v5.7.2 - Targeted Source Download & Observable Location Review
```

This phase created a source acquisition queue only. It did not extract y_true, compute PredictiveGain, reactivate LOG_BOUNDARY, validate Frontera C, or create physical claims.

---

## 1. Core rule

```txt
Downloaded source is not y_true.
Observable location is permission to extract y_true.
```

---

## 2. Mission

Implement:

```txt
v5.7.2 — Targeted Source Download & Observable Location Review
```

The mission is to convert the 6 resolved candidate sources from v5.7.1 into verifiable local source objects and inspect them for source-located observable candidates.

---

## 3. Primary objective

For each resolved candidate source from v5.7.1:

1. Determine whether a local source object exists.
2. If downloaded manually, register the local path.
3. Compute SHA256 hash.
4. Add the source to a local source manifest.
5. Inspect the source for observable locations.
6. Classify all candidate locations.
7. Decide whether v5.7.3 y_true extraction is permitted.

---

## 4. What this phase is NOT

This phase is not:

```txt
y_true extraction
accepted y_true creation
PredictiveGain computation
benchmark construction
LOG_BOUNDARY rescue
C-structure ablation
Frontera C validation
physical claim creation
```

---

## 5. Required inputs

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

Local PDF directory:

```txt
data/real_sources/pdfs/
```

---

## 6. Target source count

Expected from v5.7.1:

```txt
resolved_candidate_source_count = 6
download_required_count = 6
```

v5.7.2 must not invent downloads. If a source file is missing, mark it as:

```txt
REQUIRES_MANUAL_DOWNLOAD
```

---

## 7. Observable location targets

Search downloaded sources for:

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

Conditions may include:

```txt
pressure
temperature
time
heating_power
laser_power
mass
velocity
path_separation
gas_density
decoherence_parameter
```

Conditions are not y_true.

---

## 8. Location classifications

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

Only:

```txt
OBSERVED_MEASUREMENT_CANDIDATE
```

may enter v5.7.3.

---

## 9. Required outputs

Create:

```txt
data/frontera_c/source_download/source_download_manifest_v5_7_2.json
data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json
data/frontera_c/source_download/source_download_failures_v5_7_2.json
data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json
data/frontera_c/observable_location/v5_7_2_next_gate_decision.json
```

---

## 10. Final statuses

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

## 11. Next-gate logic

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
downloaded_source_count == 0
```

stop with:

```txt
TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES
```

If sources are missing:

```txt
TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD
```

If only figures/tables require visual inspection:

```txt
TARGETED_SOURCE_DOWNLOAD_REQUIRES_HUMAN_FIGURE_REVIEW
```

If no observed measurement candidates are found:

```txt
TARGETED_OBSERVABLE_LOCATION_BLOCKED_NO_OBSERVED_MEASUREMENTS
```

---

## 12. Final principle

```txt
No source object, no observable review.
No observable location, no y_true.
```
