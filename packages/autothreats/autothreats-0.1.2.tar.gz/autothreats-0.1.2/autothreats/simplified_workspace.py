#!/usr/bin/env python3
"""
Simplified workspace implementation for the autonomous threat modeling system.
Re-exports the SharedWorkspace class from simplified_base.py for easier imports.
"""

from .simplified_base import SharedWorkspace, WorkspaceModel

# Create an alias for SharedWorkspace as Workspace for backward compatibility
Workspace = SharedWorkspace
