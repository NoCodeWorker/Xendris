# Phygn v1.2 — Baseline Source Pack Assembly Goal

## 0. Purpose

Phygn v1.1 prepared the source acquisition machinery:

```txt
source folders
manifest validation
extract validation
support tag validation
source acquisition tasks
readiness state machine
```

v1.2 has a sharper mission:

```txt
assemble a concrete baseline source pack skeleton ready for real local papers and extracts.
```

This phase still does **not** claim that the baseline is source-backed.

It prepares:

```txt
source_manifest.json template
extract templates
canonical source slots
support targets
readiness checklist
execution handoff back to v1.0 ingestion
```

---

## 1. Current state

Prior expected result:

```txt
67_PHYGN_V1_1_BASELINE_LITERATURE_SOURCE_ACQUISITION_RESULTS.md
```

Current readiness without real sources:

```txt
NO_SOURCE_FOLDER or NO_MANIFEST
ready_for_ingestion_attempt = False
```

v1.2 target state:

```txt
SOURCE_PACK_ASSEMBLED
```

or, if local files are absent:

```txt
SOURCE_PACK_TEMPLATE_READY
```

Not:

```txt
BASELINE_SOURCE_BACKED_LIMITED
```

That comes only after actual ingestion and citation audit.

---

## 2. Goal v1.2

Create a source pack assembly plan for:

```txt
sources/baseline/
```

with:

```txt
1. canonical slots for 3-5 sources;
2. manifest template;
3. extract templates;
4. support tag map;
5. forbidden overclaim checks;
6. readiness checklist;
7. prompt for IDE to create folders/templates and validate them.
```

---

## 3. Minimum source pack

Minimum target:

```txt
SRC-BASE-DECOH-001:
decoherence / exponential decay / coherence loss

SRC-BASE-VIS-001:
visibility / interference contrast observable

SRC-BASE-MWI-001:
matter-wave or nanoparticle interferometry context
```

Optional but recommended:

```txt
SRC-BASE-THRESH-001:
visibility threshold / uncertainty / epsilon_exp

SRC-BASE-PARAM-001:
parameter support for Gamma / timescale / assumptions
```

---

## 4. Minimum support for later LIMITED upgrade

To later reach:

```txt
BASELINE_SOURCE_BACKED_LIMITED
```

the source pack must provide audited:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
local file or validated extract
PASSED_LIMITED citation audit
```

v1.2 does not perform the final upgrade.

---

## 5. What v1.2 may produce

Allowed:

```txt
source pack template exists
manifest template exists
extract templates exist
readiness checklist exists
pack can be validated
```

Not allowed:

```txt
baseline is source-backed
Frontera C is validated
Phygn predicts decoherence
candidate is validated
```

---

## 6. Scientific discipline

v1.2 must preserve the distinction:

```txt
prepared evidence ≠ ingested evidence
ingested evidence ≠ source-backed baseline
source-backed baseline ≠ validated candidate
validated candidate ≠ confirmed theory
```

---

## 7. Output folders

Expected scaffold:

```txt
sources/baseline/
  source_manifest.json
  papers/
    README.md
  extracts/
    SRC-BASE-DECOH-001_extracts.md
    SRC-BASE-VIS-001_extracts.md
    SRC-BASE-MWI-001_extracts.md
    SRC-BASE-THRESH-001_extracts.md
    SRC-BASE-PARAM-001_extracts.md
  notes/
    source_selection_notes.md
  rejected/
    README.md
```

---

## 8. Reports expected

```txt
reports/rag/source_pack_assembly_v1_2.md
reports/rag/source_manifest_template_v1_2.md
reports/rag/extract_template_validation_v1_2.md
reports/campaigns/BASELINE-SRC-PACK-001_v1_2_assembly.md
```

---

## 9. Acceptance criteria

v1.2 is complete when:

```txt
source pack assembly templates are generated;
manifest template validates structurally;
extract templates validate structurally;
readiness remains false until real files/extracts are filled;
no physical claim is unlocked;
tests pass.
```

---

## 10. Final principle

```txt
A prepared source pack is not evidence.
It is an evidence container awaiting content.
```
