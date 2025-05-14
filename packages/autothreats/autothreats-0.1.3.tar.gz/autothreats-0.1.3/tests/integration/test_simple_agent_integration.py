#!/usr/bin/env python3
"""
Integration test for the Simple Agent API.
This test demonstrates how to create a custom agent and integrate it with the system.
"""

import asyncio
import logging
import os
import sys
import tempfile
from typing import Any, Dict, List, Optional

import pytest

# Add the parent directory to the path so we can import the autothreats package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.simplified_base import SharedWorkspace
from autothreats.utils.agent_api import create_and_register_agent
from autothreats.utils.logging_config import configure_logging

# Configure logging
configure_logging(verbose=True)
logger = logging.getLogger(__name__)


# Define a custom vulnerability scanner agent
async def process_vulnerability_scan(
    agent, task_type: str, task_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Process vulnerability scanning tasks"""
    agent.logger.info(f"Processing task of type {task_type}")

    if task_type == "scan_vulnerabilities":
        # Extract parameters
        codebase_id = task_data.get("codebase_id")
        if not codebase_id:
            return {
                "status": "error",
                "message": "Missing required parameter: codebase_id",
            }

        # Get codebase from workspace
        codebase = agent.workspace.get_data(codebase_id)
        if not codebase:
            return {"status": "error", "message": f"Codebase not found: {codebase_id}"}

        # Perform vulnerability scan (simplified example)
        vulnerabilities = []

        # Check for common vulnerability patterns
        patterns = [
            {"pattern": "eval(", "name": "Code Injection", "severity": "high"},
            {"pattern": "exec(", "name": "Code Injection", "severity": "high"},
            {
                "pattern": "password =",
                "name": "Hardcoded Password",
                "severity": "medium",
            },
            {
                "pattern": "SELECT * FROM",
                "name": "SQL Injection Risk",
                "severity": "medium",
            },
            {
                "pattern": "TODO: Fix security",
                "name": "Security TODO",
                "severity": "low",
            },
        ]

        for file_path, content in codebase.get("files", {}).items():
            # Skip if content is not a string
            if not isinstance(content, str):
                continue

            # Check each pattern
            for pattern in patterns:
                if pattern["pattern"] in content:
                    # Find line numbers
                    lines = []
                    for i, line in enumerate(content.split("\n")):
                        if pattern["pattern"] in line:
                            lines.append(i + 1)

                    vulnerabilities.append(
                        {
                            "file": file_path,
                            "vulnerability": pattern["name"],
                            "severity": pattern["severity"],
                            "pattern": pattern["pattern"],
                            "lines": lines,
                        }
                    )

        # Store results in workspace
        result_key = f"vulnerability_scan_{task_data.get('job_id')}"
        agent.workspace.store_data(
            result_key,
            {
                "vulnerabilities": vulnerabilities,
                "total_vulnerabilities": len(vulnerabilities),
            },
        )

        return {
            "status": "success",
            "message": f"Found {len(vulnerabilities)} potential vulnerabilities",
            "vulnerabilities": vulnerabilities,
        }
    else:
        return {"status": "error", "message": f"Unsupported task type: {task_type}"}


@pytest.fixture
def workspace():
    """Create a workspace for testing"""
    ws = SharedWorkspace("test_workspace")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws.start())
    yield ws
    loop.run_until_complete(ws.stop())


@pytest.fixture
def vulnerability_agent(workspace):
    """Create and register a vulnerability scanner agent"""
    agent = create_and_register_agent(
        workspace=workspace,
        agent_id="vulnerability_scanner",
        agent_type="vulnerability_scanner",
        process_task_func=process_vulnerability_scan,
        config={"scan_depth": "medium", "timeout": 30},
        optional_config=["scan_depth", "timeout"],
        default_config={"scan_depth": "medium", "timeout": 30},
    )

    # Initialize the agent
    loop = asyncio.get_event_loop()
    loop.run_until_complete(agent.initialize())
    yield agent
    loop.run_until_complete(agent.shutdown())


@pytest.fixture
def mock_codebase():
    """Create a mock codebase for testing"""
    # Create temporary files with test code
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file with vulnerabilities
        vulnerable_file = os.path.join(temp_dir, "vulnerable.py")
        with open(vulnerable_file, "w") as f:
            f.write(
                """
def process_input(user_input):
    # This is vulnerable to code injection
    result = eval(user_input)
    return result

# Database connection
password = "super_secret_password"
connection_string = f"postgresql://admin:{password}@localhost/db"

def query_database(user_id):
    # This is vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # TODO: Fix security issue with parameterized queries
    return execute_query(query)
"""
            )

        # Create a file without vulnerabilities
        safe_file = os.path.join(temp_dir, "safe.py")
        with open(safe_file, "w") as f:
            f.write(
                """
def safe_function(param):
    # This function is safe
    return param.upper()
"""
            )

        # Read the files
        with open(vulnerable_file, "r") as f:
            vulnerable_content = f.read()

        with open(safe_file, "r") as f:
            safe_content = f.read()

        # Create the mock codebase
        mock_codebase = {
            "files": {"vulnerable.py": vulnerable_content, "safe.py": safe_content}
        }

        return mock_codebase


def test_vulnerability_scanner_integration(
    workspace, vulnerability_agent, mock_codebase
):
    """Test the vulnerability scanner agent integration"""
    # Store the mock codebase in the workspace
    workspace.store_data("test_codebase", mock_codebase)

    # Run the vulnerability scan
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        workspace.process_agent_task(
            agent_id="vulnerability_scanner",
            task_type="scan_vulnerabilities",
            task_data={"job_id": "test_job", "codebase_id": "test_codebase"},
        )
    )

    # Verify the result
    assert result["status"] == "success"
    assert "vulnerabilities" in result
    assert len(result["vulnerabilities"]) > 0

    # Check that we found the expected vulnerabilities
    vulnerabilities = result["vulnerabilities"]

    # Check for code injection vulnerability
    code_injection = next(
        (v for v in vulnerabilities if v["vulnerability"] == "Code Injection"), None
    )
    assert code_injection is not None
    assert code_injection["file"] == "vulnerable.py"
    assert code_injection["pattern"] == "eval("

    # Check for hardcoded password
    hardcoded_password = next(
        (v for v in vulnerabilities if v["vulnerability"] == "Hardcoded Password"), None
    )
    assert hardcoded_password is not None
    assert hardcoded_password["file"] == "vulnerable.py"

    # Check for SQL injection
    sql_injection = next(
        (v for v in vulnerabilities if v["vulnerability"] == "SQL Injection Risk"), None
    )
    assert sql_injection is not None
    assert sql_injection["file"] == "vulnerable.py"

    # Check for security TODO
    security_todo = next(
        (v for v in vulnerabilities if v["vulnerability"] == "Security TODO"), None
    )
    assert security_todo is not None
    assert security_todo["file"] == "vulnerable.py"

    # Verify that results were stored in the workspace
    stored_results = workspace.get_data("vulnerability_scan_test_job")
    assert stored_results is not None
    assert stored_results["total_vulnerabilities"] == len(vulnerabilities)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
