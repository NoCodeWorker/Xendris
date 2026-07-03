# Codex Prompt — Phygn v4.9 Candidate Source Identity Preflight Gate

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
docs/315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md
```

Therefore v4.9 starts at:

```txt
316
```

---

# 1. Read first

Read these v4.9 specs:

```txt
docs/316_PHYGN_V4_9_SOURCE_IDENTITY_PREFLIGHT_docs/status/GOAL.md
docs/317_PHYGN_V4_9_SOURCE_IDENTITY_PROTOCOL.md
docs/318_PHYGN_V4_9_OBSERVABLE_YTRUE_PREFLIGHT_PROTOCOL.md
docs/319_PHYGN_V4_9_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md
docs/309_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_RESULTS.md
docs/303_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_RESULTS.md
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
```

---

# 2. First action

Run focused v4.8 validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_phi_curvature_minimal_loader_v4_8.py tests/test_phi_curvature_source_resolution_v4_8.py tests/test_phi_curvature_source_availability_v4_8.py tests/test_phi_curvature_observable_extraction_v4_8.py tests/test_phi_curvature_ytrue_qc_v4_8.py tests/test_phi_curvature_minimal_dataset_v4_8.py tests/test_phi_curvature_next_gate_v4_8.py tests/test_phi_curvature_minimal_campaign_v4_8.py
```

Expected recent result:

```txt
v4.8 tests pass.
```

---

# 3. Mission

Implement:

```txt
v4.9 — Candidate Source Identity Preflight Gate
```

This is a preflight gate before any new candidate-family screening or minimal campaign.

Do not compute PredictiveGain.

Do not create y_true.

Do not create physical validation.

---

# 4. Required inputs

Load:

```txt
data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json
data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json
data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Optionally inspect:

```txt
data/synthetic_benchmark_design/
data/closed_loop/
data/source_pressure/
data/benchmarks/
data/real_sources/
reports/
docs/
```

If prior results are missing:

```txt
PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS
```

---

# 5. Create package

Create:

```txt
phyng/source_identity_preflight/
  __init__.py
  schemas.py
  loader.py
  inventory.py
  identity_resolution.py
  availability.py
  observable_identity.py
  ytrue_path.py
  decision.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phygn_source_identity_preflight.py
```

Entrypoint:

```python
run_phygn_source_identity_preflight_campaign(root: str | Path = ".")
```

---

# 6. Candidate families

Screen at least:

```txt
PHI_CURVATURE
PHI_LOCALIZED_WINDOW
PHI_BANDPASS
PHI_GRADIENT
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
```

Preserve:

```txt
PHI_GRADIENT = METHOD_ONLY_EMPIRICALLY_UNGROUNDED
PHI_CURVATURE = REJECTED_NO_RESOLVABLE_SOURCES unless new source identity is found
```

---

# 7. Source identity

A candidate cannot pass from raw source strings alone.

Complete identity requires:

```txt
source_id
title or exact citation identity
publication/year
DOI/arXiv/URL/local_hash
```

If unknown:

```txt
REQUIRES_HUMAN_LOOKUP
```

not optimistic pass.

---

# 8. Observable/y_true preflight

For each candidate with resolvable identity, evaluate:

```txt
source-locatable observables
numeric value expectation
unit expectation
plausible y_true path
```

No y_true is accepted in v4.9.

This is only preflight.

---

# 9. Output files

Create:

```txt
data/preflight/source_identity/candidate_family_source_inventory_v4_9.json
data/preflight/source_identity/source_identity_resolution_matrix_v4_9.json
data/preflight/source_identity/source_availability_matrix_v4_9.json
data/preflight/source_identity/observable_identity_matrix_v4_9.json
data/preflight/source_identity/ytrue_path_plausibility_matrix_v4_9.json
data/preflight/source_identity/candidate_preflight_decision_matrix_v4_9.json
data/preflight/source_identity/source_identity_preflight_gate_v4_9.json
```

---

# 10. Reports

Generate:

```txt
reports/preflight/source_identity/candidate_family_source_inventory_v4_9.md
reports/preflight/source_identity/source_identity_resolution_matrix_v4_9.md
reports/preflight/source_identity/source_availability_matrix_v4_9.md
reports/preflight/source_identity/observable_identity_matrix_v4_9.md
reports/preflight/source_identity/ytrue_path_plausibility_matrix_v4_9.md
reports/preflight/source_identity/candidate_preflight_decision_matrix_v4_9.md
reports/preflight/source_identity/source_identity_preflight_gate_v4_9.md
reports/campaigns/PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9.md
```

---

# 11. Statuses

Add mappings:

```txt
PHYGN_SOURCE_IDENTITY_PREFLIGHT_COMPLETED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS
PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_SOURCE_ACQUISITION
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_HUMAN_LOOKUP
```

---

# 12. Tests

Create:

```txt
tests/test_source_identity_preflight_loader_v4_9.py
tests/test_candidate_family_source_inventory_v4_9.py
tests/test_source_identity_resolution_matrix_v4_9.py
tests/test_source_availability_matrix_v4_9.py
tests/test_observable_identity_matrix_v4_9.py
tests/test_ytrue_path_plausibility_matrix_v4_9.py
tests/test_candidate_preflight_decision_matrix_v4_9.py
tests/test_source_identity_preflight_gate_v4_9.py
tests/test_phygn_source_identity_preflight_campaign_v4_9.py
```

Minimum tests:

```txt
test_missing_prior_results_blocks_preflight
test_raw_citation_string_cannot_pass_candidate
test_identity_requires_locator_or_local_hash
test_candidate_fails_without_resolvable_sources
test_candidate_partial_requires_human_lookup
test_ytrue_path_cannot_be_medium_without_source_identity
test_phi_gradient_remains_method_only
test_phi_curvature_reflects_v48_rejection
test_no_ytrue_created
test_no_predictive_gain_created
test_no_physical_claim_created
test_reports_include_canonical_status
```

---

# 13. Behavior preservation

Do not alter:

```txt
v4.8 PHI_CURVATURE minimal campaign
v4.7 PHI_CURVATURE accessibility screen
v4.6 candidate freeze review
v4.5 external evidence
v4.4.2 audit remediation
v4.4 manual extraction
v4.3 y_true extraction
v4.2 observable plan
v4.1 model comparison
v4.0 benchmark construction
v3.9 source pressure
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Candidate passed preflight, therefore evidence exists.
Source identity creates source support.
Source identity creates y_true.
Source identity creates PredictiveGain.
Candidate selected means validated.
```

Allowed:

```txt
Candidate families were screened for resolvable source identity.
A candidate may proceed only if source identity and y_true path plausibility survive preflight.
```

---

# 15. Acceptance criteria

Complete when:

```txt
prior results loaded
v4.9 tests pass
source inventory generated
source identity matrix generated
source availability matrix generated
observable identity matrix generated
y_true path plausibility matrix generated
candidate decision matrix generated
gate decision generated
reports generated
no y_true created
no PredictiveGain created
no physical claim upgraded
PHI_GRADIENT remains method-only
PHI_CURVATURE remains blocked unless source identity is newly resolved
```

---

# 16. Final discipline

```txt
No source identity, no science pipeline.
```
