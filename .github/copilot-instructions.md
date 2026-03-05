# AEGIS Project Copilot Instructions

This repository defines the architecture and reference implementation
for AEGIS (Architectural Enforcement & Governance of Intelligent Systems).

AEGIS is a governance runtime for AI systems that enforces deterministic
control over AI-generated actions before they interact with infrastructure.

Core principles:

1. AI systems propose actions
2. AEGIS evaluates those actions
3. Only approved actions are executed

Key components:

- Governance Gateway
- Decision Engine
- Capability Registry
- Policy Engine
- Tool Proxy Layer
- Audit System

Primary protocol:

AGP (AEGIS Governance Protocol)

Primary goals:

- deterministic governance of AI actions
- capability-based authorization
- policy-driven enforcement
- operational risk controls
- auditability

Copilot should prioritize:

- security-first architecture
- capability-based access models
- clear governance boundaries
- deterministic policy evaluation
