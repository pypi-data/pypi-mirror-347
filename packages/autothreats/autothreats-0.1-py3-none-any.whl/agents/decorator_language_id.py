#!/usr/bin/env python3
"""
Decorator-based Language Identification Agent for the autonomous threat modeling system.
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


@agent(agent_id="language_id", agent_type="language_id")
async def language_id(
    agent, task_type: str, task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process language identification tasks.

    Args:
        agent: The agent instance
        task_type: The type of task to process
        task_data: The data for the task

    Returns:
        Result data
    """
    agent.logger.info(f"Processing task of type: {task_type}")

    # Initialize language patterns if not already set
    if not hasattr(agent, "language_patterns"):
        agent.language_patterns = {
            "python": [
                r"\.py$",
                r"import\s+[a-zA-Z0-9_]+",
                r"from\s+[a-zA-Z0-9_\.]+\s+import",
                r"def\s+[a-zA-Z0-9_]+\s*\(",
                r"class\s+[a-zA-Z0-9_]+\s*[:\(]",
            ],
            "javascript": [
                r"\.js$",
                r"const\s+[a-zA-Z0-9_]+",
                r"let\s+[a-zA-Z0-9_]+",
                r"function\s+[a-zA-Z0-9_]+\s*\(",
                r"export\s+",
                r"import\s+.*from",
            ],
            "typescript": [
                r"\.ts$",
                r"\.tsx$",
                r"interface\s+[a-zA-Z0-9_]+",
                r"type\s+[a-zA-Z0-9_]+",
                r"export\s+interface",
            ],
            "java": [
                r"\.java$",
                r"public\s+class",
                r"private\s+[a-zA-Z0-9_]+",
                r"protected\s+[a-zA-Z0-9_]+",
                r"import\s+java\.",
            ],
            "c": [
                r"\.c$",
                r"#include\s+<[a-zA-Z0-9_\.]+>",
                r"void\s+[a-zA-Z0-9_]+\s*\(",
                r"int\s+main\s*\(",
            ],
            "cpp": [
                r"\.cpp$",
                r"\.hpp$",
                r"namespace\s+[a-zA-Z0-9_]+",
                r"template\s*<",
                r"std::",
            ],
            "csharp": [
                r"\.cs$",
                r"using\s+System",
                r"namespace\s+[a-zA-Z0-9_\.]+",
                r"public\s+class",
            ],
            "go": [r"\.go$", r"package\s+[a-zA-Z0-9_]+", r"import\s+\(", r"func\s+\("],
            "ruby": [
                r"\.rb$",
                r'require\s+[\'"][a-zA-Z0-9_]+[\'"]',
                r"def\s+[a-zA-Z0-9_]+",
                r"class\s+[a-zA-Z0-9_]+",
            ],
            "php": [
                r"\.php$",
                r"<\?php",
                r"function\s+[a-zA-Z0-9_]+\s*\(",
                r"namespace\s+[a-zA-Z0-9_\\]+",
            ],
            "html": [
                r"\.html$",
                r"\.htm$",
                r"<!DOCTYPE\s+html>",
                r"<html",
                r"<head",
                r"<body",
            ],
            "css": [r"\.css$", r"\{[^}]*:[^}]*\}", r"@media", r"@import"],
            "shell": [r"\.sh$", r"#!/bin/bash", r"#!/bin/sh", r"#!/usr/bin/env\s+bash"],
            "sql": [r"\.sql$", r"SELECT\s+.*FROM", r"INSERT\s+INTO", r"CREATE\s+TABLE"],
            "rust": [
                r"\.rs$",
                r"fn\s+[a-zA-Z0-9_]+",
                r"struct\s+[a-zA-Z0-9_]+",
                r"impl\s+",
            ],
            "swift": [
                r"\.swift$",
                r"import\s+Foundation",
                r"class\s+[a-zA-Z0-9_]+",
                r"func\s+[a-zA-Z0-9_]+",
            ],
            "kotlin": [
                r"\.kt$",
                r"fun\s+[a-zA-Z0-9_]+",
                r"class\s+[a-zA-Z0-9_]+",
                r"val\s+[a-zA-Z0-9_]+",
                r"var\s+[a-zA-Z0-9_]+",
            ],
            "perl": [r"\.pl$", r"use\s+[a-zA-Z0-9_:]+", r"sub\s+[a-zA-Z0-9_]+"],
            "r": [r"\.r$", r"\.R$", r"library\(", r"function\s*\("],
        }

    # Handle language identification task
    if task_type in ["identify_language", "language_id"]:
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

        # Identify languages for each file
        language_stats = {}
        file_languages = {}

        for file_path, content in codebase_model.files.items():
            # Skip if content is not a string
            if not isinstance(content, str):
                continue

            # Identify language for this file
            language = _identify_file_language(
                file_path, content, agent.language_patterns
            )

            # Update statistics
            if language:
                language_stats[language] = language_stats.get(language, 0) + 1
                file_languages[file_path] = language

        # Determine primary language
        primary_language = None
        max_count = 0
        for language, count in language_stats.items():
            if count > max_count:
                max_count = count
                primary_language = language

        # Create language identification result
        language_id_result = {
            "primary_language": primary_language,
            "language_stats": language_stats,
            "file_languages": file_languages,
        }

        # Store the result in the workspace
        language_id_key = f"language_id_{job_id}"
        agent.workspace.store_data(language_id_key, language_id_result)

        # Return success
        return {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "language_id_key": language_id_key,
            "primary_language": primary_language,
            "language_stats": language_stats,
            "status": "success",
            "message": f"Identified languages for {len(file_languages)} files",
        }
    else:
        return {"status": "error", "message": f"Unsupported task type: {task_type}"}


def _identify_file_language(
    file_path: str, content: str, language_patterns: Dict[str, List[str]]
) -> Optional[str]:
    """Identify the programming language of a file based on its path and content"""
    # First check file extension
    for language, patterns in language_patterns.items():
        for pattern in patterns:
            if pattern.startswith(r"\.") and re.search(
                pattern, file_path, re.IGNORECASE
            ):
                return language

    # If extension check didn't work, check content patterns
    language_scores = {}
    for language, patterns in language_patterns.items():
        score = 0
        for pattern in patterns:
            if not pattern.startswith(r"\."):  # Skip extension patterns
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    score += 1
        if score > 0:
            language_scores[language] = score

    # Return the language with the highest score
    if language_scores:
        return max(language_scores.items(), key=lambda x: x[1])[0]

    # If no language identified, return None
    return None
