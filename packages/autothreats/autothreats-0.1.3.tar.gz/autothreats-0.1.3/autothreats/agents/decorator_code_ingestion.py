#!/usr/bin/env python3
"""
Decorator-based Code Ingestion Agent for the autonomous threat modeling system.
Uses the decorator API for simplified implementation.
"""

import asyncio
import logging
import os
import re
from typing import Any, Dict, List, Optional, Set

from ..models.codebase_model import CodebaseModel
from ..utils.agent_decorators import agent

logger = logging.getLogger(__name__)


@agent(agent_id="code_ingestion", agent_type="code_ingestion", is_agentic=True)
async def code_ingestion(
    agent, task_type: str, task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process code ingestion tasks.

    Args:
        agent: The agent instance
        task_type: The type of task to process
        task_data: The data for the task

    Returns:
        Result data
    """
    agent.logger.info(f"Processing task of type: {task_type}")

    # Initialize configuration parameters if not already set
    if not hasattr(agent, "max_workers"):
        agent.max_workers = agent.model.config.get("max_workers", 4)
        agent.max_files = agent.model.config.get("max_files", 10000)
        agent.max_file_size = agent.model.config.get(
            "max_file_size", 60 * 1024
        )  # 60KB default

        # Store any ignored file patterns from config
        agent.ignored_patterns = agent.model.config.get(
            "ignored_patterns",
            [
                ".git",
                ".svn",
                ".hg",
                ".vscode",
                ".idea",  # Version control and IDE files
                "node_modules",
                "venv",
                "env",
                ".env",  # Dependencies
                "__pycache__",
                "*.pyc",
                "*.pyo",  # Python cache
                "dist",
                "build",
                "target",  # Build directories
                "*.min.js",
                "*.min.css",  # Minified files
                "*.log",
                "logs",  # Log files
                "*.zip",
                "*.tar.gz",
                "*.jar",
                "*.war",  # Archives
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.gif",
                "*.ico",  # Images
                "*.mp3",
                "*.mp4",
                "*.avi",
                "*.mov",  # Media
                "*.pdf",
                "*.doc",
                "*.docx",
                "*.xls",
                "*.xlsx",  # Documents
            ],
        )

    # Handle code ingestion task
    if task_type in ["ingest_code", "code_ingestion"]:
        # Validate required parameters
        job_id = task_data.get("job_id")
        codebase_path = task_data.get("codebase_path")

        # Check for missing parameters
        missing_params = []
        if not job_id:
            missing_params.append("job_id")
        if not codebase_path:
            missing_params.append("codebase_path")

        if missing_params:
            error_msg = f"Missing required parameters: {', '.join(missing_params)}"
            agent.logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "missing_parameters": missing_params,
            }

        # Check if path exists
        if not os.path.exists(codebase_path):
            return {
                "status": "error",
                "message": f"Codebase path does not exist: {codebase_path}",
            }

        # Create a new codebase model
        codebase_model = CodebaseModel()
        codebase_model.id = f"codebase_{job_id}"
        codebase_model.path = codebase_path

        # Process the codebase
        try:
            # If it's a file, just read it
            if os.path.isfile(codebase_path):
                await _process_file(
                    codebase_model, codebase_path, "", agent.max_file_size
                )
            # If it's a directory, walk through it
            elif os.path.isdir(codebase_path):
                files_processed = 0
                for root, dirs, files in os.walk(codebase_path):
                    # Skip ignored directories
                    dirs[:] = [
                        d for d in dirs if not _should_ignore(d, agent.ignored_patterns)
                    ]

                    # Process each file
                    for file in files:
                        # Skip ignored files
                        if _should_ignore(file, agent.ignored_patterns):
                            continue

                        # Get full file path
                        file_path = os.path.join(root, file)

                        # Get relative path
                        rel_path = os.path.relpath(file_path, codebase_path)

                        # Process the file
                        await _process_file(
                            codebase_model, file_path, rel_path, agent.max_file_size
                        )

                        # Increment counter
                        files_processed += 1

                        # Check if we've reached the max files limit
                        if files_processed >= agent.max_files:
                            agent.logger.warning(
                                f"Reached max files limit ({agent.max_files}), stopping ingestion"
                            )
                            break

                    # Check if we've reached the max files limit
                    if files_processed >= agent.max_files:
                        break

            # Store the codebase model in the workspace
            codebase_id = f"codebase_{job_id}"
            agent.workspace.store_data(codebase_id, codebase_model)

            # Return success
            return {
                "job_id": job_id,
                "codebase_id": codebase_id,
                "file_count": len(codebase_model.files),
                "status": "success",
                "message": f"Ingested {len(codebase_model.files)} files from {codebase_path}",
            }
        except Exception as e:
            agent.logger.error(f"Error ingesting codebase: {e}")
            return {"status": "error", "message": f"Error ingesting codebase: {str(e)}"}
    else:
        return {"status": "error", "message": f"Unsupported task type: {task_type}"}


async def _process_file(
    codebase_model: CodebaseModel, file_path: str, rel_path: str, max_file_size: int
):
    """Process a single file and add it to the codebase model"""
    try:
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_file_size:
            logger.debug(
                f"Skipping file {file_path} (size: {file_size} > max: {max_file_size})"
            )
            return

        # Read file content
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Add file to codebase model
        codebase_model.add_file(rel_path, content)
    except Exception as e:
        logger.debug(f"Error processing file {file_path}: {e}")


def _should_ignore(path: str, ignored_patterns: List[str]) -> bool:
    """Check if a path should be ignored based on patterns"""
    path_lower = path.lower()

    # Check each pattern
    for pattern in ignored_patterns:
        # Handle glob patterns
        if pattern.startswith("*"):
            suffix = pattern[1:]
            if path_lower.endswith(suffix):
                return True
        # Handle directory/file names
        elif pattern in path_lower:
            return True

    return False
