"""Tests for the GovernanceGateway."""

import pytest

from aegis import AEGISRuntime
from aegis.capability_registry import Capability
from aegis.exceptions import AEGISValidationError
from aegis.policy_engine import Policy, PolicyEffect
from aegis.protocol import AGPAction, AGPContext, AGPRequest, ActionType, Decision


@pytest.fixture()
def runtime() -> AEGISRuntime:
    rt = AEGISRuntime()
    cap = Capability(
        id="cap-1",
        name="All",
        description="",
        action_types=["tool_call"],
        target_patterns=["*"],
    )
    rt.capabilities.register(cap)
    rt.capabilities.grant("agent-1", "cap-1")
    rt.policies.add_policy(Policy(
        id="pol-allow",
        name="Allow all",
        description="",
        effect=PolicyEffect.ALLOW,
        conditions=[],
    ))
    return rt


def make_request(**overrides) -> AGPRequest:
    defaults = dict(
        agent_id="agent-1",
        action=AGPAction(type=ActionType.TOOL_CALL, target="my_tool"),
        context=AGPContext(session_id="sess-1"),
    )
    defaults.update(overrides)
    return AGPRequest(**defaults)


class TestValidation:
    def test_empty_agent_id_raises(self, runtime):
        req = make_request(agent_id="")
        with pytest.raises(AEGISValidationError, match="agent_id"):
            runtime.gateway.submit(req)

    def test_blank_agent_id_raises(self, runtime):
        req = make_request(agent_id="   ")
        with pytest.raises(AEGISValidationError, match="agent_id"):
            runtime.gateway.submit(req)

    def test_empty_target_raises(self, runtime):
        req = make_request(action=AGPAction(type=ActionType.TOOL_CALL, target=""))
        with pytest.raises(AEGISValidationError, match="target"):
            runtime.gateway.submit(req)

    def test_empty_session_id_raises(self, runtime):
        req = make_request(context=AGPContext(session_id=""))
        with pytest.raises(AEGISValidationError, match="session_id"):
            runtime.gateway.submit(req)


class TestSubmit:
    def test_valid_request_returns_response(self, runtime):
        response = runtime.gateway.submit(make_request())
        assert response.decision == Decision.APPROVED

    def test_request_id_echoed(self, runtime):
        req = make_request()
        response = runtime.gateway.submit(req)
        assert response.request_id == req.request_id

    def test_denied_request_returns_response(self, runtime):
        # Agent with no capability
        req = make_request(agent_id="unknown-agent")
        response = runtime.gateway.submit(req)
        assert response.decision == Decision.DENIED
