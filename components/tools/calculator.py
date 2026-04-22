from typing import List, Union

def sum_of_nums(nums: List[float]) -> float:
    """Calculate the sum of a list of numbers."""
    print(f"\n[Tool Call] sum_of_nums: {nums}")
    return sum(nums)

def subtract(a: float, b: float) -> float:
    """Subtract one number from another."""
    print(f"\n[Tool Call] subtract: {a} - {b}")
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    print(f"\n[Tool Call] multiply: {a} * {b}")
    return a * b

def divide(a: float, b: float) -> Union[float, str]:
    """Divide one number by another."""
    print(f"\n[Tool Call] divide: {a} / {b}")
    if b == 0:
        return "Cannot divide by zero"
    return a / b

def percentage(a: float, b: float) -> float:
    """Calculate the percentage value (b% of a)."""
    print(f"\n[Tool Call] percentage: {b}% of {a}")
    return a * (b / 100)
