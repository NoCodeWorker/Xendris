# Phygn v3.6 - Local Source Text Registry Results

Date: 2026-06-30

Source prompt:

```txt
docs/218_PHYGN_CODEX_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_PROMPT.md
```

Supporting specs:

```txt
docs/214_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_docs/status/GOAL.md
docs/215_PHYGN_LOCAL_SOURCE_REGISTRY_SCHEMA_AND_HASH_CONTRACT.md
docs/216_PHYGN_SOURCE_AVAILABILITY_AND_DOWNLOAD_TASK_PROTOCOL.md
docs/217_PHYGN_V3_6_REPORTING_AND_NEXT_EXTRACTION_GATE.md
docs/213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.6 PROMPT SPECIFICATIONS**

Final campaign status:

```txt
PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING
```

Interpretation:

```txt
The local source text registry was created.
The five priority source files were checked under data/real_sources/pdfs/.
No local priority PDFs/text files were present.
No source file was marked available from URL/arXiv/DOI metadata.
No source content was extracted.
No physical claim was upgraded.
```

Validation:

```txt
pytest -q
682 passed in 46.46s
```

Focused v3.6 validation:

```txt
pytest -q tests/test_local_source_registry_schema_v3_6.py tests/test_local_source_file_discovery_v3_6.py tests/test_local_source_hashing_v3_6.py tests/test_local_source_availability_v3_6.py tests/test_local_source_manual_download_tasks_v3_6.py tests/test_phi_gradient_local_source_text_registry_campaign_v3_6.py
12 passed in 1.23s
```

Baseline before v3.6:

```txt
pytest -q
670 passed in 45.85s
```

Net result:

```txt
670 baseline tests + 12 v3.6 tests = 682 passing tests
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/local_source_text/
  __init__.py
  schemas.py
  source_registry.py
  file_discovery.py
  hashing.py
  availability.py
  manual_download_tasks.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_local_source_text_registry.py
```

Entrypoint:

```python
run_phi_gradient_local_source_text_registry_campaign(root: str | Path = ".")
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/local_source_text/schemas.py
```

Schemas:

```txt
PriorityLocalSourceSpec
LocalSourceFileRecord
LocalSourceTextRegistry
SourceFileManifest
SourceHashRecord
SourceHashManifest
SourceAvailabilityRecord
SourceAvailabilityManifest
ManualSourceDownloadTask
ManualSourceDownloadTaskManifest
PhiGradientLocalSourceTextRegistryResult
PhiGradientLocalSourceTextRegistryCampaignResult
```

---

## 4. Priority Source File Registry

The v3.6 registry checked the five priority source files:

| Priority | Source ID | Preferred filename | Status |
|---:|---|---|---|
| 1 | `SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE` | `Hornberger_2003_Collisional_Decoherence.pdf` | Missing |
| 2 | `SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE` | `Hackermueller_2004_Thermal_Emission_Decoherence.pdf` | Missing |
| 3 | `SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST` | `Nimmrichter_2011_CSL_Matter_Wave_Test.pdf` | Missing |
| 4 | `SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` | `Schrinski_2020_QC_Hypothesis_Tests.pdf` | Missing |
| 5 | `SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING` | `Pedernales_2019_Motional_Dynamical_Decoupling.pdf` | Missing |

Target directory:

```txt
data/real_sources/pdfs/
```

Summary:

| Metric | Result |
|---|---:|
| Priority sources checked | 5 |
| Available local files | 0 |
| Missing local files | 5 |
| SHA256 hashes generated | 0 |
| Unsupported files | 0 |
| Manual download tasks | 5 |

---

## 5. Generated Data Artifacts

Created:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
data/real_sources/manual_download_tasks_v3_6.json
```

The hash manifest is empty because no local source files were present:

```txt
hash_count = 0
```

The manual download task manifest contains five tasks with:

```txt
task_id
source_id
title
preferred_filename
target_path
known_identifiers
priority
reason
status = DOWNLOAD_TASK_CREATED
```

---

## 6. Generated Reports

Created:

```txt
reports/local_source_text/phi_gradient_local_source_registry_v3_6.md
reports/local_source_text/phi_gradient_source_file_manifest_v3_6.md
reports/local_source_text/phi_gradient_source_hashes_v3_6.md
reports/local_source_text/phi_gradient_source_availability_v3_6.md
reports/local_source_text/phi_gradient_manual_download_tasks_v3_6.md
reports/local_source_text/phi_gradient_next_exact_extraction_v3_6.md
reports/campaigns/PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md
```

All generated reports include the canonical status section.

Campaign report:

```txt
reports/campaigns/PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md
```

---

## 7. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED
PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING
PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL
PHI_GRADIENT_LOCAL_SOURCE_FILES_READY
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED
```

The active status maps to:

```txt
Canonical Permission: REVIEW_REQUIRED
Blocked Reasons: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
Evidence Level: NO_EVIDENCE
Support Level: UNSUPPORTED
Risk Level: TECHNICAL_RISK
```

---

## 8. Hash Boundary

The v3.6 hash rule was preserved:

```txt
No file is reproducibly registered without a SHA256 hash.
```

For every existing supported local file, v3.6 records:

```txt
sha256
size_bytes
file_type
local_path
```

In this run:

```txt
No priority local files existed, so no SHA256 hashes were generated.
```

---

## 9. Manual Download Tasks

Created five manual download tasks:

```txt
DOWNLOAD-01-SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE
DOWNLOAD-02-SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
DOWNLOAD-03-SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST
DOWNLOAD-04-SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS
DOWNLOAD-05-SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

All tasks have:

```txt
status = DOWNLOAD_TASK_CREATED
```

These tasks are acquisition instructions only. They are not evidence support.

---

## 10. New Tests

Created:

```txt
tests/test_local_source_registry_schema_v3_6.py
tests/test_local_source_file_discovery_v3_6.py
tests/test_local_source_hashing_v3_6.py
tests/test_local_source_availability_v3_6.py
tests/test_local_source_manual_download_tasks_v3_6.py
tests/test_phi_gradient_local_source_text_registry_campaign_v3_6.py
```

Coverage includes:

| Test | Purpose |
|---|---|
| `test_priority_source_records_created` | Confirms the five priority source records are created |
| `test_missing_files_create_download_tasks` | Confirms missing files become manual download tasks |
| `test_existing_file_gets_sha256` | Confirms SHA256 hashing |
| `test_existing_file_records_size_and_type` | Confirms file size and type recording |
| `test_all_missing_status` | Confirms all-missing campaign status |
| `test_partial_available_status` | Confirms partial local availability status |
| `test_all_ready_status` | Confirms all-ready local availability status |
| `test_url_or_arxiv_does_not_count_as_local_file` | Confirms metadata is not treated as local text |
| `test_reports_include_canonical_section` | Confirms report contract integration |
| `test_campaign_generates_reports` | Confirms campaign report generation |
| `test_physical_claims_remain_blocked` | Confirms blocked claim discipline |
| `test_existing_v3_5_behavior_preserved` | Confirms v3.5 behavior remains unchanged |

---

## 11. Behavior Preservation

v3.6 did not alter:

```txt
v3.5 priority exact fill behavior
v3.4 exact extract review behavior
v3.3 source pack validation behavior
v3.2 source pack population behavior
v3.1 reviewed manifest behavior
v3.0 real source acquisition behavior
historical reports
```

Preservation evidence:

```txt
test_existing_v3_5_behavior_preserved
```

Result:

```txt
passed
```

---

## 12. Blocked Claims

The campaign explicitly blocks:

```txt
A registered PDF validates PHI_GRADIENT.
A source hash is source support.
A local file is benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed statements:

```txt
Local source registry was created.
Priority files were checked.
Missing files were converted into manual download tasks.
```

---

## 13. Next Gate

Recommended next phase:

```txt
v3.7 - Exact PDF/Text Extraction: Quotes, Equations, Tables & Ranges
```

But v3.7 should not claim source support until exact extraction and validation occur.

Current next action:

```txt
Download the five priority source files into data/real_sources/pdfs/, then rerun v3.6.
```

Expected target files:

```txt
data/real_sources/pdfs/Hornberger_2003_Collisional_Decoherence.pdf
data/real_sources/pdfs/Hackermueller_2004_Thermal_Emission_Decoherence.pdf
data/real_sources/pdfs/Nimmrichter_2011_CSL_Matter_Wave_Test.pdf
data/real_sources/pdfs/Schrinski_2020_QC_Hypothesis_Tests.pdf
data/real_sources/pdfs/Pedernales_2019_Motional_Dynamical_Decoupling.pdf
```

---

## 14. Final Assessment

v3.6 converted the v3.5 source-text gap into a reproducible local registry and concrete manual acquisition queue.

The useful result is the explicit local-file boundary:

```txt
Five priority source files are missing locally, so exact extraction remains blocked.
```

Final discipline note:

```txt
A source becomes machine-reviewable only when its text is locally registered and hashable.
```
