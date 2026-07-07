# Finitexo Code Matrix v0.3 - Strong Baseline Protocol

## Purpose

The benchmark must compare against baselines strong enough to falsify the
hypothesis that prior gains were caused by weak prompts, weak discipline, or
benchmark-specific formatting.

## Required Baselines

- `weak_base_agent`
- `strong_base_agent`
- `test_disciplined_base_agent`
- `strong_non_xendris_agent`
- `xendris_agent`
- `xendris_calibrated_agent`

Unavailable variants must be reported as:

```txt
SKIPPED_VARIANT_NOT_AVAILABLE
```

## Interpretation

A weak baseline can be diagnostic but cannot support a positive advantage
claim.

A strong non-system baseline matching or outperforming the system is not a
benchmark failure. It is direct evidence against a strong architectural claim.

