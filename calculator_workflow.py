"""Calculator as a workflow (fixed sequence of steps), contrasted with calculator_agent.py.

calculator_agent.py is an agent: the model decides which tool to call next and when to stop.

But, here the control flow lives in code and is always the same:

    1. plan     (LLM)   - turn the request into an ordered list of arithmetic steps
    2. validate (code)  - check operations and step references before running anything
    3. execute  (code)  - run each step in order; later steps may reference earlier results
    4. respond  (LLM)   - phrase the final answer from the computed results
"""

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"


def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def multiply_numbers(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

operations = {
    "add": add_numbers,
    "subtract": subtract_numbers,
    "multiply": multiply_numbers,
    "divide": divide,
}

# Operand is either a literal number or a reference such as "step1" to an earlier result.
operand_schema = {
    "anyOf": [
        {"type": "number"},
        {"type": "string", "pattern": "^step[0-9]+$"},
    ],
    "description": "A number, or 'stepN' to use the result of step N.",
}

plan_schema = {
    "name": "submit_plan",
    "description": (
        "Submit the ordered arithmetic steps needed to answer the request. "
        "Respect operator precedence: compute multiplication/division steps before "
        "the additions/subtractions that use them. Steps are numbered from 1."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "enum": list(operations)},
                        "a": operand_schema,
                        "b": operand_schema,
                    },
                    "required": ["operation", "a", "b"],
                },
            }
        },
        "required": ["steps"],
    },
}


# Step 1: plan (LLM). tool_choice forces the structured output, so there is no free-form reply.
def plan(request):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": request}],
        tools=[plan_schema],
        tool_choice={"type": "tool", "name": "submit_plan"},
    )
    return next(b.input["steps"] for b in message.content if b.type == "tool_use")


# Step 2: validate (code). Fail before executing anything.
def validate(steps):
    if not steps:
        raise ValueError("The plan has no steps.")
    for i, step in enumerate(steps, start=1):
        if step["operation"] not in operations:
            raise ValueError(f"Step {i}: unknown operation '{step['operation']}'.")
        for key in ("a", "b"):
            value = step[key]
            if isinstance(value, str) and int(value.removeprefix("step")) >= i:
                raise ValueError(f"Step {i}: '{value}' must refer to an earlier step.")


# Step 3: execute (code). Deterministic, no model involved.
def execute(steps):
    results = []
    for step in steps:
        a, b = (results[int(v[4:]) - 1] if isinstance(v, str) else v
                for v in (step["a"], step["b"]))
        results.append(operations[step["operation"]](a, b))
    return results


# Step 4: respond (LLM). Only phrases what the code already computed.
def respond(request, steps, results):
    trace = "\n".join(
        f"step{i}: {s['operation']}({s['a']}, {s['b']}) = {r}"
        for i, (s, r) in enumerate(zip(steps, results), start=1)
    )
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": (
                f"Question: {request}\n\nComputed steps:\n{trace}\n\n"
                "State the final answer briefly, using the last step's result."
            ),
        }],
    )
    return message.content[0].text


def run_workflow(request):
    steps = plan(request)

    for step in steps:
        print(step)


    validate(steps)
    results = execute(steps)
    return respond(request, steps, results)


if __name__ == "__main__":
    print(run_workflow("What is 10 + 10 + 10 + 10 + (1+2)"))
