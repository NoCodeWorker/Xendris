"""
Phygn v1.3 — Extract Target Generator

Generates extract targets and guidelines for the selected real source candidates.
"""

from __future__ import annotations

from pathlib import Path

EXTRACT_TARGETS_CONTENT = """# Phygn v1.3 — Real Extract Targets

## 0. Purpose

This document defines what to extract from selected candidate sources.
Do not copy long text. Do not invent quotes. Use short excerpts or careful paraphrase with local references.

## 1. Target claims

### CLAIM-BASELINE-FORMULA-001
- **Statement**: A visibility/coherence decay baseline can be represented phenomenologically by an exponential or monotonic decay form under explicit assumptions.
- **Support needed**: FORMULA_SUPPORT
- **What to look for**: Equations representing V(t) = exp(-Gamma t) or similar decay forms.
- **What not to infer**: Do not infer that this decay is fundamental or universal.
- **Forbidden overclaims**: "proves quantum gravity decoherence", "validates Frontera C".

### CLAIM-BASELINE-OBSERVABLE-001
- **Statement**: Visibility/interference contrast is a valid observable in interferometric decoherence contexts.
- **Support needed**: OBSERVABLE_SUPPORT
- **What to look for**: Text linking fringe visibility or contrast to quantum coherence.
- **What not to infer**: Do not infer that any loss of contrast is due to gravitational decoherence.
- **Forbidden overclaims**: "proves the theory", "shows physical prediction".

### CLAIM-BASELINE-CONTEXT-001
- **Statement**: Matter-wave or mesoscopic interferometry is an appropriate context for studying decoherence and visibility loss.
- **Support needed**: CONTEXT_SUPPORT, OBSERVABLE_SUPPORT
- **What to look for**: Matter-wave experimental setups, nanoparticle interferometers, MAQRO.
- **What not to infer**: Do not infer that MAQRO or nanoparticle interferometry validates the boundary-aware candidate.
- **Forbidden overclaims**: "the boundary-aware candidate is validated".

### CLAIM-BASELINE-LIMITATION-001
- **Statement**: The exponential baseline is limited/phenomenological and not a universal physical model.
- **Support needed**: ASSUMPTION_SUPPORT, CONTEXT_SUPPORT, CONTRADICTION
- **What to look for**: Discussions of non-exponential decay, short-time behaviors, or environmental exceptions.
- **What not to infer**: Do not infer that the baseline is completely useless.
- **Forbidden overclaims**: "Frontera C is validated by these limitations".

## 2. Extract targets by source

### SRC-BASE-DECOH-001 (Schlosshauer)
- **Target**: CLAIM-BASELINE-FORMULA-001, CLAIM-BASELINE-LIMITATION-001
- **Look for**: environment-induced decoherence, loss of coherence, limitations.
- **Forbidden**: Do not use as Frontera C support.

### SRC-BASE-MWI-001 (Kaltenbaek MAQRO)
- **Target**: CLAIM-BASELINE-CONTEXT-001
- **Look for**: MAQRO visibility, gas scattering, blackbody radiation.
- **Forbidden**: Do not claim MAQRO validates Frontera C.

### SRC-BASE-VIS-001 (Schut)
- **Target**: CLAIM-BASELINE-OBSERVABLE-001
- **Look for**: decoherence and dephasing leading to loss of contrast.
- **Forbidden**: Do not infer physical prediction.

### SRC-BASE-VIS-002 (Talbot-Lau)
- **Target**: CLAIM-BASELINE-FORMULA-001, CLAIM-BASELINE-OBSERVABLE-001
- **Look for**: exponential decrease of fringe visibility, background gas pressure.
- **Forbidden**: "SyntheticGain is PredictiveGain".

## 3. Required limitation per extract
Every extract must say one of:
- *This does not validate Frontera C.*
- *This does not validate the boundary-aware candidate.*
- *This does not imply physical prediction.*
- *This supports only the baseline.*

## 4. Final principle
Extracts must strengthen the adversary before they strengthen the theory.
"""

def generate_extract_targets(project_root: Path) -> Path:
    """
    Writes the extract targets Markdown file to sources/baseline/notes/extract_targets_v1_3.md
    and copies it to reports/rag/extract_targets_v1_3.md.
    """
    notes_dir = project_root / "sources" / "baseline" / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    
    notes_path = notes_dir / "extract_targets_v1_3.md"
    notes_path.write_text(EXTRACT_TARGETS_CONTENT, encoding="utf-8")
    
    # Write report copy
    report_dir = project_root / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "extract_targets_v1_3.md"
    report_path.write_text(
        "# Extract Targets Report — v1.3\n\n" + EXTRACT_TARGETS_CONTENT,
        encoding="utf-8"
    )
    
    return notes_path
