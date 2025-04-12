import os
import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_loader_valid_file(tmp_path):
    from orka.loader import YAMLLoader
    file = tmp_path / "orka.yaml"
    file.write_text("orchestrator:\n  id: test\nagents: []")
    loader = YAMLLoader(str(file))
    assert loader.get_orchestrator()['id'] == "test"
    assert loader.get_agents() == []

def test_loader_validation_errors(tmp_path):
    from orka.loader import YAMLLoader
    file = tmp_path / "invalid.yaml"
    file.write_text("agents: []")
    loader = YAMLLoader(str(file))
    try:
        loader.validate()
    except ValueError as e:
        assert "orchestrator" in str(e)
