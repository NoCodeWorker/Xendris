# Phygn v3.6 — Local Source Text Acquisition & PDF Registry Goal

## 0. Context

The latest confirmed document is:

```txt
D:\BIOCULTOR\PHYNG\docs\213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
```

Therefore, v3.6 starts at:

```txt
214
```

v3.5 processed the five priority sources and produced:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
```

Meaning:

```txt
Priority sources were selected.
Exact-fill records were created.
No local source text was available.
No quote, equation, page, section, table or range was fabricated.
```

v3.6 now registers local source files so later campaigns can extract exact source content reproducibly.

---

## 1. Core thesis

```txt
A URL points to evidence.
A local verified source lets Phygn touch it.
```

v3.6 is not an extraction phase.

It is a source-text acquisition and registry phase.

---

## 2. Hard rule

```txt
No local file, no local source text.
No hash, no reproducible source registry.
No source_id mapping, no extraction.
No extraction, no source pressure.
No physical claim.
```

---

## 3. Target priority sources

v3.6 must register local files for:

```txt
SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE
SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST
SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

---

## 4. Recommended local directory

Use:

```txt
data/real_sources/pdfs/
```

Recommended filenames:

```txt
Hornberger_2003_Collisional_Decoherence.pdf
Hackermueller_2004_Thermal_Emission_Decoherence.pdf
Nimmrichter_2011_CSL_Matter_Wave_Test.pdf
Schrinski_2020_QC_Hypothesis_Tests.pdf
Pedernales_2019_Motional_Dynamical_Decoupling.pdf
```

Alternative local paths are allowed if registered explicitly.

---

## 5. v3.6 output files

Create:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
```

Reports:

```txt
reports/local_source_text/phi_gradient_local_source_registry_v3_6.md
reports/local_source_text/phi_gradient_source_file_manifest_v3_6.md
reports/local_source_text/phi_gradient_source_hashes_v3_6.md
reports/local_source_text/phi_gradient_source_availability_v3_6.md
reports/local_source_text/phi_gradient_next_exact_extraction_v3_6.md
reports/campaigns/PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md
```

---

## 6. Possible v3.6 statuses

```txt
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED
PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL
PHI_GRADIENT_LOCAL_SOURCE_FILES_READY
PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED
```

---

## 7. What v3.6 may allow

Allowed:

```txt
Local source registry was created.
Some priority source files are present.
Some priority source files are missing.
Source hashes were computed for available files.
Next exact extraction can be scheduled if files are ready.
```

Blocked:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT physically validated
Frontera C validated
```

---

## 8. Acceptance criteria

v3.6 is complete when:

```txt
priority source registry schema exists
local file discovery works
source_id to file mapping works
sha256 hashes computed for available files
missing files reported clearly
availability status generated
reports generated
tests pass
physical claims remain blocked
```

---

## 9. Final principle

```txt
A source becomes machine-reviewable only when its text is locally registered and hashable.
```
