# Phygn — Blocker Taxonomy & Minimal Improvement Protocol

## 0. Purpose

This document defines how the AI classifies blockers and selects the smallest valid improvement.

---

## 1. Blocker taxonomy

Every failed gate must produce exactly one primary blocker type:

```txt
KNOWLEDGE_BLOCKER
TOOLING_BLOCKER
SOURCE_IDENTITY_BLOCKER
SOURCE_AVAILABILITY_BLOCKER
OBSERVABLE_LOCATION_BLOCKER
YTRUE_BLOCKER
DATASET_THRESHOLD_BLOCKER
BENCHMARK_BLOCKER
MODEL_BLOCKER
PREDICTIVE_GAIN_BLOCKER
CONTROL_BLOCKER
LEAKAGE_BLOCKER
ABLATION_BLOCKER
SCIENTIFIC_DEBT_BLOCKER
CLAIM_PERMISSION_BLOCKER
HUMAN_REVIEW_BLOCKER
EXTERNAL_SOURCE_BLOCKER
EXPERIMENT_REQUIRED_BLOCKER
TEST_BLOCKER
```

Secondary blockers may be listed.

---

## 2. Blocker-to-action map

## KNOWLEDGE_BLOCKER

Allowed actions:

```txt
read local docs
read local papers
extract relevant theory notes
summarize required scientific assumptions
```

Not allowed:

```txt
invent missing theory
```

## TOOLING_BLOCKER

Allowed actions:

```txt
install or document required library
add parser
add schema
add validator
add CLI wrapper
add test utility
```

## SOURCE_IDENTITY_BLOCKER

Allowed actions:

```txt
resolve DOI/arXiv/URL
build lookup packet
create identity matrix
request human lookup
```

## SOURCE_AVAILABILITY_BLOCKER

Allowed actions:

```txt
download source if available
register local path
compute SHA256
create manual download queue
```

## OBSERVABLE_LOCATION_BLOCKER

Allowed actions:

```txt
scan PDFs
extract captions
find figure/table/section/equation candidates
generate human figure/table review packet
```

## YTRUE_BLOCKER

Allowed actions:

```txt
extract numeric values
normalize units
resolve condition mapping
deduplicate records
apply QC
```

## DATASET_THRESHOLD_BLOCKER

Allowed actions:

```txt
review rejected candidates
complete missing sources
acquire more sources
perform human table/figure review
```

## BENCHMARK_BLOCKER

Allowed actions:

```txt
assemble canonical DataFrame
normalize columns
define feature/target schema
prepare GroupKFold or leave-one-source-out split
```

## MODEL_BLOCKER

Allowed actions:

```txt
define candidate model
define baseline model
ensure predictions for all y_true
prevent y_true leakage
```

## PREDICTIVE_GAIN_BLOCKER

Allowed actions:

```txt
compute metrics only when permitted
compare M_base vs M_C
record undefined gain if baseline error is zero
```

## CONTROL_BLOCKER

Allowed actions:

```txt
add simple controls
add shuffled controls
add null baselines
add parameter-count fairness checks
```

## LEAKAGE_BLOCKER

Allowed actions:

```txt
test direct fitting
test source leakage
test duplicate leakage
test condition-value leakage
```

## ABLATION_BLOCKER

Allowed actions:

```txt
remove C-features
shuffle C-features
replace C-coordinates with generic features
compare same-parameter ablated model
```

## SCIENTIFIC_DEBT_BLOCKER

Allowed actions:

```txt
map debt to claims
block affected claims
allow only scoped claims
```

## CLAIM_PERMISSION_BLOCKER

Allowed actions:

```txt
emit blocked claims
emit allowed limited claims
create validation candidate only if permitted
```

## HUMAN_REVIEW_BLOCKER

Allowed actions:

```txt
create exact human review packet
include pages/figures/tables/snippets/actions
stop until human result exists
```

## EXPERIMENT_REQUIRED_BLOCKER

Allowed actions:

```txt
design minimal experiment
define observables
define sensitivity
define required measurements
do not fabricate experimental data
```

---

## 3. Minimal improvement rule

For each blocker, the AI must implement the smallest improvement that can plausibly remove it.

Required record:

```txt
blocker_id
blocker_type
gate_failed
minimal_improvement
why this is minimal
artifacts_created
tests_added
gate_reexecuted
result
```

---

## 4. Anti-overengineering rule

If a blocker can be resolved by reviewing one file, do not build a framework.

If a blocker can be resolved by one schema validator, do not create a new architecture layer.

If a blocker requires human review, create the packet and stop.

---

## 5. Final principle

```txt
Improve only what the blocker demands.
```
