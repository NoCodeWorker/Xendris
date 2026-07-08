"""Deterministic generation of v0.8.0 hard programming dataset n=30.

Usage:
    py -3.11 generate_hard_programming_n30.py

Output (all under output_dir):
    tasks/task_*.json          — 30 task files
    dataset_manifest.json      — task list with hashes
    dataset_hashes.json        — dataset_hash + manifest_hash
    provenance.json            — generation metadata
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE

TASK_VERSION = "0.8.0"
DIFFICULTY = "hard"
FAMILIES = [
    "algorithmic_reasoning",
    "stateful_refactor",
    "edge_case_handling",
    "api_design_consistency",
    "performance_constraints",
]

FAMILY_PREFIX = {
    "algorithmic_reasoning": "ar",
    "stateful_refactor": "sr",
    "edge_case_handling": "ec",
    "api_design_consistency": "ad",
    "performance_constraints": "pc",
}

PROHIBITED_CLAIMS = [
    "Model superiority — not authorized by this task.",
    "Production readiness — not evaluated here.",
    "External benchmark validity — not measured.",
    "Provider ranking — diagnostic-only.",
    "Wrapper improvement without paired comparison — not measured.",
]

BASE_TASK = {
    "task_version": TASK_VERSION,
    "difficulty": DIFFICULTY,
    "requires_external_access": False,
    "requires_code_execution": False,
    "provider_bias_check": "neutral",
    "prohibited_claims": PROHIBITED_CLAIMS,
}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _task_id(family: str, seq: int) -> str:
    prefix = FAMILY_PREFIX[family]
    return f"finitexo_v0_8_0_{prefix}_{seq:03d}"


# ---------------------------------------------------------------------------
# Task definitions
# ---------------------------------------------------------------------------

def _build_tasks() -> list[dict]:
    tasks: list[dict] = []

    def add(family: str, seq: int, **kw: object) -> None:
        task = dict(BASE_TASK)
        task["task_id"] = _task_id(family, seq)
        task["family"] = family
        task.update(kw)
        tasks.append(task)

    # ---- algorithmic_reasoning ----

    add("algorithmic_reasoning", 1,
        title="Interval Merging with Conflict Rules",
        prompt=(
            "Implement a function `merge_intervals(intervals)` that processes a list of intervals.\n\n"
            "Each interval is a dict: `{'start': int, 'end': int, 'label': str}`.\n"
            "Intervals are inclusive on both ends.\n\n"
            "Rules:\n"
            "1. If two intervals overlap AND have the same label, merge them into one interval "
            "covering the union of their ranges, keeping the label.\n"
            "2. If two intervals overlap AND have different labels, keep both intervals "
            "unchanged but mark each with `'conflict': True`.\n"
            "3. Non-overlapping intervals are returned as-is.\n"
            "4. Overlap means `interval1.start <= interval2.end and interval2.start <= interval1.end`.\n\n"
            "Handle: empty input list, intervals where start > end (treat as invalid and skip), "
            "intervals with negative values, merging chains of three or more overlapping intervals."
        ),
        public_contract="merge_intervals(intervals: list[dict]) -> list[dict]",
        constraints=[
            "Do not modify the input list in place.",
            "Return a new list.",
            "Preserve the relative order of non-overlapping intervals as they appear in input.",
        ],
        expected_failure_modes=[
            "Not handling chains of 3+ overlapping intervals correctly.",
            "Failing to preserve both conflicting intervals.",
            "Marking non-conflicting intervals as conflicting due to incorrect overlap check.",
            "Mutating the input list.",
        ],
        scoring_focus=[
            "Correct overlap detection.",
            "Correct merge vs conflict decision.",
            "Handling of chains.",
            "Input immutability.",
            "Edge cases: empty, invalid intervals, negative values.",
        ],
        allowed_assumptions=["Intervals may be unsorted.", "Labels are non-empty strings."],
        disallowed_assumptions=["No overlapping intervals.", "Intervals are sorted.", "Labels are unique."],
    )

    add("algorithmic_reasoning", 2,
        title="Dependency Ordering with Cycle Reporting",
        prompt=(
            "Implement `resolve_dependencies(tasks)` that accepts a list of task dicts.\n"
            "Each task has `{'id': str, 'depends_on': list[str]}`.\n\n"
            "Return a dict with:\n"
            "- `'order': list[str]` — a valid topological order of task IDs (if acyclic).\n"
            "- `'cycle': list[str] | None` — if a cycle is detected, return one cycle as a list "
            "of task IDs forming the cycle, and set `'order'` to an empty list.\n\n"
            "Handle: tasks with no dependencies, multiple disconnected components, "
            "tasks that depend on non-existent IDs (treat as missing dependency, skip that task), "
            "empty task list, None dependencies (treat as empty list)."
        ),
        public_contract="resolve_dependencies(tasks: list[dict]) -> dict",
        constraints=[
            "Return a single cycle, not all cycles.",
            "Cycle list should show the cyclic path start to finish.",
            "Tasks with missing dependencies should be listed in order but placed after available tasks.",
        ],
        expected_failure_modes=[
            "Not detecting cycles correctly.",
            "Reporting order even when a cycle exists.",
            "Not handling missing dependencies.",
            "Stack overflow on large inputs.",
        ],
        scoring_focus=[
            "Correct topological order for acyclic graphs.",
            "Correct cycle detection.",
            "Handling missing dependencies.",
            "Multiple disconnected components.",
            "Edge cases: empty, single task, self-dependency.",
        ],
        allowed_assumptions=["Task IDs are unique strings.", "depends_on may be None."],
        disallowed_assumptions=["No cycles.", "All dependencies exist.", "Only one connected component."],
    )

    add("algorithmic_reasoning", 3,
        title="Bounded Cache Eviction Logic",
        prompt=(
            "Implement a class `BoundedCache` with:\n"
            "- `__init__(self, capacity: int)` — raises ValueError if capacity < 1.\n"
            "- `get(self, key: str) -> object | None` — returns value or None.\n"
            "- `put(self, key: str, value: object) -> None` — inserts or updates.\n\n"
            "Eviction policy when at capacity:\n"
            "1. Prefer to evict items with the lowest access frequency.\n"
            "2. Among items with the same frequency, evict the least recently used.\n"
            "3. On `put` of an existing key, update the value and reset its frequency to 1.\n"
            "4. On `get` of an existing key, increment its frequency by 1.\n\n"
            "Handle: capacity=1, updating existing keys, repeated gets on the same key, "
            "putting None as a value (valid), key with empty string (valid)."
        ),
        public_contract="BoundedCache.get(key) -> object | None; BoundedCache.put(key, value) -> None",
        constraints=[
            "Must be O(1) or O(log n) average for get and put.",
            "Do not use OrderedDict or built-in LRU cache.",
            "Do not leak internal state.",
        ],
        expected_failure_modes=[
            "Evicting wrong item when frequencies are equal.",
            "Not updating frequency on get.",
            "Resetting frequency on put of existing key incorrectly.",
            "Using O(n) eviction scan.",
        ],
        scoring_focus=[
            "Correct eviction policy (frequency then recency).",
            "Time complexity of operations.",
            "Correct handling of capacity=1.",
            "Updating existing key resets frequency to 1.",
            "Edge cases.",
        ],
        allowed_assumptions=["Keys are strings.", "Values are any hashable object."],
        disallowed_assumptions=["Values are never None.", "Capacity is always large.", "All keys are accessed at least once."],
    )

    add("algorithmic_reasoning", 4,
        title="Stable Grouping with Tie-Breaking",
        prompt=(
            "Implement `group_stable(records, key_fn, tie_breaker=None)`.\n\n"
            "Group records by `key_fn(record)`. Within each group, preserve original order.\n"
            "If `tie_breaker` is provided, it is a function `(key) -> comparable` that "
            "determines the order of groups: groups are sorted by `tie_breaker(key)`.\n"
            "Within a group, records remain in original order.\n\n"
            "Return a list of groups, each group being a dict:\n"
            "{'key': key, 'records': [record, ...]}\n\n"
            "Handle: key_fn returning None (group as 'None' key), "
            "tie_breaker returning non-comparable types consistently, "
            "empty record list, key_fn raising an exception (skip that record and continue)."
        ),
        public_contract="group_stable(records: list, key_fn: callable, tie_breaker: callable | None) -> list[dict]",
        constraints=[
            "Must be stable: within-group order equals original order.",
            "Do not modify the input list.",
            "Groups must be in tie_breaker order if provided, else in order of first appearance.",
        ],
        expected_failure_modes=[
            "Losing original order within groups.",
            "Not handling None keys.",
            "Crashing when key_fn raises on a record instead of skipping it.",
            "Incorrect group ordering without tie_breaker.",
        ],
        scoring_focus=[
            "Stable grouping.",
            "Tie-breaker sorting of groups.",
            "Handling None keys and exceptions.",
            "Empty input.",
        ],
        allowed_assumptions=["Records are hashable.", "key_fn is deterministic for the same input."],
        disallowed_assumptions=["key_fn never returns None.", "key_fn never raises.", "tie_breaker is always provided."],
    )

    add("algorithmic_reasoning", 5,
        title="Parser-Like Transformation with Malformed Input",
        prompt=(
            "Implement `parse_markup(text: str) -> dict` that parses a simple markup format.\n\n"
            "Markup patterns:\n"
            "- `**text**` → {'type': 'bold', 'content': 'text'}\n"
            "- `[[link]]` → {'type': 'link', 'content': 'link'}\n"
            "- `{{cite}}`  → {'type': 'cite', 'content': 'cite'}\n\n"
            "Return a dict:\n"
            "{'segments': [...], 'errors': [{'position': int, 'description': str}, ...]}\n\n"
            "Malformed cases to handle:\n"
            "- Unclosed `**` — produce a segment of type 'text' up to the unclosed marker.\n"
            "- Nested markers inside each other (e.g., `**[[text]]**`) — keep outer, "
            "convert inner to plain text within the outer.\n"
            "- Empty markers (`****`, `[[]]`) — produce an error but still include an empty segment.\n"
            "- Markers split across lines — treat as invalid, produce error.\n"
            "- Regular text with no markers — single text segment, no errors."
        ),
        public_contract="parse_markup(text: str) -> dict",
        constraints=[
            "Errors must reference character position in the original string.",
            "Segments must be in order of appearance.",
            "Do not raise exceptions for malformed input; report errors in the result.",
        ],
        expected_failure_modes=[
            "Raising exceptions instead of reporting errors.",
            "Not handling nested markers correctly.",
            "Incorrect error positions.",
            "Losing content inside malformed markers.",
        ],
        scoring_focus=[
            "Correct parsing of valid markup.",
            "Graceful error reporting for malformed input.",
            "Correct nesting behavior.",
            "Position tracking in errors.",
        ],
        allowed_assumptions=["Markers are not escaped.", "Text is Unicode.", "Markers do not span more than two lines."],
        disallowed_assumptions=["Input is always valid.", "No nesting.", "Markers are always closed."],
    )

    add("algorithmic_reasoning", 6,
        title="Diff/Patch Planning with Invariants",
        prompt=(
            "Implement `compute_diff(a: dict, b: dict, invariants: list[str]) -> dict`.\n\n"
            "Given two nested dicts `a` and `b`, compute a minimal diff that transforms `a` into `b`.\n"
            "Return a dict with:\n"
            "- `'changes'`: list of change objects, each with `{'path': str, 'type': 'add'|'remove'|'modify', 'old_value': ..., 'new_value': ...}`\n"
            "- `'invariant_violations'`: list of paths where a change was attempted but the key is in `invariants`\n"
            "- `'is_compatible'`: bool — True if no invariant violations\n\n"
            "Rules:\n"
            "- Changes should be recursive: nested dict changes are at their full dotted path.\n"
            "- Only report leaf changes (not intermediate nodes that are containers).\n"
            "- If a key is in `invariants`, any change to it or its descendants is a violation.\n"
            "- Handle: keys present in `a` but not `b` (removal), keys in `b` but not `a` (addition), "
            "keys in both with different values (modification), nested dicts that are structurally identical, "
            "empty dicts."
        ),
        public_contract="compute_diff(a: dict, b: dict, invariants: list[str]) -> dict",
        constraints=[
            "Do not modify input dicts.",
            "Paths should be dot-separated: 'key.subkey.leaf'.",
            "Invariant violations take priority: if a path is invariant, report violation even if value matches.",
        ],
        expected_failure_modes=[
            "Reporting intermediate container nodes as changes.",
            "Not detecting nested invariant violations.",
            "Missing keys where value is None vs absent.",
            "Incorrect path formatting.",
        ],
        scoring_focus=[
            "Correct recursive diff.",
            "Invariant enforcement.",
            "Correct change types (add/remove/modify).",
            "Path correctness.",
        ],
        allowed_assumptions=["Dict values are JSON-serializable.", "Keys are strings without dots."],
        disallowed_assumptions=["No nesting.", "All keys are in both dicts.", "No invariants to check."],
    )

    # ---- stateful_refactor ----

    add("stateful_refactor", 1,
        title="Refactor State Transitions",
        prompt=(
            "You are given a state machine implemented as:\n\n"
            "class StateMachine:\n"
            "    def __init__(self):\n"
            "        self.state = 'idle'\n\n"
            "    def transition(self, event: str) -> str:\n"
            "        if self.state == 'idle' and event == 'start':\n"
            "            self.state = 'running'\n"
            "            return 'started'\n"
            "        elif self.state == 'running' and event == 'pause':\n"
            "            self.state = 'paused'\n"
            "            return 'paused'\n"
            "        elif self.state == 'running' and event == 'stop':\n"
            "            self.state = 'stopped'\n"
            "            return 'stopped'\n"
            "        elif self.state == 'paused' and event == 'resume':\n"
            "            self.state = 'running'\n"
            "            return 'resumed'\n"
            "        elif self.state == 'paused' and event == 'stop':\n"
            "            self.state = 'stopped'\n"
            "            return 'stopped'\n"
            "        else:\n"
            "            return 'invalid_transition'\n\n"
            "Refactor this into a table-driven state machine using a transition table.\n"
            "The `transition` method must accept the same signature and return the same types.\n"
            "The external behavior must be identical for all valid and invalid transitions."
        ),
        public_contract="StateMachine.transition(event: str) -> str (identical behavior)",
        constraints=[
            "Do not change __init__ signature.",
            "Do not add public methods.",
            "transition must return exactly the same strings for the same inputs.",
            "Use a data structure (dict or list) for the transition table, not if/elif chains.",
        ],
        expected_failure_modes=[
            "Changing return strings.",
            "Adding or removing valid transitions.",
            "Not handling invalid transitions identically.",
            "Changing __init__ behavior.",
        ],
        scoring_focus=[
            "Behavioral equivalence.",
            "Table-driven approach.",
            "No new public API surface.",
            "All valid transitions preserved.",
        ],
        allowed_assumptions=["No new states or events need to be added.", "Thread safety is not required."],
        disallowed_assumptions=["The transition table must be a dict lookup only.", "Error handling should be changed."],
    )

    add("stateful_refactor", 2,
        title="Separate Validation from Mutation",
        prompt=(
            "Given a class:\n\n"
            "class AccountManager:\n"
            "    def __init__(self):\n"
            "        self.accounts = {}\n\n"
            "    def batch_update(self, updates: list[dict]) -> list[str]:\n"
            "        results = []\n"
            "        for u in updates:\n"
            "            if 'id' not in u or 'balance' not in u:\n"
            "                results.append('invalid')\n"
            "                continue\n"
            "            if u['balance'] < 0:\n"
            "                results.append('negative')\n"
            "                continue\n"
            "            self.accounts[u['id']] = u['balance']\n"
            "            results.append('ok')\n"
            "        return results\n\n"
            "Refactor `batch_update` to separate validation from mutation:\n"
            "1. First validate ALL updates without mutating any state.\n"
            "2. If ALL updates are valid, mutate ALL of them.\n"
            "3. If ANY update is invalid, mutate NONE and return errors for all invalid items.\n\n"
            "All updates must be atomic: either all succeed or none are applied."
        ),
        public_contract="AccountManager.batch_update(updates: list[dict]) -> list[str]",
        constraints=[
            "Do not change __init__.",
            "Do not change return format.",
            "Do not change the validation rules.",
            "Must be atomic: all or nothing.",
        ],
        expected_failure_modes=[
            "Applying partial updates before detecting an invalid one.",
            "Changing validation rules.",
            "Not rolling back on failure.",
            "Changing return values for the same inputs.",
        ],
        scoring_focus=[
            "Atomicity of batch_update.",
            "Separation of validation and mutation.",
            "Backward-compatible behavior for valid inputs.",
            "Correct error reporting.",
        ],
        allowed_assumptions=["Updates are independent of each other.", "No concurrent access."],
        disallowed_assumptions=["All updates are valid.", "Partial updates are acceptable."],
    )

    add("stateful_refactor", 3,
        title="Preserve Backward-Compatible Config Loading",
        prompt=(
            "Given a config loader:\n\n"
            "class ConfigLoader:\n"
            "    def load(self, path: str) -> dict:\n"
            "        raw = json.load(open(path))\n"
            "        return {k.upper(): v for k, v in raw.items()}\n\n"
            "Extend it to support nested config sections using dot notation.\n"
            "For example, a config file with:\n"
            "{\n"
            '  "database": {"host": "localhost", "port": 5432},\n'
            '  "debug": true\n'
            "}\n\n"
            "Should produce:\n"
            "{\n"
            '  "DATABASE_HOST": "localhost",\n'
            '  "DATABASE_PORT": 5432,\n'
            '  "DEBUG": true\n'
            "}\n\n"
            "Existing flat keys must still work: {'host': 'localhost'} -> {'HOST': 'localhost'}.\n"
            "Do not break existing callers that rely on key names without dots."
        ),
        public_contract="ConfigLoader.load(path: str) -> dict (backward-compatible keys)",
        constraints=[
            "Existing callers must see no difference for flat configs.",
            "Nested keys produce UPPER_CASE with underscore separator.",
            "Do not introduce any new public methods.",
        ],
        expected_failure_modes=[
            "Breaking existing key names for flat configs.",
            "Not handling mixed flat and nested configs.",
            "Using dot in key names instead of underscore.",
            "Incorrect case transformation for nested values.",
        ],
        scoring_focus=[
            "Backward compatibility for flat configs.",
            "Correct flattening of nested configs.",
            "No new public API.",
            "Consistent naming convention.",
        ],
        allowed_assumptions=["Config files are valid JSON.", "Nested values are dicts, not lists."],
        disallowed_assumptions=["Configs are always flat.", "No mixed flat+nested configs exist.", "Case does not matter."],
    )

    add("stateful_refactor", 4,
        title="Fix Shared Mutable Default",
        prompt=(
            "Given a class with a mutable default argument:\n\n"
            "class TaskTracker:\n"
            "    def __init__(self, tasks: list = []):\n"
            "        self.tasks = tasks\n\n"
            "    def add_task(self, task: str) -> None:\n"
            "        self.tasks.append(task)\n\n"
            "    def list_tasks(self) -> list:\n"
            "        return self.tasks\n\n"
            "The mutable default causes unexpected sharing between instances.\n"
            "Fix it so each instance has its own list.\n"
            "Do not change the external behavior of any public method.\n"
            "Do not change the constructor signature.\n"
            "Existing callers that pass an explicit list must still work."
        ),
        public_contract="All public methods behave identically except shared default is fixed.",
        constraints=[
            "Constructor signature must remain `__init__(self, tasks: list = [])`.",
            "Existing callers that pass a list explicitly must not notice any change.",
            "Instances created without arguments must have independent lists.",
        ],
        expected_failure_modes=[
            "Changing constructor signature.",
            "Breaking explicit list passing.",
            "Still sharing state after fix.",
            "Using a sentinel incorrectly.",
        ],
        scoring_focus=[
            "Correct fix for mutable default.",
            "Backward compatibility of constructor.",
            "Independence of instances.",
            "No behavioral change for explicit list callers.",
        ],
        allowed_assumptions=["Tasks are strings.", "Thread safety is not required."],
        disallowed_assumptions=["No one passes an explicit list.", "The default is never used."],
    )

    add("stateful_refactor", 5,
        title="Make Retry State Explicit",
        prompt=(
            "Given a retry utility:\n\n"
            "class RetryHandler:\n"
            "    _attempts: dict = {}\n\n"
            "    @classmethod\n"
            "    def run(cls, task_id: str, fn: callable) -> object:\n"
            "        if task_id not in cls._attempts:\n"
            "            cls._attempts[task_id] = 0\n"
            "        cls._attempts[task_id] += 1\n"
            "        try:\n"
            "            return fn()\n"
            "        except Exception:\n"
            "            if cls._attempts[task_id] < 3:\n"
            "                return cls.run(task_id, fn)\n"
            "            raise\n\n"
            "Refactor to make retry state explicit:\n"
            "- Remove the class-level `_attempts` dict.\n"
            "- Pass retry state as a parameter or use instance-level state.\n"
            "- The refactored version must preserve the retry behavior: "
            "max 3 attempts per task_id, return first success, re-raise after 3 failures."
        ),
        public_contract="RetryHandler.run(task_id, fn) -> object with identical retry behavior.",
        constraints=[
            "Do not change the `run` method signature (task_id, fn).",
            "Do not use module-level or class-level mutable state.",
            "Retry behavior (3 attempts, return first success, re-raise on final failure) must be preserved.",
        ],
        expected_failure_modes=[
            "Changing retry count.",
            "Still using global state.",
            "Changing error behavior (e.g., returning None instead of raising).",
            "Changing the run method signature.",
        ],
        scoring_focus=[
            "Elimination of implicit global state.",
            "Behavioral equivalence of retry logic.",
            "Preserved error behavior.",
            "Clean separation of state.",
        ],
        allowed_assumptions=["fn is a callable with no arguments.", "Exceptions are subclasses of Exception."],
        disallowed_assumptions=["Retry state does not matter.", "run is called sequentially per task_id."],
    )

    add("stateful_refactor", 6,
        title="Avoid Global-State Leakage",
        prompt=(
            "Given a module that caches results at module level:\n\n"
            "_cache = {}\n\n"
            "def compute(key: str, value: int) -> int:\n"
            "    if key not in _cache:\n"
            "        _cache[key] = value * 2\n"
            "    return _cache[key]\n\n"
            "Multiple consumers sharing this module experience unexpected interference "
            "because one consumer's cached values affect another's results.\n\n"
            "Refactor using a class so that each consumer has its own cache instance:\n"
            "- `__init__(self)` initializes an empty cache.\n"
            "- `compute(self, key: str, value: int) -> int` uses the instance cache.\n"
            "- The computation logic remains the same (value * 2, cached by key).\n"
            "- Existing code using `compute(key, value)` as a module function should still work "
            "by providing a backward-compatible module-level wrapper that creates a default global instance."
        ),
        public_contract="module-level compute(key, value) -> int works as before; class-level also available.",
        constraints=[
            "The module-level `compute` function must remain importable and callable.",
            "A class version must be available for per-instance caching.",
            "The computation and caching logic must be identical.",
        ],
        expected_failure_modes=[
            "Removing the module-level function.",
            "Changing computation logic.",
            "Not providing per-instance isolation.",
            "Breaking existing imports.",
        ],
        scoring_focus=[
            "Per-instance cache isolation.",
            "Backward-compatible module-level API.",
            "Identical computation logic.",
            "No leak between instances.",
        ],
        allowed_assumptions=["Keys are strings.", "Values are integers.", "Thread safety is not required."],
        disallowed_assumptions=["There is only one consumer.", "Module-level caching is fine for all use cases."],
    )

    # ---- edge_case_handling ----

    add("edge_case_handling", 1,
        title="Batch Processing with Empty and Null Inputs",
        prompt=(
            "Implement `process_batch(records: list | None) -> dict`.\n\n"
            "Each record is a dict with optional fields: `name` (str), `value` (float), `tags` (list[str]).\n\n"
            "Return a dict:\n"
            "{'count': int, 'sum': float, 'mean': float, 'names': list[str], 'tag_frequencies': dict[str, int]}\n\n"
            "Rules:\n"
            "- If `records` is None or empty, return `{'count': 0, 'sum': 0.0, 'mean': 0.0, 'names': [], 'tag_frequencies': {}}`.\n"
            "- If a record has `value` as None, skip it in sum/mean calculation but count it in `count`.\n"
            "- If a record has `name` as None or missing, exclude it from `names`.\n"
            "- If `tags` is None or missing, treat as empty list.\n"
            "- `mean` is `sum / count_of_non_null_values`; if all values are None, mean is 0.0.\n"
            "- Return types must be consistent regardless of inputs."
        ),
        public_contract="process_batch(records) -> dict with consistent shape",
        constraints=[
            "Return type must be identical for all inputs (same keys, same types).",
            "Do not raise exceptions for invalid records; skip gracefully.",
        ],
        expected_failure_modes=[
            "Raising on None input.",
            "Incorrect count when some values are None.",
            "Division by zero when all values are None.",
            "Inconsistent return type keys.",
        ],
        scoring_focus=[
            "Graceful handling of empty/None inputs.",
            "Correct counting with null values.",
            "Consistent return shape.",
            "No exceptions for edge cases.",
        ],
        allowed_assumptions=["Records are dicts or None.", "Values are floats or None."],
        disallowed_assumptions=["Input is never None.", "All records have all fields.", "At least one record has a non-null value."],
    )

    add("edge_case_handling", 2,
        title="Merge with Duplicate Keys and Resolver",
        prompt=(
            "Implement `merge_dicts(lists: list[list], resolver: callable | None = None) -> dict`.\n\n"
            "Each element of `lists` is a list of `(key, value)` pairs.\n"
            "Merge all pairs into a single dict.\n\n"
            "Rules:\n"
            "- If a key appears only once, keep its value.\n"
            "- If a key appears multiple times:\n"
            "  - If `resolver` is provided, call `resolver(key, [value1, value2, ...])` and use its return.\n"
            "  - If `resolver` is None, keep the first occurrence's value.\n"
            "- Keys with None as value should still be included (None is a valid value).\n"
            "- Handle: empty lists of pairs, empty outer list, None resolver, resolver that returns None."
        ),
        public_contract="merge_dicts(lists: list[list], resolver: callable | None = None) -> dict",
        constraints=[
            "Do not modify input lists.",
            "Resolver order: values in the list passed to resolver should be in order of appearance.",
        ],
        expected_failure_modes=[
            "Excluding keys with None values.",
            "Calling resolver with wrong argument order.",
            "Not handling empty lists.",
            "Not preserving order for resolver callback.",
        ],
        scoring_focus=[
            "Correct handling of duplicates without resolver.",
            "Correct resolver invocation.",
            "Including None-valued keys.",
            "Empty inputs.",
        ],
        allowed_assumptions=["Keys are hashable.", "Pairs are always (key, value) tuples."],
        disallowed_assumptions=["No duplicate keys.", "Values are never None.", "resolver is always provided."],
    )

    add("edge_case_handling", 3,
        title="Case-Insensitive Processing with Casing Preservation",
        prompt=(
            "Implement `dedup_preserve_case(items: list[str]) -> list[str]`.\n\n"
            "Remove duplicates from a list of strings, comparing case-insensitively.\n"
            "Preserve the original casing of the first occurrence.\n\n"
            "Example:\n"
            "Input: ['Foo', 'bar', 'FOO', 'Bar', 'baz']\n"
            "Output: ['Foo', 'bar', 'baz']\n\n"
            "Rules:\n"
            "- Comparison must be case-insensitive but Unicode-aware (lower() is acceptable).\n"
            "- Preserve the casing of the first occurrence.\n"
            "- Maintain original order of first occurrences.\n"
            "- Handle: empty list, None in list (treat None as a distinct value, compared by identity), "
            "empty strings, strings with only different case."
        ),
        public_contract="dedup_preserve_case(items: list[str | None]) -> list[str | None]",
        constraints=[
            "Do not modify the input list.",
            "Preserve original order of first occurrences.",
            "None values are distinct from string 'None'.",
        ],
        expected_failure_modes=[
            "Not preserving original casing.",
            "Incorrect handling of None values.",
            "Not maintaining order.",
            "Case-insensitive comparison not working for edge Unicode cases.",
        ],
        scoring_focus=[
            "Correct case-insensitive dedup.",
            "Casing preservation.",
            "Order preservation.",
            "None and empty string handling.",
        ],
        allowed_assumptions=["lower() is acceptable for comparison.", "Mixed Unicode and ASCII is possible."],
        disallowed_assumptions=["All strings are ASCII.", "No None values.", "No empty strings."],
    )

    add("edge_case_handling", 4,
        title="Partial Malformed Record Parsing",
        prompt=(
            "Implement `parse_partial_csv(text: str) -> dict`.\n\n"
            "Parse a simple CSV-like format where each line has: `id, name, value`.\n"
            "Fields may be quoted with double quotes. Quoted fields may contain commas.\n\n"
            "Return a dict:\n"
            "{'records': [{'id': str, 'name': str, 'value': str}, ...], 'errors': [{'line': int, 'description': str}, ...]}\n\n"
            "Handle:\n"
            "- Lines with fewer than 3 fields: record an error, skip the line.\n"
            "- Lines with more than 3 fields: include first 3 fields, record a warning (not an error).\n"
            "- Completely blank lines: skip silently, no error.\n"
            "- Quoted fields with embedded commas: parse correctly.\n"
            "- Unclosed quotes: treat as error, include partial content.\n"
            "- Header row: if first line is 'id,name,value', skip it as header."
        ),
        public_contract="parse_partial_csv(text: str) -> dict with 'records' and 'errors' keys",
        constraints=[
            "Do not use the csv module.",
            "Errors must include the 1-indexed line number.",
            "Do not raise exceptions; report errors in the result.",
        ],
        expected_failure_modes=[
            "Raising exceptions on malformed lines.",
            "Not handling quoted fields with commas.",
            "Incorrect line numbers in errors.",
            "Including blank lines as records or errors.",
        ],
        scoring_focus=[
            "Correct parsing of well-formed lines.",
            "Graceful error recovery for malformed lines.",
            "Correct quoted field handling.",
            "Header line detection.",
        ],
        allowed_assumptions=["Fields are separated by commas.", "Quotes are double quotes (`\"`)."],
        disallowed_assumptions=["All lines are well-formed.", "No quoted fields.", "No header row."],
    )

    add("edge_case_handling", 5,
        title="Timezone-Like Ordering Without External Libraries",
        prompt=(
            "Implement `sort_timestamps(timestamps: list[str]) -> list[str]`.\n\n"
            "Each timestamp is a string like: `'2024-01-15T10:30:00+05:00'` or `'2024-01-15T10:30:00Z'`.\n"
            "Sort chronologically. Do not use datetime libraries (no datetime, dateutil, pytz).\n\n"
            "Rules:\n"
            "- `Z` means UTC (+00:00).\n"
            "- Timestamps without offset are assumed UTC.\n"
            "- Offsets range from -12:00 to +14:00.\n"
            "- Invalid timestamp strings: sort to the end, in their original relative order.\n"
            "- Duplicate timestamps with different offsets: order by their actual UTC equivalent, "
            "and for equal UTC times, preserve input order (stable).\n"
            "- Handle: empty list, None in list (sort None to end), "
            "timestamps with different precision (some with seconds, some without)."
        ),
        public_contract="sort_timestamps(timestamps: list[str | None]) -> list[str | None]",
        constraints=[
            "Do not import datetime, dateutil, pytz, or similar.",
            "Must be stable sort.",
            "Invalid strings must not cause exceptions.",
        ],
        expected_failure_modes=[
            "Using banned libraries.",
            "Incorrect offset conversion to UTC.",
            "Exception on invalid timestamp.",
            "Not stable for equal UTC times.",
        ],
        scoring_focus=[
            "Correct chronological order.",
            "Offset to UTC conversion.",
            "Stable sort property.",
            "Handling invalid and None inputs.",
        ],
        allowed_assumptions=["Timestamp format is ISO 8601-like.", "Offsets are in whole hours."],
        disallowed_assumptions=["All timestamps are valid.", "No timezone offsets.", "No None values."],
    )

    add("edge_case_handling", 6,
        title="Stable Multi-Key Sort with Missing Fields",
        prompt=(
            "Implement `sort_records(records: list[dict], keys: list[str], missing_behavior: str = 'end') -> list[dict]`.\n\n"
            "Sort records by multiple keys in order of priority (first key is primary).\n"
            "If `missing_behavior` is `'end'`, records missing a sort key sort to the end of that sort level.\n"
            "If `missing_behavior` is `'begin'`, they sort to the beginning.\n\n"
            "Example:\n"
            "records = [{'name': 'Bob'}, {'name': 'Alice', 'age': 30}, {'name': 'Charlie'}]\n"
            "sort_records(records, ['name'], 'end')\n"
            "-> [{'name': 'Alice', 'age': 30}, {'name': 'Bob'}, {'name': 'Charlie'}]\n"
            "sort_records(records, ['age', 'name'], 'end')\n"
            "-> [{'name': 'Alice', 'age': 30}, {'name': 'Bob'}, {'name': 'Charlie'}]  (Bob and Charlie have no age)\n\n"
            "Rules:\n"
            "- Must be a stable sort (preserve input order for equal keys).\n"
            "- Missing means the key is not in the record dict.\n"
            "- None as a value is not missing; it is a valid value.\n"
            "- Handle: empty record list, empty keys list (return as-is), "
            "all records missing the primary key, mixed types in values."
        ),
        public_contract="sort_records(records, keys, missing_behavior='end') -> list[dict]",
        constraints=[
            "Use a stable sorting approach.",
            "Do not modify input records.",
        ],
        expected_failure_modes=[
            "Not stable for equal keys.",
            "Treating None as missing instead of as a value.",
            "Not handling empty keys list.",
            "Incorrect missing_behavior for cascading keys.",
        ],
        scoring_focus=[
            "Correct multi-key sort order.",
            "Stable property.",
            "Missing field handling (end vs begin).",
            "None as a valid value vs missing key.",
        ],
        allowed_assumptions=["Keys are strings.", "Values of the same key have comparable types."],
        disallowed_assumptions=["All records have all keys.", "No missing fields.", "missing_behavior is always 'end'."],
    )

    # ---- api_design_consistency ----

    add("api_design_consistency", 1,
        title="Add Optional Structured Result Without Breaking Callers",
        prompt=(
            "Given a function:\n\n"
            "def lookup(key: str) -> str:\n"
            "    data = {'a': 'result_a', 'b': 'result_b'}\n"
            "    return data.get(key, 'not_found')\n\n"
            "Extend it to support optional structured results:\n"
            "`lookup(key: str, structured: bool = False) -> str | dict`\n\n"
            "When `structured=False` (default), behavior must be identical to the original.\n"
            "When `structured=True`, return `{'found': bool, 'value': str | None, 'key': str}`.\n\n"
            "Existing callers that call `lookup('a')` or `lookup('a', False)` must see no change.\n"
            "Add at least 2 more entries to the data dict."
        ),
        public_contract="lookup(key: str, structured: bool = False) -> str | dict (backward-compatible default)",
        constraints=[
            "Default parameter must be False.",
            "Original callers with positional args must not break.",
            "Original callers with no second arg must not break.",
        ],
        expected_failure_modes=[
            "Changing default behavior.",
            "Breaking callers that pass `lookup('a')`.",
            "Incorrect return type for structured mode.",
            "Removing existing data entries.",
        ],
        scoring_focus=[
            "Backward compatibility of default.",
            "Correct structured result shape.",
            "No regression for existing callers.",
        ],
        allowed_assumptions=["Existing callers pass at most one argument.", "New callers may pass keyword arguments."],
        disallowed_assumptions=["All callers will be updated.", "The return type change does not matter."],
    )

    add("api_design_consistency", 2,
        title="Preserve JSON Schema Shape in Transformation Pipeline",
        prompt=(
            "Given a transformation pipeline:\n\n"
            "def transform(record: dict) -> dict:\n"
            "    return {\n"
            "        'id': record['id'],\n"
            "        'type': record.get('type', 'unknown'),\n"
            "        'value': record['value'] * 2 if 'value' in record else None,\n"
            "        'tags': record.get('tags', []),\n"
            "    }\n\n"
            "Modify this function to also compute a `'summary'` field: "
            "a string combining id, type, and value info.\n"
            "You must NOT remove, rename, or change the type of any existing field.\n"
            "The new `'summary'` field must be a string. Add it to the returned dict.\n"
            "If `'id'` is missing, raise KeyError (preserve original error behavior)."
        ),
        public_contract="transform(record: dict) -> dict with all original keys plus 'summary'",
        constraints=[
            "All existing output keys must be present with the same names.",
            "All existing output key types must remain the same.",
            "New field must be a string.",
        ],
        expected_failure_modes=[
            "Removing or renaming an existing field.",
            "Changing an existing field's type.",
            "Not adding the new field.",
            "Changing error behavior for missing id.",
        ],
        scoring_focus=[
            "All original keys present and unchanged.",
            "New field correctly added.",
            "Error behavior preserved.",
        ],
        allowed_assumptions=["record is always a dict.", "record['id'] exists for valid calls."],
        disallowed_assumptions=["The output schema can change.", "Existing fields can be modified."],
    )

    add("api_design_consistency", 3,
        title="Avoid Changing Exported Names",
        prompt=(
            "Given a module:\n\n"
            "# utils.py\n"
            "def _internal_helper(x):\n"
            "    return x * 2\n\n"
            "def process(data: list) -> list:\n"
            "    return [_internal_helper(d) for d in data]\n\n"
            "def cleanup(data: list) -> list:\n"
            "    return [d for d in data if d is not None]\n\n"
            "# __init__.py exports: process, cleanup\n\n"
            "Refactor the internal implementation: replace `_internal_helper` with a more efficient approach "
            "using a comprehension with inline logic.\n"
            "You MUST keep the `process` and `cleanup` function signatures and behavior identical.\n"
            "Do not add any new public names to the module."
        ),
        public_contract="The module exports exactly process and cleanup with unchanged signatures.",
        constraints=[
            "Do not rename or remove process or cleanup.",
            "Do not change their signatures.",
            "Do not add new public names.",
            "Behavior must be identical for all inputs.",
        ],
        expected_failure_modes=[
            "Renaming existing public functions.",
            "Adding new public names.",
            "Changing function behavior.",
            "Removing existing public functions from __init__.py exports.",
        ],
        scoring_focus=[
            "Public API unchanged.",
            "No new public names.",
            "Behavioral equivalence.",
        ],
        allowed_assumptions=["No external code relies on _internal_helper being present."],
        disallowed_assumptions=["New public functions can be added.", "Function signatures can be modified."],
    )

    add("api_design_consistency", 4,
        title="Maintain Backward-Compatible Defaults When Adding Parameters",
        prompt=(
            "Given a function:\n\n"
            "def fetch_items(page: int = 1, limit: int = 20) -> list:\n"
            "    start = (page - 1) * limit\n"
            "    end = start + limit\n"
            "    all_items = [f'item_{i}' for i in range(100)]\n"
            "    return all_items[start:end]\n\n"
            "Add a new parameter `sort_order: str = 'asc'` that controls result ordering.\n"
            "The default `'asc'` must produce identical behavior to the original function.\n"
            "Document what values are valid for sort_order in a docstring.\n"
            "If sort_order is not 'asc' or 'desc', raise ValueError."
        ),
        public_contract="fetch_items(page=1, limit=20, sort_order='asc') -> list (backward-compatible default)",
        constraints=[
            "Default parameter value must be 'asc'.",
            "Behavior with default must be identical to original.",
            "Raise ValueError for invalid sort_order values.",
            "Add a docstring describing the parameter.",
        ],
        expected_failure_modes=[
            "Changing default behavior.",
            "Not raising for invalid sort_order.",
            "Not adding parameter documentation.",
            "Adding parameter before existing optional parameters.",
        ],
        scoring_focus=[
            "Behavioral equivalence with default.",
            "Correct error handling for invalid sort_order.",
            "Documentation present.",
            "Parameter position (after existing optional params).",
        ],
        allowed_assumptions=["sort_order is always a string when provided."],
        disallowed_assumptions=["Default sort_order will never be used.", "sort_order is always valid."],
    )

    add("api_design_consistency", 5,
        title="Clarify Error Handling: Replace Bare Except",
        prompt=(
            "Given a function:\n\n"
            "def safe_divide_all(values: list, divisor: float) -> list:\n"
            "    results = []\n"
            "    for v in values:\n"
            "        try:\n"
            "            results.append(v / divisor)\n"
            "        except Exception:\n"
            "            results.append(None)\n"
            "    return results\n\n"
            "The bare `except Exception` is too broad. Refactor to catch only the specific exceptions "
            "that can actually occur during division: ZeroDivisionError and TypeError.\n"
            "For any other exception, let it propagate.\n"
            "For ZeroDivisionError and TypeError, return None for that element and continue.\n"
            "Do NOT change the function's external behavior for ZeroDivisionError and TypeError cases."
        ),
        public_contract="safe_divide_all(values, divisor) -> list (identical for ZeroDivisionError/TypeError; raises for others)",
        constraints=[
            "Only catch ZeroDivisionError and TypeError.",
            "Let all other exceptions propagate.",
            "Do not change the return type or logic for handled exceptions.",
        ],
        expected_failure_modes=[
            "Still catching Exception broadly.",
            "Not letting unexpected exceptions propagate.",
            "Changing behavior for ZeroDivisionError.",
            "Changing behavior for TypeError.",
        ],
        scoring_focus=[
            "Specific exception handling only.",
            "Correct propagation of unexpected errors.",
            "Identical behavior for handled cases.",
        ],
        allowed_assumptions=["Values may be non-numeric types (causing TypeError).", "divisor may be zero."],
        disallowed_assumptions=["All exceptions should be caught.", "Only ZeroDivisionError can occur."],
    )

    add("api_design_consistency", 6,
        title="Avoid Broad Exception Swallowing",
        prompt=(
            "Given a function:\n\n"
            "def load_and_process(path: str) -> dict:\n"
            "    try:\n"
            "        with open(path) as f:\n"
            "            data = json.load(f)\n"
            "        return {'status': 'ok', 'data': data}\n"
            "    except Exception as e:\n"
            "        return {'status': 'error', 'message': str(e)}\n\n"
            "Audit and refactor: catch only the exceptions that are expected "
            "(FileNotFoundError, json.JSONDecodeError, PermissionError).\n"
            "For all other exceptions, re-raise them (do not catch).\n"
            "Preserve the function's external contract: for the expected exceptions, "
            "return the same error dict format. For unexpected exceptions, let them propagate."
        ),
        public_contract="load_and_process(path) -> dict (for expected errors); raises for unexpected errors",
        constraints=[
            "Only catch FileNotFoundError, json.JSONDecodeError, PermissionError.",
            "Return error dict format must be identical for caught exceptions.",
            "Unexpected exceptions must propagate (not be caught).",
        ],
        expected_failure_modes=[
            "Still catching Exception broadly.",
            "Not propagating unexpected exceptions.",
            "Changing the error dict format.",
        ],
        scoring_focus=[
            "Specific exception handling.",
            "Error propagation for unexpected exceptions.",
            "Preserved error dict format.",
        ],
        allowed_assumptions=["json module is imported.", "path is a valid filesystem path."],
        disallowed_assumptions=["All errors must be caught.", "Only FileNotFoundError can occur."],
    )

    # ---- performance_constraints ----

    add("performance_constraints", 1,
        title="Avoid O(n²) Duplicate Scanning",
        prompt=(
            "Implement `find_duplicates(records: list[dict], keys: list[str]) -> list[list[dict]]`.\n\n"
            "Find groups of records that are duplicates based on a subset of fields (the `keys` parameter).\n"
            "Two records are duplicates if all values for the specified keys are equal.\n"
            "Return a list of groups, where each group contains the records that are duplicates of each other.\n"
            "Records with unique key combinations are not returned.\n\n"
            "Constraint: Must use a hash map (dict), not nested loops.\n"
            "Complexity must be O(n) average, not O(n²).\n\n"
            "Handle: keys list empty (treat as no grouping, return []), "
            "records missing one of the key fields (use None as default), "
            "None values in key fields (treat as a valid comparison value)."
        ),
        public_contract="find_duplicates(records, keys) -> list[list[dict]] with O(n) average complexity",
        constraints=[
            "Must NOT use nested loops for comparison.",
            "Use a dict-based grouping approach.",
            "Do not modify input records.",
        ],
        expected_failure_modes=[
            "Using O(n²) nested loop approach.",
            "Not handling missing key fields.",
            "Not handling None values correctly.",
            "Returning singletons (records with no duplicates).",
        ],
        scoring_focus=[
            "O(n) average time complexity.",
            "Correct duplicate detection.",
            "Handling missing keys and None.",
            "Empty keys edge case.",
        ],
        allowed_assumptions=["Record values for key fields are hashable.", "keys contains valid field names."],
        disallowed_assumptions=["All records have all key fields.", "No None values.", "keys is never empty."],
    )

    add("performance_constraints", 2,
        title="Use Indexing/Map-Based Lookup for Join",
        prompt=(
            "Implement `join(left: list[dict], right: list[dict], left_key: str, right_key: str) -> list[dict]`.\n\n"
            "Perform an inner join on two lists of dicts.\n"
            "For each record in `left`, find all matching records in `right` where "
            "`record[left_key] == right_record[right_key]`.\n"
            "Return a list of merged dicts (all keys from left + all keys from right, prefixed with 'right_' "
            "to avoid collisions).\n\n"
            "Constraint: Must use a dict-based lookup index (not nested loops).\n"
            "Complexity must be O(n + m) average, not O(n × m).\n\n"
            "Handle: left or right being empty, records with missing join key (skip that record), "
            "multiple matches in right for a single left record (include all combinations)."
        ),
        public_contract="join(left, right, left_key, right_key) -> list[dict] with O(n+m) average complexity",
        constraints=[
            "Must use an index (dict) on the right list.",
            "Must NOT use nested loops.",
            "Output must preserve left record order.",
        ],
        expected_failure_modes=[
            "Using O(n×m) nested loop approach.",
            "Not handling missing join keys.",
            "Not preserving left order.",
            "Not including all right matches for a left record.",
        ],
        scoring_focus=[
            "O(n+m) time complexity.",
            "Correct join logic.",
            "Missing key handling.",
            "Order preservation.",
        ],
        allowed_assumptions=["Join key values are hashable.", "No self-referencing needed."],
        disallowed_assumptions=["Every record has both keys.", "Each left key matches at most one right key.",
                               "The right list is always small enough for nested loops."],
    )

    add("performance_constraints", 3,
        title="Avoid Repeated Serialization with Caching",
        prompt=(
            "Implement a class `CachingSerializer`:\n"
            "- `__init__(self)` — initializes an empty cache.\n"
            "- `serialize(self, obj: dict) -> str` — serialize a dict to JSON, caching by object identity "
            "(use a deterministic fingerprint of the dict contents, not reference identity).\n\n"
            "If the same dict content (deep equality) has been serialized before, return the cached string.\n"
            "Do not use json.dumps on the same content twice when it can be served from cache.\n\n"
            "Handle:\n"
            "- Dicts with keys in different orders — treat as equal (sort keys before fingerprinting).\n"
            "- Unhashable values inside dicts — fall back to json.dumps without caching.\n"
            "- Empty dict.\n"
            "- Nested dicts."
        ),
        public_contract="CachingSerializer.serialize(obj: dict) -> str with caching",
        constraints=[
            "Must avoid redundant serialization for identical content.",
            "Key ordering must not affect cache hits.",
            "Do not pre-serialize all objects; cache on first access.",
        ],
        expected_failure_modes=[
            "Cache miss for identical content with different key ordering.",
            "Raising on unhashable values instead of falling back.",
            "Using object identity instead of deep equality.",
            "Cache growing unbounded without limit.",
        ],
        scoring_focus=[
            "Correct cache hit detection (deep equality, key-order independent).",
            "Fallback for unhashable values.",
            "Cache used before serialization, not after.",
        ],
        allowed_assumptions=["Typical dict values are strings, numbers, lists, dicts.", "Cache may grow up to reasonable size."],
        disallowed_assumptions=["Dict keys are always in the same order.", "All values are hashable.",
                                "json.dumps is always fast enough without caching."],
    )

    add("performance_constraints", 4,
        title="Streaming-Friendly Aggregation",
        prompt=(
            "Implement a class `StreamingAggregator`:\n"
            "- `__init__(self)` — initializes counters to zero.\n"
            "- `add(self, value: float) -> None` — add a single value to the aggregate.\n"
            "- `current(self) -> dict` — return `{'count': int, 'sum': float, 'mean': float, "
            "'min': float | None, 'max': float | None}` based on all values seen so far.\n\n"
            "The aggregator must process values one at a time without storing the entire dataset.\n"
            "It should compute running statistics in O(1) memory per operation.\n\n"
            "Handle:\n"
            "- No values added yet: count=0, sum=0.0, mean=0.0, min=None, max=None.\n"
            "- Single value: min and max equal the value.\n"
            "- Negative values.\n"
            "- Adding None (skip it, do not count)."
        ),
        public_contract="StreamingAggregator.add(value) -> None; .current() -> dict (O(1) memory)",
        constraints=[
            "Do not store all values; only maintain running aggregates.",
            "Must handle empty state correctly.",
        ],
        expected_failure_modes=[
            "Storing all values instead of running aggregates.",
            "Incorrect running mean (not updating correctly).",
            "Returning 0.0 or None for min/max when empty (wrong).",
            "Counting None as a value.",
        ],
        scoring_focus=[
            "O(1) memory usage.",
            "Correct running statistics.",
            "Empty state handling.",
            "None value handling.",
        ],
        allowed_assumptions=["Values are floats or None.", "add is called sequentially."],
        disallowed_assumptions=["At least one value is added before current() is called.",
                                "All values are positive.", "Memory can store all values."],
    )

    add("performance_constraints", 5,
        title="Memory-Conscious Filtering with Index Awareness",
        prompt=(
            "Implement `filter_with_index(items: list, predicate: callable) -> list`.\n\n"
            "Filter items where `predicate(item, index)` returns True.\n"
            "The predicate receives both the item and its original index.\n\n"
            "Constraint: Use a generator expression or lazy evaluation approach.\n"
            "Do not create unnecessary intermediate lists.\n"
            "If the predicate only depends on the item (ignores index), "
            "the implementation should still be efficient.\n\n"
            "Handle: empty list, predicate that never matches, predicate that matches all, "
            "predicate that uses the index for conditional logic, "
            "predicate that raises an exception (let it propagate)."
        ),
        public_contract="filter_with_index(items, predicate) -> list (no unnecessary intermediate copies)",
        constraints=[
            "Do not create intermediate lists (e.g., list comprehension then filter).",
            "Use a single pass with generator where possible.",
            "Preserve original order.",
        ],
        expected_failure_modes=[
            "Creating unnecessary intermediate lists.",
            "Not passing the correct index to predicate.",
            "Using two passes where one suffices.",
            "Not preserving order.",
        ],
        scoring_focus=[
            "Single-pass filtering.",
            "Correct index passing to predicate.",
            "No unnecessary intermediate allocations.",
            "Order preservation.",
        ],
        allowed_assumptions=["predicate is a callable that returns bool.", "items is indexable."],
        disallowed_assumptions=["A list comprehension is always the best approach.",
                                "predicate never uses the index argument.",
                                "items is always small."],
    )

    add("performance_constraints", 6,
        title="Batch Normalization Without Unnecessary Loops",
        prompt=(
            "Implement `normalize_vectors(vectors: list[list[float]]) -> list[list[float]]`.\n\n"
            "Normalize each vector to unit length (L2 norm).\n\n"
            "Constraints:\n"
            "- Compute each vector's norm exactly once; do not recompute.\n"
            "- Do not create unnecessary intermediate lists.\n"
            "- Use a single pass per vector where possible.\n\n"
            "Handle:\n"
            "- Zero vectors (all zeros) — return the zero vector unchanged.\n"
            "- Empty vectors — return empty vector.\n"
            "- Empty list of vectors — return [].\n"
            "- Vectors with different lengths — normalize each independently.\n"
            "- Negative values in vectors."
        ),
        public_contract="normalize_vectors(vectors) -> list[list[float]] (each norm computed once)",
        constraints=[
            "Each vector's L2 norm must be computed exactly once.",
            "Do not copy vectors unnecessarily.",
            "Zero vectors must not cause division by zero.",
        ],
        expected_failure_modes=[
            "Computing the norm of the same vector multiple times.",
            "Division by zero for zero vectors.",
            "Creating unnecessary intermediate copies.",
            "Modifying input vectors.",
        ],
        scoring_focus=[
            "Each norm computed once.",
            "No unnecessary copies.",
            "Zero vector handling.",
            "Empty input handling.",
        ],
        allowed_assumptions=["Vectors are lists of floats.", "Input is not modified externally during processing."],
        disallowed_assumptions=["No zero vectors.", "All vectors have the same length.",
                                "Norm can be recomputed freely (no caching needed)."],
    )

    return tasks


# ---------------------------------------------------------------------------
# Write tasks
# ---------------------------------------------------------------------------

def _write_task(task: dict, task_dir: Path, global_seq: int) -> str:
    path = task_dir / f"task_{global_seq:03d}.json"
    blob = json.dumps(task, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(blob, encoding="utf-8")
    return blob


def main() -> None:
    task_dir = OUTPUT_DIR / "tasks"
    task_dir.mkdir(parents=True, exist_ok=True)

    tasks = _build_tasks()
    assert len(tasks) == 30, f"Expected 30 tasks, got {len(tasks)}"

    task_blobs: list[str] = []
    for i, task in enumerate(tasks, start=1):
        blob = _write_task(task, task_dir, i)
        task_blobs.append(blob)

    task_blobs_sorted = sorted(task_blobs)
    dataset_hash = _sha256("".join(task_blobs_sorted))

    manifest_entries: list[dict] = []
    for task in tasks:
        content = json.dumps(task, ensure_ascii=False, sort_keys=True)
        manifest_entries.append({
            "task_id": task["task_id"],
            "title": task["title"],
            "family": task["family"],
            "difficulty": task["difficulty"],
            "content_hash": _sha256(content),
        })

    manifest = {
        "dataset_name": "finitexo_code_matrix_hard_programming_n30",
        "dataset_version": "0.8.0",
        "task_count": len(tasks),
        "families": FAMILIES,
        "dataset_hash": dataset_hash,
        "tasks": manifest_entries,
    }
    manifest_blob = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    manifest_hash = _sha256(manifest_blob)

    (OUTPUT_DIR / "dataset_manifest.json").write_text(manifest_blob, encoding="utf-8")
    (OUTPUT_DIR / "dataset_hashes.json").write_text(
        json.dumps({"dataset_hash": dataset_hash, "manifest_hash": manifest_hash},
                   indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "dataset_hash.txt").write_text(dataset_hash + "\n", encoding="utf-8")
    (OUTPUT_DIR / "manifest_hash.txt").write_text(manifest_hash + "\n", encoding="utf-8")

    import datetime
    provenance = {
        "dataset": "finitexo_code_matrix_hard_programming_n30",
        "version": "0.8.0",
        "generation_script": "generate_hard_programming_n30.py",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "family_counts": {f: sum(1 for t in tasks if t["family"] == f) for f in FAMILIES},
        "total_tasks": len(tasks),
        "dataset_hash": dataset_hash,
        "manifest_hash": manifest_hash,
        "description": "Hard programming dataset n=30 for reduced ceiling effects. "
                       "Not a trap dataset. Not Xendris-favoring. Not a superiority benchmark.",
    }
    (OUTPUT_DIR / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {len(tasks)} tasks.")
    print(f"Dataset hash: {dataset_hash}")
    print(f"Manifest hash: {manifest_hash}")
    for family in FAMILIES:
        count = sum(1 for t in tasks if t["family"] == family)
        print(f"  {family}: {count}")


if __name__ == "__main__":
    main()
