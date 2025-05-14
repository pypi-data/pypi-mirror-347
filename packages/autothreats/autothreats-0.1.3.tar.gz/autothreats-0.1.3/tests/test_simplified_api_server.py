#!/usr/bin/env python3
"""
Tests for the simplified API server
"""

import asyncio
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

# Use a relative import
from .async_test_base import AsyncTestCase, async_test

# Add the parent directory to the path so we can import the autothreats package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from autothreats.simplified_api_server import (
    create_app,
    initialize_orchestrator,
    job_statuses,
    run_analysis_task,
    send_sse_event,
    sse_clients,
)


class TestSimplifiedAPIServer(AsyncTestCase):
    """Test the simplified API server"""

    async def asyncSetUp(self):
        """Set up the test"""
        # Create the application
        self.app = await create_app()
        # Create a test server
        self.server = TestServer(self.app)
        # Create a test client
        self.client = TestClient(self.server)
        # Start the server
        await self.server.start_server()
        # Clear job statuses and SSE clients
        job_statuses.clear()
        sse_clients.clear()

    async def asyncTearDown(self):
        """Clean up after the test"""
        # Close the client and server
        await self.client.close()
        await self.server.close()

    @async_test
    async def test_index(self):
        """Test the index route"""
        resp = await self.client.get("/")
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertEqual(text, "Simplified Threat Canvas API Server")

    @async_test
    @patch("autothreats.simplified_api_server.orchestrator")
    async def test_run_analysis(self, mock_orchestrator):
        """Test the run analysis route"""
        # Mock the orchestrator
        mock_orchestrator.process_job = MagicMock(return_value=asyncio.Future())
        mock_orchestrator.process_job.return_value.set_result(None)

        # Test data
        data = {
            "repository": {
                "url": "https://github.com/example/repo",
                "type": "github",
                "branch": "main",
                "local_path": "/path/to/repo",
            },
            "system": {
                "enable_agentic_improvements": True,
                "lightweight": False,
                "enable_multi_stage": False,
            },
            "agents": {},
            "security_tools": {},
            "output_dir": "./results",
        }

        # Make the request
        resp = await self.client.post("/api/analysis/run", json=data)
        self.assertEqual(resp.status, 200)

        # Check the response
        response_data = await resp.json()
        self.assertTrue(response_data["success"])
        self.assertIn("jobId", response_data)
        self.assertEqual(response_data["message"], "Analysis started successfully")

    @async_test
    async def test_get_analysis_progress(self):
        """Test the get analysis progress route"""
        # Create a job status
        job_id = "test-job-123"
        job_statuses[job_id] = {
            "job_id": job_id,
            "status": "running",
            "progress_percentage": 50,
            "current_stage": "Testing",
            "start_time": 1234567890,
        }

        # Make the request
        resp = await self.client.get(f"/api/analysis/progress?jobId={job_id}")
        self.assertEqual(resp.status, 200)

        # Check the response
        response_data = await resp.json()
        self.assertEqual(response_data["job_id"], job_id)
        self.assertEqual(response_data["status"], "running")
        self.assertEqual(response_data["progress_percentage"], 50)
        self.assertEqual(response_data["current_stage"], "Testing")
        self.assertEqual(response_data["start_time"], 1234567890)

    @async_test
    async def test_get_analysis_progress_not_found(self):
        """Test the get analysis progress route with a non-existent job"""
        # Make the request
        resp = await self.client.get("/api/analysis/progress?jobId=non-existent")
        self.assertEqual(resp.status, 404)

        # Check the response
        response_data = await resp.json()
        self.assertIn("error", response_data)

    @async_test
    async def test_get_threat_model_mock(self):
        """Test the get threat model route with mock data"""
        # Make the request
        resp = await self.client.get("/api/threat-model?jobId=latest")
        self.assertEqual(resp.status, 200)

        # Check the response
        response_data = await resp.json()
        self.assertIn("id", response_data)
        self.assertIn("title", response_data)
        self.assertIn("vulnerabilities", response_data)
        self.assertIn("threat_scenarios", response_data)

    @async_test
    async def test_sse_events(self):
        """Test the SSE events route"""
        # Create a job status
        job_id = "test-job-123"
        job_statuses[job_id] = {
            "job_id": job_id,
            "status": "running",
            "progress_percentage": 50,
            "current_stage": "Testing",
            "start_time": 1234567890,
        }

        # Start a request to the SSE endpoint
        resp = await self.client.get(f"/api/events?jobId={job_id}")
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.headers["Content-Type"], "text/event-stream")
        self.assertEqual(resp.headers["Cache-Control"], "no-cache")
        self.assertEqual(resp.headers["Connection"], "keep-alive")

        # Check that the client was added to sse_clients
        self.assertIn(job_id, sse_clients)
        self.assertEqual(len(sse_clients[job_id]), 1)

        # Read the initial response which should contain the status event
        response_data = await resp.content.read(1024)
        response_text = response_data.decode("utf-8")

        # Check the response contains the status event
        self.assertIn("event: status", response_text)
        self.assertIn(f"data: {json.dumps(job_statuses[job_id])}", response_text)

    @async_test
    async def test_send_sse_event(self):
        """Test the send_sse_event function"""
        # Create a mock client
        mock_client = MagicMock()
        mock_client.write = MagicMock(return_value=asyncio.Future())
        mock_client.write.return_value.set_result(None)

        # Add the client to sse_clients
        job_id = "test-job-123"
        sse_clients[job_id] = {mock_client}

        # Send an event
        event_data = {"test": "data"}
        await send_sse_event(job_id, "test_event", event_data)

        # Check that the client was called with the correct data
        expected_data = f"event: test_event\ndata: {json.dumps(event_data)}\n\n".encode(
            "utf-8"
        )
        mock_client.write.assert_called_once_with(expected_data)

    @async_test
    async def test_send_sse_event_client_error(self):
        """Test the send_sse_event function with a client error"""
        # Create a mock client that raises an error
        mock_client = MagicMock()
        mock_client.write = MagicMock(
            side_effect=ConnectionResetError("Connection reset")
        )

        # Add the client to sse_clients
        job_id = "test-job-123"
        sse_clients[job_id] = {mock_client}

        # Send an event
        event_data = {"test": "data"}
        await send_sse_event(job_id, "test_event", event_data)

        # Check that the client was removed from sse_clients
        self.assertEqual(len(sse_clients[job_id]), 0)

    @async_test
    async def test_get_organization_parameters(self):
        """Test the get organization parameters route"""
        # Make the request
        resp = await self.client.get("/api/organization-parameters")
        self.assertEqual(resp.status, 200)

        # Check the response
        response_data = await resp.json()
        self.assertIn("security_controls", response_data)
        self.assertIn("compliance_requirements", response_data)
        self.assertIn("risk_tolerance", response_data)

    @async_test
    async def test_update_organization_parameters(self):
        """Test the update organization parameters route"""
        # Test data
        data = {
            "security_controls": {
                "multi_factor_authentication": {
                    "implemented": True,
                    "strength": "high",
                    "description": "MFA is required for all access",
                },
            },
            "compliance_requirements": ["PCI DSS", "GDPR", "HIPAA"],
            "risk_tolerance": "low",
        }

        # Create a temporary file for testing
        params_path = os.path.join(".", "organization-parameters.yaml")
        original_exists = os.path.exists(params_path)
        original_content = None
        if original_exists:
            with open(params_path, "r") as f:
                original_content = f.read()

        try:
            # Make the request
            resp = await self.client.post("/api/organization-parameters", json=data)
            self.assertEqual(resp.status, 200)

            # Check the response
            response_data = await resp.json()
            self.assertTrue(response_data["success"])

            # Check that the file was created
            self.assertTrue(os.path.exists(params_path))

            # Check the file content
            import yaml

            with open(params_path, "r") as f:
                file_data = yaml.safe_load(f)
                self.assertEqual(
                    file_data["security_controls"]["multi_factor_authentication"][
                        "strength"
                    ],
                    "high",
                )
                self.assertEqual(file_data["risk_tolerance"], "low")
                self.assertIn("HIPAA", file_data["compliance_requirements"])

        finally:
            # Restore the original file
            if original_exists and original_content is not None:
                with open(params_path, "w") as f:
                    f.write(original_content)
            elif os.path.exists(params_path):
                os.remove(params_path)

    @async_test
    @patch("autothreats.simplified_api_server.SimplifiedOrchestrator")
    @patch("autothreats.simplified_api_server.asyncio.sleep")
    async def test_monitor_progress(self, mock_sleep, MockOrchestrator):
        """Test the _monitor_progress function"""
        # Import the function
        from autothreats.simplified_api_server import _monitor_progress

        # Mock asyncio.sleep to avoid waiting in tests
        mock_sleep.return_value = None

        # Mock the orchestrator
        mock_orchestrator = MagicMock()
        mock_orchestrator.initialize = MagicMock(return_value=asyncio.Future())
        mock_orchestrator.initialize.return_value.set_result(None)
        mock_orchestrator.process_job = MagicMock(return_value=asyncio.Future())
        mock_orchestrator.process_job.return_value.set_result(
            {
                "status": "success",
                "results": {
                    "threat_detection": {
                        "vulnerabilities": [
                            {
                                "id": "vuln-1",
                                "type": "sql_injection",
                                "file_path": "src/auth/login.js",
                                "line": 42,
                                "severity": "high",
                                "confidence": 0.8,
                                "description": "SQL injection vulnerability",
                                "remediation": "Use parameterized queries",
                            }
                        ]
                    },
                    "executive_summary": "Test executive summary",
                },
            }
        )
        mock_orchestrator.shutdown = MagicMock(return_value=asyncio.Future())
        mock_orchestrator.shutdown.return_value.set_result(None)
        MockOrchestrator.return_value = mock_orchestrator

        # Create job data
        job_id = "test-job-123"
        orchestrator_config = {
            "log_level": "INFO",
            "threat_detection": {
                "llm_provider": "openai",
                "openai_model": "gpt-4o-mini",
            },
            "enable_multi_stage": False,
            "enable_agentic": True,
            "system": {
                "debug_logging": False,
                "lightweight": False,
                "max_scan_dirs": 1000,
            },
        }
        job_data = {
            "job_id": job_id,
            "codebase_id": f"codebase_{job_id}",
            "codebase": {
                "files": {"src/auth/login.js": "function login() { /* code */ }"}
            },
            "context": {
                "lightweight": False,
                "enable_multi_stage": False,
                "enable_redflag": False,
                "enable_codeshield": False,
                "enable_agentic": True,
            },
        }

        # Create job status
        job_statuses[job_id] = {
            "job_id": job_id,
            "status": "running",
            "progress_percentage": 15,
            "current_stage": "Starting analysis",
            "start_time": 1234567890,
            "output_dir": "./results",
        }

        # Create a temporary directory for output
        output_dir = "./results"
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Run the function
            await _monitor_progress(job_id, orchestrator_config, job_data)

            # Check that the orchestrator was initialized and used
            MockOrchestrator.assert_called_once_with(orchestrator_config)
            mock_orchestrator.initialize.assert_called_once()
            mock_orchestrator.process_job.assert_called_once_with(job_data)
            mock_orchestrator.shutdown.assert_called_once()

            # Check that the job status was updated
            self.assertEqual(job_statuses[job_id]["status"], "complete")
            self.assertEqual(job_statuses[job_id]["progress_percentage"], 100)
            self.assertEqual(job_statuses[job_id]["current_stage"], "Complete")
            self.assertIn("end_time", job_statuses[job_id])
            self.assertIn("threat_model_path", job_statuses[job_id])
            self.assertIn("html_report_path", job_statuses[job_id])

            # Check that the files were created
            job_dir = os.path.join(output_dir, job_id)
            json_path = os.path.join(job_dir, f"threat_model_{job_id}.json")
            html_path = os.path.join(job_dir, f"threat_model_{job_id}.html")
            self.assertTrue(os.path.exists(json_path))
            self.assertTrue(os.path.exists(html_path))

            # Check the file content
            with open(json_path, "r") as f:
                threat_model = json.load(f)
                self.assertEqual(threat_model["job_id"], job_id)
                self.assertEqual(len(threat_model["vulnerabilities"]), 1)
                self.assertEqual(
                    threat_model["vulnerabilities"][0]["type"], "sql_injection"
                )
                self.assertEqual(
                    threat_model["executive_summary"], "Test executive summary"
                )

        finally:
            # Clean up the files
            job_dir = os.path.join(output_dir, job_id)
            json_path = os.path.join(job_dir, f"threat_model_{job_id}.json")
            html_path = os.path.join(job_dir, f"threat_model_{job_id}.html")
            if os.path.exists(json_path):
                os.remove(json_path)
            if os.path.exists(html_path):
                os.remove(html_path)


if __name__ == "__main__":
    unittest.main()
