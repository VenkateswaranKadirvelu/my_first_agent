# my_first_agent

A learning project that compares two ways of building a calculator on the Anthropic API (`claude-haiku-4-5`):

- **Agent**: the model decides which tool to call next, in a loop.
- **Workflow**: fixed, code-driven steps. The LLM plans and phrases the answer, and code controls the flow.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An Anthropic API key

## Setup

```bash
uv sync
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Usage

```bash
uv run python calc_agent.py          # modular tool-use agent
uv run python calculator_workflow.py # plan -> validate -> execute -> answer workflow
```

Each script runs on execution and makes live API calls. The prompt is hardcoded in the script, so edit it to try different questions.

## Project structure

| File | Purpose |
|------|---------|
| `calc_agent.py` | Agent entry point. Runs a manual tool-use loop (up to `MAX_TURNS`), executes tools, and returns tool errors to the model with `is_error: True`. |
| `calc_tools.py` | Plain functions `add`, `subtract`, `multiply`, `divide` (args `num1`, `num2`). |
| `calc_schema.py` | Tool JSON schemas. Names and parameters must stay in sync with `calc_tools.py` and the dispatch dict in `calc_agent.py`. |
| `calc_messages.py` | `add_message(messages, role, text)` helper. |
| `calculator_workflow.py` | Workflow version. The LLM plans an ordered list of steps, code validates operations and `stepN` references, code executes the steps, and the LLM writes the final answer. |

## Agent vs. workflow

|  | Agent | Workflow |
|--|-------|----------|
| Control flow | Chosen by the model each turn | Fixed in code |
| Tool calls | Model-driven loop | Code executes a validated plan |
| Best for | Open-ended tasks | Predictable, auditable tasks |

## Notes

There is no test suite, linter, or build step.
