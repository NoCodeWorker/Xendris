# API Deprecation Policy

**Version:** 1.0  
**Effective:** v0.3.0+  

---

## Classification lifecycle

```
EMPTY → PUBLIC_EXPERIMENTAL → PUBLIC_STABLE → DEPRECATED → REMOVED
```

### PUBLIC_STABLE
- Breaking changes only in major version bumps (v1.0.0, v2.0.0)
- Minor versions add symbols only; never remove or break
- Patch versions fix bugs without API changes

### PUBLIC_EXPERIMENTAL
- May change without notice within the same minor version
- Must be explicitly marked in module docstring and `__init__.py`
- Consumers should pin to exact minor version
- Deprecation warning required one minor version before promotion or removal

### DEPRECATED
- Warning on import: `DeprecationWarning("use X instead")`
- Remains importable for exactly 2 minor versions after deprecation
- Removed in the next major version or after 2 minors, whichever comes first

### REMOVED
- Import raises `ImportError` with migration hint
- Documented in release notes

---

## Current deprecations

| Module | Status | Deprecated in | Removal in | Migration |
|--------|--------|---------------|------------|-----------|
| `xendris.prompts` | EMPTY | v0.3.0 | v0.5.0 | Import prompts from specific modules |
| `xendris.outputs` | EMPTY | v0.3.0 | v0.5.0 | Use `pathlib.Path` directly |
| `xendris.scripts` | EMPTY | v0.3.0 | v0.5.0 | Use `python -m scripts.<name>` |

## How to deprecate

1. Add `warnings.warn("Module X is deprecated. Use Y instead.", DeprecationWarning, stacklevel=2)` to the module's `__init__.py`
2. Add entry to this table
3. Announce in release notes
4. Remove after the defined removal window
