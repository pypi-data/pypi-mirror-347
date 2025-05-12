from .policy import PolicyEngine
from .logger.audit import AuditLogger

class PolicyEnforcer():
    """
    Runtime wrapper to evaluate and enforce tool usage policies.
    Tracks agent-specific violations and supports audit logging.
    """

    def __init__(self, policy_engine: PolicyEngine = None):
        self.policy_engine = policy_engine or PolicyEngine()
        self.agent_states = {}
        self.audit_logger = AuditLogger()

    def enforce(self, agent_id: str, tool_name: str, tool_args: dict) -> dict:
        """
        Evaluates a tool action for a given agent.
        Returns a dict with 'allowed', 'reason', and agent state metadata.
        """
        state = self.agent_states.setdefault(agent_id, {
            "blocked_tools": set(),
            "violation_count": 0,
            "last_violation": None
        })

        # Block repeat attempts to use already-denied tool
        if tool_name in state["blocked_tools"]:
            reason = "Tool previously blocked for this agent."
            self.audit_logger.log(
                agent_id=agent_id,
                tool=tool_name,
                allowed=False,
                reason=reason
            )
            return self._deny(tool_name, state, reason)

        # Run policy evaluation
        violation = self.policy_engine.evaluate_policy(tool_name, tool_args)

        if violation:
            state["blocked_tools"].add(tool_name)
            state["violation_count"] += 1
            state["last_violation"] = violation
            self.audit_logger.log(
                agent_id=agent_id,
                tool=tool_name,
                allowed=False,
                reason=violation
            )
            return self._deny(tool_name, state, violation)

        # Log allowed action
        self.audit_logger.log(
            agent_id=agent_id,
            tool=tool_name,
            allowed=True
        )

        return {
            "allowed": True,
            "reason": "Action permitted",
            "agent_state": state
        }

    def reset(self, agent_id: str = None):
        """
        Clears violation state for one agent or all agents.
        """
        if agent_id:
            self.agent_states.pop(agent_id, None)
        else:
            self.agent_states.clear()

    def _deny(self, tool_name: str, state: dict, reason: str) -> dict:
        return {
            "allowed": False,
            "reason": reason,
            "tool": tool_name,
            "agent_state": state
        }
