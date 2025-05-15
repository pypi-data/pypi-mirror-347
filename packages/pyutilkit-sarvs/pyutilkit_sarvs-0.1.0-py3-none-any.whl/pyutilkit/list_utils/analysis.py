"""
Functions for analyzing list data.

This module provides utility functions for analyzing lists,
including frequency analysis and finding common elements.
"""

from typing import List, Dict, TypeVar, Any, Tuple, Optional, Union
from collections import Counter

# Define a type variable for countable elements
T = TypeVar('T')


def get_frequency(lst: List[T]) -> Dict[T, int]:
    """
    Count the frequency of each element in a list.
    
    Args:
        lst: The list to analyze.
        
    Returns:
        A dictionary mapping each element to its frequency.
        
    Examples:
        >>> get_frequency([1, 2, 2, 3, 1, 3, 3, 4])
        {1: 2, 2: 2, 3: 3, 4: 1}
        >>> get_frequency(['a', 'b', 'a', 'c', 'c', 'c'])
        {'a': 2, 'b': 1, 'c': 3}
    """
    return dict(Counter(lst))


def most_frequent(lst: List[T], n: int = 1) -> List[Tuple[T, int]]:
    """
    Find the most frequent elements in a list.
    
    Args:
        lst: The list to analyze.
        n: The number of most frequent elements to return.
        
    Returns:
        A list of tuples (element, frequency), sorted by frequency in descending order.
        
    Examples:
        >>> most_frequent([1, 2, 2, 3, 1, 3, 3, 4])
        [(3, 3)]
        >>> most_frequent([1, 2, 2, 3, 1, 3, 3, 4], n=2)
        [(3, 3), (1, 2)]
    """
    if not lst:
        return []
    
    counter = Counter(lst)
    return counter.most_common(n)


def least_frequent(lst: List[T], n: int = 1) -> List[Tuple[T, int]]:
    """
    Find the least frequent elements in a list.
    
    Args:
        lst: The list to analyze.
        n: The number of least frequent elements to return.
        
    Returns:
        A list of tuples (element, frequency), sorted by frequency in ascending order.
        
    Examples:
        >>> least_frequent([1, 2, 2, 3, 1, 3, 3, 4])
        [(4, 1)]
        >>> least_frequent([1, 2, 2, 3, 1, 3, 3, 4], n=2)
        [(4, 1), (1, 2)]
    """
    if not lst:
        return []
    
    counter = Counter(lst)
    # Sort by frequency (ascending) and then by element for stable sorting
    items = sorted(counter.items(), key=lambda x: (x[1], x[0]))
    return items[:n]


def elements_above_threshold(lst: List[T], 
                             threshold: int = 1, 
                             comparison: str = '>') -> List[Tuple[T, int]]:
    """
    Find elements with frequency above/below/equal to a threshold.
    
    Args:
        lst: The list to analyze.
        threshold: The frequency threshold to compare against.
        comparison: The comparison operator to use.
                   Possible values: '>', '>=', '=', '==', '<', '<='.
        
    Returns:
        A list of tuples (element, frequency) that match the comparison criteria.
        
    Raises:
        ValueError: If an invalid comparison operator is provided.
        
    Examples:
        >>> elements_above_threshold([1, 2, 2, 3, 1, 3, 3, 4], threshold=2, comparison='>')
        [(3, 3)]
        >>> elements_above_threshold([1, 2, 2, 3, 1, 3, 3, 4], threshold=2, comparison='>=')
        [(3, 3), (1, 2), (2, 2)]
    """
    if not lst:
        return []
    
    counter = Counter(lst)
    
    # Define comparison functions
    comparisons = {
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '=': lambda x, y: x == y,
        '==': lambda x, y: x == y,
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y,
    }
    
    if comparison not in comparisons:
        valid_ops = "', '".join(comparisons.keys())
        raise ValueError(f"Invalid comparison operator: '{comparison}'. Expected one of: '{valid_ops}'")
    
    # Filter elements based on the comparison
    compare_func = comparisons[comparison]
    return [(item, count) for item, count in counter.items() if compare_func(count, threshold)] 