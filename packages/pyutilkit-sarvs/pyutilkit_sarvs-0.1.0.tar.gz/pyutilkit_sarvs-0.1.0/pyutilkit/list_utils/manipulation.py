"""
Functions for manipulating lists.

This module provides utility functions for manipulating lists,
including flattening, chunking, and removing duplicates.
"""

from typing import List, TypeVar, Optional, Any, Callable, Iterable, Set

# Define a type variable for list element types
T = TypeVar('T')


def flatten(nested_list: List[Any], depth: Optional[int] = None) -> List[Any]:
    """
    Flatten a nested list to a specified depth.
    
    Args:
        nested_list: The nested list to flatten.
        depth: How many levels to flatten. If None, flattens completely.
        
    Returns:
        A new flattened list.
        
    Examples:
        >>> flatten([1, [2, 3], [4, [5, 6]]])  # Flatten completely
        [1, 2, 3, 4, 5, 6]
        >>> flatten([1, [2, 3], [4, [5, 6]]], depth=1)  # Flatten only one level
        [1, 2, 3, 4, [5, 6]]
    """
    if not nested_list:
        return []
    
    result = []
    current_depth = 0
    
    def _flatten_inner(items: List[Any], current_depth: int) -> None:
        for item in items:
            if isinstance(item, list) and (depth is None or current_depth < depth):
                _flatten_inner(item, current_depth + 1)
            else:
                result.append(item)
    
    _flatten_inner(nested_list, current_depth)
    return result


def chunk(lst: List[T], size: int) -> List[List[T]]:
    """
    Split a list into chunks of a specified size.
    
    Args:
        lst: The list to split.
        size: The size of each chunk. Must be positive.
        
    Returns:
        A list of chunks (lists).
        
    Raises:
        ValueError: If size is not positive.
        
    Examples:
        >>> chunk([1, 2, 3, 4, 5, 6, 7], 3)
        [[1, 2, 3], [4, 5, 6], [7]]
        >>> chunk([1, 2, 3], 1)
        [[1], [2], [3]]
    """
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def remove_duplicates(lst: List[T], preserve_order: bool = True) -> List[T]:
    """
    Remove duplicate elements from a list.
    
    Args:
        lst: The list to process.
        preserve_order: Whether to preserve the original order of elements.
                       If False, the output may be in a different order.
        
    Returns:
        A new list with duplicates removed.
        
    Examples:
        >>> remove_duplicates([1, 2, 2, 3, 1, 4])
        [1, 2, 3, 4]
        >>> remove_duplicates(['a', 'b', 'c', 'b', 'a'])
        ['a', 'b', 'c']
    """
    if not lst:
        return []
    
    if preserve_order:
        # Using dict.fromkeys preserves order in Python 3.7+
        return list(dict.fromkeys(lst))
    else:
        # Using set is faster but doesn't preserve order
        return list(set(lst)) 