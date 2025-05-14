#!/usr/bin/env python3
"""
Decorator-based API for adding agents to Threat Canvas.
This module provides simple decorators for creating agents with minimal code.
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from ..simplified_base import (Agent, AgentController, AgentModel,
                               SharedWorkspace)

logger = logging.getLogger(__name__)

# Global registry for decorated agents
_agent_registry = {}

def agent(agent_id: str = None, agent_type: str = None,
          config: Dict[str, Any] = None, is_agentic: bool = False):
    """
    Decorator to create an agent from a function.
    This is the simplest way to create an agent - just decorate a function!
    
    Parameters:
        agent_id: Unique identifier for this agent (defaults to function name)
        agent_type: Type of agent (defaults to function name)
        config: Configuration dictionary for the agent
        is_agentic: Whether this is an agentic version of an agent
        
    Example:
        ```python
        @agent(agent_type="security_scanner", is_agentic=True)
        async def security_scanner(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success", "message": "Security scan completed"}
        ```
    """
    def decorator(func):
        # Validate that the function is async
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Agent function must be async (use 'async def')")
        
        # Validate the function signature
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        if len(params) < 3 or params[0] != 'agent' or params[1] != 'task_type' or params[2] != 'task_data':
            raise TypeError("Agent function must have signature: async def func(agent, task_type, task_data)")
        
        # Get function name for defaults
        func_name = func.__name__
        
        # Use function name as defaults if not provided
        nonlocal agent_id, agent_type
        if agent_id is None:
            agent_id = func_name
        if agent_type is None:
            agent_type = func_name
            
        # Add agentic prefix if needed
        if is_agentic and not agent_type.startswith('agentic_'):
            agent_type = f"agentic_{agent_type}"
            
        # Store the function in the registry
        _agent_registry[agent_id] = {
            "func": func,
            "agent_type": agent_type,
            "config": config or {},
            "is_agentic": is_agentic
        }
        
        # Return the original function unchanged
        return func
    
    return decorator

def register_agents(workspace: SharedWorkspace) -> Dict[str, Agent]:
    """
    Register all decorated agents with a workspace.
    
    Parameters:
        workspace: The shared workspace
        
    Returns:
        Dictionary of registered agents
        
    Example:
        ```python
        # Define agents using decorators
        @agent(agent_type="security_scanner")
        async def security_scanner(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success"}
            
        @agent(agent_type="code_analyzer")
        async def code_analyzer(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success"}
            
        # Register all agents with the workspace
        agents = register_agents(workspace)
        ```
    """
    if workspace is None:
        raise ValueError("Workspace cannot be None")
        
    agents = {}
    
    for agent_id, agent_info in _agent_registry.items():
        try:
            # Create a simple agent class dynamically
            class SimpleAgent(Agent):
                def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
                    super().__init__(agent_id, agent_info["agent_type"], config)
                    
                def _setup_config_schema(self):
                    """Set up configuration schema for this agent"""
                    # Simple default schema
                    self.model.set_config_schema(set(), set(), {})
                    
                async def _process_task_impl(self, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
                    """Process a task by delegating to the decorated function"""
                    return await agent_info["func"](self, task_type, task_data)
                    
                async def shutdown(self):
                    """Clean up resources when shutting down"""
                    self.logger.info(f"Shutting down {self.id}")
                    self.model.update_state("status", "shutdown")
            
            # Create and register the agent
            agent = SimpleAgent(agent_id=agent_id, config=agent_info["config"])
            agent.workspace = workspace
            workspace.register_agent(agent)
            
            # Store in the result dictionary
            agents[agent_id] = agent
            
            logger.info(f"Registered agent {agent_id}")
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {str(e)}")
    
    return agents

def clear_registry():
    """Clear the agent registry"""
    global _agent_registry
    _agent_registry = {}