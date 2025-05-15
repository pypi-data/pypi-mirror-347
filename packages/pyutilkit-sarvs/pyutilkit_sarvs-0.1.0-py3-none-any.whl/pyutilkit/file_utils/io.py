"""
Functions for reading and writing files.

This module provides utility functions for reading and writing
various file formats such as text, JSON, and CSV.
"""

import json
import csv
from typing import Any, Dict, List, Optional, Union


def read_text(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Read a text file and return its contents as a string.
    
    Args:
        filepath: Path to the file to read.
        encoding: Character encoding to use when reading the file.
        
    Returns:
        The contents of the file as a string.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there was an error reading the file.
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {str(e)}")


def write_text(filepath: str, content: str, encoding: str = 'utf-8', append: bool = False) -> None:
    """
    Write text content to a file.
    
    Args:
        filepath: Path to the file to write to.
        content: The string content to write.
        encoding: Character encoding to use when writing the file.
        append: Whether to append to the file (True) or overwrite it (False).
        
    Raises:
        IOError: If there was an error writing to the file.
    """
    mode = 'a' if append else 'w'
    try:
        with open(filepath, mode, encoding=encoding) as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file {filepath}: {str(e)}")


def read_json(filepath: str, encoding: str = 'utf-8') -> Any:
    """
    Read a JSON file and return its contents.
    
    Args:
        filepath: Path to the JSON file to read.
        encoding: Character encoding to use when reading the file.
        
    Returns:
        The parsed JSON content.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        IOError: If there was an error reading the file.
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {filepath}: {str(e)}", e.doc, e.pos)
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {str(e)}")


def write_json(filepath: str, 
               data: Any, 
               encoding: str = 'utf-8', 
               indent: Optional[int] = 4, 
               ensure_ascii: bool = False) -> None:
    """
    Write data to a JSON file.
    
    Args:
        filepath: Path to the file to write to.
        data: The data to write to the file.
        encoding: Character encoding to use when writing the file.
        indent: Number of spaces to indent the JSON for pretty-printing. 
                Use None for compact JSON.
        ensure_ascii: If True, non-ASCII characters are escaped. 
                      If False, non-ASCII characters are output as-is.
        
    Raises:
        TypeError: If the data cannot be serialized to JSON.
        IOError: If there was an error writing to the file.
    """
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    except TypeError as e:
        raise TypeError(f"Error serializing data to JSON: {str(e)}")
    except IOError as e:
        raise IOError(f"Error writing to file {filepath}: {str(e)}")


def read_csv(filepath: str, 
             delimiter: str = ',', 
             has_header: bool = True, 
             encoding: str = 'utf-8') -> Union[List[Dict[str, str]], List[List[str]]]:
    """
    Read a CSV file and return its contents.
    
    Args:
        filepath: Path to the CSV file to read.
        delimiter: Character used to separate fields in the CSV file.
        has_header: Whether the CSV file has a header row.
                    If True, returns a list of dictionaries.
                    If False, returns a list of lists.
        encoding: Character encoding to use when reading the file.
        
    Returns:
        If has_header is True, a list of dictionaries mapping headers to values.
        If has_header is False, a list of lists containing the row values.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        csv.Error: If there was an error parsing the CSV file.
        IOError: If there was an error reading the file.
    """
    try:
        with open(filepath, 'r', newline='', encoding=encoding) as f:
            if has_header:
                reader = csv.DictReader(f, delimiter=delimiter)
                return list(reader)
            else:
                reader = csv.reader(f, delimiter=delimiter)
                return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except csv.Error as e:
        raise csv.Error(f"Error parsing CSV file {filepath}: {str(e)}")
    except IOError as e:
        raise IOError(f"Error reading file {filepath}: {str(e)}")


def write_csv(filepath: str, 
              data: Union[List[Dict[str, Any]], List[List[Any]]], 
              fieldnames: Optional[List[str]] = None, 
              delimiter: str = ',', 
              encoding: str = 'utf-8') -> None:
    """
    Write data to a CSV file.
    
    Args:
        filepath: Path to the file to write to.
        data: The data to write to the file. Can be either a list of dictionaries
              (with fieldnames auto-extracted) or a list of lists.
        fieldnames: Column headers to use. Required if data is a list of dictionaries
                    and you want to specify the order of columns. If None, will be 
                    automatically extracted from the keys of the first dictionary.
        delimiter: Character to use as a field delimiter.
        encoding: Character encoding to use when writing the file.
        
    Raises:
        ValueError: If data is empty or has inconsistent structure.
        csv.Error: If there was an error writing the CSV file.
        IOError: If there was an error writing to the file.
    """
    try:
        with open(filepath, 'w', newline='', encoding=encoding) as f:
            if not data:
                if not fieldnames:
                    raise ValueError("Either data or fieldnames must be provided")
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerow(fieldnames)
                return
                
            # Check if data is a list of dictionaries
            if isinstance(data[0], dict):
                if not fieldnames:
                    fieldnames = list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            else:
                # Assume data is a list of lists
                writer = csv.writer(f, delimiter=delimiter)
                if fieldnames:
                    writer.writerow(fieldnames)
                writer.writerows(data)
    except csv.Error as e:
        raise csv.Error(f"Error writing CSV file {filepath}: {str(e)}")
    except IOError as e:
        raise IOError(f"Error writing to file {filepath}: {str(e)}") 