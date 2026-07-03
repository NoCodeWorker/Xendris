# Phygn v5.7.1 — Search Strategy & Seed Queries

## 0. Purpose

This document defines search strategy and seed queries for targeted visibility/decoherence literature acquisition.

---

## 1. Search targets

The goal is to find independent experimental sources with extractable observed values.

Target expressions:

```txt
visibility
fringe visibility
contrast
decoherence rate
decoherence time
interference visibility
molecular interference visibility
matter-wave visibility
thermal emission decoherence
collisional decoherence
gas collision decoherence
Talbot-Lau visibility
KDTLI visibility
```

---

## 2. High-priority search queries

Use these as query seeds:

```txt
"matter wave interferometry visibility decoherence figure"
"molecular interferometry visibility thermal decoherence"
"Talbot Lau interferometer visibility decoherence measurement"
"KDTLI molecular interference visibility data"
"collisional decoherence matter wave interferometry visibility gas pressure"
"thermal emission decoherence visibility molecule interferometer"
"interference fringe visibility decoherence rate atom interferometer"
"visibility loss decoherence matter wave experiment"
"macroscopicity test visibility matter wave interferometry"
"decoherence by thermal emission of radiation visibility figure"
```

---

## 3. Candidate known-source clues

Investigate sources related to:

```txt
Hackermueller thermal emission decoherence
Hornberger collisional decoherence
Arndt molecular quantum interference
Zeilinger molecular interferometry
Nimmrichter macroscopicity matter-wave tests
Eibenberger molecular interference KDTLI
Gerlich quantum interference large molecules
Brand matter-wave decoherence
Haslinger macromolecule quantum interference
```

---

## 4. Search output rule

Every search hit must be classified:

```txt
RESOLVED_COMPLETE
RESOLVED_PARTIAL
RAW_REF_ONLY
UNRESOLVED
REJECTED_NOT_RELEVANT
```

No raw title alone may enter the next phase.

---

## 5. Human lookup fallback

If automated lookup cannot resolve at least 3 sources, produce:

```txt
HUMAN_LOOKUP_REQUIRED
```

and include exact search queries and missing fields.

---

## 6. DOI/arXiv preference

Prefer:

```txt
DOI
arXiv
publisher URL
PubMed/INSPIRE/ADS entry
local PDF hash
```

Reject unsupported references without stable identity.

---

## 7. Final principle

```txt
Find papers for their measurable observables, not for their narrative relevance.
```
