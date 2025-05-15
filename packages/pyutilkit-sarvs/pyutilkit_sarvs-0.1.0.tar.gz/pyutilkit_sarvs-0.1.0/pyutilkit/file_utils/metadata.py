"""
Functions for getting file metadata.

This module provides utility functions for retrieving metadata
about files, such as file size, last modified time, and extension.
"""

import os
import datetime
from typing import Union


def get_file_size(filepath: str, unit: str = 'bytes') -> float:
    """
    Get the size of a file.
    
    Args:
        filepath: Path to the file.
        unit: The unit to return the file size in. 
              Possible values: 'bytes', 'KB', 'MB', 'GB'.
              
    Returns:
        The size of the file in the specified unit.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If an invalid unit is specified.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    size_bytes = os.path.getsize(filepath)
    
    unit = unit.upper() if unit.lower() in ['kb', 'mb', 'gb'] else unit.lower()
    
    if unit == 'bytes':
        return size_bytes
    elif unit == 'KB':
        return size_bytes / 1024
    elif unit == 'MB':
        return size_bytes / (1024 * 1024)
    elif unit == 'GB':
        return size_bytes / (1024 * 1024 * 1024)
    else:
        raise ValueError(f"Invalid unit: {unit}. Expected one of: 'bytes', 'KB', 'MB', 'GB'")


def get_last_modified_time(filepath: str, as_datetime: bool = False) -> Union[float, datetime.datetime]:
    """
    Get the last modified time of a file.
    
    Args:
        filepath: Path to the file.
        as_datetime: If True, returns a datetime object. 
                     If False, returns a timestamp (seconds since Unix epoch).
                     
    Returns:
        The last modified time of the file as either a datetime object or a timestamp.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    timestamp = os.path.getmtime(filepath)
    
    if as_datetime:
        return datetime.datetime.fromtimestamp(timestamp)
    else:
        return timestamp


def get_file_extension(filepath: str, with_dot: bool = True) -> str:
    """
    Get the extension of a file.
    
    Args:
        filepath: Path to the file.
        with_dot: Whether to include the dot in the extension.
        
    Returns:
        The extension of the file. If the file has no extension, returns an empty string.
    """
    _, extension = os.path.splitext(filepath)
    
    if extension and not with_dot:
        return extension[1:]
    
    return extension 