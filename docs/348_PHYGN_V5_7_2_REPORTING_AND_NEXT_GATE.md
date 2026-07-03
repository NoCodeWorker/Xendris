# Phygn v5.7.2 — Reporting & Next Gate

## 0. Purpose

This document defines reports and final gate decisions for v5.7.2.

---

## 1. Required reports

Generate:

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

---

## 2. Final result document

Create:

```txt
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
```

Note:

```txt
Spec pack occupies 345-349.
Campaign result should occupy 350.
```

---

## 3. Final statuses

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

## 4. Gate rules

If:

```txt
observed_measurement_candidate_count >= 1
```

then:

```txt
allowed_next_phase = v5.7.3 — Targeted y_true Extraction
```

If:

```txt
verified_source_object_count == 0
```

then:

```txt
allowed_next_phase = None
final_status = TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES
```

If:

```txt
verified_source_object_count > 0
observed_measurement_candidate_count == 0
```

then:

```txt
allowed_next_phase = None
final_status = TARGETED_OBSERVABLE_LOCATION_BLOCKED_NO_OBSERVED_MEASUREMENTS
```

If all source objects are missing:

```txt
final_status = TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD
```

---

## 5. Blocked claims

Always blocked:

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

## 6. Allowed claims

Allowed if true:

```txt
source objects were downloaded and hashed
source objects require manual download
observable location candidates were found
observed measurement candidates were found
v5.7.3 is permitted only if observed measurement candidates exist
```

---

## 7. Final principle

```txt
Source bytes open the door.
Observable locations decide whether y_true extraction may enter.
```
