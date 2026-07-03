# Codex Prompt — Phygn v1.2 Baseline Source Pack Assembly

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
v1.1 complete.
Source folder scaffolding exists.
Manifest validation exists.
Extract validation exists.
Source acquisition tasks exist.
Readiness state machine exists.
No physical claim is unlocked.
285 tests passed.
```

Important numbering:

```txt
Previous result:
67_PHYGN_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_RESULTS.md

v1.2 docs:
68_PHYGN_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_docs/status/GOAL.md
69_PHYGN_BASELINE_SOURCE_PACK_CANONICAL_SELECTION.md
70_PHYGN_BASELINE_SOURCE_MANIFEST_TEMPLATE.md
71_PHYGN_BASELINE_EXTRACTS_AUTHORING_GUIDE.md
72_PHYGN_CODEX_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/68_PHYGN_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_docs/status/GOAL.md
docs/69_PHYGN_BASELINE_SOURCE_PACK_CANONICAL_SELECTION.md
docs/70_PHYGN_BASELINE_SOURCE_MANIFEST_TEMPLATE.md
docs/71_PHYGN_BASELINE_EXTRACTS_AUTHORING_GUIDE.md
```

Also read:

```txt
docs/66_PHYGN_CODEX_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_PROMPT.md
docs/67_PHYGN_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_RESULTS.md
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

Implement v1.2 source pack assembly support:

```txt
source pack template creation
manifest template writing
extract template writing
canonical source slot registry
assembly readiness report
tests
```

This phase creates structured templates and validates them.

It must not claim that the baseline is source-backed.

---

# 4. New / extended modules

Create or extend:

```txt
phyng/evidence/source_pack_assembly.py
phyng/evidence/source_pack_templates.py
phyng/evidence/canonical_source_slots.py
```

Optional campaign runner:

```txt
phyng/campaigns/baseline_source_pack_assembly.py
```

---

# 5. Main function

Implement:

```python
assemble_baseline_source_pack_templates(project_root: Path) -> SourcePackAssemblyResult
```

It should create:

```txt
sources/baseline/source_manifest.json
sources/baseline/papers/README.md
sources/baseline/extracts/SRC-BASE-DECOH-001_extracts.md
sources/baseline/extracts/SRC-BASE-VIS-001_extracts.md
sources/baseline/extracts/SRC-BASE-MWI-001_extracts.md
sources/baseline/extracts/SRC-BASE-THRESH-001_extracts.md
sources/baseline/extracts/SRC-BASE-PARAM-001_extracts.md
sources/baseline/notes/source_selection_notes.md
sources/baseline/rejected/README.md
```

No fake PDFs.

No fake metadata.

---

# 6. Template behavior

Manifest template may be structurally valid but must keep:

```txt
title = null
authors = []
year = null
```

unless real metadata is supplied.

Extract templates must be marked:

```txt
TEMPLATE_NOT_EVIDENCE
```

or equivalent.

The system must not treat template extracts as validated real support.

---

# 7. Readiness

After template creation:

```txt
assembly_status = SOURCE_PACK_TEMPLATE_READY
ready_for_ingestion_attempt = False
```

Only when real files and real extracts are filled should readiness be allowed to move forward.

---

# 8. Reports

Generate:

```txt
reports/rag/source_pack_assembly_v1_2.md
reports/rag/source_manifest_template_v1_2.md
reports/rag/extract_template_validation_v1_2.md
reports/campaigns/BASELINE-SRC-PACK-001_v1_2_assembly.md
```

---

# 9. Tests

Add:

```txt
tests/test_source_pack_assembly_v1_2.py
tests/test_source_pack_templates_v1_2.py
tests/test_canonical_source_slots_v1_2.py
```

Minimum tests:

```txt
test_assembly_creates_expected_folders
test_assembly_creates_manifest_template
test_manifest_template_has_five_slots
test_manifest_template_does_not_fake_metadata
test_extract_templates_created
test_extract_templates_marked_not_evidence
test_template_readiness_false
test_reports_generated
test_campaign_runner_runs
test_idempotent_template_generation
```

---

# 10. Do not overclaim

Do not write:

```txt
baseline is source-backed
Frontera C is validated
Phygn predicts decoherence
candidate is validated
```

Allowed:

```txt
source pack templates are assembled
manifest template exists
extract templates exist
pack is not yet ready for ingestion attempt
```

---

# 11. Acceptance criteria

Complete when:

```txt
pytest -q passes
source pack templates are generated
manifest template has canonical slots
extract templates are generated and marked not evidence
readiness remains false
reports generated
no physical claim is unlocked
```

---

# 12. Final discipline

```txt
Do not confuse an empty evidence container with evidence.
```
