#!/usr/bin/env python3
"""
Integration tests for orchestrator lifecycle.
Tests initialization, shutdown, and recovery scenarios.
"""

import os
import sys
import unittest
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.simplified_base import SharedWorkspace
from autothreats.simplified_orchestrator import SimplifiedOrchestrator
from tests.async_test_base import AsyncTestCase, async_test


class TestOrchestratorLifecycle(AsyncTestCase):
    """Integration tests for orchestrator lifecycle"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a mock config
        self.config = {
            "system": {
                "enable_agentic_improvements": True,
                "debug_logging": False,
                "lightweight": False,
                "max_scan_dirs": 100,
            },
            "llm": {
                "provider": "openai",
                "mock_mode": True,  # Use mock mode for testing
            },
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Sample codebase
        self.codebase = {
            "files": {
                "test.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n",
                "app.py": "from flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route('/query')\ndef query():\n    user_input = request.args.get('q')\n    # SQL injection vulnerability\n    query = f\"SELECT * FROM users WHERE name = '{user_input}'\"\n    return query\n",
            }
        }

    async def asyncTearDown(self):
        """Clean up after the test"""
        pass

    #
    # POSITIVE TESTS FOR ORCHESTRATOR LIFECYCLE
    #

    @async_test
    async def test_orchestrator_initialization(self):
        """Test successful orchestrator initialization"""
        # Create an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)

        # Initialize the orchestrator
        await orchestrator.initialize()

        # Verify orchestrator is initialized
        self.assertTrue(
            orchestrator.running, "Orchestrator should be running after initialization"
        )
        self.assertIsNotNone(
            orchestrator.workspace, "Workspace should be created during initialization"
        )
        self.assertTrue(
            orchestrator.workspace.is_ready(),
            "Workspace should be ready after initialization",
        )

        # Verify agents are created
        self.assertGreater(
            len(orchestrator.agents),
            0,
            "Agents should be created during initialization",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    @async_test
    async def test_orchestrator_shutdown(self):
        """Test successful orchestrator shutdown"""
        # Create and initialize an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)
        await orchestrator.initialize()

        # Shutdown the orchestrator
        await orchestrator.shutdown()

        # Verify orchestrator is shut down
        self.assertFalse(
            orchestrator.running, "Orchestrator should not be running after shutdown"
        )

        # Verify workspace is shut down
        self.assertFalse(
            orchestrator.workspace.is_ready(),
            "Workspace should not be ready after shutdown",
        )

    @async_test
    async def test_orchestrator_restart(self):
        """Test orchestrator restart after shutdown"""
        # Create and initialize an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)
        await orchestrator.initialize()

        # Store the agent count
        initial_agent_count = len(orchestrator.agents)

        # Shutdown the orchestrator
        await orchestrator.shutdown()

        # Restart the orchestrator
        await orchestrator.initialize()

        # Verify orchestrator is running again
        self.assertTrue(
            orchestrator.running, "Orchestrator should be running after restart"
        )
        self.assertTrue(
            orchestrator.workspace.is_ready(), "Workspace should be ready after restart"
        )

        # Verify agents are recreated
        self.assertEqual(
            len(orchestrator.agents),
            initial_agent_count,
            "Same number of agents should be created during restart",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    @async_test
    async def test_orchestrator_with_custom_workspace_id(self):
        """Test orchestrator with a custom workspace ID"""
        # Create a custom workspace ID
        custom_workspace_id = "custom_workspace_id"

        # Create an orchestrator with the custom workspace ID
        custom_config = self.config.copy()
        custom_config["workspace_id"] = custom_workspace_id
        orchestrator = SimplifiedOrchestrator(config=custom_config)

        # Initialize the orchestrator
        await orchestrator.initialize()

        # Verify orchestrator is using the custom workspace ID
        self.assertEqual(
            orchestrator.workspace_id,
            custom_workspace_id,
            "Orchestrator should use the provided custom workspace ID",
        )
        self.assertEqual(
            orchestrator.workspace.model.id,
            custom_workspace_id,
            "Workspace should have the custom ID",
        )

        # Store some data in the workspace
        orchestrator.workspace.store_data("test_key", "test_value")

        # Verify the data in the workspace is accessible
        self.assertEqual(
            orchestrator.workspace.get_data("test_key"),
            "test_value",
            "Data in workspace should be accessible",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    @async_test
    async def test_orchestrator_process_job_after_initialization(self):
        """Test processing a job after orchestrator initialization"""
        # Create and initialize an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)
        await orchestrator.initialize()

        # Create job data
        job_data = {
            "job_id": "test_job",
            "codebase_id": "test_codebase",
            "codebase": self.codebase,
        }

        # Process the job
        result = await orchestrator.process_job(job_data)

        # Verify job was processed successfully
        self.assertEqual(
            result["status"],
            "success",
            f"Job processing failed: {result.get('message', '')}",
        )
        self.assertIn("results", result, "No results in result")

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    #
    # NEGATIVE TESTS FOR ORCHESTRATOR LIFECYCLE
    #

    @async_test
    async def test_orchestrator_process_job_without_initialization(self):
        """Test processing a job without initializing the orchestrator"""
        # Create an orchestrator but don't initialize it
        orchestrator = SimplifiedOrchestrator(config=self.config)

        # Create job data
        job_data = {
            "job_id": "test_job",
            "codebase_id": "test_codebase",
            "codebase": self.codebase,
        }

        # Try to process the job without initialization
        with self.assertRaises(RuntimeError) as context:
            await orchestrator.process_job(job_data)

        # Verify appropriate error was raised
        self.assertIn(
            "not running",
            str(context.exception).lower(),
            "Error should mention orchestrator not running",
        )

    @async_test
    async def test_orchestrator_double_initialization(self):
        """Test initializing an orchestrator twice"""
        # Create an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)

        # Initialize the orchestrator
        await orchestrator.initialize()

        # Try to initialize again
        # This should not raise an exception, but should be a no-op
        await orchestrator.initialize()

        # Verify orchestrator is still running
        self.assertTrue(
            orchestrator.running,
            "Orchestrator should still be running after double initialization",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    @async_test
    async def test_orchestrator_double_shutdown(self):
        """Test shutting down an orchestrator twice"""
        # Create and initialize an orchestrator
        orchestrator = SimplifiedOrchestrator(config=self.config)
        await orchestrator.initialize()

        # Shutdown the orchestrator
        await orchestrator.shutdown()

        # Try to shutdown again
        # This should not raise an exception, but should be a no-op
        await orchestrator.shutdown()

        # Verify orchestrator is still shut down
        self.assertFalse(
            orchestrator.running,
            "Orchestrator should still be shut down after double shutdown",
        )

    @async_test
    async def test_orchestrator_with_invalid_config(self):
        """Test orchestrator with invalid configuration"""
        # Create an orchestrator with invalid config
        invalid_config = {"invalid_key": "invalid_value"}
        orchestrator = SimplifiedOrchestrator(config=invalid_config)

        # Initialize the orchestrator (should use defaults for missing config)
        await orchestrator.initialize()

        # Verify orchestrator is initialized with defaults
        self.assertTrue(
            orchestrator.running,
            "Orchestrator should be running with default configuration",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()

    @async_test
    async def test_orchestrator_with_missing_config(self):
        """Test orchestrator with missing configuration"""
        # Create an orchestrator with no config
        orchestrator = SimplifiedOrchestrator()

        # Initialize the orchestrator (should use defaults)
        await orchestrator.initialize()

        # Verify orchestrator is initialized with defaults
        self.assertTrue(
            orchestrator.running,
            "Orchestrator should be running with default configuration",
        )

        # Shutdown the orchestrator
        await orchestrator.shutdown()


if __name__ == "__main__":
    unittest.main()
