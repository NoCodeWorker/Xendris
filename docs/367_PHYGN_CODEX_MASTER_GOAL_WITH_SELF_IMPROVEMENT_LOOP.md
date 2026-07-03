# Codex Master Goal Prompt — Frontera C Validation Decision with Evidence-Gated Self-Improvement Loop

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

Current immediate objective:

```txt
Reach total_accepted_ytrue_count >= 10 while preserving independent_source_count >= 2.
```

Current need:

```txt
At least 3 additional accepted y_true records.
```

---

# MASTER GOAL

Advance Phygn autonomously from the current partial multi-source y_true dataset to a Frontera C validation decision.

Do not force validation.

Reach validation only if every gate permits it.

If a gate fails, classify the blocker, attempt bounded self-improvement if appropriate, re-run the gate, and stop honestly if the blocker persists.

The final terminal result must be exactly one of:

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
SELF_IMPROVEMENT_LOOP_EXHAUSTED
```

---

# READ FIRST

Read these master documents:

```txt
docs/357_PHYGN_MASTER_GOAL_FRONTERA_C_VALIDATION_OR_BLOCKAGE.md
docs/358_PHYGN_AUTONOMOUS_ROADMAP_V57_4_TO_V64.md
docs/359_PHYGN_RAILWAYS_GATES_AND_TERMINAL_STATES.md
docs/360_PHYGN_TECHNICAL_ARCHITECTURE_AND_LIBRARIES.md
docs/361_PHYGN_CANDIDATE_STRATEGY_AND_VALIDATION_CRITERIA.md
docs/364_PHYGN_EVIDENCE_GATED_SELF_CORRECTION_LOOP.md
docs/365_PHYGN_BLOCKER_TAXONOMY_AND_MINIMAL_IMPROVEMENT_PROTOCOL.md
docs/366_PHYGN_SCIENTIFIC_VIBE_CODING_RUNTIME_ARCHITECTURE.md
```

Also read latest result chain:

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

Proceed autonomously through:

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

You may create intermediate sub-phases only if they remove a blocker or produce/validate empirical data.

Do not create architecture-only phases.

---

# EVIDENCE-GATED SELF-CORRECTION LOOP

For each active gate:

```txt
1. Execute the gate.
2. If the gate passes, advance.
3. If the gate fails, identify the exact blocker.
4. Classify blocker type.
5. Decide whether it is removable by code, data work, source acquisition, human review, or experiment design.
6. If removable by software/data work, implement the smallest valid improvement.
7. Add/update tests.
8. Re-run the same gate.
9. Continue only if the gate passes.
10. If the same blocker persists after 3 cycles, stop with SELF_IMPROVEMENT_LOOP_EXHAUSTED and exact blocker.
```

Blocker types:

```txt
KNOWLEDGE_BLOCKER
TOOLING_BLOCKER
SOURCE_IDENTITY_BLOCKER
SOURCE_AVAILABILITY_BLOCKER
OBSERVABLE_LOCATION_BLOCKER
YTRUE_BLOCKER
DATASET_THRESHOLD_BLOCKER
BENCHMARK_BLOCKER
MODEL_BLOCKER
PREDICTIVE_GAIN_BLOCKER
CONTROL_BLOCKER
LEAKAGE_BLOCKER
ABLATION_BLOCKER
SCIENTIFIC_DEBT_BLOCKER
CLAIM_PERMISSION_BLOCKER
HUMAN_REVIEW_BLOCKER
EXTERNAL_SOURCE_BLOCKER
EXPERIMENT_REQUIRED_BLOCKER
TEST_BLOCKER
```

Maximum cycles:

```txt
max_self_improvement_cycles_per_gate = 3
```

---

# IMMEDIATE FIRST GATE

Current dataset:

```txt
total_accepted_ytrue_count = 7
independent_source_count = 4
benchmark_readiness = PARTIAL_MULTI_SOURCE_N_SMALL
```

First gate:

```txt
dataset threshold gate
```

Threshold:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

Actions permitted:

```txt
review rejected v5.7.3 candidates
perform human figure/table review if possible
complete missing source objects
extract additional y_true under strict QC
download supplementary data if explicitly referenced
create human review packet if values cannot be extracted automatically
```

Do not proceed to v5.8 until threshold is reached.

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
Pydantic for schemas.
pytest for gates and regressions.
PyMuPDF/pdfplumber/pypdf for PDF extraction and location review.
```

Do not use PyTorch/TensorFlow unless:

```txt
accepted_ytrue_count is much larger
simple baselines are exhausted
out-of-source validation exists
controls survive
nonlinear learning is scientifically justified
```

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
build benchmark before dataset threshold
run C-structure ablation before positive PredictiveGain survives controls
reactivate LOG_BOUNDARY as validation candidate
claim validation from single-source or N-small data
treat source identity as evidence
treat observable location as y_true
treat accepted y_true as PredictiveGain
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

Do not reactivate LOG_BOUNDARY unless explicit reopen criteria are met:

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

# REQUIRED FINAL MASTER REPORT

When autonomous execution stops, create:

```txt
docs/PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md
```

It must include:

```txt
final terminal status
last completed gate
first failed gate if any
blocker type
self-improvement cycles used
accepted_ytrue_count
independent_source_count
dataset version
candidate family tested
baseline model
candidate model
PredictiveGain if computed
negative-control result
leakage result
C-structure ablation result
scientific debt status
allowed claims
blocked claims
next required human action if any
experiment requirement if any
```

---

# FINAL DISCIPLINE

```txt
The AI may run fast.
The gates must not.

The AI may self-correct the software.
It may not self-authorize the science.

No y_true, no benchmark.
No benchmark, no PredictiveGain.
No PredictiveGain, no validation.
No controls, no trust.
No C-ablation, no Frontera C claim.
```
