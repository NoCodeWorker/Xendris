# Codex Prompt — Phygn v5.7.3 Targeted y_true Extraction

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
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
```

Therefore v5.7.3 starts at:

```txt
351
```

---

# 1. Read first

Read these v5.7.3 specs:

```txt
docs/351_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_docs/status/GOAL.md
docs/352_PHYGN_V5_7_3_YTRUE_EXTRACTION_PROTOCOL.md
docs/353_PHYGN_V5_7_3_DATASET_QUALITY_AND_BENCHMARK_READINESS.md
docs/354_PHYGN_V5_7_3_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v5.7.3 — Targeted y_true Extraction
```

Convert observed measurement candidates from v5.7.2 into accepted or rejected y_true records under strict provenance and QC.

---

# 3. Current verified state

v5.7.2 result:

```txt
TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND
verified_source_objects = 4
sha256_hashes_generated = 4
download_failures = 2
observable_location_candidates = 62
observed_measurement_candidates = 10
allowed_next_phase = v5.7.3 - Targeted y_true Extraction
```

Missing/unverified:

```txt
GERLICH_2011_LARGE_ORGANIC.pdf
ARNDT_1999_C60.pdf
```

---

# 4. Hard constraints

Do not compute PredictiveGain.

Do not build benchmark.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not create physical claim.

Do not claim invariant confirmation.

Do not reactivate LOG_BOUNDARY.

Do not accept y_true without complete provenance.

Do not accept y_true from unverified source objects.

Do not fabricate values, units, page numbers, figure IDs, table IDs, snippets or hashes.

---

# 5. Required inputs

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

# 6. Create package

Create:

```txt
phyng/targeted_ytrue/
  __init__.py
  schemas.py
  loader.py
  candidate_builder.py
  qc.py
  unit_normalization.py
  deduplication.py
  dataset_assembly.py
  dataset_quality.py
  next_gate.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_targeted_ytrue_extraction.py
```

Entrypoint:

```python
run_frontera_c_targeted_ytrue_extraction_campaign(root: str | Path = ".")
```

---

# 7. Required outputs

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

# 8. Required reports

Create:

```txt
reports/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.md
reports/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.md
reports/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.md
reports/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.md
reports/campaigns/FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3.md
```

Create final result document:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
```

---

# 9. Acceptance rules

Accept only if:

```txt
source identity complete
verified local source object
local PDF hash
page/location present
numeric value present
unit resolved or dimensionless
condition mapping resolved
QC PASS or PASS_WITH_LIMITATIONS
```

Reject otherwise.

---

# 10. Deduplication

Do not duplicate Hackermueller v5.3 y_true records.

Deduplicate using:

```txt
source_id
page_number
location_label
observable_class
variable_name
value_numeric
conditions
```

---

# 11. Final statuses

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

# 12. Gate logic

If:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

permit:

```txt
v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If:

```txt
new_accepted_ytrue_count > 0
```

but threshold not reached:

```txt
permit only targeted dataset expansion
```

If:

```txt
new_accepted_ytrue_count == 0
```

stop with exact blocker.

---

# 13. Tests

Create:

```txt
tests/test_v5_7_3_ytrue_candidate_builder.py
tests/test_v5_7_3_ytrue_qc.py
tests/test_v5_7_3_unit_normalization.py
tests/test_v5_7_3_ytrue_deduplication.py
tests/test_v5_7_3_dataset_assembly.py
tests/test_v5_7_3_dataset_quality.py
tests/test_v5_7_3_next_gate_decision.py
tests/test_frontera_c_targeted_ytrue_extraction_campaign.py
```

Minimum tests:

```txt
test_observed_measurement_candidate_is_not_automatically_ytrue
test_accept_requires_verified_source_object_and_hash
test_accept_requires_numeric_value_and_unit_or_dimensionless
test_unverified_missing_sources_do_not_enter_ytrue
test_hackermueller_v53_records_not_duplicated
test_conditions_are_not_ytrue
test_threshold_requires_total_10_and_two_sources
test_no_predictive_gain_computed
test_no_physical_claim_created
test_reports_generated
```

---

# 14. Allowed claims

Allowed if true:

```txt
targeted y_true extraction was attempted
new y_true records were accepted
candidate records were rejected under QC
dataset quality was assessed
v5.8 is permitted only if threshold reached
```

Blocked:

```txt
Frontera C is validated
LOG_BOUNDARY is reactivated
accepted y_true equals PredictiveGain
dataset expansion equals validation
physical claim
invariant confirmation
```

---

# 15. Acceptance criteria

Complete when:

```txt
v5.7.2 inputs loaded
10 observed measurement candidates evaluated or explicitly accounted for
accepted/rejected y_true artifacts generated
expanded dataset generated
dataset quality generated
next gate decision generated
tests pass
reports generated
final doc 356 generated
no PredictiveGain
no benchmark
no Frontera C validation
```

---

# 16. Final discipline

```txt
A number without provenance is not truth.
A figure without extracted values is not y_true.
```
