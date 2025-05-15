"""
Functions for transforming lists.

This module provides utility functions for transforming
lists between different types and formats.
"""

from typing import List, Any, TypeVar, Optional, Union, Callable

# Define a type variable for list element types
T = TypeVar('T')


def to_string_list(lst: List[Any], format_spec: Optional[str] = None) -> List[str]:
    """
    Convert all elements in a list to strings.
    
    Args:
        lst: The list to convert.
        format_spec: Optional format specification string for formatting
                    (e.g., '.2f' for floats with 2 decimal places).
        
    Returns:
        A new list with all elements converted to strings.
        
    Examples:
        >>> to_string_list([1, 2.5, True, None])
        ['1', '2.5', 'True', 'None']
        >>> to_string_list([1.2345, 5.6789], format_spec='.2f')
        ['1.23', '5.68']
    """
    if format_spec is not None:
        return [format(item, format_spec) if item is not None else 'None' for item in lst]
    else:
        return [str(item) for item in lst]


def to_int_list(lst: List[Any], 
                on_error: str = 'raise', 
                default: Optional[int] = None) -> List[int]:
    """
    Convert all elements in a list to integers.
    
    Args:
        lst: The list to convert.
        on_error: How to handle conversion errors:
                 'raise' - raise an exception
                 'skip' - skip the element
                 'default' - use the default value
        default: Default value to use when on_error is 'default'.
        
    Returns:
        A new list with all elements converted to integers.
        
    Raises:
        ValueError: If on_error is 'raise' and an element can't be converted.
        
    Examples:
        >>> to_int_list(['1', '2', '3'])
        [1, 2, 3]
        >>> to_int_list(['1', '2.5', 'x'], on_error='skip')
        [1]
        >>> to_int_list(['1', '2.5', 'x'], on_error='default', default=0)
        [1, 2, 0]
    """
    if on_error not in ('raise', 'skip', 'default'):
        raise ValueError(f"Invalid on_error value: {on_error}. Expected one of: 'raise', 'skip', 'default'")
    
    result = []
    
    for item in lst:
        try:
            # Handle floats by truncating
            if isinstance(item, float):
                result.append(int(item))
            else:
                result.append(int(item))
        except (ValueError, TypeError):
            if on_error == 'raise':
                raise ValueError(f"Could not convert {item} to int")
            elif on_error == 'skip':
                continue
            elif on_error == 'default':
                result.append(default)
    
    return result


def to_float_list(lst: List[Any], 
                  on_error: str = 'raise', 
                  default: Optional[float] = None) -> List[float]:
    """
    Convert all elements in a list to floats.
    
    Args:
        lst: The list to convert.
        on_error: How to handle conversion errors:
                 'raise' - raise an exception
                 'skip' - skip the element
                 'default' - use the default value
        default: Default value to use when on_error is 'default'.
        
    Returns:
        A new list with all elements converted to floats.
        
    Raises:
        ValueError: If on_error is 'raise' and an element can't be converted.
        
    Examples:
        >>> to_float_list(['1', '2.5', '3'])
        [1.0, 2.5, 3.0]
        >>> to_float_list(['1', 'x', '3'], on_error='skip')
        [1.0, 3.0]
        >>> to_float_list(['1', 'x', '3'], on_error='default', default=0.0)
        [1.0, 0.0, 3.0]
    """
    if on_error not in ('raise', 'skip', 'default'):
        raise ValueError(f"Invalid on_error value: {on_error}. Expected one of: 'raise', 'skip', 'default'")
    
    result = []
    
    for item in lst:
        try:
            result.append(float(item))
        except (ValueError, TypeError):
            if on_error == 'raise':
                raise ValueError(f"Could not convert {item} to float")
            elif on_error == 'skip':
                continue
            elif on_error == 'default':
                result.append(default)
    
    return result 