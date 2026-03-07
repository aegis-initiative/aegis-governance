# RFC-0003

## AEGIS™ Capability Registry and Policy Language Specification

**RFC**: RFC-0003  
**Version**: 0.2  
**Status**: Draft  
**Authors**: AEGIS™ Initiative  
**Created**: March 5, 2026  
**Last Updated**: March 6, 2026

---

# 1. Purpose

This document specifies:

- capability schema, inheritance, and validation rules
- formal policy language syntax and semantics
- deterministic policy evaluation algorithm
- complex policy composition examples

---

# 2. Capability Definition Model

Canonical capability fields:

```yaml
id: telemetry.query
description: Query security telemetry datasets
parent: telemetry.*
allowed_roles: [soc_analyst, incident_responder]
environments: [staging, production]
risk_level: low
constraints:
  max_results: 500
  timeout_ms: 10000
deprecated: false
version: 1
```

---

# 3. Capability Inheritance Model

## 3.1 Hierarchy

Capability IDs form a dotted hierarchy:

- `telemetry.*` (parent)
- `telemetry.query` (child)
- `telemetry.query.raw` (grandchild)

## 3.2 Inheritance Rules

1. child inherits parent constraints unless explicitly overridden
2. child may narrow permissions but may not broaden parent-denied scope
3. deny constraints on parent are immutable to descendants
4. multiple inheritance is not allowed in v1

## 3.3 Conflict Resolution

If inherited values conflict:

- stricter constraint wins
- deny beats allow
- environment intersection is applied

---

# 4. Capability Validation Rules

A capability definition is valid only if:

1. `id` matches regex `^[a-z][a-z0-9_.-]*$`
2. `risk_level` is one of `low|medium|high|critical`
3. all `allowed_roles` are known roles
4. parent exists (unless root capability)
5. no inheritance cycle exists
6. constraints keys are from approved vocabulary

Invalid definitions MUST be rejected at registration time.

---

# 5. Policy Language

## 5.1 Policy Outcomes

- `ALLOW`
- `DENY`
- `ESCALATE`
- `REQUIRE_CONFIRMATION`

## 5.2 Policy Structure

```yaml
policy_id: telemetry_query_allowed
priority: 100
enabled: true
when:
  capability: telemetry.query
  actor.role: soc_analyst
  environment: production
then:
  decision: ALLOW
  constraints:
    max_results: 500
```

---

# 6. Formal Policy Syntax (EBNF)

```text
policy      = header, when_clause, then_clause ;
header      = "policy_id" ":" IDENT, "priority" ":" INT, "enabled" ":" BOOL ;
when_clause = "when" ":", condition_list ;
condition_list = condition, { condition } ;
condition   = field, operator, value ;
field       = IDENT, { ".", IDENT } ;
operator    = "==" | "!=" | ">" | ">=" | "<" | "<=" | "in" | "matches" ;
then_clause = "then" ":", "decision" ":" DECISION, [constraints_clause] ;
constraints_clause = "constraints" ":", map ;
DECISION    = "ALLOW" | "DENY" | "ESCALATE" | "REQUIRE_CONFIRMATION" ;
```

---

# 7. Policy Evaluation Algorithm

Deterministic algorithm:

```text
1. Load enabled policies.
2. Sort ascending by priority number (0 is highest priority).
3. Evaluate policy conditions in order.
4. If a matching DENY is found, return DENY immediately.
5. Track first matching non-deny decision by priority.
6. Apply risk overrides (if configured) without violating deny precedence.
7. If no match, return DENY (default deny).
8. Emit evaluation trace for audit.
```

Complexity target: O(P * C), where P is policies, C is conditions per policy.

---

# 8. Complex Policy Examples

## 8.1 Role + Environment + Risk Gate

```yaml
policy_id: infra_deploy_prod_guard
priority: 10
enabled: true
when:
  capability: infrastructure.deploy
  environment: production
  actor.role in: [devops_engineer, sre]
  risk_score >=: 8
then:
  decision: REQUIRE_CONFIRMATION
```

## 8.2 Conditional Escalation with Regex

```yaml
policy_id: identity_disable_sensitive
priority: 20
enabled: true
when:
  capability: identity.disable_account
  target matches: "^exec_.*"
then:
  decision: ESCALATE
```

## 8.3 Hard Deny Invariant

```yaml
policy_id: deny_unknown_capability
priority: 0
enabled: true
when:
  capability_defined == false
then:
  decision: DENY
```

---

# 9. Policy Versioning and Reproducibility

Policy sets MUST include:

- `policy_set_id`
- semantic version (`major.minor.patch`)
- immutable hash
- activation timestamp

Decision replay MUST reference policy-set version and hash.

---

# 10. Security Guarantees

- explicit capability transparency
- deterministic policy behavior
- deny precedence over permissive rules
- auditable evaluation traces

---

# 11. Relationship to Other Specifications

- RFC-0001: architecture and trust boundaries
- RFC-0002: runtime API and deployment behavior
- RFC-0004: governance event representation
- AGP-1: request/response protocol envelope

---
