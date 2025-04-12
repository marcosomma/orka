import os
import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_base_agent_fails():
    from orka.agents.agent_base import BaseAgent
    class Incomplete(BaseAgent): pass
    with pytest.raises(TypeError):
        Incomplete("id", "prompt", "queue")
