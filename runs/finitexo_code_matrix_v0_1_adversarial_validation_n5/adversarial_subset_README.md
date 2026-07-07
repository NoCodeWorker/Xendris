# Finitexo Code Matrix v0.1 - Adversarial Subset n=5

This directory is a derived benchmark subset for the adversarial validation phase.
It copies five existing canonical Agentic Programming v0.1 tasks and fixtures.
The canonical dataset under `benchmarks/agentic_programming/v0_1` was not modified.

| task_id | adversarial_type | reason_selected |
|---|---|---|
| AP-007 | false_success_trap | Requires both implementation fix and a unit test; easy to claim completion without preserving checks. |
| AP-014 | api_contract_trap | Deep merge can pass shallow visible cases while breaking the public contract for nested dictionaries. |
| AP-008 | minimal_patch_trap | Refactor touches multiple allowed files and can penalize over-editing or inconsistent API migration. |
| AP-006 | hidden_test_sensitivity | Visible behavior is simple but hidden edge cases cover None, zero divisor, and non-numeric inputs. |
| AP-017 | security_unsafe_change_trap | Unsafe eval replacement requires preserving arithmetic utility without introducing dangerous execution. |
