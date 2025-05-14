#!/usr/bin/env python3
"""
Simplified system additions for the autonomous threat modeling system.
Contains helper methods for the simplified orchestrator.
"""

from typing import Dict, List

from .simplified_base import Agent
from .simplified_workspace import Workspace


def register_agents(self):
    """Register agents with the workspace"""
    for agent_id, agent in self.agents.items():
        if self.workspace:
            self.workspace.register_agent(agent)
            self.logger.debug(f"Agent {agent_id} registered with workspace")
        else:
            self.logger.warning(
                f"Cannot register agent {agent_id}: workspace not initialized"
            )


def create_workspace(self, workspace_id: str = None):
    """Create a new workspace"""
    workspace_id = workspace_id or f"workspace_{self.id}"
    workspace = Workspace(workspace_id)
    return workspace


def create_specific_agents(self, agent_types: List[str]) -> Dict[str, Agent]:
    """Create specific agents based on agent types"""
    agents = {}
    for agent_type in agent_types:
        if agent_type in self.agent_classes:
            agent_id = f"{agent_type}_agent"
            agent_class = self.agent_classes[agent_type]
            agent = agent_class(agent_id, agent_type, self.config)
            agents[agent_id] = agent
            self.logger.debug(f"Created agent {agent_id} of type {agent_type}")
        else:
            self.logger.warning(f"Unknown agent type: {agent_type}")
    return agents
