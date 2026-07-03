# Codex Prompt — Phygn v1.4 Candidate Model Operationalization

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
v1.3 complete.
Real source candidates are represented.
Manifest draft exists.
Extract targets exist.
Positive Prediction Gate exists.
Kill/Pivot criteria exist.
Current status: POSITIVE_PREDICTION_NOT_OPERATIONALIZED.
Kill/Pivot status: CLAIM_GATING_ARCHITECTURE.
312 tests passed.
```

Important numbering:

```txt
Previous result:
80_PHYGN_V1_3_REAL_SOURCE_SELECTION_AND_POSITIVE_PRESSURE_RESULTS.md

v1.4 docs:
80_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_docs/status/GOAL.md
81_PHYGN_FRONTERA_C_CANDIDATE_TERM_DESIGN.md
82_PHYGN_CANDIDATE_MODEL_FAILURE_CONDITIONS.md
83_PHYGN_CANDIDATE_OBSERVABLE_AND_PARAMETER_PROTOCOL.md
84_PHYGN_CODEX_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_PROMPT.md
```

If numbering collision exists because prior result already uses 80, preserve user numbering and shift v1.4 docs accordingly.

---

# 1. Read first

Read:

```txt
docs/80_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_docs/status/GOAL.md
docs/81_PHYGN_FRONTERA_C_CANDIDATE_TERM_DESIGN.md
docs/82_PHYGN_CANDIDATE_MODEL_FAILURE_CONDITIONS.md
docs/83_PHYGN_CANDIDATE_OBSERVABLE_AND_PARAMETER_PROTOCOL.md
```

Also read:

```txt
docs/79_PHYGN_CODEX_V1_3_REAL_SOURCE_SELECTION_PROMPT.md
docs/80_PHYGN_V1_3_REAL_SOURCE_SELECTION_AND_POSITIVE_PRESSURE_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement v1.4 support for:

```txt
candidate model schemas
candidate term families
candidate admissibility classifier
failure condition evaluator
positive prediction gate integration
kill/pivot status update
reports
tests
```

This phase should move Frontera C from:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

toward:

```txt
POSITIVE_PREDICTION_REQUIRES_EVIDENCE
```

only if a candidate is formally defined.

No physical prediction is unlocked.

---

# 4. New / extended modules

Create or extend:

```txt
phyng/candidates/
  __init__.py
  schemas.py
  term_families.py
  admissibility.py
  failure_conditions.py
  readiness.py
  report.py

phyng/campaigns/candidate_model_operationalization.py
```

Reuse:

```txt
phyng/prediction_pressure/positive_gate.py
phyng/prediction_pressure/kill_criteria.py
```

---

# 5. Candidate term families

Implement candidate families:

```txt
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
```

Each must define:

```txt
candidate_family_id
formula
dimensionless_core
required_parameters
parameter_status
default_admissibility
failure_risks
```

---

# 6. Admissibility classifier

Implement:

```python
classify_candidate_admissibility(...)
```

Rules:

```txt
missing units -> BLOCKED_DIMENSIONAL_INCOMPLETE
free unconstrained parameters -> UNDERIDENTIFIED_CANDIDATE
ad hoc threshold -> BLOCKED_AS_AD_HOC_CANDIDATE
B or QB control with preregistered alpha -> ADMISSIBLE_NEGATIVE_CONTROL
log-boundary with priors -> ADMISSIBLE_TOY_CANDIDATE
source-backed candidate -> REQUIRES_SOURCE_BACKING or better
```

---

# 7. Failure condition evaluator

Implement:

```python
evaluate_candidate_failure_conditions(...)
```

It must detect:

```txt
FAIL_GAIN_NONPOSITIVE
FAIL_UNDETECTABLE_DELTA
FAIL_PARAMETER_UNDERIDENTIFIED
FAIL_AD_HOC_TERM
FAIL_DIMENSIONAL_INVALID
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
```

---

# 8. Positive gate integration

Create at least one default candidate:

```txt
CAND-FC-B-NEGCTRL-001
family = B_SUPPRESSED
observable = visibility_loss
candidate_model = exp(-(Gamma_env + alpha * B)t)
parameter_status = PRE_REGISTERED
data_target = None
benchmark_ids = []
source_ids = []
```

Expected result:

```txt
Positive Prediction Gate:
POSITIVE_PREDICTION_REQUIRES_EVIDENCE
```

not:

```txt
POSITIVE_PREDICTION_READY_FOR_BENCHMARK
```

because source/benchmark evidence is missing.

---

# 9. Kill/pivot update

If candidate exists but lacks evidence:

```txt
status may move from CLAIM_GATING_ARCHITECTURE
to STRUCTURAL_FRAMEWORK_ONLY or CONTINUE_PREDICTIVE_TRACK_PENDING_EVIDENCE
```

But do not claim predictive success.

---

# 10. Reports

Generate:

```txt
reports/candidates/candidate_term_families_v1_4.md
reports/candidates/candidate_admissibility_v1_4.md
reports/prediction_pressure/candidate_failure_conditions_v1_4.md
reports/prediction_pressure/candidate_model_readiness_v1_4.md
reports/campaigns/CANDIDATE-MODEL-OPERATIONALIZATION-v1_4.md
```

---

# 11. Tests

Add:

```txt
tests/test_candidate_term_families_v1_4.py
tests/test_candidate_admissibility_v1_4.py
tests/test_candidate_failure_conditions_v1_4.py
tests/test_candidate_model_readiness_v1_4.py
tests/test_candidate_model_operationalization_campaign_v1_4.py
```

Minimum tests:

```txt
test_candidate_families_exist
test_b_suppressed_candidate_is_negative_control
test_qb_candidate_is_structural_control
test_missing_units_blocks_candidate
test_free_parameters_underidentified
test_ad_hoc_threshold_blocked
test_default_candidate_passes_not_operationalized_to_requires_evidence
test_candidate_without_benchmark_has_fail_no_benchmark
test_candidate_without_sources_has_fail_no_source_support
test_reports_generated
```

---

# 12. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
Frontera C is validated.
Candidate model is physically validated.
Positive prediction achieved.
```

Allowed:

```txt
Frontera C now has an operational toy candidate.
The candidate requires evidence and benchmark.
The candidate has explicit failure modes.
Physical prediction remains blocked.
```

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
candidate families exist
default candidate is generated
admissibility classifier works
failure conditions are explicit
positive prediction gate updates to REQUIRES_EVIDENCE for default candidate
reports generated
physical claims remain blocked
```

---

# 14. Final discipline

```txt
Frontera C has not predicted yet.
But now it has something that can be tested.
```
