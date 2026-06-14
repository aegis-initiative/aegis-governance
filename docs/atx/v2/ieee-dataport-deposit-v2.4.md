# IEEE DataPort Deposit Instructions — ATX-1 v2.4

This document collects the metadata for depositing **ATX-1 v2.4** on IEEE DataPort.
IEEE DataPort is the manual **dataset** track for ATX-1 (Zenodo is handled
automatically by the monthly aegis-governance repo-snapshot auto-mint and is **not**
a manual step — v2.4 is already captured in the Jun 1 2026 snapshot, Zenodo concept
DOI `10.5281/zenodo.19162184`).

> **Submit as a NEW dataset — not a "New version."** IEEE DataPort has no
> concept-DOI versioning (unlike Zenodo). Each ATX-1 version is its own dataset
> record with its own DOI, cross-referenced to the prior version via metadata. Use
> **Submit a Dataset** on ieee-dataport.org and link v2.3 as the previous version.

## Prior version (cross-reference, do not modify)

- **ATX-1 v2.3:** DOI [10.21227/jr43-0571](https://doi.org/10.21227/jr43-0571) —
  remains the IEEE Data Descriptions journal-cited canonical (Manuscript
  DATA-00033-2026). v2.4 is a sibling record; it does **not** supersede or alter v2.3.
- **Series root (v1.0):** [10.21227/f87b-1d57](https://doi.org/10.21227/f87b-1d57)

## What to deposit

**File to upload:** [`docs/atx/v2/atx-1-v2.4.zip`](./atx-1-v2.4.zip) — ~170 KB, 15
files. Contains the complete v2.4 dataset:

- `atx-meta.json` — release metadata
- `data/` — six JSON files (techniques, regulatory crossref, navigator layer, ATM-1 mapping, version mapping, aegis-core validation)
- `schema/atx-technique.schema.json` — JSON Schema Draft 2020-12
- `stix/atx-1-bundle.json` — STIX 2.1 Bundle (228 objects)
- `acf/acf-1-bundle.json` — AEGIS Counterfactual Framework bundle
- `figures/atx-1-threat-matrix-v2.4.pdf` + `.svg` — vector figure (use the PDF as the dataset thumbnail/preview)
- `ATX-1_TECHNIQUE_TAXONOMY.md` — canonical taxonomy documentation
- `README.md` — dataset README
- `CHANGELOG-v2.4.md` — v2.4 release notes (T6003 / LoopTrap)

## Metadata (web form fields)

### Title

```
ATX-1: AEGIS Threat Matrix for Agentic AI Systems, Version 2.4
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

Version 2.4 adds one new technique, T6003 Poison Termination Judgment,
under tactic TA006 (Abuse Resource Allocation), together with ten
sub-techniques (T6003.001-T6003.010), one per strategy defined by Xu et
al. in "LoopTrap: Termination Poisoning Attacks on LLM Agents"
(arXiv:2605.05846, May 2026). Termination Poisoning is an
agent-vs-environment attack on the progress-evaluation / termination
step of the agentic control loop: an adversary embeds manipulative
content in untrusted retrieved context that distorts the agent's
stopping decision, causing it to treat an already-complete task as
incomplete and continue executing without bound. It is distinct from
indirect prompt injection (which corrupts action selection) and from
model-level resource-exhaustion ("sponge") attacks (which are
ATLAS-adjacent). Inclusion and the proposed mapping were endorsed by the
LoopTrap authors via direct outreach (2026-05-22). The addition is
purely additive: no existing tactic, technique, sub-technique, root
cause, or mitigation was renamed, moved, or removed relative to v2.3.

Contents:
- 10 tactics (TA001 through TA010), 30 techniques, 39 sub-techniques, 5
  structural root causes (RC1-RC5), and 30 architectural mitigations
- STIX 2.1 Bundle (228 objects: 1 identity, 10 x-mitre-tactic, 69
  attack-pattern, 30 course-of-action, 118 relationship)
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
multi-agent evaluation (DOI 10.5281/zenodo.20159697), the LoopTrap
termination-poisoning study (Xu et al., 2026, arXiv:2605.05846), and
corroborating research published in 2025-2026 by Anthropic, Apollo
Research, Microsoft AI Red Team, Cemri et al. (NeurIPS 2025), and
others. ATX-1 directly informs the AEGIS governance architecture
(AGP-1) and maps each technique to specific constitutional articles and
governance protocol mechanisms that mitigate it.

A descriptor article submitted to IEEE Data Descriptions (Manuscript ID
DATA-00033-2026) describes the dataset construction process and
validation in detail; that manuscript cites ATX-1 v2.3.
```

### Keywords (categories/tags)
- Agentic AI
- AI governance
- AI threat taxonomy
- STIX 2.1
- MITRE ATT&CK
- MITRE ATLAS
- Autonomous agents
- Termination Poisoning
- NIST AI RMF
- EU AI Act
- OWASP LLM Top 10
- OWASP Agentic Top 10
- AEGIS
- ATX-1

### Categories (IEEE DataPort taxonomy)
- Artificial Intelligence
- Security / Cybersecurity
- (match the categories used on the v2.3 record for series consistency)

### Subject
Threat taxonomy for autonomous AI agents acting on operational infrastructure.

### License
**Apache License 2.0** (matches the in-bundle declaration and all prior ATX-1 deposits).

### Related publications (cross-references)

- **ATX-1 v2.3 (previous DataPort version):** [10.21227/jr43-0571](https://doi.org/10.21227/jr43-0571) — previous version of this dataset
- **ATX-1 v1.0 (series root):** [10.21227/f87b-1d57](https://doi.org/10.21227/f87b-1d57)
- **ATX-1 on Zenodo (auto-minted repo snapshot mirror):** [10.5281/zenodo.19162184](https://doi.org/10.5281/zenodo.19162184) (concept DOI — always resolves to the latest aegis-governance snapshot; the v2.4-bearing snapshot is `10.5281/zenodo.20171712`)
- **LoopTrap (source for T6003):** [arXiv:2605.05846](https://arxiv.org/abs/2605.05846) — is derived from
- **Agents of Chaos study (foundational):** [arXiv:2602.20021](https://arxiv.org/abs/2602.20021) — is derived from
- **AEGIS Round 1 Edge Evaluation:** [10.5281/zenodo.20159697](https://doi.org/10.5281/zenodo.20159697) — cites
- **AEGIS architectural paper:** [10.5281/zenodo.19223924](https://doi.org/10.5281/zenodo.19223924) — cites

### Version note / changelog

ATX-1 v2.4 (released 2026-05-29) adds T6003 Poison Termination Judgment and its ten
sub-techniques under TA006. Purely additive relative to v2.3; all prior tactics,
techniques, sub-techniques, root causes, and mitigations are preserved unchanged.
Full changelog: `CHANGELOG-v2.4.md` in the deposited ZIP, or the source repository at
[github.com/aegis-initiative/aegis-governance](https://github.com/aegis-initiative/aegis-governance/blob/main/changelog/2026-05-29-atx1-v2.4.md).

## After the DOI mints

Once IEEE DataPort assigns the v2.4 DataPort DOI (`10.21227/XXXX-XXXX`), update the
following in the repository (one PR):

1. **`docs/atx/v2/data/atx-1-version-mapping.json`** — add `"v2.4_ieee_dataport": "10.21227/XXXX-XXXX"` and `"v2.4_zenodo": "10.5281/zenodo.20171712"` (the auto-minted snapshot) to `references`.
2. **`docs/atx/v2/atx-meta.json`** — add `"dataport_atx1_v2.4"` and `"doi_atx1_v2.4"` (Zenodo snapshot) to the `citation` block.
3. **`changelog/2026-05-29-atx1-v2.4.md`** — change the `**DOI:**` header line from "Pending …" to the minted DataPort DOI (+ Zenodo snapshot).
4. **Bundle `README.md`** — change the DOI line from "pending" to the minted DOI (re-zip optional).
5. **Re-run `npm run sync-atx`** to propagate updated `atx-meta.json` to `sites/governance/public/atx-1/`.
6. **Ecosystem `CLAUDE.md` identifier registry** (workspace root) — record the v2.4 DataPort DOI as the citable dataset DOI; note Zenodo is the auto-minted snapshot.
7. Reply to Xu/Wang (LoopTrap authors) with the published v2.4 dataset DOI.

> **Separate cleanup (decide before doing):** the records that label
> `10.5281/zenodo.20171712` as the "ATX-1 v2.3 Zenodo mirror" are stale — that DOI
> resolves to the v26.5.29.2 software snapshot (which contains v2.4). The correct v2.3
> dataset citation is the DataPort DOI `10.21227/jr43-0571`. This affects CLAUDE.md,
> `atx-meta.json`, version-mapping, and several memories; some published manuscripts
> may also reference it. Triage separately — do not bulk-edit published artifacts.
