"""
Functions for manipulating strings.

This module provides utility functions for manipulating strings,
including removing specific characters, truncating, and padding.
"""

import re


def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation from a string.
    
    Args:
        text: The string to process.
        
    Returns:
        The string with all punctuation removed.
        
    Examples:
        >>> remove_punctuation("Hello, world!")
        'Hello world'
    """
    return re.sub(r'[^\w\s]', '', text)


def remove_digits(text: str) -> str:
    """
    Remove all digits from a string.
    
    Args:
        text: The string to process.
        
    Returns:
        The string with all digits removed.
        
    Examples:
        >>> remove_digits("Hello123World")
        'HelloWorld'
    """
    return re.sub(r'\d', '', text)


def remove_whitespace(text: str, keep_single_spaces: bool = False) -> str:
    """
    Remove whitespace from a string.
    
    Args:
        text: The string to process.
        keep_single_spaces: If True, single spaces between words will be preserved.
                           If False, all whitespace will be removed.
                           
    Returns:
        The string with whitespace removed according to the parameters.
        
    Examples:
        >>> remove_whitespace("Hello   world")
        'Helloworld'
        >>> remove_whitespace("Hello   world", keep_single_spaces=True)
        'Hello world'
    """
    if keep_single_spaces:
        # Replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', text).strip()
    else:
        # Remove all whitespace
        return re.sub(r'\s', '', text)


def truncate(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length.
    
    If the string is longer than max_length, it will be truncated and
    the suffix will be appended.
    
    Args:
        text: The string to truncate.
        max_length: The maximum length of the resulting string, including the suffix.
        suffix: The string to append to truncated strings.
        
    Returns:
        The truncated string.
        
    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, suffix='')
        'Hello wo'
    """
    if len(text) <= max_length:
        return text
    
    # Calculate the actual cutoff point
    cutoff = max_length - len(suffix)
    if cutoff < 0:
        cutoff = 0
    
    return text[:cutoff] + suffix


def pad_string(text: str, length: int, pad_char: str = ' ', align: str = 'left') -> str:
    """
    Pad a string to a specified length.
    
    Args:
        text: The string to pad.
        length: The target length after padding.
        pad_char: The character to use for padding.
        align: The alignment of the original text. 
               Possible values: 'left', 'right', 'center'.
               
    Returns:
        The padded string.
        
    Examples:
        >>> pad_string("Hello", 10)
        'Hello     '
        >>> pad_string("Hello", 10, pad_char='-', align='right')
        '-----Hello'
        >>> pad_string("Hello", 10, pad_char='*', align='center')
        '**Hello***'
    """
    if len(text) >= length:
        return text
    
    padding = pad_char * (length - len(text))
    
    if align == 'left':
        return text + padding
    elif align == 'right':
        return padding + text
    elif align == 'center':
        left_padding = padding[:len(padding) // 2]
        right_padding = padding[len(padding) // 2:]
        return left_padding + text + right_padding
    else:
        raise ValueError("align must be one of 'left', 'right', or 'center'") 