"""
Functions for validating string properties.

This module provides utility functions for validating
various properties of strings.
"""

from collections import Counter


def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if a string is a palindrome.
    
    A palindrome is a string that reads the same forward and backward.
    
    Args:
        text: The string to check.
        ignore_case: Whether to perform a case-insensitive check.
        ignore_spaces: Whether to ignore spaces when checking.
        
    Returns:
        True if the string is a palindrome, False otherwise.
        
    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("Race Car", ignore_spaces=True)
        True
        >>> is_palindrome("Hello")
        False
    """
    if not text:
        return True
    
    # Prepare the string for comparison
    s = text
    if ignore_case:
        s = s.lower()
    if ignore_spaces:
        s = s.replace(" ", "")
    
    # Compare the string with its reverse
    return s == s[::-1]


def is_anagram(text1: str, text2: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if two strings are anagrams of each other.
    
    Anagrams are strings that use the same characters in different orders.
    
    Args:
        text1: The first string.
        text2: The second string.
        ignore_case: Whether to perform a case-insensitive check.
        ignore_spaces: Whether to ignore spaces when checking.
        
    Returns:
        True if the strings are anagrams, False otherwise.
        
    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("Astronomer", "Moon starer")
        True
        >>> is_anagram("hello", "world")
        False
    """
    if not text1 and not text2:
        return True
    
    # Prepare the strings for comparison
    s1, s2 = text1, text2
    if ignore_case:
        s1, s2 = s1.lower(), s2.lower()
    if ignore_spaces:
        s1, s2 = s1.replace(" ", ""), s2.replace(" ", "")
    
    # Compare character counts
    return Counter(s1) == Counter(s2) 