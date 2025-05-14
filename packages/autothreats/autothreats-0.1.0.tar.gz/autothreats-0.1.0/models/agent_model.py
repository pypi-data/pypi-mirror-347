#!/usr/bin/env python3
"""
Agent model module for the autonomous threat modeling system.
"""

import json
import time
from typing import Any, Dict, List, Mapping, Optional, Set


class AgentModel:
    """Data model for agent state and configuration"""

    def __init__(
        self, agent_id: str, agent_type: str, config: Optional[Mapping[str, Any]] = None
    ):
        self.id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        self.state: Mapping[str, Any] = {}
        self.connections: Mapping[str, dict[str, Any]] = (
            {}
        )  # Direct agent connections for A2A communication
        self.default_config: Mapping[str, Any] = {}  # Default configuration values
        self.required_config: Set[str] = set()  # Required configuration keys
        self.optional_config: Set[str] = set()  # Optional configuration keys
        self.config_schema: Mapping[str, Any] = (
            {}
        )  # Schema for configuration validation
        self._required_config: Set[str] = set()  # Internal storage for required config
        self._optional_config: Set[str] = set()  # Internal storage for optional config

    def set_config_schema(
        self, required: Set[str], optional: Set[str], defaults: Dict[str, Any]
    ):
        """Set the configuration schema for this agent"""
        self.required_config = required
        self.optional_config = optional
        self.default_config = defaults
        self._required_config = (
            required  # Store in internal attribute for test compatibility
        )
        self._optional_config = (
            optional  # Store in internal attribute for test compatibility
        )

        # Apply defaults to current config
        for key, value in defaults.items():
            if key not in self.config:
                self.config[key] = value

    def validate_config(self) -> List[str]:
        """Validate the configuration against the schema"""
        errors = []

        # Check required keys
        for key in self.required_config:
            if key not in self.config:
                errors.append(f"Missing required configuration key: {key}")

        return errors

    def update_config(self, config_updates: Dict[str, Any]) -> List[str]:
        """Update configuration with new values and validate"""
        errors = []

        # Check for invalid fields
        for key in config_updates:
            if key not in self.required_config and key not in self.optional_config:
                errors.append(f"Invalid configuration field: {key}")
                # Don't add invalid fields to config
                continue

            # Update config with valid fields
            self.config[key] = config_updates[key]

        # Validate updated config
        validation_errors = self.validate_config()
        errors.extend(validation_errors)

        return errors

    def get_config(self, key: str, default=None) -> Any:
        """Get configuration value with fallback to default"""
        return self.config.get(key, default)

    def update_state(self, key: str, value: Any):
        """Update agent state"""
        self.state[key] = value

    def get_state(self, key: str, default=None) -> Any:
        """Get agent state"""
        return self.state.get(key, default)

    def add_connection(self, agent_id: str, connection_info: Dict[str, Any]):
        """Add direct connection to another agent"""
        self.connections[agent_id] = connection_info

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "agent_type": self.agent_type,
            "config": self.config,
            "state": self.state,
            "connections": self.connections,
            "config_schema": {
                "required": list(self.required_config),
                "optional": list(self.optional_config),
                "defaults": self.default_config,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentModel":
        """Create model from dictionary"""
        model = cls(data["id"], data["agent_type"], data.get("config", {}))
        model.state = data.get("state", {})
        model.connections = data.get("connections", {})

        # Restore schema if available
        schema = data.get("config_schema", {})
        if schema:
            model.required_config = set(schema.get("required", []))
            model.optional_config = set(schema.get("optional", []))
            model.default_config = schema.get("defaults", {})

        return model
