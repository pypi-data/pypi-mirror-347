#!/usr/bin/env python3
"""
Integration tests for agent integration and orchestration.
Tests the interaction between multiple agents in the system.
"""

import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.agentic.agent_integration import (
    initialize_agentic_agents,
    register_agentic_agents,
)
from autothreats.simplified_base import SharedWorkspace
from autothreats.simplified_orchestrator import SimplifiedOrchestrator
from tests.async_test_base import AsyncTestCase, async_test


class TestAgentIntegration(AsyncTestCase):
    """Integration tests for agent integration"""

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
            "enable_redflag": False,
            "enable_codeshield": False,
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Create a workspace
        self.workspace = SharedWorkspace(f"test_workspace")
        await self.workspace.start()

        # Store the config in the workspace
        self.workspace.store_data("system_config", self.config["system"])

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_register_agentic_agents(self):
        """Test registering agentic agents"""
        # Register agentic agents
        agents = register_agentic_agents(self.workspace, self.config)

        # Verify agents were registered
        self.assertGreater(len(agents), 0, "No agentic agents were registered")

        # Verify agent types
        agent_types = [agent.model.agent_type for agent in agents]
        self.assertIn("code_graph", agent_types, "Code graph agent not registered")
        self.assertIn(
            "threat_detection", agent_types, "Threat detection agent not registered"
        )

        # Initialize agents
        await initialize_agentic_agents(agents)

        # Verify agents were initialized
        for agent in agents:
            self.assertIsNotNone(agent.workspace, "Agent workspace not set")


class TestOrchestratorIntegration(AsyncTestCase):
    """Integration tests for the orchestrator"""

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
            "enable_redflag": False,
            "enable_codeshield": False,
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Create a sample codebase
        self.codebase = {
            "files": {
                "test.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n",
                "app.py": "from flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route('/query')\ndef query():\n    user_input = request.args.get('q')\n    # SQL injection vulnerability\n    query = f\"SELECT * FROM users WHERE name = '{user_input}'\"\n    return query\n",
            }
        }

        # Create job data
        self.job_id = "test_job_123"
        self.job_data = {
            "job_id": self.job_id,
            "codebase_id": f"codebase_{self.job_id}",
            "codebase": self.codebase,
            "context": {"lightweight": False, "enable_multi_stage": False},
        }

        # Create orchestrator
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "orchestrator") and self.orchestrator:
            await self.orchestrator.shutdown()

    @async_test
    async def test_orchestrator_process_job(self):
        """Test processing a job through the orchestrator"""
        # Process the job
        result = await self.orchestrator.process_job(self.job_data)

        # Verify the result
        self.assertEqual(
            result["status"],
            "success",
            f"Job processing failed: {result.get('message', '')}",
        )
        self.assertEqual(result["job_id"], self.job_id, "Job ID mismatch")

        # Verify threat detection results
        self.assertIn("results", result, "No results in job result")
        self.assertIn(
            "threat_detection", result["results"], "No threat detection results"
        )

        # Verify vulnerabilities were found
        threat_detection = result["results"]["threat_detection"]
        self.assertIn(
            "vulnerabilities",
            threat_detection,
            "No vulnerabilities in threat detection results",
        )

        # In mock mode, we should still get some vulnerabilities
        vulnerabilities = threat_detection["vulnerabilities"]
        self.assertGreater(len(vulnerabilities), 0, "No vulnerabilities found")


class TestAgenticEnhancementIntegration(AsyncTestCase):
    """Integration tests for agentic enhancements"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a mock config with agentic improvements enabled
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
            "enable_redflag": False,
            "enable_codeshield": False,
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Create a sample codebase
        self.codebase = {
            "files": {
                "test.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n",
                "app.py": "from flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route('/query')\ndef query():\n    user_input = request.args.get('q')\n    # SQL injection vulnerability\n    query = f\"SELECT * FROM users WHERE name = '{user_input}'\"\n    return query\n",
            }
        }

        # Create job data
        self.job_id = "test_job_456"
        self.job_data = {
            "job_id": self.job_id,
            "codebase_id": f"codebase_{self.job_id}",
            "codebase": self.codebase,
            "context": {
                "lightweight": False,
                "enable_multi_stage": False,
                "enable_agentic": True,
            },
        }

        # Create orchestrator with agentic improvements
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "orchestrator") and self.orchestrator:
            await self.orchestrator.shutdown()

    @async_test
    async def test_agentic_post_processing(self):
        """Test agentic post-processing of vulnerabilities"""
        # Process the job
        result = await self.orchestrator.process_job(self.job_data)

        # Verify the result
        self.assertEqual(
            result["status"],
            "success",
            f"Job processing failed: {result.get('message', '')}",
        )

        # Verify vulnerabilities were found and processed
        vulnerabilities = result["results"]["threat_detection"]["vulnerabilities"]
        self.assertGreater(len(vulnerabilities), 0, "No vulnerabilities found")

        # Check for agentic enhancements in at least some vulnerabilities
        # These might include: priority, detailed_explanation, or in_security_boundary
        agentic_enhancements = False
        for vuln in vulnerabilities:
            if any(
                key in vuln
                for key in ["priority", "detailed_explanation", "in_security_boundary"]
            ):
                agentic_enhancements = True
                break

        self.assertTrue(
            agentic_enhancements, "No agentic enhancements found in vulnerabilities"
        )


if __name__ == "__main__":
    unittest.main()
