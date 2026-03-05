"""Tests for the PolicyEngine."""

import pytest

from aegis.exceptions import AEGISPolicyError
from aegis.policy_engine import (
    Policy,
    PolicyCondition,
    PolicyEffect,
    PolicyEngine,
    PolicyResult,
)
from aegis.protocol import AGPAction, AGPContext, AGPRequest, ActionType, Decision


def make_request(agent_id: str = "agent-1", action_type: ActionType = ActionType.TOOL_CALL,
                 target: str = "my_tool") -> AGPRequest:
    return AGPRequest(
        agent_id=agent_id,
        action=AGPAction(type=action_type, target=target),
        context=AGPContext(session_id="sess-1"),
    )


def always_true(_req: AGPRequest) -> bool:
    return True


def always_false(_req: AGPRequest) -> bool:
    return False


def make_allow_policy(policy_id: str = "pol-allow", priority: int = 200) -> Policy:
    return Policy(
        id=policy_id,
        name="Allow All",
        description="Allows everything",
        effect=PolicyEffect.ALLOW,
        conditions=[PolicyCondition(evaluate=always_true, description="always true")],
        priority=priority,
    )


def make_deny_policy(policy_id: str = "pol-deny", priority: int = 100) -> Policy:
    return Policy(
        id=policy_id,
        name="Deny All",
        description="Denies everything",
        effect=PolicyEffect.DENY,
        conditions=[PolicyCondition(evaluate=always_true, description="always true")],
        priority=priority,
    )


@pytest.fixture()
def engine() -> PolicyEngine:
    return PolicyEngine()


class TestPolicyManagement:
    def test_add_and_retrieve(self, engine):
        policy = make_allow_policy()
        engine.add_policy(policy)
        assert engine.get_policy("pol-allow") is policy

    def test_duplicate_policy_raises(self, engine):
        engine.add_policy(make_allow_policy())
        with pytest.raises(ValueError, match="already registered"):
            engine.add_policy(make_allow_policy())

    def test_remove_policy(self, engine):
        engine.add_policy(make_allow_policy())
        engine.remove_policy("pol-allow")
        assert engine.get_policy("pol-allow") is None

    def test_list_policies_sorted_by_priority(self, engine):
        engine.add_policy(make_allow_policy("p1", priority=300))
        engine.add_policy(make_deny_policy("p2", priority=100))
        ids = [p.id for p in engine.list_policies()]
        assert ids == ["p2", "p1"]


class TestDefaultDeny:
    def test_no_policies_means_denied(self, engine):
        result = engine.evaluate(make_request())
        assert result.decision == Decision.DENIED
        assert "default-deny" in result.reason

    def test_no_matching_policy_means_denied(self, engine):
        engine.add_policy(Policy(
            id="pol-never-match",
            name="Never Match",
            description="",
            effect=PolicyEffect.ALLOW,
            conditions=[PolicyCondition(evaluate=always_false, description="always false")],
        ))
        result = engine.evaluate(make_request())
        assert result.decision == Decision.DENIED


class TestAllowPolicy:
    def test_matching_allow_approves(self, engine):
        engine.add_policy(make_allow_policy())
        result = engine.evaluate(make_request())
        assert result.decision == Decision.APPROVED
        assert "Allow All" in result.reason


class TestDenyPolicy:
    def test_matching_deny_denies(self, engine):
        engine.add_policy(make_deny_policy())
        result = engine.evaluate(make_request())
        assert result.decision == Decision.DENIED
        assert "Deny All" in result.reason

    def test_deny_overrides_allow_when_higher_priority(self, engine):
        # Deny has priority=50 (evaluated first), allow has priority=200
        engine.add_policy(make_allow_policy("pol-allow", priority=200))
        engine.add_policy(make_deny_policy("pol-deny", priority=50))
        result = engine.evaluate(make_request())
        assert result.decision == Decision.DENIED

    def test_allow_wins_when_deny_does_not_match(self, engine):
        # Deny condition never matches
        engine.add_policy(Policy(
            id="pol-deny",
            name="Deny (no match)",
            description="",
            effect=PolicyEffect.DENY,
            conditions=[PolicyCondition(evaluate=always_false, description="")],
            priority=50,
        ))
        engine.add_policy(make_allow_policy())
        result = engine.evaluate(make_request())
        assert result.decision == Decision.APPROVED


class TestDisabledPolicy:
    def test_disabled_policy_is_skipped(self, engine):
        policy = make_allow_policy()
        policy.enabled = False
        engine.add_policy(policy)
        result = engine.evaluate(make_request())
        assert result.decision == Decision.DENIED  # default-deny because policy skipped


class TestEvaluationTrace:
    def test_evaluations_returned(self, engine):
        engine.add_policy(make_allow_policy())
        result = engine.evaluate(make_request())
        assert len(result.evaluations) == 1
        ev = result.evaluations[0]
        assert ev.policy_id == "pol-allow"
        assert ev.matched is True
        assert ev.effect == "allow"

    def test_deny_stops_evaluation_early(self, engine):
        # Deny is at priority=50, allow at 200. After deny matches, we stop.
        engine.add_policy(make_allow_policy("pol-allow", priority=200))
        engine.add_policy(make_deny_policy("pol-deny", priority=50))
        result = engine.evaluate(make_request())
        # Only the deny policy should be in evaluations (we stopped after match)
        assert result.evaluations[-1].policy_id == "pol-deny"
        assert result.evaluations[-1].matched is True


class TestConditionError:
    def test_condition_exception_raises_policy_error(self, engine):
        def bad_condition(_req):
            raise RuntimeError("oops")

        engine.add_policy(Policy(
            id="bad-pol",
            name="Bad",
            description="",
            effect=PolicyEffect.ALLOW,
            conditions=[PolicyCondition(evaluate=bad_condition, description="bad")],
        ))
        with pytest.raises(AEGISPolicyError, match="oops"):
            engine.evaluate(make_request())


class TestConditionalPolicy:
    def test_agent_specific_allow(self, engine):
        engine.add_policy(Policy(
            id="pol-agent-specific",
            name="Allow agent-A only",
            description="",
            effect=PolicyEffect.ALLOW,
            conditions=[
                PolicyCondition(
                    evaluate=lambda req: req.agent_id == "agent-A",
                    description="agent is agent-A",
                )
            ],
        ))
        assert engine.evaluate(make_request(agent_id="agent-A")).decision == Decision.APPROVED
        assert engine.evaluate(make_request(agent_id="agent-B")).decision == Decision.DENIED
