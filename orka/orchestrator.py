import importlib
import os
import json
from jinja2 import Template
from datetime import datetime
from .loader import YAMLLoader
from .agents import agents, llm_agents, google_duck_agents, router_agent
from .memory_logger import RedisMemoryLogger

AGENT_TYPES = {
    "binary": agents.BinaryAgent,
    "classification": agents.ClassificationAgent,
    "openai-binary": llm_agents.OpenAIBinaryAgent,
    "openai-classification": llm_agents.OpenAIClassificationAgent,
    "openai-answer": llm_agents.OpenAIAnswerBuilder,
    "google-search": google_duck_agents.GoogleSearchAgent,
    "duckduckgo": google_duck_agents.DuckDuckGoAgent,
    "router": router_agent.RouterAgent
}


class Orchestrator:
    def __init__(self, config_path):
        self.loader = YAMLLoader(config_path)
        self.loader.validate()
        self.orchestrator_cfg = self.loader.get_orchestrator()
        self.agent_cfgs = self.loader.get_agents()
        self.memory = RedisMemoryLogger()
        self.agents = self._init_agents()

    def _init_agents(self):
        instances = {}
        for cfg in self.agent_cfgs:
            agent_cls = AGENT_TYPES.get(cfg["type"])
            if not agent_cls:
                raise ValueError(f"Unsupported agent type: {cfg['type']}")

            agent_type = cfg["type"].strip().lower()
            agent_id = cfg["id"]

            clean_cfg = cfg.copy()
            clean_cfg["agent_id"] = agent_id
            clean_cfg.pop("id", None)
            clean_cfg.pop("type", None)

            print(f"[INIT] Instantiating agent {agent_id} of type {agent_type}")

            if agent_type == "router":
                clean_cfg.pop("prompt", None)
                clean_cfg.pop("queue", None)
                params = clean_cfg.pop("params", {})
                clean_cfg.pop("agent_id", None)  # 💥 Prevent double-passing
                agent = agent_cls(agent_id=agent_id,
                                  params=params, **clean_cfg)
            else:
                prompt = clean_cfg.pop("prompt")
                queue = clean_cfg.pop("queue")
                clean_cfg.pop("agent_id", None)
                agent = agent_cls(
                    agent_id=agent_id,
                    prompt=prompt,
                    queue=queue,
                    **clean_cfg
                )

            instances[agent_id] = agent
        return instances

    def render_prompt(self, template_str, payload):
        if not isinstance(template_str, str):
            raise ValueError(
                f"Expected template_str to be str, got {type(template_str)} instead.")
        return Template(template_str).render(**payload)

    @staticmethod
    def normalize_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.strip().lower()
            return value in ["true", "yes"]
        return False

    def run(self, input_data):
        outputs = {}
        queue = self.orchestrator_cfg["agents"][:]

        while queue:
            agent_id = queue.pop(0)
            agent = self.agents[agent_id]

            payload = {
                "input": input_data,
                "previous_outputs": outputs
            }

            if agent_id == "router":
                decision_key = agent.params.get('decision_key')
                if decision_key is None:
                    raise ValueError(
                        "Router agent must have 'decision_key' in params.")
                raw_decision_value = outputs.get(decision_key)
                normalized = self.normalize_bool(raw_decision_value)
                normalized_key = "true" if normalized else "false"
                payload['previous_outputs'][decision_key] = normalized_key
                result = agent.run(payload)
                print(f"[ROUTER] Using decision_key='{decision_key}' → '{normalized_key}' → route={result}")
            elif hasattr(agent, "prompt") and isinstance(agent.prompt, str):
                rendered_prompt = self.render_prompt(agent.prompt, payload)
                payload["prompt"] = rendered_prompt
                result = agent.run(payload)
            else:
                result = agent.run(payload)

            outputs[agent_id] = result
            print(f"[ORKA] Agent '{agent_id}' returned: {result}")
            if queue:  # Check if this is the last agent
                self.memory.log(agent_id, agent.__class__.__name__, {
                                "input": input_data, "result": result
                            })
            else:
                self.memory.log(agent_id, agent.__class__.__name__, {
                                "input": input_data, "result": result
                            })
                self.memory.log(agent_id, agent.__class__.__name__, { "hystory": payload })

            if isinstance(result, list) and agent_id == "router":
                queue = result + queue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"logs/orka_trace_{timestamp}.json"
        os.makedirs("logs", exist_ok=True)
        self.memory.save_to_file(file_path)
        return outputs
