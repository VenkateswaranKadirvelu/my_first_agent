# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A learning project comparing two ways of building a calculator on the Anthropic API (`claude-haiku-4-5`): an **agent** (the model decides the next tool call) versus a **workflow** (fixed code-driven steps). Python 3.13, managed with `uv`. There is no test suite, linter, or build step; the README is empty.

## Commands

```bash
uv sync                          # install deps into .venv
uv run python calc_agent.py      # modular agent (the most refined version)
uv run python calculator_agent.py
uv run python calculator_workflow.py
```

Requires `ANTHROPIC_API_KEY` in `.env` (loaded via `python-dotenv`). Each script runs on import/execution and makes live API calls; there are no `main()` guards or CLI args — the prompt is hardcoded in each script.

## Architecture

Three independent scripts, each runnable on its own (they do not import each other, except the `calc_*` set):

- **`calc_agent.py`** — entry point of the modular agent. Runs a manual tool-use loop (up to `MAX_TURNS`): call `messages.create` with tool schemas, append the assistant content, and if `stop_reason == "tool_use"` execute tools via `run_tools` and append `tool_result` blocks as a user message; otherwise stop. Tool errors are returned to the model with `is_error: True`. It imports from the three helper modules below.
  - `calc_tools.py` — plain functions `add/subtract/multiply/divide` (args `num1`, `num2`).
  - `calc_schema.py` — the matching tool JSON schemas. Names and parameter names (`num1`/`num2`) must stay in sync with `calc_tools.py` and the `tools` dispatch dict in `calc_agent.py`.
  - `calc_messages.py` — `add_message(messages, role, text)` helper.
- **`calculator_agent.py`** — earlier, self-contained single-file version of the agent (tools named `add_numbers` etc., params `a`/`b`, helpers and schemas inline). Naming differs from the `calc_*` modules.
- **`calculator_workflow.py`** — the workflow contrast: LLM plans an ordered list of steps → code validates operations and `stepN` references → code executes steps → LLM phrases the final answer. Control flow lives in code, not the model.
