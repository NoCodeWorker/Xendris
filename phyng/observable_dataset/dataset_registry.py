"""Build dataset source registry for v4.2."""

from __future__ import annotations

from phyng.observable_dataset.schemas import DatasetSourceRegistryRecord, NormalizedObservableTarget


def build_dataset_source_registry(
    targets: list[NormalizedObservableTarget],
) -> list[DatasetSourceRegistryRecord]:
    """Compile dataset source records for unique sources in targets."""
    registry: list[DatasetSourceRegistryRecord] = []
    unique_sources = {}

    for t in targets:
        sid = t.source_id
        if sid not in unique_sources:
            unique_sources[sid] = []
        unique_sources[sid].append(t)

    index = 1
    for sid, ts in unique_sources.items():
        classes = {t.observable_class for t in ts}

        # Classify source type and access status based on expected observables
        if "VISIBILITY" in classes or "DECOHERENCE_RATE" in classes:
            stype = "ARTICLE_TABLE"
            astatus = "KNOWN_LOCAL_PDF"
            method = "MANUAL_TABLE_EXTRACTION"
            manual = True
        elif "MASS_REGIME" in classes or "TIME_REGIME" in classes:
            stype = "PUBLIC_REPOSITORY"
            astatus = "NEEDS_PUBLIC_LOOKUP"
            method = "PUBLIC_DATASET_LOOKUP"
            manual = False
        else:
            stype = "SUPPLEMENTARY_MATERIAL"
            astatus = "NEEDS_SUPPLEMENTARY_FILE"
            method = "SUPPLEMENTARY_DATA_EXTRACTION"
            manual = True

        registry.append(
            DatasetSourceRegistryRecord(
                dataset_source_id=f"DSRC-v4_2-{index:03d}",
                related_source_id=sid,
                source_type=stype,
                access_status=astatus,
                expected_observables=sorted(list(classes)),
                acquisition_method=method,
                requires_manual_review=manual,
                notes=[
                    f"Identified from {len(ts)} normalized targets.",
                    "Review required to extract raw numbers.",
                ],
            )
        )
        index += 1

    return registry

