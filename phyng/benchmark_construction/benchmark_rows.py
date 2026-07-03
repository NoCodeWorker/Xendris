"""Build benchmark rows from survived extracts for v4.0."""

from __future__ import annotations

import re

from phyng.benchmark_construction.schemas import BenchmarkRow


def build_benchmark_rows(records: list[dict]) -> list[BenchmarkRow]:
    """Compile survived extract records into formal BenchmarkRows."""
    rows: list[BenchmarkRow] = []

    index = 1
    for r in records:
        slot = r.get("assigned_slot", "")
        pclass = r.get("pressure_class", "")

        # Skip SLOT_4 and un-survived classes
        if slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS" or pclass in (
            "ANALOGY_ONLY",
            "INCONCLUSIVE",
            "IRRELEVANT_AFTER_REVIEW",
        ):
            continue

        text = r.get("exact_text", "")
        text_lower = text.lower()

        # Parse regime ranges
        mass_range = _extract_range(text_lower, r"(?:mass|weight)(?:\s+range)?\s+(?:of\s+)?([\d\-\s\+]+(?:amu|kg|g|u|da))")
        time_range = _extract_range(text_lower, r"(?:time|duration|coherence|interaction)(?:\s+scale)?\s+(?:of\s+)?([\d\-\s\+]+(?:s|ms|us|ns|sec))")
        length_range = _extract_range(text_lower, r"(?:length|separation|width|distance|radius)(?:\s+scale)?\s+(?:of\s+)?([\d\-\s\+]+(?:m|cm|mm|um|nm|pm))")
        temp_press = _extract_range(text_lower, r"(?:temp|temperature|press|pressure)(?:\s+of)?\s+([\d\-\s\+e\.\<\>]+(?:k|mbar|bar|pa|torr|c))")

        # Determine observable type
        if slot == "SLOT_1_DECOHERENCE_BASELINE":
            obs_type = "BASELINE"
            benchmark_use = "Decoherence baseline loss comparison"
            allowed_comp = True
        elif slot == "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE":
            obs_type = "OBSERVABLE"
            benchmark_use = "Visibility contrast loss comparison"
            allowed_comp = True
        elif slot == "SLOT_3_BENCHMARK_RANGES":
            obs_type = "BENCHMARK_RANGE"
            benchmark_use = "Experimental regime limit comparison"
            allowed_comp = True
        elif slot == "SLOT_5_PARAMETER_CONSTRAINTS":
            obs_type = "PARAMETER_CONSTRAINT"
            benchmark_use = "CSL / model parameter bounds comparison"
            allowed_comp = True
        elif slot == "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS":
            obs_type = "NEGATIVE_LIMITATION"
            benchmark_use = "Background noise exclusions check"
            allowed_comp = False  # Limitations represent noise limits, not positive model comparison regimes
        else:
            obs_type = "EXPERIMENTAL_CONTEXT"
            benchmark_use = "Experimental context reference"
            allowed_comp = False

        limitations = list(r.get("limitations", []))
        limitations.append("Benchmark dataset cannot support gradient mechanism.")

        rows.append(
            BenchmarkRow(
                benchmark_id=f"BM-v4_0-{index:03d}",
                source_id=r.get("source_id", ""),
                extract_id=r.get("extract_id", ""),
                sha256=r.get("sha256", ""),
                page_number=r.get("page_number"),
                observable_type=obs_type,
                observable_text=text,
                regime_text=f"Regime for slot {slot}",
                mass_range=mass_range,
                time_range=time_range,
                length_or_separation_range=length_range,
                temperature_or_pressure=temp_press,
                parameter_constraints=[pclass] if pclass.startswith("SUPPORTS_PARAMETER_") else [],
                limitations=limitations,
                benchmark_use=benchmark_use,
                allowed_model_comparison=allowed_comp,
                gradient_claim_allowed=False,  # Enforce hard-coded false
            )
        )
        index += 1

    return rows


def _extract_range(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None
