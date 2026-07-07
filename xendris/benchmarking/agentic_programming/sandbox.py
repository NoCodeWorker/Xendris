from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_test_in_sandbox(fixture_dir: str, test_command: str) -> tuple[bool, str]:
    repo_path = Path(fixture_dir) / "repo"
    if not repo_path.is_dir():
        return False, f"Repository path does not exist: {repo_path}"

    if test_command.startswith("python ") or test_command.startswith("python3 "):
        python_exe = sys.executable.replace("\\", "/")
        prefix = test_command.split()[0]
        test_command = test_command.replace(prefix, python_exe, 1)

    try:
        result = subprocess.run(
            test_command,
            shell=True,
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=60,
        )
        passed = result.returncode == 0
        output = result.stdout + result.stderr
        return passed, output
    except subprocess.TimeoutExpired:
        return False, "Test execution timed out (60s)"
    except FileNotFoundError as exc:
        return False, f"Test command not found: {exc}"
    except Exception as exc:
        return False, f"Sandbox execution error: {exc}"


def run_visible_tests(fixture_dir: str, test_command: str) -> tuple[bool, str]:
    return run_test_in_sandbox(fixture_dir, test_command)


def run_hidden_tests(fixture_dir: str, test_command: str) -> tuple[bool, str]:
    return run_test_in_sandbox(fixture_dir, test_command)
