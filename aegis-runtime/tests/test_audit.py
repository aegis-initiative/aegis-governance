"""Tests for the AuditSystem."""

import pytest

from aegis.audit import AuditRecord, AuditSystem
from aegis.exceptions import AEGISAuditError


@pytest.fixture()
def audit() -> AuditSystem:
    return AuditSystem()  # in-memory


def _record_kwargs(**overrides) -> dict:
    base = {
        "request_id": "req-1",
        "agent_id": "agent-1",
        "action_type": "tool_call",
        "action_target": "my_tool",
        "action_parameters": {"key": "value"},
        "decision": "approved",
        "reason": "Approved by policy.",
        "policy_evaluations": [{"policy_id": "p1", "matched": True}],
        "session_id": "sess-1",
    }
    base.update(overrides)
    return base


class TestRecord:
    def test_returns_audit_id(self, audit):
        audit_id = audit.record(**_record_kwargs())
        assert isinstance(audit_id, str)
        assert len(audit_id) > 0

    def test_unique_audit_ids(self, audit):
        id1 = audit.record(**_record_kwargs())
        id2 = audit.record(**_record_kwargs())
        assert id1 != id2

    def test_record_content_round_trip(self, audit):
        params = {"path": "/etc/hosts", "mode": "r"}
        evals = [{"policy_id": "p1", "matched": True, "effect": "allow"}]
        audit_id = audit.record(
            **_record_kwargs(
                action_parameters=params,
                policy_evaluations=evals,
            )
        )
        rec = audit.get_record(audit_id)
        assert rec is not None
        assert rec.action_parameters == params
        assert rec.policy_evaluations == evals
        assert rec.decision == "approved"
        assert rec.agent_id == "agent-1"


class TestGetRecord:
    def test_returns_none_for_missing(self, audit):
        assert audit.get_record("nonexistent") is None

    def test_returns_immutable_record(self, audit):
        audit_id = audit.record(**_record_kwargs())
        rec = audit.get_record(audit_id)
        assert isinstance(rec, AuditRecord)


class TestGetAgentHistory:
    def test_returns_records_for_agent(self, audit):
        audit.record(**_record_kwargs(agent_id="agent-A"))
        audit.record(**_record_kwargs(agent_id="agent-A"))
        audit.record(**_record_kwargs(agent_id="agent-B"))
        history = audit.get_agent_history("agent-A")
        assert len(history) == 2
        assert all(r.agent_id == "agent-A" for r in history)

    def test_empty_for_unknown_agent(self, audit):
        assert audit.get_agent_history("unknown") == []

    def test_respects_limit(self, audit):
        for _ in range(10):
            audit.record(**_record_kwargs(agent_id="agent-X"))
        history = audit.get_agent_history("agent-X", limit=3)
        assert len(history) == 3


class TestGetSessionHistory:
    def test_returns_records_for_session(self, audit):
        audit.record(**_record_kwargs(session_id="sess-A"))
        audit.record(**_record_kwargs(session_id="sess-A"))
        audit.record(**_record_kwargs(session_id="sess-B"))
        history = audit.get_session_history("sess-A")
        assert len(history) == 2
        assert all(r.session_id == "sess-A" for r in history)

    def test_empty_for_unknown_session(self, audit):
        assert audit.get_session_history("no-such-session") == []
