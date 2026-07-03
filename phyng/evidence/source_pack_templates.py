"""
Phygn v1.2 — Source Pack Templates

Defines templates for the manifest, extracts, notes, and READMEs.
"""

from __future__ import annotations

import json
from phyng.evidence.canonical_source_slots import CANONICAL_SLOTS

MANIFEST_TEMPLATE = [
    {
        "source_candidate_id": slot.source_candidate_id,
        "requirement_id": slot.requirement_id,
        "title": None,
        "authors": [],
        "year": None,
        "source_type": "LOCAL_FILE",
        "local_path": f"sources/baseline/papers/{slot.source_candidate_id}.pdf",
        "url": None,
        "trust_level": "HIGH",
        "intended_support_types": slot.intended_support_types,
        "notes": f"Template slot for {slot.source_candidate_id}. Replace with real metadata after selection. Do not invent fields."
    }
    for slot in CANONICAL_SLOTS.values()
]

def get_extract_template(source_id: str) -> str:
    slot = CANONICAL_SLOTS[source_id]
    
    # Generate support type sections
    sections = []
    for idx, st in enumerate(slot.intended_support_types):
        sections.append(f"""## Extract {idx + 1}

Support type: {st}  
Claim target: CLAIM-BASELINE-{st.split('_')[0]}-001  
Local reference: page/section/paragraph if known  
Text:

> [TEMPLATE_NOT_EVIDENCE] Replace this placeholder text with a short excerpt or careful paraphrase from the real source.

Audit notes:

- Why this supports the claim: [TEMPLATE_NOT_EVIDENCE]
- What this does not support: [TEMPLATE_NOT_EVIDENCE]
- Limitations: {slot.required_limitation}""")

    sections_str = "\n\n".join(sections)

    return f"""# Extracts — {source_id}

[TEMPLATE_NOT_EVIDENCE] This is a template extract file and does not constitute real evidence.

## Source Metadata

- Title:
- Authors:
- Year:
- Source file: {MANIFEST_TEMPLATE[0]["local_path"] if source_id == MANIFEST_TEMPLATE[0]["source_candidate_id"] else f"sources/baseline/papers/{source_id}.pdf"}
- URL:
- Trust level: HIGH

{sections_str}
"""

PAPERS_README = """# Baseline Source Papers Directory

Place the actual PDF/text files of the canonical sources here.
The files should match the names specified in `source_manifest.json`:
- `SRC-BASE-DECOH-001.pdf`
- `SRC-BASE-VIS-001.pdf`
- `SRC-BASE-MWI-001.pdf`
- `SRC-BASE-THRESH-001.pdf`
- `SRC-BASE-PARAM-001.pdf`
"""

REJECTED_README = """# Rejected Sources Directory

Place any literature sources that were audited and rejected here.
Document the reason for rejection in `source_selection_notes.md`.
"""

SELECTION_NOTES = """# Baseline Source Selection Notes

Document the rationale for choosing specific papers for each slot here.
Also record any rejected papers and why they failed the trust or relevance criteria.

## Slots
- **SRC-BASE-DECOH-001**: [Pending selection]
- **SRC-BASE-VIS-001**: [Pending selection]
- **SRC-BASE-MWI-001**: [Pending selection]
- **SRC-BASE-THRESH-001**: [Pending selection]
- **SRC-BASE-PARAM-001**: [Pending selection]
"""
