"""Audit System.

Provides an immutable, append-only record of every governance decision
made by AEGIS.  Records are stored in a SQLite database and can be
queried for compliance reporting and forensic review.

Design principles
-----------------
* **Immutable** – records are never updated or deleted.
* **Complete** – every AGP request/response pair is recorded regardless
  of the decision outcome.
* **Queryable** – records can be retrieved by audit ID, agent ID, or session.
* **Thread-safe** – all database operations are protected by locks for
  concurrent access from multiple agents.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .exceptions import AEGISAuditError


@dataclass(frozen=True)
class AuditRecord:
    """An immutable record of a single governance decision.
    
    Parameters
    ----------
    id : str
        Unique identifier for this audit record.
    request_id : str
        The AGPRequest identifier this audit record documents.
    agent_id : str
        The agent ID that submitted the request.
    action_type : str
        The type of action that was evaluated.
    action_target : str
        The target resource for the action.
    action_parameters : dict
        The action parameters submitted.
    decision : str
        The governance decision (APPROVED, DENIED, etc.).
    reason : str
        Human-readable explanation of the decision.
    policy_evaluations : list
        List of policy evaluation results.
    session_id : str
        The session identifier for this request.
    timestamp : str
        ISO 8601 timestamp when this record was created.
    """

    id: str
    request_id: str
    agent_id: str
    action_type: str
    action_target: str
    action_parameters: dict[str, Any]
    decision: str
    reason: str
    policy_evaluations: list[dict[str, Any]]
    session_id: str
    timestamp: str


class AuditSystem:
    """SQLite-backed, append-only, thread-safe governance audit trail.

    The AuditSystem provides immutable storage of all governance decisions
    with efficient querying by audit ID, agent ID, or session.  All database
    operations use threading locks to ensure thread-safety for concurrent
    access from multiple AI agents.

    Parameters
    ----------
    db_path : str
        File path for the SQLite database.  Defaults to ``":memory:"``
        which is useful for testing.
        
    Raises
    ------
    AEGISAuditError
        If the database cannot be initialized.
    """

    _CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS audit_records (
            id                 TEXT PRIMARY KEY,
            request_id         TEXT NOT NULL,
            agent_id           TEXT NOT NULL,
            action_type        TEXT NOT NULL,
            action_target      TEXT NOT NULL,
            action_parameters  TEXT NOT NULL,
            decision           TEXT NOT NULL,
            reason             TEXT NOT NULL,
            policy_evaluations TEXT NOT NULL,
            session_id         TEXT NOT NULL,
            timestamp          TEXT NOT NULL
        )
    """

    _COLUMNS = (
        "id",
        "request_id",
        "agent_id",
        "action_type",
        "action_target",
        "action_parameters",
        "decision",
        "reason",
        "policy_evaluations",
        "session_id",
        "timestamp",
    )

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute(self._CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def record(
        self,
        *,
        request_id: str,
        agent_id: str,
        action_type: str,
        action_target: str,
        action_parameters: dict[str, Any],
        decision: str,
        reason: str,
        policy_evaluations: list[dict[str, Any]],
        session_id: str,
    ) -> str:
        """Append a governance decision to the audit trail.
        
        This method is thread-safe and ensures that the audit record is
        persisted atomically before returning.

        Parameters
        ----------
        request_id : str
            The AGPRequest identifier.
        agent_id : str
            The agent ID of the request submitter.
        action_type : str
            The action type being audited.
        action_target : str
            The target resource for the action.
        action_parameters : dict
            The parameters submitted with the action.
        decision : str
            The governance decision outcome.
        reason : str
            Explanation of the decision.
        policy_evaluations : list
            Policy evaluation results.
        session_id : str
            The session identifier.

        Returns
        -------
        str
            The newly generated audit record ID (UUID).

        Raises
        ------
        AEGISAuditError
            If the record cannot be persisted to the database.
        """
        audit_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        with self._lock:
            try:
                self._conn.execute(
                    f"INSERT INTO audit_records ({', '.join(self._COLUMNS)}) "  # noqa: S608
                    f"VALUES ({', '.join(['?'] * len(self._COLUMNS))})",
                    (
                        audit_id,
                        request_id,
                        agent_id,
                        action_type,
                        action_target,
                        json.dumps(action_parameters),
                        decision,
                        reason,
                        json.dumps(policy_evaluations),
                        session_id,
                        timestamp,
                    ),
                )
                self._conn.commit()
            except sqlite3.Error as exc:
                raise AEGISAuditError(
                    f"Failed to persist audit record: {exc}",
                    error_code="AUDIT_PERSIST_ERROR"
                ) from exc

        return audit_id

    def batch_record(
        self,
        records: list[dict[str, Any]],
    ) -> list[str]:
        """Append multiple governance decisions to the audit trail in a batch.
        
        This method is more efficient than calling :meth:`record` multiple
        times, as it batches all inserts into a single transaction. All records
        are inserted atomically.

        Parameters
        ----------
        records : list[dict]
            A list of dictionaries, each containing the keyword arguments for
            a single record (request_id, agent_id, action_type, etc.).

        Returns
        -------
        list[str]
            List of newly generated audit record IDs, in the same order as
            the input records.

        Raises
        ------
        AEGISAuditError
            If any record cannot be persisted.
        """
        if not records:
            return []

        audit_ids = [str(uuid.uuid4()) for _ in records]
        timestamp = datetime.now(timezone.utc).isoformat()

        with self._lock:
            try:
                for audit_id, record_data in zip(audit_ids, records):
                    self._conn.execute(
                        f"INSERT INTO audit_records ({', '.join(self._COLUMNS)}) "  # noqa: S608
                        f"VALUES ({', '.join(['?'] * len(self._COLUMNS))})",
                        (
                            audit_id,
                            record_data["request_id"],
                            record_data["agent_id"],
                            record_data["action_type"],
                            record_data["action_target"],
                            json.dumps(record_data["action_parameters"]),
                            record_data["decision"],
                            record_data["reason"],
                            json.dumps(record_data["policy_evaluations"]),
                            record_data["session_id"],
                            timestamp,
                        ),
                    )
                self._conn.commit()
            except sqlite3.Error as exc:
                raise AEGISAuditError(
                    f"Failed to persist batch audit records: {exc}",
                    error_code="BATCH_PERSIST_ERROR"
                ) from exc

        return audit_ids

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_record(self, audit_id: str) -> AuditRecord | None:
        """Retrieve a single audit record by its ID.
        
        Parameters
        ----------
        audit_id : str
            The audit record ID to retrieve.
            
        Returns
        -------
        AuditRecord or None
            The audit record if found, None otherwise.
        """
        with self._lock:
            cursor = self._conn.execute(
                "SELECT * FROM audit_records WHERE id = ?", (audit_id,)
            )
            row = cursor.fetchone()
        return self._row_to_record(row) if row else None

    def get_agent_history(
        self, agent_id: str, *, limit: int = 100, offset: int = 0
    ) -> list[AuditRecord]:
        """Return the most recent audit records for a given agent.
        
        Parameters
        ----------
        agent_id : str
            The agent identifier to retrieve history for.
        limit : int, optional
            Maximum number of records to return. Defaults to 100.
        offset : int, optional
            Number of records to skip. Defaults to 0. Useful for pagination.
            
        Returns
        -------
        list[AuditRecord]
            List of audit records, ordered by timestamp (newest first).
        """
        with self._lock:
            cursor = self._conn.execute(
                "SELECT * FROM audit_records "
                "WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (agent_id, limit, offset),
            )
            rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]

    def get_session_history(self, session_id: str) -> list[AuditRecord]:
        """Return all audit records for a given session.
        
        Parameters
        ----------
        session_id : str
            The session identifier to retrieve history for.
            
        Returns
        -------
        list[AuditRecord]
            List of audit records, ordered by timestamp (oldest first).
        """
        with self._lock:
            cursor = self._conn.execute(
                "SELECT * FROM audit_records "
                "WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,),
            )
            rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]

    def find_by_decision(
        self, decision: str, *, limit: int = 100
    ) -> list[AuditRecord]:
        """Find audit records by decision outcome.
        
        Parameters
        ----------
        decision : str
            The decision value to filter by (e.g., "APPROVED", "DENIED").
        limit : int, optional
            Maximum number of records to return. Defaults to 100.
            
        Returns
        -------
        list[AuditRecord]
            List of matching audit records, ordered by timestamp (newest first).
        """
        with self._lock:
            cursor = self._conn.execute(
                "SELECT * FROM audit_records "
                "WHERE decision = ? ORDER BY timestamp DESC LIMIT ?",
                (decision, limit),
            )
            rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]

    def record_count(self, agent_id: str | None = None) -> int:
        """Get the total number of audit records.
        
        Parameters
        ----------
        agent_id : str, optional
            If provided, count only records for this agent. Defaults to None
            (count all records).
            
        Returns
        -------
        int
            The number of audit records matching the criteria.
        """
        with self._lock:
            if agent_id is None:
                cursor = self._conn.execute("SELECT COUNT(*) FROM audit_records")
            else:
                cursor = self._conn.execute(
                    "SELECT COUNT(*) FROM audit_records WHERE agent_id = ?",
                    (agent_id,),
                )
            return cursor.fetchone()[0]  # type: ignore

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _row_to_record(self, row: tuple) -> AuditRecord:
        """Convert a database row to an AuditRecord."""
        data = dict(zip(self._COLUMNS, row))
        data["action_parameters"] = json.loads(data["action_parameters"])
        data["policy_evaluations"] = json.loads(data["policy_evaluations"])
        return AuditRecord(**data)
