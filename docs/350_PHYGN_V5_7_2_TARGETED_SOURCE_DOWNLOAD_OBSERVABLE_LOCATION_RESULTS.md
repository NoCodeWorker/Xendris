# Phygn v5.7.2 - Targeted Source Download & Observable Location Review Results

Date: 2026-07-02

Source prompt:

```txt
docs/349_PHYGN_CODEX_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_PROMPT.md
```

## Completion Status

Final campaign status: `TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND`
Verified source objects: `4`
SHA256 hashes generated: `4`
Download failures: `2`
Observable location candidates: `62`
Observed measurement candidates: `10`
Allowed next phase: `v5.7.3 - Targeted y_true Extraction`

No y_true was extracted. No PredictiveGain was computed. No benchmark was built. No Frontera C or physical claim was upgraded.

## Missing or Unverified Source Objects

- `GERLICH_2011_LARGE_ORGANIC.pdf`
- `ARNDT_1999_C60.pdf`

## Created Artifacts

- `data/frontera_c/source_download/source_download_manifest_v5_7_2.json`
- `data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json`
- `data/frontera_c/source_download/source_download_failures_v5_7_2.json`
- `data/frontera_c/observable_location/targeted_observable_location_candidates_v5_7_2.json`
- `data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json`
- `data/frontera_c/observable_location/targeted_rejected_location_records_v5_7_2.json`
- `data/frontera_c/observable_location/v5_7_2_next_gate_decision.json`
- `reports\frontera_c\source_download\source_download_manifest_v5_7_2.md`
- `reports\frontera_c\source_download\source_hash_registry_update_v5_7_2.md`
- `reports\frontera_c\source_download\source_download_failures_v5_7_2.md`
- `reports\frontera_c\observable_location\targeted_observable_location_candidates_v5_7_2.md`
- `reports\frontera_c\observable_location\targeted_observed_measurement_candidates_v5_7_2.md`
- `reports\frontera_c\observable_location\targeted_rejected_location_records_v5_7_2.md`
- `reports\frontera_c\observable_location\v5_7_2_next_gate_decision.md`
- `reports/campaigns/FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2.md`

## Next Gate

```txt
v5.7.3 - Targeted y_true Extraction
```

## Blocked Claims

- Frontera C is validated.
- LOG_BOUNDARY is reactivated.
- Downloaded sources are evidence.
- Observable location equals y_true.
- Source support equals PredictiveGain.
- Physical claim.
- Invariant confirmation.

## Allowed Claims

- Source objects were checked and hashed when verified.
- Missing or invalid source objects were reported.
- Observable location candidates were scanned from verified source objects.
- v5.7.3 is permitted only if observed measurement candidates exist.

Final discipline:

```txt
No source object, no observable review.
No observable location, no y_true.
```

---

## Canonical Status

- Domain Status: `TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND`
- Canonical Permission: `REVIEW_REQUIRED`
- Blocked Reasons: `MISSING_EXPERIMENTAL_DATA, MISSING_BENCHMARK`
- Evidence Level: `SOURCE_BACKED_LIMITED`
- Support Level: `NOT_YET_SUPPORTED`
- Risk Level: `SCIENTIFIC_RISK`

### Allowed Uses

- Proceed to strict y_true extraction review

### Blocked Uses

- PredictiveGain claim
- Frontera C validation
- physical claim

### Next Actions

- v5.7.3 - Targeted y_true Extraction

### Discipline Note

No source object, no observable review. No observable location, no y_true.
