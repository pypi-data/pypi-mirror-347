#!/usr/bin/env python3
"""
Tests for the simplified threat detection agent.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.agents.simplified_threat_detection import (
    SimplifiedThreatDetectionAgent,
)
from autothreats.models.codebase_model import CodebaseModel
from autothreats.simplified_base import SharedWorkspace


class TestSimplifiedThreatDetectionAgent(unittest.TestCase):
    """Test the SimplifiedThreatDetectionAgent class"""

    def setUp(self):
        """Set up the test"""
        self.config = {
            "llm_provider": "openai",
            "openai_api_key": "test_key",
            "mock_mode": True,
            "max_file_size": 1024 * 1024,
            "file_types": [".py", ".js"],
            "max_files": 100,
            "exclude_patterns": ["node_modules", "vendor"],
            "enable_redflag": False,
            "enable_codeshield": False,
        }

        # Create the agent
        self.agent = SimplifiedThreatDetectionAgent(
            "threat_detection_agent", self.config
        )

        # Create a mock workspace
        self.mock_workspace = MagicMock(spec=SharedWorkspace)
        self.mock_workspace.get_data = MagicMock(return_value=None)
        self.mock_workspace.store_data = MagicMock()

        # Register the agent with the workspace
        self.agent.register_with_workspace(self.mock_workspace)

        # Create a mock LLM service
        self.mock_llm_service = MagicMock()
        self.mock_llm_service.generate_text_async = AsyncMock(return_value="[]")

        # Create a mock RedFlag service
        self.mock_redflag_service = MagicMock()
        self.mock_redflag_service.is_available = MagicMock(return_value=True)
        self.mock_redflag_service.analyze_codebase = AsyncMock(return_value=[])

        # Create a mock CodeShield service
        self.mock_codeshield_service = MagicMock()
        self.mock_codeshield_service.is_available = MagicMock(return_value=True)
        self.mock_codeshield_service.analyze_codebase = AsyncMock(return_value=[])

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.agent.id, "threat_detection_agent")
        self.assertEqual(self.agent.model.agent_type, "threat_detection")
        self.assertEqual(self.agent.model.config, self.config)
        self.assertEqual(self.agent.max_file_size, self.config["max_file_size"])

        # Check that file_types is set from config
        self.assertEqual(self.agent.file_types, self.config["file_types"])

        self.assertEqual(self.agent.max_files, self.config["max_files"])
        self.assertEqual(self.agent.exclude_patterns, self.config["exclude_patterns"])

    def test_setup_config_schema(self):
        """Test setting up config schema"""
        # Check that the config schema was set up
        self.assertIn("openai_api_key", self.agent.model.optional_config)
        self.assertIn("anthropic_api_key", self.agent.model.optional_config)
        self.assertIn("llm_provider", self.agent.model.optional_config)
        self.assertIn("max_file_size", self.agent.model.optional_config)
        self.assertIn("file_types", self.agent.model.optional_config)
        self.assertIn("max_files", self.agent.model.optional_config)
        self.assertIn("exclude_patterns", self.agent.model.optional_config)
        self.assertIn("enable_redflag", self.agent.model.optional_config)
        self.assertIn("enable_codeshield", self.agent.model.optional_config)

        # Check default values
        self.assertEqual(self.agent.model.default_config["llm_provider"], "openai")
        self.assertEqual(self.agent.model.default_config["max_file_size"], 1024 * 1024)
        self.assertEqual(self.agent.model.default_config["max_files"], 1000)
        self.assertEqual(self.agent.model.default_config["enable_anthropic"], False)
        self.assertEqual(self.agent.model.default_config["mock_mode"], False)
        self.assertEqual(self.agent.model.default_config["enable_redflag"], False)
        self.assertEqual(self.agent.model.default_config["enable_codeshield"], False)

    @patch("autothreats.agents.simplified_threat_detection.LLMService")
    def test_initialize(self, mock_llm_service_class):
        """Test initializing the agent"""
        # Set up the mock LLM service
        mock_llm_service_class.return_value = self.mock_llm_service

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent
            loop.run_until_complete(self.agent.initialize())

            # Check that the LLM service was created
            mock_llm_service_class.assert_called_once()
            self.assertEqual(self.agent.llm_service, self.mock_llm_service)

            # Check that the agent state was updated
            self.assertEqual(self.agent.model.get_state("status"), "initialized")
        finally:
            loop.close()

    @patch("autothreats.agents.simplified_threat_detection.RedFlagService")
    def test_initialize_with_redflag(self, mock_redflag_service_class):
        """Test initializing the agent with RedFlag enabled"""
        # Enable RedFlag
        self.agent.model.config["enable_redflag"] = True

        # Set up the mock RedFlag service
        mock_redflag_service_class.return_value = self.mock_redflag_service

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent
            with patch(
                "autothreats.agents.simplified_threat_detection.LLMService",
                return_value=self.mock_llm_service,
            ):
                loop.run_until_complete(self.agent.initialize())

            # Check that the RedFlag service was created
            mock_redflag_service_class.assert_called_once()
            self.assertEqual(self.agent.redflag_service, self.mock_redflag_service)
        finally:
            # Disable RedFlag for other tests
            self.agent.model.config["enable_redflag"] = False
            loop.close()

    @patch("autothreats.agents.simplified_threat_detection.CodeShieldService")
    def test_initialize_with_codeshield(self, mock_codeshield_service_class):
        """Test initializing the agent with CodeShield enabled"""
        # Enable CodeShield
        self.agent.model.config["enable_codeshield"] = True

        # Set up the mock CodeShield service
        mock_codeshield_service_class.return_value = self.mock_codeshield_service

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent
            with patch(
                "autothreats.agents.simplified_threat_detection.LLMService",
                return_value=self.mock_llm_service,
            ):
                loop.run_until_complete(self.agent.initialize())

            # Check that the CodeShield service was created
            mock_codeshield_service_class.assert_called_once()
            self.assertEqual(
                self.agent.codeshield_service, self.mock_codeshield_service
            )
        finally:
            # Disable CodeShield for other tests
            self.agent.model.config["enable_codeshield"] = False
            loop.close()

    def test_shutdown(self):
        """Test shutting down the agent"""
        # Set up the agent
        self.agent.llm_service = self.mock_llm_service
        self.agent.redflag_service = self.mock_redflag_service
        self.agent.codeshield_service = self.mock_codeshield_service
        self.agent.cache = {"key": "value"}

        # Add close methods to the services
        self.mock_llm_service.close = AsyncMock()
        self.mock_redflag_service.close = AsyncMock()
        self.mock_codeshield_service.close = AsyncMock()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Shutdown the agent
            loop.run_until_complete(self.agent.shutdown())

            # Check that the services were closed
            self.mock_llm_service.close.assert_called_once()
            self.mock_redflag_service.close.assert_called_once()
            self.mock_codeshield_service.close.assert_called_once()

            # Check that the cache was cleared
            self.assertEqual(self.agent.cache, {})

            # Check that the agent state was updated
            self.assertEqual(self.agent.model.get_state("status"), "shutdown")
        finally:
            loop.close()

    def test_process_task_unsupported(self):
        """Test processing an unsupported task"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent first
            loop.run_until_complete(self.agent.initialize())

            # Set the agent as initialized
            self.agent.model.update_state("status", "initialized")

            # Process an unsupported task
            result = loop.run_until_complete(
                self.agent.process_task("unsupported_task", {})
            )

            # Check the result
            self.assertEqual(result["status"], "error")
            self.assertIn("Unsupported task type", result["message"])
        finally:
            loop.close()

    def test_handle_threat_detection_missing_params(self):
        """Test handling a threat detection task with missing parameters"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Process a task with missing parameters
            result = loop.run_until_complete(self.agent._handle_threat_detection({}))

            # Check the result
            self.assertEqual(result["status"], "error")
            self.assertIn("Missing required parameters", result["message"])
            self.assertIn("job_id", result["missing_parameters"])
            self.assertIn("codebase_id", result["missing_parameters"])
            self.assertIn("codebase", result["missing_parameters"])
        finally:
            loop.close()

    def test_get_files_to_scan(self):
        """Test getting files to scan"""
        # Create a codebase model
        codebase_model = CodebaseModel("test-codebase-id")
        codebase_model.files = {
            "file1.py": "print('Hello, world!')",
            "file2.js": "console.log('Hello, world!');",
            "file3.txt": "Hello, world!",
            "node_modules/file4.js": "console.log('Hello, world!');",
        }

        # Get files to scan
        files_to_scan = self.agent._get_files_to_scan(codebase_model)

        # Check the result
        self.assertEqual(len(files_to_scan), 2)
        self.assertIn("file1.py", files_to_scan)
        self.assertIn("file2.js", files_to_scan)
        self.assertNotIn("file3.txt", files_to_scan)
        self.assertNotIn("node_modules/file4.js", files_to_scan)

    def test_get_files_to_scan_lightweight(self):
        """Test getting files to scan in lightweight mode"""
        # Create a codebase model with many files
        codebase_model = CodebaseModel("test-codebase-id")
        for i in range(100):
            codebase_model.files[f"file{i}.py"] = f"print({i})"

        # Set the max_files attribute on the agent
        original_max_files = self.agent.max_files
        self.agent.max_files = 100  # Set to 100 for this test

        try:
            # Get files to scan in lightweight mode
            files_to_scan = self.agent._get_files_to_scan(
                codebase_model, {"lightweight": True}
            )

            # Check the result
            self.assertEqual(
                len(files_to_scan), 50
            )  # Half the files in lightweight mode
        finally:
            # Restore the original max_files
            self.agent.max_files = original_max_files

    @patch("autothreats.agents.simplified_threat_detection.LLMService")
    def test_detect_vulnerabilities_with_ai(self, mock_llm_service_class):
        """Test detecting vulnerabilities with AI"""
        # Set up the mock LLM service
        self.mock_llm_service.generate_text_async.return_value = """
        [
            {
                "vulnerability_type": "SQL Injection",
                "description": "Potential SQL injection vulnerability",
                "cwe_id": "CWE-89",
                "line_numbers": [10, 11],
                "confidence": 0.8,
                "severity": "High",
                "remediation": "Use parameterized queries",
                "file_path": "file1.py"
            }
        ]
        """
        mock_llm_service_class.return_value = self.mock_llm_service

        # Set up the agent
        self.agent.llm_service = self.mock_llm_service
        self.agent._is_test = True  # Set test mode flag

        # Create a codebase
        codebase = {
            "files": {
                "file1.py": "query = 'SELECT * FROM users WHERE id = ' + user_id",
                "file2.js": "console.log('Hello, world!');",
            }
        }

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent
            loop.run_until_complete(self.agent.initialize())

            # Detect vulnerabilities
            vulnerabilities, metadata = loop.run_until_complete(
                self.agent._detect_vulnerabilities_with_ai(codebase)
            )

            # Check the result
            self.assertEqual(len(vulnerabilities), 1)
            self.assertEqual(vulnerabilities[0]["vulnerability_type"], "SQL Injection")
            self.assertEqual(vulnerabilities[0]["cwe_id"], "CWE-89")
            self.assertEqual(vulnerabilities[0]["file_path"], "file1.py")

            # Check the metadata
            self.assertEqual(metadata["files_scanned"], 2)
            self.assertEqual(metadata["high_confidence_count"], 1)
            self.assertIn("CWE-89", metadata["cwe_distribution"])
            self.assertEqual(metadata["cwe_distribution"]["CWE-89"], 1)
        finally:
            loop.close()

    @patch("autothreats.agents.simplified_threat_detection.LLMService")
    def test_analyze_file_with_ai(self, mock_llm_service_class):
        """Test analyzing a file with AI"""
        # Set up the mock LLM service
        self.mock_llm_service.generate_text_async.return_value = """
        [
            {
                "vulnerability_type": "SQL Injection",
                "description": "Potential SQL injection vulnerability",
                "cwe_id": "CWE-89",
                "line_numbers": [1],
                "confidence": 0.8,
                "severity": "High",
                "remediation": "Use parameterized queries",
                "file_path": "file1.py"
            }
        ]
        """
        mock_llm_service_class.return_value = self.mock_llm_service

        # Set up the agent
        self.agent.llm_service = self.mock_llm_service

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Initialize the agent
            loop.run_until_complete(self.agent.initialize())

            # Analyze a file
            vulnerabilities = loop.run_until_complete(
                self.agent._analyze_file_with_ai(
                    "file1.py",
                    "query = 'SELECT * FROM users WHERE id = ' + user_id",
                    {},
                )
            )

            # Check the result
            self.assertEqual(len(vulnerabilities), 1)
            self.assertEqual(vulnerabilities[0]["vulnerability_type"], "SQL Injection")
            self.assertEqual(vulnerabilities[0]["cwe_id"], "CWE-89")
            self.assertEqual(vulnerabilities[0]["file_path"], "file1.py")
        finally:
            loop.close()

    def test_create_vulnerability_detection_prompt(self):
        """Test creating a vulnerability detection prompt"""
        # Create a prompt
        prompt = self.agent._create_vulnerability_detection_prompt(
            "file1.py",
            "query = 'SELECT * FROM users WHERE id = ' + user_id",
            "python",
            {},
        )

        # Check the prompt
        self.assertIn("file1.py", prompt)
        self.assertIn("python", prompt)
        self.assertIn("query = 'SELECT * FROM users WHERE id = ' + user_id", prompt)
        self.assertIn("vulnerability", prompt.lower())
        self.assertIn("json", prompt.lower())

    def test_parse_vulnerabilities_from_ai_response(self):
        """Test parsing vulnerabilities from AI response"""
        # Parse a valid response
        response = """
        [
            {
                "vulnerability_type": "SQL Injection",
                "description": "Potential SQL injection vulnerability",
                "cwe_id": "CWE-89",
                "line_numbers": [1],
                "confidence": 0.8,
                "severity": "High",
                "remediation": "Use parameterized queries"
            }
        ]
        """

        vulnerabilities = self.agent._parse_vulnerabilities_from_ai_response(
            response, "file1.py"
        )

        # Check the result
        self.assertEqual(len(vulnerabilities), 1)
        self.assertEqual(vulnerabilities[0]["vulnerability_type"], "SQL Injection")
        self.assertEqual(vulnerabilities[0]["cwe_id"], "CWE-89")
        self.assertEqual(vulnerabilities[0]["file_path"], "file1.py")

        # Parse an invalid response
        response = "This is not JSON"
        vulnerabilities = self.agent._parse_vulnerabilities_from_ai_response(
            response, "file1.py"
        )

        # Check the result
        self.assertEqual(len(vulnerabilities), 0)


if __name__ == "__main__":
    unittest.main()
