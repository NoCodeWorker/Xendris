"""Distribute unextracted targets into actionable extraction queues."""

from __future__ import annotations

from phyng.ytrue_extraction.schemas import QueueItem


def build_queues(
    targets: list[dict],
    candidates: list[dict],
) -> tuple[list[QueueItem], list[QueueItem], list[QueueItem], list[QueueItem]]:
    """Build manual table, figure digitization, public lookup, and supplementary lookup queues."""
    table_q: list[QueueItem] = []
    fig_q: list[QueueItem] = []
    pub_q: list[QueueItem] = []
    supp_q: list[QueueItem] = []

    # Map target_id to candidate
    cand_map = {c["target_id"]: c for c in candidates}

    for t in targets:
        tid = t["target_id"]
        sid = t["source_id"]
        c = t["observable_class"]
        text = t["source_observable_text"].lower()

        cand = cand_map.get(tid, {})
        # Only queue if the candidate could not enter the dataset directly
        if cand.get("can_enter_dataset", False):
            continue

        priority = "MEDIUM"
        if c in ("VISIBILITY", "CONTRAST_DECAY"):
            priority = "CRITICAL"
        elif c in ("DECOHERENCE_RATE", "COHERENCE_LOSS"):
            priority = "HIGH"

        blockers = cand.get("blockers", [])
        blocking_reason = blockers[0] if blockers else "Requires manual data extraction."

        # Route to queue based on class and text keywords
        item = QueueItem(
            target_id=tid,
            source_id=sid,
            observable_class=c,
            expected_measurement=t.get("measurement_context", "Retrieve measured values."),
            source_location_hint=f"Page {t.get('page_number', 'unknown') or 'unknown'} of local PDF or supplementary.",
            required_action="Verify exact numbers from source tables.",
            priority=priority,
            blocking_reason=blocking_reason,
        )

        if c in ("VISIBILITY", "DECOHERENCE_RATE", "COHERENCE_LOSS") and "table" in text:
            item.required_action = "Extract raw numbers from table."
            table_q.append(item)
        elif "fig" in text or "figure" in text:
            item.required_action = "Digitize data points from figure."
            fig_q.append(item)
        elif c in ("MASS_REGIME", "TIME_REGIME", "SEPARATION_REGIME", "TEMPERATURE_PRESSURE_REGIME"):
            item.required_action = "Search public data repository."
            pub_q.append(item)
        elif "supplementary" in text or c == "CONTRAST_DECAY":
            item.required_action = "Locate supplementary files and extract parameters."
            supp_q.append(item)
        else:
            # Default to table queue for manual review
            item.required_action = "Perform manual PDF review."
            table_q.append(item)

    return table_q, fig_q, pub_q, supp_q
