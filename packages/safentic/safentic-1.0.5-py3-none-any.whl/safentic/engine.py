import time
from .policy import PolicyEngine
from .logger.audit import AuditLogger


class PolicyEnforcer:
    """
    Runtime wrapper to evaluate and enforce tool usage policies.
    Tracks agent-specific violations, supports audit logging, and handles TTL-based tool blocks.
    """

    TOOL_BLOCK_TTL = 60  # seconds - how long a tool remains blocked after violation

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
            "blocked_tools": {},  # tool_name -> timestamp of block
            "violation_count": 0,
            "last_violation": None
        })

        # Check if tool is still blocked
        if self._is_tool_blocked(tool_name, state):
            reason = "Tool is temporarily blocked due to a prior violation."
            self.audit_logger.log(agent_id=agent_id, tool=tool_name, allowed=False, reason=reason)
            return self._deny(tool_name, state, reason)

        # Evaluate policy
        violation = self.policy_engine.evaluate_policy(tool_name, tool_args)

        if violation:
            # Example violation object: {"reason": "...", "level": "block"}
            level = violation.get("level", "block")
            reason = violation.get("reason", "Policy violation")

            if level == "warn":
                # Log a warning but allow the call
                self.audit_logger.log(agent_id=agent_id, tool=tool_name, allowed=True, reason=f"Warning: {reason}")
                return {
                    "allowed": True,
                    "reason": f"Warning: {reason}",
                    "agent_state": state
                }

            # Otherwise: enforce block
            state["blocked_tools"][tool_name] = time.time()
            state["violation_count"] += 1
            state["last_violation"] = violation
            self.audit_logger.log(agent_id=agent_id, tool=tool_name, allowed=False, reason=reason)
            return self._deny(tool_name, state, reason)

        # Allow
        self.audit_logger.log(agent_id=agent_id, tool=tool_name, allowed=True)
        return {
            "allowed": True,
            "reason": "Action permitted",
            "agent_state": state
        }

    def reset(self, agent_id: str = None):
        """Clears violation state for one or all agents."""
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

    def _is_tool_blocked(self, tool_name: str, state: dict) -> bool:
        """Checks if a tool is still blocked based on TTL."""
        blocked_at = state["blocked_tools"].get(tool_name)
        if not blocked_at:
            return False
        if time.time() - blocked_at > self.TOOL_BLOCK_TTL:
            # Tool block expired
            del state["blocked_tools"][tool_name]
            return False
        return True
