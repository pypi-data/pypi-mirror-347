from .engine import PolicyEnforcer
from .logger.audit import AuditLogger
from .helper.auth import validate_api_key


class SafenticError(Exception):
    """Raised when Safentic blocks an action."""
    pass


class InvalidAPIKeyError(Exception):
    """Raised when an invalid API key is used."""
    pass


class InvalidAgentInterfaceError(Exception):
    """Raised when the wrapped agent does not implement the required method."""
    pass


class SafetyLayer:
    """
    Wraps an agent with real-time enforcement of Safentic policies.
    All tool calls must go through `call_tool()`.

    Example:
        agent = SafetyLayer(MyAgent(), api_key="...", agent_id="agent-001")
        agent.call_tool("send_email", {"to": "alice@example.com"})
    """

    def __init__(self, agent, api_key: str, agent_id: str = "", enforcer: PolicyEnforcer = None, raise_on_block: bool = True):
        if not api_key:
            raise InvalidAPIKeyError("Missing API key")

        validation_response = validate_api_key(api_key)
        if not validation_response or validation_response.get("status") != "valid":
            raise InvalidAPIKeyError("Invalid or unauthorized API key")

        if not hasattr(agent, "call_tool") or not callable(getattr(agent, "call_tool")):
            raise InvalidAgentInterfaceError("Wrapped agent must implement `call_tool(tool_name: str, **kwargs)`")

        self.agent = agent
        self.api_key = api_key
        self.agent_id = agent_id
        self.raise_on_block = raise_on_block
        self.logger = AuditLogger()
        self.enforcer = enforcer or PolicyEnforcer()
        self.enforcer.reset(agent_id)

    def call_tool(self, tool_name: str, tool_args: dict) -> dict:
        """
        Intercepts a tool call and enforces policies before execution.
        If blocked, raises `SafenticError` or returns an error response (configurable).
        """
        result = self.enforcer.enforce(self.agent_id, tool_name, tool_args)

        self.logger.log(
            agent_id=self.agent_id,
            tool=tool_name,
            allowed=result["allowed"],
            reason=result["reason"] if not result["allowed"] else None
        )

        if not result["allowed"]:
            if self.raise_on_block:
                raise SafenticError(result["reason"])
            return {"error": result["reason"]}

        return self.agent.call_tool(tool_name, **tool_args)
