#!/usr/bin/env python3
"""
Simple API for adding new agents to Threat Canvas.
This module provides a simplified interface for creating and registering agents.

This API provides multiple simple functions for different agent creation patterns:
1. create_simple_agent: Create an agent from just a task processing function
2. register_agent: Register an existing agent with a workspace
3. create_from_class: Create an agent from a custom Agent class
4. wrap_existing_agent: Wrap an existing agent implementation
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from ..agentic.agent_integration import register_agentic_agents
from ..simplified_base import (Agent, AgentController, AgentModel,
                               SharedWorkspace)

logger = logging.getLogger(__name__)

def create_simple_agent(
    agent_id: str,
    process_task_func: Callable,
    agent_type: str = "custom",
    config: Optional[Dict[str, Any]] = None,
    required_config: Optional[List[str]] = None,
    optional_config: Optional[List[str]] = None,
    default_config: Optional[Dict[str, Any]] = None,
    is_agentic: bool = False
) -> Agent:
    """
    Create a new agent with just a task processing function.
    This is the simplest way to create an agent.
    
    Parameters:
        agent_id: Unique identifier for this agent instance
        process_task_func: Function that implements the agent's task processing logic
                          Should have signature: async def func(agent, task_type, task_data) -> Dict
        agent_type: Type of agent (e.g., "code_analysis", "vulnerability_detection")
        config: Configuration dictionary for the agent
        required_config: List of required configuration keys
        optional_config: List of optional configuration keys
        default_config: Dictionary of default configuration values
        is_agentic: Whether this is an agentic version of an agent
        
    Returns:
        A configured Agent instance
    
    Example:
        ```python
        async def process_task(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success", "message": "Task completed"}
            
        agent = create_simple_agent(
            agent_id="my_agent",
            process_task_func=process_task,
            agent_type="custom_analysis"
        )
        ```
    """
    # Validate that the function is async
    if not inspect.iscoroutinefunction(process_task_func):
        raise TypeError("Agent function must be async (use 'async def')")
    
    # Validate the function signature
    sig = inspect.signature(process_task_func)
    params = list(sig.parameters.keys())
    if len(params) < 3 or params[0] != 'agent' or params[1] != 'task_type' or params[2] != 'task_data':
        raise TypeError("Agent function must have signature: async def func(agent, task_type, task_data)")
    
    # Create a simple agent class dynamically
    class SimpleAgent(Agent):
        def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
            prefix = "agentic_" if is_agentic else ""
            super().__init__(agent_id, f"{prefix}{agent_type}", config)
            
        def _setup_config_schema(self):
            """Set up configuration schema for this agent"""
            # Set up configuration schema
            req_config = set(required_config or [])
            opt_config = set(optional_config or [])
            def_config = default_config or {}
            
            # Apply schema to model
            self.model.set_config_schema(req_config, opt_config, def_config)
            
        async def _process_task_impl(self, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
            """Process a task by delegating to the provided function"""
            return await process_task_func(self, task_type, task_data)
            
        async def shutdown(self):
            """Clean up resources when shutting down"""
            self.logger.info(f"Shutting down {self.id}")
            self.model.update_state("status", "shutdown")
    
    # Create and return an instance of the agent
    return SimpleAgent(agent_id=agent_id, config=config)

def register_agent(
    workspace: SharedWorkspace,
    agent: Agent
) -> Agent:
    """
    Register an agent with a workspace.
    
    Parameters:
        workspace: The shared workspace
        agent: The agent to register
        
    Returns:
        The registered agent (for chaining)
    
    Example:
        ```python
        agent = create_simple_agent(...)
        register_agent(workspace, agent)
        ```
    """
    # Validate parameters
    if workspace is None:
        raise ValueError("Workspace cannot be None")
    if agent is None:
        raise ValueError("Agent cannot be None")
    
    # Register the agent with the workspace
    agent.workspace = workspace
    workspace.register_agent(agent)
    logger.info(f"Registered agent {agent.id} with workspace")
    return agent

def create_from_class(
    agent_class: Type[Agent],
    agent_id: str,
    config: Optional[Dict[str, Any]] = None,
    agent_type: Optional[str] = None,
    workspace: Optional[SharedWorkspace] = None,
    is_agentic: bool = False
) -> Agent:
    """
    Create an agent from a custom Agent class.
    
    Parameters:
        agent_class: The Agent class to instantiate
        agent_id: Unique identifier for this agent instance
        config: Configuration dictionary for the agent
        agent_type: Type of agent (defaults to class name if not provided)
        workspace: Optional workspace to register with
        is_agentic: Whether this is an agentic version of an agent
        
    Returns:
        An initialized Agent instance
    
    Example:
        ```python
        class MyCustomAgent(Agent):
            # Custom agent implementation
            pass
            
        agent = create_from_class(
            agent_class=MyCustomAgent,
            agent_id="custom_agent",
            config={"timeout": 30}
        )
        ```
    """
    # Validate the agent class
    if not inspect.isclass(agent_class) or not issubclass(agent_class, Agent):
        raise TypeError("Agent class must extend Agent")
    
    # If agent_type not provided, use the class name
    if agent_type is None:
        agent_type = agent_class.__name__.lower()
        if agent_type.endswith('agent'):
            agent_type = agent_type[:-5]  # Remove 'agent' suffix
    
    # Add agentic prefix if needed
    if is_agentic and not agent_type.startswith('agentic_'):
        agent_type = f"agentic_{agent_type}"
    
    # Check if the agent class constructor accepts the expected parameters
    sig = inspect.signature(agent_class.__init__)
    params = list(sig.parameters.keys())
    
    # Create the agent instance
    try:
        if len(params) >= 3 and params[1] == 'agent_id' and params[2] == 'agent_type':
            # Constructor matches Agent(self, agent_id, agent_type, config)
            agent = agent_class(agent_id=agent_id, agent_type=agent_type, config=config)
        elif len(params) >= 2 and params[1] == 'agent_id':
            # Constructor matches Agent(self, agent_id, config)
            agent = agent_class(agent_id=agent_id, config=config)
        else:
            # Try a generic approach
            agent = agent_class(agent_id, config)
    except TypeError as e:
        # Re-raise with more helpful message
        if "Can't instantiate abstract class" in str(e):
            raise TypeError(f"Can't instantiate abstract class {agent_class.__name__}. Implement all abstract methods.")
        raise
    
    # Register with workspace if provided
    if workspace is not None:
        register_agent(workspace, agent)
    
    return agent

def wrap_existing_agent(
    agent: Agent,
    process_task_func: Optional[Callable] = None,
    controller_class: Optional[Type[AgentController]] = None,
    workspace: Optional[SharedWorkspace] = None
) -> Agent:
    """
    Wrap an existing agent implementation with custom behavior.
    
    Parameters:
        agent: The existing agent to wrap
        process_task_func: Optional function to override the agent's task processing
        controller_class: Optional custom controller class
        workspace: Optional workspace to register with
        
    Returns:
        The wrapped agent
    
    Example:
        ```python
        # Wrap an existing agent with custom task processing
        async def custom_processing(agent, task_type, task_data):
            # Custom processing logic
            return {"status": "success"}
            
        wrapped_agent = wrap_existing_agent(
            agent=existing_agent,
            process_task_func=custom_processing
        )
        ```
    """
    # Validate parameters
    if agent is None:
        raise ValueError("Agent cannot be None")
    
    # Validate process_task_func if provided
    if process_task_func is not None:
        if not inspect.iscoroutinefunction(process_task_func):
            raise TypeError("Agent function must be async (use 'async def')")
        
        sig = inspect.signature(process_task_func)
        params = list(sig.parameters.keys())
        if len(params) < 3 or params[0] != 'agent' or params[1] != 'task_type' or params[2] != 'task_data':
            raise TypeError("Agent function must have signature: async def func(agent, task_type, task_data)")
        
        # Override the process_task_impl method
        async def process_task_override(self, task_type, task_data):
            return await process_task_func(self, task_type, task_data)
        
        agent._process_task_impl = process_task_override.__get__(agent)
    
    # Validate controller_class if provided
    if controller_class is not None:
        if not inspect.isclass(controller_class) or not issubclass(controller_class, AgentController):
            raise TypeError("Controller class must extend AgentController")
        
        # Override the controller if the agent supports it
        if hasattr(agent, '_create_controller'):
            def create_controller_override(self):
                return controller_class(self.model)
            
            agent._create_controller = create_controller_override.__get__(agent)
        else:
            logger.warning(f"Agent {agent.id} does not support custom controllers")
    
    # Register with workspace if provided
    if workspace is not None:
        register_agent(workspace, agent)
    
    return agent

def create_and_register_agent(
    workspace: SharedWorkspace,
    agent_id: str,
    process_task_func: Callable,
    agent_type: str = "custom",
    config: Optional[Dict[str, Any]] = None,
    required_config: Optional[List[str]] = None,
    optional_config: Optional[List[str]] = None,
    default_config: Optional[Dict[str, Any]] = None,
    is_agentic: bool = False
) -> Agent:
    """
    Create a new agent and register it with the workspace in one step.
    
    Parameters:
        workspace: The shared workspace
        agent_id: Unique identifier for this agent instance
        process_task_func: Function that implements the agent's task processing logic
        agent_type: Type of agent (e.g., "code_analysis", "vulnerability_detection")
        config: Configuration dictionary for the agent
        required_config: List of required configuration keys
        optional_config: List of optional configuration keys
        default_config: Dictionary of default configuration values
        is_agentic: Whether this is an agentic version of an agent
        
    Returns:
        The registered Agent instance
    
    Example:
        ```python
        async def process_task(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success"}
            
        agent = create_and_register_agent(
            workspace=workspace,
            agent_id="my_agent",
            process_task_func=process_task
        )
        ```
    """
    # Create the agent
    agent = create_simple_agent(
        agent_id=agent_id,
        process_task_func=process_task_func,
        agent_type=agent_type,
        config=config,
        required_config=required_config,
        optional_config=optional_config,
        default_config=default_config,
        is_agentic=is_agentic
    )
    
    # Register with workspace
    return register_agent(workspace, agent)

def create_and_register_simple_agent(
    workspace: SharedWorkspace,
    agent_id: str,
    agent_type: str,
    process_task_func: Callable,
    config: Optional[Dict[str, Any]] = None,
    optional_config: Optional[List[str]] = None,
    default_config: Optional[Dict[str, Any]] = None,
    is_agentic: bool = False
) -> Agent:
    """
    Create and register a simple agent with a workspace in one step.
    This is the simplest way to create and register an agent.
    
    Parameters:
        workspace: The shared workspace
        agent_id: Unique identifier for this agent instance
        agent_type: Type of agent (e.g., "code_analysis", "vulnerability_detection")
        process_task_func: Function that implements the agent's task processing logic
                          Should have signature: async def func(agent, task_type, task_data) -> Dict
        config: Configuration dictionary for the agent
        optional_config: List of optional configuration keys
        default_config: Dictionary of default configuration values
        is_agentic: Whether this is an agentic version of an agent
        
    Returns:
        The registered agent
    
    Example:
        ```python
        async def process_task(agent, task_type, task_data):
            # Process task and return result
            return {"status": "success", "message": "Task completed"}
            
        agent = create_and_register_simple_agent(
            workspace=workspace,
            agent_id="my_agent",
            agent_type="custom_analysis",
            process_task_func=process_task
        )
        ```
    """
    # Create the agent
    agent = create_simple_agent(
        agent_id=agent_id,
        process_task_func=process_task_func,
        agent_type=agent_type,
        config=config,
        optional_config=optional_config,
        default_config=default_config,
        is_agentic=is_agentic
    )
    
    # Register with workspace
    return register_agent(workspace, agent)

def register_all_agents(
    workspace: SharedWorkspace,
    agent_factories: Dict[str, Callable[[SharedWorkspace], Agent]]
) -> Dict[str, Agent]:
    """
    Register multiple agents with a workspace using factory functions.
    
    Parameters:
        workspace: The shared workspace
        agent_factories: Dictionary mapping agent_id to factory functions
        
    Returns:
        Dictionary of registered agents
    
    Example:
        ```python
        # Define factory functions for your agents
        def create_agent1(workspace):
            return create_and_register_simple_agent(
                workspace=workspace,
                agent_id="agent1",
                agent_type="type1",
                process_task_func=process_task1
            )

        def create_agent2(workspace):
            return create_and_register_simple_agent(
                workspace=workspace,
                agent_id="agent2",
                agent_type="type2",
                process_task_func=process_task2
            )

        # Register all agents
        agents = register_all_agents(
            workspace=workspace,
            agent_factories={
                "agent1": create_agent1,
                "agent2": create_agent2
            }
        )

        # Access the registered agents
        agent1 = agents["agent1"]
        agent2 = agents["agent2"]
        ```
    """
    # Validate parameters
    if workspace is None:
        raise ValueError("Workspace cannot be None")
    if not agent_factories:
        logger.warning("No agent factories provided")
        return {}
    
    agents = {}
    
    for agent_id, factory_func in agent_factories.items():
        try:
            # Create and register the agent
            agent = factory_func(workspace)
            
            # Store in the result dictionary
            agents[agent_id] = agent
            
            logger.info(f"Registered agent {agent_id}")
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {str(e)}")
    
    return agents

# Alias for register_all_agents for backward compatibility
register_multiple_agents = register_all_agents

def register_with_orchestrator(
    orchestrator_module_path: str,
    agent_class: Type[Agent],
    agent_type: str,
    config_section: Optional[str] = None
) -> None:
    """
    Register an agent with the orchestrator by modifying the orchestrator module.
    This is a convenience function that adds the necessary import and registration code.
    
    Parameters:
        orchestrator_module_path: Path to the orchestrator module
        agent_class: The agent class to register
        agent_type: Type of the agent
        config_section: Name of the configuration section (defaults to agent_type)
    
    Example:
        ```python
        register_with_orchestrator(
            orchestrator_module_path="autothreats.simplified_orchestrator",
            agent_class=MyCustomAgent,
            agent_type="custom_analysis"
        )
        ```
    """
    import importlib.util

    # Get the module and class name
    module_name = agent_class.__module__
    class_name = agent_class.__name__
    
    # Use the agent_type as the config section if not provided
    if config_section is None:
        config_section = agent_type
    
    # Import the orchestrator module
    try:
        spec = importlib.util.find_spec(orchestrator_module_path)
        if spec is None:
            logger.error(f"Could not find orchestrator module: {orchestrator_module_path}")
            return
            
        orchestrator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(orchestrator_module)
        
        # Check if the agent is already registered
        if hasattr(orchestrator_module, "_create_agents"):
            create_agents_func = getattr(orchestrator_module, "_create_agents")
            source = inspect.getsource(create_agents_func)
            
            if class_name in source:
                logger.info(f"Agent {class_name} is already registered with the orchestrator")
                return
        
        # The agent needs to be registered
        logger.info(f"Agent {class_name} needs to be registered with the orchestrator")
        logger.info("Please add the following code to the orchestrator's _create_agents method:")
        
        import_code = f"from {module_name} import {class_name}"
        registration_code = f"""
        # Create and register {agent_type} agent
        {agent_type}_config = self.config.get("{config_section}", {{}})
        {agent_type}_agent = {class_name}(
            agent_id="{agent_type}",
            config={agent_type}_config
        )
        self.workspace.register_agent({agent_type}_agent)
        self.agents["{agent_type}"] = {agent_type}_agent
        self.logger.info("{agent_type} agent created")
        """
        
        logger.info(f"Import: {import_code}")
        logger.info(f"Registration: {registration_code}")
        
    except Exception as e:
        logger.error(f"Error registering agent with orchestrator: {str(e)}")