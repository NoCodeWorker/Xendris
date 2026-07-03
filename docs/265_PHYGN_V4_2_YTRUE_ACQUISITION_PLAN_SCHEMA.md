# Phygn v4.2 — y_true Acquisition Plan Schema

## 0. Purpose

This document defines how Phygn plans acquisition of real observed truth.

---

## 1. y_true acquisition plan

Create:

```txt
data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json
```

Schema:

```python
class YTrueAcquisitionItem(BaseModel):
    acquisition_id: str
    target_id: str
    observable_class: str
    y_true_status: str
    required_measurement: str
    candidate_data_sources: list[str]
    acquisition_method: str
    manual_extraction_required: bool
    experimental_required: bool
    expected_unit: str | None
    quality_requirements: list[str]
    blockers: list[str]
    priority: str
```

Acquisition methods:

```txt
PUBLIC_DATASET_LOOKUP
MANUAL_TABLE_EXTRACTION
MANUAL_FIGURE_DIGITIZATION
SUPPLEMENTARY_DATA_EXTRACTION
AUTHOR_DATA_REQUEST
NEW_EXPERIMENT_REQUIRED
NOT_ACQUIRABLE_FROM_CURRENT_SOURCES
```

---

## 2. Dataset source registry

Create:

```txt
data/observables/phi_gradient_dataset_source_registry_v4_2.json
```

Schema:

```python
class DatasetSourceRegistryRecord(BaseModel):
    dataset_source_id: str
    related_source_id: str
    source_type: str
    access_status: str
    expected_observables: list[str]
    acquisition_method: str
    requires_manual_review: bool
    notes: list[str]
```

Source types:

```txt
ARTICLE_TABLE
ARTICLE_FIGURE
SUPPLEMENTARY_MATERIAL
PUBLIC_REPOSITORY
AUTHOR_REQUEST
NEW_EXPERIMENT
```

Access statuses:

```txt
KNOWN_LOCAL_PDF
NEEDS_SUPPLEMENTARY_FILE
NEEDS_PUBLIC_LOOKUP
NEEDS_MANUAL_DIGITIZATION
NEEDS_AUTHOR_CONTACT
NEEDS_EXPERIMENT
```

---

## 3. Measurement readiness matrix

Create:

```txt
data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json
```

Fields:

```txt
observable_class
target_count
y_true_available_count
public_data_acquirable_count
manual_extraction_count
experiment_required_count
blocked_count
readiness_status
next_action
```

Readiness statuses:

```txt
READY_FOR_YTRUE_EXTRACTION
MANUAL_EXTRACTION_REQUIRED
PUBLIC_DATA_SEARCH_REQUIRED
EXPERIMENT_REQUIRED
BLOCKED
```

---

## 4. Quality-control rules

Create:

```txt
data/observables/phi_gradient_quality_control_rules_v4_2.json
```

Rules:

```txt
unit normalization required
source hash traceability required
page/table/figure reference required
numeric uncertainty required when available
do not infer data from prose unless explicitly quantitative
figure digitization must be marked as approximate
supplementary files must be hashed
author-provided data must be provenance-tagged
```

---

## 5. Priority assignment

Recommended priority:

```txt
CRITICAL:
  VISIBILITY / CONTRAST_DECAY y_true for benchmark rows

HIGH:
  DECOHERENCE_RATE and COHERENCE_LOSS values

MEDIUM:
  MASS/TIME/SEPARATION/TEMPERATURE/PRESSURE regimes

LOW:
  context-only experimental fields
```

---

## 6. Final principle

```txt
The acquisition plan is not data.
It is a map to data.
```
