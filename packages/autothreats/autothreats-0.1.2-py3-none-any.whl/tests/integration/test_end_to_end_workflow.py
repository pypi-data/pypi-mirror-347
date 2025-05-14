#!/usr/bin/env python3
"""
End-to-end integration tests for the threat modeling system.
Tests the complete workflow from codebase ingestion to threat model generation.
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import simplified_main
from autothreats.simplified_orchestrator import SimplifiedOrchestrator
from tests.async_test_base import AsyncTestCase, async_test


class TestEndToEndWorkflow(AsyncTestCase):
    """End-to-end integration tests for the threat modeling system"""

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

        # Create a temporary directory for output files
        self.temp_dir = tempfile.mkdtemp()

        # Create a sample codebase directory
        self.codebase_dir = os.path.join(self.temp_dir, "codebase")
        os.makedirs(self.codebase_dir, exist_ok=True)

        # Create sample files with vulnerabilities
        self.create_sample_codebase()

    def tearDown(self):
        """Clean up after the test"""
        # Remove temporary directory and all its contents
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_sample_codebase(self):
        """Create a sample codebase with known vulnerabilities"""
        # Create a simple Python file with SQL injection
        sql_injection_file = os.path.join(self.codebase_dir, "app.py")
        with open(sql_injection_file, "w") as f:
            f.write(
                """
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return str(cursor.fetchone())

@app.route('/command')
def run_command():
    import os
    cmd = request.args.get('cmd')
    # Command injection vulnerability
    return os.popen(cmd).read()

if __name__ == '__main__':
    app.run(debug=True)
            """
            )

        # Create a JavaScript file with XSS
        xss_file = os.path.join(self.codebase_dir, "script.js")
        with open(xss_file, "w") as f:
            f.write(
                """
function displayUserInput() {
    // Get the user input from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const userInput = urlParams.get('input');
    
    // XSS vulnerability
    document.getElementById('output').innerHTML = userInput;
}

// Execute when page loads
window.onload = displayUserInput;
            """
            )

        # Create a config file
        config_file = os.path.join(self.codebase_dir, "config.json")
        with open(config_file, "w") as f:
            f.write(
                """
{
    "database": {
        "username": "admin",
        "password": "hardcoded_password",
        "host": "localhost",
        "port": 5432
    },
    "api_keys": {
        "service_a": "1234567890abcdef",
        "service_b": "abcdef1234567890"
    }
}
            """
            )

    @patch("simplified_main.load_api_key")
    @patch("simplified_main.load_config")
    @patch("simplified_main.validate_config")
    @patch("simplified_main.get_config_with_cli_overrides")
    @async_test
    async def test_end_to_end_workflow(
        self, mock_get_config, mock_validate, mock_load_config, mock_load_api_key
    ):
        """Test the complete end-to-end workflow"""
        # Set up the mocks
        mock_load_api_key.return_value = "test-api-key"
        mock_load_config.return_value = self.config
        mock_validate.return_value = []
        mock_get_config.return_value = self.config

        # Run the simplified threat modeling
        job_id = await simplified_main.run_simplified_threat_modeling(
            codebase_path=self.codebase_dir,
            output_dir=self.temp_dir,
            lightweight=False,
            enable_multi_stage=False,
            api_key="test-api-key",
            config=self.config,
            verbose=True,
            debug=False,
        )

        # Verify job ID was returned
        self.assertIsNotNone(job_id, "No job ID returned")

        # Check that output files were created
        json_path = os.path.join(self.temp_dir, f"threat_model_{job_id}.json")
        html_path = os.path.join(self.temp_dir, f"threat_model_{job_id}.html")

        self.assertTrue(
            os.path.exists(json_path), f"JSON output file not created: {json_path}"
        )
        self.assertTrue(
            os.path.exists(html_path), f"HTML output file not created: {html_path}"
        )

        # Load and verify the JSON output
        with open(json_path, "r") as f:
            threat_model = json.load(f)

        # Verify threat model structure
        self.assertEqual(
            threat_model["job_id"], job_id, "Job ID mismatch in threat model"
        )
        self.assertIn(
            "vulnerabilities", threat_model, "No vulnerabilities in threat model"
        )
        self.assertIn("metadata", threat_model, "No metadata in threat model")

        # Verify vulnerabilities were found
        # In mock mode, we might not get actual vulnerabilities matching our sample code,
        # but we should at least have some vulnerabilities
        self.assertGreater(
            len(threat_model["vulnerabilities"]), 0, "No vulnerabilities found"
        )


class TestMultipleCodebasesWorkflow(AsyncTestCase):
    """Integration tests for processing multiple codebases"""

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

        # Create a temporary directory for output files
        self.temp_dir = tempfile.mkdtemp()

        # Create sample codebase directories
        self.codebase1_dir = os.path.join(self.temp_dir, "codebase1")
        self.codebase2_dir = os.path.join(self.temp_dir, "codebase2")

        os.makedirs(self.codebase1_dir, exist_ok=True)
        os.makedirs(self.codebase2_dir, exist_ok=True)

        # Create sample files with different vulnerabilities
        self.create_sample_codebases()

        # Create orchestrator
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        # Shutdown orchestrator
        if hasattr(self, "orchestrator"):
            await self.orchestrator.shutdown()

        # Remove temporary directory and all its contents
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_sample_codebases(self):
        """Create sample codebases with different vulnerabilities"""
        # Codebase 1: SQL injection and XSS
        sql_file = os.path.join(self.codebase1_dir, "database.py")
        with open(sql_file, "w") as f:
            f.write(
                """
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()
            """
            )

        # Codebase 2: Command injection and hardcoded credentials
        cmd_file = os.path.join(self.codebase2_dir, "utils.py")
        with open(cmd_file, "w") as f:
            f.write(
                """
import os
import subprocess

def run_command(command):
    # Command injection vulnerability
    os.system(command)
    
def connect_to_database():
    # Hardcoded credentials
    username = "admin"
    password = "super_secret_password"
    connection_string = f"postgresql://{username}:{password}@localhost:5432/mydb"
    return connection_string
            """
            )

    @async_test
    async def test_multiple_codebases_workflow(self):
        """Test processing multiple codebases sequentially"""
        # Process first codebase
        codebase1 = simplified_main.load_codebase(self.codebase1_dir)
        job_id1 = f"job_codebase1_{int(os.path.getmtime(self.codebase1_dir))}"

        job_data1 = {
            "job_id": job_id1,
            "codebase_id": f"codebase_{job_id1}",
            "codebase": codebase1,
            "context": {"lightweight": False, "enable_multi_stage": False},
        }

        result1 = await self.orchestrator.process_job(job_data1)

        # Process second codebase
        codebase2 = simplified_main.load_codebase(self.codebase2_dir)
        job_id2 = f"job_codebase2_{int(os.path.getmtime(self.codebase2_dir))}"

        job_data2 = {
            "job_id": job_id2,
            "codebase_id": f"codebase_{job_id2}",
            "codebase": codebase2,
            "context": {"lightweight": False, "enable_multi_stage": False},
        }

        result2 = await self.orchestrator.process_job(job_data2)

        # Verify both results are successful
        self.assertEqual(
            result1["status"],
            "success",
            f"First job failed: {result1.get('message', '')}",
        )
        self.assertEqual(
            result2["status"],
            "success",
            f"Second job failed: {result2.get('message', '')}",
        )

        # Verify vulnerabilities were found in both codebases
        vulnerabilities1 = result1["results"]["threat_detection"]["vulnerabilities"]
        vulnerabilities2 = result2["results"]["threat_detection"]["vulnerabilities"]

        self.assertGreater(
            len(vulnerabilities1), 0, "No vulnerabilities found in first codebase"
        )
        self.assertGreater(
            len(vulnerabilities2), 0, "No vulnerabilities found in second codebase"
        )

        # Verify the results are different (different codebases should have different vulnerabilities)
        # In mock mode, this might not be true, but we can at least check they have different job IDs
        self.assertNotEqual(
            result1["job_id"],
            result2["job_id"],
            "Job IDs are the same for different codebases",
        )


class TestErrorHandlingWorkflow(AsyncTestCase):
    """Integration tests for error handling in the workflow"""

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

        # Create orchestrator
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "orchestrator"):
            await self.orchestrator.shutdown()

    @async_test
    async def test_missing_codebase_handling(self):
        """Test handling of missing codebase"""
        # Create job data with missing codebase
        job_id = "test_missing_codebase"
        job_data = {
            "job_id": job_id,
            "codebase_id": f"codebase_{job_id}",
            # No codebase provided
            "context": {"lightweight": False, "enable_multi_stage": False},
        }

        # Process the job
        result = await self.orchestrator.process_job(job_data)

        # Verify the result indicates an error
        self.assertEqual(
            result["status"], "error", "Job with missing codebase did not fail"
        )
        self.assertIn("message", result, "No error message in result")

    @async_test
    async def test_invalid_job_data_handling(self):
        """Test handling of invalid job data"""
        # Create invalid job data (missing job_id)
        job_data = {
            # No job_id provided
            "codebase": {"files": {}},
            "context": {"lightweight": False, "enable_multi_stage": False},
        }

        # Process the job
        result = await self.orchestrator.process_job(job_data)

        # Verify a job_id was generated
        self.assertIn("job_id", result, "No job_id in result")
        self.assertIsNotNone(result["job_id"], "Generated job_id is None")


if __name__ == "__main__":
    unittest.main()
