# Codex Prompt — Phygn v1.1 Baseline Literature Source Acquisition

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v1.0 complete.
BASELINE-SRC-PACK-001 runs.
local source scanner exists.
manifest loading exists.
citation audit exists.
baseline limited upgrade execution exists.
empty and URL-only cases fail honestly.
formula + observable local support upgrades to BASELINE_SOURCE_BACKED_LIMITED in tests.
224 tests passed.
```

Important numbering:

```txt
Previous result:
61_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_RESULTS.md

v1.1 docs:
62_PHYGN_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_docs/status/GOAL.md
63_PHYGN_DECOHERENCE_AND_VISIBILITY_CANONICAL_SOURCES.md
64_PHYGN_SOURCE_MANIFEST_AUTHORING_PROTOCOL.md
65_PHYGN_EXTRACTS_AND_SUPPORT_TAGGING_PROTOCOL.md
66_PHYGN_CODEX_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/62_PHYGN_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_docs/status/GOAL.md
docs/63_PHYGN_DECOHERENCE_AND_VISIBILITY_CANONICAL_SOURCES.md
docs/64_PHYGN_SOURCE_MANIFEST_AUTHORING_PROTOCOL.md
docs/65_PHYGN_EXTRACTS_AND_SUPPORT_TAGGING_PROTOCOL.md
```

Also read:

```txt
docs/59_PHYGN_CODEX_V1_0_BASELINE_SOURCE_PACK_INGESTION_PROMPT.md
docs/61_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement v1.1 source acquisition support:

```txt
manifest validation
extract file validation
support tag validation
source acquisition task generation
baseline source pack readiness report
optional source folder scaffolding
tests
```

This phase prepares sources.  
It must not claim that sources have been ingested unless local files actually exist and pass audit.

---

# 4. New or extended modules

Create or extend:

```txt
phyng/evidence/source_manifest_validation.py
phyng/evidence/extract_validation.py
phyng/evidence/source_acquisition_tasks.py
phyng/evidence/source_pack_readiness_v1_1.py
```

Optional:

```txt
phyng/campaigns/baseline_literature_source_acquisition.py
```

---

# 5. Source folder scaffolding

Implement optional helper:

```python
create_baseline_source_folders(project_root: Path) -> list[Path]
```

It should create if missing:

```txt
sources/baseline/
sources/baseline/papers/
sources/baseline/extracts/
sources/baseline/notes/
sources/baseline/rejected/
```

Do not create fake source files.

---

# 6. Manifest validation

Implement:

```python
validate_source_manifest(manifest_path: Path) -> ManifestValidationResult
```

It must check:

```txt
JSON parses
top-level list
required fields present
allowed source_type
allowed trust_level
allowed support tags
local files exist for LOCAL_FILE
URL-only does not count as ingested
unknown metadata allowed only as null/[]
no fake DOI/page/quote fields required
```

Generate:

```txt
reports/rag/source_manifest_validation_v1_1.md
```

---

# 7. Extract validation

Implement:

```python
validate_extract_file(path: Path) -> ExtractValidationResult
```

It must check:

```txt
has source id/title section
has at least one support type
support tags are allowed
claim target present
local reference present if available
audit notes present
does not contain forbidden overclaims
does not mark Frontera C validation
```

Generate:

```txt
reports/rag/extract_support_tags_v1_1.md
```

---

# 8. Source acquisition tasks

Generate tasks for missing categories:

```txt
VISIBILITY_DECAY
ENVIRONMENTAL_DECOHERENCE
MATTER_WAVE_INTERFEROMETRY
DETECTABILITY_OR_VISIBILITY_THRESHOLD
OPTIONAL_PARAMETER_OR_RATE_SUPPORT
```

Write:

```txt
rag/research_tasks/RT-V1-1-SRC-VISIBILITY_DECAY.json
rag/research_tasks/RT-V1-1-SRC-ENVIRONMENTAL_DECOHERENCE.json
rag/research_tasks/RT-V1-1-SRC-MATTER_WAVE_INTERFEROMETRY.json
rag/research_tasks/RT-V1-1-SRC-DETECTABILITY_OR_VISIBILITY_THRESHOLD.json
rag/research_tasks/RT-V1-1-SRC-OPTIONAL_PARAMETER_OR_RATE_SUPPORT.json
```

---

# 9. Readiness report

Implement:

```python
generate_baseline_source_pack_readiness_v1_1(project_root: Path) -> SourcePackReadinessResult
```

It must report:

```txt
folders_exist
manifest_exists
manifest_valid
extracts_count
validated_extracts_count
missing_categories
ready_for_ingestion_attempt
allowed_next_action
```

Readiness statuses:

```txt
NO_SOURCE_FOLDER
NO_MANIFEST
MANIFEST_INVALID
EXTRACTS_MISSING
PARTIAL_READY
READY_FOR_INGESTION_ATTEMPT
```

---

# 10. Reports

Generate:

```txt
reports/rag/source_manifest_validation_v1_1.md
reports/rag/extract_support_tags_v1_1.md
reports/rag/baseline_source_pack_readiness_v1_1.md
reports/campaigns/BASELINE-SRC-PACK-001_v1_1_readiness.md
```

---

# 11. Tests

Add:

```txt
tests/test_source_manifest_validation_v1_1.py
tests/test_extract_validation_v1_1.py
tests/test_source_acquisition_tasks_v1_1.py
tests/test_baseline_source_pack_readiness_v1_1.py
```

Minimum tests:

```txt
test_create_baseline_source_folders
test_missing_manifest_not_ready
test_malformed_manifest_invalid
test_manifest_required_fields
test_manifest_url_only_not_ingested
test_manifest_local_file_missing_blocks_ready
test_manifest_local_file_exists_valid
test_extract_missing_support_type_invalid
test_extract_forbidden_overclaim_invalid
test_extract_formula_support_valid
test_missing_categories_create_research_tasks
test_readiness_ready_only_with_valid_manifest_and_extracts
test_reports_generated
```

---

# 12. Do not overclaim

Do not write:

```txt
baseline is source-backed
Frontera C is validated
Phygn predicts decoherence
candidate is validated
```

Allowed:

```txt
source folder is ready
manifest is valid
extract tags are valid
source pack is ready for ingestion attempt
```

---

# 13. Acceptance criteria

Complete when:

```txt
pytest -q passes
source folders can be created
manifest validation works
extract validation works
missing categories create research tasks
readiness report generated
ready_for_ingestion_attempt only true with valid manifest and validated extracts
no physical claim is unlocked
```

---

# 14. Final discipline

```txt
Prepare evidence.
Do not pretend it has already spoken.
```
