from anthropic import Anthropic
from calc_messages import add_message
from calc_schema import add_schema, divide_schema, multiply_schema, subtract_schema
from calc_tools import add, divide, multiply, subtract
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"
MAX_TURNS = 8

messages = []

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        tools=[add_schema, subtract_schema, multiply_schema, divide_schema]
    )
    return message

tools = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
}

add_message(messages, "user", "What is the result of (4 + 4) / (4 - 2) + (6 / 3)")

def run_tools(message):
    tool_results = []
    for block in message.content:
        if block.type == "tool_use":
            try:
                output = tools[block.name](**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(output)
                })
            except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Error: {e}",
                    "is_error": True
                })
        else:
            continue

    return tool_results

for turn in range(MAX_TURNS):
    print("Turn : " + str(turn))
    result = chat(messages=messages)
    add_message(messages=messages, role="assistant", text=result.content)
    if result.stop_reason == "tool_use":
        tool_result = run_tools(result)
        add_message(messages=messages, role="user", text=tool_result)
    else:
        break

print(result.content[0].text)

    







