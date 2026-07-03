# Phygn v3.1 — Reviewed Local Manifest & Real Source Extract Pack Goal

## 0. Context

The latest confirmed document is:

```txt
183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
```

Therefore, v3.1 starts at:

```txt
184
```

v3.0 converted real-source acquisition into an explicit testable boundary:

```txt
query plan
→ acquisition backend
→ candidate manifest
→ extract validation
→ slot coverage
→ benchmark comparability
→ closed-loop feedback
```

v3.0 final status:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

Meaning:

```txt
The gate is ready.
No acquisition backend was attached.
No real source support was granted.
No benchmark support was granted.
No physical claim was unlocked.
```

v3.1 now introduces a reviewed local manifest and real source extract pack.

---

## 1. Core thesis

```txt
A reviewed manifest is the bridge between query planning and evidence pressure.
```

v3.1 does not attempt autonomous web acquisition.

It accepts a curated local manifest of real source candidates, with DOI/arXiv/URL/local_path metadata, and forces every source through extract validation.

---

## 2. Hard rule

```txt
No DOI/arXiv/path, no manifest entry.
No extract, no source support.
No observable/equation/parameter, no slot coverage.
No comparable benchmark, no benchmark support.
No ignored contradiction.
No physical claim.
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
prior_status: PHI_CANDIDATE_SURVIVES_CONTROLS
real_acquisition_status: PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

Current evidence remains:

```txt
SYNTHETIC_ONLY
```

until reviewed real extracts are validated.

---

## 4. v3.1 input artifact

v3.1 expects a local reviewed manifest:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.yaml
```

or:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.json
```

Each manifest entry must contain:

```txt
source_id
title
authors
year
doi OR arxiv_id OR url OR local_path
target_slots
review_status
expected_components
reviewer_notes
risk_flags
```

---

## 5. v3.1 extract pack

v3.1 expects or generates:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.yaml
```

or:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json
```

Each extract must contain:

```txt
extract_id
source_id
slot_id
extract_text_or_paraphrase
equation_text
observable_text
parameter_constraint_text
benchmark_data_text
supported_components
contradicted_components
limitations
manual_review_required
```

---

## 6. Possible campaign statuses

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
PHI_GRADIENT_REVIEWED_MANIFEST_LOADED
PHI_GRADIENT_REVIEWED_MANIFEST_INVALID
PHI_GRADIENT_REAL_EXTRACT_PACK_LOADED
PHI_GRADIENT_REAL_EXTRACTS_VALIDATED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_REVIEWED_MANIFEST_BLOCKED
```

---

## 7. Acceptance criteria

v3.1 is complete when:

```txt
reviewed manifest schema exists
manifest loader exists
manifest validator exists
extract pack schema exists
extract pack loader exists
extract validator reuses v2.9 rules
slot coverage reuses v3.0 matrix
negative sources block upgrades
benchmark comparability requires real comparable records
reports generated
loop feedback generated
tests pass
physical claims remain blocked
```

---

## 8. Final principle

```txt
A reviewed manifest can open the evidence gate.
Only validated extracts can walk through it.
```
