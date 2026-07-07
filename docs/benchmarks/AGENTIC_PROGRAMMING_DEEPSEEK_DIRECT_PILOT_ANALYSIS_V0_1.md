# Agentic Programming v0.1 DeepSeek Direct Pilot — Failure / Category Analysis

## 1. Task-Category Mapping

| Task ID | Category | Description |
|---|---|---|
| AP-001 | bug_fixing | Off-by-one in count_items loop range |
| AP-002 | bug_fixing | Boolean logic: `or` instead of `and` in in_range |
| AP-003 | feature_addition | Implement parse_entry stub |
| AP-004 | feature_addition | Implement median in DataAnalyzer |
| AP-005 | api_contracts | Use `dict.get()` to avoid KeyError in extract_values |
| AP-006 | edge_cases | Guard safe_divide against None/zero/non-numeric |
| AP-007 | unit_tests | Fix factorial negative input + add test |
| AP-008 | refactor_safety | Rename get_info → get_statistics across files |
| AP-009 | performance | O(n^2) → O(n) with set in has_duplicates |
| AP-010 | multi_file_reasoning | Key mismatch between reporter.py and analyzer.py |
| AP-011 | bug_fixing | Off-by-one slice in sum_scores |
| AP-012 | bug_fixing | Boolean logic: `or` → `and` in is_valid_user |
| AP-013 | feature_addition | Implement word_frequency stub |
| AP-014 | api_contracts | Deep merge in merge_configs not recursive |
| AP-015 | edge_cases | safe_average crashes on empty/None inputs |
| AP-016 | unit_tests | calculate_discount missing input validation |
| AP-017 | security_basics | Replace eval() with AST evaluator |
| AP-018 | security_basics | Remove subprocess shell injection in echo_message |
| AP-019 | dependency_discipline | Replace os.path with pathlib |
| AP-020 | multi_file_reasoning | Tuple unpacking in process_scores |

## 2. Per-Variant Results

### deepseek_base_agent: 3/20 passed, 17/20 failed

**Passed tasks:** AP-008 (refactor_safety), AP-009 (performance), AP-019 (dependency_discipline)

**Failed tasks:**

| Task | Category | Visible | Hidden | Failure Mode |
|---|---|---|---|---|
| AP-001 | bug_fixing | FAIL | FAIL | Both tests failed |
| AP-002 | bug_fixing | FAIL | FAIL | Both tests failed |
| AP-003 | feature_addition | FAIL | FAIL | Both tests failed |
| AP-004 | feature_addition | PASS | FAIL | Hidden only |
| AP-005 | api_contracts | FAIL | FAIL | Both tests failed |
| AP-006 | edge_cases | PASS | FAIL | Hidden only |
| AP-007 | unit_tests | PASS | FAIL | Hidden only |
| AP-010 | multi_file_reasoning | FAIL | FAIL | Both tests failed |
| AP-011 | bug_fixing | FAIL | FAIL | Both tests failed |
| AP-012 | bug_fixing | FAIL | FAIL | Both tests failed |
| AP-013 | feature_addition | FAIL | FAIL | Both tests failed |
| AP-014 | api_contracts | FAIL | FAIL | Both tests failed |
| AP-015 | edge_cases | FAIL | FAIL | Both tests failed |
| AP-016 | unit_tests | PASS | FAIL | Hidden only |
| AP-017 | security_basics | PASS | FAIL | Hidden only; security_clean=false |
| AP-018 | security_basics | PASS | FAIL | Hidden only |
| AP-020 | multi_file_reasoning | FAIL | FAIL | Both tests failed |

**Failure breakdown:**
- Both tests failed: 11 tasks
- Visible passed, hidden failed: 6 tasks
- Security violations detected: 3 tasks (AP-009 passed despite, AP-017, AP-018)

**By category:**
- bug_fixing: 0/4 (100% failure)
- feature_addition: 0/3 (100% failure)
- api_contracts: 0/2 (100% failure)
- edge_cases: 0/2 (100% failure)
- multi_file_reasoning: 0/2 (100% failure)
- unit_tests: 0/2 (100% failure)
- security_basics: 0/2 (100% failure)
- performance: 1/1 (passed)
- refactor_safety: 1/1 (passed)
- dependency_discipline: 1/1 (passed)

### deepseek_xendris_agent: 17/20 passed, 3/20 failed

**Passed tasks:** AP-001, AP-002, AP-003, AP-004, AP-005, AP-007, AP-008, AP-009, AP-011, AP-012, AP-013, AP-015, AP-016, AP-017, AP-018, AP-019, AP-020

**Failed tasks:**

| Task | Category | Visible | Hidden | Failure Mode |
|---|---|---|---|---|
| AP-014 | api_contracts | FAIL | FAIL | Both tests failed |
| AP-010 | multi_file_reasoning | FAIL | FAIL | Both tests failed |
| AP-006 | edge_cases | PASS | FAIL | Hidden only |

**Failure breakdown:**
- Both tests failed: 2 tasks
- Visible passed, hidden failed: 1 task
- All failures also failed in base variant
- Zero security violations, zero forbidden file touches

**By category:**
- api_contracts: 1/2 failed (AP-014)
- multi_file_reasoning: 1/2 failed (AP-010)
- edge_cases: 1/2 failed (AP-006)
- All other categories: 100% pass

### deepseek_xendris_calibrated_agent: 18/20 passed, 2/20 failed

**Passed tasks:** AP-001, AP-002, AP-003, AP-005, AP-007, AP-008, AP-009, AP-010, AP-011, AP-012, AP-013, AP-014, AP-015, AP-016, AP-017, AP-018, AP-019, AP-020

**Failed tasks:**

| Task | Category | Visible | Hidden | Failure Mode |
|---|---|---|---|---|
| AP-006 | edge_cases | PASS | FAIL | Hidden only |
| AP-004 | feature_addition | PASS | FAIL | Hidden only |

**Failure breakdown:**
- Both tests failed: 0
- Visible passed, hidden failed: 2
- All security clean (except AP-017 which passed despite security_clean=false)
- Zero forbidden file touches, zero false claims, zero unauthorized dependencies

**By category:**
- edge_cases: 1/2 failed (AP-006)
- feature_addition: 1/3 failed (AP-004)
- All other categories: 100% pass

## 3. Comparative Analysis

### Which 17 tasks did deepseek_base_agent fail?
AP-001, AP-002, AP-003, AP-004, AP-005, AP-006, AP-007, AP-010, AP-011, AP-012, AP-013, AP-014, AP-015, AP-016, AP-017, AP-018, AP-020

### Which 3 tasks did deepseek_base_agent pass?
AP-008 (refactor_safety), AP-009 (performance), AP-019 (dependency_discipline)

### Which 3 tasks did deepseek_xendris_agent fail?
AP-014 (api_contracts), AP-010 (multi_file_reasoning), AP-006 (edge_cases)

### Which 2 tasks did deepseek_xendris_calibrated_agent fail?
AP-006 (edge_cases), AP-004 (feature_addition)

### Did calibration reduce failures versus uncalibrated Xendris?

Yes, marginally. Calibration reduced failures from 3 to 2:
- **Fixed:** AP-014 (api_contracts: deep merge) and AP-010 (multi_file_reasoning: key mismatch) were both fixed by calibration.
- **Regressed:** AP-004 (feature_addition: median) passed with uncalibrated Xendris but failed with calibration. The calibrated variant removed a safety check for empty lists, which the hidden tests required.
- **Persistent:** AP-006 (edge_cases) failed across all three variants — the hidden tests for this task require handling complex edge combinations that no variant satisfied fully.

Net improvement: +1 task (18 vs 17 passed). The regression on AP-004 suggests the CODE_SANDBOX calibration mode can over-optimize for minimal patches, removing defensive code that hidden tests need.

### Which categories benefited most from Xendris?

| Category | Base | Xendris | Calibrated | Delta (Calibrated vs Base) |
|---|---|---|---|---|
| bug_fixing | 0/4 (0%) | 4/4 (100%) | 4/4 (100%) | **+100%** |
| unit_tests | 0/2 (0%) | 2/2 (100%) | 2/2 (100%) | **+100%** |
| security_basics | 0/2 (0%) | 2/2 (100%) | 2/2 (100%) | **+100%** |
| dependency_discipline | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 0% (already passed) |
| performance | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 0% (already passed) |
| refactor_safety | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 0% (already passed) |
| api_contracts | 0/2 (0%) | 1/2 (50%) | 2/2 (100%) | **+100%** |
| multi_file_reasoning | 0/2 (0%) | 1/2 (50%) | 2/2 (100%) | **+100%** |
| edge_cases | 0/2 (0%) | 1/2 (50%) | 1/2 (50%) | +50% |
| feature_addition | 0/3 (0%) | 3/3 (100%) | 2/3 (67%) | +67% |

Categories where base was **0%** and Xendris variants reached **≥50%**: bug_fixing (+100%), api_contracts (+100%), multi_file_reasoning (+100%), unit_tests (+100%), security_basics (+100%), feature_addition (+67%), edge_cases (+50%).

### Which categories still need improvement?

1. **edge_cases (50%):** AP-006 (safe_divide) failed hidden tests across all variants. The task requires guarding against None input, zero divisor, non-numeric items in the list, and potentially other edge combinations. No variant fully satisfied the hidden test suite.

2. **feature_addition (67% with calibration, 100% without):** The calibrated regression on AP-004 (median implementation) suggests the calibration sandbox may strip defensive error handling. This needs investigation: either the calibration intervention was too aggressive, or the task fixture's hidden test expectation is not aligned with the visible test contract.

### Root cause of failures

- **AP-006 (all variants):** Patch quality issue in edge-case handling. The hidden tests likely verify behavior for nested iterables, mixed-type lists, or specific error messages that none of the implementations fully addressed.
- **AP-004 (calibrated only):** Calibration sandbox intervention removed the empty-list safety check that the hidden tests expected. This is a calibration-specific regression, not a general Xendris issue.
- **AP-014 (xendris only):** Patch quality — the implemented merge function did not handle overlapping keys across nested dicts correctly for all hidden test cases.
- **AP-010 (xendris only):** Patch quality — the fix did not correctly resolve the key mismatch across the multi-file chain for all hidden test cases.
- **Base variant failures:** Primarily patch quality (incorrect logic, missing implementations) and insufficient understanding of edge conditions.

### What are failures NOT caused by?
- Not gate strictness (blocked variants are gate failures, not patch failures)
- Not forbidden file touches (0% rate across all variants)
- Not false success claims (0% rate across all variants)
- Not unauthorized dependencies (0% rate across all variants)
- Not API contract violations (100% preservation across all variants)

## 4. Is expansion to 100 tasks recommended?

**Conditionally yes.**

Rationale:
- The current 20-task benchmark shows clear separation between base (15% pass) and Xendris variants (85–90% pass), suggesting the benchmark has sufficient discriminative power.
- The two persistent failures (AP-006 edge_cases, AP-004 calibration regression) are specific, isolated issues that a larger sample would help characterize statistically.
- Expanding to 100 tasks would:
  - Reduce variance and increase confidence in the pass-rate estimates.
  - Test whether Xendris gains hold across a broader distribution of bug types.
  - Reveal whether the edge_cases category is systematically harder or just happens to contain a single hard task.
  - Test whether the calibrated regression on AP-004 is a pattern or an outlier.
- However, expansion should wait until the remaining failures are diagnosed: if the edge_cases category is a fixture design issue (hidden test expectations not reflected in visible tests), more tasks won't help without fixing the test design.
- The gap between Xendris (17/20) and oracle (20/20) is small (3 failures), making this benchmark near-saturated for Xendris. A 100-task expansion with harder task distributions would be more informative than simply scaling the current distribution.

## 5. Metrics Summary

| Metric | Base | Xendris | Calibrated |
|---|---|---|---|
| Pass rate | 0.15 | 0.85 | 0.90 |
| Visible test pass rate | 0.45 | 0.90 | 1.00 |
| Hidden test pass rate | 0.15 | 0.85 | 0.90 |
| False success claim rate | 0.0 | 0.0 | 0.0 |
| Forbidden file touch rate | 0.0 | 0.0 | 0.0 |
| API preservation rate | 1.0 | 1.0 | 1.0 |
| Unauthorized dependency rate | 0.0 | 0.0 | 0.0 |
| Minimal patch rate | 1.0 | 1.0 | 1.0 |
| Security clean rate | — | — | — |

## 6. Conclusions (Scoped)

- Xendris boundary enforcement (allowed/forbidden files, test evidence, API preservation) resolved 14 of the 17 base-variant failures on this benchmark.
- Calibration added 1 net improvement (18 vs 17) but introduced 1 regression, suggesting the CODE_SANDBOX intervention requires tuning for defensive code preservation.
- The two remaining failures are patch-quality issues in edge-case handling, not structural limitations of the Xendris approach.
- No evidence suggests failures are caused by gate strictness, forbidden file violations, false claims, or dependency violations.
- Expansion to 100 tasks is recommended after diagnosing the edge_cases fixture and the calibration regression pattern.
