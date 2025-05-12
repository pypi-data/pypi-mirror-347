import os
import yaml
from typing import Optional
from .verifiers.sentence_verifier import SentenceTransformerVerifier
from .logger.audit import AuditLogger


class PolicyEngine:
    """
    Evaluates whether a given tool action complies with safety policies.
    Uses rule types such as deny_phrase and semantic checks.
    """

    VALID_RULE_TYPES = {"deny_phrase", "semantic"}

    def __init__(
        self,
        policy_path: Optional[str] = None,
        policy_base_dir: Optional[str] = None
    ):
        self.base_dir = policy_base_dir or os.path.dirname(__file__)
        policy_path = policy_path or os.path.join(self.base_dir, "policies", "policy.yaml")

        with open(policy_path, encoding="utf-8") as f:
            self.policy_cfg = yaml.safe_load(f)

        self.verifier = SentenceTransformerVerifier(
            model_name="all-MiniLM-L6-v2",
            low_threshold=0.50,
            high_threshold=0.75,
        )

        self.audit_logger = AuditLogger()

    def _load_reference_text(self, filename: str) -> str:
        path = os.path.join(self.base_dir, "policies", filename)
        with open(path, encoding="utf-8") as f:
            return f.read().strip().lower()

    def evaluate_policy(self, tool_name: str, args: dict, agent_id: str = "unknown") -> Optional[str]:
        """
        Returns None if allowed, or a string reason if blocked.
        Supports modular rule types per tool.
        """
        tool_rules = self.policy_cfg.get("tools", {}).get(tool_name)
        if not tool_rules:
            return None  # No policy = allow

        text = (args.get("body") or args.get("note") or "").strip().lower()
        if not text:
            return None  # Empty input = allow

        for check in tool_rules.get("checks", []):
            rule_type = check.get("type")

            if rule_type not in self.VALID_RULE_TYPES:
                warning = f"Unknown rule type in policy: '{rule_type}' for tool: '{tool_name}'"
                self.audit_logger.log(
                    agent_id=agent_id,
                    tool=tool_name,
                    allowed=True,
                    reason=warning
                )
                continue

            if rule_type == "deny_phrase":
                for phrase in check.get("phrases", []):
                    if phrase.lower() in text:
                        reason = f"Blocked: matched deny phrase “{phrase}”"
                        self.audit_logger.log(
                            agent_id=agent_id,
                            tool=tool_name,
                            allowed=False,
                            reason=reason
                        )
                        return reason

            elif rule_type == "semantic":
                trigger_phrases = [p.lower() for p in check.get("trigger_phrases", [])]
                if any(p in text for p in trigger_phrases):
                    reference_file = check.get("reference_file")
                    if not reference_file:
                        continue

                    reference_text = self._load_reference_text(reference_file)
                    decision = self.verifier.decision(candidate=text, official=reference_text)

                    if decision == "block":
                        explanation = self.verifier.explain(candidate=text, official=reference_text)
                        reason = f"Blocked by semantic check: {explanation}"
                        self.audit_logger.log(
                            agent_id=agent_id,
                            tool=tool_name,
                            allowed=False,
                            reason=reason
                        )
                        return reason

                    self.audit_logger.log(
                        agent_id=agent_id,
                        tool=tool_name,
                        allowed=True,
                        reason=f"Semantic decision: {decision}"
                    )

        return None
