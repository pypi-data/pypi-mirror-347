from sentence_transformers import SentenceTransformer, util
from ..logger.audit import AuditLogger


class SentenceTransformerVerifier:
    """
    Verifies whether a candidate text is semantically aligned with an official policy text.
    Uses cosine similarity thresholds to decide: allow, verify, or block.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        low_threshold: float = 0.50,
        high_threshold: float = 0.75,
    ):
        self.embedder = SentenceTransformer(model_name)
        self.low = low_threshold
        self.high = high_threshold
        self.logger = AuditLogger()

    def similarity(self, a: str, b: str) -> float:
        """
        Computes cosine similarity between two strings.
        """
        vecs = self.embedder.encode([a, b], convert_to_tensor=True)
        return util.cos_sim(vecs[0], vecs[1]).item()

    def decision(self, candidate: str, official: str, agent_id: str = "semantic-check") -> str:
        """
        Returns one of: "allow", "verify", or "block"
        based on similarity thresholds.
        Also logs the similarity score and decision.
        """
        score = self.similarity(candidate, official)

        if score >= self.high:
            result = "allow"
        elif score <= self.low:
            result = "block"
        else:
            result = "verify"

        self.logger.log(
            agent_id=agent_id,
            tool="semantic_policy_check",
            allowed=(result != "block"),
            reason=f"Semantic decision: {result} (score={score:.2f})"
        )

        return result

    def explain(self, candidate: str, official: str, agent_id: str = "semantic-check") -> str:
        """
        Returns a debug-friendly explanation string including the similarity score.
        Also logs it to structured audit log for traceability.
        """
        score = self.similarity(candidate, official)
        explanation = f"Semantic similarity = {score:.2f} (low={self.low}, high={self.high})"

        # Structured debug logging (allowed=True since it’s informational)
        self.logger.log(
            agent_id=agent_id,
            tool="semantic_policy_check",
            allowed=True,
            reason=explanation
        )

        return explanation
