# agents-for-all

**Modular agent framework combining LLMs and tools.**

[![Built with uv](https://img.shields.io/badge/built%20with-uv-blue?logo=rust)](https://github.com/astral-sh/uv)
[![Test Coverage](https://img.shields.io/codecov/c/github/dhungana/agents-for-all?label=coverage)](https://codecov.io/gh/dhungana/agents-for-all)
[![Python 3.10](https://github.com/dhungana/agents-for-all/actions/workflows/test_310.yml/badge.svg)](https://github.com/dhungana/agents-for-all/actions/workflows/test_310.yml)
[![Python 3.11](https://github.com/dhungana/agents-for-all/actions/workflows/test_311.yml/badge.svg)](https://github.com/dhungana/agents-for-all/actions/workflows/test_311.yml)
[![Python 3.12](https://github.com/dhungana/agents-for-all/actions/workflows/test_312.yml/badge.svg)](https://github.com/dhungana/agents-for-all/actions/workflows/test_312.yml)
[![Python 3.13](https://github.com/dhungana/agents-for-all/actions/workflows/test_313.yml/badge.svg)](https://github.com/dhungana/agents-for-all/actions/workflows/test_313.yml)

Designed to help developers quickly build task-solving agents using large language models and pluggable toolchains.

---

## ✨ Features

- 🔌 Pluggable tool architecture
- 🤖 LLM integration (OpenAI, Anthropic, Gemini, Direct, etc.)
- 🧪 Built-in testing with `pytest`
- 📝 Documentation support via `sphinx`
- ⚡ Fast dependency management using [`uv`](https://github.com/astral-sh/uv)

---

## 📦 Installation and Usage

```bash
pip install agents-for-all
```

```python
from agents_for_all import Agent
from agents_for_all.llms.direct import DirectModel
from agents_for_all.tools.python import Python

llm = DirectModel(
  api_endpoint="http://localhost:1234/v1/chat/completions",
  model="deepseek-r1-distill-qwen-14b"
)
agent = Agent(llm=llm, tools=[Python()])
result = agent.do("Generate a Fibonacci sequence of length 10.")
print(result.output) # Final output
print(result.history) # History of steps taken
```

---

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

### Prerequisites

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) installed:
  ```bash
  curl -Ls https://astral.sh/uv/install.sh | sh
  ```

### Installation

Create a virtual environment and install dependencies:

```bash
uv sync --extra dev
```

## 🧪 Running Tests

```bash
uv run pytest
```

## 📚 Documentation

To build the Sphinx docs (if configured):

```bash
uv run sphinx-build docs docs/_build
```

## 🛠 Project Structure (Sample)

```
agents_for_all/
├── agent.py           # Agent class
├── tools/             # Modular tools the agent can use
├── llms/              # Collection of LLMs the agent can connect to
├── tests/             # Pytest test cases
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## 📄 License

Apache License 2.0

---

## 🔗 Links

- 📦 GitHub: [agents-for-all](https://github.com/dhungana/agents-for-all.git)
- ✉️ Maintainer: [Sailesh Dhungana](mailto:dhunganasailesh@gmail.com)
- 📘 Docs: [dhungana.github.io/agents-for-all](https://dhungana.github.io/agents-for-all/)
- 📦 PyPI: [agents-for-all](https://pypi.org/project/agents-for-all/)
