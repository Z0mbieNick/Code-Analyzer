


def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b  # Potential ZeroDivisionError here

def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    
    num1 = float(input("Enter first number: "))  # Potential ValueError
    operation = input("Enter operation (+, -, *, /): ")  # No check for valid operation
    num2 = float(input("Enter second number: "))  # Potential ValueError

    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)  # ZeroDivisionError if num2 is 0
    else:
        print("Invalid operation")  # No exception handling for invalid input
        return

    print(f"Result: {result}")

calculator()
