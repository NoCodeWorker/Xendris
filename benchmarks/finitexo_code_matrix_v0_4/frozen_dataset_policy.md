# Finitexo Code Matrix v0.4 - Frozen Dataset Policy

## Rules

- Frozen dataset tasks must not be modified in place.
- Any task, provenance, scoring, or manifest change requires an explicit version
  bump.
- Provenance records must remain linked to every frozen task.
- Hashes must be regenerated only after an authorized version bump.
- Provider execution is not authorized in v0.4.
- Model comparison is deferred to v0.5.
- External superiority claims are not authorized.
- Statistical significance claims are not authorized.
- Frozen dataset existence does not imply model performance validation.

## Boundary

```txt
candidate_pool != frozen_benchmark_dataset
acquisition_record != benchmark_task
adapted_candidate != frozen_benchmark_task
audit_pass != dataset_promotion
frozen_dataset_created != provider_performance_validated
```

## Authorized Claim

```txt
Finitexo Code Matrix v0.4 contains a frozen external/adapted candidate dataset with provenance and hash controls.
```

## Blocked Claims

- provider superiority demonstrated;
- Xendris superiority demonstrated;
- external benchmark performance validated;
- statistical significance established;
- production-readiness proven;
- verified third-party external benchmark.
