# Claude API Python Project Setup

A step-by-step guide to setting up Python, Jupyter notebooks, and the UV package manager on macOS, then connecting to the Claude API.

## Prerequisites

- macOS
- Xcode Command Line Tools (needed for some packages to compile): `xcode-select --install`
- An Anthropic API key from the [Anthropic Console](https://console.anthropic.com)

## 1. Install UV

Open Terminal and run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal (or run `source ~/.zshrc`), then confirm it installed:

```bash
uv --version
```

UV replaces `pip`, `venv`, and `pyenv` for most workflows — it manages Python versions, virtual environments, and packages, and it's much faster.

## 2. Create Your Project

```bash
mkdir claude-project
cd claude-project
uv init
```

This creates a `pyproject.toml`, a `.python-version` file, and a starter `main.py`.

If you want a specific Python version:

```bash
uv python install 3.12
uv python pin 3.12
```

## 3. Add Jupyter Notebook Support

```bash
uv add --dev jupyter ipykernel
```

`--dev` marks these as development dependencies (not needed for production, just for local notebook work).

## 4. Add the Anthropic SDK

```bash
uv add anthropic
```

If you'll also want to load environment variables from a `.env` file:

```bash
uv add python-dotenv
```

## 5. Launch the Notebook

```bash
uv run jupyter notebook
```

`uv run` automatically creates/activates the virtual environment and runs the command inside it — no need to manually `source venv/bin/activate`. This opens Jupyter in your browser. Create a new notebook (`.ipynb` file) from there.

**Alternative (VS Code):** Open the project folder, create a `.ipynb` file, and select the `.venv` UV created (`./.venv/bin/python`) as the kernel — no need to launch Jupyter separately.

## 6. Set Up Your API Key Safely

Never hardcode your API key in a notebook cell. Instead:

```bash
touch .env
echo ".env" >> .gitignore
```

Add this line inside `.env`:

```
ANTHROPIC_API_KEY=your-key-here
```

## 7. Test the API Connection

In a notebook cell:

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()  # automatically reads ANTHROPIC_API_KEY from environment

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)

print(message.content[0].text)
```

## Quick Command Reference

| Task | Command |
|---|---|
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Run a script | `uv run script.py` |
| Run notebook | `uv run jupyter notebook` |
| Sync deps (after cloning) | `uv sync` |