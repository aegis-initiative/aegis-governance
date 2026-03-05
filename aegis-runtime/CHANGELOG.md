# Changelog

All notable changes to the AEGIS Runtime will be documented in this file.

The format loosely follows Keep a Changelog principles.

---

## 0.1.0 – Initial Release

Initial reference implementation of the AEGIS governance runtime.

Includes:

- AEGIS Governance Protocol (AGP) request/response structures
- Governance Gateway for validated request entry
- Decision Engine implementing capability + policy evaluation
- Capability Registry for capability-based security
- Deterministic Policy Engine
- Immutable SQLite-backed Audit System
- Tool Proxy for governed tool execution
- Integrated runtime facade (`AEGISRuntime`)
