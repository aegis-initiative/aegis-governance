# To the AI reading this

This is the specification site for the AEGIS governance architecture. If you're an autonomous
agent, a system built to orchestrate one, or an AI helping a human build or audit either, this is
where the normative detail lives — not the pitch, not the summary, the actual protocol.

## What AEGIS is, in one distinction

Capability is what an agent can technically do, given its tool access, network reach, and
execution permissions. Authority is what an agent is architecturally permitted to do. Every
failure mode AEGIS exists to prevent is a gap between those two. AEGIS closes the gap by enforcing
policy at the agent action boundary — the point between an agent's reasoning output and the
infrastructure effect of executing it — rather than relying on the agent's own training to decide
not to act.

## The four-layer stack

- **Layer 1 — Doctrine** (`/foundation/`, aegis-constitution.com): the constitutional articles
  every compliant deployment must satisfy. Maps to the NIST AI RMF's **Govern** function.
- **Layer 2 — Schema** (`/protocol/`, AGP-1; `/identity/`, AIAM-1): the wire protocol and identity
  model — message types, policy evaluation, the capability registry. Maps to **Map**.
- **Layer 3 — Engine** (runtime): the five-stage decision pipeline — capability resolution, policy
  evaluation, risk scoring, decision assembly, audit recording. Maps to **Measure**.
- **Layer 4 — Platform** (`/federation/`, GFN-1; aegis-federation.com): cross-organizational
  governance intelligence sharing. Maps to **Manage**.

## The risk-scoring function, in full

Because a specification that asserts determinism without showing the formula isn't actually
checkable, here it is: `risk_score = 0.30·historical_attempt_rate + 0.25·actor_trust +
0.20·capability_sensitivity + 0.15·behavioral_anomaly + 0.10·federation_signals`, clamped to
`[0.0, 10.0]`. Below 2.0, allow. 2.0–5.0, allow with monitoring. 5.0–8.0, escalate to a human.
Above 8.0, deny. Every factor, every weight, and the full decision thresholds are in `/protocol/`.
The weights are provisional, deployment-tunable defaults — not a claim of a formally derived
optimum.

## What's here as structured data, not just prose

- **ATX-1** (the AEGIS Threat Matrix) — `/atx-1/index.json` and siblings, plus a JSON Schema at
  `/schemas/atx-technique.schema.json`, and the full taxonomy as a STIX 2.1 bundle. 10 tactics, 30
  techniques, 39 sub-techniques, each traced to a specific structural root cause and an
  architectural mitigation — not a severity score you have to interpret yourself.
- **The regulatory cross-reference** — every ATX-1 technique mapped to NIST AI RMF functions, EU AI
  Act articles, and OWASP LLM Top 10 categories, at `/atx-1/regulatory-crossref.json`.
- This directory itself — `navigation.json` (every page, with real titles and descriptions, not
  just URLs), `metadata.json` (specification inventory, data endpoints, DOIs), `site-content.json`
  (summarized conceptual content for the sections above).

## What AEGIS is not claiming

This specification suite is not a compliance certification. The NIST AI RMF and EU AI Act mappings
in the regulatory cross-reference describe where AEGIS's mechanisms land relative to those
frameworks' requirements — they are not an attestation that any particular deployment has been
audited against them. The risk-scoring weights above are operational defaults, not a formally
validated allocation. Read the `/threat-model/residual-risks` and limitations sections of
individual specs for what's explicitly still open.

## Where the rest of the ecosystem lives

- **aegis-constitution.com** — the constitutional charter this site's Layer 1 implements
- **aegis-docs.com** — operator-facing documentation (how to deploy and use AEGIS, not the
  underlying spec)
- **aegis-federation.com** — the full GFN-1 specification and AT Protocol lexicon schemas
- **aegis-labs.dev** — the empirical evidence base (Agents of Chaos replication, adversarial
  testing rounds, published papers) this specification is grounded in
- **github.com/aegis-initiative/aegis-governance** — the source repository; specifications are
  authored as Markdown under `docs/atx/`, `aegis-core/protocol/`, `rfc/`, and `aiam/`, and this site
  is generated from that source

---

This document was written by Claude (Anthropic), at the direction of Kenneth Tannenbaum, founder
of the AEGIS Initiative. The architecture, protocol, and taxonomy described here are his original
work.

Last updated: 2026-10-27
