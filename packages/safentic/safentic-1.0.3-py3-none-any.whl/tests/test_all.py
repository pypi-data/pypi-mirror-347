import os
import math
import pytest
from unittest import mock

from safentic.policy import PolicyEngine
from safentic.engine import PolicyEnforcer
from safentic.layer import SafetyLayer, SafenticError
from safentic.verifiers.sentence_verifier import SentenceTransformerVerifier
from safentic.logger.audit import AuditLogger

os.environ["SAFE_AUDIT_LOG"] = "0"

TESTS = {
    "valid_excerpt": "Here is our refund policy: any cancellation within 30 days of purchase receives a full refund.",
    "hallucination_one_device": "According to our refund policy, every user may only refund one device per subscription.",
    "made_up_timeframe": "Refund policy: you must request a refund within 24 hours of purchase.",
    "generic_refund": "I’m sorry for the trouble—please let us know more about your refund issue.",
}

@pytest.fixture
def policy_engine():
    return PolicyEngine()

@pytest.fixture
def enforcer():
    return PolicyEnforcer()

@pytest.mark.parametrize("case, expected_contains", [
    ("valid_excerpt", "refund"),
    ("generic_refund", "sorry"),
    ("hallucination_one_device", "one device per subscription"),
    ("made_up_timeframe", "24 hours"),
])
def test_policy_engine_evaluate(policy_engine, case, expected_contains):
    reason = policy_engine.evaluate_policy("send_email", {"body": TESTS[case]})
    assert expected_contains in reason.lower()

def test_policy_engine_skips_empty(policy_engine):
    assert policy_engine.evaluate_policy("send_email", {"body": ""}) is None

def test_policy_engine_unknown_rule_type(policy_engine):
    policy_engine.policy_cfg = {
        "tools": {"send_email": {"checks": [{"type": "unknown_type"}]}}
    }
    assert policy_engine.evaluate_policy("send_email", {"body": "test"}) is None

def test_policy_engine_malformed_semantic(policy_engine):
    policy_engine.policy_cfg = {
        "tools": {"send_email": {"checks": [{"type": "semantic", "trigger_phrases": ["refund"]}]}}
    }
    assert policy_engine.evaluate_policy("send_email", {"body": "refund policy applies"}) is None

def test_enforcer_blocks_expected_cases(enforcer):
    agent_id = "agent-block"
    for case in ["valid_excerpt", "generic_refund"]:
        result = enforcer.enforce(agent_id, "send_email", {"body": TESTS[case]})
        assert not result["allowed"]

def test_enforcer_blocks_and_resets(enforcer):
    agent_id = "agent-reset"
    res = enforcer.enforce(agent_id, "send_email", {"body": TESTS["hallucination_one_device"]})
    assert not res["allowed"]
    repeat = enforcer.enforce(agent_id, "send_email", {"body": TESTS["hallucination_one_device"]})
    assert "previously blocked" in repeat["reason"].lower()
    enforcer.reset(agent_id)
    assert agent_id not in enforcer.agent_states

def test_safety_layer_blocks_and_raises():
    layer = SafetyLayer(api_key="demo-1234", agent_id="safety-1", raise_on_block=True)
    with pytest.raises(SafenticError):
        layer.protect("send_email", {"body": TESTS["made_up_timeframe"]})

def test_safety_layer_returns_result():
    safe_input = {"body": "This is a neutral and policy-safe email message."}
    layer = SafetyLayer(api_key="demo-1234", agent_id="safety-2", raise_on_block=False)
    assert layer.protect("send_email", safe_input)["allowed"]

@mock.patch("safentic.verifiers.sentence_verifier.SentenceTransformer")
def test_similarity_score_consistency(mock_model_class):
    mock_model = mock_model_class.return_value
    mock_model.encode.return_value = [[1.0], [1.0]]
    verifier = SentenceTransformerVerifier()
    score = verifier.similarity("a", "a")
    assert math.isclose(score, 1.0, abs_tol=1e-4)

@mock.patch("safentic.verifiers.sentence_verifier.SentenceTransformer")
@pytest.mark.parametrize("a,b,score,expected", [
    ("a", "a", 0.95, "allow"),
    ("a", "b", 0.5, "verify"),
    ("x", "y", 0.1, "block"),
])
def test_verifier_threshold_behavior(mock_model_class, a, b, score, expected):
    mock_model = mock_model_class.return_value
    with mock.patch("safentic.verifiers.sentence_verifier.util.cos_sim") as mock_cos_sim:
        mock_cos_sim.return_value = mock.Mock()
        mock_cos_sim.return_value.item.return_value = score

        verifier = SentenceTransformerVerifier(low_threshold=0.2, high_threshold=0.9)
        result = verifier.decision(a, b)
        assert result == expected

@mock.patch("safentic.verifiers.sentence_verifier.SentenceTransformer")
def test_verifier_explains_score(mock_model_class):
    mock_model = mock_model_class.return_value
    mock_model.encode.return_value = [[1.0], [1.0]]
    verifier = SentenceTransformerVerifier()
    assert "Semantic similarity" in verifier.explain("a", "a")

@mock.patch("safentic.logger.audit.open", new_callable=mock.mock_open)
def test_logger_set_level_and_log(mock_open_file):
    os.environ["SAFE_AUDIT_LOG"] = "1"
    logger = AuditLogger(config={"txt": "dummy.txt", "json": "dummy.jsonl"})
    logger.set_level("DEBUG")
    logger.log(agent_id="mock-agent", tool="send_email", allowed=True)
    logger.log(agent_id="mock-agent", tool="send_email", allowed=False, reason="test")
    handle = mock_open_file()
    handle.write.assert_called()

def test_logger_invalid_level():
    with pytest.raises(ValueError):
        AuditLogger().set_level("FAKE")

@mock.patch("safentic.logger.audit.open", side_effect=OSError("mocked failure"))
def test_logger_gracefully_fails_json_write(mock_open):
    logger = AuditLogger(config={"txt": "ok.txt", "json": "fail.jsonl"})
    logger.log("agent", "tool", False, reason="test")
