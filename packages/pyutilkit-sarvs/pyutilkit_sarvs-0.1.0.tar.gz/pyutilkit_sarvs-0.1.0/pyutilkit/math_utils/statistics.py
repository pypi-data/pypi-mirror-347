"""
Basic statistics functions.

This module provides simple functions for calculating basic
statistics like mean, median, mode, and standard deviation.
"""

from typing import List, Union, Optional, Dict, Any, TypeVar
from collections import Counter

# Define a type variable for numeric types
Numeric = TypeVar('Numeric', int, float)


def mean(values: List[Numeric]) -> float:
    """
    Calculate the arithmetic mean (average) of a list of numbers.
    
    Args:
        values: List of numeric values.
        
    Returns:
        The arithmetic mean of the values.
        
    Raises:
        ValueError: If the list is empty.
        
    Examples:
        >>> mean([1, 2, 3, 4, 5])
        3.0
        >>> mean([1, 1, 1])
        1.0
    """
    if not values:
        raise ValueError("Cannot calculate mean of an empty list")
    
    return sum(values) / len(values)


def median(values: List[Numeric]) -> float:
    """
    Calculate the median (middle value) of a list of numbers.
    
    Args:
        values: List of numeric values.
        
    Returns:
        The median of the values.
        
    Raises:
        ValueError: If the list is empty.
        
    Examples:
        >>> median([1, 3, 5, 7, 9])  # Odd number of values
        5
        >>> median([1, 3, 5, 7])     # Even number of values
        4.0
    """
    if not values:
        raise ValueError("Cannot calculate median of an empty list")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 1:
        # Odd number of values, return the middle one
        return sorted_values[n // 2]
    else:
        # Even number of values, return the average of the two middle ones
        return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2


def mode(values: List[Any]) -> Any:
    """
    Find the most common value in a list.
    
    If there are multiple modes, returns the first one encountered.
    
    Args:
        values: List of values (can be any type).
        
    Returns:
        The most common value in the list.
        
    Raises:
        ValueError: If the list is empty.
        
    Examples:
        >>> mode([1, 2, 2, 3, 3, 3, 4])
        3
        >>> mode(['apple', 'banana', 'apple', 'orange'])
        'apple'
    """
    if not values:
        raise ValueError("Cannot calculate mode of an empty list")
    
    # Use Counter to count occurrences of each value
    counts = Counter(values)
    
    # Find the value with the highest count
    return counts.most_common(1)[0][0]


def standard_deviation(values: List[Numeric], population: bool = True) -> float:
    """
    Calculate the standard deviation of a list of numbers.
    
    Args:
        values: List of numeric values.
        population: If True, calculates the population standard deviation.
                   If False, calculates the sample standard deviation.
        
    Returns:
        The standard deviation of the values.
        
    Raises:
        ValueError: If the list is empty or has only one value when population=False.
        
    Examples:
        >>> standard_deviation([1, 2, 3, 4, 5])  # Population std dev
        1.4142135623730951
        >>> standard_deviation([1, 2, 3, 4, 5], population=False)  # Sample std dev
        1.5811388300841898
    """
    n = len(values)
    
    if n == 0:
        raise ValueError("Cannot calculate standard deviation of an empty list")
    
    if n == 1 and not population:
        raise ValueError("Cannot calculate sample standard deviation with only one value")
    
    # Calculate the mean
    avg = sum(values) / n
    
    # Calculate the sum of squared differences from the mean
    squared_diff_sum = sum((x - avg) ** 2 for x in values)
    
    # For population standard deviation, divide by n
    # For sample standard deviation, divide by (n-1)
    divisor = n if population else (n - 1)
    
    # Return the square root of the variance
    return (squared_diff_sum / divisor) ** 0.5 