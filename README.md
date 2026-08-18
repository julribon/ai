# AI — Local LLM Playground

Small Python project for experimenting with local Large Language Model backends: **Ollama**, **LM Studio**, and **Hugging Face (transformers)**, plus helpers to read chat history from local AI tools.

## Features

- **Agents** built with `pydantic-ai`:
  - Ollama agent (`src/ai/agent/ollama_agent.py`) — talks to the Ollama OpenAI-compatible API on `http://localhost:11434/v1`
  - LM Studio agent (`src/ai/agent/lms_agent.py`) — talks to the LM Studio OpenAI-compatible API on `http://localhost:1234/v1`
- **Direct SDK clients** (`src/ai/chat/`):
  - `ollama_chat.py` — uses the official `ollama` Python SDK
  - `lmstudio_chat.py` — uses the `lmstudio` Python SDK
- **Local inference** (`src/ai/chat/huggingface_chat.py`) — runs a model directly with `transformers` (`pipeline("text-generation")`), no server needed
- **HTTP chat completions** (`src/ai/chat/request_chat.py`) — raw `requests` calls to the `/v1/chat/completions` endpoint of either backend
- **Chat history access** (`src/ai/chat/request_chat.py`):
  - `list_ollama_chats()` / `get_ollama_chat(id)` — reads Open WebUI's SQLite database
  - `list_lmstudio_chats()` / `get_lmstudio_chat(id)` — reads LM Studio conversation JSON files (`~/.lmstudio/conversations`)

## Requirements

- Python **>= 3.13**
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A local model server:
  - **Ollama** running on `http://localhost:11434` with model `mistral-small3.2`
  - **LM Studio** running on `http://localhost:1234` with model `mistralai/mistral-small-3.2`
- For the Hugging Face client: enough RAM/VRAM to load `unsloth/Mistral-Small-3.2-24B-Instruct-2506` (downloaded on first run)

## Installation

```bash
uv sync        # or: pip install -e .
```

Key dependencies: `pydantic-ai`, `ollama`, `lmstudio`, `transformers`, `torch`, `accelerate`, `requests`.

## Usage

### Agents (pydantic-ai)

```bash
python agent.py
```

`agent.py` asks the Ollama and LM Studio agents a question and prints their answers.

To use an agent in your own code:

```python
from ai.agent import ollama_agent, lms_agent

print(ollama_agent.ask("Quelle est la capitale de la France?"))
print(lms_agent.ask("Quelle est la capitale de la France?"))
```

### Chat clients & history

```bash
python chat.py
```

`chat.py` demonstrates the different backends and lists/inspects stored conversations:

- `request_chat.get_response(prompt, backend="ollama" | "lmstudio")` — one-shot chat completion
- `request_chat.list_chats()` — list Open WebUI chats via the REST API (requires a valid token)
- `request_chat.list_ollama_chats()` / `get_ollama_chat(id)` — Ollama/Open WebUI history from the local SQLite DB
- `request_chat.list_lmstudio_chats()` / `get_lmstudio_chat(id)` — LM Studio history from JSON files

### Hugging Face (local inference)

```python
from src.ai.chat.huggingface_chat import get_response

print(get_response("Hello!"))
```

## Project structure

```
.
├── agent.py                  # Entry point: pydantic-ai agents (Ollama + LM Studio)
├── chat.py                   # Entry point: chat clients & conversation history demo
├── pyproject.toml            # Project config (uv, Python >= 3.13)
└── src/
    └── ai/
        ├── agent/
        │   ├── lms_agent.py      # LM Studio agent (pydantic-ai + OpenAI provider)
        │   └── ollama_agent.py   # Ollama agent (pydantic-ai + Ollama provider)
        └── chat/
            ├── huggingface_chat.py  # Local inference with transformers
            ├── lmstudio_chat.py     # LM Studio SDK client
            ├── ollama_chat.py       # Ollama SDK client
            └── request_chat.py      # HTTP completions + chat history (Ollama/LM Studio)
```

## Notes

- Model names and base URLs are hardcoded in the source files; adjust them to match your local setup.
- `list_chats()` expects an Open WebUI instance on `http://localhost:8080` with a bearer token (see `API_KEY` in `request_chat.py`).
- The Ollama history helpers assume the default Open WebUI database location on macOS: `~/Library/Application Support/open-webui/data/webui.db`.
