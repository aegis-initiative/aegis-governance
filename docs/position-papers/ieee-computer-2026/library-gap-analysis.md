# Library Gap Analysis for AEGIS IEEE Paper

**Date:** 2026-03-24
**Library path:** `d:\dev\AEGIS Initiative\Library\`
**Paper:** AEGIS: A Constitutional Governance Architecture for Autonomous AI Agent Systems
**Current bibliography:** R01-R21 (21 refs, limit 20 -- must drop 1)

---

## 1. Library Inventory

31 PDFs + bibliography.bib + 3 working files (non-PDF).

### Already in paper bibliography (R01-R21)

| Library PDF | Paper Ref |
|---|---|
| Agents_of_Chaos_-_Shapira_2026 | R01 |
| Computer_Security_Technology_Planning_Study_-_Anderson_1972 | R02 |
| The_Protection_of_Information_in_Computer_Systems_-_Saltzer_Schroeder_1975 | R03 |
| NIST_AI_Risk_Management_Framework_AI_RMF_1.0_-_2023 | R04 |
| EU_Artificial_Intelligence_Act_Regulation_2024-1689_-_2024 | R05 |
| W3C_Decentralized_Identifiers_DIDs_v1.0_-_2022 | R06 |
| MI9_Integrated_Runtime_Governance_Framework_for_Agentic_AI_-_Wang_2025 | R07 |
| Governance-as-a-Service_Multi-Agent_Framework_for_AI_Compliance_-_Gaurav_2025 | R08 |
| Toward_Adaptive_Categories_Dimensional_Governance_for_Agentic_AI_-_Engin_Hand_2025 | R09 |
| A_Survey_of_Trust_and_Reputation_Systems_for_Online_Service_Provision_-_Josang_2007 | R10 |
| AI_Agents_with_Decentralized_Identifiers_and_Verifiable_Credentials_-_Rodriguez_Garzon_2025 | R11 |
| Decentralised_Identity_Federations_Using_Blockchain_-_Shuhan_2024 | R12 |
| A_Survey_of_Agentic_AI_and_Cybersecurity_-_2026 | R13 |
| The_2025_AI_Agent_Index_-_Chan_2025 | R14 |
| SAGA_A_Security_Architecture_for_Governing_AI_Agentic_Systems_-_Syros_2026 | R15 |
| POLYNIX_Hybrid_Policy_Enforcement_Framework_for_Zero-Trust_Security_-_Arunachalam_2026 | R16 |
| Scalable_Security_Enforcement_for_Cyber-Physical_Systems_-_Baird_2024 | R17 |
| Smart_IO_Modules_for_Mitigating_Cyber-Physical_Attacks_on_Industrial_Control_Systems_-_Pearce_2020 | R18 |
| ProSAS_Proactive_Security_Auditing_System_for_Clouds_-_Majumdar_2022 | R19 |
| Enforceable_Security_Policies_-_Schneider_2000 | R20 |
| NIST_SP_800-207_Zero_Trust_Architecture_-_2020 | R21 |

### Explicitly skipped (reviewed and rejected per bibliography-final.yaml)

| Library PDF | Reason |
|---|---|
| Runtime_Enforcement_of_Web_Service_Message_Contracts_with_Data_-_Halle_Villemaire_2012 | Domain too narrow (web services). No NEAT grounding. Outcompeted by R17/R18. |
| DroidForce_Enforcing_Complex_Data-centric_System-wide_Policies_in_Android_-_Rasthofer_2014 | Mobile app security domain. PDP/PEP pattern covered by stronger candidates. ARES lower tier. |
| Toward_Constitutional_Autonomy_in_AI_Systems_-_Agbemabiese_2026 | Terminological overlap only. Model-layer enforcement. IEEE Access pay-to-publish. |

### Not in paper bibliography, not skipped -- candidates for review

| # | Library PDF | Topic | Est. citations |
|---|---|---|---|
| A | Constitutional_AI_Harmlessness_from_AI_Feedback_-_Bai_2022 | RLAIF / model-layer alignment | ~3,000+ |
| B | Deep_Reinforcement_Learning_from_Human_Preferences_-_Christiano_2017 | RLHF origin paper | ~8,000+ |
| C | ISO_IEC_42001_AI_Management_System_-_2023 | AI management system standard | N/A (standard) |
| D | OWASP_Top_10_for_Large_Language_Model_Applications_-_2025 | LLM threat taxonomy | N/A (industry) |
| E | RFC_8705_OAuth_2.0_Mutual-TLS_Client_Authentication_-_2020 | mTLS client auth spec | N/A (RFC) |
| F | CoE_Framework_Convention_on_AI_and_Human_Rights_CETS_225_-_2024 | First binding int'l AI treaty | N/A (treaty) |
| G | EP_Press_Release_Framework_Convention_on_AI_Consent_Vote_-_2026 | EU ratification news | N/A (press) |

---

## 2. Assessment of Candidates A-G

### A. Bai et al. 2022 -- Constitutional AI (arXiv:2212.08073)

**Citation count:** ~3,000+. Extremely well-cited.

**Relevance to paper argument:** HIGH but as a **foil, not a support**. The paper's core argument is that governance must be enforced at the execution boundary, not the model layer. Constitutional AI is the strongest exemplar of model-layer governance. Citing Bai 2022 would let you make the "model-layer alignment is necessary but insufficient" argument with precision:

> "Constitutional AI [Bai 2022] and RLHF [Christiano 2017] operate at training time, producing probabilistic behavioral constraints. AEGIS operates at runtime, producing deterministic action-level enforcement."

**Problem:** The bibliography-final.yaml notes in the Agbemabiese skip decision: "Use Bai et al. 2022 if model-layer contrast needed." This was explicitly contemplated but never added to R01-R21. Given the 20-ref ceiling, adding Bai means dropping two refs (currently need to drop 1).

**Verdict:** STRONG CANDIDATE if you drop both R13 and R14 (both LOW weight, both flagged as drop candidates). Bai 2022 is worth more than either landscape survey for the architectural enforcement argument. It gives you a named, highly-cited target to contrast against.

### B. Christiano et al. 2017 -- RLHF (arXiv:1706.03741)

**Citation count:** ~8,000+. Foundational ML paper.

**Relevance:** MEDIUM. Same model-layer foil as Bai, but one generation earlier. If you cite Bai, Christiano becomes redundant -- Bai cites Christiano extensively and subsumes the lineage. In a 20-ref paper, Bai alone covers the model-layer contrast.

**Verdict:** SKIP for the IEEE paper. Bai 2022 is sufficient to represent the RLHF/Constitutional AI lineage.

### C. ISO/IEC 42001:2023

**Relevance:** MEDIUM. You already cite NIST AI RMF (R04) and EU AI Act (R05) as the standards triad. ISO 42001 is the management system standard -- AEGIS makes its requirements "technically auditable" per the bib note. But the paper argument is about architectural enforcement, not management systems.

**Verdict:** SKIP for the IEEE paper. R04 (NIST) + R05 (EU AI Act) adequately establish the standards context. ISO 42001 is more relevant to aegis-governance specs than to the architectural argument.

### D. OWASP Top 10 for LLM Applications 2025

**Relevance:** MEDIUM-HIGH. LLM01 (Prompt Injection) and LLM06 (Excessive Agency) directly name the failure modes AEGIS addresses. Could strengthen the motivation section alongside R01 (Agents of Chaos).

**Problem:** OWASP is an industry taxonomy, not a peer-reviewed paper. IEEE Computer reviewers may view it as grey literature. Also, R01 (Shapira) already provides empirical failure evidence with more academic rigor.

**Verdict:** MARGINAL. Only worth it if you need a widely-recognized threat taxonomy citation. R01 is stronger for the same purpose.

### E. RFC 8705 -- OAuth 2.0 Mutual-TLS

**Relevance:** LOW for the paper. This is an implementation-level protocol spec for AGP-1 authentication. The IEEE paper argues at the architectural level, not the protocol level. Citing an RFC for mTLS in a 20-ref governance paper would waste a slot.

**Verdict:** SKIP. Belongs in aegis-governance specs, not the IEEE paper.

### F. CoE Framework Convention on AI (CETS 225, 2024)

**Relevance:** MEDIUM. First legally binding international AI treaty. Article 3(1)(b) establishes conformance flexibility. Could strengthen the regulatory context alongside R05 (EU AI Act).

**Problem:** Same constraint as OWASP -- you already have R04 (NIST) + R05 (EU AI Act) for the regulatory frame. Adding a third standards/treaty ref at the expense of a technical ref weakens the architectural argument.

**Verdict:** SKIP for the IEEE paper unless the regulatory framing section is expanded.

### G. EP Press Release on CETS 225 Vote (2026)

**Relevance:** LOW. Press release, not a primary source. Secondary to (F) above.

**Verdict:** SKIP. Not appropriate for IEEE bibliography.

---

## 3. Gap Analysis: What the Library Is Missing

The Library covers the current bibliography well but has notable gaps for papers that would strengthen the architectural enforcement argument. These are papers NOT in the Library that the paper could benefit from:

### 3a. Capability-based security

No papers on capability-based security in the Library. Key missing works:

- **Dennis and Van Horn, 1966** -- "Programming Semantics for Multiprogrammed Computations" (Comm. ACM). Origin of capability-based addressing. ~1,500+ citations. AEGIS's capability tokens are a direct descendant. Would strengthen the lineage from Anderson (reference monitor) through capability-based authorization.

- **Miller, Yee, Shapiro, 2003** -- "Capability Myths Demolished" (tech report). Clarifies capability vs. ACL debate. Directly relevant to AEGIS's token-based authorization model.

### 3b. Modern reference monitor implementations

No papers on applying the reference monitor concept to modern systems (containers, cloud-native, microservices). Missing:

- **Jaeger et al., 2004** -- "Leveraging IPSec for Mandatory Access Control of Linux Network Communications" or related SELinux/Flask papers applying Anderson's reference monitor to Linux. Would show the reference monitor pattern has been successfully instantiated in production systems before AEGIS.

### 3c. Policy languages and formal verification

- **Becker, Fournet, Gordon, 2010** -- "SecPAL: Design and Semantics of a Decentralized Authorization Language" (J. Computer Security). Formal authorization language with federation. ~200 citations. Directly relevant to cross-org governance intelligence sharing.

### 3d. Runtime verification / monitoring

- **Leucker and Schallhart, 2009** -- "A Brief Account of Runtime Verification" (J. Logic and Algebraic Programming). ~800+ citations. Canonical survey of runtime verification. Would strengthen the theoretical foundation alongside Schneider 2000 (R20).

### 3e. AI agent architectures (for positioning)

- **Yao et al., 2023** -- "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR). ~2,500+ citations. Defines the reasoning-then-acting loop that AEGIS intercepts. Citing ReAct would let you precisely locate the enforcement boundary: "between ReAct's Act phase and infrastructure execution."

---

## 4. Recommendations

Given the 20-reference ceiling and the current state (21 refs, must drop 1):

### Highest-impact single swap

**Drop R13 (Agentic AI Survey) AND R14 (AI Agent Index). Add Bai 2022 (Constitutional AI).**

Result: 20 refs exactly. You gain the single most highly-cited foil for the model-layer vs. execution-layer argument. The landscape context from R13/R14 can be handled in prose ("agentic AI deployments have grown by an order of magnitude" needs no citation in a 2026 paper -- it is common knowledge to the audience).

### If the ceiling were relaxed or additional slots open

Priority order for additions NOT currently in the Library:

1. **Bai 2022** -- already in Library, highest impact (model-layer contrast)
2. **Yao et al. 2023 (ReAct)** -- NOT in Library; precisely locates the enforcement boundary
3. **Leucker-Schallhart 2009** -- NOT in Library; runtime verification theoretical foundation
4. **Dennis-Van Horn 1966** -- NOT in Library; capability-based security lineage

### Papers to acquire for the Library (not for the paper, for long-term AEGIS reference)

These would strengthen the Library's coverage even if they don't make the IEEE paper:

- Yao et al. 2023, "ReAct" (arXiv:2210.03629)
- Leucker and Schallhart 2009, "A Brief Account of Runtime Verification"
- Dennis and Van Horn 1966, "Programming Semantics for Multiprogrammed Computations"
- Lampson 1974, "Protection" (ACM OSR) -- capability and access control foundations
- Watson et al. 2010, "Capsicum: Practical Capabilities for UNIX" -- modern capability-based OS security

---

## 5. Summary

| Category | In Library | In Paper | Gap |
|---|---|---|---|
| Foundational security theory | 3 | 3 (R02, R03, R20) | None |
| Runtime/architectural enforcement | 6 | 4 (R16-R19) | None (2 skipped appropriately) |
| Model-layer AI governance | 3 | 0 | Bai 2022 is the critical gap |
| Standards and frameworks | 7 | 3 (R04, R05, R21) | ISO 42001 marginal; others correctly excluded |
| AI agent governance | 5 | 4 (R07-R09, R15) | None |
| Distributed trust/identity | 4 | 3 (R06, R10-R12) | None |
| Agent failures/landscape | 3 | 3 (R01, R13, R14) | None |
| Capability-based security | 0 | 0 | Structural gap in Library |
| Runtime verification theory | 0 | 0 | Structural gap in Library |
| Agent architecture (ReAct etc.) | 0 | 0 | Structural gap in Library |

**Bottom line:** The Library's coverage is strong for the current paper. The single highest-value action is adding Bai 2022 to the paper (it is already in the Library) by dropping R13+R14. The structural gaps (capability-based security, runtime verification, agent architecture papers) are worth acquiring for the Library but are not blocking for the IEEE paper at 20 refs.
