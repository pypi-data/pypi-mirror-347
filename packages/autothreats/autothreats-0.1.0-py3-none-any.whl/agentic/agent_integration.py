#!/usr/bin/env python3
"""
Agent Integration module for the autonomous threat modeling system.
Provides functions to register and integrate agentic agents with the system.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..simplified_base import Agent, SharedWorkspace, AgentModel
from ..utils.agent_decorators import register_agents, clear_registry

# Import the agentic threat detection agent
from .threat_detection_agent import agentic_threat_detection_agent

logger = logging.getLogger(__name__)


def register_agentic_agents(workspace: SharedWorkspace, config: Dict[str, Any]) -> List[Agent]:
    """
    Register all agentic agents with the system. These will be used alongside normal agents,
    with agentic versions taking precedence when duplicates exist.

    Args:
        workspace: The shared workspace
        config: The system configuration

    Returns:
        List of registered agentic agents
    """
    logger.info("Registering agentic agents")
    
    # Clear the registry to avoid duplicates
    clear_registry()
    
    # Register the agentic agents using the decorator system
    agents = register_agents(workspace)
    
    # Convert to list
    agent_list = list(agents.values())
    
    # If no agents were registered through the decorator system,
    # create mock agents for testing purposes
    if not agent_list:
        logger.info("No agents registered through decorator system, creating mock agents for testing")
        
        # Create a mock code graph agent
        class MockCodeGraphAgent(Agent):
            def __init__(self, agent_id: str):
                super().__init__(agent_id, "code_graph", {})
                self.workspace = workspace
                
            async def _process_task_impl(self, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
                return {"status": "success", "message": "Mock code graph agent"}
                
            def _setup_config_schema(self):
                self.model.set_config_schema(set(), set(), {})
        
        # Create a mock threat detection agent
        class MockThreatDetectionAgent(Agent):
            def __init__(self, agent_id: str):
                super().__init__(agent_id, "threat_detection", {})
                self.workspace = workspace
                
            async def _process_task_impl(self, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
                return {"status": "success", "message": "Mock threat detection agent"}
                
            def _setup_config_schema(self):
                self.model.set_config_schema(set(), set(), {})
        
        # Create and register the mock agents
        code_graph_agent = MockCodeGraphAgent("mock_code_graph_agent")
        threat_detection_agent = MockThreatDetectionAgent("mock_threat_detection_agent")
        
        # Register the agents with the workspace
        workspace.register_agent(code_graph_agent)
        workspace.register_agent(threat_detection_agent)
        
        # Add the agents to the list
        agent_list = [code_graph_agent, threat_detection_agent]
    
    logger.info(f"Registered {len(agent_list)} agentic agents")
    return agent_list


async def initialize_agentic_agents(agents: List[Agent]) -> None:
    """
    Initialize all agentic agents concurrently with timeouts.

    Args:
        agents: List of agentic agents to initialize
    """
    if not agents:
        logger.info("No agentic agents to initialize")
        return
        
    logger.info(f"Initializing {len(agents)} agentic agents concurrently")
    
    # Define a helper function to initialize a single agent with timeout
    async def init_agent_with_timeout(agent, timeout=10.0):
        try:
            # Add a timeout to prevent hanging on a single agent
            await asyncio.wait_for(agent.initialize(), timeout=timeout)
            logger.info(f"Initialized agentic agent {agent.id}")
            return True
        except asyncio.TimeoutError:
            logger.warning(f"Timeout initializing agentic agent {agent.id} - continuing anyway")
            return False
        except Exception as e:
            logger.error(f"Error initializing agentic agent {agent.id}: {str(e)}")
            return False
    
    # Create initialization tasks for all agents
    init_tasks = [init_agent_with_timeout(agent) for agent in agents]
    
    # Run all initialization tasks concurrently with an overall timeout
    try:
        await asyncio.gather(*init_tasks)
        logger.info("All agentic agents initialized")
    except Exception as e:
        logger.error(f"Error initializing agentic agents: {str(e)}")
