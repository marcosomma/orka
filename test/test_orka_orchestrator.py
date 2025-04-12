import os
import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

class DummyAgent:
    def __init__(self, agent_id, prompt, queue, **kwargs):
        self.agent_id = agent_id
        self.prompt = prompt
        self.queue = queue
    def run(self, input_data): return f"processed: {input_data}"

def test_orchestrator_flow(monkeypatch, tmp_path):
    from orka.orchestrator import Orchestrator
    file = tmp_path / "orka.yaml"
    file.write_text("""
orchestrator:
  id: test
  agents: [a1, a2]
agents:
  - id: a1
    type: dummy
    prompt: test
    queue: q1
  - id: a2
    type: dummy
    prompt: test
    queue: q2
""")
    from orka import orchestrator
    orchestrator.AGENT_TYPES["dummy"] = DummyAgent
    o = Orchestrator(str(file))
    result = o.run("msg")
    assert "a1" in result and "a2" in result
