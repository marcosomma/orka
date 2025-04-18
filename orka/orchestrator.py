# OrKa: Orchestrator Kit Agents
# Copyright © 2025 Marco Somma
#
# This file is part of OrKa – https://github.com/marcosomma/orka
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).
# You may not use this file for commercial purposes without explicit permission.
#
# Full license: https://creativecommons.org/licenses/by-nc/4.0/legalcode
# For commercial use, contact: marcosomma.work@gmail.com
# 
# Required attribution: OrKa by Marco Somma – https://github.com/marcosomma/orka

import importlib
import os
import json
from jinja2 import Template
from datetime import datetime
from .loader import YAMLLoader
from .agents import agents, llm_agents, google_duck_agents
from .memory_logger import RedisMemoryLogger

AGENT_TYPES = {
    "binary": agents.BinaryAgent,
    "classification": agents.ClassificationAgent,
    "openai-binary": llm_agents.OpenAIBinaryAgent,
    "openai-classification": llm_agents.OpenAIClassificationAgent,
    "openai-answer": llm_agents.OpenAIAnswerBuilder,
    "google-search": google_duck_agents.GoogleSearchAgent,
    "duckduckgo": google_duck_agents.DuckDuckGoAgent
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

            if hasattr(agent, "prompt") and isinstance(agent.prompt, str):
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

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.getenv("ORKA_LOG_DIR", "logs")
        file_path = f"orka_trace_{timestamp}.json"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, file_path)
        self.memory.save_to_file(log_path)
        return outputs
