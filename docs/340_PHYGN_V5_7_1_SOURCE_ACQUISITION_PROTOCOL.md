# Phygn v5.7.1 — Source Acquisition Protocol

## 0. Purpose

This document defines the source acquisition protocol for targeted visibility/decoherence literature.

---

## 1. Source acquisition queue

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.json
```

Schema:

```python
class SourceAcquisitionQueueItem(BaseModel):
    acquisition_id: str
    priority: str
    source_title_candidate: str | None
    authors_candidate: list[str]
    year_candidate: int | None
    publication_candidate: str | None
    doi_candidate: str | None
    arxiv_candidate: str | None
    url_candidate: str | None
    search_queries: list[str]
    reason_for_relevance: str
    target_observable_classes: list[str]
    expected_conditions: list[str]
    source_identity_status: str
    availability_status: str
    likely_observable_location: str | None
    manual_action_required: str
    notes: list[str]
```

Priority values:

```txt
CRITICAL
HIGH
MEDIUM
LOW
REJECT
```

Source identity status:

```txt
RESOLVED_COMPLETE
RESOLVED_PARTIAL
RAW_REF_ONLY
UNRESOLVED
REJECTED_NOT_RELEVANT
```

Availability status:

```txt
LOCAL_AVAILABLE
OPEN_ACCESS_LIKELY
OPEN_ACCESS_CONFIRMED
REQUIRES_DOWNLOAD
PAYWALL_LIKELY
UNKNOWN
```

---

## 2. Candidate source identity matrix

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json
```

Minimum fields:

```txt
source_candidate_id
title
authors
year
publication
doi
arxiv
url
identity_completeness_score
identity_complete
missing_identity_fields
```

Identity is complete only if it has:

```txt
title
authors or publication authority
year
DOI/arXiv/URL
```

---

## 3. Observable target matrix

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.json
```

Fields:

```txt
source_candidate_id
target_observable_class
target_variable
expected_condition_axis
expected_location_type
expected_numeric_form
why_ytrue_possible
risk_of_not_ytrue
priority
```

Expected location types:

```txt
FIGURE
TABLE
CAPTION
RESULTS_SECTION
SUPPLEMENTARY_DATA
DATA_REPOSITORY
```

---

## 4. Download priority queue

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.json
```

Fields:

```txt
source_candidate_id
download_priority
preferred_url
expected_filename
target_local_path
requires_manual_download
requires_paywall_access
requires_supplementary_download
notes
```

---

## 5. Rejection log

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_source_rejection_log_v5_7_1.json
```

Reject reasons:

```txt
NO_OBSERVED_MEASUREMENTS
REVIEW_ONLY
THEORY_ONLY
NO_VISIBILITY_OR_DECOHERENCE_OBSERVABLE
NO_RESOLVABLE_IDENTITY
DUPLICATE_SOURCE
OUT_OF_DOMAIN
INSUFFICIENT_PROVENANCE
```

---

## 6. Candidate priority guidance

Critical/high priority sources should satisfy at least two:

```txt
directly reports visibility/contrast/decoherence measurements
contains figures or tables with numeric observables
independent of Hackermueller 2004
open access likely
strong source identity
relevant to molecular/matter-wave decoherence
```

---

## 7. Final principle

```txt
Acquisition priority is not citation fame.
It is probability of becoming accepted y_true.
```
