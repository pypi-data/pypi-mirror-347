"""
Safe and useful arithmetic functions.

This module provides enhanced arithmetic operations that handle
edge cases like division by zero and other common math utilities.
"""

from typing import List, Optional, Union, TypeVar, Any, Tuple

# Define a type variable for numeric types
Numeric = TypeVar('Numeric', int, float, complex)


def safe_divide(numerator: Numeric, denominator: Numeric, default: Optional[Numeric] = None) -> Numeric:
    """
    Safely divide two numbers, handling division by zero.
    
    Args:
        numerator: The number to divide.
        denominator: The number to divide by.
        default: Value to return if denominator is zero. If None, returns numerator.
        
    Returns:
        The result of the division, or the default value if the denominator is zero.
        
    Examples:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)  # Returns numerator when default is None
        10
        >>> safe_divide(10, 0, default=0)
        0
    """
    if denominator == 0:
        return default if default is not None else numerator
    return numerator / denominator


def percent_change(old_value: Numeric, new_value: Numeric, default: Optional[Numeric] = 0) -> float:
    """
    Calculate the percentage change between two values.
    
    Args:
        old_value: The original value.
        new_value: The new value.
        default: Value to return if old_value is zero.
        
    Returns:
        The percentage change from old_value to new_value.
        If old_value is zero, returns default.
        
    Examples:
        >>> percent_change(100, 150)
        50.0
        >>> percent_change(100, 80)
        -20.0
        >>> percent_change(0, 100, default=100)
        100
    """
    if old_value == 0:
        return default
    return ((new_value - old_value) / old_value) * 100


def normalize(values: List[Numeric], 
              new_min: Numeric = 0, 
              new_max: Numeric = 1) -> List[float]:
    """
    Normalize a list of values to a new range.
    
    Args:
        values: List of values to normalize.
        new_min: The minimum value in the new range.
        new_max: The maximum value in the new range.
        
    Returns:
        A list of normalized values in the specified range.
        If all values are the same, returns a list of (new_min + new_max) / 2.
        
    Examples:
        >>> normalize([1, 2, 3, 4, 5])
        [0.0, 0.25, 0.5, 0.75, 1.0]
        >>> normalize([1, 2, 3, 4, 5], new_min=0, new_max=100)
        [0.0, 25.0, 50.0, 75.0, 100.0]
    """
    if not values:
        return []
    
    min_val = min(values)
    max_val = max(values)
    
    # If all values are the same, return the middle of the new range
    if min_val == max_val:
        return [float(new_min + new_max) / 2] * len(values)
    
    # Apply normalization formula
    return [
        float(new_min) + (float(new_max) - float(new_min)) * 
        ((float(x) - float(min_val)) / (float(max_val) - float(min_val)))
        for x in values
    ]


def z_score(values: List[Numeric], 
            mean: Optional[float] = None, 
            std_dev: Optional[float] = None) -> List[float]:
    """
    Calculate the z-score (standard score) for each value in a list.
    
    Z-score represents how many standard deviations a value is from the mean.
    
    Args:
        values: List of values to convert to z-scores.
        mean: The mean of the values. If None, calculated from the values.
        std_dev: The standard deviation of the values. If None, calculated from the values.
        
    Returns:
        A list of z-scores. If the standard deviation is zero (or close to it),
        returns a list of zeros.
        
    Examples:
        >>> z_score([2, 4, 6])
        [-1.0, 0.0, 1.0]
        >>> z_score([2, 2, 2])  # All values are the same
        [0.0, 0.0, 0.0]
    """
    if not values:
        return []
    
    if mean is None:
        mean = sum(values) / len(values)
    
    if std_dev is None:
        # Calculate standard deviation
        squared_diff_sum = sum((x - mean) ** 2 for x in values)
        std_dev = (squared_diff_sum / len(values)) ** 0.5
    
    # If standard deviation is zero (or very close to it), return all zeros
    if std_dev < 1e-10:
        return [0.0] * len(values)
    
    return [(x - mean) / std_dev for x in values] 