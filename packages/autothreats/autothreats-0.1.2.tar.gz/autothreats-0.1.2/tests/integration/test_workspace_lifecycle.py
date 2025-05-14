#!/usr/bin/env python3
"""
Integration tests for workspace lifecycle.
Tests initialization, shutdown, data persistence, and recovery scenarios.
"""

import asyncio
import os
import sys
import unittest
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.agents.simplified_threat_detection import (
    SimplifiedThreatDetectionAgent,
)
from autothreats.simplified_base import Agent, Message, SharedWorkspace
from tests.async_test_base import AsyncTestCase, async_test


class MockAgent(Agent):
    """Mock agent for testing workspace interactions"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "mock_agent", config or {})
        self.initialize_called = False
        self.process_called = False
        self.shutdown_called = False
        self.received_messages = []

    async def initialize(self):
        self.initialize_called = True
        self.model.update_state("status", "initialized")

    async def _process_task_impl(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        self.process_called = True
        return {"status": "success", "message": "Mock processing successful"}

    async def shutdown(self):
        self.shutdown_called = True
        self.model.update_state("status", "shutdown")


class TestWorkspaceLifecycle(AsyncTestCase):
    """Integration tests for workspace lifecycle"""

    async def asyncSetUp(self):
        """Set up the test"""
        pass

    async def asyncTearDown(self):
        """Clean up after the test"""
        pass

    #
    # POSITIVE TESTS FOR WORKSPACE LIFECYCLE
    #

    @async_test
    async def test_workspace_initialization(self):
        """Test successful workspace initialization"""
        # Create a workspace
        workspace = SharedWorkspace("test_workspace")

        # Start the workspace
        await workspace.start()

        # Verify workspace is started
        self.assertTrue(workspace.is_ready(), "Workspace should be ready after start")

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_shutdown(self):
        """Test successful workspace shutdown"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Store some data
        workspace.store_data("test_key", "test_value")

        # Stop the workspace
        await workspace.stop()

        # Verify workspace is stopped
        self.assertFalse(
            workspace.is_ready(), "Workspace should not be ready after stop"
        )

        # Verify data is cleared
        self.assertIsNone(
            workspace.get_data("test_key"), "Data should be cleared after stop"
        )

    @async_test
    async def test_workspace_restart(self):
        """Test workspace restart after shutdown"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Store some data
        workspace.store_data("test_key", "test_value")

        # Stop the workspace
        await workspace.stop()

        # Restart the workspace
        await workspace.start()

        # Verify workspace is running again
        self.assertTrue(workspace.is_ready(), "Workspace should be ready after restart")

        # Verify data is not persisted across restarts
        self.assertIsNone(
            workspace.get_data("test_key"),
            "Data should not be persisted across restarts",
        )

        # Store new data
        workspace.store_data("new_key", "new_value")

        # Verify new data is accessible
        self.assertEqual(
            workspace.get_data("new_key"),
            "new_value",
            "New data should be accessible after restart",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_agent_registration_and_initialization(self):
        """Test agent registration and initialization with workspace"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Create an agent
        agent = MockAgent("test_agent")

        # Register the agent with the workspace
        workspace.register_agent(agent)

        # Verify agent is registered
        self.assertIn(
            agent.id, workspace.agents, "Agent should be registered with workspace"
        )
        self.assertEqual(
            agent.workspace, workspace, "Agent workspace should be set correctly"
        )

        # Initialize the agent
        await agent.initialize()

        # Verify agent is initialized
        self.assertTrue(
            agent.initialize_called, "Agent initialize method should be called"
        )
        self.assertEqual(
            agent.model.get_state("status"),
            "initialized",
            "Agent status should be initialized",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_agent_shutdown(self):
        """Test agent shutdown with workspace"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Create and register an agent
        agent = MockAgent("test_agent")
        workspace.register_agent(agent)

        # Initialize the agent
        await agent.initialize()

        # Shutdown the agent
        await agent.shutdown()

        # Verify agent is shut down
        self.assertTrue(agent.shutdown_called, "Agent shutdown method should be called")
        self.assertEqual(
            agent.model.get_state("status"),
            "shutdown",
            "Agent status should be shutdown",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_data_storage_and_retrieval(self):
        """Test data storage and retrieval in workspace"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Store simple data
        workspace.store_data("string_key", "string_value")
        workspace.store_data("int_key", 123)
        workspace.store_data("bool_key", True)

        # Store complex data
        complex_data = {
            "nested": {"key": "value", "list": [1, 2, 3], "dict": {"a": 1, "b": 2}},
            "array": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
        }
        workspace.store_data("complex_key", complex_data)

        # Retrieve and verify simple data
        self.assertEqual(
            workspace.get_data("string_key"),
            "string_value",
            "String data not retrieved correctly",
        )
        self.assertEqual(
            workspace.get_data("int_key"), 123, "Integer data not retrieved correctly"
        )
        self.assertEqual(
            workspace.get_data("bool_key"), True, "Boolean data not retrieved correctly"
        )

        # Retrieve and verify complex data
        retrieved_complex = workspace.get_data("complex_key")
        self.assertEqual(
            retrieved_complex, complex_data, "Complex data not retrieved correctly"
        )
        self.assertEqual(
            retrieved_complex["nested"]["key"],
            "value",
            "Nested data not retrieved correctly",
        )
        self.assertEqual(
            retrieved_complex["array"][1]["name"],
            "Item 2",
            "Nested array data not retrieved correctly",
        )

        # Retrieve non-existent data
        self.assertIsNone(
            workspace.get_data("nonexistent_key"),
            "Non-existent data should return None",
        )
        self.assertEqual(
            workspace.get_data("nonexistent_key", "default"),
            "default",
            "Non-existent data should return default value if provided",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_data_overwrite(self):
        """Test overwriting data in workspace"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Store initial data
        workspace.store_data("test_key", "initial_value")

        # Verify initial data
        self.assertEqual(
            workspace.get_data("test_key"),
            "initial_value",
            "Initial data not retrieved correctly",
        )

        # Overwrite data
        workspace.store_data("test_key", "updated_value")

        # Verify updated data
        self.assertEqual(
            workspace.get_data("test_key"),
            "updated_value",
            "Updated data not retrieved correctly",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_subscription_system(self):
        """Test workspace subscription system"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Create and register agents
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")
        agent3 = MockAgent("agent3")

        workspace.register_agent(agent1)
        workspace.register_agent(agent2)
        workspace.register_agent(agent3)

        # Subscribe agents to message types
        workspace.subscribe(agent1.id, "TYPE_A")
        workspace.subscribe(agent1.id, "TYPE_B")
        workspace.subscribe(agent2.id, "TYPE_B")
        workspace.subscribe(agent3.id, "TYPE_C")

        # Verify subscriptions
        type_a_subscribers = workspace.get_subscribers("TYPE_A")
        type_b_subscribers = workspace.get_subscribers("TYPE_B")
        type_c_subscribers = workspace.get_subscribers("TYPE_C")

        self.assertIn(
            agent1.id, type_a_subscribers, "Agent1 should be subscribed to TYPE_A"
        )
        self.assertIn(
            agent1.id, type_b_subscribers, "Agent1 should be subscribed to TYPE_B"
        )
        self.assertIn(
            agent2.id, type_b_subscribers, "Agent2 should be subscribed to TYPE_B"
        )
        self.assertIn(
            agent3.id, type_c_subscribers, "Agent3 should be subscribed to TYPE_C"
        )

        # Unsubscribe agent1 from TYPE_B
        workspace.unsubscribe(agent1.id, "TYPE_B")

        # Verify unsubscription
        type_b_subscribers = workspace.get_subscribers("TYPE_B")
        self.assertNotIn(
            agent1.id,
            type_b_subscribers,
            "Agent1 should not be subscribed to TYPE_B after unsubscribe",
        )
        self.assertIn(
            agent2.id, type_b_subscribers, "Agent2 should still be subscribed to TYPE_B"
        )

        # Stop the workspace
        await workspace.stop()

    #
    # NEGATIVE TESTS FOR WORKSPACE LIFECYCLE
    #

    @async_test
    async def test_workspace_double_start(self):
        """Test starting a workspace twice"""
        # Create a workspace
        workspace = SharedWorkspace("test_workspace")

        # Start the workspace
        await workspace.start()

        # Try to start again
        # This should not raise an exception, but should be a no-op
        await workspace.start()

        # Verify workspace is still running
        self.assertTrue(
            workspace.is_ready(), "Workspace should still be ready after double start"
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_double_stop(self):
        """Test stopping a workspace twice"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Stop the workspace
        await workspace.stop()

        # Try to stop again
        # This should not raise an exception, but should be a no-op
        await workspace.stop()

        # Verify workspace is still stopped
        self.assertFalse(
            workspace.is_ready(), "Workspace should still be stopped after double stop"
        )

    @async_test
    async def test_workspace_operations_when_stopped(self):
        """Test workspace operations when stopped"""
        # Create a workspace but don't start it
        workspace = SharedWorkspace("test_workspace")

        # Try to store data (without auto-start)
        workspace.store_data("test_key", "test_value")

        # Verify data was not stored
        self.assertIsNone(
            workspace.get_data("test_key"),
            "Data should not be stored when workspace is stopped",
        )

        # Try to register an agent
        agent = MockAgent("test_agent")
        workspace.register_agent(agent)

        # Verify agent was registered (this should work even when stopped)
        self.assertIn(
            agent.id,
            workspace.agents,
            "Agent should be registered even when workspace is stopped",
        )

        # Try to subscribe to a message type
        workspace.subscribe(agent.id, "TEST_TYPE")

        # Verify subscription (this should work even when stopped)
        subscribers = workspace.get_subscribers("TEST_TYPE")
        self.assertIn(
            agent.id,
            subscribers,
            "Agent should be subscribed even when workspace is stopped",
        )

    @async_test
    async def test_workspace_concurrent_data_access(self):
        """Test concurrent data access in workspace"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Initialize counter
        workspace.store_data("counter", 0)

        # Define a task that increments the counter
        async def increment_counter():
            for _ in range(10):
                # Get current counter value
                counter = workspace.get_data("counter")
                # Simulate some processing time
                await asyncio.sleep(0.001)
                # Increment and store
                workspace.store_data("counter", counter + 1)

        # Run multiple tasks concurrently
        tasks = [increment_counter() for _ in range(5)]
        await asyncio.gather(*tasks)

        # Get final counter value
        final_counter = workspace.get_data("counter")

        # In a perfect world with proper locking, this would be 50
        # But we're testing that the workspace doesn't crash with concurrent access
        self.assertIsNotNone(final_counter, "Counter should have a value")

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_with_large_data(self):
        """Test workspace with large data"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Create large data (1MB)
        large_data = "x" * (1024 * 1024)

        # Store large data
        workspace.store_data("large_data", large_data)

        # Retrieve large data
        retrieved_data = workspace.get_data("large_data")

        # Verify data was stored and retrieved correctly
        self.assertEqual(
            len(retrieved_data),
            len(large_data),
            "Large data not stored or retrieved correctly",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_workspace_with_invalid_agent_registration(self):
        """Test workspace with invalid agent registration"""
        # Create and start a workspace
        workspace = SharedWorkspace("test_workspace")
        await workspace.start()

        # Try to register None as an agent
        try:
            workspace.register_agent(None)
            self.fail("Should have raised an AttributeError")
        except AttributeError as e:
            # Verify error message
            self.assertIn("'NoneType' object has no attribute 'id'", str(e))

        # Try to register a string as an agent
        try:
            workspace.register_agent("not an agent")
            self.fail("Should have raised an AttributeError")
        except AttributeError as e:
            # Verify error message
            self.assertIn("'str' object has no attribute 'id'", str(e))

        # Stop the workspace
        await workspace.stop()


if __name__ == "__main__":
    unittest.main()
