"""
Number theory functions.

This module provides functions for common number theory operations
like primality testing, factorial, and GCD/LCM calculations.
"""

import math
from typing import List, Union, Optional, TypeVar

# Define a type variable for integer types
IntType = TypeVar('IntType', int, bool)


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    A prime number is a natural number greater than 1 that is not a product
    of two smaller natural numbers.
    
    Args:
        n: The integer to check.
        
    Returns:
        True if the number is prime, False otherwise.
        
    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(4)
        False
        >>> is_prime(17)
        True
    """
    if n <= 1:
        return False
    
    if n <= 3:
        return True
    
    # Check if n is divisible by 2 or 3
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # Check through all numbers of form 6k ± 1 up to sqrt(n)
    # This is an optimization based on the fact that all primes > 3 are of the form 6k ± 1
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True


def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.
    
    The factorial of n (denoted as n!) is the product of all positive
    integers less than or equal to n.
    
    Args:
        n: The non-negative integer to calculate the factorial of.
        
    Returns:
        The factorial of n.
        
    Raises:
        ValueError: If n is negative.
        
    Examples:
        >>> factorial(0)
        1
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor (GCD) of two integers.
    
    The GCD is the largest positive integer that divides both numbers without a remainder.
    
    Args:
        a: First integer.
        b: Second integer.
        
    Returns:
        The greatest common divisor of a and b.
        
    Examples:
        >>> gcd(8, 12)
        4
        >>> gcd(17, 23)
        1
        >>> gcd(0, 5)
        5
    """
    # Handle edge cases
    a, b = abs(a), abs(b)
    
    if a == 0:
        return b
    if b == 0:
        return a
    
    # Euclidean algorithm
    while b:
        a, b = b, a % b
    
    return a


def lcm(a: int, b: int) -> int:
    """
    Calculate the least common multiple (LCM) of two integers.
    
    The LCM is the smallest positive integer that is divisible by both a and b.
    
    Args:
        a: First integer.
        b: Second integer.
        
    Returns:
        The least common multiple of a and b.
        
    Raises:
        ValueError: If both a and b are 0 (LCM is undefined).
        
    Examples:
        >>> lcm(4, 6)
        12
        >>> lcm(15, 25)
        75
        >>> lcm(0, 5)
        0
    """
    # Handle edge cases
    a, b = abs(a), abs(b)
    
    if a == 0 and b == 0:
        raise ValueError("LCM is undefined when both inputs are 0")
    
    if a == 0 or b == 0:
        return 0
    
    # LCM formula: |a * b| / gcd(a, b)
    return (a * b) // gcd(a, b)