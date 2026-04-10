# AIAM-1: A Specification for Identity and Access Management for AI Agents (aIAM)

**Position Paper — v0.1**
**AEGIS Initiative · Finnoybu IP LLC**
**Author:** Ken Tannenbaum, Founder, AEGIS Initiative

---

## Abstract

This position paper introduces AIAM-1, a specification for identity and access management for AI agents (aIAM), developed under the AEGIS Initiative. AIAM-1 addresses a gap that existing identity and access management frameworks were never designed to close: the governance of autonomous and semi-autonomous AI agents that plan, decide, and execute against production infrastructure. Traditional IAM assumes that actors are humans or scripted services — actors whose identity is durable, whose authorization is relatively static, and whose actions are discrete and reviewable. AI agents violate every one of these assumptions. AIAM-1 defines the identity, intent, authority, capability, delegation, session, attestation, revocation, interoperability, and threat model primitives required to govern agentic systems as a distinct actor class. AIAM-1 introduces Intent-Bound Access Control (IBAC), an authorization model in which every access decision is evaluated as a function of identity, action, and intent context. This paper establishes the normative scope of AIAM-1 v0.1 and specifies the requirements that a conformant implementation must satisfy.

---

## 1. Background and Motivation

### 1.1 The Actor Class Gap

Identity and access management as a discipline was built for two actor classes: humans and service accounts. Humans are slow, deliberate, individually accountable, and operate within well-understood constraints of reaction time and cognitive load. Service accounts are narrow, scripted, and predictable — their behavior is bounded by the code that runs under them. Every significant IAM specification published in the last two decades — OAuth 2.0, OIDC, SAML, SCIM, XACML — was designed against these two actor classes, with their assumptions embedded in the core primitives.

AI agents are a third actor class. They are not humans, and they are not service accounts. They plan toward goals, compose actions dynamically, update their models based on intermediate results, and operate at machine speed. Their identity is durable but their intent is not. Their authorization cannot be static because their goals shift within a single session. Their actions are not discrete — they are composed chains of tool calls where each step conditions the next. Accountability cannot rest on the agent itself, because an agent is not a legal or moral entity.

Attempting to govern AI agents using existing IAM primitives results in a predictable failure mode: agents are either over-scoped (given broad credentials because narrow scoping would make them useless) or under-scoped (constrained to the point of being non-functional). Neither outcome is governance. Both are abdication.

### 1.2 The Scope of aIAM

aIAM — identity and access management for AI agents — is the category of problem this specification addresses. It is a distinct specialization within the broader IAM discipline, related to but not derivable from existing human and service account IAM. AIAM-1 is the AEGIS Initiative's normative specification for aIAM, one possible realization of the category. Other specifications may emerge from other bodies; AIAM-1 is the first.

### 1.3 Relationship to AEGIS

AIAM-1 is a normative artifact within the AEGIS specification family, which includes AGP-1 (AEGIS Governance Protocol), ATX-1 (AEGIS Threat Matrix), ATM-1 (AEGIS Threat Model), and GFN-1 (Governance Federated Network). AIAM-1 extends AEGIS principles into the identity and access management layer of agentic systems, providing the identity and authority primitives that AGP-1 enforcement decisions and ATX-1 threat detections depend on.

### 1.4 Relationship to Other Standards

AIAM-1 is designed to be implemented independently of any specific governance runtime. While it is part of the AEGIS specification family and integrates with AGP-1, ATX-1, ATM-1, and GFN-1 when deployed within an AEGIS-governed environment, conformance to AIAM-1 does not require adoption of any other AEGIS specification. Cross-references to AEGIS artifacts in this document are informative, not normative, unless explicitly stated.

AIAM-1 is intended to complement, not replace, existing IAM specifications. Specifically:

- **OAuth 2.1 and OIDC** provide the transport and token format that AIAM-1 identity claims can map into. AIAM-1 adds the intent and authority primitives that OAuth does not specify.
- **SCIM** provides the lifecycle management primitives that AIAM-1 agents can integrate with. AIAM-1 extends SCIM schema to cover agent-specific identity attributes.
- **XACML and ABAC frameworks** provide the policy evaluation patterns that AIAM-1 authority binding builds on. AIAM-1 extends the evaluation model to include intent context as a first-class input.
- **NIST AI RMF** provides the governance context within which AIAM-1 operates. AIAM-1 implements the identity and access management controls that an AI RMF program requires at the technical layer.
- **ATX-1** provides the threat taxonomy that AIAM-1 defends against. The two specifications are designed to be used together but can be adopted independently.

### 1.5 Intent-Bound Access Control (IBAC)

AIAM-1 introduces Intent-Bound Access Control (IBAC) as its authorization model. IBAC evaluates every access decision as a function of three inputs: identity, action, and intent context. This is a categorical extension of existing authorization models:

- **RBAC** (Role-Based Access Control) evaluates access as a function of identity and role membership. Intent is not an input.
- **ABAC** (Attribute-Based Access Control) evaluates access as a function of actor attributes, resource attributes, and environmental conditions. Intent is not a first-class attribute.
- **PBAC** (Purpose-Based Access Control) evaluates access as a function of identity and declared purpose. IBAC extends PBAC with structured intent claims, principal chains, and session governance.

IBAC generalizes these models: an RBAC policy is an IBAC policy where the intent context pattern is wildcard. An ABAC policy is an IBAC policy where attributes are mapped to identity and action patterns with wildcard intent. IBAC is the first authorization model designed specifically for the agent actor class, where intent shifts dynamically within a single operational session.

---

## 2. Scope and Applicability

### 2.1 In Scope

AIAM-1 v0.1 defines normative requirements for:

- Identity claims for AI agents, including composite identity structure and cryptographic attestation
- Intent claims as structured assertions of agent purpose at the moment of action
- Authority binding as a function of identity, action, and intent context (IBAC)
- Capability scoping, composition, and revocation
- Delegation and principal chain semantics for agent-to-agent and agent-to-sub-agent relationships
- Session semantics as first-class governance boundaries
- Attestation and audit records as primary accountability surfaces
- Revocation and kill-switch propagation with real-time guarantees
- Interoperability requirements with existing IAM standards (OAuth 2.1, OIDC, SAML, SCIM)
- Threat model and defensive posture

### 2.2 Out of Scope

AIAM-1 v0.1 does not define:

- The internal architecture of AI models or agent orchestration frameworks
- Specific cryptographic algorithm choices beyond general requirements for attestation and signing
- Performance benchmarks or scalability targets for conformant implementations
- User interface or developer experience specifications
- Billing, metering, or commercial licensing mechanisms
- Model training or fine-tuning governance
- Trust scoring for agents or federation nodes (see GFN-1 and RFC-0004 for trust models within the AEGIS ecosystem)

### 2.3 Normative Language

This specification uses the terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY as defined in RFC 2119. A conformant AIAM-1 implementation satisfies all MUST and MUST NOT requirements. SHOULD and SHOULD NOT requirements express strong recommendations whose violation must be justified and documented.

---

## 3. Normative Requirements

### 3.1 Identity

**Terminology note:** AIAM-1 uses "principal" to refer to the human, organization, or legal entity on whose behalf an agent acts — the accountable party. Other AEGIS specifications (AGP-1, ATM-1) use "actor" to refer to any entity submitting an action proposal (agent, human, or service). In AIAM-1, an agent is an actor; its principal is the entity accountable for the agent's actions. An AIAM-1 composite identity claim is the rich identity record that an AGP-1 `actor.id` resolves to. AGP-1 implementations that adopt AIAM-1 resolve `actor.id` to a composite identity claim; implementations that do not adopt AIAM-1 continue to treat `actor.id` as an opaque string.

**3.1.1** A conformant implementation MUST represent every AI agent identity as a composite of four dimensions: model provenance, orchestration layer, goal context, and principal.

**3.1.2** Model provenance MUST include, at minimum, the model family, version identifier, and a cryptographic hash or attestation of the model artifact used at runtime.

**3.1.3** Orchestration layer identity MUST include the runtime environment, framework identifier, and version of the agent harness executing the agent loop.

**3.1.4** Goal context MUST include a structured statement of the purpose for which the agent was instantiated, sufficient to distinguish one instantiation from another.

**3.1.5** Principal MUST identify the human, organization, or legal entity on whose behalf the agent acts. The principal is the accountable party for all actions taken by the agent under this identity.

**3.1.6** Agent identity claims MUST be cryptographically signed by an issuing authority whose trust chain is verifiable by any relying party within the governance domain.

**3.1.7** A single agent MAY hold multiple identity claims simultaneously if it operates across multiple goal contexts or on behalf of multiple principals. Each claim MUST be independently verifiable and independently revocable.

### 3.2 Intent

**Terminology note:** Intent claims are a new primitive introduced by AIAM-1. They are not present in AGP-1, which treats intent as implicit in ACTION_PROPOSE parameters. AIAM-1 intent claims extend AGP-1 action proposals with structured, validated assertions of purpose; they do not replace AGP-1 message structures.

**3.2.1** Every action taken by a conformant AI agent MUST carry an intent claim. Actions without a valid intent claim MUST be treated as unauthorized by default.

**3.2.2** An intent claim MUST be a structured assertion, not free text. It MUST include, at minimum: a reference to the goal context the action serves, a summary of the reasoning chain that produced the decision to act, the expected outcome of the action, and a dependency reference to any prior actions this action builds upon.

**3.2.3** Intent claims MUST be produced by the agent at the moment of action, not synthesized after the fact.

**3.2.4** A conformant implementation MUST validate intent claims against the goal context declared in the agent's identity. An intent claim whose goal reference does not match the active goal context MUST result in the action being denied.

**3.2.5** Intent claims MUST be preserved as part of the attestation record for every action (see Section 3.7).

**3.2.6** A conformant implementation SHOULD provide mechanisms to detect intent spoofing — cases where an agent produces an intent claim that does not correspond to the actual reasoning that drove the action.

### 3.3 Authority Binding (IBAC)

**3.3.1** Authorization decisions in a conformant implementation MUST be evaluated as a function of three inputs: identity, action, and intent context. This authorization model is designated Intent-Bound Access Control (IBAC). Authorization decisions based solely on identity and action (without intent context) MUST NOT be considered conformant.

**3.3.2** A conformant implementation MUST define authority policies as triples of the form (identity pattern, action pattern, intent context pattern). IBAC generalizes existing authorization models: an RBAC policy is an IBAC triple where the intent context pattern is wildcard; an ABAC policy is an IBAC triple where attributes are mapped to identity and action patterns with wildcard intent.

**3.3.3** Authority policies MUST be expressible in a machine-readable format and MUST be evaluable deterministically. Policy evaluation MUST NOT depend on the state of the agent being evaluated.

**3.3.4** A conformant implementation MUST deny by default. Any action whose (identity, action, intent) triple does not match an explicit authorizing policy MUST be denied.

**3.3.5** Authority policy changes MUST take effect within a bounded time window. Conformant implementations MUST define and publish their policy propagation latency guarantee.

**3.3.6** AIAM-1 authorization decisions MUST NOT be influenced by trust scores from external specifications except through explicit capability scoping. Trust scores MAY inform which capabilities are granted to an agent, but MUST NOT override an AIAM-1 authorization decision for a granted capability.

### 3.4 Capability Scoping

**3.4.1** Agent capabilities (tool access, API access, credential access) MUST be scoped at the time of agent instantiation.

**3.4.2** Capability scopes MUST be time-bounded. A conformant implementation MUST NOT permit capabilities to persist beyond an explicit expiration without re-authorization.

**3.4.3** A conformant implementation MUST treat capability composition as a governed operation. Composed actions — sequences of individual capability invocations that together produce an effect not achievable by any single invocation — MUST be evaluable against authority policies as first-class actions.

**3.4.4** Capability authorization MUST NOT be closed under transitivity. An agent authorized to perform capability A and capability B is not, by default, authorized to perform the composition A-then-B. Composed actions require explicit authorization.

**3.4.5** A conformant implementation MUST provide mechanisms to revoke individual capabilities without requiring full re-instantiation of the agent.

### 3.5 Delegation and Principal Chains

**3.5.1** A conformant implementation MUST represent delegation as an explicit principal chain. Each agent in the chain MUST identify the principal on whose behalf it acts.

**3.5.2** Delegated authority MUST narrow monotonically down a principal chain. A sub-agent MUST NOT receive delegated authority that exceeds the authority of its parent agent. This requirement applies to authority inherited through delegation; it does not prevent a sub-agent from holding independent capability grants issued directly to it by the governance system.

**3.5.3** The principal at the top of a principal chain MUST remain the accountable party for all actions taken anywhere in the chain.

**3.5.4** A conformant implementation MUST make principal chain obscuration structurally impossible. Attestation records MUST preserve the complete principal chain for every action.

**3.5.5** Sub-agent instantiation MUST itself be a governed action subject to authority policy evaluation.

**3.5.6** A conformant implementation MUST define and publish a maximum delegation chain depth. Unbounded delegation chains are an attack surface for multi-agent collusion and authority diffusion.

### 3.6 Session Semantics

**Terminology note:** AIAM-1 introduces session semantics as a new governance primitive. Other AEGIS specifications (AGP-1, RFC-0002) treat `session_id` as a stateless correlation key. AIAM-1 sessions are stateful governance boundaries that bound agent operations along four dimensions.

**3.6.1** A conformant implementation MUST treat agent sessions as first-class governance boundaries, not as convenience layers over authentication.

**3.6.2** A session MUST be bounded by four dimensions: goal context, time window, capability envelope, and accountability chain.

**3.6.3** Actions taken outside an active session MUST be treated as unauthorized.

**3.6.4** A session MUST terminate on the first of: goal completion, time expiration, capability exhaustion, or explicit revocation.

**3.6.5** A conformant implementation MUST NOT permit silent session escalation. Actions that exceed the session's capability envelope MUST require explicit re-authorization, which MUST produce a new attestation record distinct from the prior session.

### 3.7 Attestation and Audit

**Terminology note:** AIAM-1 attestation records attest to individual governance decisions at the action level. This is distinct from GFN-1 governance attestations (`governance.attestation.v1`), which attest to node-level governance posture. When both AIAM-1 and GFN-1 are deployed together, action-level attestation (AIAM-1) and node-level attestation (GFN-1) coexist as complementary records at different granularities.

**3.7.1** Every action taken by a conformant AI agent MUST produce an attestation record.

**3.7.2** An attestation record MUST include, at minimum: the identity claim, the intent claim, the authority decision, the capabilities invoked, the outcome, the principal chain, and a timestamp.

**3.7.3** Attestation records MUST be cryptographically signed by the enforcement layer that produced them.

**3.7.4** Attestation records MUST be tamper-evident. A conformant implementation MUST provide mechanisms to detect unauthorized modification of attestation records after the fact.

**3.7.5** A conformant implementation MUST define and publish its attestation record retention policy.

**3.7.6** Attestation records MUST be the primary accountability surface. Conformant implementations MUST NOT rely on agent-internal logging or orchestration layer logging as a substitute for attestation records.

### 3.8 Revocation and Kill-Switch Semantics

**3.8.1** Revocation in a conformant implementation MUST be pre-action, not eventually consistent. Revoked credentials, capabilities, or sessions MUST NOT be usable for any action that has not yet committed at the moment of revocation.

**3.8.2** A conformant implementation MUST define and publish its revocation propagation latency guarantee. This guarantee MUST be expressed as a maximum time between revocation command and universal enforcement.

**3.8.3** A conformant implementation MUST provide a kill-switch mechanism capable of halting all actions by a specified agent, principal chain, or session within the revocation propagation latency window.

**3.8.4** Revocation operations MUST themselves be governed actions subject to authority policy evaluation. Only authorized principals may revoke credentials, capabilities, or sessions.

**3.8.5** Revocation events MUST produce attestation records.

### 3.9 Interoperability

**3.9.1** A conformant implementation MUST support agent authentication against existing identity providers using OAuth 2.1 and OpenID Connect without requiring those identity providers to natively understand AIAM-1 identity claims.

**3.9.2** A conformant implementation MUST define a mapping from AIAM-1 identity claims to OAuth 2.1 token formats such that an AIAM-1 agent can present credentials acceptable to an OAuth 2.1-compliant resource server.

**3.9.3** A conformant implementation SHOULD support SCIM for agent lifecycle management (provisioning, updating, deprovisioning) to enable integration with existing identity governance tooling.

**3.9.4** A conformant implementation SHOULD support SAML assertions for federated agent identity in environments that have not adopted OAuth 2.1.

**3.9.5** Interoperability mappings MUST NOT compromise the integrity of AIAM-1 primitives. If an interoperability target cannot express intent context, the mapping MUST document the loss of enforcement guarantee and require compensating controls.

### 3.10 Threat Model

**3.10.1** A conformant implementation MUST explicitly address the following threat classes:

- **Intent spoofing:** An agent produces an intent claim that does not correspond to its actual reasoning or goal. (Informative: relates to ATM-1 AV-3.1, AV-2.1.)
- **Capability composition attacks:** An agent composes individually authorized capabilities into a sequence that produces an unauthorized effect. (Informative: relates to ATM-1 AV-7.1. Note: AEGIS governance architecture provides baseline mitigation through ATM-1 SP-4 explicit-grant-only model; AIAM-1 requires conformant implementations to address this threat regardless of underlying governance runtime.)
- **Authority inheritance exploitation:** A sub-agent or delegated agent exploits inherited authority to take actions the original principal did not intend. (Informative: AEGIS governance architecture provides baseline mitigation through ATM-1 SP-4 default-deny + explicit grant; AIAM-1 requires conformant implementations to address this threat regardless of underlying governance runtime.)
- **Principal chain obscuration:** An agent or orchestration layer hides or misrepresents the principal on whose behalf an action is taken.
- **Attestation forgery:** An attacker produces attestation records that misrepresent actions taken.
- **Revocation evasion:** An agent continues to act after its credentials, capabilities, or session have been revoked. (Informative: relates to ATM-1 RC-2.)
- **Governance visibility exploitation:** An agent probes the enforcement layer to learn what triggers flags or denials, and adapts its behavior to avoid detection. (See ATX-1 TA010.)

**3.10.2** For each threat class, a conformant implementation MUST identify the mechanisms in this specification that provide defense and MUST document any residual risk not addressed by this specification.

**3.10.3** A conformant implementation SHOULD align its threat model documentation with ATX-1 where applicable.

**3.10.4** Any trust evaluation of agent identity or behavior implemented alongside AIAM-1 MUST comply with the structural separation of security and reputation signals. Trust scores and security decisions MUST NOT be collapsed into a single metric. (Informative: within the AEGIS ecosystem, this requirement is normatively specified in RFC-0004 §5.)

---

## 4. Conformance

### 4.1 Conformance Profiles

AIAM-1 v0.1 defines a single conformance profile. A conformant implementation satisfies all MUST and MUST NOT requirements in Section 3. Future versions of this specification MAY define additional profiles for constrained environments or specialized use cases.

### 4.2 Conformance Claims

An implementation claiming AIAM-1 v0.1 conformance MUST publish a conformance statement identifying which requirements are satisfied, which are not, and the rationale for any deviations. Conformance statements MUST reference the specification version and MUST be updated when the implementation changes materially.

### 4.3 Testing and Validation

This specification does not define a normative test suite for v0.1. A companion test suite is planned for a subsequent version. In the interim, conformant implementations SHOULD publish their own validation methodology for review by the community.

---

## 5. Open Questions and Implementation Considerations

The following issues are identified as open questions for v0.2 and beyond. They are not resolved in v0.1 and implementations should document their approach to each.

1. **Intent claim verifiability.** How can a relying party verify that an intent claim corresponds to the agent's actual reasoning, given that the reasoning process itself is typically opaque?

2. **Policy language standardization.** AIAM-1 v0.1 does not mandate a specific policy language. A subsequent version should evaluate candidate languages (Rego, Cedar, XACML) for suitability.

3. **Attestation storage scale.** High-frequency agentic systems may produce millions of attestation records per day. Storage, indexing, and query patterns for attestation at scale require further specification.

4. **Cross-domain federation.** GFN-1 addresses some aspects of cross-domain trust, but the interaction between AIAM-1 identity claims and GFN-1 federation primitives requires explicit specification. In particular: how do AIAM-1 intent claims map to GFN-1 governance attestations?

5. **Model-level attestation.** Attesting the model itself (weights, training provenance, fine-tuning state) is a deeper problem than attesting the runtime agent. v0.2 should consider whether model-level attestation is in scope.

6. **Human-in-the-loop boundaries.** Many agentic systems incorporate human approval steps. AIAM-1 v0.1 treats these as out of scope; a subsequent version should specify how human approval integrates with the identity and authority primitives defined here.

7. **Cross-organization delegation.** When an agent delegates to an agent owned by a different organization, the principal chain crosses an organizational boundary. Minimum requirements for cross-boundary delegation (mutual attestation, bilateral capability agreement, or similar) require explicit specification in v0.2.

---

## 6. Publication and Versioning

This document is v0.1 of the AIAM-1 specification. It is published by the AEGIS Initiative under Finnoybu IP LLC and deposited to Zenodo with a stable DOI. Subsequent versions will be published with incremented version numbers and stable DOIs for each release. Version 0.x releases are considered draft specifications; v1.0 will be the first stable release.

Comments, corrections, and contributions are welcomed. The canonical repository for AIAM-1 is maintained under the AEGIS Initiative GitHub organization.

---

## 7. Acknowledgments

AIAM-1 builds on the body of work developed under the AEGIS Initiative, including AGP-1, ATX-1, ATM-1, and GFN-1. It also draws on conversations with the broader AI governance community, including the NCCoE public comment process on agentic AI identity and authorization.

---

## Appendix A: Glossary

- **Agent:** An AI system capable of planning, deciding, and executing actions against production infrastructure, typically with some degree of autonomy.
- **aIAM:** Identity and access management for AI agents. A category of problem and practice.
- **AIAM-1:** The AEGIS Initiative's normative specification for aIAM, version 1.
- **Attestation record:** A cryptographically signed record of an action taken by an agent, including identity, intent, authority decision, capabilities, outcome, and principal chain.
- **Authority binding:** The association of an identity, action, and intent context with an authorization decision.
- **Capability:** A discrete ability granted to an agent, typically in the form of tool access, API access, or credential access.
- **Goal context:** A structured statement of the purpose for which an agent was instantiated.
- **IBAC (Intent-Bound Access Control):** The authorization model defined by AIAM-1 in which every access decision is evaluated as a function of identity, action, and intent context.
- **Intent claim:** A structured assertion of the purpose of a specific action at the moment it is taken.
- **Principal:** The human, organization, or legal entity on whose behalf an agent acts. The accountable party. Distinguished from "actor" (used in other AEGIS specifications to refer to any entity submitting an action proposal).
- **Principal chain:** The sequence of principals linking an action back to its originating accountable party through any intermediate agents.
- **Session:** A bounded governance context defined by goal, time window, capability envelope, and accountability chain.

---

*AEGIS™* | *"Capability without constraint is not intelligence"™*\
*AEGIS Initiative — Finnoybu IP LLC*
