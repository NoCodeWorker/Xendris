# Phygn v3.3 — Extract Validation Decision Rules

## 0. Purpose

This document defines the decision rules for validating v3.2 source-pack extracts.

The objective is to distinguish:

```txt
support
benchmark pressure
contradiction
analogy-only
not comparable
manual-review required
```

---

## 1. Extract validation statuses

Allowed statuses:

```txt
EXTRACT_VALID_SUPPORTS_OBSERVABLE
EXTRACT_VALID_SUPPORTS_BASELINE
EXTRACT_VALID_SUPPORTS_COMPONENT
EXTRACT_VALID_CONSTRAINS_PARAMETER
EXTRACT_VALID_PROVIDES_BENCHMARK_DATA
EXTRACT_VALID_CONTRADICTS_CANDIDATE
EXTRACT_REJECTED_ANALOGY_ONLY
EXTRACT_REJECTED_NO_COMPONENT_SUPPORT
EXTRACT_REJECTED_NO_OBSERVABLE
EXTRACT_REJECTED_NOT_COMPARABLE
EXTRACT_REQUIRES_MANUAL_REVIEW
```

---

## 2. Manual-review rule

If an extract has:

```txt
manual_review_required = true
```

and no exact quote, equation, observable, benchmark table, or parameter constraint has been manually confirmed, then default to:

```txt
EXTRACT_REQUIRES_MANUAL_REVIEW
```

It may not count as support.

---

## 3. Observable/baseline support rule

To validate as observable/baseline support, require at least one:

```txt
explicit visibility/fringe/contrast observable
decoherence rate equation
environmental decoherence model
Gamma_env-like baseline rate
experimentally measured visibility loss
```

Valid statuses:

```txt
EXTRACT_VALID_SUPPORTS_OBSERVABLE
EXTRACT_VALID_SUPPORTS_BASELINE
```

---

## 4. Component support rule

To validate as PHI_GRADIENT component support, require:

```txt
explicit gradient/transition/boundary operator
and connection to rate, decoherence, visibility, interferometry, or effective dynamics
```

Reject if:

```txt
gradient is only a physical field gradient unrelated to candidate structure
gradient appears only as optimization language
boundary is metaphorical
transition is conceptual only
```

Possible statuses:

```txt
EXTRACT_VALID_SUPPORTS_COMPONENT
EXTRACT_REJECTED_ANALOGY_ONLY
EXTRACT_REJECTED_NO_COMPONENT_SUPPORT
```

---

## 5. Parameter constraint rule

To validate alpha-like pressure, require:

```txt
parameter bound
coupling constraint
rate-ratio constraint
collapse-model parameter exclusion
environmental dominance constraint
```

Valid status:

```txt
EXTRACT_VALID_CONSTRAINS_PARAMETER
```

---

## 6. Benchmark data rule

To validate benchmark support, require:

```txt
observable
mass range
length/separation range
time range
visibility/decoherence measure
limitation notes
source traceability
```

If source is a proposal, it may be:

```txt
BENCHMARK_CANDIDATE_ONLY
```

but not:

```txt
EXTRACT_VALID_PROVIDES_BENCHMARK_DATA
```

unless comparable values are extracted.

---

## 7. Negative-source rule

If an extract shows:

```txt
environmental baseline dominates candidate effect
candidate parameter range is excluded
observable mismatch is unavoidable
benchmark range is incompatible
model mechanism conflicts with candidate
```

then mark:

```txt
EXTRACT_VALID_CONTRADICTS_CANDIDATE
```

Negative evidence must not be ignored.

---

## 8. Analogy rejection rule

Reject as analogy-only if the extract contains only:

```txt
decoherence vocabulary
boundary metaphor
gradient vocabulary
scale/log terminology
quantum-classical transition language
without a component constraint
```

Status:

```txt
EXTRACT_REJECTED_ANALOGY_ONLY
```

---

## 9. Final principle

```txt
A source extract validates by constraining a component, not by sounding adjacent.
```
