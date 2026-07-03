# Codex Prompt — Phygn v5.7 Visibility/Decoherence Dataset Expansion

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
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
```

Therefore v5.7 starts at:

```txt
333
```

---

# 1. Read first

Read these v5.7 specs:

```txt
docs/333_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_docs/status/GOAL.md
docs/334_PHYGN_V5_7_DATASET_EXPANSION_PROTOCOL.md
docs/335_PHYGN_V5_7_BENCHMARKING_STACK_HARDENING.md
docs/336_PHYGN_V5_7_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
docs/325_PHYGN_V5_4_LOG_BOUNDARY_PREDICTION_ALIGNMENT_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
docs/323_PHYGN_V5_2_1_LOG_BOUNDARY_OBSERVABLE_LOCATION_REVIEW_RESULTS.md
docs/322_PHYGN_V5_0_TO_V5_3_SOURCE_TO_YTRUE_ROADMAP_RESULTS.md
```

---

# 2. Mission

Implement:

```txt
v5.7 — Visibility/Decoherence Dataset Expansion
```

This is not candidate rescue.

LOG_BOUNDARY remains archived as a validation candidate.

The mission is to expand the empirical y_true domain for visibility/decoherence so future candidates can be judged against stronger data and harder controls.

---

# 3. Hard constraints

Do not reactivate LOG_BOUNDARY as a validation candidate.

Do not run C-structure ablation.

Do not validate Frontera C.

Do not create physical claims.

Do not claim invariant confirmation.

Do not compute Frontera C validation.

Do not treat dataset expansion as PredictiveGain.

Do not treat source identity as evidence.

Do not accept y_true without strict provenance.

---

# 4. Required inputs

Load:

```txt
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json
data/frontera_c/disposition/v5_6_next_research_direction.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_extraction_audit_trail_v5_3.json
data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json
data/frontera_c/source_availability_matrix_v5_2.json
data/real_sources/source_hashes_v3_6.json
```

Inspect local PDFs:

```txt
data/real_sources/pdfs/
```

---

# 5. Target source pool

Start with:

```txt
Hackermueller 2004
Hornberger 2003
Nimmrichter 2011
Pedernales 2019
Schrinski 2020
```

Then create an optional source-lookup queue only if local sources cannot produce enough observable candidates.

---

# 6. Target observables

Search for observed measurement candidates related to:

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
heating_power_W
temperature_K
pressure_mbar
time_s
mass_amu
path_separation_m
velocity_m_s
laser_power_W
material
```

Conditions are not y_true.

---

# 7. Create package

Create or update:

```txt
phyng/dataset_expansion/
  __init__.py
  schemas.py
  source_pool.py
  observable_location_scan.py
  ytrue_extraction.py
  dataset_assembly.py
  dataset_quality.py
  benchmark_readiness.py
  reports.py
  campaign.py
```

Create or update benchmark stack:

```txt
phyng/benchmarking/
  __init__.py
  datasets.py
  metrics.py
  baselines.py
  controls.py
  cross_validation.py
  leakage.py
  reports.py
```

Create wrapper:

```txt
phyng/campaigns/frontera_c_visibility_decoherence_dataset_expansion.py
```

Entrypoint:

```python
run_frontera_c_visibility_decoherence_dataset_expansion_campaign(root: str | Path = ".")
```

---

# 8. Required output data

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_source_pool_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_observable_location_candidates_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_ytrue_candidates_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_accepted_ytrue_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_rejected_ytrue_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json
data/frontera_c/dataset_expansion/v5_7_next_gate_decision.json
```

---

# 9. Required reports

Create:

```txt
reports/frontera_c/dataset_expansion/visibility_decoherence_source_pool_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_observable_location_candidates_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_ytrue_candidates_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_accepted_ytrue_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_rejected_ytrue_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.md
reports/campaigns/FRONTERA-C-VISIBILITY-DECOHERENCE-DATASET-EXPANSION-v5_7.md
```

Create final result document:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
```

---

# 10. Benchmarking stack

Formalize the following dependencies and modules:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
```

Use Pandas/NumPy for data normalization and metrics.

Use Scikit-Learn for baselines, controls, cross-validation and leakage-aware comparison.

Do not use deep learning.

Reason:

```txt
Current problem is evidence, benchmarking and controls, not neural-network capacity.
```

---

# 11. Tests

Create:

```txt
tests/test_visibility_decoherence_source_pool_v5_7.py
tests/test_visibility_decoherence_location_scan_v5_7.py
tests/test_visibility_decoherence_ytrue_extraction_v5_7.py
tests/test_visibility_decoherence_dataset_assembly_v5_7.py
tests/test_visibility_decoherence_dataset_quality_v5_7.py
tests/test_visibility_decoherence_benchmark_readiness_v5_7.py
tests/test_benchmarking_datasets_v5_7.py
tests/test_benchmarking_metrics_v5_7.py
tests/test_benchmarking_controls_v5_7.py
tests/test_frontera_c_visibility_decoherence_dataset_expansion_campaign_v5_7.py
```

Minimum tests:

```txt
test_log_boundary_remains_archived
test_dataset_expansion_is_not_candidate_rescue
test_context_conditions_are_not_ytrue
test_accepted_ytrue_requires_provenance
test_no_physical_claim_created
test_benchmarking_stack_metrics_are_consistent
test_sklearn_baselines_available
test_out_of_source_readiness_requires_two_sources
test_next_gate_decision_matches_counts
test_reports_generated
```

---

# 12. Final statuses

Emit exactly one:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_COMPLETED
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_THRESHOLD_REACHED
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_NEW_OBSERVABLES
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_ACCEPTED_YTRUE
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_REQUIRES_HUMAN_FIGURE_REVIEW
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_REQUIRES_SOURCE_LOOKUP
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

---

# 13. Gate logic

If:

```txt
accepted_ytrue_count_total >= 10
independent_source_count >= 2
```

emit:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_THRESHOLD_REACHED
```

and permit:

```txt
v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If:

```txt
0 < accepted_ytrue_count_total < 10
```

emit:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL
```

and permit only targeted dataset expansion.

If:

```txt
accepted_ytrue_count_total == 0
```

emit a blocking status.

---

# 14. Do not overclaim

Blocked claims:

```txt
Frontera C is validated
LOG_BOUNDARY is restored as active validation candidate
The invariant is empirically confirmed
Dataset expansion equals PredictiveGain
Dataset expansion equals validation
Single-source or in-source benchmark generalizes
```

Allowed claims if true:

```txt
visibility/decoherence source pool was expanded
additional observable locations were found
additional y_true records were accepted
dataset quality was assessed
benchmarking stack was hardened
multi-source benchmark is ready or not ready
```

---

# 15. Acceptance criteria

Complete when:

```txt
v5.6 disposition loaded
LOG_BOUNDARY remains archived
dataset expansion artifacts generated
benchmarking stack hardened
tests pass
reports generated
final result doc 338 generated
no physical claim created
no Frontera C validation created
```

---

# 16. Final discipline

```txt
No more single-source smoke-test authority.
Build the benchmark field before judging candidates again.
```
