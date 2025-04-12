import os
import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

@pytest.fixture
def example_yaml(tmp_path):
    yaml_content = '''\
orchestrator:
  id: fact-checker
  strategy: sequential
  queue: orka:fact-core
  agents:
    - domain_classifier
    - is_fact

agents:
  - id: domain_classifier
    type: openai-classification
    prompt: >
      Classify this question into one of the following domains:
      - science, geography, history, technology, date check, general
    options: [science, geography, history, technology, date check, general]
    queue: orka:domain

  - id: is_fact
    type: openai-binary
    prompt: >
      Is this a {{ input }} factual assertion that can be verified externally? Answer TRUE or FALSE.
    queue: validation_queue
    '''
    config_file = tmp_path / "example_valid.yml"
    config_file.write_text(yaml_content)
    print(f"YAML config file created at: {config_file}")
    return config_file

def test_env_variables():
    assert os.getenv("OPENAI_API_KEY") is not None
    assert os.getenv("BASE_OPENAI_MODEL") is not None

def test_yaml_structure(example_yaml):
    import yaml
    data = yaml.safe_load(example_yaml.read_text())
    assert "agents" in data
    assert "orchestrator" in data
    assert isinstance(data["agents"], list)
    assert isinstance(data["orchestrator"]["agents"], list)
    assert len(data["agents"]) == len(data["orchestrator"]["agents"])

def test_run_orka(monkeypatch, example_yaml):
    # Mock the core agent system
    monkeypatch.setenv("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    monkeypatch.setenv("BASE_OPENAI_MODEL", os.getenv("BASE_OPENAI_MODEL"))
    
    # Simulate CLI logic (replace with actual OrKa call if available)
    from orka.orka_cli import run_cli_entrypoint

    try:
        print(f"example_yaml: {str(example_yaml)}")
        run_cli_entrypoint(
            config_path=str(example_yaml),
            input_text="What is the capital of France?",
            log_to_file=False,
        )
    except Exception as e:
        pytest.fail(f"Execution failed: {e}")