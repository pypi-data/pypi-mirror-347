#!/usr/bin/env python3
"""
Tests for the simplified main module.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import simplified_main
from autothreats.simplified_orchestrator import SimplifiedOrchestrator

# Import async test utilities
from .async_test_base import AsyncTestCase, async_test


class TestSimplifiedMain(AsyncTestCase):
    """Test the simplified main module"""

    def setUp(self):
        """Set up the test"""
        # Create a mock orchestrator
        self.mock_orchestrator = MagicMock(spec=SimplifiedOrchestrator)
        self.mock_orchestrator.initialize = AsyncMock()
        self.mock_orchestrator.process_job = AsyncMock(
            return_value={"status": "success"}
        )
        self.mock_orchestrator.shutdown = AsyncMock()

        # Create a mock config
        self.mock_config = {
            "system": {
                "enable_agentic_improvements": True,
                "debug_logging": False,
                "lightweight": False,
                "max_scan_dirs": 100,
            },
            "llm": {
                "provider": "openai",
            },
            "enable_redflag": False,
            "enable_codeshield": False,
        }

    def test_load_codebase_file(self):
        """Test loading a codebase from a file"""
        # Mock open to return a test file
        with patch(
            "builtins.open", mock_open(read_data="print('Hello, world!')")
        ) as mock_file:
            # Mock os.path.isfile to return True
            with patch("os.path.isfile", return_value=True):
                # Load the codebase
                codebase = simplified_main.load_codebase("test.py")

                # Check that the file was opened
                mock_file.assert_called_once_with(
                    "test.py", "r", encoding="utf-8", errors="ignore"
                )

                # Check the codebase
                self.assertIn("files", codebase)
                self.assertIn("test.py", codebase["files"])
                self.assertEqual(codebase["files"]["test.py"], "print('Hello, world!')")

    def test_load_codebase_directory(self):
        """Test loading a codebase from a directory"""
        # Mock os.path.isfile to return False and os.path.isdir to return True
        with patch("os.path.isfile", return_value=False):
            with patch("os.path.isdir", return_value=True):
                # Mock os.walk to return a test directory structure
                with patch(
                    "os.walk",
                    return_value=[
                        ("test_dir", [], ["test.py", ".hidden.py"]),
                        ("test_dir/subdir", [], ["test2.py"]),
                    ],
                ):
                    # Mock open to return test files
                    with patch(
                        "builtins.open", mock_open(read_data="print('Hello, world!')")
                    ) as mock_file:
                        # Mock os.path.relpath to return relative paths
                        with patch(
                            "os.path.relpath",
                            side_effect=lambda path, base: path.replace(base + "/", ""),
                        ):
                            # Load the codebase
                            codebase = simplified_main.load_codebase("test_dir")

                            # Check that the files were opened
                            self.assertEqual(
                                mock_file.call_count, 2
                            )  # Only 2 files, .hidden.py is skipped

                            # Check the codebase
                            self.assertIn("files", codebase)
                            self.assertIn("test.py", codebase["files"])
                            self.assertIn("subdir/test2.py", codebase["files"])
                            self.assertEqual(
                                codebase["files"]["test.py"], "print('Hello, world!')"
                            )
                            self.assertEqual(
                                codebase["files"]["subdir/test2.py"],
                                "print('Hello, world!')",
                            )

    def test_load_codebase_nonexistent(self):
        """Test loading a codebase from a nonexistent path"""
        # Mock os.path.isfile and os.path.isdir to return False
        with patch("os.path.isfile", return_value=False):
            with patch("os.path.isdir", return_value=False):
                # Load the codebase and expect an exception
                with self.assertRaises(ValueError):
                    simplified_main.load_codebase("nonexistent")

    def test_generate_html_report(self):
        """Test generating an HTML report"""
        # Create a threat model
        threat_model = {
            "job_id": "test-job",
            "codebase_id": "test-codebase",
            "vulnerabilities": [
                {
                    "id": "vuln-1",
                    "vulnerability_type": "SQL Injection",
                    "description": "Potential SQL injection vulnerability",
                    "cwe_id": "CWE-89",
                    "line_numbers": [10, 11],
                    "confidence": 0.8,
                    "severity": "High",
                    "remediation": "Use parameterized queries",
                    "file_path": "test.py",
                }
            ],
            "threat_scenarios": [
                {
                    "name": "Data Breach",
                    "description": "Attacker steals sensitive data",
                    "impact": "High",
                    "likelihood": "Medium",
                    "mitigations": "Encrypt sensitive data",
                }
            ],
            "executive_summary": "This is a test summary",
            "metadata": {
                "timestamp": 1234567890,
                "analysis_type": "complete",
                "files_analyzed": 10,
            },
        }

        # Generate the report
        report = simplified_main.generate_html_report(threat_model)

        # Check the report
        self.assertIsInstance(report, str)
        self.assertIn("<!DOCTYPE html>", report)
        self.assertIn("Threat Canvas Report", report)
        self.assertIn("SQL Injection", report)
        self.assertIn("Data Breach", report)
        self.assertIn("This is a test summary", report)

    @patch("simplified_main.os.environ.get")
    def test_load_api_key_from_env(self, mock_environ_get):
        """Test loading an API key from environment variable"""
        # Mock os.environ.get to return a test key
        mock_environ_get.return_value = "test-key"

        # Load the API key
        api_key = simplified_main.load_api_key()

        # Check the API key
        self.assertEqual(api_key, "test-key")
        mock_environ_get.assert_called_once_with("OPENAI_API_KEY")

    @patch("simplified_main.os.environ.get")
    @patch("simplified_main.os.path.exists")
    def test_load_api_key_from_file(self, mock_path_exists, mock_environ_get):
        """Test loading an API key from a file"""
        # Mock os.environ.get to return None
        mock_environ_get.return_value = None

        # Mock os.path.exists to return True
        mock_path_exists.return_value = True

        # Mock open to return a test file
        with patch(
            "builtins.open", mock_open(read_data='{"api_key": "test-key"}')
        ) as mock_file:
            # Load the API key
            api_key = simplified_main.load_api_key("api_key.json")

            # Check the API key
            self.assertEqual(api_key, "test-key")
            mock_file.assert_called_once_with("api_key.json", "r")

    @patch("simplified_main.os.environ.get")
    @patch("simplified_main.os.path.exists")
    @patch("simplified_main.os.path.expanduser")
    def test_load_api_key_from_default_location(
        self, mock_expanduser, mock_path_exists, mock_environ_get
    ):
        """Test loading an API key from a default location"""
        # Mock os.environ.get to return None
        mock_environ_get.return_value = None

        # Mock os.path.exists to return True for the default location
        mock_path_exists.side_effect = (
            lambda path: path == "/home/user/.openai/api_key.txt"
        )

        # Mock os.path.expanduser to return the expanded path
        mock_expanduser.side_effect = lambda path: path.replace("~", "/home/user")

        # Mock open to return a test file
        with patch("builtins.open", mock_open(read_data="test-key")) as mock_file:
            # Load the API key
            api_key = simplified_main.load_api_key()

            # Check the API key
            self.assertEqual(api_key, "test-key")
            mock_file.assert_called_once_with("/home/user/.openai/api_key.txt", "r")

    @async_test
    @patch("simplified_main.SimplifiedOrchestrator")
    @patch("simplified_main.load_codebase")
    @patch("simplified_main.load_config")
    @patch("simplified_main.validate_config")
    @patch("simplified_main.get_config_with_cli_overrides")
    @patch("simplified_main.os.makedirs")
    @patch("simplified_main.time.time")
    @patch("builtins.open", new_callable=mock_open)
    async def test_run_simplified_threat_modeling(
        self,
        mock_open,
        mock_time,
        mock_makedirs,
        mock_get_config,
        mock_validate,
        mock_load_config,
        mock_load_codebase,
        mock_orchestrator_class,
    ):
        """Test running simplified threat modeling"""
        # Set up the mocks
        mock_time.return_value = 1234567890
        mock_load_config.return_value = self.mock_config
        mock_validate.return_value = []
        mock_get_config.return_value = self.mock_config
        mock_load_codebase.return_value = {
            "files": {"test.py": "print('Hello, world!')"}
        }
        mock_orchestrator_class.return_value = self.mock_orchestrator

        # Set up the orchestrator to return a successful result
        self.mock_orchestrator.process_job.return_value = {
            "status": "success",
            "results": {
                "threat_detection": {
                    "vulnerabilities": [
                        {
                            "vulnerability_type": "SQL Injection",
                            "description": "Potential SQL injection vulnerability",
                            "cwe_id": "CWE-89",
                            "line_numbers": [10, 11],
                            "confidence": 0.8,
                            "severity": "high",
                            "remediation": "Use parameterized queries",
                            "file_path": "test.py",
                        }
                    ]
                }
            },
        }

        # Run simplified threat modeling
        job_id = await simplified_main.run_simplified_threat_modeling(
            codebase_path="test_dir",
            output_dir="output_dir",
            lightweight=False,
            enable_multi_stage=False,
            api_key="test-key",
            verbose=False,
            debug=False,
        )

        # Check that the orchestrator was created and used
        mock_orchestrator_class.assert_called_once()
        self.mock_orchestrator.initialize.assert_called_once()
        self.mock_orchestrator.process_job.assert_called_once()
        self.mock_orchestrator.shutdown.assert_called_once()

        # Check that the output files were created
        mock_open.assert_any_call(
            os.path.join("output_dir", f"threat_model_{job_id}.json"), "w"
        )
        mock_open.assert_any_call(
            os.path.join("output_dir", f"threat_model_{job_id}.html"), "w"
        )

        # Check the job ID
        self.assertEqual(job_id, f"job_{int(mock_time.return_value)}")

    @patch("simplified_main.run_simplified_threat_modeling")
    @patch("simplified_main.load_api_key")
    @patch("simplified_main.load_config")
    @patch("simplified_main.validate_config")
    @patch("simplified_main.get_config_with_cli_overrides")
    @patch("simplified_main.install_security_tools")
    @patch("simplified_main.configure_logging")
    @patch("simplified_main.argparse.ArgumentParser.parse_args")
    @patch("simplified_main.asyncio.run")
    def test_main(
        self,
        mock_asyncio_run,
        mock_parse_args,
        mock_configure_logging,
        mock_install_tools,
        mock_get_config,
        mock_validate,
        mock_load_config,
        mock_load_api_key,
        mock_run_threat_modeling,
    ):
        """Test the main function"""
        # Set up the mocks
        mock_args = MagicMock()
        mock_args.codebase = "test_dir"
        mock_args.output = "output_dir"
        mock_args.lightweight = False
        mock_args.enable_multi_stage = False
        mock_args.api_key_file = "api_key.json"
        mock_args.config = "config.json"
        mock_args.verbose = False
        mock_args.debug = False
        mock_args.max_files = 100
        mock_args.max_scan_dirs = 100
        mock_args.enable_redflag = False
        mock_args.disable_redflag = False
        mock_args.enable_codeshield = False
        mock_args.disable_codeshield = False
        mock_args.enable_agentic = True
        mock_args.disable_agentic = False
        mock_parse_args.return_value = mock_args

        mock_load_api_key.return_value = "test-key"
        mock_load_config.return_value = self.mock_config
        mock_validate.return_value = []
        mock_get_config.return_value = self.mock_config
        mock_asyncio_run.return_value = "test-job"

        # Run the main function
        with patch("sys.exit") as mock_exit:
            simplified_main.main()

            # Check that the functions were called
            mock_configure_logging.assert_called_once()
            mock_load_api_key.assert_called_once_with(mock_args.api_key_file)
            mock_load_config.assert_called()
            mock_install_tools.assert_called_once()
            mock_validate.assert_called_once()
            mock_get_config.assert_called_once()
            mock_asyncio_run.assert_called_once()
            mock_exit.assert_called_once_with(0)

    @patch("autothreats.utils.install_tools.install_all_tools")
    def test_install_security_tools(self, mock_install_all_tools):
        """Test installing security tools"""
        # Set up the mock
        mock_install_all_tools.return_value = True

        # Install security tools
        simplified_main.install_security_tools()

        # Check that the function was called
        mock_install_all_tools.assert_called_once()


if __name__ == "__main__":
    unittest.main()
