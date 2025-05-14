#!/usr/bin/env python3
"""
Extension loader for Threat Canvas.
This module provides functionality to discover, load, and register Python extension agents.
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

class ExtensionManager:
    """
    Manager for Threat Canvas extensions.
    Discovers, loads, and registers extension agents.
    """
    
    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the extension manager.
        
        Parameters:
            workspace: The shared workspace to register agents with
        """
        self.workspace = workspace
        self.extensions = {}
        self.registered_agents = {}
    
    def discover_extensions(self, extension_dirs: List[str]) -> Dict[str, str]:
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
                if filename.endswith('.py') and not filename.startswith('_'):
                    module_name = filename[:-3]  # Remove .py extension
                    module_path = os.path.join(extension_dir, filename)
                    discovered[module_name] = module_path
                    logger.info(f"Discovered extension: {module_name} at {module_path}")
        
        return discovered
    
    def load_extension(self, name: str, path: str) -> Optional[Any]:
        """
        Load an extension module from a file path.
        
        Parameters:
            name: Name of the extension
            path: File path to the extension module
            
        Returns:
            The loaded module, or None if loading failed
        """
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None:
                logger.error(f"Could not create spec for extension: {name}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            
            self.extensions[name] = module
            logger.info(f"Loaded extension: {name}")
            return module
        except Exception as e:
            logger.error(f"Error loading extension {name}: {str(e)}")
            return None
    
    def register_extension_agents(self, module: Any) -> Dict[str, Agent]:
        """
        Register agents from an extension module.
        
        Parameters:
            module: The extension module
            
        Returns:
            Dictionary of registered agents
        """
        # Check if the module has a register_agents function
        if hasattr(module, 'register_agents'):
            try:
                # Call the register_agents function with the workspace
                agents = module.register_agents(self.workspace)
                
                # Store the registered agents
                for agent_id, agent in agents.items():
                    self.registered_agents[agent_id] = agent
                
                logger.info(f"Registered {len(agents)} agents from extension")
                return agents
            except Exception as e:
                logger.error(f"Error registering agents from extension: {str(e)}")
                return {}
        
        # Check if the module has agent factory functions
        agent_factories = {}
        for name, obj in inspect.getmembers(module):
            if name.startswith('create_') and inspect.isfunction(obj):
                agent_id = name[7:]  # Remove 'create_' prefix
                agent_factories[agent_id] = obj
        
        if agent_factories:
            try:
                # Register all agents using the factory functions
                agents = register_all_agents(
                    workspace=self.workspace,
                    agent_factories=agent_factories
                )
                
                # Store the registered agents
                for agent_id, agent in agents.items():
                    self.registered_agents[agent_id] = agent
                
                logger.info(f"Registered {len(agents)} agents from extension")
                return agents
            except Exception as e:
                logger.error(f"Error registering agents from extension: {str(e)}")
                return {}
        
        logger.warning("No agents found in extension")
        return {}
    
    def load_and_register_extensions(self, extension_dirs: List[str]) -> Dict[str, Dict[str, Agent]]:
        """
        Discover, load, and register all extensions in the specified directories.
        
        Parameters:
            extension_dirs: List of directories to search for extensions
            
        Returns:
            Dictionary mapping extension names to their registered agents
        """
        result = {}
        
        # Discover extensions
        discovered = self.discover_extensions(extension_dirs)
        
        # Load and register each extension
        for name, path in discovered.items():
            module = self.load_extension(name, path)
            if module:
                agents = self.register_extension_agents(module)
                if agents:
                    result[name] = agents
        
        return result
    
    async def initialize_all_agents(self) -> None:
        """
        Initialize all registered agents.
        """
        for agent_id, agent in self.registered_agents.items():
            try:
                await agent.initialize()
                logger.info(f"Initialized agent: {agent_id}")
            except Exception as e:
                logger.error(f"Error initializing agent {agent_id}: {str(e)}")
    
    async def shutdown_all_agents(self) -> None:
        """
        Shutdown all registered agents.
        """
        for agent_id, agent in self.registered_agents.items():
            try:
                await agent.shutdown()
                logger.info(f"Shut down agent: {agent_id}")
            except Exception as e:
                logger.error(f"Error shutting down agent {agent_id}: {str(e)}")

def load_extensions(workspace: SharedWorkspace, extension_dirs: List[str]) -> ExtensionManager:
    """
    Load and register extensions from the specified directories.
    
    Parameters:
        workspace: The shared workspace to register agents with
        extension_dirs: List of directories to search for extensions
        
    Returns:
        The extension manager with loaded extensions
    """
    manager = ExtensionManager(workspace)
    manager.load_and_register_extensions(extension_dirs)
    return manager