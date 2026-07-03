# Codex Prompt — Phygn v3.6 Local Source Text Acquisition & PDF Registry

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
```

Therefore v3.6 starts at:

```txt
214
```

---

# 1. Read first

Read these v3.6 specs:

```txt
docs/214_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_docs/status/GOAL.md
docs/215_PHYGN_LOCAL_SOURCE_REGISTRY_SCHEMA_AND_HASH_CONTRACT.md
docs/216_PHYGN_SOURCE_AVAILABILITY_AND_DOWNLOAD_TASK_PROTOCOL.md
docs/217_PHYGN_V3_6_REPORTING_AND_NEXT_EXTRACTION_GATE.md
```

Also read:

```txt
docs/213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
```

Inspect:

```txt
phyng/priority_exact_fill/
phyng/exact_extract_review/
phyng/source_pack_validation/
phyng/source_pack_population/
phyng/reviewed_manifest/
phyng/core/
phyng/closed_loop/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
670 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.6:

```txt
Local Source Text Registry
PDF/File Manifest
Source File Discovery
SHA256 Hashing
Source Availability Classification
Manual Download Task Generation
Canonical Reports
Next Extraction Gate
Tests
```

Do not extract source content yet.

Do not make physical claims.

---

# 4. Priority source files

Register and check these priority files under:

```txt
data/real_sources/pdfs/
```

Preferred filenames:

```txt
Hornberger_2003_Collisional_Decoherence.pdf
Hackermueller_2004_Thermal_Emission_Decoherence.pdf
Nimmrichter_2011_CSL_Matter_Wave_Test.pdf
Schrinski_2020_QC_Hypothesis_Tests.pdf
Pedernales_2019_Motional_Dynamical_Decoupling.pdf
```

Source IDs:

```txt
SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE
SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST
SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

---

# 5. Extend package

Create or extend:

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

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_local_source_text_registry.py
```

---

# 6. Output files

Create:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
data/real_sources/manual_download_tasks_v3_6.json
```

---

# 7. Status rules

If all five files are missing:

```txt
PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING
```

If some files are available and hashed:

```txt
PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL
```

If all five files are available and hashed:

```txt
PHI_GRADIENT_LOCAL_SOURCE_FILES_READY
```

If registry created but file check incomplete:

```txt
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED
```

If root/input structure blocks operation:

```txt
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED
```

---

# 8. Hashing

For every existing file:

```txt
compute SHA256
record size_bytes
record file_type
record local_path
```

No file is reproducibly registered without a SHA256 hash.

---

# 9. Manual download tasks

For every missing priority source, create a task:

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

# 10. Reports

Generate:

```txt
reports/local_source_text/phi_gradient_local_source_registry_v3_6.md
reports/local_source_text/phi_gradient_source_file_manifest_v3_6.md
reports/local_source_text/phi_gradient_source_hashes_v3_6.md
reports/local_source_text/phi_gradient_source_availability_v3_6.md
reports/local_source_text/phi_gradient_manual_download_tasks_v3_6.md
reports/local_source_text/phi_gradient_next_exact_extraction_v3_6.md
reports/campaigns/PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md
```

Reports must include:

```txt
canonical status section
available file count
missing file count
hash count
manual download task count
source_id to path mapping
source_id to hash mapping
blocked claims
next actions
discipline note
```

---

# 11. Tests

Create:

```txt
tests/test_local_source_registry_schema_v3_6.py
tests/test_local_source_file_discovery_v3_6.py
tests/test_local_source_hashing_v3_6.py
tests/test_local_source_availability_v3_6.py
tests/test_local_source_manual_download_tasks_v3_6.py
tests/test_phi_gradient_local_source_text_registry_campaign_v3_6.py
```

Minimum tests:

```txt
test_priority_source_records_created
test_missing_files_create_download_tasks
test_existing_file_gets_sha256
test_existing_file_records_size_and_type
test_all_missing_status
test_partial_available_status
test_all_ready_status
test_url_or_arxiv_does_not_count_as_local_file
test_reports_include_canonical_section
test_campaign_generates_reports
test_physical_claims_remain_blocked
test_existing_v3_5_behavior_preserved
```

---

# 12. Behavior preservation

Do not alter:

```txt
existing v3.5 priority exact fill behavior
existing v3.4 exact extract review behavior
existing v3.3 source pack validation behavior
existing v3.2 source pack population behavior
existing v3.1 reviewed manifest behavior
existing v3.0 real source acquisition behavior
existing historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
A registered PDF validates PHI_GRADIENT.
A source hash is source support.
A local file is benchmark support.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
Local source files were checked.
Available files were hashed.
Missing files were converted into download tasks.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
priority source registry works
missing file detection works
hashing works
download tasks generated
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
670 + new v3.6 tests
```

---

# 15. Final discipline

```txt
A source becomes machine-reviewable only when its text is locally registered and hashable.
```
