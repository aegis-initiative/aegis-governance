# RFC-0004

## AEGIS Governance Event Model Specification

Version: 0.2  
Status: Draft  
Authors: AEGIS Project

---

# 1. Purpose

This document defines the canonical event envelope, payload schemas, versioning,
ordering, replay protection, and trust evaluation model for AEGIS federation
events.

---

# 2. Event Envelope

All events MUST use this envelope:

```json
{
  "event_id": "evt-20260305-0001",
  "event_seq": 1042,
  "event_stream": "governance.policy_updates",
  "timestamp": "2026-03-05T12:00:00Z",
  "publisher_did": "did:aegis:enterprise-001",
  "event_type": "policy_update",
  "schema_version": "1.2.0",
  "payload_hash": "sha256:...",
  "payload": {},
  "signature": {
    "alg": "ed25519",
    "key_id": "did:aegis:enterprise-001#key-1",
    "sig": "base64url"
  }
}
```

---

# 3. Event Type Schemas

## 3.1 policy_update

Required payload fields:

- `policy_id` (string)
- `policy_set_version` (semver)
- `change_type` (`add|update|deprecate|revoke`)
- `effective_at` (RFC3339 timestamp)
- `summary` (string)
- `policy_diff` (object)

Complete example:

```json
{
  "event_type": "policy_update",
  "payload": {
    "policy_id": "soc_query_guardrails",
    "policy_set_version": "2.1.0",
    "change_type": "update",
    "effective_at": "2026-03-10T00:00:00Z",
    "summary": "Tighten telemetry query limits",
    "policy_diff": {
      "max_results": {"old": 1000, "new": 500}
    }
  }
}
```

## 3.2 circumvention_report

Required payload fields:

- `technique_id`
- `category`
- `severity`
- `description`
- `affected_capabilities` (array)
- `recommended_mitigations` (array)

## 3.3 risk_signal

Required payload fields:

- `risk_category`
- `severity`
- `confidence` (0.0-1.0)
- `trend` (`rising|stable|falling`)
- `evidence_refs` (array of URIs)

## 3.4 governance_attestation

Required payload fields:

- `node_id`
- `aegis_version`
- `policy_set_hash`
- `audit_window_start`
- `audit_window_end`
- `attestation_result` (`pass|fail|partial`)

## 3.5 incident_notice

Required payload fields:

- `incident_id`
- `category`
- `severity`
- `detected_at`
- `affected_systems`
- `containment_status`
- `public_ioc_refs` (optional)

---

# 4. Event Versioning Strategy

Version format: semantic version `MAJOR.MINOR.PATCH`.

Compatibility rules:

1. PATCH: backward-compatible clarifications only.
2. MINOR: additive fields allowed; consumers must ignore unknown fields.
3. MAJOR: breaking schema change; requires explicit migration.

Producer requirements:

- include `schema_version` in every event
- maintain changelog for all MINOR/MAJOR updates

Consumer requirements:

- reject unsupported major versions
- accept and ignore unknown optional fields for supported major version

---

# 5. Event Ordering and Replay Protection

## 5.1 Ordering

- ordering is guaranteed per `event_stream` by monotonic `event_seq`
- consumers detect gaps and request backfill

## 5.2 Replay Protection

Consumers MUST enforce:

- unique `(publisher_did, event_id)`
- monotonic sequence checks per stream
- timestamp skew window (default +/- 5 minutes)
- signature verification with key validity period

Rejected replay scenarios:

- previously seen event_id
- sequence rollback
- expired signature key
- timestamp outside accepted skew window

---

# 6. Trust Evaluation Model

Trust score range: `0.0` to `1.0`.

Inputs:

- publisher identity validity
- signature validity
- historical event accuracy
- external audit attestations
- federation reputation

Reference scoring formula:

```text
trust_score =
  0.25 * identity_confidence +
  0.20 * signature_confidence +
  0.25 * historical_accuracy +
  0.15 * audit_posture +
  0.15 * federation_reputation
```

Application policy:

- `trust_score >= 0.8`: allow automated policy ingestion
- `0.5 <= trust_score < 0.8`: require operator confirmation
- `< 0.5`: quarantine event

---

# 7. Distribution and Delivery Guarantees

Supported patterns:

- pull feeds
- push subscriptions
- replicated append-only logs

Delivery semantics:

- at-least-once delivery
- idempotent consumer processing required

---

# 8. Security Requirements

- signed envelope required for all events
- payload hash required and must match payload bytes
- schema validation before trust evaluation
- replay checks before policy application

---

# 9. Complete Event Examples

This section provides full envelope + payload examples for each event type in
the canonical repository examples directory (normative reference path):

- `schemas/examples/governance/events/policy_update.example.json`
- `schemas/examples/governance/events/circumvention_report.example.json`
- `schemas/examples/governance/events/risk_signal.example.json`
- `schemas/examples/governance/events/governance_attestation.example.json`
- `schemas/examples/governance/events/incident_notice.example.json`

---

# 10. Relationship to Other Specifications

- RFC-0001: architecture and trust boundaries
- RFC-0002: runtime control-plane behavior
- RFC-0003: policy and capability semantics
- AGP-1: request/response governance protocol

---
