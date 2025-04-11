
# OrKa — Orchestrator Kit for Agentic Reasoning

![OrKa Logo](./logo.png)

OrKa is a modular AI orchestration system that turns LLMs into composable agents capable of reasoning, fact-checking, and building answers — all with transparent traceability.

## 🧠 What OrKa Does

- 🧩 Modular agent orchestration via YAML
- 🔀 Configurable reasoning paths using Redis streams
- 🧠 Memory logging and trace-saving for every reasoning step
- 🛠️ Built-in support for OpenAI agents, web search, routers, and validation
- 📦 CLI to run YAML-defined flows with single questions or inputs

## 🚀 Getting Started

```bash
git clone https://github.com/YOU/OrKa.git
cd OrKa
pip install -e .
python -m orka.orka_cli ./example.yml "Your input question" --log-to-file
```

## License & Attribution

This project is licensed under CC BY-NC 4.0 with additional requirements for attribution.
See the `LICENSE` file for details.
