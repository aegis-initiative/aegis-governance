# ATX-1: AEGIS Threat Matrix — Adversarial Knowledge Base for Agentic AI

This directory contains the ATX-1 technique taxonomy, a structured adversarial knowledge base for agentic AI actor behavior.

## Contents

- [ATX-1_TECHNIQUE_TAXONOMY.md](ATX-1_TECHNIQUE_TAXONOMY.md) — Full technique taxonomy document

## What Is ATX-1?

ATX-1 (AEGIS Threat Matrix — Agentic Exploitation and Governance Intelligence Schema) fills the gap between two existing MITRE frameworks:

- **ATT&CK** catalogs how human adversaries attack computer systems
- **ATLAS** catalogs how adversaries attack AI/ML systems
- **ATX-1** catalogs how AI agents act outside their governance boundaries

ATX-1 addresses the scenario where the AI agent itself is the threat source — not through compromise or malicious intent, but through capability without governance constraint.

## Structure

The taxonomy defines:

- **4 structural root causes** (RC1-RC4)
- **9 tactics** (TA001-TA009)
- **20 techniques** (T1001-T9001)
- **Mitigation mappings** to AEGIS constitutional articles and AGP mechanisms
- **Cross-references** to OWASP Top 10 for LLM Applications

## Empirical Foundation

All techniques are grounded in the **Agents of Chaos** study (Shapira et al., arXiv:2602.20021, February 2026), which documented 11 failure modes across live agentic AI deployments with 20 researchers over 2 weeks.

## Related

- [AEGIS Governance Specification](../../SPECIFICATION.md)
- [AEGIS Terminology](../../TERMINOLOGY.md)
- [AEGIS References](../../REFERENCES.md)
