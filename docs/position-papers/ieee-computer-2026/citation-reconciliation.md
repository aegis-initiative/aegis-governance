# Citation Reconciliation — aegis-ieee-paper-draft-v0_2.md

Generated: 2026-03-24

---

## Reconciliation Table

| Line | Inline Citation | Ref [N] | Paper Title | Correct? | Notes |
|------|----------------|---------|-------------|----------|-------|
| 20 | ¹⁴ | [14] | Syros et al., "SAGA: Security Architecture for Governing AI Agentic Systems" | WRONG | Context is OpenClaw deployment growth stats. SAGA is about inter-agent security architecture, not deployment metrics. This likely should be [13] (Chan et al., AI Agent Index) or [1] (Shapira et al., Agents of Chaos). Possible superscript formatting error — ¹⁴ may have been intended as two separate citations ¹ ⁴ that merged, or it was meant to be [14] but the wrong reference. Given the sentence is about rapid deployment growth, [13] (AI Agent Index) is the correct citation. |
| 20 | ¹ | [1] | Shapira et al., "Agents of Chaos" | CORRECT | Failure patterns in agentic systems — matches Shapira's red-teaming findings exactly. |
| 22 | ¹ | [1] | Shapira et al., "Agents of Chaos" | WRONG | Context is "reinforcement learning from human feedback." Shapira is about agent failure modes, not RLHF. Should cite Christiano et al. 2017 ("Deep Reinforcement Learning from Human Preferences"), which is in the bibliography.bib but NOT in the paper's [N] reference list. Needs a new reference number. |
| 22 | ⁴ | [4] | NIST AI RMF 1.0 | WRONG | Context is "Constitutional AI training." NIST AI RMF is a risk management framework, not about Constitutional AI. Should cite Bai et al. 2022 ("Constitutional AI: Harmlessness from AI Feedback"), which is in the bibliography.bib but NOT in the paper's [N] reference list. Needs a new reference number. |
| 28 | ² | [2] | Anderson, "Computer Security Technology Planning Study" (1972) | CORRECT | Reference monitor properties — exact match. |
| 28 | ⁴ | [4] | NIST AI RMF 1.0 | CORRECT | NIST AI Risk Management Framework mapping — exact match. |
| 40 | ¹ | [1] | Shapira et al., "Agents of Chaos" | CORRECT | Detailed description of four failure classes from Shapira's study — exact match. |
| 42 | ¹³ | [13] | Chan et al., "The 2025 AI Agent Index" | CORRECT | Production deployment growth statistics — exact match. |
| 46 | ² | [2] | Anderson, "Computer Security Technology Planning Study" (1972) | CORRECT | Reference monitor concept and NEAT properties — exact match. |
| 54 | ³ | [3] | Saltzer & Schroeder, "The Protection of Information in Computer Systems" (1975) | CORRECT | Eight design principles — exact match. |
| 80 | ¹⁷ | [17] | Pearce et al., "Smart I/O Modules for Mitigating Cyber-Physical Attacks on ICS" (2020) | CORRECT | Industrial control system boundary enforcement — exact match. |
| 84 | ⁴ | [4] | NIST AI RMF 1.0 | CORRECT | Four functions of NIST AI RMF — exact match. |
| 102 | ² | [2] | Anderson, "Computer Security Technology Planning Study" (1972) | CORRECT | NEAT properties — exact match. |
| 110 | ⁶ | [6] | W3C, "Decentralized Identifiers (DIDs) v1.0" (2022) | CORRECT | DID-based identity for federation nodes — exact match. |
| 114 | ¹⁰ | [10] | Josang, Ismail, Boyd, "A survey of trust and reputation systems" (2007) | CORRECT | Trust/reputation systems, temporal factors in trust — exact match. |
| 124 | ¹ | [1] | Shapira et al., "Agents of Chaos" | CORRECT | Threat actor classes for agentic AI — reasonable fit (Shapira documents these attack patterns). |
| 128 | ¹⁷ | [17] | Pearce et al., "Smart I/O Modules" (2020) | CORRECT | Industrial control system boundary enforcement — exact match. |
| 128 | ¹⁸ | [18] | Majumdar et al., "ProSAS" (2022) | CORRECT | Proactive cloud security auditing — exact match. |
| 136 | ⁸ | [8] | Gaurav et al., "Governance-as-a-Service for AI Systems" (2025) | CORRECT | Post-inference governance filtering — exact match. |
| 138 | ⁷ | [7] | Wang et al., "MI9: A Multi-Intelligence Agent Protocol" (2025) | CORRECT | Reasoning loop governance — exact match. |
| 140 | ¹⁴ | [14] | Syros et al., "SAGA" (2026) | CORRECT | Inter-agent communication governance — exact match. |
| 142 | ¹¹ | [11] | Rodriguez Garzon et al., "LOKA" (2025) | CORRECT | DID/VC for AI agent identity — exact match. |
| 146 | ¹⁵ | [15] | Arunachalam et al., "POLYNIX" (2026) | CORRECT | Zero-trust policy enforcement, sub-1% overhead — exact match. |
| 146 | ¹⁶ | [16] | Baird et al., "Scalable Security Enforcement for CPS" (2024) | CORRECT | Compositional enforcement scaling — exact match. |
| 152 | ⁴ | [4] | NIST AI RMF 1.0 | CORRECT | Four functions of NIST AI RMF — exact match. |
| 162 | ⁵ | [5] | EU AI Act (2024) | CORRECT | Article 14 human oversight requirements — exact match. |

---

## Summary of Errors

### Error 1 — Line 20: ¹⁴ on OpenClaw deployment growth
**Current:** Cites [14] (SAGA — Syros et al.)
**Problem:** SAGA is about inter-agent security architecture. The sentence describes rapid deployment growth.
**Fix:** Change to ¹³ (Chan et al., AI Agent Index) — which is the deployment statistics paper. Alternatively, if ¹⁴ was intended as two separate superscript citations (¹ and ⁴), that is also wrong (¹ = Shapira, ⁴ = NIST RMF — neither are about deployment scale).

### Error 2 — Line 22: ¹ on "reinforcement learning from human feedback"
**Current:** Cites [1] (Shapira et al., Agents of Chaos)
**Problem:** Shapira is about red-teaming agent failures, not RLHF.
**Fix:** Add Christiano et al. 2017 ("Deep Reinforcement Learning from Human Preferences") to the reference list and cite it here. This paper is in the master bibliography as `christiano2017deep`.

### Error 3 — Line 22: ⁴ on "Constitutional AI training"
**Current:** Cites [4] (NIST AI RMF 1.0)
**Problem:** NIST AI RMF is a risk management framework, not about Constitutional AI training.
**Fix:** Add Bai et al. 2022 ("Constitutional AI: Harmlessness from AI Feedback") to the reference list and cite it here. This paper is in the master bibliography as `bai2022constitutional`.

---

## Reference List Audit

### References [1]–[18]: Gaps and Sequence

| Ref | In List? | Cited Inline? | Notes |
|-----|----------|---------------|-------|
| [1] | Yes | Yes (lines 20, 22*, 40, 124) | *Line 22 citation is incorrect |
| [2] | Yes | Yes (lines 28, 46, 102) | OK |
| [3] | Yes | Yes (line 54) | OK |
| [4] | Yes | Yes (lines 22*, 28, 84, 152) | *Line 22 citation is incorrect |
| [5] | Yes | Yes (line 162) | OK |
| [6] | Yes | Yes (line 110) | OK |
| [7] | Yes | Yes (line 138) | OK |
| [8] | Yes | Yes (line 136) | OK |
| [9] | Yes | **NO — NEVER CITED** | Engin & Hand, "Toward Adaptive Categories for AI Governance" — present in reference list but never cited anywhere in the paper |
| [10] | Yes | Yes (line 114) | OK |
| [11] | Yes | Yes (line 142) | OK |
| [12] | Yes | **NO — NEVER CITED** | Shuhan et al., "Decentralised identity federations using blockchain" — present in reference list but never cited anywhere in the paper |
| [13] | Yes | Yes (line 42) | OK |
| [14] | Yes | Yes (lines 20*, 140) | *Line 20 citation is incorrect |
| [15] | Yes | Yes (line 146) | OK |
| [16] | Yes | Yes (line 146) | OK |
| [17] | Yes | Yes (lines 80, 128) | OK |
| [18] | Yes | Yes (line 128) | OK |

**Sequence:** [1] through [18] — sequential, no gaps.

### Inline citations pointing to nonexistent references
None. All inline citation numbers (1–18) have corresponding entries.

### Uncited references
- **[9]** Engin & Hand, "Toward Adaptive Categories for AI Governance" (2025) — never cited
- **[12]** Shuhan et al., "Decentralised identity federations using blockchain" (2024) — never cited

**Recommendation:** Either cite [9] and [12] somewhere appropriate or remove them. IEEE format requires that all references be cited in text.

---

## Placement Recommendations for R20 and R21

### R20: Schneider 2000 — "Enforceable Security Policies"

Schneider's paper establishes that only safety policies (those that can be checked by monitoring execution prefixes) are enforceable by runtime monitors / security automata. This is the formal theoretical foundation for why AEGIS's enforcement model works — it enforces safety properties at the action boundary.

**Recommended placements:**

1. **Line 12 (Abstract)** — Where the paper says "making unauthorized actions structurally unavailable rather than merely discouraged." A Schneider citation would ground the claim that AEGIS enforces safety properties per the formal definition. However, abstracts typically avoid citations in IEEE format. Better to cite in the body.

2. **Line 50 (end of Reference Monitor section)** — After "This positions AEGIS as an AI-domain reference monitor rather than a behavioral guidance system." Add a sentence: "Schneider (2000) established formally that only safety policies — those verifiable by monitoring execution prefixes — are enforceable by runtime monitors; AEGIS's constitutional constraints are safety policies by construction, ensuring they fall within the class of properties that architectural enforcement can guarantee." This is the strongest natural placement.

3. **Line 86 (Layer 1: Doctrine)** — Where Article III (Deterministic Enforcement) is described. The bibliography note for Schneider explicitly says it is the "Foundation for AEGIS Constitution Article III." A citation here would be: "Article III (Deterministic Enforcement) requires that governance decisions be made by an architectural component, not by the AI — a requirement grounded in Schneider's formal result that safety policies are the maximal class enforceable by runtime monitors [R20]."

### R21: NIST SP 800-207 — "Zero Trust Architecture" (Rose et al. 2020)

This is the canonical zero trust architecture reference. AEGIS implements ZTA tenets (never trust, always verify; least privilege; assume breach).

**Recommended placements:**

1. **Line 98 (Governance Gateway section)** — Where JWT/mTLS authentication and default-deny are described. The gateway's design — authenticate every request, no implicit trust, fail-closed — is textbook zero trust. Add: "This gateway design implements the core tenets of zero trust architecture as defined by NIST SP 800-207: no implicit trust granted based on network location or asset ownership; authentication and authorization required for every request; and access granted on a per-session basis with least privilege."

2. **Line 46 (Reference Monitor section)** — After describing NEAT properties, note the parallel to ZTA: "These properties align with the zero trust architecture model (Rose et al., 2020), which similarly requires that no resource is inherently trusted and that every access request is fully authenticated and authorized."

3. **Line 146 (Runtime enforcement precedents in Related Work)** — Where POLYNIX is discussed for zero-trust enforcement. POLYNIX explicitly implements zero trust; a citation to NIST SP 800-207 as the canonical ZTA definition would strengthen the paragraph: "The POLYNIX framework implements zero trust security principles as defined in NIST SP 800-207 [R21]..."

---

## Complete Citation Inventory

Total inline citations found: **25**
- Correct: **21**
- Incorrect: **3** (line 20 ¹⁴, line 22 ¹, line 22 ⁴)
- Correct but citing uncited-elsewhere refs: **1** (n/a — [9] and [12] are never cited at all)

Total references in list: **18**
- Cited at least once: **16**
- Never cited: **2** ([9], [12])

Missing from reference list (needed for corrections):
- Christiano et al. 2017 — for RLHF citation on line 22
- Bai et al. 2022 — for Constitutional AI citation on line 22

Missing from reference list (canon additions per bibliography):
- Schneider 2000 — "Enforceable Security Policies"
- NIST SP 800-207 (Rose et al. 2020) — "Zero Trust Architecture"
