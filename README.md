# aegis-governance

**AEGIS** – Architectural Enforcement & Governance Intelligence System

A governance runtime for AI systems that enforces deterministic control over
AI-generated actions before they interact with infrastructure.

---

## Overview

AEGIS implements a *propose → evaluate → execute* model:

1. An AI agent **proposes** an action via the AGP (AEGIS Governance Protocol).
2. The **Governance Gateway** validates and forwards the request.
3. The **Decision Engine** evaluates capability and policy rules deterministically.
4. Only `Decision.APPROVED` responses allow the action to proceed.
5. Every decision — approved *or* denied — is permanently recorded in the **Audit System**.

---

## Architecture

```
AI Agent
   │  AGPRequest
   ▼
┌──────────────────────┐
│  Governance Gateway  │  ← validates AGP requests
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Decision Engine    │
│                      │
│  ┌────────────────┐  │
│  │ Capability     │  │  Stage 1: does the agent hold a capability
│  │ Registry       │  │           covering this action & target?
│  └────────────────┘  │
│  ┌────────────────┐  │
│  │ Policy Engine  │  │  Stage 2: do configured policies allow it?
│  └────────────────┘  │           (default-deny, priority-ordered)
└──────────┬───────────┘
           │  commits every decision
           ▼
┌──────────────────────┐
│    Audit System      │  ← immutable, append-only SQLite trail
└──────────────────────┘
           │
           ▼  AGPResponse (decision + audit_id)
        AI Agent
```

### Key Components

| Component | Module | Responsibility |
|---|---|---|
| **AGP Protocol** | `aegis.protocol` | Wire-level request/response data structures |
| **Governance Gateway** | `aegis.gateway` | Validation and request routing |
| **Decision Engine** | `aegis.decision_engine` | Orchestrates capability + policy evaluation |
| **Capability Registry** | `aegis.capability_registry` | Capability-based access model |
| **Policy Engine** | `aegis.policy_engine` | Deterministic, priority-ordered policy rules |
| **Tool Proxy Layer** | `aegis.tool_proxy` | Transparent governance for tool invocations |
| **Audit System** | `aegis.audit` | Immutable governance decision log |
| **Runtime Facade** | `aegis.runtime` | Single-object wiring of all components |

---

## Quick Start

```python
from aegis import AEGISRuntime
from aegis.capability_registry import Capability
from aegis.policy_engine import Policy, PolicyEffect, PolicyCondition
from aegis.protocol import ActionType

# 1. Create the runtime (in-memory audit by default)
runtime = AEGISRuntime()

# 2. Register a capability
runtime.capabilities.register(Capability(
    id="cap-docs",
    name="Read documentation",
    description="Allows reading files under /docs",
    action_types=[ActionType.FILE_READ.value, ActionType.TOOL_CALL.value],
    target_patterns=["/docs/*", "read_*"],
))

# 3. Grant the capability to an agent
runtime.capabilities.grant("agent-1", "cap-docs")

# 4. Add a policy (policies are default-deny; at least one allow rule is needed)
runtime.policies.add_policy(Policy(
    id="pol-allow-docs",
    name="Allow documentation reads",
    description="Agents with the docs capability may read documentation.",
    effect=PolicyEffect.ALLOW,
    conditions=[],  # no extra conditions – capability check is sufficient
))

# 5. Create a governed tool proxy for the agent
proxy = runtime.create_tool_proxy("agent-1", session_id="session-xyz")
proxy.register_tool("read_doc", fn=lambda path: open(path).read(), target="read_doc")

# 6. Invoke the tool – governance is applied transparently
content = proxy.call("read_doc", path="/docs/intro.md")
```

---

## AGP Protocol

Every governance interaction is expressed as an `AGPRequest` / `AGPResponse` pair.

### `AGPRequest`

| Field | Type | Description |
|---|---|---|
| `request_id` | `str` | Auto-generated UUID4 |
| `agent_id` | `str` | Identifier of the requesting agent |
| `action.type` | `ActionType` | `tool_call`, `file_read`, `file_write`, `api_call`, `shell_exec`, `data_access` |
| `action.target` | `str` | Target resource (URI, path, tool name, …) |
| `action.parameters` | `dict` | Action-specific parameters |
| `context.session_id` | `str` | Current session identifier |
| `context.metadata` | `dict` | Supplementary metadata |

### `AGPResponse`

| Field | Type | Description |
|---|---|---|
| `request_id` | `str` | Echoes the request ID |
| `decision` | `Decision` | `approved`, `denied`, or `deferred` |
| `reason` | `str` | Human-readable explanation |
| `audit_id` | `str` | ID of the immutable audit record |
| `conditions` | `list[str]` | Optional conditions on approval |
| `timestamp` | `datetime` | UTC decision timestamp |

---

## Policy Engine

Policies are evaluated in ascending *priority* order (lower number = evaluated
first). The engine is **default-deny**: if no allow policy matches, the decision
is `DENIED`.

```python
from aegis.policy_engine import Policy, PolicyCondition, PolicyEffect

# A deny rule that blocks shell execution for all agents
no_shell = Policy(
    id="pol-no-shell",
    name="Block shell execution",
    description="Shell commands are never permitted.",
    effect=PolicyEffect.DENY,
    priority=0,   # evaluated before any allow rule
    conditions=[
        PolicyCondition(
            evaluate=lambda req: req.action.type.value == "shell_exec",
            description="action is shell_exec",
        )
    ],
)
runtime.policies.add_policy(no_shell)
```

---

## Capability Registry

Capabilities use `fnmatch` glob patterns for target matching:

```python
Capability(
    id="cap-s3-read",
    name="S3 Read",
    description="Read objects from the analytics bucket",
    action_types=["api_call"],
    target_patterns=["s3://analytics-bucket/*"],
)
```

Capabilities can be time-limited via `expires_at`:

```python
from datetime import datetime, timedelta, timezone

Capability(
    ...,
    expires_at=datetime.now(timezone.utc) + timedelta(hours=8),
)
```

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=aegis --cov-report=term-missing
```

---

## Design Principles

- **Security-first** – default-deny posture; every action requires explicit capability + policy approval.
- **Deterministic** – same request against the same configuration always yields the same decision.
- **Auditability** – every decision is permanently recorded with full context.
- **Capability-based** – fine-grained, revocable, time-limited authorization model.
- **Separation of concerns** – capability and policy evaluation are independent, composable stages.
