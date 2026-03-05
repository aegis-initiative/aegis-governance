"""Tests for the AGP (AEGIS Governance Protocol) data structures."""

import uuid
from datetime import datetime, timezone

import pytest

from aegis.protocol import (
    AGPAction,
    AGPContext,
    AGPRequest,
    AGPResponse,
    ActionType,
    Decision,
)


class TestDecision:
    def test_values(self):
        assert Decision.APPROVED == "approved"
        assert Decision.DENIED == "denied"
        assert Decision.DEFERRED == "deferred"

    def test_string_comparison(self):
        assert Decision.APPROVED == "approved"


class TestActionType:
    def test_all_types_present(self):
        types = {at.value for at in ActionType}
        assert "tool_call" in types
        assert "file_read" in types
        assert "file_write" in types
        assert "api_call" in types
        assert "shell_exec" in types
        assert "data_access" in types


class TestAGPAction:
    def test_defaults(self):
        action = AGPAction(type=ActionType.TOOL_CALL, target="my_tool")
        assert action.parameters == {}

    def test_custom_parameters(self):
        action = AGPAction(
            type=ActionType.FILE_READ,
            target="/etc/hosts",
            parameters={"encoding": "utf-8"},
        )
        assert action.parameters["encoding"] == "utf-8"


class TestAGPContext:
    def test_auto_timestamp(self):
        ctx = AGPContext(session_id="sess-1")
        assert isinstance(ctx.timestamp, datetime)
        assert ctx.timestamp.tzinfo is not None

    def test_metadata_defaults(self):
        ctx = AGPContext(session_id="sess-1")
        assert ctx.metadata == {}


class TestAGPRequest:
    def test_auto_request_id(self):
        req = AGPRequest(
            agent_id="agent-1",
            action=AGPAction(type=ActionType.TOOL_CALL, target="tool"),
            context=AGPContext(session_id="sess-1"),
        )
        # Should be a valid UUID
        uuid.UUID(req.request_id)

    def test_unique_request_ids(self):
        make_req = lambda: AGPRequest(
            agent_id="a",
            action=AGPAction(type=ActionType.TOOL_CALL, target="t"),
            context=AGPContext(session_id="s"),
        )
        assert make_req().request_id != make_req().request_id

    def test_explicit_request_id(self):
        req = AGPRequest(
            agent_id="a",
            action=AGPAction(type=ActionType.TOOL_CALL, target="t"),
            context=AGPContext(session_id="s"),
            request_id="custom-id",
        )
        assert req.request_id == "custom-id"


class TestAGPResponse:
    def test_required_fields(self):
        resp = AGPResponse(
            request_id="req-1",
            decision=Decision.APPROVED,
            reason="Approved by policy.",
            audit_id="aud-1",
        )
        assert resp.decision == Decision.APPROVED
        assert resp.conditions == []
        assert isinstance(resp.timestamp, datetime)
