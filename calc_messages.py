def add_message(messages, role, text):
    message = {
        "role": role,
        "content": text
    }
    messages.append(message)
