#!/usr/bin/env python3
"""
Tests for the simplified orchestrator component.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import SharedWorkspace
from autothreats.simplified_orchestrator import SimplifiedOrchestrator, run_orchestrator


class TestSimplifiedOrchestrator(unittest.TestCase):
    """Test the SimplifiedOrchestrator class"""

    def setUp(self):
        """Set up the test"""
        self.config = {
            "log_level": "INFO",
            "threat_detection": {
                "llm_provider": "openai",
                "openai_api_key": "test_key",
                "mock_mode": True,
            },
            "enable_multi_stage": False,
            "enable_agentic": True,
            "system": {
                "debug_logging": False,
                "lightweight": False,
                "max_scan_dirs": 100,
            },
        }

        # Create a mock workspace
        self.mock_workspace = MagicMock(spec=SharedWorkspace)
        self.mock_workspace.register_agent = MagicMock()
        self.mock_workspace.store_data = MagicMock()
        self.mock_workspace.start = AsyncMock()
        self.mock_workspace.stop = AsyncMock()
        self.mock_workspace.process_agent_task = AsyncMock(
            return_value={"status": "success"}
        )

        # Patch the SharedWorkspace class
        self.workspace_patcher = patch(
            "autothreats.simplified_orchestrator.SharedWorkspace",
            return_value=self.mock_workspace,
        )
        self.mock_workspace_class = self.workspace_patcher.start()

        # Create the orchestrator
        self.orchestrator = SimplifiedOrchestrator(self.config)

    def tearDown(self):
        """Clean up after the test"""
        self.workspace_patcher.stop()

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.orchestrator.config, self.config)
        self.assertIsNotNone(self.orchestrator.logger)
        self.assertIsNone(self.orchestrator.workspace)
        self.assertEqual(self.orchestrator.agents, {})
        self.assertFalse(self.orchestrator.running)
        self.assertIn("workspace_id", self.orchestrator.__dict__)

    def test_initialize(self):
        """Test initializing the orchestrator"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the orchestrator
            loop.run_until_complete(self.orchestrator.initialize())

            # Check that the workspace was created and started
            self.mock_workspace_class.assert_called_once_with(
                self.orchestrator.workspace_id
            )
            self.assertEqual(self.orchestrator.workspace, self.mock_workspace)
            self.mock_workspace.start.assert_called_once()

            # Check that the orchestrator is running
            self.assertTrue(self.orchestrator.running)
        finally:
            loop.close()

    @patch("autothreats.simplified_orchestrator.SimplifiedThreatDetectionAgent")
    def test_create_agents(self, mock_agent_class):
        """Test creating agents"""
        # Create a mock agent
        mock_agent = MagicMock()
        mock_agent.id = "threat_detection_agent"
        mock_agent.initialize = AsyncMock()
        mock_agent_class.return_value = mock_agent

        # Reset the mock to clear any previous calls
        mock_agent_class.reset_mock()

        # Set up the orchestrator with a workspace but don't call initialize()
        self.orchestrator.workspace = self.mock_workspace

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Call _create_agents directly
            loop.run_until_complete(self.orchestrator._create_agents())

            # Check that the agent was created and registered
            mock_agent_class.assert_called_once_with(
                agent_id="threat_detection_agent",
                config=self.config.get("threat_detection", {}),
            )
            self.mock_workspace.register_agent.assert_called_once_with(mock_agent)
            self.assertIn("threat_detection", self.orchestrator.agents)
            self.assertEqual(self.orchestrator.agents["threat_detection"], mock_agent)

            # Check that the agent was initialized
            mock_agent.initialize.assert_called_once()
        finally:
            loop.close()

    @patch("autothreats.simplified_orchestrator.SimplifiedContextAwareSecurity")
    @patch("autothreats.simplified_orchestrator.SimplifiedAdaptivePrioritization")
    @patch("autothreats.simplified_orchestrator.SimplifiedHierarchicalAnalysis")
    @patch("autothreats.simplified_orchestrator.SimplifiedExplainableSecurity")
    def test_initialize_agentic_components(
        self, mock_explainable, mock_hierarchical, mock_adaptive, mock_context
    ):
        """Test initializing agentic components"""
        # Create mock components
        mock_context_instance = MagicMock()
        mock_adaptive_instance = MagicMock()
        mock_hierarchical_instance = MagicMock()
        mock_explainable_instance = MagicMock()

        # Reset all mocks to clear any previous calls
        mock_context.reset_mock()
        mock_adaptive.reset_mock()
        mock_hierarchical.reset_mock()
        mock_explainable.reset_mock()

        mock_context.return_value = mock_context_instance
        mock_adaptive.return_value = mock_adaptive_instance
        mock_hierarchical.return_value = mock_hierarchical_instance
        mock_explainable.return_value = mock_explainable_instance

        # Set up the orchestrator with a workspace but don't call initialize()
        self.orchestrator.workspace = self.mock_workspace

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Call _initialize_agentic_components directly
            loop.run_until_complete(self.orchestrator._initialize_agentic_components())

            # Check that the components were created
            mock_context.assert_called_once_with(self.mock_workspace)
            mock_adaptive.assert_called_once_with(self.mock_workspace)
            mock_hierarchical.assert_called_once_with(self.mock_workspace)
            mock_explainable.assert_called_once_with(self.mock_workspace)

            # Check that the components were stored in the workspace
            self.mock_workspace.store_data.assert_any_call(
                "context_aware_security", mock_context_instance
            )
            self.mock_workspace.store_data.assert_any_call(
                "adaptive_prioritization", mock_adaptive_instance
            )
            self.mock_workspace.store_data.assert_any_call(
                "hierarchical_analysis", mock_hierarchical_instance
            )
            self.mock_workspace.store_data.assert_any_call(
                "explainable_security", mock_explainable_instance
            )
        finally:
            loop.close()

    def test_shutdown(self):
        """Test shutting down the orchestrator"""
        # Set up the orchestrator
        self.orchestrator.workspace = self.mock_workspace
        self.orchestrator.running = True

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Shutdown the orchestrator
            loop.run_until_complete(self.orchestrator.shutdown())

            # Check that the workspace was stopped
            self.mock_workspace.stop.assert_called_once()

            # Check that the orchestrator is not running
            self.assertFalse(self.orchestrator.running)
        finally:
            loop.close()

    def test_process_job(self):
        """Test processing a job"""
        # Set up the orchestrator
        self.orchestrator.workspace = self.mock_workspace
        self.orchestrator.running = True

        # Create a job
        job_data = {
            "job_id": "test_job",
            "codebase_id": "test_codebase",
            "codebase": {"files": {"test.py": "print('Hello, world!')"}},
            "context": {
                "lightweight": False,
                "enable_multi_stage": False,
                "enable_redflag": False,
                "enable_codeshield": False,
                "enable_agentic": True,
            },
        }

        # Mock the _post_process_vulnerabilities method
        self.orchestrator._post_process_vulnerabilities = AsyncMock(
            return_value=[{"id": "vuln1"}]
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Process the job
            result = loop.run_until_complete(self.orchestrator.process_job(job_data))

            # Check that the workspace.process_agent_task was called
            self.mock_workspace.process_agent_task.assert_called_once_with(
                agent_id="threat_detection_agent",
                task_type="threat_detection",
                task_data=job_data,
            )

            # Check that _post_process_vulnerabilities was called
            self.orchestrator._post_process_vulnerabilities.assert_called_once()

            # Check the result
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["job_id"], "test_job")
            self.assertIn("results", result)
            self.assertIn("threat_detection", result["results"])
        finally:
            loop.close()

    def test_process_job_not_running(self):
        """Test processing a job when the orchestrator is not running"""
        # Set up the orchestrator
        self.orchestrator.running = False

        # Create a job
        job_data = {
            "job_id": "test_job",
            "codebase_id": "test_codebase",
            "codebase": {"files": {"test.py": "print('Hello, world!')"}},
        }

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Process the job and expect an exception
            with self.assertRaises(RuntimeError):
                loop.run_until_complete(self.orchestrator.process_job(job_data))
        finally:
            loop.close()

    @patch("autothreats.simplified_orchestrator.SimplifiedContextAwareSecurity")
    @patch("autothreats.simplified_orchestrator.SimplifiedAdaptivePrioritization")
    @patch("autothreats.simplified_orchestrator.SimplifiedExplainableSecurity")
    def test_post_process_vulnerabilities(
        self, mock_explainable, mock_adaptive, mock_context
    ):
        """Test post-processing vulnerabilities"""
        # Set up the orchestrator
        self.orchestrator.workspace = self.mock_workspace

        # Create mock components
        mock_context_instance = MagicMock()
        mock_context_instance.analyze_security_context = AsyncMock(
            return_value={"security_boundaries": []}
        )
        mock_context_instance.enhance_vulnerability_detection = AsyncMock(
            return_value=[{"id": "vuln1", "enhanced": True}]
        )

        mock_adaptive_instance = MagicMock()
        mock_adaptive_instance.prioritize_vulnerabilities = AsyncMock(
            return_value=[{"id": "vuln1", "enhanced": True, "prioritized": True}]
        )

        mock_explainable_instance = MagicMock()
        mock_explainable_instance.explain_vulnerabilities = AsyncMock(
            return_value=[
                {
                    "id": "vuln1",
                    "enhanced": True,
                    "prioritized": True,
                    "explained": True,
                }
            ]
        )

        # Mock workspace.get_data to return the components
        self.mock_workspace.get_data.side_effect = lambda key: {
            "context_aware_security": mock_context_instance,
            "adaptive_prioritization": mock_adaptive_instance,
            "explainable_security": mock_explainable_instance,
        }.get(key)

        # Create vulnerabilities
        vulnerabilities = [{"id": "vuln1"}]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Post-process the vulnerabilities
            result = loop.run_until_complete(
                self.orchestrator._post_process_vulnerabilities(
                    vulnerabilities, "test_job", "test_codebase"
                )
            )

            # Check that the components were used
            mock_context_instance.analyze_security_context.assert_called_once()
            mock_context_instance.enhance_vulnerability_detection.assert_called_once()
            mock_adaptive_instance.prioritize_vulnerabilities.assert_called_once()
            mock_explainable_instance.explain_vulnerabilities.assert_called_once()

            # Check the result
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["id"], "vuln1")
            self.assertTrue(result[0]["enhanced"])
            self.assertTrue(result[0]["prioritized"])
            self.assertTrue(result[0]["explained"])
        finally:
            loop.close()

    def test_detect_threats(self):
        """Test detecting threats"""
        # Set up the orchestrator
        self.orchestrator.workspace = self.mock_workspace
        self.orchestrator.running = True

        # Create a job
        job_data = {
            "job_id": "test_job",
            "codebase_id": "test_codebase",
            "codebase": {"files": {"test.py": "print('Hello, world!')"}},
        }

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Detect threats
            result = loop.run_until_complete(self.orchestrator.detect_threats(job_data))

            # Check that the workspace.process_agent_task was called
            self.mock_workspace.process_agent_task.assert_called_once_with(
                agent_id="threat_detection_agent",
                task_type="threat_detection",
                task_data=job_data,
            )

            # Check the result
            self.assertEqual(result["status"], "success")
        finally:
            loop.close()


class TestRunOrchestrator(unittest.TestCase):
    """Test the run_orchestrator function"""

    @patch("autothreats.simplified_orchestrator.SimplifiedOrchestrator")
    def test_run_orchestrator(self, mock_orchestrator_class):
        """Test running the orchestrator"""
        # Create mock orchestrator
        mock_orchestrator = MagicMock()
        mock_orchestrator.initialize = AsyncMock()
        mock_orchestrator.process_job = AsyncMock(return_value={"status": "success"})
        mock_orchestrator.shutdown = AsyncMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        # Create config and job data
        config = {"key": "value"}
        job_data = {"job_id": "test_job"}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Run the orchestrator
            result = loop.run_until_complete(run_orchestrator(config, job_data))

            # Check that the orchestrator was created and used
            mock_orchestrator_class.assert_called_once_with(config)
            mock_orchestrator.initialize.assert_called_once()
            mock_orchestrator.process_job.assert_called_once_with(job_data)
            mock_orchestrator.shutdown.assert_called_once()

            # Check the result
            self.assertEqual(result["status"], "success")
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
