from .engine import PolicyEnforcer
from .logger.audit import AuditLogger
from .helper.auth import validate_api_key

class SafenticError(Exception):
    """Raised when Safentic blocks an action."""
    pass

class InvalidAPIKeyError(Exception):
    """Raised when an invalid API key is used."""
    pass

class SafetyLayer:
    """
    Safentic runtime enforcement wrapper for agent actions.
    Requires a valid API key to function.
    """

    def __init__(self, api_key: str = "", agent_id: str = "", enforcer: PolicyEnforcer = None, raise_on_block: bool = True):
        if not api_key:
            raise InvalidAPIKeyError("Missing API key")

        validation_response = validate_api_key(api_key)
        if not validation_response or validation_response.get("status") != "valid":
            raise InvalidAPIKeyError("Invalid or unauthorized API key")

        self.api_key = api_key
        self.agent_id = agent_id
        self.raise_on_block = raise_on_block
        self.logger = AuditLogger()

        self.enforcer = enforcer or PolicyEnforcer()
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

        if not result["allowed"]:
            if self.raise_on_block:
                raise SafenticError(result["reason"])
            return result

        return result