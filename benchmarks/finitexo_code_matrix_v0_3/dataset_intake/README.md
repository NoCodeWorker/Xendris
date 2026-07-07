# Finitexo Code Matrix v0.3.1 - Dataset Intake

This package validates source traceability and candidate task metadata before
any candidate can be considered for a future dataset promotion phase.

It does not execute providers, does not measure performance, and does not
modify the frozen v0.3 seed dataset.

The candidate pool is separate:

```txt
candidate_pool != frozen_benchmark_dataset
```

