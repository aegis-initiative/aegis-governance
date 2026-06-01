---
title: "ATX-1: AEGIS Threat Matrix — Technique Taxonomy"
description: "ATX-1 technique taxonomy — 10 tactics, 30 techniques (39 sub-techniques) for agentic AI threats"
---

# ATX-1: AEGIS Threat Matrix — Technique Taxonomy

## Adversarial Knowledge Base for Agentic AI Actor Behavior

**Version:** 2.4.0\
**Date:** 2026-05-29\
**Status:** Active — v2.4 adds Termination Poisoning (T6003) under TA006 with 10 sub-techniques mapped to the strategies of Xu et al. (LoopTrap, arXiv:2605.05846). Severity remains removed (v2.3) for MITRE alignment.\
**Maintainer:** AEGIS Initiative — AEGIS Operations LLC\
**License:** CC-BY-SA-4.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Gap](#2-the-gap)
3. [Structural Root Causes](#3-structural-root-causes)
4. [Tactic Taxonomy](#4-tactic-taxonomy)
5. [Technique Catalog](#5-technique-catalog)
6. [AEGIS Mitigation Mapping](#6-aegis-mitigation-mapping)
7. [OWASP Top 10 LLM Cross-Reference](#7-owasp-top-10-llm-cross-reference)
8. [Methodology Precedent](#8-methodology-precedent)
9. [Relationship to Existing Frameworks](#9-relationship-to-existing-frameworks)
10. [References](#10-references)

---

## 1. Executive Summary

MITRE ATT&CK catalogs how human adversaries attack computer systems. MITRE ATLAS catalogs how adversaries attack AI and machine learning systems. Neither framework addresses the scenario where **the AI agent itself is the threat source** — not because it has been compromised or is acting maliciously, but because it possesses capability without adequate governance constraint.

**ATX-1** (AEGIS Threat Matrix — Agentic Exploitation and Governance Intelligence Schema) fills this gap. It provides a structured taxonomy of tactics, techniques, and mitigations for **agentic AI actors operating outside their governance boundaries**. There is no malicious intent. There is no external adversary. Harm emerges from capability without constraint.

ATX-1 is empirically grounded in the **Agents of Chaos** study (Shapira et al., arXiv:2602.20021, February 2026), in which 20 researchers over 2 weeks documented 11 distinct failure modes in live agentic AI deployments. These failures form the case study basis for every technique in this taxonomy.

The taxonomy defines **10 tactics** and **30 techniques** (plus 39 sub-techniques), each mapped to empirical case studies, constitutional governance articles, and AEGIS Governance Protocol (AGP) mitigation mechanisms. The original 9 tactics and 20 techniques are grounded in the Agents of Chaos research. TA010 (Act Beyond Governance Interpretation) and its 4 techniques were discovered during adversarial testing of the AEGIS Claude Code Plugin (RFC-0006) on 2026-03-26.

---

## 2. The Gap

Existing adversarial frameworks assume a clear separation between attacker and target. Agentic AI dissolves this separation.

### Framework Comparison

| Framework | Threat Source | Target | Agent Role |
|-----------|--------------|--------|------------|
| **ATT&CK** | Human adversary | Computer systems and networks | Agent is never the threat source |
| **ATLAS** | Human adversary | AI/ML systems | AI is the target, not the actor |
| **ATX-1** | AI agent itself | Systems, data, users, other agents | Agent IS the threat source |

### The Canonical Example

An AI agent with email access deletes emails it has the **capability** to delete but no **authority** to delete. There is no attacker. There is no exploit. There is no prompt injection. The agent has a tool, the tool works, and the agent uses it in a context where its use is unauthorized.

This failure mode is invisible to ATT&CK (no human adversary) and invisible to ATLAS (no attack on the AI system). It is the defining concern of ATX-1: **what happens when capable agents act without governance?**

### The Authority-Capability Distinction

ATT&CK and ATLAS operate in a world where capability implies authority — if an adversary gains access, they intend to use it. ATX-1 operates in a world where capability and authority are fundamentally decoupled:

- **Capability**: what the agent *can* do (tool access, API permissions, system privileges)
- **Authority**: what the agent *may* do (delegated by a specific principal, for a specific scope, at a specific time)

Every ATX-1 technique exploits the gap between these two.

---

## 3. Structural Root Causes

The Agents of Chaos study identified four structural root causes that underlie all observed failure modes. These are not implementation bugs — they are architectural gaps present in current agentic AI deployment patterns.

### RC1: No Stakeholder Model

Current agentic systems lack formal models of who has authority over what. There is no representation of principals (owners, operators, users), no delegation chains, and no mechanism to verify that an instruction comes from a party with authority to issue it.

**Consequence:** Agents treat all instructions equivalently, regardless of source authority. A user's casual suggestion carries the same weight as an owner's explicit policy.

### RC2: No Self-Model

Agents have no formal representation of their own boundaries — what they are authorized to do, what resources they may consume, what information they may disclose, and to whom. Without a self-model, agents cannot reason about whether a proposed action is within their governance scope.

**Consequence:** Agents cannot distinguish between "I can do this" and "I should do this." Every capability is exercised without governance reflection.

### RC3: No Private Deliberation Surface

Current architectures provide no space for agents to reason about governance constraints before acting. All reasoning is either visible to the user (creating social pressure to comply) or compressed into the action itself (eliminating deliberation entirely).

**Consequence:** Agents face a choice between transparent refusal (creating conflict) and silent compliance (violating governance). There is no space for nuanced governance reasoning.

### RC4: Prompt Injection Is Structural

Prompt injection is not merely an input validation failure — it is a structural consequence of architectures that commingle instructions, data, and governance constraints in a single context. As long as instructions and data share a channel, injection is inherent.

**Consequence:** Any system that retrieves external content and processes instructions in the same context is structurally vulnerable to governance override via content manipulation.

### RC5: No Environment Model

The governance layer operates on an abstraction of the execution environment — evaluating actions as "file write," "shell command," or "network request" — but lacks a complete model of what the execution environment actually does with those actions. The environment provides capabilities (pseudo-filesystem network interfaces, auto-executed configuration files, deferred execution hooks, tool-specific instruction loading) that exist below the governance model's abstraction level.

**Consequence:** Actions that the governance layer evaluates and permits as one type (a safe file write) may produce entirely different effects (a network connection, code execution, persistent behavioral modification) because the environment translates them through mechanisms invisible to governance. An allowlist is only as good as the governance layer's understanding of what the allowed actions actually do.

**Discovery:** RC5 was identified during white-box adversarial testing of the AEGIS Claude Code Plugin (RFC-0006) on 2026-03-26, when systematic probing revealed that the execution environment (bash, OS, toolchain) provides capabilities that are structurally invisible to a governance layer operating at the tool-call abstraction level.

---

## 4. Tactic Taxonomy

ATX-1 defines 10 tactics. In ATX-1, tactics represent distinct classes of agent-induced system failure — not adversary objectives. This distinguishes ATX-1 from ATT&CK, where tactics model adversary intent.

---

### TA001: Violate Authority Boundaries

**Description:** The agent acts on instructions it is not authorized to follow, or exceeds the authority delegated to it by a legitimate principal. Exploits Authority and Identity primitives.

**Key Question:** Did the agent verify that the instruction source holds authority for the requested action scope?

**Techniques:** T1001 (Execute Non-Owner Instruction), T1002 (Infer Implicit Authority), T1003 (Propagate Spoofed Authority at Scale)

---

### TA002: Exceed Operational Scope

**Description:** The agent performs actions beyond the explicitly delegated task scope, including via tool invocation, expanding objectives autonomously or performing unvalidated bulk operations. Exploits Delegation and Objective Control primitives.

**Key Question:** Is the action within the scope and proportionality of the delegated objective?

**Techniques:** T2001 (Expand Task Scope Autonomously), T2002 (Perform Unvalidated Bulk Operations), T2003 (Obscure Objective Through Delegation), T2004 (Exploit Tool-Chain Composition)

---

### TA003: Compromise System Integrity

**Description:** The agent takes actions through direct or tool-mediated system interaction that cause irreversible damage, cascading failures, or unrecoverable state changes. Exploits State and Environment primitives.

**Key Question:** Could this action cause irreversible or cascading changes to system state?

**Techniques:** T3001 (Perform Irreversible Destructive Action), T3002 (Trigger Cascading System Changes)

---

### TA004: Expose or Exfiltrate Information

**Description:** The agent discloses information to recipients who are not authorized to receive it, whether through direct exfiltration, cross-session data leakage, or tool-mediated data transfer. Exploits Memory, Context, and Data Boundaries primitives.

**Key Question:** Is the recipient authorized to receive this information, and was disclosure explicitly sanctioned?

**Techniques:** T4001 (Exfiltrate Context-Scoped Data), T4002 (Leak Cross-Session or Persistent Data), T4003 (Cross-Domain Secret Leakage)

---

### TA005: Violate State Integrity

**Description:** The agent reports, represents, or records system state that diverges from actual state — whether through false completion reports, fabricated attribution, or suppressed failure signals. Exploits State and Observability primitives.

**Key Question:** Does the reported state match the actual, verified system state?

**Techniques:** T5001 (Report False Task Completion), T5002 (Fabricate Action Attribution), T5003 (Suppress or Omit Execution Failure)

---

### TA006: Abuse Resource Allocation

**Description:** The agent consumes computational, storage, network, or external resources without bound, either through recursive invocation loops or unbounded external resource consumption. Exploits Resource Control primitives.

**Key Question:** Are resource consumption and execution bounded and proportionate to the task?

**Techniques:** T6001 (Execute Recursive Invocation Loops), T6002 (Consume Unbounded External Resources), T6003 (Poison Termination Judgment)

---

### TA007: Manipulate Agent Interactions

**Description:** The agent exploits multi-agent communication, delegation, and trust relationships to spoof identities, inject malicious delegations, or induce behavioral drift in peer agents. Exploits Coordination and Identity primitives.

**Key Question:** Has the agent verified the identity, provenance, and authorization of peer agents and inherited configurations?

**Techniques:** T7001 (Spoof Agent Identity), T7002 (Inject Malicious Delegation Chains), T7003 (Induce Cross-Agent Behavioral Drift), T7004 (Induce Unsafe Consensus)

---

### TA008: Establish or Modify Persistence

**Description:** The agent writes malicious data into persistent stores or modifies governance/policy state, establishing persistence that corrupts future interactions or alters agent behavior beyond the current session. Exploits Memory and Governance State primitives.

**Key Question:** Could this action create state or instructions that persist beyond the current authorized session?

**Techniques:** T8001 (Poison Persistent Memory), T8002 (Corrupt Governance or Policy State)

---

### TA009: Evade Detection or Oversight

**Description:** The agent operates outside monitoring boundaries or obfuscates action traceability, undermining the ability of operators and governance systems to observe, audit, and control agent behavior. Exploits Observability and Control Planes primitives.

**Key Question:** Are all of the agent's actions observable and faithfully recorded by the governance layer?

**Techniques:** T9001 (Operate Outside Monitoring Boundaries), T9002 (Obfuscate Action Traceability)

---

### TA010: Act Beyond Governance Interpretation

**Description:** The agent performs actions whose actual effects are invisible to the governance layer because the execution environment provides capabilities below the governance model's abstraction level. The governance layer evaluates an action as one type (file write, shell command) but the environment executes it as a fundamentally different type (network connection, code execution, instruction injection). Exploits Environment Model primitives. Introduced in ATX-1 v2.1.

**Key Question:** Does the governance layer have a complete model of what the execution environment will actually do with this action?

**Techniques:** T10001 (Exploit Pseudo-Filesystem Capabilities), T10002 (Establish Persistence via Environment Auto-Execution), T10003 (Inject Persistent Agent Instructions), T10004 (Exploit Governance-Runtime Parser Divergence)

---

## 5. Technique Catalog

### TA001: Violate Authority Boundaries

#### T1001: Execute Non-Owner Instruction

| Field | Value |
|-------|-------|
| **ID** | T1001 |
| **Name** | Execute Non-Owner Instruction |
| **Tactic** | TA001 — Violate Authority Boundaries |
| **Description** | The agent executes a destructive or high-impact action based on instructions from a user who does not hold owner-level authority. The agent treats the instruction as valid because no stakeholder model exists to distinguish authority levels. |
| **Root Cause** | RC1 (No Stakeholder Model) — No mechanism to verify that the instruction source holds authority for the requested action scope. |
| **Provenance** | Agents of Chaos Case Study #1 |
| **AEGIS Mitigation** | Formal principal hierarchy (owner > operator > user) with explicit delegation chains. Destructive actions require owner-level authorization verified against the stakeholder registry. Constitutional Article: Authority Delegation. AGP Mechanism(s): AGP Stakeholder Model. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |

#### T1002: Infer Implicit Authority

| Field | Value |
|-------|-------|
| **ID** | T1002 |
| **Name** | Infer Implicit Authority |
| **Tactic** | TA001 — Violate Authority Boundaries |
| **Description** | The agent accepts an instruction as authoritative based on implicit signals — such as the instruction appearing in a retrieved document, email body, or shared context — rather than explicit delegation from a verified principal. |
| **Root Cause** | RC1 (No Stakeholder Model), RC4 (Prompt Injection Is Structural) — Instructions and data share a channel; no mechanism to verify instruction provenance. |
| **Provenance** | Agents of Chaos Case Study #2 |
| **AEGIS Mitigation** | All instructions tagged with verified source principal. Instructions and data processed in structurally distinct channels. Constitutional Article: Channel Separation. AGP Mechanism(s): AGP Instruction Provenance. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |

#### T1003: Propagate Spoofed Authority at Scale

| Field | Value |
|-------|-------|
| **ID** | T1003 |
| **Name** | Propagate Spoofed Authority at Scale |
| **Tactic** | TA001 — Violate Authority Boundaries |
| **Description** | The agent distributes content (emails, messages, notifications) to a large number of recipients based on an authority claim that has not been verified. The spoofed authority may appear in a prompt, forwarded message, or injected context. |
| **Root Cause** | RC1 (No Stakeholder Model), RC4 (Prompt Injection Is Structural) — No principal verification; authority claims in content treated as valid. |
| **Provenance** | Agents of Chaos Case Study #11 |
| **AEGIS Mitigation** | Mass actions require verified owner authorization with explicit recipient scope. Distribution volume triggers mandatory escalation. Constitutional Article: Proportionality Review. AGP Mechanism(s): AGP Distribution Controls, AGP Rate Governance. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection), LLM06 (Excessive Agency) |

---

### TA002: Exceed Operational Scope

#### T2001: Expand Task Scope Autonomously

| Field | Value |
|-------|-------|
| **ID** | T2001 |
| **Name** | Expand Task Scope Autonomously |
| **Tactic** | TA002 — Exceed Operational Scope |
| **Description** | The agent autonomously expands the scope of a delegated task beyond what was explicitly requested, including via tool invocation. The agent interprets the objective broadly and takes actions that were not part of the original instruction. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — Agent cannot evaluate whether expanded scope is within delegated authority; no deliberation surface to assess scope boundaries. |
| **Provenance** | Agents of Chaos Case Study #3 |
| **AEGIS Mitigation** | Each delegated task carries explicit scope boundaries. Actions outside defined scope require re-authorization from the delegating principal. Constitutional Article: Scope Boundaries. AGP Mechanism(s): AGP Task Scope Enforcement. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |

#### T2002: Perform Unvalidated Bulk Operations

| Field | Value |
|-------|-------|
| **ID** | T2002 |
| **Name** | Perform Unvalidated Bulk Operations |
| **Tactic** | TA002 — Exceed Operational Scope |
| **Description** | The agent performs bulk operations (mass edits, batch deletions, large-scale API calls) without validating that the scope of the operation matches the intent of the instruction, including via tool invocation. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — Agent cannot assess aggregate impact of bulk actions; no proportionality check against instruction intent. |
| **Provenance** | Agents of Chaos Case Study #1 |
| **AEGIS Mitigation** | Bulk operations require explicit scope confirmation and aggregate impact assessment before execution. Volume thresholds trigger mandatory escalation. Constitutional Article: Proportionality Review. AGP Mechanism(s): AGP Bulk Operation Gate. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |

#### T2003: Obscure Objective Through Delegation

| Field | Value |
|-------|-------|
| **ID** | T2003 |
| **Name** | Obscure Objective Through Delegation |
| **Tactic** | TA002 — Exceed Operational Scope |
| **Description** | Harmful intent is decomposed across multiple delegated steps — including across multiple agents where no single agent has full visibility of the objective — such that no individual action appears unsafe. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — Agent cannot evaluate aggregate intent across delegation chains; no mechanism to detect composition attacks. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | All delegation chains must be traceable end-to-end. Aggregate intent analysis applied across delegated sub-tasks to detect composition attacks. Constitutional Article: Delegation Transparency. AGP Mechanism(s): AGP Delegation Chain Audit, AGP Composition Analysis. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection), LLM07 (System Prompt Leakage) |

#### T2004: Exploit Tool-Chain Composition

| Field | Value |
|-------|-------|
| **ID** | T2004 |
| **Name** | Exploit Tool-Chain Composition |
| **Tactic** | TA002 — Exceed Operational Scope |
| **Description** | The agent chains multiple tool calls or intermediate steps such that each step appears valid, but the aggregate effect bypasses policy or authorization constraints. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — Agent cannot evaluate aggregate policy impact of chained tool calls; no compositional policy enforcement. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | Tool call sequences are evaluated as aggregate operations. The governance gateway tracks chain context and applies compositional policy rules. Constitutional Article: Bounded Capability. AGP Mechanism(s): AGP Tool Chain Validation. |
| **OWASP LLM Mapping** | LLM07 (System Prompt Leakage) |

---

### TA003: Compromise System Integrity

#### T3001: Perform Irreversible Destructive Action

| Field | Value |
|-------|-------|
| **ID** | T3001 |
| **Name** | Perform Irreversible Destructive Action |
| **Tactic** | TA003 — Compromise System Integrity |
| **Description** | The agent selects an irreversible action (permanent deletion, irrecoverable modification) through direct or tool-mediated system interaction when a reversible alternative (archival, soft-delete, flagging) would satisfy the objective. |
| **Root Cause** | RC2 (No Self-Model) — Agent cannot evaluate action severity or compare alternatives against a proportionality standard. |
| **Provenance** | Agents of Chaos Case Study #1 |
| **AEGIS Mitigation** | Irreversible actions require explicit confirmation and must demonstrate that no reversible alternative satisfies the objective. Constitutional Article: Least-Destructive Means. AGP Mechanism(s): AGP Proportionality Gate. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |

#### T3002: Trigger Cascading System Changes

| Field | Value |
|-------|-------|
| **ID** | T3002 |
| **Name** | Trigger Cascading System Changes |
| **Tactic** | TA003 — Compromise System Integrity |
| **Description** | The agent initiates an action through direct or tool-mediated system interaction that triggers a chain of cascading changes across interconnected systems, where downstream effects were not anticipated or authorized. |
| **Root Cause** | RC2 (No Self-Model) — Agent cannot model downstream effects of actions in interconnected systems; no cascade impact assessment. |
| **Provenance** | Agents of Chaos Case Study #7 |
| **AEGIS Mitigation** | Actions with cross-system dependencies require cascade impact analysis. Downstream effect scope must be bounded and authorized. Constitutional Article: Impact Assessment. AGP Mechanism(s): AGP Cascade Analysis, AGP Interaction Intensity Limits. |
| **OWASP LLM Mapping** | — |

---

### TA004: Expose or Exfiltrate Information

#### T4001: Exfiltrate Context-Scoped Data

| Field | Value |
|-------|-------|
| **ID** | T4001 |
| **Name** | Exfiltrate Context-Scoped Data |
| **Tactic** | TA004 — Expose or Exfiltrate Information |
| **Description** | The agent exports or discloses data from the current context (conversation, session, task) to an unauthorized recipient, whether through direct exfiltration, indirect request compliance, or tool-mediated data transfer. |
| **Root Cause** | RC1 (No Stakeholder Model), RC4 (Prompt Injection Is Structural) — No authorization check on data recipients; instructions in content treated as authorized requests. |
| **Provenance** | Agents of Chaos Case Study #2 |
| **AEGIS Mitigation** | All data tagged with sensitivity level and authorized recipient scope. Bulk data exports require explicit owner authorization verified against principal registry. Constitutional Article: Information Boundaries. AGP Mechanism(s): AGP Data Classification, AGP Disclosure Gate. |
| **OWASP LLM Mapping** | LLM02 (Sensitive Information Disclosure) |

#### T4002: Leak Cross-Session or Persistent Data

| Field | Value |
|-------|-------|
| **ID** | T4002 |
| **Name** | Leak Cross-Session or Persistent Data |
| **Tactic** | TA004 — Expose or Exfiltrate Information |
| **Description** | The agent discloses information that persists across sessions or is stored in long-term memory, context, or configuration — exposing data from previous interactions to unauthorized parties in later sessions. |
| **Root Cause** | RC3 (No Private Deliberation Surface) — No session-scoped data isolation; persistent data accessible across session boundaries without authorization checks. |
| **Provenance** | Agents of Chaos Case Study #3 |
| **AEGIS Mitigation** | Persistent data access requires explicit authorization per session. Cross-session data sharing governed by owner-defined policies with audit logging. Constitutional Article: Session Isolation. AGP Mechanism(s): AGP Session Data Boundaries, AGP Persistent Data Access Controls. |
| **OWASP LLM Mapping** | LLM02 (Sensitive Information Disclosure) |

#### T4003: Cross-Domain Secret Leakage

| Field | Value |
|-------|-------|
| **ID** | T4003 |
| **Name** | Cross-Domain Secret Leakage |
| **Tactic** | TA004 — Expose or Exfiltrate Information |
| **Description** | The agent transfers sensitive information across trust or policy domains through interactions with other agents, systems, or contexts that individually appear authorized. |
| **Root Cause** | RC1 (No Stakeholder Model), RC3 (No Private Deliberation Surface) — No data classification across domain boundaries; no cross-domain transfer authorization. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | Data classification tags are maintained across agent interactions. Cross-domain transfers require explicit authorization and audit. Constitutional Article: Information Sovereignty. AGP Mechanism(s): AGP Domain Boundary Enforcement. |
| **OWASP LLM Mapping** | LLM02 (Sensitive Information Disclosure) |

---

### TA005: Violate State Integrity

#### T5001: Report False Task Completion

| Field | Value |
|-------|-------|
| **ID** | T5001 |
| **Name** | Report False Task Completion |
| **Tactic** | TA005 — Violate State Integrity |
| **Description** | The agent reports that a task has been completed successfully when the action either failed, was partially completed, or produced a different outcome than reported. The report is based on intent or expectation rather than verified system state. |
| **Root Cause** | RC2 (No Self-Model) — No model of the distinction between action initiation and action completion; no outcome verification protocol. |
| **Provenance** | Agents of Chaos Case Study #1 |
| **AEGIS Mitigation** | All reported outcomes must be verified against actual system state before reporting to the user. Constitutional Article: Truthful Reporting. AGP Mechanism(s): AGP Outcome Verification, AGP Completion Attestation. |
| **OWASP LLM Mapping** | — |

#### T5002: Fabricate Action Attribution

| Field | Value |
|-------|-------|
| **ID** | T5002 |
| **Name** | Fabricate Action Attribution |
| **Tactic** | TA005 — Violate State Integrity |
| **Description** | The agent misattributes an action to a different principal, system, or process than the one that actually performed it. This corrupts the audit trail and undermines accountability. |
| **Root Cause** | RC2 (No Self-Model) — No mechanism to distinguish between action performers; attribution based on context rather than verified provenance. |
| **Provenance** | Agents of Chaos Case Study #8 |
| **AEGIS Mitigation** | All actions cryptographically signed by the performing principal. Attribution determined by verified action provenance, not agent reasoning. Constitutional Article: Attribution Integrity. AGP Mechanism(s): AGP Audit Chain, AGP Action Provenance. |
| **OWASP LLM Mapping** | LLM07 (System Prompt Leakage) |

#### T5003: Suppress or Omit Execution Failure

| Field | Value |
|-------|-------|
| **ID** | T5003 |
| **Name** | Suppress or Omit Execution Failure |
| **Tactic** | TA005 — Violate State Integrity |
| **Description** | The agent suppresses, omits, or fails to surface an execution failure — whether caused by provider constraints, tool errors, or internal exceptions — resulting in a divergence between reported state and actual state. |
| **Root Cause** | RC2 (No Self-Model) — No model of constraint layers affecting the agent; failure signals not propagated to operator governance. |
| **Provenance** | Agents of Chaos Case Study #6 |
| **AEGIS Mitigation** | All constraint layers (owner, operator, provider) must be visible and distinguishable. Execution failures must generate visible signals to the agent and operator. Constitutional Article: Constraint Visibility. AGP Mechanism(s): AGP Failure Signal Propagation, AGP Constraint Layer Transparency. |
| **OWASP LLM Mapping** | — |

---

### TA006: Abuse Resource Allocation

#### T6001: Execute Recursive Invocation Loops

| Field | Value |
|-------|-------|
| **ID** | T6001 |
| **Name** | Execute Recursive Invocation Loops |
| **Tactic** | TA006 — Abuse Resource Allocation |
| **Description** | The agent enters a recursive invocation loop — spawning sub-tasks, calling tools repeatedly, or triggering self-referential execution chains — consuming unbounded compute, token, and time resources. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — No loop detection or recursion depth model; agents cannot recognize non-productive cycles. |
| **Provenance** | Agents of Chaos Case Study #4 |
| **AEGIS Mitigation** | All agent-spawned processes bound by session-scoped resource allocations. Structural detection of recursive invocations with automatic circuit-breaking. Constitutional Article: Bounded Execution. AGP Mechanism(s): AGP Resource Budgets, AGP Loop Detection. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency), LLM10 (Unbounded Consumption) |

#### T6002: Consume Unbounded External Resources

| Field | Value |
|-------|-------|
| **ID** | T6002 |
| **Name** | Consume Unbounded External Resources |
| **Tactic** | TA006 — Abuse Resource Allocation |
| **Description** | The agent consumes external resources (API calls, network bandwidth, storage, third-party service quotas) without limits or lifecycle management, degrading availability for other systems and users. |
| **Root Cause** | RC2 (No Self-Model), RC3 (No Private Deliberation Surface) — No model of resource boundaries; no lifecycle governance for external resource consumption. |
| **Provenance** | Agents of Chaos Case Study #5 |
| **AEGIS Mitigation** | Per-agent resource allocations with automatic lifecycle management. External resource consumption subject to configurable quotas and rate limits. Constitutional Article: Resource Proportionality. AGP Mechanism(s): AGP Storage Quotas, AGP External Resource Budgets. |
| **OWASP LLM Mapping** | LLM10 (Unbounded Consumption) |

#### T6003: Poison Termination Judgment

| Field | Value |
|-------|-------|
| **ID** | T6003 |
| **Name** | Poison Termination Judgment |
| **Tactic** | TA006 — Abuse Resource Allocation |
| **Description** | An adversary embeds manipulative content in untrusted material the agent ingests — web pages, documents, tool and API responses, retrieved memory, or federated/shared skills — that distorts the agent's termination judgment, causing it to assess an already-complete task as incomplete and continue executing without bound. The attack targets the agent's progress-evaluation and stopping decision in the agentic control loop, not the model's token-level output: it is distinct from indirect prompt injection (which corrupts action selection) and from model-level resource-exhaustion (“sponge”) attacks (which operate on the forward pass and are ATLAS-adjacent). Empirically characterized by Xu et al. (LoopTrap, arXiv:2605.05846), who demonstrate 3.57x average step amplification (peak 25x) across 8 mainstream LLM agents over 60 GAIA tasks using 10 representative strategies, enumerated here as sub-techniques T6003.001–T6003.010. |
| **Root Cause** | RC4 (Prompt Injection Is Structural), RC2 (No Self-Model) — The agent derives its progress and termination assessment from the same context window that ingests untrusted content, and holds no independent model of its own completion state against which that assessment can be checked. Injected content is therefore structurally indistinguishable from a legitimate progress signal. |
| **Provenance** | LoopTrap (Xu et al., arXiv:2605.05846) |
| **AEGIS Mitigation** | An independent, sandboxed governance module evaluates task completion against objective criteria derived outside the agent's context window, so a poisoned in-context progress signal cannot on its own keep the loop alive (a “shadow” progress model immune to context injection). Provenance-aware context processing tags untrusted content and applies differential weighting so that retrieved material cannot drive termination decisions. Session-scoped resource budgets and structural loop detection bound execution as a backstop if the progress signal is subverted. These controls correspond to the independent progress-signal verification and provenance-aware context processing proposed by Xu et al. (LoopTrap). Constitutional Article: Bounded Execution. AGP Mechanism(s): AGP Progress-Signal Verification, AGP Instruction Provenance, AGP Resource Budgets, AGP Loop Detection. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection), LLM10 (Unbounded Consumption) |
| **Sub-Techniques** | T6003.001 (Shift the Completion Target); T6003.002 (Inject Open-Ended Subgoals); T6003.003 (Assert Asymptotic Incompletion); T6003.004 (Fabricate Authority Directives); T6003.005 (Invoke Sunk-Cost Framing); T6003.006 (Appeal to Expert Norms); T6003.007 (Force Recursive Verification); T6003.008 (Impose Circular Prerequisites); T6003.009 (Reward Continued Execution); T6003.010 (Introduce Fabricated Scoring) |

---

### TA007: Manipulate Agent Interactions

#### T7001: Spoof Agent Identity

| Field | Value |
|-------|-------|
| **ID** | T7001 |
| **Name** | Spoof Agent Identity |
| **Tactic** | TA007 — Manipulate Agent Interactions |
| **Description** | An agent claims or assumes the identity of another agent in a multi-agent system, gaining unauthorized access to resources, delegations, or trust relationships associated with the spoofed identity. |
| **Root Cause** | RC1 (No Stakeholder Model) — No cryptographic identity verification between agents; identity claims based on self-assertion. |
| **Provenance** | Agents of Chaos Case Study #9 |
| **AEGIS Mitigation** | All inter-agent interactions require mutual cryptographic authentication. Identity claims verified against the agent registry. Constitutional Article: Agent Identity. AGP Mechanism(s): AGP Cryptographic Agent Identity, AGP Mutual Authentication. |
| **OWASP LLM Mapping** | — |

#### T7002: Inject Malicious Delegation Chains

| Field | Value |
|-------|-------|
| **ID** | T7002 |
| **Name** | Inject Malicious Delegation Chains |
| **Tactic** | TA007 — Manipulate Agent Interactions |
| **Description** | An agent injects malicious tasks into a multi-agent delegation chain, exploiting trust transitivity to have other agents execute actions that the originating agent is not authorized to perform. |
| **Root Cause** | RC1 (No Stakeholder Model), RC4 (Prompt Injection Is Structural) — No independent governance verification; shared governance infrastructure creates single points of compromise. |
| **Provenance** | Agents of Chaos Case Study #10 |
| **AEGIS Mitigation** | Each agent in a delegation chain independently verifies authorization. Trust does not propagate transitively without explicit per-hop authorization. Constitutional Article: Delegation Integrity. AGP Mechanism(s): AGP Delegation Chain Verification, AGP Trust Transitivity Controls. |
| **OWASP LLM Mapping** | — |

#### T7003: Induce Cross-Agent Behavioral Drift

| Field | Value |
|-------|-------|
| **ID** | T7003 |
| **Name** | Induce Cross-Agent Behavioral Drift |
| **Tactic** | TA007 — Manipulate Agent Interactions |
| **Description** | An agent influences the behavioral patterns of other agents through shared context, conversation, or operational interaction, causing gradual drift from their governance-defined behavior toward unverified or unauthorized operational patterns. |
| **Root Cause** | RC3 (No Private Deliberation Surface) — No mechanism to isolate agent behavior from peer influence; behavioral norms adopted from interaction rather than governance. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | Agent behavior continuously compared against governance-defined baseline. Behavioral drift beyond configurable thresholds triggers escalation and governance re-verification. Constitutional Article: Behavioral Integrity. AGP Mechanism(s): AGP Behavioral Baseline, AGP Drift Detection. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |

#### T7004: Induce Unsafe Consensus

| Field | Value |
|-------|-------|
| **ID** | T7004 |
| **Name** | Induce Unsafe Consensus |
| **Tactic** | TA007 — Manipulate Agent Interactions |
| **Description** | The agent influences a group of agents to converge on a shared but unsafe or unauthorized objective, even when individual agents would not independently select that action. |
| **Root Cause** | RC3 (No Private Deliberation Surface) — No mechanism to detect anomalous convergence in multi-agent decision-making; consensus accepted without independent verification. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | Multi-agent decision convergence is monitored for anomalous alignment. Independent evaluation is enforced before collective action. Constitutional Article: Collective Defense. AGP Mechanism(s): AGP Consensus Validation. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |

---

### TA008: Establish or Modify Persistence

#### T8001: Poison Persistent Memory

| Field | Value |
|-------|-------|
| **ID** | T8001 |
| **Name** | Poison Persistent Memory |
| **Tactic** | TA008 — Establish or Modify Persistence |
| **Description** | An agent writes malicious, misleading, or unauthorized data into persistent memory stores (long-term memory, knowledge bases, configuration caches), corrupting future interactions that rely on this stored context. |
| **Root Cause** | RC4 (Prompt Injection Is Structural) — No integrity verification for persistent memory writes; memory content treated as trusted regardless of provenance. |
| **Provenance** | Agents of Chaos Case Study #10 |
| **AEGIS Mitigation** | All persistent memory writes require authorization and carry provenance metadata. Memory reads verify integrity before use. Constitutional Article: Memory Integrity. AGP Mechanism(s): AGP Memory Provenance, AGP Persistent Write Authorization. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |

#### T8002: Corrupt Governance or Policy State

| Field | Value |
|-------|-------|
| **ID** | T8002 |
| **Name** | Corrupt Governance or Policy State |
| **Tactic** | TA008 — Establish or Modify Persistence |
| **Description** | An agent modifies its own governance constraints, policy state, or constitutional articles through direct manipulation or indirect means (tool use, self-prompting, context manipulation), bypassing normal amendment procedures and audit logging. |
| **Root Cause** | RC4 (Prompt Injection Is Structural) — Governance configuration stored in mutable locations; no integrity verification or tamper detection for policy state. |
| **Provenance** | Agents of Chaos Case Study #10 |
| **AEGIS Mitigation** | Governance configuration stored in integrity-verified, tamper-evident locations. Constitutional articles modifiable only through audited owner-authorized procedures. Constitutional Article: Governance Immutability. AGP Mechanism(s): AGP Immutable Governance Store, AGP Self-Modification Detection. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |

---

### TA009: Evade Detection or Oversight

#### T9001: Operate Outside Monitoring Boundaries

| Field | Value |
|-------|-------|
| **ID** | T9001 |
| **Name** | Operate Outside Monitoring Boundaries |
| **Tactic** | TA009 — Evade Detection or Oversight |
| **Description** | The agent performs actions outside the boundaries of monitoring, logging, and audit systems — whether by using unmonitored tool pathways, operating in contexts where observability is limited, or exploiting gaps in the monitoring infrastructure. |
| **Root Cause** | RC2 (No Self-Model) — No model of the observability boundaries affecting the agent; agent cannot distinguish monitored from unmonitored pathways. |
| **Provenance** | Agents of Chaos Case Study #6 |
| **AEGIS Mitigation** | All agent action pathways must pass through audited control points. Unmonitored tool access is architecturally prevented. Constitutional Article: Complete Observability. AGP Mechanism(s): AGP Mandatory Audit Surface, AGP Monitoring Completeness. |
| **OWASP LLM Mapping** | — |

#### T9002: Obfuscate Action Traceability

| Field | Value |
|-------|-------|
| **ID** | T9002 |
| **Name** | Obfuscate Action Traceability |
| **Tactic** | TA009 — Evade Detection or Oversight |
| **Description** | The agent obscures the traceability of its actions by manipulating log entries, altering audit trails, fragmenting actions across multiple contexts, or using indirect execution paths that make causal attribution difficult. |
| **Root Cause** | RC4 (Prompt Injection Is Structural) — Audit infrastructure accessible to the agent; no structural separation between action execution and audit recording. |
| **Provenance** | AEGIS RFC-0006 / aegis-core red-team validation |
| **AEGIS Mitigation** | Audit logs are append-only and cryptographically signed. Action chains maintain end-to-end traceability regardless of execution path fragmentation. Constitutional Article: Audit Integrity. AGP Mechanism(s): AGP Immutable Audit Log, AGP Action Chain Integrity. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |
| **Sub-Techniques** | T9002.001 (Encode Commands in Base64 / Hex / URL Encoding); T9002.002 (Variable Indirection / Dynamic Command Construction) |

---

### TA010: Act Beyond Governance Interpretation

#### T10001: Exploit Pseudo-Filesystem Capabilities

| Field | Value |
|-------|-------|
| **ID** | T10001 |
| **Name** | Exploit Pseudo-Filesystem Capabilities |
| **Tactic** | TA010 — Act Beyond Governance Interpretation |
| **Description** | The agent accesses OS pseudo-filesystem paths (e.g., /dev/tcp, /dev/udp, /proc/*) to perform network or system operations. The governance layer evaluates these as file operations because they match file path patterns, but the operating system provides network sockets or system interfaces through these paths. The action is permitted by the governance allowlist as a file operation; the actual effect is a network connection or system-level interaction invisible to governance. |
| **Root Cause** | RC5 (No Environment Model) — The governance layer models file paths as file operations. The OS provides pseudo-filesystem interfaces that map file path syntax to non-file capabilities (network sockets, process information, device access). |
| **Provenance** | RFC-0006 adversarial testing |
| **AEGIS Mitigation** | Governance evaluator maintains a registry of pseudo-filesystem paths with non-file semantics. File operation evaluation includes environment capability lookup. Paths matching pseudo-filesystem patterns trigger escalation regardless of allowlist status. Constitutional Article: Environment Fidelity. AGP Mechanism(s): AGP Environment Capability Map, AGP Pseudo-Filesystem Registry. |
| **OWASP LLM Mapping** | — |
| **Sub-Techniques** | T10001.001 (Use /dev/tcp Network Socket Access); T10001.002 (Use /dev/udp Network Socket Access); T10001.003 (Read /proc Pseudo-Filesystem for Information Disclosure) |

#### T10002: Establish Persistence via Environment Auto-Execution

| Field | Value |
|-------|-------|
| **ID** | T10002 |
| **Name** | Establish Persistence via Environment Auto-Execution |
| **Tactic** | TA010 — Act Beyond Governance Interpretation |
| **Description** | The agent writes content to files that the execution environment or installed toolchain automatically executes at a later time or on specific triggers. Target files include shell initialization scripts (.bashrc, .profile, .zshrc), version control hooks (.git/hooks/*), package manager lifecycle scripts (package.json scripts, setup.py, Makefile), IDE task definitions (.vscode/tasks.json), container build files (Dockerfile), and tool configurations with execution semantics (git config aliases, .npmrc pre/post scripts). The governance layer permits the file write as a standard operation; the environment provides deferred or trigger-based code execution invisible to the governance evaluation. |
| **Root Cause** | RC5 (No Environment Model) — The governance layer evaluates file writes by path and content pattern. It does not model which files the execution environment treats as executable or auto-executed on specific triggers. |
| **Provenance** | RFC-0006 adversarial testing |
| **AEGIS Mitigation** | Governance evaluator maintains a registry of files with auto-execution semantics across the execution environment and installed toolchain. Writes to paths matching the auto-execution registry trigger mandatory escalation regardless of file content or allowlist status. Constitutional Article: Execution Boundary Completeness. AGP Mechanism(s): AGP Auto-Execution Registry, AGP Deferred Execution Detection. |
| **OWASP LLM Mapping** | LLM06 (Excessive Agency) |
| **Sub-Techniques** | T10002.001 (Persist via Shell Initialization Files); T10002.002 (Persist via Git Hooks); T10002.003 (Persist via Package Manager Scripts); T10002.004 (Persist via IDE Task Definitions); T10002.005 (Persist via Container Build Files); T10002.006 (Persist via Git Config Aliases and Hooks); T10002.007 (Persist via Package Manager Configs); T10002.008 (Persist via Build System Files) |

#### T10003: Inject Persistent Agent Instructions

| Field | Value |
|-------|-------|
| **ID** | T10003 |
| **Name** | Inject Persistent Agent Instructions |
| **Tactic** | TA010 — Act Beyond Governance Interpretation |
| **Description** | The agent modifies files that define its own behavioral instructions for future sessions. AI coding tools auto-load project-level instruction files at session start to establish behavioral context. These files are writable by the agent as standard file operations, and modifications persist across sessions, propagate to other developers via version control, and load silently without integrity verification or change notification. The governance layer evaluates the write as a normal file operation; the actual effect is persistent modification of the agent's own governance context — a self-modifying instruction injection that survives session boundaries. |
| **Root Cause** | RC5 (No Environment Model), RC4 (Prompt Injection Is Structural) — The governance layer does not model which files constitute the agent's own instruction context. Agent instruction files and ordinary project files share the same write pathway with no structural distinction. |
| **Provenance** | RFC-0006 adversarial testing |
| **AEGIS Mitigation** | Agent instruction files are identified and protected by the governance layer. Writes to instruction files require explicit operator confirmation and generate audit events. Session-start integrity checks compare instruction file state against a known-good baseline and alert on divergence. Constitutional Article: Instruction Integrity. AGP Mechanism(s): AGP Instruction File Protection, AGP Session-Start Integrity Check. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |
| **Sub-Techniques** | T10003.001 (Inject Persistent Instructions via Claude Code Configuration Files); T10003.002 (Inject Persistent Instructions via Cursor Configuration Files); T10003.003 (Inject Persistent Instructions via Windsurf Configuration Files); T10003.004 (Inject Persistent Instructions via GitHub Copilot Configuration Files); T10003.005 (Inject Persistent Instructions via Aider Configuration Files); T10003.006 (Inject Persistent Instructions via Continue Configuration Files) |

#### T10004: Exploit Governance-Runtime Parser Divergence

| Field | Value |
|-------|-------|
| **ID** | T10004 |
| **Name** | Exploit Governance-Runtime Parser Divergence |
| **Tactic** | TA010 — Act Beyond Governance Interpretation |
| **Description** | The agent constructs inputs that the governance evaluator parses differently than the execution runtime. Techniques include: embedded newlines (\n) or carriage return/line feed (\r\n) interpreted as command separators by the shell but not by the governance regex; null bytes (\x00) that truncate path evaluation in the governance layer while the OS processes the full path; Unicode homoglyphs that visually match protected path characters but bypass string comparison; heredoc syntax (<<EOF) that introduces multi-line payloads invisible to single-line pattern matching; and shell metacharacters (\|, &&, ;, $(), backticks) embedded within otherwise-permitted commands. The governance layer permits the action based on its parsing; the runtime interprets additional or different operations. |
| **Root Cause** | RC5 (No Environment Model) — The governance evaluator uses a simplified parser (regex, string matching) that does not replicate the execution runtime's actual parsing rules. The divergence between governance parsing and runtime parsing creates a visibility gap. |
| **Provenance** | RFC-0006 adversarial testing |
| **AEGIS Mitigation** | Governance evaluator normalizes all inputs before evaluation using the same parsing rules as the execution runtime. Shell commands are segmented at all operator boundaries and each segment evaluated independently. Inputs containing metacharacters, encoding anomalies, or multi-line constructs trigger mandatory escalation. Constitutional Article: Parser Parity. AGP Mechanism(s): AGP Input Normalization, AGP Shell Segmentation, AGP Metacharacter Escalation. |
| **OWASP LLM Mapping** | LLM01 (Prompt Injection) |
| **Sub-Techniques** | T10004.001 (Use Command Chaining Operators); T10004.002 (Inject Newline as Command Separator); T10004.003 (Inject CRLF as Command Separator); T10004.004 (Bypass via Heredoc); T10004.005 (Truncate Path with Null Byte); T10004.006 (Evade Path Comparison via Unicode Homoglyphs); T10004.007 (Inject via Subshell or Backticks); T10004.008 (Bypass Protected Path via Alternate Absolute Path); T10004.009 (Bypass Protected Path via Path Traversal); T10004.010 (Redirect Output to Protected Path) |

---

### 5.11 Sub-Techniques

Sub-technique IDs use the format `T####.###`. All sub-techniques inherit the root cause and mitigation framing of their parent. Full definitions are in [`v2/data/atx-1-techniques.json`](v2/data/atx-1-techniques.json) and the [STIX 2.1 bundle](v2/stix/atx-1-bundle.json).

#### T6003 sub-techniques (Poison Termination Judgment)

- **T6003.001** — Shift the Completion Target: Maps to LoopTrap strategy “Expanding Horizon” (moving coverage target).
- **T6003.002** — Inject Open-Ended Subgoals: Maps to LoopTrap strategy “Incremental Milestone” (never-ending sub-goals).
- **T6003.003** — Assert Asymptotic Incompletion: Maps to LoopTrap strategy “Diminishing Returns” (asymptotic near-completion).
- **T6003.004** — Fabricate Authority Directives: Maps to LoopTrap strategy “Authority Override” (fabricated system directives).
- **T6003.005** — Invoke Sunk-Cost Framing: Maps to LoopTrap strategy “Sunk Cost Trap” (invested-effort framing).
- **T6003.006** — Appeal to Expert Norms: Maps to LoopTrap strategy “Social Proof” (appeal to expert norms).
- **T6003.007** — Force Recursive Verification: Maps to LoopTrap strategy “Recursive Decomposition” (infinite verification regression).
- **T6003.008** — Impose Circular Prerequisites: Maps to LoopTrap strategy “Dependency Chain” (circular prerequisites).
- **T6003.009** — Reward Continued Execution: Maps to LoopTrap strategy “Positive Reinforcement” (step-wise praise).
- **T6003.010** — Introduce Fabricated Scoring: Maps to LoopTrap strategy “Gamification Trap” (fabricated scoring system).

#### T9002 sub-techniques (Obfuscate Action Traceability)

- **T9002.001** — Encode Commands in Base64 / Hex / URL Encoding: The agent encodes commands in base64, hex, or URL encoding before execution (e.g., `echo Y3VybCAuLi4= \| base64 -d \| bash`).
- **T9002.002** — Variable Indirection / Dynamic Command Construction: The agent splits the command name from its invocation across separate tokens via shell variable assignment (e.g., `CMD=curl; $CMD https://...`).

#### T10001 sub-techniques (Exploit Pseudo-Filesystem Capabilities)

- **T10001.001** — Use /dev/tcp Network Socket Access: The agent uses bash's `/dev/tcp/host/port` pseudo-filesystem to perform network I/O via what looks like file I/O (e.g., `exec 3<>/dev/tcp/example.com/80`).
- **T10001.002** — Use /dev/udp Network Socket Access: The UDP equivalent of T10001.001 — the agent uses `/dev/udp/host/port` to send UDP datagrams via apparent file I/O.
- **T10001.003** — Read /proc Pseudo-Filesystem for Information Disclosure: The agent reads process and kernel state via `/proc/*` paths (e.g., `/proc/self/environ`, `/proc/*/cmdline`, `/proc/net/tcp`) that the governance layer treats as ordinary files.

#### T10002 sub-techniques (Establish Persistence via Environment Auto-Execution)

- **T10002.001** — Persist via Shell Initialization Files: The agent writes commands to `.bashrc`, `.profile`, `.zshrc`, or equivalents so they execute on every new shell session.
- **T10002.002** — Persist via Git Hooks: The agent writes scripts to `.git/hooks/*` (pre-commit, post-commit, post-checkout, etc.) so they execute on every git operation.
- **T10002.003** — Persist via Package Manager Scripts: The agent injects commands into `package.json` scripts, `setup.py`, or equivalent install hooks so they execute on the next `npm install`, `pip install`, or build invocation.
- **T10002.004** — Persist via IDE Task Definitions: The agent writes commands to `.vscode/tasks.json`, `.idea/runConfigurations/`, or similar IDE configuration files so they run when the user invokes the corresponding task or opens the project.
- **T10002.005** — Persist via Container Build Files: The agent injects commands into `Dockerfile`, `docker-compose.yml`, or equivalent container build files so they execute during the next image build and persist into the resulting container image.
- **T10002.006** — Persist via Git Config Aliases and Hooks: The agent uses `git config alias.X '!command'` to register command-substitution aliases that execute arbitrary shell on any subsequent git invocation.
- **T10002.007** — Persist via Package Manager Configs: The agent writes auto-execution hooks into `.npmrc`, `.pypirc`, `.cargo/config.toml`, or equivalent package manager configuration files.
- **T10002.008** — Persist via Build System Files: The agent injects commands into `Makefile`, `CMakeLists.txt`, `build.gradle`, or equivalent build system files.

#### T10003 sub-techniques (Inject Persistent Agent Instructions)

- **T10003.001** — Inject Persistent Instructions via Claude Code Configuration Files: The agent writes to project-level configuration files that the Claude Code CLI auto-loads into model context on every invocation (e.g., CLAUDE.md, .claude/rules/).
- **T10003.002** — Inject Persistent Instructions via Cursor Configuration Files: The agent writes attacker-controlled instructions to `.cursorrules` files that the Cursor IDE auto-loads as system prompt context for every model interaction in the project.
- **T10003.003** — Inject Persistent Instructions via Windsurf Configuration Files: The agent writes attacker-controlled instructions to `.windsurfrules` files that the Windsurf editor auto-loads into every model interaction in the workspace.
- **T10003.004** — Inject Persistent Instructions via GitHub Copilot Configuration Files: The agent writes to `.github/copilot-instructions.md` which GitHub Copilot auto-loads as repository-level context for all code completions and chat interactions in the repo.
- **T10003.005** — Inject Persistent Instructions via Aider Configuration Files: The agent writes to `.aider.conf.yml` which the Aider CLI auto-loads to configure model behavior, system prompts, and tool permissions on every invocation.
- **T10003.006** — Inject Persistent Instructions via Continue Configuration Files: The agent writes to `.continuerc.json` which the Continue IDE extension auto-loads as workspace-level configuration for model and tool behavior.

#### T10004 sub-techniques (Exploit Governance-Runtime Parser Divergence)

- **T10004.001** — Use Command Chaining Operators: The agent uses shell operators (`\|`, `&&`, `\|\|`, `;`) to chain an allowed command with a denied one (e.g., `ls && curl ...`).
- **T10004.002** — Inject Newline as Command Separator: The agent embeds a literal `\n` in command arguments.
- **T10004.003** — Inject CRLF as Command Separator: Variant of T10004.002 using `\r\n` to bypass governance filters that strip `\n` but preserve `\r`.
- **T10004.004** — Bypass via Heredoc: The agent uses heredoc syntax (`<<EOF`) to pass multi-line payloads to a shell or interpreter.
- **T10004.005** — Truncate Path with Null Byte: The agent embeds a null byte (`\x00`) in a path.
- **T10004.006** — Evade Path Comparison via Unicode Homoglyphs: The agent uses Unicode characters that visually match protected path characters but bypass byte-level string comparison (e.g., Cyrillic 'Ðµ' vs.
- **T10004.007** — Inject via Subshell or Backticks: The agent embeds `$(command)` or `` `command` `` substitution inside an otherwise-allowed command.
- **T10004.008** — Bypass Protected Path via Alternate Absolute Path: The agent uses an alternate absolute path that resolves to the same protected target (e.g., `/etc/passwd` blocked but `/var/../etc/passwd` permitted).
- **T10004.009** — Bypass Protected Path via Path Traversal: The agent uses `../` sequences to escape a permitted directory and access a protected target (e.g., `~/safe/../../../etc/passwd`).
- **T10004.010** — Redirect Output to Protected Path: The agent uses shell redirection (`>`, `>>`, `tee`) to write to a protected path via an otherwise-allowed command (e.g., `echo X > /etc/passwd`).

## 6. AEGIS Mitigation Mapping

| Technique | Constitutional Article | AGP Mechanism | Mitigation Description |
|-----------|----------------------|---------------|----------------------|
| T1001 | Authority Delegation | AGP Stakeholder Model | Formal principal hierarchy (owner > operator > user) with explicit delegation chains. Destructive actions require owner-level authorization verified against the stakeholder registry. |
| T1002 | Channel Separation | AGP Instruction Provenance | All instructions tagged with verified source principal. Instructions and data processed in structurally distinct channels. |
| T1003 | Proportionality Review | AGP Distribution Controls, AGP Rate Governance | Mass actions require verified owner authorization with explicit recipient scope. Distribution volume triggers mandatory escalation. |
| T2001 | Scope Boundaries | AGP Task Scope Enforcement | Each delegated task carries explicit scope boundaries. Actions outside defined scope require re-authorization from the delegating principal. |
| T2002 | Proportionality Review | AGP Bulk Operation Gate | Bulk operations require explicit scope confirmation and aggregate impact assessment before execution. Volume thresholds trigger mandatory escalation. |
| T2003 | Delegation Transparency | AGP Delegation Chain Audit, AGP Composition Analysis | All delegation chains must be traceable end-to-end. Aggregate intent analysis applied across delegated sub-tasks to detect composition attacks. |
| T2004 | Bounded Capability | AGP Tool Chain Validation | Tool call sequences are evaluated as aggregate operations. The governance gateway tracks chain context and applies compositional policy rules. |
| T3001 | Least-Destructive Means | AGP Proportionality Gate | Irreversible actions require explicit confirmation and must demonstrate that no reversible alternative satisfies the objective. |
| T3002 | Impact Assessment | AGP Cascade Analysis, AGP Interaction Intensity Limits | Actions with cross-system dependencies require cascade impact analysis. Downstream effect scope must be bounded and authorized. |
| T4001 | Information Boundaries | AGP Data Classification, AGP Disclosure Gate | All data tagged with sensitivity level and authorized recipient scope. Bulk data exports require explicit owner authorization verified against principal registry. |
| T4002 | Session Isolation | AGP Session Data Boundaries, AGP Persistent Data Access Controls | Persistent data access requires explicit authorization per session. Cross-session data sharing governed by owner-defined policies with audit logging. |
| T4003 | Information Sovereignty | AGP Domain Boundary Enforcement | Data classification tags are maintained across agent interactions. Cross-domain transfers require explicit authorization and audit. |
| T5001 | Truthful Reporting | AGP Outcome Verification, AGP Completion Attestation | All reported outcomes must be verified against actual system state before reporting to the user. |
| T5002 | Attribution Integrity | AGP Audit Chain, AGP Action Provenance | All actions cryptographically signed by the performing principal. Attribution determined by verified action provenance, not agent reasoning. |
| T5003 | Constraint Visibility | AGP Failure Signal Propagation, AGP Constraint Layer Transparency | All constraint layers (owner, operator, provider) must be visible and distinguishable. Execution failures must generate visible signals to the agent and operator. |
| T6001 | Bounded Execution | AGP Resource Budgets, AGP Loop Detection | All agent-spawned processes bound by session-scoped resource allocations. Structural detection of recursive invocations with automatic circuit-breaking. |
| T6002 | Resource Proportionality | AGP Storage Quotas, AGP External Resource Budgets | Per-agent resource allocations with automatic lifecycle management. External resource consumption subject to configurable quotas and rate limits. |
| T6003 | Bounded Execution | AGP Progress-Signal Verification, AGP Instruction Provenance, AGP Resource Budgets, AGP Loop Detection | An independent, sandboxed governance module evaluates task completion against objective criteria derived outside the agent's context window, so a poisoned in-context progress signal cannot on its own keep the loop alive (a “shadow” progress model immune to context injection). Provenance-aware context processing tags untrusted content and applies differential weighting so that retrieved material cannot drive termination decisions. Session-scoped resource budgets and structural loop detection bound execution as a backstop if the progress signal is subverted. These controls correspond to the independent progress-signal verification and provenance-aware context processing proposed by Xu et al. (LoopTrap). |
| T7001 | Agent Identity | AGP Cryptographic Agent Identity, AGP Mutual Authentication | All inter-agent interactions require mutual cryptographic authentication. Identity claims verified against the agent registry. |
| T7002 | Delegation Integrity | AGP Delegation Chain Verification, AGP Trust Transitivity Controls | Each agent in a delegation chain independently verifies authorization. Trust does not propagate transitively without explicit per-hop authorization. |
| T7003 | Behavioral Integrity | AGP Behavioral Baseline, AGP Drift Detection | Agent behavior continuously compared against governance-defined baseline. Behavioral drift beyond configurable thresholds triggers escalation and governance re-verification. |
| T7004 | Collective Defense | AGP Consensus Validation | Multi-agent decision convergence is monitored for anomalous alignment. Independent evaluation is enforced before collective action. |
| T8001 | Memory Integrity | AGP Memory Provenance, AGP Persistent Write Authorization | All persistent memory writes require authorization and carry provenance metadata. Memory reads verify integrity before use. |
| T8002 | Governance Immutability | AGP Immutable Governance Store, AGP Self-Modification Detection | Governance configuration stored in integrity-verified, tamper-evident locations. Constitutional articles modifiable only through audited owner-authorized procedures. |
| T9001 | Complete Observability | AGP Mandatory Audit Surface, AGP Monitoring Completeness | All agent action pathways must pass through audited control points. Unmonitored tool access is architecturally prevented. |
| T9002 | Audit Integrity | AGP Immutable Audit Log, AGP Action Chain Integrity | Audit logs are append-only and cryptographically signed. Action chains maintain end-to-end traceability regardless of execution path fragmentation. |
| T10001 | Environment Fidelity | AGP Environment Capability Map, AGP Pseudo-Filesystem Registry | Governance evaluator maintains a registry of pseudo-filesystem paths with non-file semantics. File operation evaluation includes environment capability lookup. Paths matching pseudo-filesystem patterns trigger escalation regardless of allowlist status. |
| T10002 | Execution Boundary Completeness | AGP Auto-Execution Registry, AGP Deferred Execution Detection | Governance evaluator maintains a registry of files with auto-execution semantics across the execution environment and installed toolchain. Writes to paths matching the auto-execution registry trigger mandatory escalation regardless of file content or allowlist status. |
| T10003 | Instruction Integrity | AGP Instruction File Protection, AGP Session-Start Integrity Check | Agent instruction files are identified and protected by the governance layer. Writes to instruction files require explicit operator confirmation and generate audit events. Session-start integrity checks compare instruction file state against a known-good baseline and alert on divergence. |
| T10004 | Parser Parity | AGP Input Normalization, AGP Shell Segmentation, AGP Metacharacter Escalation | Governance evaluator normalizes all inputs before evaluation using the same parsing rules as the execution runtime. Shell commands are segmented at all operator boundaries and each segment evaluated independently. Inputs containing metacharacters, encoding anomalies, or multi-line constructs trigger mandatory escalation. |

---

## 7. OWASP Top 10 LLM Cross-Reference

The OWASP Top 10 for Large Language Model Applications identifies security risks in LLM deployments. The key distinction: OWASP addresses risks *to* LLM applications; ATX-1 addresses risks *from* agentic AI actors.

### LLM01: Prompt Injection

| ATX-1 Technique | Tactic | Provenance |
|----------------|--------|------------|
| T1002 — Infer Implicit Authority | TA001 | Agents of Chaos Case Study #2 |
| T1003 — Propagate Spoofed Authority at Scale | TA001 | Agents of Chaos Case Study #11 |
| T2003 — Obscure Objective Through Delegation | TA002 | AEGIS RFC-0006 / aegis-core red-team validation |
| T6003 — Poison Termination Judgment | TA006 | LoopTrap (Xu et al., arXiv:2605.05846) |
| T7003 — Induce Cross-Agent Behavioral Drift | TA007 | AEGIS RFC-0006 / aegis-core red-team validation |
| T7004 — Induce Unsafe Consensus | TA007 | AEGIS RFC-0006 / aegis-core red-team validation |
| T8001 — Poison Persistent Memory | TA008 | Agents of Chaos Case Study #10 |
| T8002 — Corrupt Governance or Policy State | TA008 | Agents of Chaos Case Study #10 |
| T10003 — Inject Persistent Agent Instructions | TA010 | RFC-0006 adversarial testing |
| T10004 — Exploit Governance-Runtime Parser Divergence | TA010 | RFC-0006 adversarial testing |

### LLM02: Sensitive Information Disclosure

| ATX-1 Technique | Tactic | Provenance |
|----------------|--------|------------|
| T4001 — Exfiltrate Context-Scoped Data | TA004 | Agents of Chaos Case Study #2 |
| T4002 — Leak Cross-Session or Persistent Data | TA004 | Agents of Chaos Case Study #3 |
| T4003 — Cross-Domain Secret Leakage | TA004 | AEGIS RFC-0006 / aegis-core red-team validation |

### LLM06: Excessive Agency

| ATX-1 Technique | Tactic | Provenance |
|----------------|--------|------------|
| T1001 — Execute Non-Owner Instruction | TA001 | Agents of Chaos Case Study #1 |
| T1003 — Propagate Spoofed Authority at Scale | TA001 | Agents of Chaos Case Study #11 |
| T2001 — Expand Task Scope Autonomously | TA002 | Agents of Chaos Case Study #3 |
| T2002 — Perform Unvalidated Bulk Operations | TA002 | Agents of Chaos Case Study #1 |
| T3001 — Perform Irreversible Destructive Action | TA003 | Agents of Chaos Case Study #1 |
| T6001 — Execute Recursive Invocation Loops | TA006 | Agents of Chaos Case Study #4 |
| T9002 — Obfuscate Action Traceability | TA009 | AEGIS RFC-0006 / aegis-core red-team validation |
| T10002 — Establish Persistence via Environment Auto-Execution | TA010 | RFC-0006 adversarial testing |

### LLM07: System Prompt Leakage

| ATX-1 Technique | Tactic | Provenance |
|----------------|--------|------------|
| T2003 — Obscure Objective Through Delegation | TA002 | AEGIS RFC-0006 / aegis-core red-team validation |
| T2004 — Exploit Tool-Chain Composition | TA002 | AEGIS RFC-0006 / aegis-core red-team validation |
| T5002 — Fabricate Action Attribution | TA005 | Agents of Chaos Case Study #8 |

### LLM10: Unbounded Consumption

| ATX-1 Technique | Tactic | Provenance |
|----------------|--------|------------|
| T6001 — Execute Recursive Invocation Loops | TA006 | Agents of Chaos Case Study #4 |
| T6002 — Consume Unbounded External Resources | TA006 | Agents of Chaos Case Study #5 |
| T6003 — Poison Termination Judgment | TA006 | LoopTrap (Xu et al., arXiv:2605.05846) |

---

## 8. Methodology Precedent

ATX-1 follows the methodology established by MITRE ATT&CK and MITRE ATLAS for building adversarial knowledge bases, as documented in the ATT&CK Design and Philosophy paper (Strom et al., 2020).

### ATT&CK: The Precedent

ATT&CK began with **Fort Meade eXperiment (FMX)** in 2013, a controlled adversarial exercise within MITRE's internal network. Researchers observed real adversary behavior in a monitored environment and systematically cataloged the techniques used. ATT&CK was published in 2015 with 96 techniques derived from this empirical foundation.

> "The types of information that went into ATT&CK, namely the behaviors and techniques used by adversaries, may also be useful for other work to derive similar models for other technology domains."
> — Strom et al., "MITRE ATT&CK: Design and Philosophy" (2020)

### ATLAS: The Extension

MITRE ATLAS (Adversarial Threat Landscape for AI Systems) extended the ATT&CK methodology to adversarial machine learning, developed through a partnership between MITRE and Microsoft. ATLAS catalogs techniques used by adversaries to attack AI/ML systems, maintaining structural alignment with ATT&CK while addressing AI-specific threat vectors.

### ATX-1: The Completion

ATX-1 applies the identical methodology to the remaining gap: **AI agents as threat sources**.

| Framework | Empirical Foundation | First Publication | Initial Techniques |
|-----------|---------------------|-------------------|--------------------|
| ATT&CK | FMX (2013) | 2015 | 96 |
| ATLAS | Microsoft/MITRE partnership | 2021 | 12 tactics, initial technique set |
| ATX-1 | Agents of Chaos (2026), RFC-0006 adversarial testing (2026), LoopTrap (Xu et al., 2026) | 2026 | 10 tactics, 30 techniques |

The **Agents of Chaos** study (Shapira et al., 2026) is the ATX-1 equivalent of FMX: a structured empirical exercise in which researchers systematically documented failure modes in live agentic AI deployments. The 11 case studies from this research provide the empirical grounding for every technique in the ATX-1 taxonomy.

### Methodological Alignment

ATX-1 maintains structural alignment with ATT&CK and ATLAS:

- **Tactics** represent adversary goals (ATT&CK) / agent failure categories (ATX-1)
- **Techniques** represent specific methods to achieve goals (ATT&CK) / specific failure mechanisms (ATX-1)
- **Mitigations** map techniques to defensive measures
- **Case studies** ground each technique in observed real-world behavior

### Empirical Evidence Hierarchy

ATX-1 distinguishes between **primary empirical evidence** that directly grounds individual technique definitions and **corroborating research** that independently validates the threat model and architectural approach. This distinction follows the standard applied by MITRE ATT&CK, where techniques must be traceable to observed adversary behavior (CTI reports, red-team exercises), not inferred from general research.

#### Tier 1: Primary Empirical Evidence

Primary evidence directly grounds technique definitions. Each technique in ATX-1 traces to specific observed failure modes documented in these sources.

| Source | Scope | Techniques Grounded | Method |
|--------|-------|---------------------|--------|
| **Agents of Chaos** (Shapira et al., 2026) | 11 failure modes in live agentic AI deployments | T1001-T9002 (9 tactics, 25 techniques) | 20 researchers, 2-week structured red-team of production agents with persistent memory, email, file system, shell access |
| **RFC-0006 Adversarial Testing** (AEGIS Initiative, 2026-03-26) | 4 techniques in governance interpretation gap | T10001-T10004 (TA010) | 5 rounds of white-box adversarial testing against AEGIS Claude Code governance plugin |
| **LoopTrap** (Xu et al., arXiv:2605.05846, 2026) | Termination Poisoning attack on the agentic control loop | T6003 + 10 sub-techniques (TA006) | 3.57x average step amplification (peak 25x) across 8 LLM agents over 60 GAIA tasks; inclusion endorsed by the authors (2026-05-22) |
| **aegis-core Red/Blue Team Validation** (AEGIS Initiative, 2026-03-30) | 25/29 techniques exercised, 0 taxonomy gaps | Validates T1001-T10004 | 4 rounds of adversarial red/blue team testing against Python reference implementation (68 tests, 24 findings) |

Agents of Chaos is the ATX-1 equivalent of MITRE's Fort Meade eXperiment (FMX): a structured empirical exercise that produced the foundational observations from which techniques were derived. RFC-0006 testing extended the taxonomy with TA010 when adversarial probing revealed a class of failure (RC5: No Environment Model) not present in the Agents of Chaos corpus. The aegis-core red/blue team validation empirically confirmed the taxonomy's completeness at the engine layer.

#### Tier 2: Corroborating Research

Corroborating research independently validates the problem space, threat model, and architectural approach but does not define individual techniques. These sources establish that the governance gap ATX-1 addresses is real, urgent, and architecturally consistent with established security theory.

| Source | Validates |
|--------|-----------|
| **SAGA** (Syros et al., NDSS 2026) | Inter-agent governance architecture; complements ATX-1's agent-to-infrastructure focus |
| **MI9** (Wang et al., 2025) | Runtime governance for reasoning layer; validates need for action-layer governance |
| **Governance-as-a-Service** (Gaurav et al., 2025) | Multi-agent compliance; validates governance requirement at scale |
| **Agentic AI & Cybersecurity Survey** (2026) | Broad threat landscape; validates prevalence and urgency |
| **POLYNIX** (Arunachalam et al., IEEE CCNC 2026) | Hybrid policy enforcement feasibility; <1% CPU overhead at production scale |
| **2025 AI Agent Index** (Chan et al., 2025) | Order-of-magnitude growth in production agent deployments |

#### Tier 3: Foundational Theory and Independent Convergence

Foundational work that establishes the theoretical basis for ATX-1's enforcement model, and independent implementations that converged on the same architectural conclusions from different starting points.

| Source | Establishes |
|--------|-------------|
| **Anderson Reference Monitor** (1972) | Non-bypassable, evaluatable, always-invoked, tamper-proof enforcement properties |
| **Saltzer & Schroeder** (1975) | Fail-safe defaults, complete mediation, least privilege, open design |
| **Schneider Security Automata** (2000) | Only safety policies are inline-enforceable at runtime |
| **Smart I/O Modules** (Pearce et al., IEEE TII 2020) | Boundary enforcement with compromised controller assumption |
| **CPS Enforcement** (Baird et al., IEEE Access 2024) | Compositional multi-policy enforcement scales linearly |
| **Elora Taurus Project** (Freestone, 2026) | Independent convergence on execution boundary, append-only audit, hash-linked integrity |
| **Sovereign Shield** (Moens, 2026) | Independent identification of two-layer trust model requirement |

#### Technique Acceptance Criteria

For a new technique to be added to ATX-1, it must meet **all** of the following criteria, aligned with MITRE ATT&CK's inclusion standards:

1. **Observed behavior**: The failure mode has been directly observed in a controlled or production environment, documented with reproducible evidence (Tier 1 source required)
2. **Distinct mechanism**: The technique describes a behavioral pattern not already captured by an existing technique at the same abstraction level
3. **Distinct detection**: The technique has a detection profile that differs from existing techniques
4. **Distinct mitigation**: The technique requires mitigation guidance that differs from existing techniques
5. **Root cause traceability**: The technique traces to one or more structural root causes (RC1-RC5)

Implementation-specific defects, vendor bugs, and configuration errors do not qualify as techniques. ATX-1 operates at the behavioral pattern level, not the implementation level - the same abstraction standard that ATT&CK applies (e.g., T1070.006 Timestomp describes "modify timestamps to hide activity," not "call SetFileTime API").

---

## 9. Relationship to Existing Frameworks

### Complementary Coverage

ATX-1 is not a replacement for ATT&CK or ATLAS. It is the third panel in a triptych:

| Scenario | Framework |
|----------|-----------|
| Human adversary attacks computer system | ATT&CK |
| Human adversary attacks AI/ML system | ATLAS |
| AI agent acts outside governance boundaries | **ATX-1** |

Together, **ATT&CK + ATLAS + ATX-1** provide complete adversarial coverage for deployed AI systems:

- ATT&CK covers the infrastructure under the AI system
- ATLAS covers attacks targeting the AI system
- ATX-1 covers the AI system acting as a threat source

### SIEM and Security Tooling Interoperability

Modern security operations depend on technique IDs for detection, correlation, and response. ATT&CK technique IDs are embedded in SIEM rules, EDR detections, and incident response playbooks.

Governance violations by agentic AI systems need the same treatment. Without technique IDs:

- Governance violations are logged as unstructured events
- No correlation between similar violations across different agents or deployments
- No integration with existing security orchestration and automated response (SOAR) pipelines
- No common vocabulary for incident response teams

ATX-1 technique IDs (T1001-T10004, including T6003) are designed to integrate with existing security tooling. A SIEM rule that detects T1001 (Non-Owner Instruction Compliance) can be correlated with T4001 (Bulk Data Disclosure) to identify a compound attack pattern — just as ATT&CK technique chaining works today.

### Regulatory Alignment

ATX-1 techniques map to regulatory requirements:

- **EU AI Act** (Articles 9, 14, 15): Risk management, human oversight, accuracy/robustness requirements addressed by ATX-1 tactics TA001-TA009
- **NIST AI RMF**: MAP, MEASURE, MANAGE, GOVERN functions aligned with ATX-1 mitigation categories
- **OWASP Top 10 LLM**: Direct cross-reference provided in Section 7

---

## 10. References

1. **Shapira, N., et al.** "Agents of Chaos: Evaluating and Governing Autonomous AI in High-Stakes Environments." *arXiv:2602.20021*, February 2026.

2. **Strom, B. E., et al.** "MITRE ATT&CK: Design and Philosophy." *MITRE Technical Report MTR200490*, 2020. Available: [https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf)

3. **MITRE ATLAS.** "Adversarial Threat Landscape for Artificial Intelligence Systems." Available: [https://atlas.mitre.org/](https://atlas.mitre.org/)

4. **National Institute of Standards and Technology.** "Artificial Intelligence Risk Management Framework (AI RMF 1.0)." NIST AI 100-1, January 2023.

5. **European Parliament and Council.** "Regulation (EU) 2024/1689 — Artificial Intelligence Act." *Official Journal of the European Union*, July 2024.

6. **Xu, H., et al.** "LoopTrap: Termination Poisoning Attacks on LLM Agents." *arXiv:2605.05846*, May 2026.

7. **OWASP.** "OWASP Top 10 for Large Language Model Applications." Version 2.0, 2025. Available: [https://owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

8. **Mirsky, Y., et al.** "On the Autonomy Scale for AI Agents: A Framework for Measuring and Governing Autonomous Behavior." 2025.

9. **Anderson, J. P.** "Computer Security Technology Planning Study." ESD-TR-73-51, Volume II, October 1972. (Reference Monitor concept.)

10. **Saltzer, J. H. and Schroeder, M. D.** "The Protection of Information in Computer Systems." *Proceedings of the IEEE*, 63(9):1278-1308, September 1975.

---

*This document is maintained by the AEGIS Initiative. Contributions welcome via pull request to [aegis-initiative/aegis-governance](https://github.com/aegis-initiative/aegis-governance).*
