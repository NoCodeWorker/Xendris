"""Module boundary and dependency audits."""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

from phyng.repository_audit.schemas import DependencyRecord, ModuleAuditRecord
from phyng.repository_audit.structure import (
    defined_models_and_enums,
    import_names,
    module_name,
    parse_python,
    py_files,
)


def audit_module_boundaries(root: Path) -> list[ModuleAuditRecord]:
    root = Path(root)
    py_paths = [p for p in py_files(root) if p.relative_to(root).parts[0] == "phyng"]
    module_imports: dict[str, list[str]] = {}
    module_defs: dict[str, tuple[list[str], list[str]]] = {}
    report_writes: dict[str, list[str]] = {}

    for path in py_paths:
        mod = module_name(root, path)
        tree = parse_python(path)
        if tree is None:
            continue
        module_imports[mod] = import_names(tree)
        module_defs[mod] = defined_models_and_enums(tree)
        report_writes[mod] = _report_targets(tree)

    imported_by = _reverse_imports(module_imports)
    test_texts = _test_texts(root)
    records: list[ModuleAuditRecord] = []
    schema_name_index: dict[str, list[str]] = defaultdict(list)
    for mod, (schemas, _enums) in module_defs.items():
        for schema in schemas:
            schema_name_index[schema.lower()].append(mod)

    for path in py_paths:
        mod = module_name(root, path)
        schemas, enums = module_defs.get(mod, ([], []))
        warnings = _boundary_warnings(mod, module_imports.get(mod, []))
        duplicates = [
            f"{schema} also appears in {', '.join(sorted(set(schema_name_index[schema.lower()]) - {mod}))}"
            for schema in schemas
            if len(set(schema_name_index[schema.lower()])) > 1
        ]
        records.append(
            ModuleAuditRecord(
                module=mod,
                path=str(path.relative_to(root)).replace("\\", "/"),
                responsibility_guess=_responsibility_guess(mod),
                imports=module_imports.get(mod, []),
                imported_by=imported_by.get(mod, []),
                defined_schemas=schemas,
                defined_enums=enums,
                reports_written=report_writes.get(mod, []),
                tests_covering_module=_tests_covering(mod, test_texts),
                possible_duplicates=duplicates,
                boundary_warnings=warnings,
            )
        )
    return sorted(records, key=lambda r: r.module)


def audit_dependencies(root: Path) -> list[DependencyRecord]:
    records = audit_module_boundaries(root)
    imports = {r.module: r.imports for r in records}
    imported_by = {r.module: r.imported_by for r in records}
    graph = {
        mod: sorted(i for i in deps if i.startswith("phyng.") and i in imports)
        for mod, deps in imports.items()
    }
    cycles = _find_simple_cycles(graph)
    output: list[DependencyRecord] = []
    for record in records:
        cycle_warnings = [
            " -> ".join(cycle)
            for cycle in cycles
            if record.module in cycle
        ]
        coupling_warnings: list[str] = []
        if len([i for i in record.imports if i.startswith("phyng.")]) > 8:
            coupling_warnings.append("High outbound phyng import count; review coupling.")
        if len(record.imported_by) > 8:
            coupling_warnings.append("High inbound import count; candidate shared boundary.")
        output.append(
            DependencyRecord(
                module=record.module,
                imports=record.imports,
                imported_by=imported_by.get(record.module, []),
                cycle_warnings=cycle_warnings,
                coupling_warnings=coupling_warnings,
                boundary_warnings=record.boundary_warnings,
            )
        )
    return output


def _reverse_imports(module_imports: dict[str, list[str]]) -> dict[str, list[str]]:
    reverse: dict[str, set[str]] = defaultdict(set)
    for mod, imports in module_imports.items():
        for imported in imports:
            for candidate in module_imports:
                if imported == candidate or candidate.startswith(imported + "."):
                    reverse[candidate].add(mod)
    return {key: sorted(value) for key, value in reverse.items()}


def _report_targets(tree: ast.Module) -> list[str]:
    targets: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if value.endswith(".md") or value.startswith("reports/"):
                targets.add(value)
    return sorted(targets)


def _responsibility_guess(mod: str) -> str:
    parts = mod.split(".")
    if len(parts) >= 2 and parts[1] == "campaigns":
        return "campaign orchestration"
    if len(parts) >= 2:
        return f"{parts[1]} domain logic"
    return "core package module"


def _boundary_warnings(mod: str, imports: list[str]) -> list[str]:
    warnings: list[str] = []
    if mod.startswith("phyng.core.") and any(i.startswith("phyng.") and not i.startswith("phyng.core") for i in imports):
        warnings.append("Core module imports domain module.")
    if mod.startswith("phyng.business_validation.") and any(i.startswith("phyng.candidates.") for i in imports):
        warnings.append("Business validation imports candidate physics domain.")
    return warnings


def _test_texts(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)).replace("\\", "/"): p.read_text(encoding="utf-8", errors="ignore")
        for p in (root / "tests").glob("test_*.py")
    }


def _tests_covering(mod: str, test_texts: dict[str, str]) -> list[str]:
    tail = mod.split(".", 1)[1] if mod.startswith("phyng.") else mod
    path_hint = tail.replace(".", "/")
    return sorted(
        rel
        for rel, text in test_texts.items()
        if mod in text or path_hint in rel or tail.split(".")[0] in rel
    )


def _find_simple_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    seen_keys: set[tuple[str, ...]] = set()
    for source, targets in graph.items():
        for target in targets:
            if source in graph.get(target, []):
                key = tuple(sorted([source, target]))
                if key not in seen_keys:
                    seen_keys.add(key)
                    cycles.append([source, target, source])
            for third in graph.get(target, []):
                if third != source and source in graph.get(third, []):
                    key = tuple(sorted([source, target, third]))
                    if key not in seen_keys:
                        seen_keys.add(key)
                        cycles.append([source, target, third, source])
    return cycles[:50]
