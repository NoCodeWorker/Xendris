# Phygn v3.5 — Priority Exact Extract Fill: Baseline, Benchmark & Gradient Review Goal

## 0. Context

The latest confirmed document is:

```txt
207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
```

Therefore, v3.5 starts at:

```txt
208
```

v3.4 generated exact-extract review templates but did not resolve manual review debt.

v3.4 final status:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
```

Current state:

```txt
validation_ready_extracts = 0
manual_review_debt_before = 8
manual_review_debt_after = 8
real_source_support = 0
benchmark_support = 0
physical_claims_blocked = true
```

v3.5 now prioritizes and fills exact extracts for the minimum source-pressure path.

---

## 1. Core thesis

```txt
The first real positive will not come from more architecture.
It will come from one exact extract that survives pain.
```

v3.5 is not a validation gate.

It is an exact-fill campaign.

It prepares the evidence material that v3.6 can validate.

---

## 2. Hard rule

```txt
No fabricated quote.
No fabricated equation.
No fabricated page, section, table or figure.
No fabricated parameter range.
No physical claim.
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
previous_status: PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
current_evidence: SYNTHETIC_ONLY
```

---

## 4. Priority review objective

v3.5 must focus on the minimum useful set, not the whole bibliography.

Priority sources:

```txt
1. SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE
2. SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
3. SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST
4. SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS
5. SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

Priority slots:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
SLOT_4_GRADIENT_TRANSITION_OPERATORS
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
```

---

## 5. Why these sources

### Hornberger 2003

Purpose:

```txt
visibility/decoherence observable
environmental baseline
interferometry contact
```

### Hackermüller 2004

Purpose:

```txt
thermal-emission decoherence baseline
environmental dominance pressure
negative-source candidate
```

### Nimmrichter 2011

Purpose:

```txt
matter-wave benchmark constraints
collapse/localization parameter pressure
alpha-like constraint analogue
```

### Schrinski 2020

Purpose:

```txt
quantum-classical hypothesis tests
benchmark scoring
parameter exclusion pressure
```

### Pedernales 2019

Purpose:

```txt
possible gradient/transition component
high analogy-only risk
critical SLOT_4 test
```

---

## 6. v3.5 output files

Create:

```txt
data/real_sources/extracts/phi_gradient_priority_exact_extracts_v3_5.json
data/real_sources/extracts/phi_gradient_priority_exact_extract_locations_v3_5.json
data/real_sources/extracts/phi_gradient_priority_equation_observable_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_parameter_range_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_review_notes_v3_5.md
```

If exact source text is unavailable, produce structured unresolved records with:

```txt
review_status = EXACT_EXTRACT_REQUIRES_SOURCE_TEXT
validation_ready = false
```

---

## 7. Possible v3.5 statuses

```txt
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_COMPLETED
PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL
PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED
```

---

## 8. What v3.5 may allow

Allowed:

```txt
Priority exact extract fill was attempted.
Some exact extracts are validation-ready.
Some sources remain unresolved.
SLOT_4 may be flagged as analogy-only risk.
```

Blocked:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT physical validation
Frontera C validation
```

Those belong to the next validation gate.

Recommended next phase:

```txt
v3.6 — Priority Exact Extract Validation & First Source-Pressure Decision
```

---

## 9. Acceptance criteria

v3.5 is complete when:

```txt
priority sources selected
exact-fill schema implemented
source-text availability checked
unresolved records created if exact text unavailable
no quote/equation/range fabricated
maps generated
manual review debt reduced or explicitly preserved
reports generated
tests pass
physical claims remain blocked
```

---

## 10. Final principle

```txt
The smallest useful exact extract is worth more than a large decorative bibliography.
```
