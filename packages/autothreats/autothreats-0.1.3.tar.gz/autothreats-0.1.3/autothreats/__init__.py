"""
Autonomous Threat Modeling System

A system for automated threat modeling of codebases.
"""

# Import and expose types
from .message_types import MessageType

# Import and expose core classes
from .simplified_base import Agent, AgentModel, SharedWorkspace, WorkspaceModel

# Import and expose system modules
from .simplified_orchestrator import SimplifiedOrchestrator
from .simplified_workspace import Workspace

# Version information
__version__ = "0.1.2"
