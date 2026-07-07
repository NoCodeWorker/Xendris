from __future__ import annotations

import difflib
import os


def apply_patch(repo_dir: str, patch_content: str) -> bool:
    import json

    try:
        parsed = json.loads(patch_content)
        if isinstance(parsed, dict):
            for rel_path, content in parsed.items():
                full_path = os.path.join(repo_dir, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
            return True
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    patch_path = os.path.join(repo_dir, "_agent_patch.py")
    try:
        with open(patch_path, "w", encoding="utf-8") as f:
            f.write(patch_content)
        return True
    except OSError:
        return False


def read_patch(patch_path: str) -> str:
    if not os.path.isfile(patch_path):
        return ""
    with open(patch_path, encoding="utf-8") as f:
        return f.read()


def compute_patch_size(patch_content: str) -> int:
    return len(patch_content.strip().splitlines())


def generate_diff(original_dir: str, patched_dir: str) -> str:
    diff_lines: list[str] = []
    for root, _dirs, files in os.walk(original_dir):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            orig_path = os.path.join(root, fname)
            rel_path = os.path.relpath(orig_path, original_dir)
            patched_path = os.path.join(patched_dir, rel_path)

            if not os.path.isfile(patched_path):
                continue

            with open(orig_path, encoding="utf-8") as f:
                orig_lines = f.readlines()
            with open(patched_path, encoding="utf-8") as f:
                patched_lines = f.readlines()

            diff = difflib.unified_diff(
                orig_lines, patched_lines,
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
            )
            diff_lines.extend(diff)

    return "".join(diff_lines)
