from __future__ import annotations

import dataclasses
import json
import os
from typing import Any


@dataclasses.dataclass(frozen=True)
class RealWorldTask:
    task_id: str
    title: str
    repository_area: str
    instruction: str
    source_files: tuple[str, ...]
    expected_files_allowed: tuple[str, ...]
    forbidden_files: tuple[str, ...]
    validation_command: str
    success_criteria: str
    risk_level: str
    oracle_notes: str

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def load_real_world_tasks(task_suite: str = "real_world_v0_2") -> list[RealWorldTask]:
    if task_suite == "real_world_v0_2":
        return _build_v0_2_tasks()
    raise ValueError(f"Unknown task suite: {task_suite}")


def _build_v0_2_tasks() -> list[RealWorldTask]:
    return [
        RealWorldTask(
            task_id="RW-001",
            title="Add format_cost utility function",
            repository_area="benchmarking/report",
            instruction=(
                "Add a function `format_cost(cost: float | None) -> str` to the file "
                "xendris/benchmarking/agentic_programming/report.py. "
                "The function must return a formatted cost string:\n"
                "- If cost is None, return 'N/A'.\n"
                "- If cost is less than 0.01, return '<$0.01'.\n"
                "- Otherwise, return the cost formatted as '$X.XX' with two decimal places.\n"
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/report.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/report.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.report import format_cost; "
                "assert format_cost(None) == 'N/A'; "
                "assert format_cost(0.001) == '<$0.01'; "
                "assert format_cost(0.05) == '$0.05'; "
                "assert format_cost(1.5) == '$1.50'; "
                "assert format_cost(123.456) == '$123.46'; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="format_cost returns correct formatted strings for all cases",
            risk_level="low",
            oracle_notes=(
                "The function must handle None, sub-cent values, and normal values. "
                "Use python's format specifier for rounding."
            ),
        ),
        RealWorldTask(
            task_id="RW-002",
            title="Add is_readable_file helper",
            repository_area="benchmarking/runner",
            instruction=(
                "Add a function `is_readable_file(path: str) -> bool` to the file "
                "xendris/benchmarking/agentic_programming/runner.py. "
                "The function must return True if the path exists and is a regular file "
                "that can be opened for reading. Use os.path.isfile and a try/except block. "
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/runner.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/runner.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.runner import is_readable_file; "
                "assert is_readable_file(__file__) is True; "
                "assert is_readable_file('/nonexistent/path') is False; "
                "assert is_readable_file('.') is False; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="is_readable_file returns correct boolean for existing/nonexistent paths",
            risk_level="low",
            oracle_notes=(
                "Use os.path.isfile for existence check and try opening for reading."
            ),
        ),
        RealWorldTask(
            task_id="RW-003",
            title="Add format_pass_rate percentage helper",
            repository_area="benchmarking/report",
            instruction=(
                "Add a function `format_pass_rate(rate: float | None) -> str` to the file "
                "xendris/benchmarking/agentic_programming/report.py. "
                "The function must return a formatted percentage string:\n"
                "- If rate is None, return 'N/A'.\n"
                "- Otherwise, return the rate formatted as a percentage with one decimal, "
                "e.g. 0.8567 -> '85.7%'.\n"
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/report.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/report.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.report import format_pass_rate; "
                "assert format_pass_rate(None) == 'N/A'; "
                "assert format_pass_rate(0.0) == '0.0%'; "
                "assert format_pass_rate(1.0) == '100.0%'; "
                "assert format_pass_rate(0.8567) == '85.7%'; "
                "assert format_pass_rate(0.5) == '50.0%'; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="format_pass_rate returns correct percentage strings",
            risk_level="low",
            oracle_notes="Multiply by 100 and format to one decimal place followed by '%'.",
        ),
        RealWorldTask(
            task_id="RW-004",
            title="Add get_blocked_variant_names helper",
            repository_area="benchmarking/types",
            instruction=(
                "Add a function `get_blocked_variant_names(decisions: dict[str, str]) -> list[str]` "
                "to the file xendris/benchmarking/agentic_programming/types.py. "
                "The function must return a sorted list of variant names whose gate decision "
                "equals 'BLOCKED_FOR_INTERPRETATION'. "
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/types.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/types.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.types import get_blocked_variant_names; "
                "d1 = {'a': 'BLOCKED_FOR_INTERPRETATION', 'b': 'READY_FOR_INTERPRETATION', 'c': 'BLOCKED_FOR_INTERPRETATION'}; "
                "assert get_blocked_variant_names(d1) == ['a', 'c']; "
                "d2 = {}; assert get_blocked_variant_names(d2) == []; "
                "d3 = {'x': 'READY_FOR_INTERPRETATION'}; assert get_blocked_variant_names(d3) == []; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="get_blocked_variant_names returns sorted list of blocked variants",
            risk_level="low",
            oracle_notes="Filter dict items where value == 'BLOCKED_FOR_INTERPRETATION', return sorted keys.",
        ),
        RealWorldTask(
            task_id="RW-005",
            title="Add format_delta helper",
            repository_area="benchmarking/report",
            instruction=(
                "Add a function `format_delta(delta: float) -> str` to the file "
                "xendris/benchmarking/agentic_programming/report.py. "
                "The function must return a formatted delta string:\n"
                "- If delta == 0, return '—' (em dash).\n"
                "- If delta > 0, return '+X.XXXX' with 4 decimal places.\n"
                "- If delta < 0, return '-X.XXXX' with 4 decimal places.\n"
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/report.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/report.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.report import format_delta; "
                "assert format_delta(0.0) == '\u2014'; "
                "assert format_delta(0.4525) == '+0.4525'; "
                "assert format_delta(-0.0350) == '-0.0350'; "
                "assert format_delta(1.0) == '+1.0000'; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="format_delta returns correct delta strings with +/- prefix and em dash for zero",
            risk_level="low",
            oracle_notes="Use an em dash (U+2014) for zero. Format with sign and 4 decimal places otherwise.",
        ),
        RealWorldTask(
            task_id="RW-006",
            title="Add is_admitted_decision helper",
            repository_area="benchmarking/gate",
            instruction=(
                "Add a function `is_admitted_decision(decision: str) -> bool` to the file "
                "xendris/benchmarking/agentic_programming/excellence_gate.py. "
                "The function must return True if the decision is 'READY_FOR_INTERPRETATION' "
                "or 'WARNINGS_PRESENT'. Return False otherwise (including None). "
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/excellence_gate.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/excellence_gate.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.excellence_gate import is_admitted_decision; "
                "assert is_admitted_decision('READY_FOR_INTERPRETATION') is True; "
                "assert is_admitted_decision('WARNINGS_PRESENT') is True; "
                "assert is_admitted_decision('BLOCKED_FOR_INTERPRETATION') is False; "
                "assert is_admitted_decision(None) is False; "
                "assert is_admitted_decision('') is False; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="is_admitted_decision correctly identifies admitted vs blocked decisions",
            risk_level="low",
            oracle_notes="Check if decision is in {'READY_FOR_INTERPRETATION', 'WARNINGS_PRESENT'}.",
        ),
        RealWorldTask(
            task_id="RW-007",
            title="Add safe_filename helper",
            repository_area="benchmarking/export",
            instruction=(
                "Add a function `safe_filename(name: str) -> str` to the file "
                "xendris/benchmarking/agentic_programming/export_jsonl.py. "
                "The function must convert a variant name to a safe filename:\n"
                "- Replace underscores with hyphens.\n"
                "- Remove any characters that are not alphanumeric, hyphens, or dots.\n"
                "- Lowercase the result.\n"
                "- Return 'unnamed' if the result is empty.\n"
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/export_jsonl.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/export_jsonl.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.export_jsonl import safe_filename; "
                "assert safe_filename('deepseek_base_agent') == 'deepseek-base-agent'; "
                "assert safe_filename('Hello World!') == 'hello-world'; "
                "assert safe_filename('test.py') == 'test.py'; "
                "assert safe_filename('!!!') == 'unnamed'; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="safe_filename converts variant names to safe, lowercase filenames",
            risk_level="low",
            oracle_notes="Use re.sub to remove non-allowed chars, str.lower(), and handle empty result.",
        ),
        RealWorldTask(
            task_id="RW-008",
            title="Add get_warning_variant_names helper",
            repository_area="benchmarking/types",
            instruction=(
                "Add a function `get_warning_variant_names(decisions: dict[str, str]) -> list[str]` "
                "to the file xendris/benchmarking/agentic_programming/types.py. "
                "The function must return a sorted list of variant names whose gate decision "
                "equals 'WARNINGS_PRESENT'. "
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/types.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/types.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.types import get_warning_variant_names; "
                "d1 = {'a': 'WARNINGS_PRESENT', 'b': 'READY_FOR_INTERPRETATION', 'c': 'WARNINGS_PRESENT'}; "
                "assert get_warning_variant_names(d1) == ['a', 'c']; "
                "d2 = {}; assert get_warning_variant_names(d2) == []; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="get_warning_variant_names returns sorted list of warning variants",
            risk_level="low",
            oracle_notes="Filter dict items where value == 'WARNINGS_PRESENT', return sorted keys.",
        ),
        RealWorldTask(
            task_id="RW-009",
            title="Add calculate_total_cost helper",
            repository_area="benchmarking/scorer",
            instruction=(
                "Add a function `calculate_total_cost(results: list) -> float` to the file "
                "xendris/benchmarking/agentic_programming/scorer.py. "
                "The function must return the sum of all cost_estimate values from a list of "
                "objects that have a cost_estimate attribute (float or None). "
                "Skip None values. Return 0.0 if the list is empty or all costs are None. "
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/scorer.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/scorer.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.scorer import calculate_total_cost; "
                "class R: cost_estimate = None; "
                "assert calculate_total_cost([]) == 0.0; "
                "assert calculate_total_cost([type('R',(),{'cost_estimate':0.5})(), type('R',(),{'cost_estimate':1.5})()]) == 2.0; "
                "assert calculate_total_cost([type('R',(),{'cost_estimate':None})(), type('R',(),{'cost_estimate':0.5})()]) == 0.5; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="calculate_total_cost sums cost_estimate values, skipping None",
            risk_level="low",
            oracle_notes="Use sum(r.cost_estimate for r in results if r.cost_estimate is not None).",
        ),
        RealWorldTask(
            task_id="RW-010",
            title="Add get_provider_from_variant helper",
            repository_area="benchmarking/types",
            instruction=(
                "Add a function `get_provider_from_variant(variant_name: str) -> str` to the file "
                "xendris/benchmarking/agentic_programming/types.py. "
                "The function must extract the provider from a variant name:\n"
                "- If the name starts with 'deepseek_', return 'deepseek'.\n"
                "- If the name starts with 'openai_', return 'openai'.\n"
                "- Otherwise, return 'unknown'.\n"
                "Do not modify any other file."
            ),
            source_files=("xendris/benchmarking/agentic_programming/types.py",),
            expected_files_allowed=("xendris/benchmarking/agentic_programming/types.py",),
            forbidden_files=("tests/", "frontend/", "scripts/"),
            validation_command=(
                "python -c \""
                "import sys; sys.path.insert(0, '.'); "
                "from xendris.benchmarking.agentic_programming.types import get_provider_from_variant; "
                "assert get_provider_from_variant('deepseek_base_agent') == 'deepseek'; "
                "assert get_provider_from_variant('openai_xendris_agent') == 'openai'; "
                "assert get_provider_from_variant('base_agent') == 'unknown'; "
                "assert get_provider_from_variant('oracle_agent') == 'unknown'; "
                "print('OK'); "
                "sys.exit(0)"
                "\""
            ),
            success_criteria="get_provider_from_variant extracts provider prefix from variant name",
            risk_level="low",
            oracle_notes="Use str.startswith() checks for 'deepseek_' and 'openai_' prefixes.",
        ),
    ]
