# Phygn v5.7.3 — Targeted y_true Extraction Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
```

Therefore v5.7.3 starts at:

```txt
351
```

v5.7.2 status:

```txt
TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND
verified_source_objects = 4
sha256_hashes_generated = 4
download_failures = 2
observable_location_candidates = 62
observed_measurement_candidates = 10
allowed_next_phase = v5.7.3 - Targeted y_true Extraction
```

Missing or unverified source objects:

```txt
GERLICH_2011_LARGE_ORGANIC.pdf
ARNDT_1999_C60.pdf
```

These missing sources must not enter y_true extraction unless verified in this phase with local file + SHA256.

---

## 1. Core rule

```txt
Observed measurement candidate is not y_true.
Only strict provenance plus numeric extraction creates y_true.
```

---

## 2. Mission

Implement:

```txt
v5.7.3 — Targeted y_true Extraction
```

The mission is to evaluate the 10 observed measurement candidates from v5.7.2 and convert them into accepted or rejected y_true records under strict QC.

---

## 3. Primary objective

For each observed measurement candidate:

1. Confirm complete source identity.
2. Confirm verified local source object.
3. Confirm SHA256 hash.
4. Confirm page/table/figure/section/equation location.
5. Extract numeric observed value(s).
6. Extract or normalize units.
7. Preserve condition mapping.
8. Decide QC.
9. Accept or reject as y_true.
10. Assemble expanded visibility/decoherence y_true dataset.

---

## 4. What this phase is NOT

This phase is not:

```txt
PredictiveGain computation
benchmark construction
C-structure ablation
LOG_BOUNDARY reactivation
Frontera C validation
physical claim creation
invariant confirmation
```

---

## 5. Inputs

Load:

```txt
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json
data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json
data/frontera_c/observable_location/v5_7_2_next_gate_decision.json
data/frontera_c/source_download/source_download_manifest_v5_7_2.json
data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json
data/frontera_c/source_download/source_download_failures_v5_7_2.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
```

---

## 6. Candidate scope

Primary scope:

```txt
10 observed measurement candidates from v5.7.2
```

Existing Hackermueller v5.3 y_true records may be included in total dataset counts but must not be duplicated.

---

## 7. Strict acceptance criteria

A y_true record may be accepted only if it has:

```txt
y_true_id
source_id
source_title
source_authors or publication authority
source_year
source_doi_or_arxiv_or_url
local_pdf_path
local_pdf_hash
page_number
location_label
observable_class
variable_name
numeric_value
original_value_text
unit unless explicitly dimensionless
condition_mapping
extraction_method
provenance_status
qc_status = PASS or PASS_WITH_LIMITATIONS
limitations
claim_impact
```

---

## 8. Rejection criteria

Reject if any of these apply:

```txt
source identity incomplete
local source object missing
local hash missing
page/location missing
numeric value missing
unit unresolved
condition mapping ambiguous
model-only value
bound/constraint only
regime/context value only
qualitative prose
figure requires human visual extraction and not enough numeric text exists
supplementary data required but absent
```

---

## 9. QC statuses

Allowed QC statuses:

```txt
PASS
PASS_WITH_LIMITATIONS
REJECT
REQUIRES_HUMAN_FIGURE_REVIEW
REQUIRES_SUPPLEMENTARY_DATA
REQUIRES_UNIT_RESOLUTION
REQUIRES_CONDITION_MAPPING
```

Only:

```txt
PASS
PASS_WITH_LIMITATIONS
```

may enter accepted y_true.

---

## 10. Required outputs

Create:

```txt
data/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.json
data/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.json
data/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.json
data/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.json
data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json
data/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.json
data/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.json
```

---

## 11. Final statuses

Emit exactly one:

```txt
TARGETED_YTRUE_EXTRACTION_COMPLETED
TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED
TARGETED_YTRUE_EXTRACTION_PARTIAL
TARGETED_YTRUE_EXTRACTION_BLOCKED_NO_ACCEPTED_YTRUE
TARGETED_YTRUE_EXTRACTION_REQUIRES_HUMAN_FIGURE_REVIEW
TARGETED_YTRUE_EXTRACTION_REQUIRES_SUPPLEMENTARY_DATA
TARGETED_YTRUE_EXTRACTION_BLOCKED_PROVENANCE_FAILURE
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

---

## 12. Gate logic

Let:

```txt
new_accepted_ytrue_count = accepted records created in v5.7.3
total_accepted_ytrue_count = previous accepted y_true + new accepted y_true, deduplicated
independent_source_count = unique sources in total accepted dataset
```

If:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

then emit:

```txt
TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED
```

and permit:

```txt
v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If:

```txt
new_accepted_ytrue_count > 0
```

but threshold is not reached, emit:

```txt
TARGETED_YTRUE_EXTRACTION_PARTIAL
```

and permit only targeted expansion.

If:

```txt
new_accepted_ytrue_count == 0
```

emit a blocking status.

---

## 13. Final principle

```txt
No accepted y_true, no benchmark.
No benchmark, no PredictiveGain.
No PredictiveGain, no Frontera C validation.
```
