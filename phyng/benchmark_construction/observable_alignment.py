"""Build observable alignment records for v4.0."""

from __future__ import annotations

from phyng.benchmark_construction.schemas import ObservableAlignmentRecord


def align_observables(records: list[dict]) -> list[ObservableAlignmentRecord]:
    """Build observable alignment records from survived extracts."""
    alignments: list[ObservableAlignmentRecord] = []

    # Map of slot to observable name
    slot_map = {
        "SLOT_1_DECOHERENCE_BASELINE": "Decoherence rate / baseline loss",
        "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE": "Interference visibility / contrast",
        "SLOT_3_BENCHMARK_RANGES": "Benchmark regime parameters (mass/time/temp)",
        "SLOT_5_PARAMETER_CONSTRAINTS": "CSL collapse parameter / bounds",
        "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS": "Environmental background / noise constraints",
        "SLOT_7_EXPERIMENTAL_CONTEXT": "Experimental setup details",
    }

    index = 1
    for r in records:
        # Check if it survived v3.9 (not SLOT_4 and not ANALOGY_ONLY/INCONCLUSIVE/IRRELEVANT)
        pclass = r.get("pressure_class", "")
        slot = r.get("assigned_slot", "")

        if slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS" or pclass in (
            "ANALOGY_ONLY",
            "INCONCLUSIVE",
            "IRRELEVANT_AFTER_REVIEW",
        ):
            continue

        observable = slot_map.get(slot, "Generic physical observable")

        # Determine alignment status
        if pclass in ("SUPPORTS_OBSERVABLE_ONLY", "SUPPORTS_BASELINE_ONLY"):
            status = "OBSERVABLE_ALIGNED_FOR_BENCHMARK"
        elif pclass in ("SUPPORTS_BENCHMARK_ALIGNMENT", "SUPPORTS_PARAMETER_CONSTRAINT", "LIMITS_COMPONENT"):
            status = "OBSERVABLE_ALIGNED_LIMITED"
        else:
            status = "OBSERVABLE_REQUIRES_MANUAL_REVIEW"

        limits = list(r.get("limitations", []))
        if status == "OBSERVABLE_ALIGNED_LIMITED":
            limits.append("Alignment is regime-limited; no gradient mechanism verification.")

        alignments.append(
            ObservableAlignmentRecord(
                alignment_id=f"ALIGN-v4_0-{index:03d}",
                source_id=r.get("source_id", ""),
                extract_id=r.get("extract_id", ""),
                observable=observable,
                source_observable_text=r.get("exact_text", ""),
                phygn_observable_mapping="Matter-wave coherence loss model",
                baseline_model_mapping="Standard environmental decoherence (thermal/scattering)",
                candidate_model_mapping="PHI_GRADIENT transition dynamics (zeroed out/mechanism blocked)",
                alignment_status=status,
                limitations=limits,
            )
        )
        index += 1

    return alignments
