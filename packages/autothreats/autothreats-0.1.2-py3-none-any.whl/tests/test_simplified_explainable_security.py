#!/usr/bin/env python3
"""
Tests for the simplified explainable security component.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.agentic.simplified_explainable_security import (
    SimplifiedExplainableSecurity,
)
from autothreats.simplified_base import SharedWorkspace


class TestSimplifiedExplainableSecurity(unittest.TestCase):
    """Test the SimplifiedExplainableSecurity class"""

    def setUp(self):
        """Set up the test"""
        # Create a mock workspace
        self.mock_workspace = MagicMock(spec=SharedWorkspace)
        self.mock_workspace.get_data = MagicMock(return_value=None)
        self.mock_workspace.store_data = MagicMock()
        self.mock_workspace.get_cached_analysis = MagicMock(return_value=None)
        self.mock_workspace.cache_analysis = MagicMock()

        # Create a mock LLM service
        self.mock_llm_service = MagicMock()
        self.mock_llm_service.generate_text_async = AsyncMock(
            return_value="""
        {
            "detailed_explanation": "This is a SQL injection vulnerability that allows an attacker to execute arbitrary SQL commands.",
            "exploitation_vector": "An attacker can inject malicious SQL code through user input fields.",
            "potential_impact": "Data theft, data manipulation, unauthorized access.",
            "remediation": "Use parameterized queries and input validation.",
            "code_fix_example": "Use prepared statements instead of string concatenation."
        }
        """
        )

        # Set up the workspace to return the LLM service
        self.mock_workspace.get_data.side_effect = lambda key: (
            self.mock_llm_service if key == "llm_service" else None
        )

        # Create the explainable security component
        self.explainable_security = SimplifiedExplainableSecurity(self.mock_workspace)

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.explainable_security.workspace, self.mock_workspace)
        self.assertIsNotNone(self.explainable_security.logger)
        self.assertEqual(self.explainable_security.llm_service, self.mock_llm_service)
        self.assertEqual(self.explainable_security.explanation_cache, {})

    def test_get_standard_explanation(self):
        """Test getting standard explanations"""
        # Test SQL injection explanation
        sql_explanation = self.explainable_security._get_standard_explanation(
            "sql_injection", "high"
        )
        self.assertIn("SQL Injection", sql_explanation)
        self.assertIn("Exploitation:", sql_explanation)
        self.assertIn("Impact:", sql_explanation)
        self.assertIn("Remediation:", sql_explanation)

        # Test XSS explanation
        xss_explanation = self.explainable_security._get_standard_explanation(
            "xss", "medium"
        )
        self.assertIn("Cross-Site Scripting", xss_explanation)

        # Test unknown vulnerability with high severity
        high_explanation = self.explainable_security._get_standard_explanation(
            "unknown", "high"
        )
        self.assertIn("high severity", high_explanation)

        # Test unknown vulnerability with medium severity
        medium_explanation = self.explainable_security._get_standard_explanation(
            "unknown", "medium"
        )
        self.assertIn("medium severity", medium_explanation)

        # Test unknown vulnerability with low severity
        low_explanation = self.explainable_security._get_standard_explanation(
            "unknown", "low"
        )
        self.assertIn("low severity", low_explanation)

    async def _test_explain_vulnerability(self):
        """Test explaining a vulnerability"""
        # Create a test vulnerability
        vulnerability = {
            "id": "vuln-1",
            "type": "sql_injection",
            "file_path": "auth/login.py",
            "line": 10,
            "code": 'query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"',
            "confidence": 0.8,
            "severity": "high",
            "description": "SQL injection vulnerability in login function",
        }

        # Explain the vulnerability
        explained_vuln = await self.explainable_security._explain_vulnerability(
            vulnerability, "test_job"
        )

        # Check the results
        self.assertEqual(explained_vuln["id"], "vuln-1")
        self.assertEqual(explained_vuln["type"], "sql_injection")
        self.assertIn("detailed_explanation", explained_vuln)
        self.assertIn("exploitation_vector", explained_vuln)
        self.assertIn("potential_impact", explained_vuln)
        self.assertIn("remediation", explained_vuln)
        self.assertIn("code_fix_example", explained_vuln)

    async def _test_explain_vulnerability_with_error(self):
        """Test explaining a vulnerability with an error"""
        # Create a test vulnerability
        vulnerability = {
            "id": "vuln-1",
            "type": "sql_injection",
            "file_path": "auth/login.py",
            "line": 10,
            "code": 'query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"',
            "confidence": 0.8,
            "severity": "high",
            "description": "SQL injection vulnerability in login function",
        }

        # Make the LLM service raise an exception
        self.mock_llm_service.generate_text_async.side_effect = Exception("Test error")

        # Explain the vulnerability
        explained_vuln = await self.explainable_security._explain_vulnerability(
            vulnerability, "test_job"
        )

        # Check the results
        self.assertEqual(explained_vuln["id"], "vuln-1")
        self.assertEqual(explained_vuln["type"], "sql_injection")
        self.assertIn(
            "detailed_explanation", explained_vuln
        )  # Should fall back to standard explanation

    async def _test_explain_vulnerabilities(self):
        """Test explaining multiple vulnerabilities"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "code": 'query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"',
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability in login function",
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "code": "element.innerHTML = userInput",
                "confidence": 0.7,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability in form",
            },
        ]

        # Reset the LLM service mock
        self.mock_llm_service.generate_text_async.side_effect = None
        self.mock_llm_service.generate_text_async.reset_mock()

        # Explain the vulnerabilities
        explained_vulnerabilities = (
            await self.explainable_security.explain_vulnerabilities(
                vulnerabilities, "test_job"
            )
        )

        # Check the results
        self.assertEqual(len(explained_vulnerabilities), 2)
        self.assertIn("detailed_explanation", explained_vulnerabilities[0])
        self.assertIn("detailed_explanation", explained_vulnerabilities[1])

        # Check that the LLM service was called twice (once for each vulnerability)
        self.assertEqual(self.mock_llm_service.generate_text_async.call_count, 2)

    def _generate_standard_summary(self):
        """Test generating a standard summary"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability in login function",
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.7,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability in form",
            },
            {
                "id": "vuln-3",
                "type": "csrf",
                "file_path": "api/endpoint.py",
                "line": 30,
                "confidence": 0.6,
                "severity": "low",
                "description": "CSRF vulnerability in API endpoint",
            },
        ]

        # Calculate severity counts
        severity_counts = {
            "critical": 0,
            "high": 1,
            "medium": 1,
            "low": 1,
            "info": 0,
        }

        # Calculate top vulnerability types
        top_types = [
            ("sql_injection", 1),
            ("xss", 1),
            ("csrf", 1),
        ]

        # Generate standard summary
        summary = self.explainable_security._generate_standard_summary(
            vulnerabilities, severity_counts, top_types
        )

        # Check the results
        self.assertIn("Executive Security Summary", summary)
        self.assertIn("Vulnerability Breakdown", summary)
        self.assertIn("Key Risk Areas", summary)
        self.assertIn("Recommendations", summary)

        # Check that the risk level is correct
        self.assertIn("Moderate to High Risk Level", summary)

        # Check that the vulnerability counts are correct
        self.assertIn("**High**: 1", summary)
        self.assertIn("**Medium**: 1", summary)
        self.assertIn("**Low**: 1", summary)

    async def _test_generate_executive_summary(self):
        """Test generating an executive summary"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability in login function",
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.7,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability in form",
            },
        ]

        # Set up the LLM service to return an executive summary
        self.mock_llm_service.generate_text_async.reset_mock()
        self.mock_llm_service.generate_text_async.return_value = """
        # Executive Security Summary
        
        ## Overview
        The security analysis identified 2 vulnerabilities in the codebase, representing a Moderate to High Risk Level.
        
        ## Key Findings
        - SQL Injection vulnerability in the authentication system
        - Cross-site scripting vulnerability in the user interface
        
        ## Recommendations
        1. Implement parameterized queries for database operations
        2. Apply proper output encoding for user-generated content
        """

        # Generate executive summary
        summary = await self.explainable_security.generate_executive_summary(
            vulnerabilities, "test_job"
        )

        # Check the results
        self.assertIn("Executive Security Summary", summary)
        self.assertIn("Overview", summary)
        self.assertIn("Key Findings", summary)
        self.assertIn("Recommendations", summary)
        self.assertIn("Moderate to High Risk Level", summary)

        # Check that the LLM service was called
        self.mock_llm_service.generate_text_async.assert_called_once()

    async def _test_generate_executive_summary_with_error(self):
        """Test generating an executive summary with an error"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability in login function",
            }
        ]

        # Make the LLM service raise an exception
        self.mock_llm_service.generate_text_async.side_effect = Exception("Test error")

        # Generate executive summary
        summary = await self.explainable_security.generate_executive_summary(
            vulnerabilities, "test_job"
        )

        # Check the results
        self.assertIn(
            "Executive Security Summary", summary
        )  # Should fall back to standard summary

    def test_async_methods(self):
        """Test async methods"""
        # Create a new event loop for this test
        old_loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Test explain_vulnerability
            loop.run_until_complete(self._test_explain_vulnerability())

            # Test explain_vulnerability with error
            loop.run_until_complete(self._test_explain_vulnerability_with_error())

            # Test explain_vulnerabilities
            loop.run_until_complete(self._test_explain_vulnerabilities())

            # Test generate_executive_summary
            loop.run_until_complete(self._test_generate_executive_summary())

            # Test generate_executive_summary with error
            loop.run_until_complete(self._test_generate_executive_summary_with_error())

            # Test generate_standard_summary
            self._generate_standard_summary()
        finally:
            # Clean up the loop
            loop.close()
            asyncio.set_event_loop(old_loop)


if __name__ == "__main__":
    unittest.main()
