"""
Tests for phyng.evidence.extract_validation
"""

from pathlib import Path

import pytest

from phyng.evidence.extract_validation import (
    validate_extract_file,
    validate_extract_folder,
    write_extract_support_tags_report,
)

# ── Helpers ────────────────────────────────────────────────────────────────

_VALID_EXTRACT = """\
# Extracts — SRC-BASE-DECOH-001

## Source Metadata

- Title: Some Decoherence Paper
- Authors: Author A
- Year: 2024
- Trust level: HIGH

## Extract 1

Support type: FORMULA_SUPPORT
Claim target: CLAIM-BASELINE-FORMULA-001
Local reference: page 12, eq. 3
Text:

> Coherence decays exponentially as V(t) = exp(-Gamma t).

Audit notes:

- Why this supports the claim: Explicit exponential form for coherence decay.
- What this does not support: Does not validate Frontera C or the candidate model.
"""

_MISSING_SUPPORT_EXTRACT = """\
# Extracts — SRC-BASE-TEST-001

## Source Metadata

- Title: Some Paper

## Extract 1

Claim target: CLAIM-BASELINE-FORMULA-001
Local reference: page 5
Text:

> Some text without a support type tag.

Audit notes:

- Why: background only.
"""

_FORBIDDEN_PHRASE_EXTRACT = """\
# Extracts — SRC-BASE-FORBIDDEN-001

## Source Metadata

- Title: Bad Paper

## Extract 1

Support type: FORMULA_SUPPORT
Claim target: CLAIM-BASELINE-FORMULA-001
Local reference: page 1
Text:

> Frontera C is validated by this source.

Audit notes:

- Why: should be rejected.
"""

_OBSERVABLE_EXTRACT = """\
# Extracts — SRC-BASE-OBS-001

## Source Metadata

- Title: Interferometry Paper
- Trust level: HIGH

## Extract 1

Support type: OBSERVABLE_SUPPORT
Claim target: CLAIM-BASELINE-OBSERVABLE-001
Local reference: section 3.2
Text:

> Visibility is measured as interference contrast.

Audit notes:

- Why this supports the claim: Explicit visibility observable.
- What this does not support: Does not predict decoherence.
"""

_MISSING_CLAIM_TARGET = """\
# Extracts — SRC-BASE-NCT-001

## Source Metadata

## Extract 1

Support type: FORMULA_SUPPORT
Local reference: page 1
Text: > something

Audit notes:
- note
"""

_MISSING_AUDIT_NOTES = """\
# Extracts — SRC-BASE-NAN-001

## Source Metadata

## Extract 1

Support type: FORMULA_SUPPORT
Claim target: CLAIM-BASELINE-FORMULA-001
Local reference: page 2
Text: > something
"""


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


# ── Tests ──────────────────────────────────────────────────────────────────

class TestValidateExtractFile:
    def test_valid_formula_support(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "src_decoh_001_extracts.md", _VALID_EXTRACT)
        result = validate_extract_file(p)
        assert result.valid is True
        assert "FORMULA_SUPPORT" in result.support_types_found

    def test_valid_observable_support(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "src_obs_001_extracts.md", _OBSERVABLE_EXTRACT)
        result = validate_extract_file(p)
        assert result.valid is True
        assert "OBSERVABLE_SUPPORT" in result.support_types_found

    def test_missing_support_type_invalid(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "no_support.md", _MISSING_SUPPORT_EXTRACT)
        result = validate_extract_file(p)
        assert result.valid is False
        assert not result.support_types_found

    def test_forbidden_overclaim_invalid(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "forbidden.md", _FORBIDDEN_PHRASE_EXTRACT)
        result = validate_extract_file(p)
        assert result.valid is False
        assert len(result.forbidden_phrases_found) >= 1

    def test_missing_claim_target_invalid(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "no_claim.md", _MISSING_CLAIM_TARGET)
        result = validate_extract_file(p)
        assert result.valid is False
        assert result.has_claim_target is False

    def test_missing_audit_notes_invalid(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "no_audit.md", _MISSING_AUDIT_NOTES)
        result = validate_extract_file(p)
        assert result.valid is False
        assert result.has_audit_notes is False

    def test_missing_file_invalid(self, tmp_path: Path) -> None:
        p = tmp_path / "nonexistent.md"
        result = validate_extract_file(p)
        assert result.valid is False

    def test_invalid_support_tag_detected(self, tmp_path: Path) -> None:
        bad_content = _VALID_EXTRACT.replace("FORMULA_SUPPORT", "FAKE_SUPPORT_TYPE")
        p = _write(tmp_path, "bad_tag.md", bad_content)
        result = validate_extract_file(p)
        assert result.valid is False
        assert "FAKE_SUPPORT_TYPE" in result.invalid_support_types

    def test_forbidden_predicts_decoherence(self, tmp_path: Path) -> None:
        content = _VALID_EXTRACT + "\nPhygn predicts decoherence in this extract.\n"
        p = _write(tmp_path, "pred.md", content)
        result = validate_extract_file(p)
        assert result.valid is False

    def test_missing_source_header_invalid(self, tmp_path: Path) -> None:
        content = _VALID_EXTRACT.replace("# Extracts — SRC-BASE-DECOH-001", "# Some Other Header")
        p = _write(tmp_path, "no_header.md", content)
        result = validate_extract_file(p)
        assert result.has_source_header is False
        assert result.valid is False


class TestValidateExtractFolder:
    def test_empty_folder_returns_empty(self, tmp_path: Path) -> None:
        folder = tmp_path / "extracts"
        folder.mkdir()
        results = validate_extract_folder(folder)
        assert results == []

    def test_missing_folder_returns_empty(self, tmp_path: Path) -> None:
        results = validate_extract_folder(tmp_path / "nonexistent")
        assert results == []

    def test_multiple_files(self, tmp_path: Path) -> None:
        folder = tmp_path / "extracts"
        folder.mkdir()
        _write(folder, "a.md", _VALID_EXTRACT)
        _write(folder, "b.md", _MISSING_SUPPORT_EXTRACT)
        results = validate_extract_folder(folder)
        assert len(results) == 2
        assert sum(1 for r in results if r.valid) == 1

    def test_report_generated(self, tmp_path: Path) -> None:
        folder = tmp_path / "extracts"
        folder.mkdir()
        _write(folder, "a.md", _VALID_EXTRACT)
        results = validate_extract_folder(folder)
        rp = write_extract_support_tags_report(results, tmp_path)
        assert rp.exists()
        content = rp.read_text(encoding="utf-8")
        assert "FORMULA_SUPPORT" in content
