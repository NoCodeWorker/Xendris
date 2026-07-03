"""Repository structure discovery for the v2.0 audit."""

from __future__ import annotations

import ast
from pathlib import Path

from phyng.repository_audit.schemas import RepositoryAuditResult


STATUS_TOKEN_PREFIXES = (
    "RISK_",
    "FRICTION_",
    "WTP_",
    "CHANNEL_",
    "UNIT_ECONOMICS_",
    "BUSINESS_",
    "CLAIM_",
    "ACTION_",
    "EXECUTION_",
    "DETECTABLE_",
    "UNDETECTABLE_",
    "FAIL_",
    "PASS_",
    "BLOCKED",
    "ALLOWED",
)

SKIPPED_TOP_LEVEL_DIRS = {
    ".venv",
    ".pytest_cache",
    "fastapi",
    "numpy",
    "pydantic",
    "pytest",
    "scipy",
    "phyng.egg-info",
    "frontend",
}


def py_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*.py")
        if "__pycache__" not in p.parts and _is_project_python_file(root, p)
    )


def _is_project_python_file(root: Path, path: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    if not rel.parts:
        return False
    return rel.parts[0] not in SKIPPED_TOP_LEVEL_DIRS


def module_name(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    return ".".join(rel.parts)


def parse_python(path: Path) -> ast.Module | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return None


def import_names(tree: ast.Module) -> list[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return sorted(names)


def defined_models_and_enums(tree: ast.Module) -> tuple[list[str], list[str]]:
    schemas: list[str] = []
    enums: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            base_names = {_name_of(base) for base in node.bases}
            if "BaseModel" in base_names:
                schemas.append(node.name)
            if "Enum" in base_names or "str, Enum" in base_names:
                enums.append(node.name)
        elif isinstance(node, ast.Assign):
            if _is_literal_assignment(node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        enums.append(target.id)
    return schemas, sorted(set(enums))


def status_literals(tree: ast.Module) -> list[str]:
    values: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            token = node.value.strip()
            if token.isupper() and any(token.startswith(prefix) for prefix in STATUS_TOKEN_PREFIXES):
                values.add(token)
    return sorted(values)


def audit_repository_structure(root: Path) -> RepositoryAuditResult:
    root = Path(root)
    files = py_files(root)
    packages = sorted(
        str(p.parent.relative_to(root)).replace("\\", "/")
        for p in files
        if p.name == "__init__.py" and p.parent != root
    )
    modules: list[str] = []
    schemas: set[str] = set()
    enums: set[str] = set()
    statuses: set[str] = set()
    imports: dict[str, list[str]] = {}

    for path in files:
        mod = module_name(root, path)
        modules.append(mod)
        tree = parse_python(path)
        if tree is None:
            continue
        imports[mod] = import_names(tree)
        file_schemas, file_enums = defined_models_and_enums(tree)
        schemas.update(f"{mod}.{name}" for name in file_schemas)
        enums.update(f"{mod}.{name}" for name in file_enums)
        statuses.update(status_literals(tree))

    tests = sorted(str(p.relative_to(root)).replace("\\", "/") for p in (root / "tests").glob("test_*.py"))
    reports = sorted(str(p.relative_to(root)).replace("\\", "/") for p in (root / "reports").rglob("*.md"))
    campaigns = sorted(m for m in modules if m.startswith("phyng.campaigns.") and not m.endswith("__init__"))

    warnings: list[str] = []
    if not campaigns:
        warnings.append("No campaign modules discovered under phyng/campaigns.")
    if not reports:
        warnings.append("No markdown reports discovered under reports/.")

    return RepositoryAuditResult(
        root=str(root),
        packages=packages,
        modules=sorted(modules),
        tests=tests,
        reports=reports,
        campaigns=campaigns,
        schemas=sorted(schemas),
        enums=sorted(enums),
        status_strings=sorted(statuses),
        imports=imports,
        warnings=warnings,
    )


def _name_of(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):
        return _name_of(node.value)
    if isinstance(node, ast.Tuple):
        return ", ".join(_name_of(elt) for elt in node.elts)
    return ""


def _is_literal_assignment(node: ast.Assign) -> bool:
    value = node.value
    if isinstance(value, ast.Subscript):
        return _name_of(value.value) == "Literal"
    return False
