# Phygn v3.4 — Exact Extract Acquisition & Quote-Level Source Review Goal

## 0. Context

The latest confirmed document is:

```txt
201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
```

Therefore, v3.4 starts at:

```txt
202
```

v3.3 validated the v3.2 source pack and found:

```txt
validated_source_support = 0
benchmark_comparable_support = 0
manual_review_debt = 8
physical_claims_blocked = true
```

v3.3 final status:

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
```

Meaning:

```txt
Source-pack validation ran correctly.
Seed paraphrases did not auto-promote.
Manual-review debt is now the bottleneck.
```

v3.4 now converts seed paraphrases into exact reviewed extracts.

---

## 1. Core thesis

```txt
A paraphrase can guide review.
Only an exact extract can face the gate.
```

The purpose of v3.4 is not to prove PHI_GRADIENT.

The purpose is to create quote-level and equation-level material that v3.3/v3.5 can actually validate.

---

## 2. Hard rule

```txt
No exact location, no reviewed extract.
No observable/equation/range, no source pressure.
No benchmark ranges, no benchmark support.
No contradiction omission.
No physical claim.
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
previous_status: PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
current_evidence: SYNTHETIC_ONLY
manual_review_debt: 8
```

---

## 4. v3.4 input files

Load:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

Do not invent sources if missing.

If missing, return:

```txt
PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED
```

---

## 5. v3.4 output files

Create:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json
data/real_sources/extracts/phi_gradient_exact_extract_locations_v3_4.json
data/real_sources/extracts/phi_gradient_equation_observable_map_v3_4.json
data/real_sources/extracts/phi_gradient_parameter_range_map_v3_4.json
```

---

## 6. Exact extract requirement

Every reviewed extract must contain at least one of:

```txt
exact_quote
equation_text
observable_text
parameter_range_text
benchmark_range_text
negative_constraint_text
```

and must also contain:

```txt
source_id
slot_id
location_type
location_value
review_status
reviewer_notes
limitations
```

---

## 7. Possible v3.4 statuses

```txt
PHI_GRADIENT_EXACT_EXTRACT_REVIEW_COMPLETED
PHI_GRADIENT_EXACT_EXTRACTS_ACQUIRED
PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
PHI_GRADIENT_EXACT_EXTRACTS_NO_VALIDATABLE_CONTENT
PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED
```

---

## 8. v3.4 does not promote claims

v3.4 may produce exact extracts.

It must not automatically grant:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

Those statuses belong to the validation gate after exact extracts are acquired.

Recommended next phase:

```txt
v3.5 — Exact Extract Validation & Limited Source-Pressure Gate
```

---

## 9. Acceptance criteria

v3.4 is complete when:

```txt
seed files loaded
manual-review extracts enumerated
exact extract schema implemented
quote/equation/observable/range maps produced
unresolved manual-review debt reported
reports generated
tests pass
physical claims remain blocked
no paraphrase auto-promotes
```

---

## 10. Final principle

```txt
Exactness is the price a source pays to become pressure.
```
