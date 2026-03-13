# CLAUDE.md — AEGIS Repository as Living Paper
_Vision Document — 2026-03-13_

## Core Thesis

**The entire `finnoybu/aegis-governance` repository IS the living paper.**

Not just code + docs. A complete, living, peer-reviewable governance framework where every claim is traceable to established research, every position is cited, and the entire corpus evolves as a unified scholarly work.

---

## The Vision

### Current State:
- AEGIS repo = collection of documents
- Some cite sources, some don't
- Positioning happened organically
- Prior art exists but isn't systematically referenced

### Target State:
**Every document in the repository contributes to a unified, academically rigorous framework.**

Every major document should:
- ✅ Cite foundational prior art where relevant
- ✅ Position AEGIS relative to established work
- ✅ Use consistent terminology aligned with cited sources
- ✅ Reference the same corpus of papers systematically
- ✅ Cross-reference other AEGIS documents
- ✅ Link to canonical bibliography

---

## Why This Works

### 1. Academic Rigor
- Shows AEGIS is built on established research
- Demonstrates awareness of the field
- Positions AEGIS in scholarly context
- Every claim traceable to source

### 2. Community Trust
- Transparent about influences
- Acknowledges prior art
- Shows this isn't invented in a vacuum
- Demonstrates intellectual honesty

### 3. Adoption Path
- Engineers can trace concepts back to source papers
- Researchers can validate claims
- Standards bodies see established precedent
- Reduces "not invented here" skepticism

### 4. Living Document
- Papers evolve, repo evolves
- New research gets incorporated
- Citations stay current
- Corpus grows with the field

---

## What This Means Practically

### Every Major Document Gets Citations

**`AEGIS_System_Overview.md`:**
- Cite DroidForce (2014) for PDP/PEP architecture
- Cite Smart I/O Modules (2020) for boundary enforcement
- Cite Web Services (2012) for runtime contracts
- Cite Constitutional Autonomy (2026) for model-layer positioning

**`AEGIS_Reference_Architecture.md`:**
- Cite POLYNIX (2026) for hybrid enforcement validation
- Cite DroidForce (2014) for architectural pattern
- Cite CPS Parallel (2024) for compositional enforcement
- Reference OPA for policy engine design

**`AEGIS_Threat_Model.md` (ATM-1):**
- Cite Smart I/O (2020) for compromised controller model
- Cite relevant STRIDE methodology papers
- Reference industrial control security literature

**`AEGIS_Constitution.md`:**
- Cite foundational security automata work (Schneider)
- Cite reference monitor concepts
- Reference policy enforcement literature

**`AGP-1 Protocol Specification`:**
- Cite Web Services runtime enforcement (2012)
- Cite relevant protocol papers
- Reference LTL-FO+ specification languages

**`README.md` (root):**
- Cite key papers that establish the field
- Position AEGIS in landscape
- Link to REFERENCES.md

---

## The Canonical Bibliography

**Create: `REFERENCES.md` at repository root**

Every paper cited anywhere in the repo, in one canonical place.

### Structure:

```markdown
# AEGIS References

## Foundational Prior Art

### Runtime Enforcement
1. Hallé, S., & Villemaire, R. (2012). Runtime Enforcement of Web Service Message Contracts with Data. *IEEE Transactions on Services Computing*, 5(2), 192-206. doi: 10.1109/TSC.2011.10

2. Rasthofer, S., Arzt, S., Lovat, E., & Bodden, E. (2014). DroidForce: Enforcing Complex, Data-centric, System-wide Policies in Android. *2014 Ninth International Conference on Availability, Reliability and Security*, 40-49. doi: 10.1109/ARES.2014.13

3. Pearce, H., Pinisetty, S., Roop, P. S., Kuo, M. M. Y., & Ukil, A. (2020). Smart I/O Modules for Mitigating Cyber-Physical Attacks on Industrial Control Systems. *IEEE Transactions on Industrial Informatics*, 16(7), 4659-4669. doi: 10.1109/TII.2019.2945520

4. Baird, A., Panda, A., Pearce, H., Pinisetty, S., & Roop, P. (2024). Scalable Security Enforcement for Cyber-Physical Systems. *IEEE Access*, 12, 18475-18498. doi: 10.1109/ACCESS.2024.3357714

5. Arunachalam, K., Kayyidavazhiyil, A., & Santikellur, P. (2026). POLYNIX: A Hybrid Policy Enforcement Framework for Zero-Trust Security in Virtualized Systems. *2026 IEEE 23rd Consumer Communications & Networking Conference (CCNC)*. doi: 10.1109/CCNC65079.2026.11366307

### Model-Layer Approaches
1. Agbemabiese, W. T. (2026). Toward Constitutional Autonomy in AI Systems: A Theoretical Framework for Aligned Agentic Intelligence. *IEEE Access*, 14, 11385-11402. doi: 10.1109/ACCESS.2026.3654907

2. [Constitutional AI papers from Anthropic]

3. [RLHF foundational papers]

### Foundational Security
1. Schneider, F. B. (2000). Enforceable Security Policies. *ACM Transactions on Information and System Security*, 3(1), 30-50.

2. [Reference monitor concept papers]

3. [Security automata literature]

### Distributed Systems & Trust
1. [Byzantine fault tolerance - Lamport et al.]

2. [Distributed consensus - Paxos/Raft]

3. [Trust models and reputation systems]

### Standards & Frameworks
1. NIST AI Risk Management Framework (AI RMF 1.0). (2023). National Institute of Standards and Technology. https://www.nist.gov/itl/ai-risk-management-framework

2. [ISO/IEC AI standards]

3. [IEEE autonomous systems standards]

### Application Domain
1. [LLM agent frameworks - LangChain, AutoGPT, CrewAI]

2. [AI supply chain security]

3. [Multi-agent systems security]
```

---

## Cross-Referencing Pattern

**In every document, include a "Related Work" or "Foundations" section:**

```markdown
## Related Work

AEGIS builds on established runtime enforcement patterns, particularly:

- **Centralized PDP + Decentralized PEPs** [DroidForce, 2014] - AEGIS adopts this proven architectural pattern for system-wide governance. The centralized Policy Decision Point (AGP-1) mirrors DroidForce's architecture, while AEGIS gates function as distributed Policy Enforcement Points.

- **Boundary enforcement** [Smart I/O Modules, 2020] - AEGIS operates at the same architectural boundary (between controller and infrastructure) using the same threat model (compromised controller assumption). The I/O module pattern directly informs AEGIS gate positioning.

- **Runtime contract enforcement** [Hallé & Villemaire, 2012] - AEGIS extends these foundational principles to agentic AI systems, maintaining the transparency and determinism established in web service contract enforcement.

- **Hybrid enforcement architecture** [POLYNIX, 2026] - AEGIS's centralized decision + distributed enforcement model is validated by POLYNIX's demonstration of <1% CPU overhead and <2s policy propagation in zero-trust environments.

See [REFERENCES.md](../../REFERENCES.md) for complete citations.
```

---

## Citation Format

**Use IEEE citation style consistently:**

```
[Author(s)], "Title," *Publication*, vol. X, no. Y, pp. ZZZ-ZZZ, Year, doi: XX.XXXX/XXXXXX.
```

**In-text citations:**

```
The centralized PDP + decentralized PEP architecture [DroidForce, 2014] provides...
```

OR

```
Rasthofer et al. demonstrated that centralized policy decision with distributed enforcement scales to system-wide governance without modification to underlying applications [1].
```

---

## Terminology Alignment

**Use terms from cited papers consistently:**

| AEGIS Term | Source Paper | Source Term |
|------------|--------------|-------------|
| Policy Decision Point (PDP) | DroidForce (2014) | Centralized Policy Decision Point |
| Policy Enforcement Point (PEP) | DroidForce (2014) | Decentralized Policy Enforcement Point |
| Boundary enforcement | Smart I/O Modules (2020) | Runtime enforcement between cyber and physical domains |
| Compromised controller model | Smart I/O Modules (2020) | Assumption of controller compromise |
| Runtime contract | Web Services (2012) | Message contracts with data |
| Hybrid enforcement | POLYNIX (2026) | Centralized OPA + Distributed Tetragon |
| Architectural-layer governance | (AEGIS original) | Contrasts with model-layer (Constitutional Autonomy) |

---

## Document-Specific Citation Guidelines

### Constitution (`AEGIS_Constitution.md`)
**Cite:**
- Security automata (Schneider)
- Reference monitors
- Policy enforcement fundamentals

**Example:**
```markdown
Article III — Deterministic Enforcement draws from the reference monitor concept [Anderson, 1972] and security automata theory [Schneider, 2000], requiring that governance be architecturally guaranteed rather than probabilistically enforced.
```

### Threat Model (`AEGIS_Threat_Model.md`)
**Cite:**
- STRIDE methodology
- Smart I/O compromised controller model
- Industrial control security literature

**Example:**
```markdown
The compromised agent threat (T-01) mirrors the compromised controller model established in industrial control systems [Smart I/O, 2020]. AEGIS assumes that AI agents, like PLCs in industrial environments, may be compromised through prompt injection, model weights manipulation, or adversarial inputs.
```

### Protocol Specification (`AGP-1`)
**Cite:**
- Web Services runtime enforcement
- Message contract specifications
- LTL-FO+ or similar formal languages

**Example:**
```markdown
The ACTION_PROPOSE → ACTION_DECIDE → ACTION_EXECUTE message flow follows the transparent enforcement pattern established for web service contracts [Hallé & Villemaire, 2012], adapted for agentic AI governance.
```

### Architecture Documents
**Cite:**
- DroidForce for PDP/PEP
- POLYNIX for hybrid validation
- CPS papers for compositional enforcement

**Example:**
```markdown
The AEGIS architecture implements the centralized PDP + distributed PEP pattern proven effective in Android system-wide policy enforcement [DroidForce, 2014]. This separation of policy decision (AGP-1) from policy enforcement (gates) enables governance across heterogeneous AI agent fleets.
```

---

## What This Makes AEGIS

✅ **Academically rigorous** - built on cited prior art\
✅ **Defensible** - every claim traceable to source\
✅ **Credible** - shows awareness of field\
✅ **Adoptable** - readers can validate claims\
✅ **Living** - citations stay current\
✅ **Peer-reviewable** - structured like academic work\
✅ **Standards-ready** - documented foundation for IEEE/NIST submissions

---

## The Repository Becomes

**Not just code + docs.**

**A complete, living, peer-reviewable governance framework** with:
- Constitution (principles with cited foundations)
- Architecture (design with architectural precedents)
- Protocol (specification with protocol foundations)
- Implementation (code with reference implementations)
- Threat Model (security with established threat models)
- **Citations (traceable foundation for every claim)**

**Every piece traceable to established research.**

---

## Relationship to IEEE/NIST Submissions

**The repository is the authoritative living document.**

**Submissions are snapshots:**

- **IEEE paper** = snapshot of living paper at time T1
- **NIST submission** = snapshot of living paper at time T2
- **Future standards work** = snapshots of living paper at time TN

**But the repository:**
- Evolves continuously
- Incorporates new research
- Updates citations
- Refines positioning
- Remains current

**Submissions cite the repository. The repository cites the field.**

---

## Implementation Plan

### Phase 1: Create Foundation (Week 1)
- [ ] Create `REFERENCES.md` at repository root
- [ ] Populate with 6 core papers (DroidForce, Smart I/O, POLYNIX, Web Services, CPS Parallel, Constitutional Autonomy)
- [ ] Add foundational security papers (Schneider, reference monitors)
- [ ] Add AI safety/alignment papers (Constitutional AI, RLHF)

### Phase 2: Audit Major Documents (Week 2)
- [ ] `AEGIS_System_Overview.md` - add Related Work section
- [ ] `AEGIS_Reference_Architecture.md` - add architectural precedents
- [ ] `AEGIS_Constitution.md` - add foundational citations
- [ ] `AEGIS_Threat_Model.md` - add security literature citations
- [ ] `AGP-1_Protocol_Spec.md` - add protocol foundations

### Phase 3: Align Terminology (Week 3)
- [ ] Create terminology mapping table (AEGIS term → source paper)
- [ ] Update documents to use consistent terms
- [ ] Cross-reference between AEGIS documents
- [ ] Ensure definitions align with cited sources

### Phase 4: Cross-Reference (Week 4)
- [ ] Add "See also" sections linking related AEGIS docs
- [ ] Link all citations to `REFERENCES.md`
- [ ] Add citation anchors for internal references
- [ ] Create citation index

### Phase 5: Maintain (Ongoing)
- [ ] Update `REFERENCES.md` as new papers emerge
- [ ] Add citations when new research is relevant
- [ ] Keep terminology aligned
- [ ] Review citations quarterly

---

## Success Criteria

**When complete, the repository will:**

1. ✅ Every major claim has a traceable citation
2. ✅ Every architectural decision references precedent
3. ✅ Every term aligns with established literature
4. ✅ `REFERENCES.md` is comprehensive and current
5. ✅ Cross-references create coherent navigation
6. ✅ Readers can validate AEGIS claims through cited sources
7. ✅ The repository functions as a complete scholarly work
8. ✅ IEEE/NIST submissions draw from canonical repository citations

---

## Key Principle

**The repository is not documentation for AEGIS.**

**The repository IS AEGIS.**

Every document contributes to a unified, living, peer-reviewable framework where:
- Principles are cited to foundations
- Architecture is traced to precedents
- Protocol is grounded in established patterns
- Threat model builds on security literature
- Implementation references best practices

**The whole is greater than the sum of its parts.**

**The repository becomes the definitive scholarly work on architectural AI governance.**

---

## For Claude Code / AI Assistants

When working in `finnoybu/aegis-governance` or related AEGIS repositories:

### Approach

**Always:**
- Check if claims should be cited
- Reference `REFERENCES.md` when adding technical content
- Maintain consistent terminology with cited sources
- Cross-reference related AEGIS documents
- Suggest citations when reviewing content
- Read a file before editing it

**Never:**
- Make uncited claims about architectural precedents
- Use terminology inconsistent with cited sources
- Create isolated documents without cross-references
- Ignore existing citations when updating content

**The repository is a living paper. Treat it with academic rigor.**

---

### Terminology: Critical Distinctions

These distinctions matter for positioning accuracy. Do not conflate them.

| Term | Definition | Do Not Confuse With |
|------|-----------|---------------------|
| **RLHF** | Reinforcement learning from human feedback (human labelers) | Constitutional AI |
| **Constitutional AI** | Reinforcement learning from AI feedback / RLAIF (Anthropic) | RLHF |
| **Constitutional Autonomy** | Agbemabiese (IEEE Access 2026) — runtime attention mechanism modification | Constitutional AI |
| **Architectural-layer governance** | AEGIS — enforcement at execution boundary, model-agnostic | Model-layer approaches |
| **Model-layer governance** | Training-time alignment (RLHF, Constitutional AI, fine-tuning) | Architectural enforcement |

**Constitutional Autonomy** (Agbemabiese 2026) is a brand-new, not-yet-widely-cited paper. Use it only where properly cited (outreach, Discussion #39). Do not add it to comparison tables without explicit instruction.

**Defense-in-depth framing:** Model-layer and architectural-layer approaches are **complementary**, not competitive. AEGIS positioning should always reflect this.

---

### Frozen & Protected Documents

| Document | Status | Rule |
|----------|--------|------|
| `docs/position-papers/nist/2026-03-aegis-nist-ai-rmf-position-statement.md` | SUBMITTED | Do not edit. Contains `> **SUBMITTED — DO NOT EDIT**` header. |
| `aegis-core/manifesto/AEGIS_Manifesto.md` | v0.1, referenced in NIST submission | Substantial edits require version bump to 0.2. Treat changes as amendments, not revisions. |

---

### Single Source of Truth

Canonical files are authoritative. All other documents must **link** to them, not restate their content.

- NIST submission details → `docs/position-papers/nist/2026-03-aegis-nist-ai-rmf-position-statement.md`
- NIST directory index → `docs/position-papers/nist/README.md`
- Outreach records → `docs/outreach/`

Before adding content that describes a canonical document, check whether it already exists there. If it does, link — don't copy.

---

### Git Workflow

```
git checkout -b <type>/<short-description>
# make changes
git add <specific files>
git commit -m "Type: description\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push -u origin <branch>
gh pr create ...
gh pr merge <number> --squash --auto
```

**Branch naming:** `docs/topic`, `feat/topic`, `fix/topic`\
**Merge strategy:** squash merge always\
**Never force-push, never skip hooks**

---

### Markdown Conventions

- **Line breaks in metadata/headers:** Use backslash `\` at end of line — not trailing spaces (linter strips trailing spaces)
- **Notes and notices:** Use blockquotes `>` — not fenced code blocks
- **Document metadata:** Version, Status, Author, Last Updated at top of file
- **Frozen notice:** `> **SUBMITTED — DO NOT EDIT**` as first content after metadata

---

### Outreach Records (`docs/outreach/`)

Header fields (in order): Date, From, To, Status, Response, Discussion\
Status values: `Initial outreach sent` | `Follow-up sent` | `Response received` | `Closed`\
Response values: `Pending` | `Received` | `No response`\
File naming: `YYYY-MM-<topic>.md`

Keep `docs/outreach/README.md` log table current when adding new records.

---

## Questions This Raises

1. Should RFCs include formal citations in addition to references?
2. How do we handle citations in code comments?
3. Should examples reference source papers when demonstrating patterns?
4. Do we create a separate bibliography for each major component (AGP-1, ATM-1, GFN-1)?
5. How do we version REFERENCES.md as citations evolve?

**These questions should be addressed as the citation framework matures.**

---

**End of Vision Document**

*This document establishes the principle that the AEGIS repository functions as a comprehensive, living, peer-reviewable scholarly work. All contributors should treat the repository with the rigor expected of academic publications.*

**Status:** Vision documented — implementation begins after immediate priorities (positioning updates, outreach)

**Next Review:** After Phase 1 (REFERENCES.md creation)
