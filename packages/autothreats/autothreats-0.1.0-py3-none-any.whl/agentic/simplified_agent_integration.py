#!/usr/bin/env python3
"""
Simplified Agent Integration module for the autonomous threat modeling system.
Provides functions to register and integrate simplified agents with the system.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..agents.simplified_threat_detection import SimplifiedThreatDetectionAgent
from ..simplified_base import Agent, SharedWorkspace

logger = logging.getLogger(__name__)


def register_simplified_agents(workspace: SharedWorkspace, config: Dict[str, Any]) -> List[Agent]:
    """
    Register all simplified agents with the system.

    Args:
        workspace: The shared workspace
        config: The system configuration

    Returns:
        List of registered simplified agents
    """
    logger.info("Registering simplified agents")

    # Check if agentic improvements are enabled
    enable_agentic = config.get("enable_agentic_improvements", False) or config.get(
        "system", {}
    ).get("enable_agentic_improvements", False)

    if not enable_agentic:
        logger.info("Agentic improvements are disabled, skipping simplified agent registration")
        return []

    agents = []

    # Register simplified threat detection agent
    try:
        threat_detection_agent = SimplifiedThreatDetectionAgent(
            agent_id="simplified_threat_detection",
            config=config.get("agents", {}).get("threat_detection", {}),
        )
        # Set workspace directly on the agent
        threat_detection_agent.workspace = workspace
        agents.append(threat_detection_agent)
        logger.info("Registered simplified threat detection agent")
    except Exception as e:
        logger.error(f"Error registering simplified threat detection agent: {str(e)}")

    # Multi-stage agent has been removed

    # Add more simplified agents here as they are implemented

    logger.info(f"Registered {len(agents)} simplified agents")
    return agents


async def initialize_simplified_agents(agents: List[Agent]) -> None:
    """
    Initialize all simplified agents concurrently with timeouts.

    Args:
        agents: List of simplified agents to initialize
    """
    logger.info(f"Initializing {len(agents)} simplified agents concurrently")
    
    # Define a helper function to initialize a single agent with timeout
    async def init_agent_with_timeout(agent, timeout=10.0):
        try:
            # Add a timeout to prevent hanging on a single agent
            await asyncio.wait_for(agent.initialize(), timeout=timeout)
            logger.info(f"Initialized simplified agent {agent.id}")
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Timeout initializing simplified agent {agent.id} - continuing anyway")
            return False
        except Exception as e:
            logger.error(f"Error initializing simplified agent {agent.id}: {str(e)}")
            return False
    
    # Create initialization tasks for all agents
    init_tasks = [init_agent_with_timeout(agent) for agent in agents]
    
    # Run all initialization tasks concurrently with an overall timeout
    try:
        results = await asyncio.wait_for(asyncio.gather(*init_tasks, return_exceptions=True),
                                         timeout=30.0)
        success_count = sum(1 for r in results if r is True)
        logger.info(f"Successfully initialized {success_count} out of {len(agents)} simplified agents")
    except asyncio.TimeoutError:
        logger.warning(f"Overall timeout while initializing simplified agents - continuing with system operation")
    except Exception as e:
        logger.error(f"Unexpected error during simplified agent initialization: {e}")


async def shutdown_simplified_agents(agents: List[Agent]) -> None:
    """
    Shut down all simplified agents concurrently with timeouts.

    Args:
        agents: List of simplified agents to shut down
    """
    logger.info(f"Shutting down {len(agents)} simplified agents concurrently")
    
    # Define a helper function to shut down a single agent with timeout
    async def shutdown_agent_with_timeout(agent, timeout=5.0):
        try:
            # Add a timeout to prevent hanging on a single agent
            await asyncio.wait_for(agent.shutdown(), timeout=timeout)
            logger.info(f"Shut down simplified agent {agent.id}")
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Timeout shutting down simplified agent {agent.id} - continuing anyway")
            return False
        except Exception as e:
            logger.error(f"Error shutting down simplified agent {agent.id}: {str(e)}")
            return False
    
    # Create shutdown tasks for all agents
    shutdown_tasks = [shutdown_agent_with_timeout(agent) for agent in agents]
    
    # Run all shutdown tasks concurrently with an overall timeout
    try:
        results = await asyncio.wait_for(asyncio.gather(*shutdown_tasks, return_exceptions=True),
                                         timeout=15.0)
        success_count = sum(1 for r in results if r is True)
        logger.info(f"Successfully shut down {success_count} out of {len(agents)} simplified agents")
    except asyncio.TimeoutError:
        logger.warning(f"Overall timeout while shutting down simplified agents - continuing anyway")
    except Exception as e:
        logger.error(f"Unexpected error during simplified agent shutdown: {e}")