# Phygn v2.8 — Source Support vs Analogy Gate

## 0. Purpose

This document defines the gate that distinguishes genuine source support from decorative analogy.

---

## 1. Core rule

```txt
A source supports PHI_GRADIENT only if it constrains a component of the candidate.
```

A source is analogy-only if it merely resembles the candidate in vocabulary or broad concept.

---

## 2. Source candidate schema

```python
class SourceCandidate(BaseModel):
    source_id: str
    title: str
    authors: list[str]
    year: int | None
    source_type: str
    url_or_path: str | None
    slot_ids: list[str]
    extracted_claims: list[str]
    supported_components: list[str]
    contradicted_components: list[str]
    equations_found: list[str]
    observables_found: list[str]
    parameter_constraints_found: list[str]
    benchmark_data_found: bool
    citation_quality: str
```

---

## 3. Support levels

```txt
SOURCE_REJECTED_DECORATIVE_ANALOGY
SOURCE_ANALOGY_ONLY
SOURCE_SUPPORTS_OBSERVABLE
SOURCE_SUPPORTS_BASELINE
SOURCE_SUPPORTS_COMPONENT
SOURCE_CONSTRAINS_PARAMETER
SOURCE_PROVIDES_BENCHMARK_DATA
SOURCE_CONTRADICTS_CANDIDATE
```

---

## 4. Minimum support rules

To reach:

```txt
PHI_GRADIENT_SOURCE_BACKED_LIMITED
```

require at least:

```txt
one source supporting observable or baseline
one source supporting or constraining gradient/transition component
no unaddressed contradiction
citation extract with equation/observable/component evidence
```

To reach:

```txt
PHI_GRADIENT_BENCHMARK_DATA_FOUND
```

require:

```txt
benchmark dataset or published numerical benchmark
observable match
parameter range match or transform
documented extraction
```

---

## 5. Analogy-only blockers

Block source upgrade if the only evidence is:

```txt
similar words
general theory resemblance
unspecified boundary metaphor
generic gradient usage
generic log coordinate usage
high-level decoherence discussion without equation/observable
```

---

## 6. Negative source handling

If a source contradicts the candidate:

```txt
record it
classify affected component
block source-backed status unless contradiction is addressed
include in report
```

Do not discard negative evidence because it is inconvenient.

---

## 7. Required report extract

Every accepted source must provide:

```txt
source id
slot id
supported component
short extract or paraphrased claim
equation or observable if present
parameter constraint if present
reason it is not merely analogy
limitations
```

---

## 8. Final principle

```txt
A paper that sounds related is not evidence.
A paper that constrains the model is evidence pressure.
```
