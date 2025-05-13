from .engine import PolicyEnforcer
from .logger.audit import AuditLogger
from .helper.auth import validate_api_key

class SafenticError(Exception):
    """Raised when Safentic blocks an action."""
    pass


class SafetyLayer():
    """
    Safentic runtime enforcement wrapper for agent actions.
    First, insert your api key, then run an action.
    Example:
        safety.protect("send_email", {"body": "..."})
        # Raises SafenticError if blocked
    """

    def __init__(self, api_key="", agent_id="", enforcer: PolicyEnforcer = None, raise_on_block: bool = True):
        self.agent_id = agent_id
        self.raise_on_block = raise_on_block
        self.logger = AuditLogger()

        self.enforcer = enforcer or PolicyEnforcer()
        self.api_key = validate_api_key(api_key)
        self.enforcer.reset(agent_id)

    def protect(self, tool_name: str, tool_args: dict) -> dict:
        """
        Checks whether a tool action is allowed.
        Raises SafenticError if blocked (default), or returns result if raise_on_block=False.
        """
            
        result = self.enforcer.enforce(self.agent_id, tool_name, tool_args)

        # Log structured event
        self.logger.log(
            agent_id=self.agent_id,
            tool=tool_name,
            allowed=result["allowed"],
            reason=result["reason"] if not result["allowed"] else None
        )

        # Raise or return based on outcome and config
        if not result["allowed"]:
            if self.raise_on_block:
                raise SafenticError(result["reason"])
            return result

        return result
