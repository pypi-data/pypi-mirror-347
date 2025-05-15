"""
Functions for file and directory management.

This module provides utility functions for managing files and directories,
including creating, renaming, deleting, and merging files.
"""

import os
import shutil
import json
import csv
from typing import Any, Dict, List, Optional, Union


def create_file(filepath: str, content: str = "", encoding: str = 'utf-8', overwrite: bool = False) -> bool:
    """
    Create a new file with optional content.
    
    Args:
        filepath: Path of the file to create.
        content: Optional content to write to the file.
        encoding: Character encoding to use when writing the file.
        overwrite: Whether to overwrite the file if it already exists.
        
    Returns:
        True if the file was created (or overwritten), False if the file already exists
        and overwrite is False.
        
    Raises:
        IOError: If there was an error creating the file.
    """
    if os.path.exists(filepath) and not overwrite:
        return False
    
    # Create parent directories if they don't exist
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
        with open(filepath, 'w', encoding=encoding) as f:
            if content:
                f.write(content)
        return True
    except IOError as e:
        raise IOError(f"Error creating file {filepath}: {str(e)}")


def create_directory(dirpath: str, exist_ok: bool = True) -> bool:
    """
    Create a new directory and its parent directories if they don't exist.
    
    Args:
        dirpath: Path of the directory to create.
        exist_ok: If False, raise an error if the directory already exists.
        
    Returns:
        True if the directory was created, False if it already existed and exist_ok is True.
        
    Raises:
        FileExistsError: If the directory already exists and exist_ok is False.
        IOError: If there was an error creating the directory.
    """
    try:
        if os.path.exists(dirpath):
            if exist_ok:
                return False
            else:
                raise FileExistsError(f"Directory already exists: {dirpath}")
                
        os.makedirs(dirpath)
        return True
    except FileExistsError:
        raise
    except IOError as e:
        raise IOError(f"Error creating directory {dirpath}: {str(e)}")


def rename_file(source: str, destination: str, overwrite: bool = False) -> bool:
    """
    Rename or move a file from source to destination.
    
    Args:
        source: Path of the file to rename/move.
        destination: New path for the file.
        overwrite: Whether to overwrite the destination if it already exists.
        
    Returns:
        True if the file was successfully renamed/moved.
        
    Raises:
        FileNotFoundError: If the source file does not exist.
        FileExistsError: If the destination already exists and overwrite is False.
        IOError: If there was an error renaming/moving the file.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file not found: {source}")
    
    if os.path.exists(destination) and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")
    
    # Create parent directories of destination if they don't exist
    dest_dir = os.path.dirname(destination)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    try:
        shutil.move(source, destination)
        return True
    except IOError as e:
        raise IOError(f"Error renaming/moving file from {source} to {destination}: {str(e)}")


def delete_file(filepath: str, missing_ok: bool = True) -> bool:
    """
    Delete a file.
    
    Args:
        filepath: Path of the file to delete.
        missing_ok: If True, don't raise an error if the file doesn't exist.
        
    Returns:
        True if the file was deleted, False if it didn't exist and missing_ok is True.
        
    Raises:
        FileNotFoundError: If the file does not exist and missing_ok is False.
        IOError: If there was an error deleting the file.
    """
    if not os.path.exists(filepath):
        if missing_ok:
            return False
        else:
            raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        os.remove(filepath)
        return True
    except IOError as e:
        raise IOError(f"Error deleting file {filepath}: {str(e)}")


def merge_csv_files(filepaths: List[str], 
                    output_filepath: str, 
                    delimiter: str = ',', 
                    encoding: str = 'utf-8') -> int:
    """
    Merge multiple CSV files into a single file.
    
    Args:
        filepaths: List of paths to the CSV files to merge.
        output_filepath: Path of the output merged CSV file.
        delimiter: Character used to separate fields in the CSV files.
        encoding: Character encoding to use when reading/writing the files.
        
    Returns:
        Number of rows in the merged file.
        
    Raises:
        FileNotFoundError: If any of the input files does not exist.
        csv.Error: If there was an error parsing any of the CSV files.
        IOError: If there was an error reading or writing the files.
    """
    if not filepaths:
        raise ValueError("No input files specified")
    
    # Check if all files exist
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
    
    # Create parent directories of output file if they don't exist
    output_dir = os.path.dirname(output_filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    row_count = 0
    
    try:
        with open(output_filepath, 'w', newline='', encoding=encoding) as outfile:
            writer = None
            
            for i, filepath in enumerate(filepaths):
                with open(filepath, 'r', newline='', encoding=encoding) as infile:
                    reader = csv.reader(infile, delimiter=delimiter)
                    
                    # For the first file, copy the header and initialize the writer
                    if i == 0:
                        header = next(reader)
                        writer = csv.writer(outfile, delimiter=delimiter)
                        writer.writerow(header)
                        row_count += 1
                    else:
                        # Skip the header for subsequent files
                        next(reader)
                    
                    # Copy the data rows
                    for row in reader:
                        writer.writerow(row)
                        row_count += 1
                        
        return row_count
    except csv.Error as e:
        raise csv.Error(f"Error processing CSV file: {str(e)}")
    except IOError as e:
        raise IOError(f"Error processing file: {str(e)}")


def merge_json_files(filepaths: List[str], 
                     output_filepath: str, 
                     merge_mode: str = 'concat_arrays', 
                     encoding: str = 'utf-8') -> Any:
    """
    Merge multiple JSON files into a single file.
    
    Args:
        filepaths: List of paths to the JSON files to merge.
        output_filepath: Path of the output merged JSON file.
        merge_mode: How to merge the JSON files. Options:
                    - 'concat_arrays': Concatenate arrays from different files.
                    - 'merge_objects': Merge objects, with later files overriding earlier ones.
        encoding: Character encoding to use when reading/writing the files.
        
    Returns:
        The merged JSON data.
        
    Raises:
        FileNotFoundError: If any of the input files does not exist.
        ValueError: If an invalid merge_mode is specified.
        json.JSONDecodeError: If any of the input files contains invalid JSON.
        IOError: If there was an error reading or writing the files.
    """
    if not filepaths:
        raise ValueError("No input files specified")
    
    if merge_mode not in ['concat_arrays', 'merge_objects']:
        raise ValueError(f"Invalid merge_mode: {merge_mode}. Expected one of: 'concat_arrays', 'merge_objects'")
    
    # Check if all files exist
    for filepath in filepaths:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
    
    # Create parent directories of output file if they don't exist
    output_dir = os.path.dirname(output_filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    result = None
    
    try:
        for filepath in filepaths:
            with open(filepath, 'r', encoding=encoding) as f:
                data = json.load(f)
                
                if result is None:
                    result = data
                else:
                    if merge_mode == 'concat_arrays':
                        if isinstance(result, list) and isinstance(data, list):
                            result.extend(data)
                        else:
                            raise ValueError(f"Cannot concat non-arrays when merge_mode is 'concat_arrays'")
                    elif merge_mode == 'merge_objects':
                        if isinstance(result, dict) and isinstance(data, dict):
                            # Recursively merge dictionaries
                            def merge_dicts(d1, d2):
                                for key, value in d2.items():
                                    if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                                        merge_dicts(d1[key], value)
                                    else:
                                        d1[key] = value
                            
                            merge_dicts(result, data)
                        else:
                            raise ValueError(f"Cannot merge non-objects when merge_mode is 'merge_objects'")
        
        # Write the merged data to the output file
        with open(output_filepath, 'w', encoding=encoding) as f:
            json.dump(result, f, indent=4)
        
        return result
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in one of the input files: {str(e)}", e.doc, e.pos)
    except IOError as e:
        raise IOError(f"Error processing file: {str(e)}")