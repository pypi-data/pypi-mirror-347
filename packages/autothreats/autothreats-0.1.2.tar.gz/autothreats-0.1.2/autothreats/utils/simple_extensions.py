#!/usr/bin/env python3
"""
Simplified extension API for Threat Canvas.
This module provides a single, simple API for loading and using extension agents.
"""

import importlib
import importlib.util
import inspect
import logging
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Type, Union

from ..simplified_base import Agent, SharedWorkspace
from .agent_api import create_and_register_simple_agent, register_all_agents

logger = logging.getLogger(__name__)


async def load_and_run_extensions(
    workspace: SharedWorkspace,
    extension_dirs: List[str],
    task_type: str,
    task_data: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """
    Load extensions, run them with the specified task, and return the results.
    This is a single, simple API that handles everything in one step.

    Parameters:
        workspace: The shared workspace
        extension_dirs: List of directories to search for extensions
        task_type: Type of task to run
        task_data: Data for the task

    Returns:
        Dictionary mapping agent IDs to their results

    Example:
        ```python
        # Create a workspace
        workspace = SharedWorkspace("my_workspace")
        await workspace.start()

        # Load and run extensions
        results = await load_and_run_extensions(
            workspace=workspace,
            extension_dirs=["/path/to/extensions"],
            task_type="analyze_code",
            task_data={"codebase_id": "my_codebase"}
        )

        # Print the results
        for agent_id, result in results.items():
            print(f"Result from {agent_id}: {result}")
        ```
    """
    # Discover and load extensions
    extensions = _discover_extensions(extension_dirs)
    agents = _load_extensions(workspace, extensions)

    # Initialize agents
    for agent in agents.values():
        await agent.initialize()

    # Run the task on each agent
    results = {}
    for agent_id, agent in agents.items():
        try:
            result = await workspace.process_agent_task(
                agent_id=agent_id, task_type=task_type, task_data=task_data
            )
            results[agent_id] = result
        except Exception as e:
            logger.error(f"Error running task on agent {agent_id}: {str(e)}")
            results[agent_id] = {"status": "error", "message": str(e)}

    # Shutdown agents
    for agent in agents.values():
        await agent.shutdown()

    return results


def _discover_extensions(extension_dirs: List[str]) -> Dict[str, str]:
    """
    Discover extension modules in the specified directories.

    Parameters:
        extension_dirs: List of directories to search for extensions

    Returns:
        Dictionary mapping extension names to their file paths
    """
    discovered = {}

    for extension_dir in extension_dirs:
        if not os.path.exists(extension_dir):
            logger.warning(f"Extension directory does not exist: {extension_dir}")
            continue

        logger.info(f"Searching for extensions in: {extension_dir}")

        for filename in os.listdir(extension_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]  # Remove .py extension
                module_path = os.path.join(extension_dir, filename)
                discovered[module_name] = module_path
                logger.info(f"Discovered extension: {module_name} at {module_path}")

    return discovered


def _load_extensions(
    workspace: SharedWorkspace, extensions: Dict[str, str]
) -> Dict[str, Agent]:
    """
    Load extensions and register their agents.

    Parameters:
        workspace: The shared workspace
        extensions: Dictionary mapping extension names to their file paths

    Returns:
        Dictionary of registered agents
    """
    agents = {}

    for name, path in extensions.items():
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None:
                logger.error(f"Could not create spec for extension: {name}")
                continue

            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)

            # Register agents from the module
            module_agents = _register_agents_from_module(workspace, module)
            agents.update(module_agents)

            logger.info(f"Loaded extension {name} with {len(module_agents)} agents")
        except Exception as e:
            logger.error(f"Error loading extension {name}: {str(e)}")

    return agents


def _register_agents_from_module(
    workspace: SharedWorkspace, module: Any
) -> Dict[str, Agent]:
    """
    Register agents from a module.

    Parameters:
        workspace: The shared workspace
        module: The module to register agents from

    Returns:
        Dictionary of registered agents
    """
    # Check if the module has a register_agents function
    if hasattr(module, "register_agents"):
        try:
            return module.register_agents(workspace)
        except Exception as e:
            logger.error(f"Error calling register_agents: {str(e)}")

    # Check if the module has agent factory functions
    agent_factories = {}
    for name, obj in inspect.getmembers(module):
        if name.startswith("create_") and inspect.isfunction(obj):
            agent_id = name[7:]  # Remove 'create_' prefix
            agent_factories[agent_id] = obj

    if agent_factories:
        try:
            return register_all_agents(workspace, agent_factories)
        except Exception as e:
            logger.error(f"Error registering agents: {str(e)}")

    return {}
