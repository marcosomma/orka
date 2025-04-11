
# OrKa — Orchestrator Kit for Agentic Reasoning

![OrKa Logo](./logo.png)

OrKa is a modular AI orchestration system that transforms Large Language Models (LLMs) into composable agents capable of reasoning, fact-checking, and constructing answers with transparent traceability.

## 🚀 Features

- **Modular Agent Orchestration**: Define and manage agents using intuitive YAML configurations.
- **Configurable Reasoning Paths**: Utilize Redis streams to set up dynamic reasoning workflows.
- **Comprehensive Logging**: Record and trace every step of the reasoning process for transparency.
- **Built-in Integrations**: Support for OpenAI agents, web search functionalities, routers, and validation mechanisms.
- **Command-Line Interface (CLI)**: Execute YAML-defined workflows with ease.

## 🛠️ Installation

Ensure you have Python and Redis installed on your system.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/marcosomma/orka.git
   cd orka
   ```

2. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

3. **Create a `.env` file** in the root directory with your API credentials and settings:
   ```
   OPENAI_API_KEY=your_openai_api_key
   BASE_OPENAI_MODEL=gpt-4o-mini
   GOOGLE_API_KEY=sksdsadasqwdad....
   GOOGLE_CSE_ID=1234
   ```

## 📄 Usage

OrKa operates based on YAML configuration files that define the orchestration of agents.

1. **Prepare a YAML Configuration**: Create a YAML file (e.g., `example.yml`) that outlines your agentic workflow.
2. **Run OrKa with the Configuration**:
   ```bash
   python -m orka.orka_cli ./example.yml "Your input question" --log-to-file
   ```

This command processes the input question through the defined workflow and logs the reasoning steps.

## 📝 YAML Configuration Structure

The YAML file specifies the agents and their interactions. Below is an example configuration:

```yaml
agents:
  - name: "web_search"
    type: "search"
  - name: "openai_agent"
    type: "llm"

workflow:
  - from: "input"
    to: "web_search"
  - from: "web_search"
    to: "openai_agent"
  - from: "openai_agent"
    to: "output"
```

### Key Sections

- **agents**: Defines the individual agents involved in the workflow. Each agent has:
  - **name**: Unique identifier for the agent.
  - **type**: Specifies the agent's function (e.g., `search`, `llm`).

- **workflow**: Outlines the sequence of interactions between agents:
  - **from**: Source agent or input.
  - **to**: Destination agent or output.

Settings such as the model and API keys are loaded from the `.env` file, keeping your configuration secure and flexible.

## 🧪 Example

To see OrKa in action, use the provided `example.yml` configuration:

```bash
python -m orka.orka_cli ./example.yml "What is the capital of France?" --log-to-file
```

This will execute the workflow defined in `example.yml` with the input question, logging each reasoning step.

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📜 License & Attribution

This project is licensed under the CC BY-NC 4.0 License. For more details, refer to the [LICENSE.md](./LICENSE.md) file.
