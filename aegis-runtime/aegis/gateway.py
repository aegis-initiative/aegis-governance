"""Governance Gateway.

The Governance Gateway is the single, validated entry point through
which AI agents submit :class:`~aegis.protocol.AGPRequest` objects for
governance review.

Responsibilities
----------------
* **Schema validation** – rejects structurally or semantically invalid
  requests before they reach the Decision Engine.
* **Semantic validation** – validates agent IDs, action types, and request
  completeness according to AEGIS governance rules.
* **Routing** – forwards valid requests to the :class:`~aegis.decision_engine.DecisionEngine`.

All interaction with AEGIS from external code should go through this
class rather than calling the Decision Engine directly.
"""

from __future__ import annotations

import re
from .decision_engine import DecisionEngine
from .exceptions import AEGISValidationError
from .protocol import AGPRequest, AGPResponse, ActionType


# Regex for valid agent IDs: alphanumeric, hyphens, underscores, dots
_AGENT_ID_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')


class GovernanceGateway:
    """Validates and routes AGP requests to the Decision Engine.

    Parameters
    ----------
    decision_engine:
        The :class:`~aegis.decision_engine.DecisionEngine` instance that
        will evaluate governance decisions.
    """

    def __init__(self, decision_engine: DecisionEngine) -> None:
        self._engine = decision_engine

    def submit(self, request: AGPRequest) -> AGPResponse:
        """Submit a governance request.

        Parameters
        ----------
        request:
            The :class:`~aegis.protocol.AGPRequest` to evaluate.

        Returns
        -------
        AGPResponse
            The governance decision.

        Raises
        ------
        AEGISValidationError
            If the request is structurally or semantically invalid.
        """
        self._validate(request)
        return self._engine.evaluate(request)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self, request: AGPRequest) -> None:
        """Validate a governance request for structural and semantic correctness.
        
        Performs the following validation checks:
        
        1. **Request object validation** – AGPRequest instance exists
        2. **Agent ID validation** – non-empty, valid format
        3. **Action validation** – action type exists, target is non-empty
        4. **Action type compatibility** – validates target type matches action
        5. **Context validation** – session_id is non-empty, timestamp validity
        6. **Parameters validation** – parameters dict is valid, no None keys
        
        Raises
        ------
        AEGISValidationError
            If any validation check fails, with specific error message.
        """
        # Request object must exist
        if request is None:
            raise AEGISValidationError("AGPRequest object must not be None")
        
        # Validate agent_id
        self._validate_agent_id(request.agent_id)
        
        # Validate action
        if request.action is None:
            raise AEGISValidationError("AGPRequest.action must not be None")
        self._validate_action(request.action)
        
        # Validate context
        if request.context is None:
            raise AEGISValidationError("AGPRequest.context must not be None")
        self._validate_context(request.context)
        
        # Validate request_id
        if not request.request_id or not request.request_id.strip():
            raise AEGISValidationError("AGPRequest.request_id must not be empty")
    
    def _validate_agent_id(self, agent_id: str) -> None:
        """Validate agent ID format and content.
        
        Agent IDs must:
        - Be non-empty and non-whitespace
        - Contain only alphanumeric characters, hyphens, underscores, dots
        - Not exceed 256 characters
        
        Parameters
        ----------
        agent_id : str
            The agent identifier to validate.
            
        Raises
        ------
        AEGISValidationError
            If agent_id is invalid.
        """
        if not agent_id or not agent_id.strip():
            raise AEGISValidationError(
                "AGPRequest.agent_id must not be empty",
                error_code="EMPTY_AGENT_ID"
            )
        
        if len(agent_id) > 256:
            raise AEGISValidationError(
                f"AGPRequest.agent_id exceeds maximum length (256): {len(agent_id)}",
                error_code="AGENT_ID_TOO_LONG"
            )
        
        if not _AGENT_ID_PATTERN.match(agent_id):
            raise AEGISValidationError(
                f"AGPRequest.agent_id contains invalid characters: {agent_id!r}",
                error_code="INVALID_AGENT_ID_FORMAT"
            )
    
    def _validate_action(self, action) -> None:
        """Validate action completeness and type compatibility.
        
        Parameters
        ----------
        action : AGPAction
            The action to validate.
            
        Raises
        ------
        AEGISValidationError
            If action is invalid.
        """
        if action.type is None:
            raise AEGISValidationError(
                "AGPRequest.action.type must not be None",
                error_code="MISSING_ACTION_TYPE"
            )
        
        if not isinstance(action.type, ActionType):
            raise AEGISValidationError(
                f"AGPRequest.action.type is not a valid ActionType: {action.type!r}",
                error_code="INVALID_ACTION_TYPE"
            )
        
        if not action.target or not action.target.strip():
            raise AEGISValidationError(
                "AGPRequest.action.target must not be empty",
                error_code="EMPTY_ACTION_TARGET"
            )
        
        if len(action.target) > 1024:
            raise AEGISValidationError(
                f"AGPRequest.action.target exceeds maximum length (1024): {len(action.target)}",
                error_code="TARGET_TOO_LONG"
            )
        
        # Validate parameters dict
        if action.parameters is None:
            raise AEGISValidationError(
                "AGPRequest.action.parameters must not be None",
                error_code="MISSING_PARAMETERS"
            )
        
        if not isinstance(action.parameters, dict):
            raise AEGISValidationError(
                f"AGPRequest.action.parameters must be a dict, got {type(action.parameters).__name__}",
                error_code="INVALID_PARAMETERS_TYPE"
            )
        
        # Check for None keys in parameters
        for key in action.parameters:
            if key is None:
                raise AEGISValidationError(
                    "AGPRequest.action.parameters contains None key",
                    error_code="NULL_PARAMETER_KEY"
                )
    
    def _validate_context(self, context) -> None:
        """Validate request context.
        
        Parameters
        ----------
        context : AGPContext
            The context to validate.
            
        Raises
        ------
        AEGISValidationError
            If context is invalid.
        """
        if not context.session_id or not context.session_id.strip():
            raise AEGISValidationError(
                "AGPRequest.context.session_id must not be empty",
                error_code="EMPTY_SESSION_ID"
            )
        
        if len(context.session_id) > 256:
            raise AEGISValidationError(
                f"AGPRequest.context.session_id exceeds maximum length (256): {len(context.session_id)}",
                error_code="SESSION_ID_TOO_LONG"
            )
        
        if context.timestamp is None:
            raise AEGISValidationError(
                "AGPRequest.context.timestamp must not be None",
                error_code="MISSING_TIMESTAMP"
            )
        
        if context.metadata is None:
            raise AEGISValidationError(
                "AGPRequest.context.metadata must not be None",
                error_code="MISSING_METADATA"
            )

