# Phygn v3.2 — PHI_GRADIENT Reviewed Real Source Pack Population Goal

## 0. Context

The latest confirmed document is:

```txt
189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
```

Therefore, v3.2 starts at:

```txt
190
```

v3.1 created empty reviewed-manifest and extract-pack templates:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json
```

v3.1 final status:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
```

Meaning:

```txt
The evidence gate is prepared.
No real source support exists yet.
No benchmark support exists yet.
Physical claims remain blocked.
```

v3.2 now populates a first reviewed real source candidate pack for PHI_GRADIENT.

---

## 1. Core thesis

```txt
A source pack is not a bibliography.
It is an evidence stress test in structured form.
```

The goal is not to collect papers that sound related.

The goal is to populate a manifest and extract pack with sources that can support, constrain, benchmark or damage PHI_GRADIENT.

---

## 2. Hard rule

```txt
No paper enters because it sounds similar.
It enters because it pressures a slot.
```

No source may count as support until:

```txt
it has a traceable identifier
it targets a valid slot
it has a reviewed extract
the extract supports or contradicts a concrete component
the validator accepts it
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
status: SYNTHETIC_ONLY
```

PHI_GRADIENT remains physically unvalidated.

---

## 4. v3.2 input/output files

v3.2 generates seed files:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

These are seed packs.

They must be loaded, reviewed and validated before they can produce:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

---

## 5. Required source categories

The seed pack should include sources across:

```txt
decoherence baseline / visibility decay
matter-wave interferometry benchmarks
environmental decoherence models
gravitational decoherence / collapse models
gradient or transition operators
scale/log-coordinate formulations
alpha-like parameter constraints
negative/conflicting sources
```

---

## 6. Possible v3.2 statuses

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
PHI_GRADIENT_SOURCE_PACK_REQUIRES_REVIEW
PHI_GRADIENT_SOURCE_PACK_PARTIALLY_VALIDATED
PHI_GRADIENT_SOURCE_PACK_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_PACK_HAS_NEGATIVE_PRESSURE
PHI_GRADIENT_SOURCE_PACK_BENCHMARK_CANDIDATES_FOUND
PHI_GRADIENT_SOURCE_PACK_BLOCKED
```

---

## 7. Acceptance criteria

v3.2 is complete when:

```txt
seed manifest exists
seed extract pack exists
all entries have traceable identifiers
all entries target valid slots
sources are marked as candidate pressure, not support
extracts are marked review_required unless manually validated
negative-source candidates are included
benchmark candidates are included
reports generated
tests pass
physical claims remain blocked
```

---

## 8. Final principle

```txt
The first source pack must make ignorance searchable, not decorate belief.
```
