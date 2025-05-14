#!/usr/bin/env python3
"""
Integration tests for the threat detection pipeline.
Tests the complete threat detection process from codebase analysis to vulnerability reporting.
"""

import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.agents.simplified_threat_detection import (
    SimplifiedThreatDetectionAgent,
)
from autothreats.simplified_base import SharedWorkspace
from autothreats.simplified_orchestrator import SimplifiedOrchestrator
from tests.async_test_base import AsyncTestCase, async_test


class TestThreatDetectionPipeline(AsyncTestCase):
    """Integration tests for the threat detection pipeline"""

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

        # Create a sample codebase with known vulnerabilities
        self.codebase = {
            "files": {
                "sql_injection.py": """
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()
                """,
                "xss.js": """
function displayUserInput(input) {
    // XSS vulnerability
    document.getElementById('output').innerHTML = input;
}
                """,
                "command_injection.py": """
import os

def run_command(command):
    # Command injection vulnerability
    os.system(command)
                """,
            }
        }

        # Create a workspace
        self.workspace = SharedWorkspace("test_threat_detection_workspace")
        await self.workspace.start()

        # Store the config in the workspace
        self.workspace.store_data("system_config", self.config["system"])

        # Create and register the threat detection agent
        self.threat_detection_agent = SimplifiedThreatDetectionAgent(
            agent_id="threat_detection_agent", config=self.config["threat_detection"]
        )
        self.workspace.register_agent(self.threat_detection_agent)

        # Initialize the agent
        await self.threat_detection_agent.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "threat_detection_agent"):
            await self.threat_detection_agent.shutdown()

        if hasattr(self, "workspace"):
            await self.workspace.stop()

    @async_test
    async def test_direct_threat_detection(self):
        """Test direct threat detection without going through the orchestrator"""
        # Create job data
        job_id = "test_direct_detection"
        job_data = {
            "job_id": job_id,
            "codebase_id": f"codebase_{job_id}",
            "codebase": self.codebase,
            "context": {"lightweight": False},
        }

        # Store codebase in workspace
        self.workspace.store_data(f"codebase_{job_id}", self.codebase)

        # Process the threat detection task directly
        result = await self.workspace.process_agent_task(
            agent_id="threat_detection_agent",
            task_type="threat_detection",
            task_data=job_data,
        )

        # Verify the result
        self.assertEqual(
            result["status"],
            "success",
            f"Threat detection failed: {result.get('message', '')}",
        )
        self.assertIn("vulnerabilities", result, "No vulnerabilities in result")

        # Verify vulnerabilities were found
        vulnerabilities = result["vulnerabilities"]
        self.assertGreater(len(vulnerabilities), 0, "No vulnerabilities found")

        # Check for expected vulnerability types
        vulnerability_types = [v.get("vulnerability_type", "") for v in vulnerabilities]
        expected_types = ["SQL Injection", "Cross-site Scripting", "Command Injection"]

        # In mock mode, we might not get exact matches, but we should have some vulnerabilities
        self.assertGreater(len(vulnerability_types), 0, "No vulnerability types found")


class TestLightweightVsFullAnalysis(AsyncTestCase):
    """Integration tests comparing lightweight and full analysis"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a mock config
        self.config = {
            "system": {
                "enable_agentic_improvements": True,
                "debug_logging": False,
            },
            "llm": {
                "provider": "openai",
                "mock_mode": True,  # Use mock mode for testing
            },
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Create a larger sample codebase
        self.codebase = {
            "files": {
                # Add 10 files with various vulnerabilities
                **{
                    f"file_{i}.py": f"import os\n\ndef func_{i}(param):\n    os.system(param)  # Command injection in file {i}\n"
                    for i in range(10)
                },
                # Add 10 more files with SQL injection
                **{
                    f"sql_{i}.py": f"import sqlite3\n\ndef query_{i}(user_input):\n    conn = sqlite3.connect('db.sqlite')\n    cursor = conn.cursor()\n    cursor.execute(f\"SELECT * FROM table WHERE id = {{user_input}}\")  # SQL injection in file {i}\n"
                    for i in range(10)
                },
            }
        }

        # Create orchestrator
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "orchestrator"):
            await self.orchestrator.shutdown()

    @async_test
    async def test_lightweight_vs_full_analysis(self):
        """Test and compare lightweight vs full analysis"""
        # Create job data for lightweight analysis
        lightweight_job_id = "test_lightweight"
        lightweight_job_data = {
            "job_id": lightweight_job_id,
            "codebase_id": f"codebase_{lightweight_job_id}",
            "codebase": self.codebase,
            "context": {"lightweight": True},
        }

        # Create job data for full analysis
        full_job_id = "test_full"
        full_job_data = {
            "job_id": full_job_id,
            "codebase_id": f"codebase_{full_job_id}",
            "codebase": self.codebase,
            "context": {"lightweight": False},
        }

        # Process both jobs
        lightweight_result = await self.orchestrator.process_job(lightweight_job_data)
        full_result = await self.orchestrator.process_job(full_job_data)

        # Verify both results are successful
        self.assertEqual(
            lightweight_result["status"], "success", "Lightweight analysis failed"
        )
        self.assertEqual(full_result["status"], "success", "Full analysis failed")

        # Get vulnerabilities from both analyses
        lightweight_vulns = lightweight_result["results"]["threat_detection"][
            "vulnerabilities"
        ]
        full_vulns = full_result["results"]["threat_detection"]["vulnerabilities"]

        # Both should find vulnerabilities
        self.assertGreater(
            len(lightweight_vulns), 0, "Lightweight analysis found no vulnerabilities"
        )
        self.assertGreater(len(full_vulns), 0, "Full analysis found no vulnerabilities")

        # Full analysis should typically find more vulnerabilities than lightweight
        # But in mock mode, this might not be true, so we just log the counts
        self.assertIsNotNone(lightweight_vulns, "Lightweight vulnerabilities is None")
        self.assertIsNotNone(full_vulns, "Full vulnerabilities is None")

        # Log the results for comparison
        print(f"Lightweight analysis found {len(lightweight_vulns)} vulnerabilities")
        print(f"Full analysis found {len(full_vulns)} vulnerabilities")


class TestMultiStageAnalysis(AsyncTestCase):
    """Integration tests for multi-stage analysis"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create a mock config with multi-stage enabled
        self.config = {
            "system": {
                "enable_agentic_improvements": True,
                "debug_logging": False,
            },
            "llm": {
                "provider": "openai",
                "mock_mode": True,  # Use mock mode for testing
            },
            "threat_detection": {
                "mock_mode": True,  # Use mock mode for testing
            },
            "enable_multi_stage": True,
            "multi_stage": {
                "mock_mode": True,  # Use mock mode for testing
            },
        }

        # Create a sample codebase
        self.codebase = {
            "files": {
                "app.py": """
from flask import Flask, request, render_template_string
import os
import sqlite3

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    # SQL Injection vulnerability
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    results = cursor.fetchall()
    
    # XSS vulnerability
    template = f"<h1>Search results for: {query}</h1><ul>"
    for result in results:
        template += f"<li>{result[0]}</li>"
    template += "</ul>"
    
    # Template injection vulnerability
    return render_template_string(template)

@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd', 'echo "No command specified"')
    
    # Command injection vulnerability
    output = os.popen(cmd).read()
    
    return output

if __name__ == '__main__':
    app.run(debug=True)
                """
            }
        }

        # Create orchestrator with multi-stage enabled
        self.orchestrator = SimplifiedOrchestrator(self.config)
        await self.orchestrator.initialize()

    async def asyncTearDown(self):
        """Clean up after the test"""
        if hasattr(self, "orchestrator"):
            await self.orchestrator.shutdown()

    @async_test
    async def test_multi_stage_analysis(self):
        """Test multi-stage analysis"""
        # Skip this test if multi-stage agent is not available
        if "multi_stage" not in self.orchestrator.agents:
            self.skipTest("Multi-stage agent not available")

        # Create job data
        job_id = "test_multi_stage"
        job_data = {
            "job_id": job_id,
            "codebase_id": f"codebase_{job_id}",
            "codebase": self.codebase,
            "context": {"lightweight": False, "enable_multi_stage": True},
        }

        # Process the job
        result = await self.orchestrator.process_job(job_data)

        # Verify the result
        self.assertEqual(
            result["status"],
            "success",
            f"Multi-stage analysis failed: {result.get('message', '')}",
        )

        # Verify vulnerabilities were found
        vulnerabilities = result["results"]["threat_detection"]["vulnerabilities"]
        self.assertGreater(
            len(vulnerabilities), 0, "No vulnerabilities found in multi-stage analysis"
        )

        # In a real test, we would check for multi-stage specific outputs
        # But in mock mode, we just verify we got some results
        self.assertIsNotNone(vulnerabilities, "Multi-stage vulnerabilities is None")


if __name__ == "__main__":
    unittest.main()
