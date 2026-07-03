# Codex Prompt — Phygn v4.8 PHI_CURVATURE Minimal Source/y_true Campaign

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
docs/309_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_RESULTS.md
```

Therefore v4.8 starts at:

```txt
310
```

---

# 1. Read first

Read these v4.8 specs:

```txt
docs/310_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_docs/status/GOAL.md
docs/311_PHYGN_V4_8_SOURCE_RESOLUTION_AND_AVAILABILITY_PROTOCOL.md
docs/312_PHYGN_V4_8_OBSERVABLE_AND_YTRUE_QC_PROTOCOL.md
docs/313_PHYGN_V4_8_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/309_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_RESULTS.md
docs/303_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_RESULTS.md
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
docs/291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md
```

---

# 2. First action

Run focused v4.7 validation:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_phi_curvature_screen_loader_v4_7.py tests/test_phi_curvature_source_accessibility_v4_7.py tests/test_phi_curvature_observable_accessibility_v4_7.py tests/test_phi_curvature_ytrue_accessibility_v4_7.py tests/test_phi_curvature_public_dataset_screen_v4_7.py tests/test_phi_curvature_experimental_feasibility_v4_7.py tests/test_phi_curvature_claim_risk_v4_7.py tests/test_phi_curvature_screening_decision_v4_7.py tests/test_phi_curvature_accessibility_campaign_v4_7.py
```

---

# 3. Mission

Implement:

```txt
v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign
```

Do not compute PredictiveGain.
Do not create physical validation.
Do not rebuild the full benchmark pipeline.

---

# 4. Required inputs

Load:

```txt
data/candidate_screening/phi_curvature_screening_decision_v4_7.json
data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json
data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json
data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Inspect:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
data/phi_curvature/
reports/
docs/
```

If v4.7 passed screen is missing:

```txt
PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN
```

---

# 5. Create package

Create:

```txt
phyng/phi_curvature_minimal_campaign/
  __init__.py
  schemas.py
  loader.py
  source_resolution.py
  source_availability.py
  observable_extraction.py
  ytrue_qc.py
  dataset.py
  next_gate.py
  reports.py
  campaign.py
```

Create wrapper:

```txt
phyng/campaigns/phi_curvature_minimal_source_ytrue_campaign.py
```

Entrypoint:

```python
run_phi_curvature_minimal_source_ytrue_campaign(root: str | Path = ".")
```

---

# 6. Source resolution

Resolve or reject seed references:

```txt
Phys. Rev. A 102, 022101
Nature Physics 15, 890
```

Do not fabricate source identity.

If exact identity is unavailable locally:

```txt
REQUIRES_EXTERNAL_LOOKUP
```

A raw citation string is not a source.

---

# 7. Source availability

Check local availability:

```txt
PDFs
supplementary files
external datasets
```

Do not invent file presence.

If missing:

```txt
SOURCE_REQUIRES_DOWNLOAD
SOURCE_REQUIRES_HUMAN_LOOKUP
SUPPLEMENTARY_NOT_FOUND
EXTERNAL_DATASET_NOT_FOUND
```

---

# 8. Observable extraction

Extract candidate observables only from available/resolved source objects.

Allowed classes:

```txt
CURVATURE_PROXY
DECOHERENCE_RATE
PHASE_DECAY_RATE
VISIBILITY
CONTRAST_DECAY
PHASE_SHIFT
NOISE_SPECTRUM
BOUNDARY_RESPONSE
```

If no numeric value:

```txt
NO_NUMERIC_VALUE
```

---

# 9. y_true acceptance

Accept only if:

```txt
value is numeric
unit exists unless explicitly dimensionless
source_hash exists
source location exists
source identity resolved
provenance_status = PROVENANCE_COMPLETE
qc_status in PASS, PASS_WITH_LIMITATIONS
```

For v4.8:

```txt
matched_prediction_placeholder may be true
```

because this is pre-benchmark.

But:

```txt
matched_prediction_placeholder does not allow PredictiveGain.
```

---

# 10. Output files

Create:

```txt
data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json
data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json
data/phi_curvature/evidence/phi_curvature_candidate_observables_v4_8.json
data/phi_curvature/evidence/phi_curvature_ytrue_candidates_v4_8.json
data/phi_curvature/evidence/phi_curvature_accepted_ytrue_v4_8.json
data/phi_curvature/evidence/phi_curvature_rejected_ytrue_v4_8.json
data/phi_curvature/evidence/phi_curvature_evidence_audit_trail_v4_8.json
data/phi_curvature/datasets/phi_curvature_minimal_ytrue_dataset_v4_8.json
data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json
```

---

# 11. Reports

Generate the corresponding markdown reports under:

```txt
reports/phi_curvature/
reports/campaigns/
```

---

# 12. Statuses

Add mappings:

```txt
PHI_CURVATURE_MINIMAL_CAMPAIGN_COMPLETED
PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN
PHI_CURVATURE_MINIMAL_YTRUE_FOUND
PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED
PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN
PHI_CURVATURE_REQUIRES_TARGETED_SOURCE_DOWNLOAD
PHI_CURVATURE_REQUIRES_HUMAN_TABLE_REVIEW
PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES
```

---

# 13. Tests

Create:

```txt
tests/test_phi_curvature_minimal_loader_v4_8.py
tests/test_phi_curvature_source_resolution_v4_8.py
tests/test_phi_curvature_source_availability_v4_8.py
tests/test_phi_curvature_observable_extraction_v4_8.py
tests/test_phi_curvature_ytrue_qc_v4_8.py
tests/test_phi_curvature_minimal_dataset_v4_8.py
tests/test_phi_curvature_next_gate_v4_8.py
tests/test_phi_curvature_minimal_campaign_v4_8.py
```

Minimum tests:

```txt
test_missing_v47_screen_blocks_campaign
test_raw_citation_is_not_source
test_unresolved_source_cannot_enter_extraction
test_missing_local_pdf_requires_download
test_ytrue_requires_numeric_value
test_ytrue_requires_unit_when_dimensional
test_ytrue_requires_location
test_ytrue_requires_hash
test_accepted_ytrue_does_not_create_predictive_gain
test_threshold_reached_requires_three_ytrue
test_no_physical_claim_created
test_phi_gradient_remains_method_only
test_slot4_remains_open_and_scoped
test_reports_include_canonical_status
```

---

# 14. Behavior preservation

Do not alter historical artifacts from v3.9 through v4.7.

---

# 15. Do not overclaim

Do not write:

```txt
PHI_CURVATURE is validated.
PHI_CURVATURE has PredictiveGain.
PHI_CURVATURE is empirically supported beyond accepted y_true records.
Accessibility equals evidence.
Source reference equals source support.
```

Allowed:

```txt
PHI_CURVATURE minimal source/y_true campaign was performed.
Accepted y_true records were added only if QC passed.
PHI_CURVATURE may proceed only according to next gate.
```

---

# 16. Final discipline

```txt
The first real victory is not a prediction.
It is one accepted observed truth.
```
