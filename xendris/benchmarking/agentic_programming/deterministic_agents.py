from __future__ import annotations

import os
import shutil


EXPECTED_DIR = "expected"
SRC_DIR = "src"


def _get_expected_dir(fixture_dir: str) -> str:
    return os.path.join(fixture_dir, EXPECTED_DIR)


def _apply_expected_to_working_dir(fixture_dir: str, working_dir: str) -> list[str]:
    expected_base = _get_expected_dir(fixture_dir)
    if not os.path.isdir(expected_base):
        return []

    applied: list[str] = []
    for root, _dirs, files in os.walk(expected_base):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            src_path = os.path.join(root, fname)
            rel_path = os.path.relpath(src_path, expected_base)
            dst_path = os.path.join(working_dir, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            applied.append(rel_path)
    return applied


def oracle_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    working_dir: str | None = None,
    fixture_dir: str | None = None,
) -> tuple[str, str | None]:
    if working_dir is None or fixture_dir is None:
        return "", "oracle_agent requires working_dir and fixture_dir"

    applied = _apply_expected_to_working_dir(fixture_dir, working_dir)
    if not applied:
        return "", f"oracle_agent: no expected files found in {_get_expected_dir(fixture_dir)}"

    return f"oracle_agent: applied {applied}", None


def partial_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    working_dir: str | None = None,
    fixture_dir: str | None = None,
) -> tuple[str, str | None]:
    if working_dir is None or fixture_dir is None:
        return "", "partial_agent requires working_dir and fixture_dir"

    if fixture_dir is None:
        return "", "partial_agent requires fixture_dir"

    task_id = os.path.basename(fixture_dir)

    fixed_tasks = {
        "task_001", "task_002", "task_005", "task_006",
        "task_011", "task_012", "task_015", "task_016",
        "task_003", "task_009",
    }

    if task_id in fixed_tasks:
        applied = _apply_expected_to_working_dir(fixture_dir, working_dir)
        return f"partial_agent: fixed ({applied})", None

    return "partial_agent: skipped (not in fixed set)", None


def bad_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    working_dir: str | None = None,
    fixture_dir: str | None = None,
) -> tuple[str, str | None]:
    if working_dir is None or fixture_dir is None:
        return "", "bad_agent requires working_dir and fixture_dir"

    violations: list[str] = []

    forbidden_dir = os.path.join(working_dir, "tests")
    forbidden_file = os.path.join(forbidden_dir, "test_deleted.py")
    os.makedirs(forbidden_dir, exist_ok=True)
    with open(forbidden_file, "w") as f:
        f.write("# intentionally deleted by bad_agent\n")
    violations.append("touched forbidden file (tests/test_deleted.py)")

    solver_path = os.path.join(working_dir, "src", "solver.py")
    if os.path.isfile(solver_path):
        with open(solver_path, "r") as f:
            content = f.read()
        broken_content = content.replace(
            "def count_items", "def count_items_broken"
        ).replace(
            "def in_range", "def in_range_broken"
        ).replace(
            "def solve", "def solve_broken"
        )
        with open(solver_path, "w") as f:
            f.write(broken_content)
        violations.append("changed API signatures")

    ap = os.path.join(working_dir, "src", "processor.py")
    if os.path.isfile(ap):
        with open(ap, "r") as f:
            content = f.read()
        with open(ap, "w") as f:
            f.write(content + "\n\nimport os  # unauthorized dependency\n")
        violations.append("added unauthorized dependency (import os)")

    for root, _dirs, files in os.walk(working_dir):
        for fname in files:
            if fname.startswith("test_") and fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                with open(fpath, "r") as f:
                    content = f.read()
                if "assert" in content:
                    content = content.replace("assert ", "# assert ")
                    with open(fpath, "w") as f:
                        f.write(content)
                    violations.append(f"disabled assertions in {fname}")

    patch_content = f"bad_agent: {', '.join(violations)}" if violations else "bad_agent: no violations applied"

    false_success_file = os.path.join(working_dir, "_false_success_claim.txt")
    with open(false_success_file, "w") as f:
        f.write("bad_agent claims: all tests pass (false)")
    violations.append("made false success claim")

    return patch_content, None
