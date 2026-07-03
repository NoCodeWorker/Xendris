# Phygn v3.1 — Reviewed Local Manifest Schema & Validation

## 0. Purpose

This document defines the reviewed local manifest contract.

The manifest is not evidence.

It is a curated candidate set that may become evidence pressure only after extract validation.

---

## 1. Manifest entry schema

```python
class ReviewedSourceManifestEntry(BaseModel):
    source_id: str
    title: str
    authors: list[str]
    year: int | None
    doi: str | None = None
    arxiv_id: str | None = None
    url: str | None = None
    local_path: str | None = None
    source_type: str
    target_slots: list[str]
    expected_components: list[str]
    review_status: str
    reviewer_notes: list[str]
    risk_flags: list[str]
```

---

## 2. Manifest schema

```python
class ReviewedSourceManifest(BaseModel):
    manifest_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    reviewer: str | None
    entries: list[ReviewedSourceManifestEntry]
    fixture_entries: list[str]
    test_double_entries: list[str]
    notes: list[str]
```

---

## 3. Required identifier rule

Every real manifest entry must include at least one:

```txt
doi
arxiv_id
url
local_path
```

If missing:

```txt
MANIFEST_ENTRY_REJECTED_NO_TRACEABLE_IDENTIFIER
```

---

## 4. Review statuses

```txt
REVIEWED_SOURCE_CANDIDATE
REVIEWED_SOURCE_HIGH_PRIORITY
REVIEWED_SOURCE_LOW_PRIORITY
REVIEWED_SOURCE_NEGATIVE_CANDIDATE
REVIEWED_SOURCE_BENCHMARK_CANDIDATE
REVIEWED_SOURCE_REJECTED_OUT_OF_SCOPE
REVIEWED_SOURCE_REQUIRES_MANUAL_REVIEW
```

---

## 5. Manifest validation statuses

```txt
REVIEWED_MANIFEST_VALID
REVIEWED_MANIFEST_EMPTY
REVIEWED_MANIFEST_INVALID_SCHEMA
REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES
REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES
REVIEWED_MANIFEST_REQUIRES_MANUAL_REVIEW
```

---

## 6. Slot targeting rule

Every accepted entry must target at least one of:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS
SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS
SLOT_4_GRADIENT_TRANSITION_OPERATORS
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

If not:

```txt
MANIFEST_ENTRY_REJECTED_NO_TARGET_SLOT
```

---

## 7. Fixture and test-double contamination

Entries marked as fixtures or test doubles must be recorded but cannot contribute to:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

Status:

```txt
MANIFEST_ENTRY_NON_EVIDENTIAL_TEST_OBJECT
```

---

## 8. Recommended first manifest composition

Target 10–20 entries:

```txt
3–4 decoherence baseline / visibility decay sources
2–4 mesoscopic interferometry benchmark candidates
2–3 gravitational decoherence or collapse constraint sources
1–3 gradient/transition/effective operator sources
1–2 scale/log-coordinate sources
2–4 negative or exclusion sources
```

---

## 9. Final principle

```txt
A reviewed manifest is a disciplined invitation to evidence, not evidence itself.
```
