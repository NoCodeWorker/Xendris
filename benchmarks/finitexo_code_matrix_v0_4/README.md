# Finitexo Code Matrix v0.4

## Purpose

This package contains the first frozen external/adapted candidate dataset for
Finitexo Code Matrix.

It exists after the v0.3.x trust infrastructure block:

- v0.3 adversarial benchmark infrastructure;
- v0.3.1 external dataset intake;
- v0.3.2 external source acquisition gate;
- v0.3.3 external adaptation and contamination audit.

## Dataset Status

```txt
dataset_status: FROZEN
dataset_externality_label: EXTERNAL_ADAPTED_CANDIDATE_FREEZE
```

This is not an externally verified benchmark. The frozen tasks come from the
small set of candidates that passed the previous trust gates with conservative
labels and explicit provenance.

Only two tasks are frozen in v0.4 because only two v0.3.3 adaptation records
were eligible for future freeze or human-review freeze. The third-task target is
intentionally not met rather than promoting weaker or blocked records.

## Boundaries

```txt
candidate_pool != frozen_benchmark_dataset
acquisition_record != benchmark_task
adapted_candidate != frozen_benchmark_task
audit_pass != dataset_promotion
frozen_dataset_created != provider_performance_validated
```

## Final Decision

```txt
FROZEN_EXTERNAL_ADAPTED_DATASET_CREATED_NO_PROVIDER_EXECUTION
```
