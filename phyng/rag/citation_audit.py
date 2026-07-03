from pathlib import Path
from phyng.rag.schemas import ClaimRecord
from phyng.rag.source_registry import get_source


def audit_citations(claim: ClaimRecord, root_dir: Path) -> list[str]:
    missing_citations = []
    text_lower = claim.text.lower()
    
    # Define mapping of keywords to required citation markers
    citation_rules = {
        "minkowski": "Minkowski / Spacetime geometry",
        "special relativity": "Special relativity",
        "light cone": "Minkowski / Spacetime geometry",
        "spacetime": "Minkowski / Spacetime geometry",
        "compton": "Compton Reduced Wavelength",
        "schwarzschild": "Schwarzschild Horizon / Event Horizon",
        "horizon": "Schwarzschild Horizon / Event Horizon",
        "gravity": "Relativistic Gravity",
        "zurek": "Zurek / Quantum Decoherence",
        "decoherence": "Zurek / Quantum Decoherence",
        "quantum darwinism": "Zurek / Quantum Decoherence",
        "susskind": "Susskind / Horizon Complementarity",
        "complementarity": "Susskind / Horizon Complementarity",
        "pearl": "Pearl / Causal Inference",
        "causality": "Pearl / Causal Inference",
        "jensen-shannon": "Jensen-Shannon / Statistical Distinguishability",
        "js divergence": "Jensen-Shannon / Statistical Distinguishability",
        "kl divergence": "Kullback-Leibler Divergence"
    }
    
    # Collect all authors and notes from the actual linked sources
    linked_source_texts = []
    for src_id in claim.source_ids:
        src = get_source(src_id, root_dir)
        if src:
            linked_source_texts.extend([author.lower() for author in src.authors])
            if src.title:
                linked_source_texts.append(src.title.lower())
                
    for key, marker in citation_rules.items():
        if key in text_lower:
            # Check if any linked source contains the key in authors or title
            found = False
            for src_text in linked_source_texts:
                if key in src_text:
                    found = True
                    break
            if not found:
                missing_citations.append(marker)
                
    return missing_citations
