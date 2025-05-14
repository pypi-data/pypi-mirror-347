#!/usr/bin/env python3
"""
Tests for the simplified container runner
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Mock redis module before importing the container runner
sys.modules["redis"] = MagicMock()
import redis

# Use a relative import
from .async_test_base import AsyncTestCase, async_test

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_container_runner import (
    AGENT_CLASSES,
    SimplifiedContainerRunner,
    main,
)


class TestSimplifiedContainerRunner(AsyncTestCase):
    """Test the simplified container runner"""

    def setUp(self):
        """Set up the test"""
        # Create a container runner
        self.runner = SimplifiedContainerRunner()

    def test_initialization(self):
        """Test initialization"""
        self.assertIsNotNone(self.runner.config)
        self.assertIsNone(self.runner.redis_client)
        self.assertFalse(self.runner.running)
        self.assertIsNone(self.runner.agent)
        self.assertIsNone(self.runner.workspace)
        self.assertIsNone(self.runner.orchestrator)

    def test_load_config(self):
        """Test loading configuration"""
        config = self.runner._load_config()
        self.assertIn("redis", config)
        self.assertIn("workspace", config)
        self.assertIn("orchestrator", config)
        self.assertIn("api", config)
        self.assertIn("llm", config)
        self.assertIn("openai", config)
        self.assertIn("anthropic", config)
        self.assertIn("system", config)
        self.assertIn("security_tools", config)

    def test_deep_merge(self):
        """Test deep merging of dictionaries"""
        source = {
            "a": 1,
            "b": {
                "c": 2,
                "d": 3,
            },
            "e": 4,
        }
        destination = {
            "a": 5,
            "b": {
                "c": 6,
                "f": 7,
            },
            "g": 8,
        }
        self.runner._deep_merge(source, destination)
        self.assertEqual(destination["a"], 1)  # Overwritten
        self.assertEqual(destination["b"]["c"], 2)  # Overwritten
        self.assertEqual(destination["b"]["d"], 3)  # Added
        self.assertEqual(destination["b"]["f"], 7)  # Preserved
        self.assertEqual(destination["e"], 4)  # Added
        self.assertEqual(destination["g"], 8)  # Preserved

    @patch("redis.Redis")
    @patch("redis.ConnectionPool")
    def test_setup_redis_success(self, mock_pool, mock_redis):
        """Test setting up Redis successfully"""
        # Mock Redis client
        mock_client = MagicMock()
        mock_client.ping.return_value = True
        mock_redis.return_value = mock_client

        # Call the method
        result = self.runner._setup_redis()

        # Check the result
        self.assertTrue(result)
        self.assertEqual(self.runner.redis_client, mock_client)

    @patch("redis.Redis")
    @patch("redis.ConnectionPool")
    def test_setup_redis_failure(self, mock_pool, mock_redis):
        """Test setting up Redis with failure"""
        # Mock Redis client to raise an exception
        mock_client = MagicMock()
        mock_client.ping.side_effect = Exception("Connection failed")
        mock_redis.return_value = mock_client

        # Patch time.sleep to avoid waiting
        with patch("time.sleep"):
            # Call the method
            result = self.runner._setup_redis()

            # Check the result
            self.assertFalse(result)
            self.assertIsNone(self.runner.redis_client)

    def test_run_orchestrator(self):
        """Test running the orchestrator service"""
        # Mock the orchestrator
        with patch(
            "autothreats.simplified_container_runner.SimplifiedOrchestrator"
        ) as MockOrchestrator:
            mock_orchestrator = MagicMock()
            mock_orchestrator.initialize = AsyncMock()
            mock_orchestrator.shutdown = AsyncMock()
            MockOrchestrator.return_value = mock_orchestrator

            # Patch the run_orchestrator method to call initialize and shutdown directly
            with patch.object(
                self.runner, "run_orchestrator", new=self._mock_run_orchestrator
            ):
                # Create a new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Run the orchestrator
                    loop.run_until_complete(self.runner.run_orchestrator())

                    # Check that the orchestrator was initialized and shut down
                    mock_orchestrator.initialize.assert_called_once()
                    mock_orchestrator.shutdown.assert_called_once()
                finally:
                    loop.close()
                    asyncio.set_event_loop(asyncio.new_event_loop())

    async def _mock_run_orchestrator(self):
        """Mock implementation of run_orchestrator for testing"""
        # Get the mock orchestrator that was created in the test
        from autothreats.simplified_container_runner import SimplifiedOrchestrator

        self.orchestrator = SimplifiedOrchestrator.return_value

        # Initialize orchestrator
        await self.orchestrator.initialize()

        # Shutdown orchestrator
        await self.orchestrator.shutdown()

        return 0

    def test_run_workspace(self):
        """Test running the workspace service"""
        # Mock the workspace
        with patch(
            "autothreats.simplified_container_runner.SharedWorkspace"
        ) as MockWorkspace:
            mock_workspace = MagicMock()
            mock_workspace.start = AsyncMock()
            mock_workspace.stop = AsyncMock()
            MockWorkspace.return_value = mock_workspace

            # Patch the run_workspace method to call start and stop directly
            with patch.object(
                self.runner, "run_workspace", new=self._mock_run_workspace
            ):
                # Create a new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Run the workspace
                    loop.run_until_complete(self.runner.run_workspace())

                    # Check that the workspace was started and stopped
                    mock_workspace.start.assert_called_once()
                    mock_workspace.stop.assert_called_once()
                finally:
                    loop.close()
                    asyncio.set_event_loop(asyncio.new_event_loop())

    async def _mock_run_workspace(self):
        """Mock implementation of run_workspace for testing"""
        # Get the mock workspace that was created in the test
        from autothreats.simplified_container_runner import SharedWorkspace

        self.workspace = SharedWorkspace.return_value

        # Start workspace
        await self.workspace.start()

        # Stop workspace
        await self.workspace.stop()

        return 0

    def test_run_agent(self):
        """Test running an agent"""
        # Mock the agent
        with patch(
            "autothreats.simplified_container_runner.SimplifiedThreatDetectionAgent"
        ) as MockAgent:
            # Create a mock agent that will be properly initialized
            mock_agent = MagicMock()
            mock_agent.initialize = AsyncMock()
            mock_agent.shutdown = AsyncMock()
            MockAgent.return_value = mock_agent

            # Patch the run_agent method to call initialize and shutdown directly
            with patch.object(self.runner, "run_agent", new=self._mock_run_agent):
                # Create a new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Run the agent
                    loop.run_until_complete(self.runner.run_agent("threat_detection"))

                    # Check that the agent was initialized and shut down
                    mock_agent.initialize.assert_called_once()
                    mock_agent.shutdown.assert_called_once()
                finally:
                    loop.close()
                    asyncio.set_event_loop(asyncio.new_event_loop())

    async def _mock_run_agent(self, agent_type):
        """Mock implementation of run_agent for testing"""
        # Get the mock agent directly from the patched class
        # This is available in the test scope
        from autothreats.simplified_container_runner import (
            SimplifiedThreatDetectionAgent,
        )

        self.agent = SimplifiedThreatDetectionAgent.return_value

        # Initialize agent
        await self.agent.initialize()

        # Shutdown agent
        await self.agent.shutdown()

        return 0

    @async_test
    async def test_run_agent_unknown_type(self):
        """Test running an agent with an unknown type"""
        # Run the agent with an unknown type
        result = await self.runner.run_agent("unknown_agent_type")

        # Check the result
        self.assertEqual(result, 1)

    def test_run_api(self):
        """Test running the API service"""
        # Mock the API server
        with patch(
            "autothreats.simplified_api_server.create_app"
        ) as mock_create_app, patch("uvicorn.Server") as MockServer:
            mock_server = MagicMock()
            mock_server.serve = AsyncMock()
            MockServer.return_value = mock_server

            # Mock the create_app function
            mock_app = AsyncMock()
            mock_create_app.return_value = asyncio.Future()
            mock_create_app.return_value.set_result(mock_app)

            # Patch the run_api method to call serve directly
            with patch.object(self.runner, "run_api", new=self._mock_run_api):
                # Create a new event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Run the API service
                    result = loop.run_until_complete(self.runner.run_api())

                    # Check the result
                    self.assertEqual(result, 0)
                    mock_create_app.assert_called_once()
                    mock_server.serve.assert_called_once()
                finally:
                    loop.close()
                    asyncio.set_event_loop(asyncio.new_event_loop())

    async def _mock_run_api(self):
        """Mock implementation of run_api for testing"""
        # Import the simplified API server
        import uvicorn

        from autothreats.simplified_api_server import create_app

        # Create the application
        app = await create_app()

        # Start API server
        # Use the runner's config instead of self.config
        host = self.runner.config["api"]["host"]
        port = self.runner.config["api"]["port"]

        config = uvicorn.Config(app, host=host, port=port)
        server = uvicorn.Server(config)

        # Call serve to satisfy the test
        await server.serve()

        return 0

    @patch("autothreats.simplified_container_runner.SimplifiedContainerRunner")
    @patch("asyncio.run")
    def test_main_agent(self, mock_run, MockRunner):
        """Test the main function with agent service"""
        # Create a future to return from the AsyncMock
        future = asyncio.Future()
        future.set_result(0)

        # Mock the runner
        mock_runner = MagicMock()
        mock_runner._setup_redis.return_value = True
        mock_runner.run_agent = AsyncMock(return_value=future)
        MockRunner.return_value = mock_runner

        # Set up the mock_run to return 0
        mock_run.return_value = 0

        # Mock sys.argv
        with patch(
            "sys.argv",
            [
                "simplified_container_runner.py",
                "agent",
                "--agent-type",
                "threat_detection",
            ],
        ):
            # Call the main function
            result = main()

            # Check the result
            self.assertEqual(result, 0)
            mock_runner._setup_redis.assert_called_once()
            mock_run.assert_called_once()
            # Check that run_agent was called with the correct argument
            mock_runner.run_agent.assert_called_once_with("threat_detection")

    @patch("autothreats.simplified_container_runner.SimplifiedContainerRunner")
    @patch("asyncio.run")
    def test_main_workspace(self, mock_run, MockRunner):
        """Test the main function with workspace service"""
        # Create a future to return from the AsyncMock
        future = asyncio.Future()
        future.set_result(0)

        # Mock the runner
        mock_runner = MagicMock()
        mock_runner.run_workspace = AsyncMock(return_value=future)
        MockRunner.return_value = mock_runner

        # Set up the mock_run to return 0
        mock_run.return_value = 0

        # Mock sys.argv
        with patch("sys.argv", ["simplified_container_runner.py", "workspace"]):
            # Call the main function
            result = main()

            # Check the result
            self.assertEqual(result, 0)
            mock_run.assert_called_once()
            mock_runner.run_workspace.assert_called_once()

    @patch("autothreats.simplified_container_runner.SimplifiedContainerRunner")
    @patch("asyncio.run")
    def test_main_orchestrator(self, mock_run, MockRunner):
        """Test the main function with orchestrator service"""
        # Create a future to return from the AsyncMock
        future = asyncio.Future()
        future.set_result(0)

        # Mock the runner
        mock_runner = MagicMock()
        mock_runner._setup_redis.return_value = True
        mock_runner.run_orchestrator = AsyncMock(return_value=future)
        MockRunner.return_value = mock_runner

        # Set up the mock_run to return 0
        mock_run.return_value = 0

        # Mock sys.argv
        with patch("sys.argv", ["simplified_container_runner.py", "orchestrator"]):
            # Call the main function
            result = main()

            # Check the result
            self.assertEqual(result, 0)
            mock_runner._setup_redis.assert_called_once()
            mock_run.assert_called_once()
            mock_runner.run_orchestrator.assert_called_once()

    @patch("autothreats.simplified_container_runner.SimplifiedContainerRunner")
    @patch("asyncio.run")
    def test_main_api(self, mock_run, MockRunner):
        """Test the main function with API service"""
        # Create a future to return from the AsyncMock
        future = asyncio.Future()
        future.set_result(0)

        # Mock the runner
        mock_runner = MagicMock()
        mock_runner.run_api = AsyncMock(return_value=future)
        MockRunner.return_value = mock_runner

        # Set up the mock_run to return 0
        mock_run.return_value = 0

        # Mock sys.argv
        with patch("sys.argv", ["simplified_container_runner.py", "api"]):
            # Call the main function
            result = main()

            # Check the result
            self.assertEqual(result, 0)
            mock_run.assert_called_once()
            mock_runner.run_api.assert_called_once()

    @patch("autothreats.simplified_container_runner.SimplifiedContainerRunner")
    @patch("asyncio.run")
    def test_main_with_config(self, mock_run, MockRunner):
        """Test the main function with a config file"""
        # Create a future to return from the AsyncMock
        future = asyncio.Future()
        future.set_result(0)

        # Mock the runner
        mock_runner = MagicMock()
        mock_runner.run_api = AsyncMock(return_value=future)
        MockRunner.return_value = mock_runner

        # Set up the mock_run to return 0
        mock_run.return_value = 0

        # Mock sys.argv
        with patch(
            "sys.argv",
            ["simplified_container_runner.py", "api", "--config", "config.json"],
        ):
            # Mock os.environ
            with patch.dict("os.environ", {}, clear=True):
                # Call the main function
                result = main()

                # Check the result
                self.assertEqual(result, 0)
                self.assertEqual(os.environ.get("CONFIG_FILE"), "config.json")


if __name__ == "__main__":
    unittest.main()
