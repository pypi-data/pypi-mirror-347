"""
File utility functions for common file operations.

This module provides utility functions for working with files,
including reading/writing files, file metadata, and file management.
"""

from .io import (
    read_text,
    write_text,
    read_json,
    write_json,
    read_csv,
    write_csv
)

from .metadata import (
    get_file_size,
    get_last_modified_time,
    get_file_extension
)

from .management import (
    create_file,
    create_directory,
    rename_file,
    delete_file,
    merge_csv_files,
    merge_json_files
)

__all__ = [
    'read_text',
    'write_text',
    'read_json',
    'write_json',
    'read_csv',
    'write_csv',
    'get_file_size',
    'get_last_modified_time',
    'get_file_extension',
    'create_file',
    'create_directory',
    'rename_file',
    'delete_file',
    'merge_csv_files',
    'merge_json_files'
] 