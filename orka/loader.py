import yaml

class YAMLLoader:
    def __init__(self, path):
        self.path = path
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.path, 'r') as f:
            return yaml.safe_load(f)

    def get_orchestrator(self):
        return self.config.get('orchestrator', {})

    def get_agents(self):
        return self.config.get('agents', [])

    def validate(self):
        if 'orchestrator' not in self.config:
            raise ValueError("Missing 'orchestrator' section in config")
        if 'agents' not in self.config:
            raise ValueError("Missing 'agents' section in config")
        if not isinstance(self.config['agents'], list):
            raise ValueError("'agents' should be a list")
        return True