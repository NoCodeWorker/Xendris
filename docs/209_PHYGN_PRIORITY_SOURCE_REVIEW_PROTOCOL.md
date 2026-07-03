# Phygn v3.5 — Priority Source Review Protocol

## 0. Purpose

This document defines how the priority source review must be executed.

v3.5 must not attempt to review all sources.

It must target the minimum set that can decide whether PHI_GRADIENT has any real source-pressure path.

---

## 1. Priority source table

| Priority | Source ID | Primary Role | Secondary Role | Risk |
|---:|---|---|---|---|
| 1 | `SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE` | Observable / baseline | Visibility decay | Not PHI_GRADIENT component |
| 2 | `SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE` | Baseline / negative | Thermal decoherence | Environmental dominance |
| 3 | `SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST` | Benchmark / parameter | Collapse-model pressure | Not direct alpha |
| 4 | `SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` | Benchmark / exclusion | Quantum-classical boundary | May be negative |
| 5 | `SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING` | Possible gradient component | Interferometry dynamics | High analogy-only risk |

---

## 2. Required review questions

For each source, answer:

```txt
Does the source contain an explicit observable?
Does it contain a decoherence or visibility equation?
Does it contain a mass/length/time/visibility range?
Does it contain a parameter constraint or exclusion?
Does it contain a gradient/transition/effective operator relevant to PHI_GRADIENT?
Does it contradict, constrain or weaken the candidate?
Does it only sound adjacent?
```

---

## 3. Source text availability

Each source must be classified as:

```txt
SOURCE_TEXT_AVAILABLE_LOCAL
SOURCE_TEXT_AVAILABLE_URL
SOURCE_TEXT_AVAILABLE_ARXIV
SOURCE_TEXT_AVAILABLE_DOI
SOURCE_TEXT_UNAVAILABLE
SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD
```

If unavailable:

```txt
do not invent content
create unresolved exact-fill record
```

---

## 4. Exact fill record

Each priority source must produce one of:

```txt
EXACT_FILL_READY
EXACT_FILL_PARTIAL
EXACT_FILL_REQUIRES_SOURCE_TEXT
EXACT_FILL_REJECTED_ANALOGY_ONLY
EXACT_FILL_NEGATIVE_CANDIDATE
EXACT_FILL_NO_VALIDATABLE_CONTENT
```

---

## 5. SLOT_4 special caution

SLOT_4 is the key bottleneck.

A gradient-like source must be rejected or marked analogy-only unless it contains:

```txt
explicit gradient/transition/effective operator
and
a connection to decoherence, rate, visibility, interferometry or effective dynamics
```

Physical field gradients alone do not automatically support PHI_GRADIENT.

---

## 6. Negative-source priority

Do not hide negative sources.

If a source shows that environmental decoherence explains the relevant observable fully, record:

```txt
NEGATIVE_ENVIRONMENTAL_DOMINANCE_CANDIDATE
```

If a parameter regime is excluded, record:

```txt
NEGATIVE_PARAMETER_EXCLUSION_CANDIDATE
```

---

## 7. Final principle

```txt
A priority source is valuable when it can decide a bottleneck.
```
