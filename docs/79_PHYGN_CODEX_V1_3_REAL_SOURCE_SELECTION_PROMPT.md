# Codex Prompt — Phygn v1.3 Real Source Selection & Positive Prediction Pressure

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v1.2 complete.
Source pack templates exist.
Manifest template exists.
Extract templates exist.
Template extracts are marked TEMPLATE_NOT_EVIDENCE.
Readiness remains false.
No physical claim is unlocked.
299 tests passed.
```

Important numbering:

```txt
Previous result:
73_PHYGN_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_RESULTS.md

v1.3 docs:
74_PHYGN_V1_3_REAL_SOURCE_SELECTION_AND_POSITIVE_PRESSURE_docs/status/GOAL.md
75_PHYGN_BASELINE_REAL_SOURCE_CANDIDATES.md
76_PHYGN_FILLED_SOURCE_MANIFEST_DRAFT.md
77_PHYGN_REAL_EXTRACT_TARGETS.md
78_PHYGN_POSITIVE_PREDICTION_PRESSURE_AND_KILL_CRITERIA.md
79_PHYGN_CODEX_V1_3_REAL_SOURCE_SELECTION_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/74_PHYGN_V1_3_REAL_SOURCE_SELECTION_AND_POSITIVE_PRESSURE_docs/status/GOAL.md
docs/75_PHYGN_BASELINE_REAL_SOURCE_CANDIDATES.md
docs/76_PHYGN_FILLED_SOURCE_MANIFEST_DRAFT.md
docs/77_PHYGN_REAL_EXTRACT_TARGETS.md
docs/78_PHYGN_POSITIVE_PREDICTION_PRESSURE_AND_KILL_CRITERIA.md
```

Also read:

```txt
docs/72_PHYGN_CODEX_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_PROMPT.md
docs/73_PHYGN_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_RESULTS.md
```

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

# 3. Mission

Implement v1.3 support for:

```txt
real source candidate records
manifest draft writing
source acquisition checklist
extract target generation
positive prediction gate
kill/pivot criteria
reports
tests
```

This phase may prepare a manifest draft.

It must not claim local sources are ingested unless files exist and audit passes.

# 4. New / extended modules

Create or extend:

```txt
phyng/evidence/real_source_candidates.py
phyng/evidence/manifest_draft_writer.py
phyng/evidence/extract_target_generator.py
phyng/campaigns/real_source_selection.py

phyng/prediction_pressure/
  __init__.py
  schemas.py
  positive_gate.py
  kill_criteria.py
  report.py
```

# 5. Real source candidate behavior

Implement:

```python
get_baseline_real_source_candidates() -> list[RealSourceCandidate]
```

Fields:

```txt
source_candidate_id
slot
title
authors
year
url
intended_support_types
trust_level
verification_status
local_file_status
notes
```

Candidate states:

```txt
CANDIDATE_ONLY
NEEDS_LOCAL_FILE
NEEDS_METADATA_VERIFICATION
READY_FOR_MANIFEST_DRAFT
READY_FOR_EXTRACTION
```

# 6. Manifest draft writer

Implement:

```python
write_filled_manifest_draft(project_root: Path) -> Path
```

It may write:

```txt
sources/baseline/source_manifest_draft_v1_3.json
```

or update:

```txt
sources/baseline/source_manifest.json
```

depending on existing files.

No fake local ingestion.

If local file does not exist:

```txt
local_file_status = MISSING
```

# 7. Extract target generator

Generate target files or plans:

```txt
sources/baseline/notes/extract_targets_v1_3.md
```

It must list:

```txt
claim target
support type
what to look for
what not to infer
forbidden overclaims
```

# 8. Positive Prediction Gate

Implement:

```python
evaluate_positive_prediction_gate(candidate: CandidatePredictionSpec) -> PositivePredictionGateResult
```

Required fields:

```txt
observable
baseline_model
candidate_model
candidate_term
parameters
data_target
error_metric
expected_pattern
detectability_threshold
failure_condition
```

If any are missing:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

If all present but no source/benchmark:

```txt
POSITIVE_PREDICTION_REQUIRES_EVIDENCE
```

If complete:

```txt
POSITIVE_PREDICTION_READY_FOR_BENCHMARK
```

# 9. Kill / pivot criteria

Implement:

```python
evaluate_kill_or_pivot(...)
```

Possible outputs:

```txt
CONTINUE_PREDICTIVE_TRACK
NEGATIVE_FILTER_ONLY
STRUCTURAL_FRAMEWORK_ONLY
CLAIM_GATING_ARCHITECTURE
NOT_PREDICTIVE_CURRENTLY
```

Rules:

```txt
negative bounds only + no candidate + no gain -> NOT_PREDICTIVE_CURRENTLY
claim blocking useful -> CLAIM_GATING_ARCHITECTURE
structural atlas useful -> STRUCTURAL_FRAMEWORK_ONLY
detectable candidate exists -> CONTINUE_PREDICTIVE_TRACK
```

# 10. Reports

Generate:

```txt
reports/rag/real_source_candidates_v1_3.md
reports/rag/filled_manifest_draft_v1_3.md
reports/rag/extract_targets_v1_3.md
reports/prediction_pressure/positive_prediction_gate_v1_3.md
reports/prediction_pressure/kill_pivot_criteria_v1_3.md
reports/campaigns/REAL-SOURCE-SELECTION-v1_3.md
```

# 11. Tests

Add:

```txt
tests/test_real_source_candidates_v1_3.py
tests/test_manifest_draft_writer_v1_3.py
tests/test_extract_target_generator_v1_3.py
tests/test_positive_prediction_gate_v1_3.py
tests/test_kill_pivot_criteria_v1_3.py
tests/test_real_source_selection_campaign_v1_3.py
```

Minimum tests:

```txt
test_real_candidates_exist
test_candidates_are_not_ingested
test_manifest_draft_does_not_mark_sources_ingested
test_missing_local_files_keep_missing_status
test_extract_targets_include_forbidden_overclaims
test_positive_gate_missing_fields_blocks
test_positive_gate_complete_requires_evidence
test_kill_criteria_negative_only_not_predictive
test_kill_criteria_detectable_candidate_continues
test_reports_generated
```

# 12. Do not overclaim

Do not write:

```txt
baseline is source-backed
Frontera C is validated
Phygn predicts decoherence
candidate is validated
```

Allowed:

```txt
real source candidates are selected
manifest draft is prepared
positive prediction gate is defined
Frontera C may be demoted if no positive candidate appears
```

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
real source candidates are represented
manifest draft generated
extract targets generated
positive prediction gate implemented
kill/pivot criteria implemented
reports generated
sources remain candidate-only unless local files/audit exist
no physical claim is unlocked
```

# 14. Final discipline

```txt
A theory that cannot risk losing cannot earn the right to win.
```
