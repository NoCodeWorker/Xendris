# Codex Prompt — Phygn v0.5 Dashboard Reflection

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current v0.5 core objective:

```txt
Invariant Boundary Atlas
CAMPAIGN-001 Mesoscopic Boundary Number
Non-Triviality Protocol
RAG Source Plan
Claim Exclusion Matrix
```

Your task is to update the dashboard so the v0.5 core work is visible in the cockpit.

This is not a styling task.  
This is a scientific state representation task.

---

# 1. Read first

Read:

```txt
docs/28_PHYGN_V0_5_DASHBOARD_ATLAS_CAMPAIGNS_SPEC.md
docs/29_PHYGN_DASHBOARD_V0_5_DATA_CONTRACTS.md
```

Also read:

```txt
docs/22_PHYGN_V0_5_GOAL_INVARIANT_BOUNDARY_ATLAS.md
docs/23_PHYGN_CAMPAIGN_001_MESOSCOPIC_BOUNDARY_NUMBER.md
docs/24_PHYGN_BOUNDARY_EXCLUSION_ATLAS_ARCHITECTURE.md
docs/25_PHYGN_NON_TRIVIALITY_AND_FALSIFIABILITY_PROTOCOL.md
docs/26_PHYGN_CAMPAIGN_RAG_SOURCE_PLAN_v0_5.md
```

---

# 2. First action

Inspect frontend:

```bash
cd frontend
dir
dir app
dir components
dir lib
```

Do not recreate frontend if it already exists.

---

# 3. Mission

Add dashboard visibility for:

```txt
Boundary Atlas
Atlas Points
Claim Exclusions
Campaigns
CAMPAIGN-001 Mesoscopic Boundary Number
Non-Triviality
RAG Coverage
RAG Sources
RAG Claims
```

---

# 4. Add routes

Create/adapt:

```txt
app/atlas/page.tsx
app/atlas/points/page.tsx
app/atlas/exclusions/page.tsx
app/campaigns/page.tsx
app/campaigns/mesoscopic-boundary-number/page.tsx
app/non-triviality/page.tsx
app/rag/page.tsx
app/rag/sources/page.tsx
app/rag/claims/page.tsx
```

---

# 5. Update sidebar

Add:

```txt
Boundary Atlas
Campaigns
Non-Triviality
RAG / Sources
```

If sidebar already has RAG or Docs, integrate cleanly.

Use existing dashboard-01 layout.

---

# 6. Add components

Create:

```txt
components/phygn/AtlasStatusCard.tsx
components/phygn/AtlasPointTable.tsx
components/phygn/AtlasRegionBadge.tsx
components/phygn/ClaimExclusionMatrix.tsx
components/phygn/CampaignCard.tsx
components/phygn/CampaignResultPanel.tsx
components/phygn/NonTrivialityBadge.tsx
components/phygn/NonTrivialityPanel.tsx
components/phygn/RagCoverageCard.tsx
components/phygn/RagSourceTable.tsx
components/phygn/ResearchTaskTable.tsx
components/phygn/ReportLinkCard.tsx
components/phygn/CoreTruthBanner.tsx
```

Reuse existing card/badge/table components where possible.

---

# 7. Add data contracts

Create or extend:

```txt
lib/atlas.ts
lib/campaigns.ts
lib/non-triviality.ts
lib/rag.ts
```

Use the contracts from:

```txt
docs/29_PHYGN_DASHBOARD_V0_5_DATA_CONTRACTS.md
```

---

# 8. API client

Extend `lib/api.ts` with:

```ts
getAtlas()
getAtlasPoints()
getAtlasExclusions()
getCampaigns()
getMesoscopicBoundaryCampaign()
getNonTrivialityStatus()
getRagCoverage()
getRagSources()
getRagClaims()
getRagResearchTasks()
```

If backend endpoints do not exist, implement honest fallback.

Do not fake successful backend state.

---

# 9. Honest fallback rule

If no endpoint:

```txt
Awaiting backend endpoint
```

If no report:

```txt
Awaiting generated report
```

If mock:

```txt
Development placeholder
```

Never present mock data as real campaign output.

---

# 10. Dashboard page update

In `/dashboard`, add section:

```txt
v0.5 Research Campaign Layer
```

Cards:

```txt
Invariant Boundary Atlas
CAMPAIGN-001
Claim Exclusion Matrix
Non-Triviality Status
RAG Source Coverage
```

Each card should link to its page.

---

# 11. /atlas

Show:

```txt
title
QB formula
atlas status
region counts
QB validation summary
blocked claims count
RAG coverage
report links
```

Mandatory copy:

```txt
The atlas does not prove new physics. It classifies allowed, limited and blocked claims under explicit assumptions.
```

---

# 12. /atlas/points

Show table columns:

```txt
system_id
label
m_kg
L_value_m
L_type
Q
B
QB
logQ
logB
u
w
region
trace_type
claim_status
scale_status
```

Add filters if simple.

---

# 13. /atlas/exclusions

Show:

```txt
claim_id
claim_text
decision
reason
safe_rewrite
region
source_status
test_status
benchmark_status
```

Must include or be ready to include the blocked claim:

```txt
Phygn predicts new gravitational decoherence.
```

---

# 14. /campaigns

Show CampaignCard for:

```txt
CAMPAIGN-001 — Mesoscopic Boundary Number
```

---

# 15. /campaigns/mesoscopic-boundary-number

Show:

```txt
Scientific Question
Input System
Operational Scale Review
Boundary Signature
Invariant Check
Region Classification
Non-Triviality Status
Allowed Claims
Blocked Claims
RAG Status
Benchmark Status
Tests
Next Tasks
```

Must clearly show:

```txt
blocked claim:
Phygn predicts new gravitational decoherence.
```

---

# 16. /non-triviality

Show definitions:

```txt
TRIVIAL_STRUCTURAL
STRUCTURAL_USEFUL
NEGATIVE_NONTRIVIAL
PREDICTIVE_NONTRIVIAL
EMPIRICALLY_ACTIONABLE
```

Show:

```txt
current CAMPAIGN-001 status
why
what would upgrade it
what would defeat it
what is missing
```

Mandatory copy:

```txt
Lo no trivial no es lo que suena profundo. Lo no trivial es lo que cambia una decisión.
```

---

# 17. /rag

Show RagCoverageCard:

```txt
sources
claims
links
research tasks
requires source
requires higher trust
contradicted
blocked
```

---

# 18. /rag/sources

Show RagSourceTable.

---

# 19. /rag/claims

Show claim table.

---

# 20. Prohibited language

Do not write:

```txt
Phygn proves new physics.
The atlas validates Frontera C.
CAMPAIGN-001 predicts decoherence.
The invariant is a discovered law.
```

Allowed language:

```txt
Phygn computes a negative bound.
The atlas classifies claim status under explicit assumptions.
CAMPAIGN-001 blocks the decoherence overclaim unless model comparison exists.
```

---

# 21. Acceptance criteria

Complete when:

```txt
npm run dev works
sidebar includes Boundary Atlas, Campaigns, Non-Triviality, RAG/Sources
/atlas loads
/atlas/points loads
/atlas/exclusions loads
/campaigns loads
/campaigns/mesoscopic-boundary-number loads
/non-triviality loads
/rag loads
/rag/sources loads
/rag/claims loads
dashboard exposes v0.5 cards
blocked decoherence claim visible
no new-physics proof language appears
fallback states are honest
```

---

# 22. Final rule

The dashboard must show what the core knows, what it blocks, and what it still cannot claim.

Build that.
