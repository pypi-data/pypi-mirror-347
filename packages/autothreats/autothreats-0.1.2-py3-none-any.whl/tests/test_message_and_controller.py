#!/usr/bin/env python3
"""
Unit tests for the Message and AgentController classes.
"""

import os
import sys
import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import Agent, AgentController, AgentModel, Message
from tests.async_test_base import AsyncTestCase, async_test


class TestMessage(unittest.TestCase):
    """Test the Message class"""

    def test_message_initialization(self):
        """Test message initialization with default values"""
        message = Message(message_type="test_type")

        # Check default values
        self.assertEqual(message.message_type, "test_type")
        self.assertEqual(message.content, {})
        self.assertIsNone(message.sender_id)
        self.assertIsNone(message.receiver_id)
        self.assertIsNotNone(message.message_id)
        self.assertIsNone(message.correlation_id)
        self.assertIsNotNone(message.timestamp)

    def test_message_initialization_with_values(self):
        """Test message initialization with provided values"""
        content = {"key": "value"}
        message_id = "test_message_id"
        correlation_id = "test_correlation_id"
        timestamp = 1234567890.0

        message = Message(
            message_type="test_type",
            content=content,
            sender_id="sender",
            receiver_id="receiver",
            message_id=message_id,
            correlation_id=correlation_id,
            timestamp=timestamp,
        )

        # Check values
        self.assertEqual(message.message_type, "test_type")
        self.assertEqual(message.content, content)
        self.assertEqual(message.sender_id, "sender")
        self.assertEqual(message.receiver_id, "receiver")
        self.assertEqual(message.message_id, message_id)
        self.assertEqual(message.correlation_id, correlation_id)
        self.assertEqual(message.timestamp, timestamp)

    def test_to_dict(self):
        """Test converting message to dictionary"""
        content = {"key": "value"}
        message_id = "test_message_id"
        correlation_id = "test_correlation_id"
        timestamp = 1234567890.0

        message = Message(
            message_type="test_type",
            content=content,
            sender_id="sender",
            receiver_id="receiver",
            message_id=message_id,
            correlation_id=correlation_id,
            timestamp=timestamp,
        )

        message_dict = message.to_dict()

        # Check dictionary values
        self.assertEqual(message_dict["message_type"], "test_type")
        self.assertEqual(message_dict["content"], content)
        self.assertEqual(message_dict["sender_id"], "sender")
        self.assertEqual(message_dict["receiver_id"], "receiver")
        self.assertEqual(message_dict["message_id"], message_id)
        self.assertEqual(message_dict["correlation_id"], correlation_id)
        self.assertEqual(message_dict["timestamp"], timestamp)

    def test_from_dict(self):
        """Test creating message from dictionary"""
        message_dict = {
            "message_type": "test_type",
            "content": {"key": "value"},
            "sender_id": "sender",
            "receiver_id": "receiver",
            "message_id": "test_message_id",
            "correlation_id": "test_correlation_id",
            "timestamp": 1234567890.0,
        }

        message = Message.from_dict(message_dict)

        # Check values
        self.assertEqual(message.message_type, "test_type")
        self.assertEqual(message.content, {"key": "value"})
        self.assertEqual(message.sender_id, "sender")
        self.assertEqual(message.receiver_id, "receiver")
        self.assertEqual(message.message_id, "test_message_id")
        self.assertEqual(message.correlation_id, "test_correlation_id")
        self.assertEqual(message.timestamp, 1234567890.0)


class MockAgent(Agent):
    """Mock agent for testing"""

    async def initialize(self):
        """Initialize the agent"""
        pass

    async def shutdown(self):
        """Shut down the agent"""
        pass

    async def _process_task_impl(self, task_type, task_data):
        """Implementation of task processing logic"""
        return {"status": "success", "task_type": task_type}


class TestAgentController(AsyncTestCase):
    """Test the AgentController class"""

    def setUp(self):
        """Set up the test"""
        # Create a mock agent
        self.agent = MockAgent("test_agent", "test_type")

        # Create a controller
        self.controller = AgentController(self.agent)

    @async_test
    async def test_controller_initialization(self):
        """Test controller initialization"""
        # Check values
        self.assertEqual(self.controller.agent, self.agent)
        self.assertEqual(self.controller.model, self.agent.model)

        # Initialize the controller
        await self.controller.initialize()

    @async_test
    async def test_controller_shutdown(self):
        """Test controller shutdown"""
        # Initialize and then shut down
        await self.controller.initialize()
        await self.controller.shutdown()

    @async_test
    async def test_handle_message(self):
        """Test handling a message"""
        # Create a message
        message = Message(message_type="test_type", content={"key": "value"})

        # Handle the message
        result = await self.controller.handle_message(message)

        # Default implementation returns None
        self.assertIsNone(result)

    @async_test
    async def test_handle_message_error(self):
        """Test handling a message with an error"""
        # Create a message
        message = Message(message_type="test_type", content={"key": "value"})

        # Mock _handle_message_impl to raise an exception
        self.controller._handle_message_impl = AsyncMock(
            side_effect=Exception("Test error")
        )

        # Handle the message
        result = await self.controller.handle_message(message)

        # Check error result
        self.assertEqual(result["status"], "error")
        self.assertIn("Test error", result["message"])


class CustomController(AgentController):
    """Custom controller for testing overriding _handle_message_impl"""

    async def _handle_message_impl(self, message):
        """Custom implementation of message handling"""
        if message.message_type == "test_type":
            return {"status": "success", "custom": True}
        return await super()._handle_message_impl(message)


class TestCustomController(AsyncTestCase):
    """Test a custom controller implementation"""

    def setUp(self):
        """Set up the test"""
        # Create a mock agent
        self.agent = MockAgent("test_agent", "test_type")

        # Create a controller
        self.controller = CustomController(self.agent)

    @async_test
    async def test_custom_handle_message(self):
        """Test custom message handling"""
        # Create a message
        message = Message(message_type="test_type", content={"key": "value"})

        # Handle the message
        result = await self.controller.handle_message(message)

        # Check custom result
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["custom"])

    @async_test
    async def test_unhandled_message_type(self):
        """Test handling an unhandled message type"""
        # Create a message with a different type
        message = Message(message_type="unknown_type", content={"key": "value"})

        # Handle the message
        result = await self.controller.handle_message(message)

        # Default implementation returns None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
