"""Tests for the ToolProxy layer."""

import pytest

from aegis import AEGISRuntime
from aegis.capability_registry import Capability
from aegis.policy_engine import Policy, PolicyEffect
from aegis.protocol import ActionType


@pytest.fixture()
def runtime() -> AEGISRuntime:
    rt = AEGISRuntime()
    cap = Capability(
        id="cap-tools",
        name="Tool access",
        description="",
        action_types=["tool_call"],
        target_patterns=["*"],
    )
    rt.capabilities.register(cap)
    rt.capabilities.grant("agent-1", "cap-tools")
    rt.policies.add_policy(Policy(
        id="pol-allow",
        name="Allow all tools",
        description="",
        effect=PolicyEffect.ALLOW,
        conditions=[],
    ))
    return rt


@pytest.fixture()
def proxy(runtime):
    return runtime.create_tool_proxy("agent-1", "sess-1")


class TestRegistration:
    def test_register_tool(self, proxy):
        proxy.register_tool("greet", fn=lambda name: f"Hello, {name}!", target="greet")
        assert "greet" in proxy.registered_tools()

    def test_unregister_tool(self, proxy):
        proxy.register_tool("greet", fn=lambda: None)
        proxy.unregister_tool("greet")
        assert "greet" not in proxy.registered_tools()

    def test_default_target_is_tool_name(self, runtime):
        proxy = runtime.create_tool_proxy("agent-1", "sess-1")
        proxy.register_tool("my_tool", fn=lambda: None)
        # Target defaults to tool name; should be callable without error
        result = proxy.call("my_tool")
        assert result is None


class TestGovernedCall:
    def test_approved_call_executes_fn(self, proxy):
        proxy.register_tool("add", fn=lambda a, b: a + b, target="add")
        assert proxy.call("add", a=2, b=3) == 5

    def test_denied_call_raises_permission_error(self, runtime):
        # Create proxy for an agent with NO capabilities
        proxy = runtime.create_tool_proxy("no-cap-agent", "sess-2")
        proxy.register_tool("restricted", fn=lambda: "secret", target="restricted")
        with pytest.raises(PermissionError, match="denied"):
            proxy.call("restricted")

    def test_unknown_tool_raises_value_error(self, proxy):
        with pytest.raises(ValueError, match="not registered"):
            proxy.call("nonexistent")

    def test_fn_is_not_called_when_denied(self, runtime):
        called = []

        def side_effect():
            called.append(True)
            return "data"

        proxy = runtime.create_tool_proxy("no-cap-agent", "sess-3")
        proxy.register_tool("spy", fn=side_effect, target="spy")

        with pytest.raises(PermissionError):
            proxy.call("spy")

        assert called == [], "Tool function must not be called when governance denies"

    def test_audit_record_created_for_tool_call(self, proxy, runtime):
        proxy.register_tool("echo", fn=lambda msg: msg, target="echo")
        proxy.call("echo", msg="hello")
        history = runtime.audit.get_agent_history("agent-1")
        assert any(r.action_target == "echo" for r in history)

    def test_kwargs_forwarded_correctly(self, proxy):
        captured = {}

        def capture(**kwargs):
            captured.update(kwargs)

        proxy.register_tool("capture", fn=capture, target="capture")
        proxy.call("capture", x=1, y=2)
        assert captured == {"x": 1, "y": 2}
