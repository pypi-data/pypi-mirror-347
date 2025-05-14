#!/usr/bin/env python3
"""
File utility functions for the autonomous threat modeling system.
Provides functions for reading, writing, and listing files.
"""

import glob
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


def read_file(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    Read the contents of a file.

    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        File contents as a string, or None if the file could not be read
    """
    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            content = f.read()
        logger.debug(f"Read {len(content)} bytes from {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return None


def write_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """
    Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        encoding: File encoding (default: utf-8)

    Returns:
        True if the file was written successfully, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        logger.debug(f"Wrote {len(content)} bytes to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {str(e)}")
        return False


def list_files(
    directory: str, pattern: str = "*", recursive: bool = False
) -> List[str]:
    """
    List files in a directory matching a pattern.

    Args:
        directory: Directory to list files from
        pattern: Glob pattern to match files (default: '*')
        recursive: Whether to search recursively (default: False)

    Returns:
        List of file paths matching the pattern
    """
    try:
        if not os.path.exists(directory):
            logger.warning(f"Directory {directory} does not exist")
            return []

        if recursive:
            # Use ** for recursive glob
            search_pattern = os.path.join(directory, "**", pattern)
            files = glob.glob(search_pattern, recursive=True)
        else:
            search_pattern = os.path.join(directory, pattern)
            files = glob.glob(search_pattern)

        # Sort files for consistent results
        files.sort()

        logger.debug(f"Found {len(files)} files matching {search_pattern}")
        return files
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        return []


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about a file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file information (size, modification time, etc.)
    """
    try:
        if not os.path.exists(file_path):
            return {"exists": False}

        stat = os.stat(file_path)
        return {
            "exists": True,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "is_dir": os.path.isdir(file_path),
            "extension": (
                os.path.splitext(file_path)[1].lower()
                if not os.path.isdir(file_path)
                else ""
            ),
            "basename": os.path.basename(file_path),
        }
    except Exception as e:
        logger.error(f"Error getting file info for {file_path}: {str(e)}")
        return {"exists": False, "error": str(e)}


def ensure_directory(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path to ensure exists

    Returns:
        True if the directory exists or was created, False otherwise
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Created directory {directory}")
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get the extension of a file.

    Args:
        file_path: Path to the file

    Returns:
        File extension (lowercase, without the dot)
    """
    return os.path.splitext(file_path)[1].lower().lstrip(".")


def is_binary_file(file_path: str) -> bool:
    """
    Check if a file is binary.

    Args:
        file_path: Path to the file

    Returns:
        True if the file is binary, False otherwise
    """
    try:
        # Check file extension first
        ext = get_file_extension(file_path)
        binary_extensions = {
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "gif",
            "zip",
            "tar",
            "gz",
            "exe",
            "dll",
            "so",
            "pyc",
        }
        if ext in binary_extensions:
            return True

        # Read the first 8KB of the file
        with open(file_path, "rb") as f:
            chunk = f.read(8192)

        # Check for null bytes (common in binary files)
        if b"\x00" in chunk:
            return True

        # Try to decode as text
        try:
            chunk.decode("utf-8")
            return False
        except UnicodeDecodeError:
            return True
    except Exception as e:
        logger.error(f"Error checking if {file_path} is binary: {str(e)}")
        return False
