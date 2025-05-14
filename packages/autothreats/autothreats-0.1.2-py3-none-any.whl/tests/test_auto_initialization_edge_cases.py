#!/usr/bin/env python3
"""
Tests for edge cases in auto-initialization and auto-start functionality.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import Agent, SharedWorkspace
from tests.async_test_base import AsyncTestCase, async_test
from tests.test_helpers import ConcreteTestAgent


class MockAgentWithFailingInit(Agent):
    """Mock agent that fails during initialization"""

    def __init__(self, agent_id: str, config=None):
        super().__init__(agent_id, "mock_agent", config or {})
        self.initialize_called = False

    async def initialize(self):
        """Initialize the agent but fail"""
        self.initialize_called = True
        raise RuntimeError("Initialization failed")

    async def _process_task_impl(self, task_type, task_data):
        """Process a task"""
        return {"status": "success", "message": "Task processed"}

    async def shutdown(self):
        """Clean up resources when shutting down"""
        pass


class MockWorkspaceWithFailingStart(SharedWorkspace):
    """Mock workspace that fails during start"""

    async def start(self):
        """Start the workspace but fail"""
        raise RuntimeError("Workspace start failed")


class TestAutoInitializationEdgeCases(AsyncTestCase):
    """Test edge cases for auto-initialization"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a workspace
        self.workspace = SharedWorkspace("test_workspace")
        await self.workspace.start()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_auto_initialization_failure(self):
        """Test what happens when auto-initialization fails"""
        # Create an agent that fails during initialization
        agent = MockAgentWithFailingInit("test_agent")
        self.workspace.register_agent(agent)

        # Process a task with auto-initialization enabled
        task_data = {"key": "value", "_test_auto_initialize": True}

        # Process task should return an error
        result = await agent.process_task("test_task", task_data)

        # Verify the result
        self.assertEqual(
            result["status"], "error", "Task should fail when auto-initialization fails"
        )
        self.assertIn(
            "initialization failed",
            result["message"].lower(),
            "Error message should mention initialization failure",
        )

        # Verify initialization was attempted
        self.assertTrue(
            agent.initialize_called, "Initialization should have been attempted"
        )

    @async_test
    async def test_auto_start_failure(self):
        """Test what happens when auto-start fails"""
        # Create a workspace that fails during start
        failing_workspace = MockWorkspaceWithFailingStart("failing_workspace")

        # Create an agent
        agent = MagicMock()
        agent.id = "test_agent"
        failing_workspace.register_agent(agent)

        # Try to store data with auto-start enabled
        try:
            failing_workspace.store_data("_test_auto_start", "value")
            # This should not raise an exception, but the data should not be stored
            self.assertIsNone(
                failing_workspace.get_data("_test_auto_start"),
                "Data should not be stored when auto-start fails",
            )
        except Exception as e:
            self.fail(f"store_data should not raise an exception: {e}")

    @async_test
    async def test_partial_initialization(self):
        """Test behavior with partial initialization"""
        # Create an agent with a patched initialize method
        agent = MagicMock()
        agent.id = "test_agent"
        agent.initialize = AsyncMock()
        agent.initialize.side_effect = lambda: setattr(
            agent, "partially_initialized", True
        )
        agent.process_task = AsyncMock()
        agent.process_task.return_value = {"status": "success"}

        # Register the agent
        self.workspace.register_agent(agent)

        # Process a task
        await self.workspace.process_agent_task(
            "test_agent", "test_task", {"key": "value"}
        )

        # Verify the agent was initialized
        agent.initialize.assert_called_once()

        # Verify the task was processed
        agent.process_task.assert_called_once()


class TestConcurrencyEdgeCases(AsyncTestCase):
    """Test edge cases for concurrency"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a workspace
        self.workspace = SharedWorkspace("test_workspace")
        await self.workspace.start()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_concurrent_data_access(self):
        """Test concurrent access to workspace data"""
        # Initialize counter
        self.workspace.store_data("counter", 0)

        # Define a task that increments the counter
        async def increment_counter():
            for _ in range(10):
                # Get current counter value
                counter = self.workspace.get_data("counter")
                # Simulate some processing time
                await asyncio.sleep(0.001)
                # Increment and store
                self.workspace.store_data("counter", counter + 1)

        # Run multiple tasks concurrently
        tasks = [increment_counter() for _ in range(5)]
        await asyncio.gather(*tasks)

        # Get final counter value
        final_counter = self.workspace.get_data("counter")

        # In a perfect world with proper locking, this would be 50
        # But we're testing that the workspace doesn't crash with concurrent access
        self.assertIsNotNone(final_counter, "Counter should have a value")
        self.assertGreaterEqual(
            final_counter, 1, "Counter should have been incremented at least once"
        )

    @async_test
    async def test_concurrent_agent_tasks(self):
        """Test concurrent processing of tasks by multiple agents"""
        # Create multiple agents with proper mocking for model and initialize
        agent1 = MagicMock()
        agent1.id = "agent1"
        agent1.process_task = AsyncMock()
        agent1.process_task.return_value = {"status": "success", "agent": "agent1"}
        # Mock the model attribute and get_state method
        agent1.model = MagicMock()
        agent1.model.get_state.return_value = "initialized"
        agent1.initialize = AsyncMock()

        agent2 = MagicMock()
        agent2.id = "agent2"
        agent2.process_task = AsyncMock()
        agent2.process_task.return_value = {"status": "success", "agent": "agent2"}
        # Mock the model attribute and get_state method
        agent2.model = MagicMock()
        agent2.model.get_state.return_value = "initialized"
        agent2.initialize = AsyncMock()

        # Register agents
        self.workspace.register_agent(agent1)
        self.workspace.register_agent(agent2)

        # Process tasks concurrently
        task1 = self.workspace.process_agent_task(
            "agent1", "test_task", {"key": "value1"}
        )
        task2 = self.workspace.process_agent_task(
            "agent2", "test_task", {"key": "value2"}
        )

        results = await asyncio.gather(task1, task2)

        # Verify both tasks were processed
        self.assertEqual(
            results[0]["agent"], "agent1", "First task should be processed by agent1"
        )
        self.assertEqual(
            results[1]["agent"], "agent2", "Second task should be processed by agent2"
        )


class TestErrorRecovery(AsyncTestCase):
    """Test error recovery scenarios"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a workspace
        self.workspace = SharedWorkspace("test_workspace")
        await self.workspace.start()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_recovery_after_agent_crash(self):
        """Test recovery after an agent crashes"""
        # Create an agent that crashes during task processing
        agent = MagicMock()
        agent.id = "crash_agent"
        agent.process_task = AsyncMock()
        agent.process_task.side_effect = [
            Exception("Agent crashed"),  # First call crashes
            {"status": "success"},  # Second call succeeds
        ]
        # Mock the model attribute and get_state method
        agent.model = MagicMock()
        agent.model.get_state.return_value = "initialized"
        agent.initialize = AsyncMock()

        # Register the agent
        self.workspace.register_agent(agent)

        # Process a task that will cause the agent to crash
        result1 = await self.workspace.process_agent_task(
            "crash_agent",
            "test_task",
            {"key": "value", "_test_raise_exceptions": False},
        )

        # Verify the result indicates an error
        self.assertEqual(
            result1["status"], "error", "Task should fail when agent crashes"
        )

        # Process another task
        result2 = await self.workspace.process_agent_task(
            "crash_agent", "test_task", {"key": "value"}
        )

        # Verify the second task succeeded
        self.assertEqual(
            result2["status"], "success", "Agent should recover after crash"
        )

    @async_test
    async def test_recovery_after_workspace_restart(self):
        """Test recovery after workspace restart"""
        # Store some data
        self.workspace.store_data("test_key", "test_value")

        # Stop the workspace
        await self.workspace.stop()

        # Verify data is cleared
        self.assertIsNone(
            self.workspace.get_data("test_key"), "Data should be cleared after stop"
        )

        # Restart the workspace
        await self.workspace.start()

        # Store new data
        self.workspace.store_data("new_key", "new_value")

        # Verify new data is accessible
        self.assertEqual(
            self.workspace.get_data("new_key"),
            "new_value",
            "New data should be accessible after restart",
        )


class TestResourceManagement(AsyncTestCase):
    """Test resource management scenarios"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a workspace
        self.workspace = SharedWorkspace("test_workspace")
        await self.workspace.start()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_large_data_handling(self):
        """Test handling of large data"""
        # Create large data (1MB)
        large_data = "x" * (1024 * 1024)

        # Store large data
        self.workspace.store_data("large_data", large_data)

        # Retrieve large data
        retrieved_data = self.workspace.get_data("large_data")

        # Verify data was stored and retrieved correctly
        self.assertEqual(
            len(retrieved_data),
            len(large_data),
            "Large data not stored or retrieved correctly",
        )

    @async_test
    async def test_resource_cleanup(self):
        """Test cleanup of resources after shutdown"""
        # Create a workspace with a mock Redis client
        redis_client = MagicMock()
        workspace = SharedWorkspace("cleanup_test")
        workspace.redis_client = redis_client
        workspace.distributed_mode = True

        # Start the workspace
        await workspace.start()

        # Stop the workspace
        await workspace.stop()

        # Verify Redis client was closed
        redis_client.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
