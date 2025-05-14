#!/usr/bin/env python3
"""
Integration tests for simplified agents and workspace interactions.
Tests how simplified agents interact with the workspace and how the workspace manages simplified agents.
"""

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
from autothreats.simplified_base import Agent, SharedWorkspace
from tests.async_test_base import AsyncTestCase, async_test


class SimplifiedTestAgent(Agent):
    """Simple test agent for testing workspace integration"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "test_agent", config)
        self.test_data = {}

    async def initialize(self):
        """Initialize the agent"""
        self.logger.info(f"Initializing agent {self.id}")
        self.test_data["initialized"] = True
        # Set status to initialized
        self.model.update_state("status", "initialized")

    async def shutdown(self):
        """Clean up resources when shutting down"""
        self.logger.info(f"Shutting down agent {self.id}")
        self.test_data["shutdown"] = True

    async def _process_task_impl(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a task and return a result"""
        self.logger.info(f"Processing task of type {task_type}")

        if task_type == "test_task":
            # Store data in workspace if available
            if self.workspace and task_data.get("store_in_workspace"):
                key = task_data.get("key", "test_result")
                value = task_data.get("value", {"status": "success"})
                self.workspace.store_data(key, value)

            # Retrieve data from workspace if requested
            if self.workspace and task_data.get("retrieve_from_workspace"):
                key = task_data.get("retrieve_key", "test_data")
                retrieved_data = self.workspace.get_data(key)
                return {
                    "status": "success",
                    "retrieved_data": retrieved_data,
                    "message": f"Retrieved data for key: {key}",
                }

            return {
                "status": "success",
                "message": "Test task processed successfully",
                "task_data": task_data,
            }
        else:
            return {
                "status": "error",
                "message": f"Unsupported task type: {task_type}",
                "details": "This agent only supports 'test_task' tasks",
            }


class TestSimplifiedAgentWorkspaceIntegration(AsyncTestCase):
    """Integration tests for simplified agents and workspace interactions"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a mock config
        self.config = {
            "system": {
                "enable_agentic_improvements": False,  # Disable agentic improvements for simplified agent tests
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

        # Create a workspace
        self.workspace = SharedWorkspace(f"test_simplified_workspace")
        await self.workspace.start()

        # Store the config in the workspace
        self.workspace.store_data("system_config", self.config["system"])

        # Sample codebase
        self.codebase = {
            "files": {
                "test.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n",
                "app.py": "from flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route('/query')\ndef query():\n    user_input = request.args.get('q')\n    # SQL injection vulnerability\n    query = f\"SELECT * FROM users WHERE name = '{user_input}'\"\n    return query\n",
            }
        }

        # Store codebase in workspace
        self.workspace.store_data("codebase_test_codebase", self.codebase)

    async def asyncTearDown(self):
        """Clean up after the test"""
        if self.workspace:
            await self.workspace.stop()

    @async_test
    async def test_simplified_agent_registration_with_workspace(self):
        """Test simplified agent registration with workspace"""
        # Create a simplified agent
        agent = SimplifiedTestAgent("test_simplified_agent", self.config)

        # Register with workspace
        self.workspace.register_agent(agent)

        # Verify agent is registered
        self.assertIn(
            agent.id, self.workspace.agents, "Agent not registered with workspace"
        )
        self.assertEqual(
            agent.workspace, self.workspace, "Agent workspace not set correctly"
        )

        # Verify agent can access workspace data
        system_config = agent.workspace.get_data("system_config")
        self.assertIsNotNone(system_config, "Agent cannot access workspace data")
        self.assertEqual(
            system_config,
            self.config["system"],
            "Agent retrieved incorrect workspace data",
        )

    @async_test
    async def test_simplified_agent_accessing_workspace_data(self):
        """Test simplified agent accessing data from workspace"""
        # Create and initialize agent
        agent = SimplifiedTestAgent("test_simplified_agent", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Store data in workspace
        test_data = {"key": "value", "nested": {"inner": "data"}}
        self.workspace.store_data("test_data", test_data)

        # Process task that retrieves data from workspace
        task_data = {"retrieve_from_workspace": True, "retrieve_key": "test_data"}

        result = await agent.process_task("test_task", task_data)

        # Verify agent retrieved the data correctly
        self.assertEqual(result["status"], "success", "Task processing failed")
        self.assertIn("retrieved_data", result, "No retrieved data in result")
        self.assertEqual(
            result["retrieved_data"],
            test_data,
            "Agent retrieved incorrect data from workspace",
        )

        # Shutdown agent
        await agent.shutdown()

    @async_test
    async def test_simplified_agent_storing_data_in_workspace(self):
        """Test simplified agent storing data in workspace"""
        # Create and initialize agent
        agent = SimplifiedTestAgent("test_simplified_agent", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Process task that stores data in workspace
        task_data = {
            "store_in_workspace": True,
            "key": "agent_result",
            "value": {"test": "data", "numbers": [1, 2, 3]},
        }

        result = await agent.process_task("test_task", task_data)

        # Verify task was processed successfully
        self.assertEqual(result["status"], "success", "Task processing failed")

        # Verify data was stored in workspace
        stored_data = self.workspace.get_data("agent_result")
        self.assertIsNotNone(stored_data, "Data not stored in workspace")
        self.assertEqual(
            stored_data, task_data["value"], "Data not stored correctly in workspace"
        )

        # Shutdown agent
        await agent.shutdown()

    @async_test
    async def test_simplified_threat_detection_agent_with_workspace(self):
        """Test SimplifiedThreatDetectionAgent integration with workspace"""
        # Create and initialize agent
        agent = SimplifiedThreatDetectionAgent("test_threat_detection", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Create a mock codebase and store it in the workspace
        codebase_id = "test_codebase"
        mock_codebase = {
            "files": {
                "test.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n"
            }
        }
        self.workspace.store_data(codebase_id, mock_codebase)

        # Create task data with reference to workspace data
        task_data = {
            "job_id": "test_job",
            "codebase_id": codebase_id,  # This should be retrieved from workspace
        }

        # Process task
        result = await agent.process_task("threat_detection", task_data)

        # Verify task was processed successfully
        self.assertEqual(
            result["status"],
            "success",
            f"Task processing failed: {result.get('message', '')}",
        )
        self.assertIn("vulnerabilities", result, "No vulnerabilities in result")

        # Verify codebase was retrieved from workspace
        self.assertEqual(
            result["codebase_id"], "test_codebase", "Incorrect codebase ID in result"
        )

        # Shutdown agent
        await agent.shutdown()

    @async_test
    async def test_multiple_simplified_agents_sharing_workspace(self):
        """Test multiple simplified agents sharing the same workspace"""
        # Create multiple agents
        agent1 = SimplifiedTestAgent("test_agent_1", self.config)
        agent2 = SimplifiedTestAgent("test_agent_2", self.config)
        agent3 = SimplifiedThreatDetectionAgent("test_threat_detection", self.config)

        # Register all agents with the same workspace
        self.workspace.register_agent(agent1)
        self.workspace.register_agent(agent2)
        self.workspace.register_agent(agent3)

        # Initialize all agents
        await agent1.initialize()
        await agent2.initialize()
        await agent3.initialize()

        # Verify all agents are registered
        self.assertEqual(len(self.workspace.agents), 3, "Not all agents registered")
        self.assertIn(agent1.id, self.workspace.agents)
        self.assertIn(agent2.id, self.workspace.agents)
        self.assertIn(agent3.id, self.workspace.agents)

        # Verify all agents have the same workspace
        self.assertEqual(agent1.workspace, self.workspace)
        self.assertEqual(agent2.workspace, self.workspace)
        self.assertEqual(agent3.workspace, self.workspace)

        # Have agent1 store data in workspace
        await agent1.process_task(
            "test_task",
            {
                "store_in_workspace": True,
                "key": "agent1_data",
                "value": {"source": "agent1", "data": "test"},
            },
        )

        # Have agent2 retrieve the data
        result = await agent2.process_task(
            "test_task",
            {"retrieve_from_workspace": True, "retrieve_key": "agent1_data"},
        )

        # Verify agent2 retrieved the data correctly
        self.assertEqual(result["status"], "success", "Task processing failed")
        self.assertIn("retrieved_data", result, "No retrieved data in result")
        self.assertEqual(
            result["retrieved_data"]["source"],
            "agent1",
            "Agent retrieved incorrect data from workspace",
        )

        # Shutdown all agents
        await agent1.shutdown()
        await agent2.shutdown()
        await agent3.shutdown()

    @async_test
    async def test_workspace_data_sharing_between_simplified_agents(self):
        """Test data sharing between simplified agents through workspace"""
        # Create and initialize agents
        test_agent = SimplifiedTestAgent("test_agent", self.config)
        threat_detection_agent = SimplifiedThreatDetectionAgent(
            "threat_detection_agent", self.config
        )

        # Register agents with workspace
        self.workspace.register_agent(test_agent)
        self.workspace.register_agent(threat_detection_agent)

        # Initialize agents
        await test_agent.initialize()
        await threat_detection_agent.initialize()

        # Create a mock codebase and store it in the workspace
        codebase_id = "test_codebase"
        mock_codebase = {
            "files": {
                "app.py": "import os\n\ndef execute_command(cmd):\n    os.system(cmd)  # Potential OS command injection\n"
            }
        }
        self.workspace.store_data(codebase_id, mock_codebase)

        # Have test agent store data in workspace
        await test_agent.process_task(
            "test_task",
            {
                "store_in_workspace": True,
                "key": "vulnerability_data",
                "value": [
                    {
                        "vulnerability_type": "SQL Injection",
                        "cwe_id": "CWE-89",
                        "file_path": "app.py",
                        "line_numbers": [10],
                        "confidence": 0.8,
                        "severity": "high",
                    }
                ],
            },
        )

        # Have threat detection agent process a task that uses the data
        task_data = {
            "job_id": "test_job",
            "codebase_id": codebase_id,
            "vulnerabilities": self.workspace.get_data("vulnerability_data"),
        }

        result = await threat_detection_agent.process_task(
            "threat_detection", task_data
        )

        # Verify task was processed successfully
        self.assertEqual(
            result["status"],
            "success",
            f"Task processing failed: {result.get('message', '')}",
        )

        # Shutdown agents
        await test_agent.shutdown()
        await threat_detection_agent.shutdown()

    @async_test
    async def test_simplified_agent_with_nonexistent_codebase(self):
        """Test simplified agent behavior when codebase is not found in workspace"""
        # Create and initialize agent
        agent = SimplifiedThreatDetectionAgent("test_threat_detection", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Create task data with a non-existent codebase ID
        task_data = {
            "job_id": "test_job",
            "codebase_id": "nonexistent_codebase",  # This doesn't exist in workspace
        }

        # Process task
        result = await agent.process_task("threat_detection", task_data)

        # Verify task processing failed with appropriate error
        self.assertEqual(
            result["status"], "error", "Task should fail when codebase not found"
        )
        self.assertIn("message", result, "Error result should contain message")
        self.assertIn(
            "codebase",
            result.get("missing_parameters", []),
            "Missing parameters should include 'codebase'",
        )

        # Shutdown agent
        await agent.shutdown()

    @async_test
    async def test_simplified_agent_with_invalid_task_type(self):
        """Test simplified agent behavior with invalid task type"""
        # Create and initialize agent
        agent = SimplifiedThreatDetectionAgent("test_threat_detection", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Process task with invalid task type
        result = await agent.process_task("invalid_task_type", {"job_id": "test_job"})

        # Verify task processing failed with appropriate error
        self.assertEqual(
            result["status"], "error", "Task should fail with invalid task type"
        )
        self.assertIn("message", result, "Error result should contain message")
        self.assertIn(
            "Unsupported task type",
            result["message"],
            "Error message should mention unsupported task type",
        )

        # Shutdown agent
        await agent.shutdown()

    @async_test
    async def test_simplified_agent_with_missing_parameters(self):
        """Test simplified agent behavior with missing required parameters"""
        # Create and initialize agent
        agent = SimplifiedThreatDetectionAgent("test_threat_detection", self.config)
        self.workspace.register_agent(agent)
        await agent.initialize()

        # Process task with missing required parameters
        result = await agent.process_task(
            "threat_detection", {}
        )  # No job_id or codebase_id

        # Verify task processing failed with appropriate error
        self.assertEqual(
            result["status"], "error", "Task should fail with missing parameters"
        )
        self.assertIn("message", result, "Error result should contain message")
        self.assertIn(
            "Missing required parameters",
            result["message"],
            "Error message should mention missing parameters",
        )
        self.assertIn(
            "job_id",
            result.get("missing_parameters", []),
            "Missing parameters should include 'job_id'",
        )
        self.assertIn(
            "codebase_id",
            result.get("missing_parameters", []),
            "Missing parameters should include 'codebase_id'",
        )

        # Shutdown agent
        await agent.shutdown()


if __name__ == "__main__":
    unittest.main()
