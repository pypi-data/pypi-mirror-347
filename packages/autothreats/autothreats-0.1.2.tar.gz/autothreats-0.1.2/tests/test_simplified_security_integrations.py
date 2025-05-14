#!/usr/bin/env python3
"""
Tests for the simplified security integration modules (RedFlag and CodeShield).
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import Agent, AgentModel
from autothreats.utils.codeshield_service import CodeShieldService
from autothreats.utils.redflag_service import RedFlagService


class SimplifiedRedFlagAgent(Agent):
    """Simplified RedFlag agent for security scanning"""

    def __init__(self, agent_id: str, config=None):
        super().__init__(agent_id, "redflag", config)
        self.redflag_service = RedFlagService(api_key=self.model.config.get("api_key"))

    async def initialize(self):
        """Initialize the agent"""
        self.logger.info("Initializing RedFlag agent")
        return {"status": "success"}

    async def shutdown(self):
        """Shutdown the agent"""
        self.logger.info("Shutting down RedFlag agent")
        return {"status": "success"}

    async def _process_task_impl(self, task_type, task_data):
        """Implementation of task processing logic"""
        if task_type == "scan_codebase":
            return await self._scan_codebase(task_data)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _scan_codebase(self, task_data):
        """Scan a codebase for security vulnerabilities"""
        codebase = task_data.get("codebase")
        if not codebase:
            return {"status": "error", "message": "No codebase provided"}

        try:
            # Scan the codebase
            vulnerabilities = await self.redflag_service.analyze_codebase(codebase)

            # Format the result
            result = {
                "status": "success",
                "job_id": task_data.get("job_id"),
                "codebase_id": task_data.get("codebase_id"),
                "vulnerabilities": vulnerabilities,
            }

            return result
        except Exception as e:
            self.logger.error(f"Error scanning codebase: {e}")
            return {
                "status": "error",
                "message": str(e),
                "job_id": task_data.get("job_id"),
                "codebase_id": task_data.get("codebase_id"),
            }


class SimplifiedCodeShieldAgent(Agent):
    """Simplified CodeShield agent for security scanning"""

    def __init__(self, agent_id: str, config=None):
        super().__init__(agent_id, "codeshield", config)
        self.codeshield_service = CodeShieldService(
            api_key=self.model.config.get("api_key")
        )

    async def initialize(self):
        """Initialize the agent"""
        self.logger.info("Initializing CodeShield agent")
        return {"status": "success"}

    async def shutdown(self):
        """Shutdown the agent"""
        self.logger.info("Shutting down CodeShield agent")
        return {"status": "success"}

    async def _process_task_impl(self, task_type, task_data):
        """Implementation of task processing logic"""
        if task_type == "scan_codebase":
            return await self._scan_codebase(task_data)
        else:
            return {"status": "error", "message": f"Unknown task type: {task_type}"}

    async def _scan_codebase(self, task_data):
        """Scan a codebase for security vulnerabilities"""
        codebase = task_data.get("codebase")
        if not codebase:
            return {"status": "error", "message": "No codebase provided"}

        try:
            # Scan the codebase
            vulnerabilities = await self.codeshield_service.analyze_codebase(codebase)

            # Format the result
            result = {
                "status": "success",
                "job_id": task_data.get("job_id"),
                "codebase_id": task_data.get("codebase_id"),
                "vulnerabilities": vulnerabilities,
            }

            return result
        except Exception as e:
            self.logger.error(f"Error scanning codebase: {e}")
            return {
                "status": "error",
                "message": str(e),
                "job_id": task_data.get("job_id"),
                "codebase_id": task_data.get("codebase_id"),
            }


@pytest.fixture
def redflag_agent():
    """Create a RedFlag agent for testing"""
    agent = SimplifiedRedFlagAgent("redflag_agent", {"api_key": "test-key"})

    # Mock the RedFlagService
    mock_service = MagicMock()
    mock_service.analyze_codebase = AsyncMock()
    agent.redflag_service = mock_service

    return agent


class TestSimplifiedRedFlagIntegration:
    """Test the simplified RedFlag integration"""

    def test_agent_initialization(self, redflag_agent):
        """Test agent initialization"""
        assert redflag_agent.id == "redflag_agent"
        assert redflag_agent.model.agent_type == "redflag"
        assert redflag_agent.model.config["api_key"] == "test-key"

    @pytest.mark.asyncio
    async def test_scan_codebase(self, redflag_agent):
        """Test scanning a codebase with RedFlag"""
        # Set up the mock service
        redflag_agent.redflag_service.analyze_codebase.return_value = [
            {
                "id": "vuln-1",
                "vulnerability_type": "SQL Injection",
                "cwe_id": "CWE-89",
                "description": "SQL injection vulnerability",
                "file_path": "app.py",
                "line_numbers": [10],
                "severity": "High",
            }
        ]

        # Create a test codebase
        codebase = {
            "id": "test-codebase",
            "files": {"app.py": "print('Hello, world!')"},
        }

        # Create a test task
        task_data = {
            "job_id": "test-job",
            "codebase_id": "test-codebase",
            "codebase": codebase,
        }

        # Process the task
        result = await redflag_agent._scan_codebase(task_data)

        # Check the result
        assert result["status"] == "success"
        assert result["job_id"] == "test-job"
        assert result["codebase_id"] == "test-codebase"
        assert len(result["vulnerabilities"]) == 1
        assert result["vulnerabilities"][0]["vulnerability_type"] == "SQL Injection"

        # Check that the service was called
        redflag_agent.redflag_service.analyze_codebase.assert_called_once_with(codebase)


@pytest.fixture
def codeshield_agent():
    """Create a CodeShield agent for testing"""
    agent = SimplifiedCodeShieldAgent("codeshield_agent", {"api_key": "test-key"})

    # Mock the CodeShieldService
    mock_service = MagicMock()
    mock_service.analyze_codebase = AsyncMock()
    agent.codeshield_service = mock_service

    return agent


class TestSimplifiedCodeShieldIntegration:
    """Test the simplified CodeShield integration"""

    def test_agent_initialization(self, codeshield_agent):
        """Test agent initialization"""
        assert codeshield_agent.id == "codeshield_agent"
        assert codeshield_agent.model.agent_type == "codeshield"
        assert codeshield_agent.model.config["api_key"] == "test-key"

    @pytest.mark.asyncio
    async def test_scan_codebase(self, codeshield_agent):
        """Test scanning a codebase with CodeShield"""
        # Set up the mock service
        codeshield_agent.codeshield_service.analyze_codebase.return_value = [
            {
                "id": "vuln-1",
                "vulnerability_type": "Cross-Site Scripting",
                "cwe_id": "CWE-79",
                "description": "XSS vulnerability",
                "file_path": "app.js",
                "line_numbers": [15],
                "severity": "Medium",
            }
        ]

        # Create a test codebase
        codebase = {
            "id": "test-codebase",
            "files": {"app.js": "console.log('Hello, world!');"},
        }

        # Create a test task
        task_data = {
            "job_id": "test-job",
            "codebase_id": "test-codebase",
            "codebase": codebase,
        }

        # Process the task
        result = await codeshield_agent._scan_codebase(task_data)

        # Check the result
        assert result["status"] == "success"
        assert result["job_id"] == "test-job"
        assert result["codebase_id"] == "test-codebase"
        assert len(result["vulnerabilities"]) == 1
        assert (
            result["vulnerabilities"][0]["vulnerability_type"] == "Cross-Site Scripting"
        )

        # Check that the service was called
        codeshield_agent.codeshield_service.analyze_codebase.assert_called_once_with(
            codebase
        )


@pytest.fixture
def redflag_service():
    """Create a RedFlag service for testing"""
    return RedFlagService(api_key="test-key")


@pytest.fixture
def codeshield_service():
    """Create a CodeShield service for testing"""
    return CodeShieldService(api_key="test-key")


class TestRedFlagService:
    """Test the RedFlagService class"""

    def test_initialization(self, redflag_service):
        """Test initialization"""
        assert redflag_service.api_key == "test-key"
        assert redflag_service.logger is not None
        assert hasattr(redflag_service, "initialized")

    @pytest.mark.asyncio
    @patch("autothreats.utils.redflag_service.RedFlagService.analyze_codebase")
    async def test_analyze_codebase(self, mock_analyze_codebase, redflag_service):
        """Test analyzing a codebase"""
        # Set up the mock
        mock_analyze_codebase.return_value = [
            {
                "id": "vuln-1",
                "vulnerability_type": "SQL Injection",
                "cwe_id": "CWE-89",
                "description": "SQL injection vulnerability",
                "file_path": "app.py",
                "line_numbers": [10],
                "severity": "High",
            }
        ]

        # Create a test codebase
        codebase = {
            "id": "test-codebase",
            "files": {"app.py": "print('Hello, world!')"},
        }

        # Analyze the codebase
        result = await redflag_service.analyze_codebase(codebase)

        # Check the result
        assert len(result) == 1
        assert result[0]["vulnerability_type"] == "SQL Injection"


class TestCodeShieldService:
    """Test the CodeShieldService class"""

    def test_initialization(self, codeshield_service):
        """Test initialization"""
        assert codeshield_service.api_key == "test-key"
        assert codeshield_service.logger is not None
        assert hasattr(codeshield_service, "initialized")

    @pytest.mark.asyncio
    @patch("autothreats.utils.codeshield_service.CodeShieldService.analyze_codebase")
    async def test_analyze_codebase(self, mock_analyze_codebase, codeshield_service):
        """Test analyzing a codebase"""
        # Set up the mock
        mock_analyze_codebase.return_value = [
            {
                "id": "vuln-1",
                "vulnerability_type": "Cross-Site Scripting",
                "cwe_id": "CWE-79",
                "description": "XSS vulnerability",
                "file_path": "app.js",
                "line_numbers": [15],
                "severity": "Medium",
            }
        ]

        # Create a test codebase
        codebase = {
            "id": "test-codebase",
            "files": {"app.js": "console.log('Hello, world!');"},
        }

        # Analyze the codebase
        result = await codeshield_service.analyze_codebase(codebase)

        # Check the result
        assert len(result) == 1
        assert result[0]["vulnerability_type"] == "Cross-Site Scripting"


if __name__ == "__main__":
    pytest.main()
