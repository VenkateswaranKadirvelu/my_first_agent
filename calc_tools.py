def add(num1, num2):
    if num1 is None or num2 is None:
        raise ValueError("Num1, Num2 cannot be empty.")
    return num1 + num2;

def subtract(num1, num2):
    if num1 is None or num2 is None:
        raise ValueError("Num1, Num2 cannot be empty.")
    return num1 - num2;

def multiply(num1, num2):
    if num1 is None or num2 is None:
        raise ValueError("Num1, Num2 cannot be empty.")
    return num1 * num2;

def divide(num1, num2):
    if num1 is None or num2 is None:
        raise ValueError("Num1, Num2 cannot be empty.")
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2;
