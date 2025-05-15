"""
Functions for converting between different string case formats.

This module provides utility functions for converting strings between
different case formats such as snake_case, camelCase, and PascalCase.
"""

import re


def to_snake_case(text: str) -> str:
    """
    Convert a string to snake_case.
    
    Args:
        text: The string to convert.
        
    Returns:
        The converted string in snake_case format.
        
    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("helloWorld")
        'hello_world'
        >>> to_snake_case("Hello-World")
        'hello_world'
    """
    # Replace hyphens with spaces
    s = text.replace('-', ' ')
    
    # Insert space before uppercase letters
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s)
    
    # Replace spaces with underscores and convert to lowercase
    s = s.lower().replace(' ', '_')
    
    # Remove any non-alphanumeric characters (except underscores)
    s = re.sub(r'[^a-z0-9_]', '', s)
    
    # Replace multiple underscores with a single one
    s = re.sub(r'_+', '_', s)
    
    return s


def to_camel_case(text: str) -> str:
    """
    Convert a string to camelCase.
    
    Args:
        text: The string to convert.
        
    Returns:
        The converted string in camelCase format.
        
    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("HelloWorld")
        'helloWorld'
        >>> to_camel_case("hello-world")
        'helloWorld'
    """
    # First convert to snake_case to handle various input formats
    s = to_snake_case(text)
    
    # Split by underscore
    words = s.split('_')
    
    # Join with first word lowercase and others capitalized
    if not words:
        return ""
    
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(text: str) -> str:
    """
    Convert a string to PascalCase.
    
    Args:
        text: The string to convert.
        
    Returns:
        The converted string in PascalCase format.
        
    Examples:
        >>> to_pascal_case("hello_world")
        'HelloWorld'
        >>> to_pascal_case("helloWorld")
        'HelloWorld'
        >>> to_pascal_case("hello-world")
        'HelloWorld'
    """
    # First convert to snake_case to handle various input formats
    s = to_snake_case(text)
    
    # Split by underscore and capitalize each word
    words = s.split('_')
    
    # Join with all words capitalized
    return ''.join(word.capitalize() for word in words) 