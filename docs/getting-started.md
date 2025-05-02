[📘 Getting Start](./getting-started.md) | [🤖 Advanced Agents](./agents-advanced.md) | [🔍 Architecture](./architecture.md) | [🧠 Idea](./index.md) | [🧪 Extending Agents](./extending-agents.md) | [📊 Observability](./observability.md) | [📜 YAML Schema](./orka.yaml-schema.md) | [⚙ Runtime Modes](./runtime-modes.md) | [🔐 Security](./security.md) | [❓ FAQ](./faq.md)

# Getting Started with OrKa

## 1. Install
```bash
git clone https://github.com/marcosomma/orka.git
cd orka
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure `.env`
```
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-3.5-turbo
```

## 3. Run Demo
```bash
python test_run.py
```
This runs `orka.yaml` against a sample input.

## 4. Inspect Logs
```bash
redis-cli xrevrange orka:memory + - COUNT 5
```

## 5. Edit `orka.yaml`
- Change prompts
- Add agents
- Insert fallback paths

## 6. Need Help?
GitHub issues or Discord: https://discord.gg/UthTN8Xu

[📘 Getting Start](./getting-started.md) | [🤖 Advanced Agents](./agents-advanced.md) | [🔍 Architecture](./architecture.md) | [🧠 Idea](./index.md) | [🧪 Extending Agents](./extending-agents.md) | [📊 Observability](./observability.md) | [📜 YAML Schema](./orka.yaml-schema.md) | [⚙ Runtime Modes](./runtime-modes.md) | [🔐 Security](./security.md) | [❓ FAQ](./faq.md)
