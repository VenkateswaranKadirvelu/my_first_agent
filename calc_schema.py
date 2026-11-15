add_schema = {
  "name": "add",
  "description": "Add two numbers together and return their sum. Both numbers are required.",
  "input_schema": {
    "type": "object",
    "properties": {
      "num1": {
        "type": "number",
        "description": "The first number to add."
      },
      "num2": {
        "type": "number",
        "description": "The second number to add."
      }
    },
    "required": ["num1", "num2"]
  }
}

subtract_schema = {
  "name": "subtract",
  "description": "Subtract the second number from the first and return the difference (num1 - num2). Both numbers are required.",
  "input_schema": {
    "type": "object",
    "properties": {
      "num1": {
        "type": "number",
        "description": "The number to subtract from (the minuend)."
      },
      "num2": {
        "type": "number",
        "description": "The number to subtract (the subtrahend)."
      }
    },
    "required": ["num1", "num2"]
  }
}

multiply_schema = {
  "name": "multiply",
  "description": "Multiply two numbers together and return the product (num1 * num2). Both numbers are required.",
  "input_schema": {
    "type": "object",
    "properties": {
      "num1": {
        "type": "number",
        "description": "The first number to multiply."
      },
      "num2": {
        "type": "number",
        "description": "The second number to multiply."
      }
    },
    "required": ["num1", "num2"]
  }
}

divide_schema = {
  "name": "divide",
  "description": "Divide the first number by the second and return the quotient (num1 / num2). Both numbers are required, and the divisor must not be zero.",
  "input_schema": {
    "type": "object",
    "properties": {
      "num1": {
        "type": "number",
        "description": "The dividend (the number to be divided)."
      },
      "num2": {
        "type": "number",
        "description": "The divisor (the number to divide by). Must not be zero."
      }
    },
    "required": ["num1", "num2"]
  }
}