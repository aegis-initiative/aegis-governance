# IEEE DataPort Deposit Instructions — ATX-1 v2.3

This document collects the metadata for depositing ATX-1 v2.3 on IEEE DataPort as a new version of the existing v1.0 record. IEEE DataPort is the journal's preferred archive for IEEE Data Descriptions submissions.

## Existing record (v1.0)

- **DOI:** [10.21227/f87b-1d57](https://doi.org/10.21227/f87b-1d57)
- **URL:** https://ieee-dataport.org/documents/atx-1-aegis-threat-matrix-agentic-ai-systems
- **Status:** Frozen; reflects the v1.0 baseline reviewed in the original DATA-00033-2026 submission.

## What to deposit

**File to upload:** [`aegis-governance/docs/atx/v2/atx-1-v2.3.zip`](./atx-1-v2.3.zip) — 396 KB, 14 files. Contains the complete v2.3 dataset:

- `atx-meta.json` — release metadata
- `data/` — six JSON files (techniques, regulatory crossref, navigator layer, ATM-1 mapping, version mapping, aegis-core validation)
- `schema/atx-technique.schema.json` — JSON Schema Draft 2020-12
- `stix/atx-1-bundle.json` — STIX 2.1 Bundle (204 objects, 151 KB)
- `figures/atx-1-threat-matrix-v2.3.pdf` — vector figure (PDF)
- `figures/atx-1-threat-matrix-v2.3.svg` — vector figure (SVG)
- `ATX-1_TECHNIQUE_TAXONOMY.md` — canonical taxonomy documentation
- `README.md` — dataset README
- `CHANGELOG-v2.3.md` — v2.3 release notes (severity removal rationale)

## Upload path: "New version" of existing v1.0 record

1. Log in to [ieee-dataport.org](https://ieee-dataport.org) with the account that owns the v1.0 record (DOI 10.21227/f87b-1d57).
2. Navigate to the existing v1.0 record.
3. Look for a **"New version"** button (similar to Zenodo's flow). This creates a new versioned deposit linked to the existing record's DOI series.
4. If the New-version flow is unavailable, contact IEEE DataPort support — the v1.0 record needs to be linked via versioning, not deposited as a standalone (the latter would orphan it from the existing series, same lesson as the Zenodo orphan-DOI experience).

## Metadata (web form fields)

### Title
```
ATX-1: AEGIS Threat Matrix for Agentic AI Systems, Version 2.3
```

### Authors
```
Kenneth Tannenbaum (AEGIS Initiative, AEGIS Operations LLC, ORCID 0009-0007-4215-1789)
```

### Abstract / Description

```
ATX-1 (AEGIS Threat Matrix) is a structured adversarial knowledge base
cataloguing failure modes of autonomous AI agents operating without
governance constraints. Unlike MITRE ATT&CK (which targets human
adversaries) or MITRE ATLAS (which targets adversaries against AI
systems), ATX-1 addresses a distinct threat class: AI agents that act
outside their governance boundaries through structural capability
without authority, not through external compromise. Composite scenarios
in which external triggers (e.g., indirect prompt injection) flow into
the agent's action surface are explicitly in scope.

Version 2.3 removes the `severity` field from technique definitions in
alignment with MITRE ATT&CK and ATLAS conventions, which leave
contextual scoring to the consumer. Tactic, technique, sub-technique,
root cause, and mitigation structure carries over unchanged from v2.2.

Contents:
- 10 tactics (TA001 through TA010), 29 techniques, 29 sub-techniques, 5
  structural root causes (RC1-RC5), and 29 architectural mitigations
- STIX 2.1 Bundle (204 objects: 1 identity, 10 x-mitre-tactic, 58
  attack-pattern, 29 course-of-action, 106 relationship)
- Technique database (JSON Array) with parent-sub-technique structure
- Regulatory cross-reference matrix mapping each technique to NIST AI
  RMF functions, EU AI Act articles, OWASP Top 10 for LLM Applications,
  OWASP Top 10 for Agentic Applications (December 2025), and ATM-1
  threat scenarios
- JSON Schema (Draft 2020-12) for technique validation
- ATT&CK Navigator layer (v4.5)
- ATM-1 attack-vector mapping
- Vector figure (PDF + SVG)

The empirical foundation derives from the Agents of Chaos study
(Shapira et al., 2026, arXiv:2602.20021), the AEGIS Round 1 controlled
multi-agent evaluation (DOI 10.5281/zenodo.20159697), and corroborating
research published in 2025-2026 by Anthropic, Apollo Research, Microsoft
AI Red Team, Cemri et al. (NeurIPS 2025), and others. ATX-1 directly
informs the AEGIS governance architecture (AGP-1) and maps each
technique to specific constitutional articles and governance protocol
mechanisms that mitigate it.

A descriptor article submitted to IEEE Data Descriptions (Manuscript ID
DATA-00033-2026, under revision as of 2026-05) describes the dataset
construction process and validation in detail.
```

### Keywords (categories/tags)
- Agentic AI
- AI governance
- AI threat taxonomy
- STIX 2.1
- MITRE ATT&CK
- MITRE ATLAS
- Autonomous agents
- NIST AI RMF
- EU AI Act
- OWASP LLM Top 10
- OWASP Agentic Top 10
- AEGIS
- ATX-1

### Categories (IEEE DataPort taxonomy)
- Artificial Intelligence
- Cybersecurity
- (and any additional applicable IEEE DataPort top-level categories)

### Subject
Threat taxonomy for autonomous AI agents acting on operational infrastructure.

### License
**Apache License 2.0** (matches the in-bundle declaration and all prior ATX-1 deposits).

### Related publications (cross-references)

- **AEGIS architectural paper:** [10.5281/zenodo.19223924](https://doi.org/10.5281/zenodo.19223924) (cites)
- **ATX-1 v2.3 on Zenodo:** [10.5281/zenodo.20171712](https://doi.org/10.5281/zenodo.20171712) (alternate-identifier / mirror)
- **AEGIS Round 1 Edge Evaluation:** [10.5281/zenodo.20159697](https://doi.org/10.5281/zenodo.20159697) (cites)
- **Agents of Chaos study (foundational):** [arXiv:2602.20021](https://arxiv.org/abs/2602.20021) (isDerivedFrom)
- **Prior version v1.0 (this record's parent):** [10.21227/f87b-1d57](https://doi.org/10.21227/f87b-1d57) (isNewVersionOf)

### Version note / changelog

ATX-1 v2.3 (released 2026-04-24) removes the `severity` field from technique definitions in alignment with MITRE ATT&CK and ATLAS conventions. Tactic, technique, sub-technique, root cause, and mitigation structure carries over unchanged from v2.2. Full changelog: see `CHANGELOG-v2.3.md` in the deposited ZIP, or the source repository at [github.com/aegis-initiative/aegis-governance](https://github.com/aegis-initiative/aegis-governance/blob/main/changelog/2026-04-24-atx1-v2.3.md).

## After the DOI mints

Once IEEE DataPort assigns the v2.3 DataPort DOI (formatted as `10.21227/XXXX-XXXX`), update the following files in the repository:

1. **`docs/atx/v2/data/atx-1-version-mapping.json`** — change `"v2.3_ieee_dataport": "pending"` to the minted DOI.
2. **`docs/atx/v2/atx-meta.json`** — add `"dataport_atx1_v2.3": "..."` (or equivalent field) to the citation block.
3. **Descriptor manuscript ([`docs/position-papers/ieee-data-descriptions/submission/atx1-descriptor-v05.tex`](../position-papers/ieee-data-descriptions/submission/atx1-descriptor-v05.tex))** — update the DATA DOI/PID field in the abstract to use the IEEE DataPort DOI as the canonical citation (since IEEE Data Descriptions journal preferentially cites IEEE DataPort), with the Zenodo DOI listed as a mirror.
4. **`docs/position-papers/ieee-data-descriptions/submission/response-to-reviewers.md`** — update the Editorial Note's reference to the v2.3 DOI to include the IEEE DataPort minting.
5. **Re-run `npm run sync-atx`** to propagate updated metadata to `site/public/atx-1/`.

The propagation pattern follows the same approach used for the Zenodo deposit (commits `3eb5a3b`, `82012d6`, `a3bfa67`, `ed94ae5`, and `c9f77ed` in the ecosystem repos).
