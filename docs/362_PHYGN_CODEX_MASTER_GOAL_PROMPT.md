# Codex Master Goal Prompt — Advance Phygn to Frontera C Validation Decision

You are working in:

```txt
D:\BIOCULTOR\PHYNG
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Latest confirmed result:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
```

Current verified state:

```txt
TARGETED_YTRUE_EXTRACTION_PARTIAL
observed_candidates_evaluated = 10
new_accepted_ytrue = 3
rejected_ytrue_candidates = 7
total_accepted_ytrue = 7
independent_source_count = 4
benchmark_readiness = PARTIAL_MULTI_SOURCE_N_SMALL
```

Current blocker:

```txt
MISSING_EXPERIMENTAL_DATA
MISSING_BENCHMARK
```

Current allowed next phase:

```txt
v5.7.4 — Targeted Human Figure/Table Review or Additional Source Download & y_true Expansion
```

---

# MASTER GOAL

Advance Phygn autonomously from the current partial multi-source y_true dataset to a Frontera C validation decision.

The terminal result must be exactly one of:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_NO_PREDICTIVE_GAIN
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
NO_CANDIDATE_WITH_REALITY_CONTACT
```

Do not force validation.

Reach validation only if every gate permits it.

If a gate fails, stop with the exact blocker.

---

# READ FIRST

Read these master roadmap documents:

```txt
docs/357_PHYGN_MASTER_GOAL_FRONTERA_C_VALIDATION_OR_BLOCKAGE.md
docs/358_PHYGN_AUTONOMOUS_ROADMAP_V57_4_TO_V64.md
docs/359_PHYGN_RAILWAYS_GATES_AND_TERMINAL_STATES.md
docs/360_PHYGN_TECHNICAL_ARCHITECTURE_AND_LIBRARIES.md
docs/361_PHYGN_CANDIDATE_STRATEGY_AND_VALIDATION_CRITERIA.md
```

Also read recent results:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
docs/350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md
docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
docs/326_PHYGN_V5_5_LOG_BOUNDARY_NEGATIVE_CONTROLS_RESULTS.md
docs/324_PHYGN_V5_3_LOG_BOUNDARY_ACCEPTED_YTRUE_EXTRACTION_RESULTS.md
```

---

# AUTONOMOUS ROADMAP

Execute autonomously, but only if each gate permits the next:

```txt
v5.7.4  Targeted Human Figure/Table Review & Missing Source Completion
v5.8    Multi-Source Benchmark & Out-of-Source Control Gate
v5.9    Candidate Family Reprioritization Against Expanded Dataset
v6.0    Candidate Prediction Alignment & PredictiveGain Gate
v6.1    Negative Controls, Leakage and Simplicity Tests
v6.2    C-Structure Ablation Gate
v6.3    Scientific Debt and Claim Permission Gate
v6.4    Frontera C Validation Candidate Report or Terminal Block
```

You may create intermediate sub-phases if required by evidence blockers, but do not create architecture-only phases that do not remove a blocker or produce external/empirical data.

---

# CURRENT IMMEDIATE TASK

First reach benchmark threshold:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

Current:

```txt
total_accepted_ytrue_count = 7
independent_source_count = 4
```

Need:

```txt
at least 3 additional accepted y_true
```

Use:

```txt
rejected v5.7.3 candidates
human figure/table review
missing source completion
supplementary data acquisition
additional source download if necessary
```

Do not move to v5.8 until threshold is reached.

---

# SCIENTIFIC STACK

Use and harden:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
pymupdf
pdfplumber
pypdf
```

Use:

```txt
Pandas/NumPy for dataset assembly, normalization and metrics.
Scikit-Learn for baselines, controls, cross-validation and leakage tests.
Pydantic for artifact schemas.
pytest for gate tests.
```

Do not use PyTorch/TensorFlow unless the dataset becomes large enough and simple baselines are exhausted.

---

# HARD CONSTRAINTS

Never:

```txt
fabricate sources
fabricate PDFs
fabricate hashes
fabricate values
fabricate units
fabricate y_true
fabricate page/table/figure IDs
compute PredictiveGain without benchmark-ready accepted y_true
run C-structure ablation before positive PredictiveGain survives controls
reactivate LOG_BOUNDARY as validation candidate
claim validation from single-source or N-small data
treat source identity as evidence
treat observable location as y_true
treat y_true as PredictiveGain
treat PredictiveGain as validation
hide failed controls
skip leakage tests
skip C-structure ablation
```

---

# LOG_BOUNDARY STATUS

LOG_BOUNDARY remains:

```txt
ARCHIVED_AS_VALIDATION_CANDIDATE
```

Allowed only as:

```txt
benchmark fixture
negative-control fixture
pipeline regression fixture
```

Do not use LOG_BOUNDARY as active validation candidate unless explicit reopen criteria are met:

```txt
at least 2 independent sources
at least 10 accepted y_true
out-of-source evaluation
negative controls survive
simple controls no longer explain gain
```

---

# VALIDATION CONDITIONS

Only emit:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
```

if all are true:

```txt
dataset threshold reached
benchmark readiness passed
candidate family selected
baseline and candidate predictions complete
PredictiveGain > 0
negative controls survived
leakage tests survived
C-structure ablation survived
scientific debt does not block scoped claim
claim permission explicitly allows limited validation-candidate report
```

---

# FINAL OUTPUT

When autonomous execution stops, create a final master decision document:

```txt
docs/PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md
```

It must include:

```txt
final terminal status
last completed gate
first failed gate if any
accepted_ytrue_count
independent_source_count
dataset version
candidate family tested
baseline model
candidate model
PredictiveGain if computed
negative-control result
C-structure ablation result
scientific debt status
allowed claims
blocked claims
next required human action if any
```

---

# FINAL DISCIPLINE

```txt
The AI may run fast.
The gates must not.

No y_true, no benchmark.
No benchmark, no PredictiveGain.
No PredictiveGain, no validation.
No controls, no trust.
No C-ablation, no Frontera C claim.
```
