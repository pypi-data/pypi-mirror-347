#!/usr/bin/env python3
"""
Tests for the simplified base components.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import (
    Agent,
    AgentModel,
    SharedWorkspace,
    WorkspaceModel,
)


class TestAgentModel(unittest.TestCase):
    """Test the AgentModel class"""

    def test_initialization(self):
        """Test initialization"""
        model = AgentModel("test_agent", "test_type", {"key": "value"})
        self.assertEqual(model.id, "test_agent")
        self.assertEqual(model.agent_type, "test_type")
        self.assertEqual(model.config, {"key": "value"})
        self.assertEqual(model.state, {})

    def test_set_config_schema(self):
        """Test setting config schema"""
        model = AgentModel("test_agent", "test_type")
        required_config = {"required_key"}
        optional_config = {"optional_key"}
        default_config = {"default_key": "default_value"}

        model.set_config_schema(required_config, optional_config, default_config)

        self.assertEqual(model.required_config, required_config)
        self.assertEqual(model.optional_config, optional_config)
        self.assertEqual(model.default_config, default_config)
        self.assertEqual(model.config["default_key"], "default_value")

    def test_validate_config(self):
        """Test validating config"""
        model = AgentModel("test_agent", "test_type", {"optional_key": "value"})
        model.set_config_schema({"required_key"}, {"optional_key"}, {})

        errors = model.validate_config()
        self.assertEqual(len(errors), 1)
        self.assertIn("required_key", errors[0])

        # Add the required key and validate again
        model.config["required_key"] = "value"
        errors = model.validate_config()
        self.assertEqual(len(errors), 0)

    def test_update_config(self):
        """Test updating config"""
        model = AgentModel("test_agent", "test_type", {"key1": "value1"})

        errors = model.update_config({"key2": "value2"})
        self.assertEqual(len(errors), 0)
        self.assertEqual(model.config["key1"], "value1")
        self.assertEqual(model.config["key2"], "value2")

    def test_update_state(self):
        """Test updating state"""
        model = AgentModel("test_agent", "test_type")

        model.update_state("key", "value")
        self.assertEqual(model.state["key"], "value")

        model.update_state("key", "new_value")
        self.assertEqual(model.state["key"], "new_value")

    def test_get_state(self):
        """Test getting state"""
        model = AgentModel("test_agent", "test_type")

        # Test with default
        self.assertEqual(model.get_state("key", "default"), "default")

        # Test with value
        model.update_state("key", "value")
        self.assertEqual(model.get_state("key", "default"), "value")

    def test_to_dict(self):
        """Test converting to dictionary"""
        model = AgentModel("test_agent", "test_type", {"key": "value"})
        model.update_state("state_key", "state_value")

        data = model.to_dict()
        self.assertEqual(data["id"], "test_agent")
        self.assertEqual(data["agent_type"], "test_type")
        self.assertEqual(data["config"], {"key": "value"})
        self.assertEqual(data["state"], {"state_key": "state_value"})

    def test_from_dict(self):
        """Test creating from dictionary"""
        data = {
            "id": "test_agent",
            "agent_type": "test_type",
            "config": {"key": "value"},
            "state": {"state_key": "state_value"},
        }

        model = AgentModel.from_dict(data)
        self.assertEqual(model.id, "test_agent")
        self.assertEqual(model.agent_type, "test_type")
        self.assertEqual(model.config, {"key": "value"})
        self.assertEqual(model.state, {"state_key": "state_value"})


class TestWorkspaceModel(unittest.TestCase):
    """Test the WorkspaceModel class"""

    def test_initialization(self):
        """Test initialization"""
        model = WorkspaceModel("test_workspace")
        self.assertEqual(model.id, "test_workspace")
        self.assertEqual(model.data_store, {})
        self.assertEqual(model.status, "initialized")
        self.assertEqual(model.metadata, {})
        self.assertIsNone(model.parent_workspace)

    def test_store_data(self):
        """Test storing data"""
        model = WorkspaceModel("test_workspace")

        model.store_data("key", "value")
        self.assertEqual(model.data_store["key"], "value")

        model.store_data("key", "new_value")
        self.assertEqual(model.data_store["key"], "new_value")

    def test_get_data(self):
        """Test getting data"""
        model = WorkspaceModel("test_workspace")

        # Test with default
        self.assertEqual(model.get_data("key", "default"), "default")

        # Test with value
        model.store_data("key", "value")
        self.assertEqual(model.get_data("key", "default"), "value")

    def test_update_status(self):
        """Test updating status"""
        model = WorkspaceModel("test_workspace")

        model.update_status("running")
        self.assertEqual(model.status, "running")

        model.update_status("stopped")
        self.assertEqual(model.status, "stopped")

    def test_set_metadata(self):
        """Test setting metadata"""
        model = WorkspaceModel("test_workspace")

        model.set_metadata("key", "value")
        self.assertEqual(model.metadata["key"], "value")

        model.set_metadata("key", "new_value")
        self.assertEqual(model.metadata["key"], "new_value")

    def test_get_metadata(self):
        """Test getting metadata"""
        model = WorkspaceModel("test_workspace")

        # Test with default
        self.assertEqual(model.get_metadata("key", "default"), "default")

        # Test with value
        model.set_metadata("key", "value")
        self.assertEqual(model.get_metadata("key", "default"), "value")

    def test_to_dict(self):
        """Test converting to dictionary"""
        model = WorkspaceModel("test_workspace")
        model.store_data("data_key", "data_value")
        model.update_status("running")
        model.set_metadata("meta_key", "meta_value")

        data = model.to_dict()
        self.assertEqual(data["id"], "test_workspace")
        self.assertEqual(data["data_store"], {"data_key": "data_value"})
        self.assertEqual(data["status"], "running")
        self.assertEqual(data["metadata"], {"meta_key": "meta_value"})

    def test_from_dict(self):
        """Test creating from dictionary"""
        data = {
            "id": "test_workspace",
            "data_store": {"data_key": "data_value"},
            "status": "running",
            "metadata": {"meta_key": "meta_value"},
        }

        model = WorkspaceModel.from_dict(data)
        self.assertEqual(model.id, "test_workspace")
        self.assertEqual(model.data_store, {"data_key": "data_value"})
        self.assertEqual(model.status, "running")
        self.assertEqual(model.metadata, {"meta_key": "meta_value"})


class TestAgent(unittest.TestCase):
    """Test the Agent class"""

    def setUp(self):
        """Set up the test"""

        # Create a concrete implementation of the abstract Agent class
        class ConcreteAgent(Agent):
            async def initialize(self):
                pass

            async def shutdown(self):
                pass

            async def _process_task_impl(self, task_type, task_data):
                return {"status": "success", "task_type": task_type}

        self.agent_class = ConcreteAgent
        self.agent = self.agent_class("test_agent", "test_type", {"key": "value"})

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.agent.id, "test_agent")
        self.assertEqual(self.agent.model.agent_type, "test_type")
        self.assertEqual(self.agent.model.config, {"key": "value"})
        self.assertIsNone(self.agent.workspace)
        self.assertEqual(self.agent.cache, {})

    def test_setup_config_schema(self):
        """Test setting up config schema"""
        # The default implementation should set up some basic schema
        self.assertIn("openai_api_key", self.agent.model.optional_config)

    def test_update_config(self):
        """Test updating config"""
        errors = self.agent.update_config({"new_key": "new_value"})
        self.assertEqual(len(errors), 0)
        self.assertEqual(self.agent.model.config["key"], "value")
        self.assertEqual(self.agent.model.config["new_key"], "new_value")

    def test_register_with_workspace(self):
        """Test registering with workspace"""
        workspace = MagicMock()
        self.agent.register_with_workspace(workspace)
        self.assertEqual(self.agent.workspace, workspace)


class TestSharedWorkspace(unittest.TestCase):
    """Test the SharedWorkspace class"""

    def setUp(self):
        """Set up the test"""
        self.workspace = SharedWorkspace("test_workspace")

        # Create a mock agent
        self.mock_agent = MagicMock()
        self.mock_agent.id = "test_agent"
        self.mock_agent.register_with_workspace = MagicMock()

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.workspace.model.id, "test_workspace")
        self.assertEqual(self.workspace.agents, {})
        self.assertFalse(self.workspace._running)
        self.assertEqual(self.workspace.metrics["tasks_processed"], 0)
        self.assertEqual(self.workspace.metrics["agent_errors"], 0)
        self.assertIsNone(self.workspace.metrics["start_time"])

    def test_register_agent(self):
        """Test registering an agent"""
        self.workspace.register_agent(self.mock_agent)
        self.assertIn("test_agent", self.workspace.agents)
        self.assertEqual(self.workspace.agents["test_agent"], self.mock_agent)
        self.mock_agent.register_with_workspace.assert_called_once_with(self.workspace)

    def test_store_data(self):
        """Test storing data"""
        # Start the workspace for this test
        self.workspace._running = True
        self.workspace.model = WorkspaceModel("test_workspace")  # Create a fresh model

        # Store data
        self.workspace.store_data("key", "value")
        self.assertEqual(self.workspace.model.data_store["key"], "value")

    def test_get_data(self):
        """Test getting data"""
        # Start the workspace for this test
        self.workspace._running = True
        self.workspace.model = WorkspaceModel("test_workspace")  # Create a fresh model

        # Test with default
        self.assertEqual(self.workspace.get_data("key", "default"), "default")

        # Test with value
        self.workspace.store_data("key", "value")
        self.assertEqual(self.workspace.get_data("key", "default"), "value")

    def test_cache_analysis(self):
        """Test caching analysis"""
        self.workspace.cache_analysis("key", "value")
        self.assertIn("key", self.workspace.analysis_cache)
        self.assertEqual(self.workspace.analysis_cache["key"]["value"], "value")
        self.assertIn("timestamp", self.workspace.analysis_cache["key"])

    def test_get_cached_analysis(self):
        """Test getting cached analysis"""
        # Test with no cache
        self.assertIsNone(self.workspace.get_cached_analysis("key"))

        # Test with cache
        self.workspace.cache_analysis("key", "value")
        self.assertEqual(self.workspace.get_cached_analysis("key"), "value")

    def test_is_ready(self):
        """Test checking if workspace is ready"""
        self.assertFalse(self.workspace.is_ready())
        self.workspace._running = True
        self.assertTrue(self.workspace.is_ready())


class TestSharedWorkspaceAsync(unittest.TestCase):
    """Test the async methods of SharedWorkspace"""

    def setUp(self):
        """Set up the test"""
        self.workspace = SharedWorkspace("test_workspace")

        # Create a mock agent
        self.mock_agent = MagicMock()
        self.mock_agent.id = "test_agent"
        self.mock_agent.register_with_workspace = MagicMock()
        self.mock_agent.process_task = AsyncMock(return_value={"status": "success"})
        self.mock_agent.initialize = AsyncMock()
        self.mock_agent.model = MagicMock()
        self.mock_agent.model.get_state = MagicMock(return_value="initialized")

        # Register the agent
        self.workspace.register_agent(self.mock_agent)

    def test_start(self):
        """Test starting the workspace"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Start the workspace
            loop.run_until_complete(self.workspace.start())

            # Check that the workspace is running
            self.assertTrue(self.workspace._running)
            self.assertEqual(self.workspace.model.status, "running")
            self.assertIsNotNone(self.workspace.metrics["start_time"])
        finally:
            loop.close()

    def test_stop(self):
        """Test stopping the workspace"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Start and then stop the workspace
            loop.run_until_complete(self.workspace.start())
            loop.run_until_complete(self.workspace.stop())

            # Check that the workspace is stopped
            self.assertFalse(self.workspace._running)
            self.assertEqual(self.workspace.model.status, "stopped")
        finally:
            loop.close()

    def test_process_agent_task(self):
        """Test processing an agent task"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Start the workspace
            loop.run_until_complete(self.workspace.start())

            # Process a task
            result = loop.run_until_complete(
                self.workspace.process_agent_task(
                    "test_agent", "test_task", {"key": "value"}
                )
            )

            # Check the result
            self.assertEqual(result["status"], "success")

            # Check that the agent was called
            self.mock_agent.process_task.assert_called_once_with(
                "test_task", {"key": "value"}
            )

            # Check that the metrics were updated
            self.assertEqual(self.workspace.metrics["tasks_processed"], 1)
        finally:
            loop.close()

    def test_process_agent_task_error(self):
        """Test processing an agent task with an error"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Start the workspace
            loop.run_until_complete(self.workspace.start())

            # Make the agent raise an exception
            self.mock_agent.process_task.side_effect = Exception("Test error")

            # Process a task and expect an exception
            with self.assertRaises(Exception):
                loop.run_until_complete(
                    self.workspace.process_agent_task(
                        "test_agent",
                        "test_task",
                        {"key": "value", "_test_raise_exceptions": True},
                    )
                )

            # Check that the metrics were updated
            self.assertEqual(self.workspace.metrics["agent_errors"], 1)
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
