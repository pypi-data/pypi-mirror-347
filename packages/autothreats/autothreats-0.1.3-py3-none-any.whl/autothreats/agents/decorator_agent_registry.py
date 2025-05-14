#!/usr/bin/env python3
"""
Registry for decorator-based agents in the autonomous threat modeling system.
This module imports and registers all decorator-based agents.
"""

import logging
from typing import Any, Dict

from ..simplified_base import Agent, SharedWorkspace
from ..utils.agent_decorators import register_agents
from .decorator_code_ingestion import code_ingestion
from .decorator_language_id import language_id
from .decorator_normalization import normalization
from .decorator_risk_scoring import risk_scoring

# Import all decorator-based agents
from .decorator_threat_detection import threat_detection

logger = logging.getLogger(__name__)


def register_all_decorator_agents(workspace: SharedWorkspace) -> Dict[str, Agent]:
    """
    Register all decorator-based agents with the workspace.

    Args:
        workspace: The shared workspace

    Returns:
        Dictionary of registered agents
    """
    logger.info("Registering all decorator-based agents")

    # Register all agents using the decorator registry
    agents = register_agents(workspace)

    logger.info(
        f"Registered {len(agents)} decorator-based agents: {', '.join(agents.keys())}"
    )

    return agents


async def initialize_all_agents(agents: Dict[str, Agent]) -> None:
    """
    Initialize all registered agents.

    Args:
        agents: Dictionary of agents to initialize
    """
    logger.info("Initializing all decorator-based agents")

    # Initialize each agent
    for agent_id, agent in agents.items():
        logger.info(f"Initializing agent: {agent_id}")
        await agent.initialize()

    logger.info(f"All {len(agents)} decorator-based agents initialized")


async def shutdown_all_agents(agents: Dict[str, Agent]) -> None:
    """
    Shutdown all registered agents.

    Args:
        agents: Dictionary of agents to shutdown
    """
    logger.info("Shutting down all decorator-based agents")

    # Shutdown each agent
    for agent_id, agent in agents.items():
        logger.info(f"Shutting down agent: {agent_id}")
        await agent.shutdown()

    logger.info(f"All {len(agents)} decorator-based agents shut down")
