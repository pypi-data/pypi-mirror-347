# Safentic SDK

Safentic is a runtime guardrail SDK for agentic AI systems.  
It intercepts and evaluates unsafe tool calls between agent **intent** and **execution**, enforcing custom safety policies.

---

## Installation

Install from PyPI:

    pip install safentic

---

## API Key Required

Safentic requires a valid API key to function.  
To obtain one, contact: contact@safentic.com

---

## Quick Start

```python
from safentic import SafetyLayer, SafenticError

layer = SafetyLayer(api_key="your-api-key", agent_id="agent-007")

try:
    layer.protect("send_email", {"body": "Refund me now!"})
except SafenticError as e:
    print("Blocked by policy:", e)
