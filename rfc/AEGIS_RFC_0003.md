# RFC-0003

## Capability Registry and Policy Language

Version: 0.1
Status: Draft

---

## 1. Purpose

This document defines the **AEGIS™ Capability Registry** and the governance policy language used by the decision engine.

---

## 2. Capability Registry

The registry defines all actions AI systems may request.

Each capability record contains:

* identifier
* description
* permitted roles
* environment scope
* risk classification
* optional constraints

Example:

```yaml
capability: telemetry.query
description: Query security telemetry
allowed_roles:
  - soc_analyst
environment:
  - production
risk_level: low
constraints:
  max_results: 500
```

---

## 3. Capability Categories

Capabilities are grouped by domain.

```
telemetry.*
data.*
identity.*
communication.*
infrastructure.*
governance.*
```

---

## 4. Policy Language

Policies define when capabilities may be exercised.

Example rule:

```
policy: telemetry_query_allowed
when:
 capability: telemetry.query
 actor.role: soc_analyst
then:
 decision: ALLOW
```

---

## 5. Conditional Policies

Policies may evaluate contextual attributes.

Example:

```
policy: production_deploy_guardrail
when:
 capability: infrastructure.deploy
 environment: production
then:
 decision: ESCALATE
```

---

## 6. Risk-Based Policies

Policies may reference risk evaluation.

```
policy: high_risk_operation
when:
 risk_score > 7
then:
 decision: REQUIRE_CONFIRMATION
```

---

## 7. Policy Evaluation Order

Policy evaluation occurs in the following order:

1. governance invariants
2. capability registry rules
3. policy engine evaluation
4. risk assessment

Any **DENY** decision overrides other outcomes.

---

## 8. Governance Invariants

Certain rules cannot be overridden.

Examples:

```
deny if capability undefined
deny if actor not authenticated
deny if secret exposure detected
```

---

## 9. Policy Versioning

Policies must include version identifiers to ensure reproducibility.

```
policy_set: enterprise_governance
version: 2026.03.05
```

---

## 10. Conclusion

The capability registry and policy language form the **governance logic layer** of the AEGIS™ runtime.
