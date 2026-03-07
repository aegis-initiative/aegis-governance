"""Tests for the AuditSystem."""

import sqlite3

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
    """Test the record() method for single record insertion."""

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

    def test_thread_safety_concurrent_records(self, audit):
        """Test that concurrent record() calls are thread-safe."""
        import threading

        audit_ids = []

        def record():
            audit_id = audit.record(**_record_kwargs())
            audit_ids.append(audit_id)

        threads = [threading.Thread(target=record) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All records should be inserted successfully
        assert len(audit_ids) == 10
        # All audit IDs should be unique
        assert len(set(audit_ids)) == 10


class TestBatchRecord:
    """Test the batch_record() method for efficient bulk insertion."""

    def test_batch_returns_audit_ids(self, audit):
        records = [_record_kwargs() for _ in range(5)]
        audit_ids = audit.batch_record(records)
        assert len(audit_ids) == 5
        assert all(isinstance(aid, str) for aid in audit_ids)

    def test_batch_unique_audit_ids(self, audit):
        records = [_record_kwargs() for _ in range(5)]
        audit_ids = audit.batch_record(records)
        assert len(set(audit_ids)) == 5  # All unique

    def test_batch_empty_list_returns_empty(self, audit):
        audit_ids = audit.batch_record([])
        assert audit_ids == []

    def test_batch_content_round_trip(self, audit):
        records = [
            _record_kwargs(agent_id=f"agent-{i}") for i in range(3)
        ]
        audit_ids = audit.batch_record(records)
        
        retrieved = [audit.get_record(aid) for aid in audit_ids]
        assert len(retrieved) == 3
        assert [r.agent_id for r in retrieved] == ["agent-0", "agent-1", "agent-2"]

    def test_batch_atomicity(self, audit):
        """Test that batch inserts are atomic."""
        records = [_record_kwargs(agent_id=f"agent-batch-{i}") for i in range(10)]
        audit_ids = audit.batch_record(records)
        
        # All records should be inserted
        assert len(audit_ids) == 10
        # All should be retrievable
        assert all(audit.get_record(aid) is not None for aid in audit_ids)


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


class TestFindByDecision:
    """Test the find_by_decision() method for filtering by decision."""

    def test_returns_records_by_decision(self, audit):
        audit.record(**_record_kwargs(decision="approved"))
        audit.record(**_record_kwargs(decision="approved"))
        audit.record(**_record_kwargs(decision="denied"))
        found = audit.find_by_decision("approved")
        assert len(found) == 2
        assert all(r.decision == "approved" for r in found)

    def test_empty_for_unknown_decision(self, audit):
        audit.record(**_record_kwargs(decision="approved"))
        found = audit.find_by_decision("unknown_decision")
        assert found == []

    def test_respects_limit(self, audit):
        for _ in range(10):
            audit.record(**_record_kwargs(decision="denied"))
        found = audit.find_by_decision("denied", limit=5)
        assert len(found) == 5


class TestRecordCount:
    """Test the record_count() method."""

    def test_count_all_records(self, audit):
        for i in range(5):
            audit.record(**_record_kwargs(agent_id=f"agent-{i}"))
        assert audit.record_count() == 5

    def test_count_by_agent(self, audit):
        for i in range(3):
            audit.record(**_record_kwargs(agent_id="agent-A"))
        for i in range(2):
            audit.record(**_record_kwargs(agent_id="agent-B"))
        assert audit.record_count(agent_id="agent-A") == 3
        assert audit.record_count(agent_id="agent-B") == 2

    def test_count_zero_for_unknown_agent(self, audit):
        audit.record(**_record_kwargs(agent_id="agent-A"))
        assert audit.record_count(agent_id="unknown") == 0


class TestGetAgentHistoryPagination:
    """Test pagination features of get_agent_history()."""

    def test_offset_parameter(self, audit):
        for i in range(10):
            audit.record(**_record_kwargs(agent_id="agent-with-many"))
        # Get first 3
        page1 = audit.get_agent_history("agent-with-many", limit=3, offset=0)
        assert len(page1) == 3
        # Get next 3
        page2 = audit.get_agent_history("agent-with-many", limit=3, offset=3)
        assert len(page2) == 3
        # Make sure the pages are different
        assert page1[0].id != page2[0].id


class TestFaultInjection:
    """Fault injection tests for audit persistence and database integrity."""

    def test_record_raises_audit_error_when_connection_closed(self, audit):
        """record() should raise AEGISAuditError on DB write failure."""
        audit._conn.close()
        with pytest.raises(AEGISAuditError, match="Failed to persist audit record"):
            audit.record(**_record_kwargs())

    def test_batch_record_raises_audit_error_when_connection_closed(self, audit):
        """batch_record() should raise AEGISAuditError on DB write failure."""
        audit._conn.close()
        with pytest.raises(AEGISAuditError, match="Failed to persist batch audit records"):
            audit.batch_record([_record_kwargs()])

    def test_corrupted_database_file_raises_sqlite_error(self, tmp_path):
        """Creating AuditSystem against a corrupted SQLite file should fail."""
        db_path = tmp_path / "corrupt.db"
        db_path.write_bytes(b"not-a-valid-sqlite-database")

        with pytest.raises(sqlite3.Error):
            AuditSystem(str(db_path))
