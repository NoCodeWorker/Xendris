# Phygn — Tool & Knowledge Self-Provisioning Protocol

## 0. Purpose

This document defines how the agent may acquire or create missing capabilities.

---

## 1. Missing capability types

When a gate fails, classify the missing capability as one of:

```txt
MISSING_THEORY_KNOWLEDGE
MISSING_DOMAIN_KNOWLEDGE
MISSING_SOURCE_ACCESS_TOOL
MISSING_PDF_EXTRACTION_TOOL
MISSING_FIGURE_TABLE_REVIEW_TOOL
MISSING_YTRUE_EXTRACTION_TOOL
MISSING_UNIT_NORMALIZATION_TOOL
MISSING_DATASET_SCHEMA
MISSING_BENCHMARK_TOOL
MISSING_BASELINE_TOOL
MISSING_CANDIDATE_FORMALIZATION
MISSING_PREDICTION_RULE
MISSING_LEAKAGE_TEST
MISSING_NEGATIVE_CONTROL
MISSING_C_ABLATION_TOOL
MISSING_CLAIM_PERMISSION_CHECKER
MISSING_REPORTING_TOOL
MISSING_EXPERIMENT_DESIGN
```

---

## 2. Allowed self-provisioning

The agent may create:

```txt
new Python modules
new schemas
new validators
new benchmark utilities
new leakage tests
new control tests
new ablation utilities
new report generators
new candidate registries
new theory notes
new human review packets
new minimal experiment designs
```

The agent may read and summarize:

```txt
local docs
local papers
local PDFs
local artifacts
local reports
existing theory notes
source metadata
```

The agent may use libraries:

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
networkx if useful for candidate/dependency mapping
sympy if symbolic expression validation is useful
```

---

## 3. Forbidden self-provisioning

The agent must not:

```txt
fabricate papers
fabricate sources
fabricate measurements
invent y_true
invent hashes
invent page numbers
invent physical variables not present or derivable
invent an operational scale L without justification
convert an arbitrary model into a C-structure candidate by naming
use deep learning to bypass lack of theory
use source_id as a target proxy
use target-derived values as features
```

---

## 4. Knowledge acquisition protocol

If knowledge is missing:

```txt
1. Search local docs and reports first.
2. Search local source PDFs if available.
3. Extract minimal theory needed.
4. Create a theory note.
5. State assumptions explicitly.
6. Mark unsupported assumptions as blockers.
7. Continue only if assumptions are sufficient and not ad hoc.
```

Output:

```txt
data/frontera_c/self_provisioning/knowledge_notes_<phase>.json
reports/frontera_c/self_provisioning/knowledge_notes_<phase>.md
```

---

## 5. Tool acquisition protocol

If a tool is missing:

```txt
1. Define the exact function needed.
2. Implement minimal module.
3. Add tests.
4. Run tests.
5. Use the tool only for the active gate.
```

Required record:

```txt
tool_name
blocker_removed
module_path
tests_added
gate_retried
result
```

---

## 6. Candidate formalization protocol

If no candidate exists:

```txt
1. Inspect dataset columns and conditions.
2. Identify available physical variables.
3. Identify unavailable but required variables.
4. Propose candidate families only from available or derivable variables.
5. Reject candidates requiring unavailable variables.
6. Define prediction rules only if they can generate out-of-source predictions.
7. Define baseline and ablation plan before selection.
```

---

## 7. Final principle

```txt
A missing capability is an invitation to build.
A missing evidence object is a reason to stop.
```
