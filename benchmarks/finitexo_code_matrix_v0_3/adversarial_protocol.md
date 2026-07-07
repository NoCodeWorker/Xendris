# Finitexo Code Matrix v0.3 - Adversarial Protocol

## Purpose

The v0.3 protocol reduces self-favoring benchmark risk by making baseline
strength, dataset origin, scoring blindness, and null-hypothesis preservation
explicit.

## Required Properties

- Tasks must not reuse v0.1 or v0.2 fixtures.
- Task prompts must not mention the system under evaluation.
- Blind scoring must remove variant, provider, model, and agent identity.
- Strong non-system baselines must be available before positive claims.
- H0 remains live by default.
- Provider execution must not occur without `--execute`.

## Blockers

Interpretation is blocked when:

- dataset hash is missing or invalid;
- task hashes are missing or invalid;
- scoring-contract hash is missing or invalid;
- identity leaks into blind scoring;
- strong baseline is unavailable;
- provider execution occurs without explicit execution mode;
- report wording implies universal or general coding superiority;
- sample size is too small for the claim being made.

