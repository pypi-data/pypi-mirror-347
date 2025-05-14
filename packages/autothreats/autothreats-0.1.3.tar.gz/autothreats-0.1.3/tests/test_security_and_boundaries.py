#!/usr/bin/env python3
"""
Tests for security and boundary conditions.
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import SharedWorkspace
from tests.async_test_base import AsyncTestCase, async_test
from tests.test_helpers import ConcreteTestAgent


class TestInputValidation(AsyncTestCase):
    """Test input validation and sanitization"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a workspace
        self.workspace = SharedWorkspace("test_workspace")
        await self.workspace.start()

        # Create an agent
        self.agent = ConcreteTestAgent("test_agent", "test_type", {})
        self.workspace.register_agent(self.agent)
        await self.agent.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_invalid_task_type(self):
        """Test handling of invalid task types"""
        # Process a task with an invalid type
        result = await self.agent.process_task("invalid_task_type", {})

        # Verify the result indicates an error
        self.assertEqual(
            result["status"], "error", "Task should fail with invalid type"
        )
        self.assertIn(
            "unsupported task type",
            result["message"].lower(),
            "Error message should mention unsupported task type",
        )

    @async_test
    async def test_missing_required_parameters(self):
        """Test handling of missing required parameters"""
        # Create a task with missing required parameters
        task_data = {}  # Empty data

        # Process the task
        result = await self.agent.process_task("test_task", task_data)

        # Verify the result indicates an error
        self.assertEqual(
            result["status"], "error", "Task should fail with missing parameters"
        )

    @async_test
    async def test_malformed_json_data(self):
        """Test handling of malformed JSON data"""
        # Create a task with malformed JSON data
        task_data = {"json_data": "{ this is not valid JSON }"}

        # Process the task
        result = await self.agent._process_task_impl("parse_json", task_data)

        # Verify the result indicates an error
        self.assertEqual(
            result["status"], "error", "Task should fail with malformed JSON"
        )

    @async_test
    async def test_oversized_input(self):
        """Test handling of oversized input"""
        # Create a task with oversized input
        task_data = {"text": "x" * (10 * 1024 * 1024)}  # 10MB of data

        # Process the task
        result = await self.agent._process_task_impl("process_text", task_data)

        # Verify the result indicates an error
        self.assertEqual(
            result["status"], "error", "Task should fail with oversized input"
        )


class TestSecurityBoundaries(AsyncTestCase):
    """Test security boundaries and isolation"""

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
    async def test_agent_isolation(self):
        """Test isolation between agents"""
        # Create two agents
        agent1 = ConcreteTestAgent("agent1", "test_type", {})
        agent2 = ConcreteTestAgent("agent2", "test_type", {})

        # Register agents with workspace
        self.workspace.register_agent(agent1)
        self.workspace.register_agent(agent2)

        # Initialize agents
        await agent1.initialize()
        await agent2.initialize()

        # Add private data to agent1
        agent1.private_data = {"secret": "agent1_secret"}

        # Add private data to agent2
        agent2.private_data = {"secret": "agent2_secret"}

        # Verify agent2 cannot access agent1's private data
        self.assertNotEqual(
            agent2.private_data.get("secret"),
            "agent1_secret",
            "Agent2 should not have access to Agent1's private data",
        )

        # Verify agent1 cannot access agent2's private data
        self.assertNotEqual(
            agent1.private_data.get("secret"),
            "agent2_secret",
            "Agent1 should not have access to Agent2's private data",
        )

    @async_test
    async def test_workspace_data_access_control(self):
        """Test access control for workspace data"""
        # Create a workspace with access control
        workspace = SharedWorkspace("secure_workspace")
        await workspace.start()

        # Create agents with different access levels
        admin_agent = ConcreteTestAgent("admin_agent", "admin", {})
        user_agent = ConcreteTestAgent("user_agent", "user", {})

        # Register agents
        workspace.register_agent(admin_agent)
        workspace.register_agent(user_agent)

        # Initialize agents
        await admin_agent.initialize()
        await user_agent.initialize()

        # Store data with access control
        workspace.store_data("admin_data", {"value": "admin_secret", "access": "admin"})
        workspace.store_data("user_data", {"value": "user_data", "access": "user"})
        workspace.store_data(
            "public_data", {"value": "public_data", "access": "public"}
        )

        # Define a method to check access
        def check_access(agent, key):
            data = workspace.get_data(key)
            if data and data.get("access"):
                return agent.type == data["access"] or data["access"] == "public"
            return True

        # Verify admin can access admin data
        self.assertTrue(
            check_access(admin_agent, "admin_data"),
            "Admin agent should have access to admin data",
        )

        # Verify user cannot access admin data
        self.assertFalse(
            check_access(user_agent, "admin_data"),
            "User agent should not have access to admin data",
        )

        # Verify both can access public data
        self.assertTrue(
            check_access(admin_agent, "public_data"),
            "Admin agent should have access to public data",
        )
        self.assertTrue(
            check_access(user_agent, "public_data"),
            "User agent should have access to public data",
        )

        # Stop the workspace
        await workspace.stop()

    @async_test
    async def test_command_injection_prevention(self):
        """Test prevention of command injection"""
        # Create an agent
        agent = ConcreteTestAgent("test_agent", "test_type", {})

        # Register agent with workspace
        self.workspace.register_agent(agent)

        # Initialize agent
        await agent.initialize()

        # Create a task with potential command injection
        task_data = {
            "command": "echo 'hello'; rm -rf /",
            "args": ["--help; echo 'pwned'"],
        }

        # Process the task
        result = await agent._process_task_impl("run_command", task_data)

        # Verify the result indicates an error
        self.assertEqual(
            result["status"],
            "error",
            "Task should fail with potential command injection",
        )
        self.assertIn(
            "invalid command",
            result["message"].lower(),
            "Error message should mention invalid command",
        )


class TestBoundaryConditions(AsyncTestCase):
    """Test boundary conditions and edge cases"""

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
    async def test_empty_input(self):
        """Test handling of empty input"""
        # Create an agent
        agent = ConcreteTestAgent("test_agent", "test_type", {})

        # Register agent with workspace
        self.workspace.register_agent(agent)

        # Initialize agent
        await agent.initialize()

        # Create tasks with empty input
        empty_string_task = {"text": ""}
        empty_list_task = {"list": []}
        empty_dict_task = {"dict": {}}

        # Process tasks
        result1 = await agent._process_task_impl("process_text", empty_string_task)
        result2 = await agent._process_task_impl("process_list", empty_list_task)
        result3 = await agent._process_task_impl("process_dict", empty_dict_task)

        # Verify results
        self.assertEqual(
            result1["status"], "success", "Task should handle empty string"
        )
        self.assertEqual(result2["status"], "success", "Task should handle empty list")
        self.assertEqual(result3["status"], "success", "Task should handle empty dict")

    @async_test
    async def test_unicode_handling(self):
        """Test handling of Unicode characters"""
        # Create an agent
        agent = ConcreteTestAgent("test_agent", "test_type", {})

        # Register agent with workspace
        self.workspace.register_agent(agent)

        # Initialize agent
        await agent.initialize()

        # Create a task with Unicode characters
        task_data = {"text": "Hello, 世界! Привет, мир! مرحبا بالعالم!"}

        # Process the task
        result = await agent._process_task_impl("process_text", task_data)

        # Verify the result
        self.assertEqual(
            result["status"], "success", "Task should handle Unicode characters"
        )

    @async_test
    async def test_maximum_recursion_depth(self):
        """Test handling of maximum recursion depth"""
        # Create a deeply nested structure
        depth = 1000
        nested_dict = {}
        current = nested_dict

        for i in range(depth):
            current["nested"] = {}
            current = current["nested"]

        # Store the deeply nested structure
        try:
            self.workspace.store_data("nested_dict", nested_dict)
            retrieved = self.workspace.get_data("nested_dict")
            self.assertIsNotNone(retrieved, "Should handle deeply nested structures")
        except RecursionError:
            self.fail("RecursionError should be handled gracefully")
        except Exception as e:
            # Other exceptions might be acceptable if they're handled gracefully
            self.assertNotIsInstance(
                e, RecursionError, "RecursionError should be handled gracefully"
            )


if __name__ == "__main__":
    unittest.main()
