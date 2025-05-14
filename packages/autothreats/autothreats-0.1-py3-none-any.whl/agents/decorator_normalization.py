#!/usr/bin/env python3
"""
Decorator-based Normalization Agent for the autonomous threat modeling system.
Uses the decorator API for simplified implementation.
"""

import asyncio
import logging
import os
import re
from typing import Any, Callable, Dict, List, Optional

from ..models.codebase_model import CodebaseModel
from ..utils.agent_decorators import agent

logger = logging.getLogger(__name__)


@agent(agent_id="normalization", agent_type="normalization")
async def normalization(
    agent, task_type: str, task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process code normalization tasks.

    Args:
        agent: The agent instance
        task_type: The type of task to process
        task_data: The data for the task

    Returns:
        Result data
    """
    agent.logger.info(f"Processing task of type: {task_type}")

    # Initialize language parsers if not already set
    if not hasattr(agent, "language_parsers"):
        agent.language_parsers = {
            ".py": _parse_python,
            ".js": _parse_javascript,
            ".ts": _parse_typescript,
            ".java": _parse_java,
            ".c": _parse_c,
            ".cpp": _parse_cpp,
            ".cs": _parse_csharp,
            ".go": _parse_go,
            ".php": _parse_php,
            ".rb": _parse_ruby,
            ".sh": _parse_shell,
        }

    # Handle normalization task
    if task_type in ["normalize_code", "normalization"]:
        # Validate required parameters
        job_id = task_data.get("job_id")
        codebase_id = task_data.get("codebase_id")

        # Check for missing parameters
        missing_params = []
        if not job_id:
            missing_params.append("job_id")
        if not codebase_id:
            missing_params.append("codebase_id")

        if missing_params:
            error_msg = f"Missing required parameters: {', '.join(missing_params)}"
            agent.logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "missing_parameters": missing_params,
            }

        # Get codebase from workspace
        codebase = agent.workspace.get_data(codebase_id)
        if not codebase:
            return {"status": "error", "message": f"Codebase not found: {codebase_id}"}

        # Convert to CodebaseModel if needed
        if isinstance(codebase, dict):
            codebase_model = CodebaseModel.from_dict(codebase)
        elif isinstance(codebase, CodebaseModel):
            codebase_model = codebase
        else:
            return {
                "status": "error",
                "message": f"Invalid codebase format: {type(codebase)}",
            }

        # Create a new normalized codebase model
        normalized_codebase = CodebaseModel()
        normalized_codebase.id = f"normalized_{codebase_id}"
        normalized_codebase.path = codebase_model.path

        # Process each file in the codebase
        for file_path, content in codebase_model.files.items():
            # Skip if content is not a string
            if not isinstance(content, str):
                continue

            # Get file extension
            _, ext = os.path.splitext(file_path)

            # Normalize the file content based on its extension
            if ext.lower() in agent.language_parsers:
                normalized_content = agent.language_parsers[ext.lower()](content)
            else:
                # For unknown file types, just remove comments and extra whitespace
                normalized_content = _remove_comments_and_whitespace(content)

            # Add normalized file to the new codebase
            normalized_codebase.add_file(file_path, normalized_content)

        # Store the normalized codebase in the workspace
        normalized_codebase_id = f"normalized_{codebase_id}"
        agent.workspace.store_data(normalized_codebase_id, normalized_codebase)

        # Return success
        return {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "normalized_codebase_id": normalized_codebase_id,
            "file_count": len(normalized_codebase.files),
            "status": "success",
            "message": f"Normalized {len(normalized_codebase.files)} files",
        }
    else:
        return {"status": "error", "message": f"Unsupported task type: {task_type}"}


# Language-specific parsers


def _parse_python(content: str) -> str:
    """Parse and normalize Python code"""
    # Remove comments
    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)

    # Remove docstrings (simplified approach)
    content = re.sub(r'""".*?"""', "", content, flags=re.DOTALL)
    content = re.sub(r"'''.*?'''", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_javascript(content: str) -> str:
    """Parse and normalize JavaScript code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_typescript(content: str) -> str:
    """Parse and normalize TypeScript code"""
    # TypeScript is similar to JavaScript
    return _parse_javascript(content)


def _parse_java(content: str) -> str:
    """Parse and normalize Java code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_c(content: str) -> str:
    """Parse and normalize C code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_cpp(content: str) -> str:
    """Parse and normalize C++ code"""
    # C++ is similar to C
    return _parse_c(content)


def _parse_csharp(content: str) -> str:
    """Parse and normalize C# code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_go(content: str) -> str:
    """Parse and normalize Go code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_php(content: str) -> str:
    """Parse and normalize PHP code"""
    # Remove single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)

    # Remove multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_ruby(content: str) -> str:
    """Parse and normalize Ruby code"""
    # Remove comments
    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _parse_shell(content: str) -> str:
    """Parse and normalize shell scripts"""
    # Remove comments
    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content


def _remove_comments_and_whitespace(content: str) -> str:
    """Generic function to remove common comment styles and extra whitespace"""
    # Try to remove common comment styles
    # Single-line comments
    content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)

    # Multi-line comments
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r"\s+", " ", content)

    return content
