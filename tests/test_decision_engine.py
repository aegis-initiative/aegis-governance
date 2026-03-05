"""Tests for the DecisionEngine."""

import pytest

from aegis.audit import AuditSystem
from aegis.capability_registry import Capability, CapabilityRegistry
from aegis.decision_engine import DecisionEngine
from aegis.policy_engine import Policy, PolicyCondition, PolicyEffect, PolicyEngine
from aegis.protocol import AGPAction, AGPContext, AGPRequest, ActionType, Decision


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def audit():
    return AuditSystem()


@pytest.fixture()
def registry():
    return CapabilityRegistry()


@pytest.fixture()
def policies():
    return PolicyEngine()


@pytest.fixture()
def engine(registry, policies, audit):
    return DecisionEngine(
        capability_registry=registry,
        policy_engine=policies,
        audit_system=audit,
    )


def make_request(
    agent_id: str = "agent-1",
    action_type: ActionType = ActionType.TOOL_CALL,
    target: str = "my_tool",
) -> AGPRequest:
    return AGPRequest(
        agent_id=agent_id,
        action=AGPAction(type=action_type, target=target),
        context=AGPContext(session_id="sess-1"),
    )


def setup_allow(registry: CapabilityRegistry, policies: PolicyEngine,
                agent_id: str = "agent-1") -> None:
    """Grant capability and add a permissive allow policy."""
    cap = Capability(
        id="cap-1",
        name="All tools",
        description="",
        action_types=["tool_call"],
        target_patterns=["*"],
    )
    registry.register(cap)
    registry.grant(agent_id, "cap-1")
    policies.add_policy(Policy(
        id="pol-allow",
        name="Allow all",
        description="",
        effect=PolicyEffect.ALLOW,
        conditions=[],
    ))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCapabilityGate:
    def test_no_capability_denies(self, engine):
        response = engine.evaluate(make_request())
        assert response.decision == Decision.DENIED
        assert "lacks a capability" in response.reason

    def test_with_capability_proceeds_to_policy(self, engine, registry, policies):
        setup_allow(registry, policies)
        response = engine.evaluate(make_request())
        assert response.decision == Decision.APPROVED


class TestPolicyGate:
    def test_capability_present_but_no_policy_denies(self, engine, registry):
        cap = Capability(
            id="cap-1",
            name="Tools",
            description="",
            action_types=["tool_call"],
            target_patterns=["*"],
        )
        registry.register(cap)
        registry.grant("agent-1", "cap-1")
        # No allow policy added → default-deny
        response = engine.evaluate(make_request())
        assert response.decision == Decision.DENIED
        assert "default-deny" in response.reason

    def test_deny_policy_overrides_capability(self, engine, registry, policies):
        setup_allow(registry, policies)
        # Add a higher-priority deny policy
        policies.add_policy(Policy(
            id="pol-deny",
            name="Emergency deny",
            description="",
            effect=PolicyEffect.DENY,
            conditions=[],
            priority=0,
        ))
        response = engine.evaluate(make_request())
        assert response.decision == Decision.DENIED


class TestAuditIntegration:
    def test_approved_decision_is_audited(self, engine, registry, policies, audit):
        setup_allow(registry, policies)
        response = engine.evaluate(make_request())
        record = audit.get_record(response.audit_id)
        assert record is not None
        assert record.decision == "approved"
        assert record.agent_id == "agent-1"
        assert record.action_type == "tool_call"

    def test_denied_decision_is_also_audited(self, engine, audit):
        response = engine.evaluate(make_request())
        record = audit.get_record(response.audit_id)
        assert record is not None
        assert record.decision == "denied"

    def test_audit_id_in_response(self, engine, registry, policies, audit):
        setup_allow(registry, policies)
        response = engine.evaluate(make_request())
        assert response.audit_id
        assert audit.get_record(response.audit_id) is not None


class TestResponseFields:
    def test_request_id_echoed(self, engine, registry, policies):
        setup_allow(registry, policies)
        req = make_request()
        response = engine.evaluate(req)
        assert response.request_id == req.request_id

    def test_policy_evaluations_in_audit(self, engine, registry, policies, audit):
        setup_allow(registry, policies)
        response = engine.evaluate(make_request())
        record = audit.get_record(response.audit_id)
        assert isinstance(record.policy_evaluations, list)
        assert len(record.policy_evaluations) >= 1
