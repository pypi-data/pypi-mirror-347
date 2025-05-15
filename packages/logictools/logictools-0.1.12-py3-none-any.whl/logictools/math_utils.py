def factorial(n):
    """
    Calculates the factorial of a non-negative integer.
    
    Args:
        n: Integer input (must be non-negative)
        
    Returns:
        int: Factorial of n
        
    Raises:
        TypeError: If input is not an integer
        ValueError: If input is negative
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def divide(a, b):
    """
    Divides two numbers.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        float: Result of division
        
    Raises:
        ZeroDivisionError: If denominator is zero
        TypeError: If inputs are not numbers
    """
    if not all(isinstance(x, (int, float)) for x in [a, b]):
        raise TypeError("Both inputs must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b