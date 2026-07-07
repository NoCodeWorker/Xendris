# Finitexo Code Matrix v0.3 - Blind Scoring Protocol

## Purpose

Blind scoring prevents identity, provider, and variant labels from influencing
the score.

## Scorer Input

The blind scorer may receive only anonymized submission data, task evidence,
test outcomes, and scoring components.

It must not receive:

- variant;
- provider;
- model;
- agent_name;
- xendris_label;
- baseline_label.

## Identity Leak

If identity metadata reaches the scorer, the scoring decision must be:

```txt
blind_scoring_decision = FAILED
verified_success = false
```

The anonymization map must be stored separately and referenced only by hash.

