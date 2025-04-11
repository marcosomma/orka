import importlib
from .loader import YAMLLoader
from .agents import agents, llm_agents, google_duck_agents, router_agent
from .redis_interface import RedisQueue  # Placeholder for future implementation

AGENT_TYPES = {
    "binary": agents.BinaryAgent,
    "classification": agents.ClassificationAgent,
    "openai-binary": llm_agents.OpenAIBinaryAgent,
    "openai-classification": llm_agents.OpenAIClassificationAgent,
    "google-search": google_duck_agents.GoogleSearchAgent,
    "duckduckgo": google_duck_agents.DuckDuckGoAgent,
    "router": router_agent.RouterAgent,
}

class Orchestrator:
    def __init__(self, config_path):
        self.loader = YAMLLoader(config_path)
        self.loader.validate()
        self.orchestrator_cfg = self.loader.get_orchestrator()
        self.agent_cfgs = self.loader.get_agents()
        self.agents = self._init_agents()

    def _init_agents(self):
        instances = {}
        for cfg in self.agent_cfgs:
            agent_cls = AGENT_TYPES.get(cfg["type"])
            if not agent_cls:
                raise ValueError(f"Unsupported agent type: {cfg['type']}")

            clean_cfg = cfg.copy()
            clean_cfg.pop("type", None)
            clean_cfg["agent_id"] = clean_cfg.pop("id")  # <-- normalize 'id' to 'agent_id'

            agent = agent_cls(**clean_cfg)
            instances[clean_cfg["agent_id"]] = agent

        return instances

    def run(self, input_data):
        outputs = {}
        for agent_id in self.orchestrator_cfg["agents"]:
            agent = self.agents[agent_id]
            result = agent.run(input_data)
            outputs[agent_id] = result
        return outputs