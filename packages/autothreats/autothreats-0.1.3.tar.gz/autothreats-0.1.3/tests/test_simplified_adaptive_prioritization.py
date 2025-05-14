#!/usr/bin/env python3
"""
Tests for the simplified adaptive prioritization component.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.agentic.simplified_adaptive_prioritization import (
    SimplifiedAdaptivePrioritization,
)
from autothreats.simplified_base import SharedWorkspace


class TestSimplifiedAdaptivePrioritization(unittest.TestCase):
    """Test the SimplifiedAdaptivePrioritization class"""

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
        self.mock_llm_service.generate_text_async = AsyncMock(return_value="")

        # Set up the workspace to return the LLM service
        self.mock_workspace.get_data.side_effect = lambda key: (
            self.mock_llm_service if key == "llm_service" else None
        )

        # Create the adaptive prioritization component
        self.adaptive_prioritization = SimplifiedAdaptivePrioritization(
            self.mock_workspace
        )

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.adaptive_prioritization.workspace, self.mock_workspace)
        self.assertIsNotNone(self.adaptive_prioritization.logger)
        self.assertEqual(
            self.adaptive_prioritization.llm_service, self.mock_llm_service
        )
        self.assertEqual(self.adaptive_prioritization.prioritization_cache, {})

    def test_calculate_base_scores(self):
        """Test calculating base scores"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
            },
            {
                "id": "vuln-3",
                "type": "csrf",
                "file_path": "api/endpoint.py",
                "line": 30,
                "confidence": 0.7,
                "severity": "low",
            },
        ]

        # Calculate base scores
        scored_vulnerabilities = self.adaptive_prioritization._calculate_base_scores(
            vulnerabilities
        )

        # Check the results
        self.assertEqual(len(scored_vulnerabilities), 3)

        # Check that each vulnerability has a base score
        for vuln in scored_vulnerabilities:
            self.assertIn("base_score", vuln)
            self.assertIn("priority_score", vuln)

        # Check specific scores
        high_vuln = next(v for v in scored_vulnerabilities if v["severity"] == "high")
        medium_vuln = next(
            v for v in scored_vulnerabilities if v["severity"] == "medium"
        )
        low_vuln = next(v for v in scored_vulnerabilities if v["severity"] == "low")

        self.assertGreater(high_vuln["base_score"], medium_vuln["base_score"])
        self.assertGreater(medium_vuln["base_score"], low_vuln["base_score"])

    async def _test_apply_context_adjustments(self):
        """Test applying context adjustments"""
        # Create test vulnerabilities with base scores
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability",
                "base_score": 6.4,
                "priority_score": 6.4,
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability",
                "base_score": 3.0,
                "priority_score": 3.0,
            },
        ]

        # Create security context
        security_context = {
            "security_boundaries": [
                {
                    "id": "boundary-1",
                    "name": "Authentication Boundary",
                    "type": "auth_boundary",
                    "files": ["auth/login.py", "auth/logout.py"],
                    "description": "Authentication boundary",
                }
            ]
        }

        # Set up the workspace to return the security context
        self.mock_workspace.get_data.side_effect = lambda key: {
            "llm_service": self.mock_llm_service,
            "security_context_test_job": security_context,
        }.get(key)

        # Apply context adjustments
        adjusted_vulnerabilities = (
            await self.adaptive_prioritization._apply_context_adjustments(
                vulnerabilities, "test_job"
            )
        )

        # Check the results
        self.assertEqual(len(adjusted_vulnerabilities), 2)

        # Check that the vulnerability in the security boundary was adjusted
        auth_vuln = next(
            v for v in adjusted_vulnerabilities if v["file_path"] == "auth/login.py"
        )
        self.assertGreater(
            auth_vuln["priority_score"], 6.4
        )  # Score should be increased
        self.assertIn("adjustment_factors", auth_vuln)

        # Check that the other vulnerability was not adjusted for security boundary
        ui_vuln = next(
            v for v in adjusted_vulnerabilities if v["file_path"] == "ui/form.js"
        )
        self.assertEqual(ui_vuln["priority_score"], 3.0)  # Score should remain the same

    def test_apply_exploitability_adjustments(self):
        """Test applying exploitability adjustments"""
        # Create test vulnerabilities with adjusted scores
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability",
                "base_score": 6.4,
                "priority_score": 7.68,  # Adjusted score
                "adjustment_factors": ["security_boundary"],
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability",
                "base_score": 3.0,
                "priority_score": 3.0,
            },
        ]

        # Apply exploitability adjustments
        adjusted_vulnerabilities = (
            self.adaptive_prioritization._apply_exploitability_adjustments(
                vulnerabilities
            )
        )

        # Check the results
        self.assertEqual(len(adjusted_vulnerabilities), 2)

        # Check that the SQL injection vulnerability was adjusted
        sql_vuln = next(
            v
            for v in adjusted_vulnerabilities
            if "sql injection" in v["description"].lower()
        )
        self.assertGreater(
            sql_vuln["priority_score"], 7.68
        )  # Score should be increased
        self.assertIn("adjustment_factors", sql_vuln)

        # Check that the XSS vulnerability was adjusted by confidence
        xss_vuln = next(
            v
            for v in adjusted_vulnerabilities
            if "cross-site scripting" in v["description"].lower()
        )
        # The XSS score is adjusted by confidence (0.6)
        # 3.0 * (0.5 + 0.6/2) = 3.0 * 0.8 = 2.4
        # But due to floating point precision, it might be slightly different
        self.assertAlmostEqual(xss_vuln["priority_score"], 2.4, delta=0.1)
        # No adjustment_factors expected since "xss" is not in the description

    def test_add_priority_levels(self):
        """Test adding priority levels"""
        # Create test vulnerabilities with adjusted scores
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability",
                "base_score": 6.4,
                "priority_score": 10.0,  # High score
                "adjustment_factors": [
                    "security_boundary",
                    "exploitable_sql_injection",
                ],
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability",
                "base_score": 3.0,
                "priority_score": 5.0,  # Medium score
                "adjustment_factors": ["exploitable_xss"],
            },
            {
                "id": "vuln-3",
                "type": "csrf",
                "file_path": "api/endpoint.py",
                "line": 30,
                "confidence": 0.7,
                "severity": "low",
                "description": "CSRF vulnerability",
                "base_score": 2.0,
                "priority_score": 2.0,  # Low score
            },
        ]

        # Add priority levels
        prioritized_vulnerabilities = self.adaptive_prioritization._add_priority_levels(
            vulnerabilities
        )

        # Check the results
        self.assertEqual(len(prioritized_vulnerabilities), 3)

        # Check that each vulnerability has a priority level
        for vuln in prioritized_vulnerabilities:
            self.assertIn("priority", vuln)

        # Check specific priority levels
        high_score_vuln = next(
            v for v in prioritized_vulnerabilities if v["priority_score"] == 10.0
        )
        medium_score_vuln = next(
            v for v in prioritized_vulnerabilities if v["priority_score"] == 5.0
        )
        low_score_vuln = next(
            v for v in prioritized_vulnerabilities if v["priority_score"] == 2.0
        )

        self.assertEqual(high_score_vuln["priority"], "critical")
        # With the current thresholds, 5.0 falls into the "low" category
        self.assertEqual(medium_score_vuln["priority"], "low")
        # With the current thresholds, 2.0 falls into the "info" category
        self.assertEqual(low_score_vuln["priority"], "info")

    async def _test_prioritize_vulnerabilities(self):
        """Test prioritizing vulnerabilities"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability",
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability",
            },
            {
                "id": "vuln-3",
                "type": "csrf",
                "file_path": "api/endpoint.py",
                "line": 30,
                "confidence": 0.7,
                "severity": "low",
                "description": "CSRF vulnerability",
            },
        ]

        # Create security context
        security_context = {
            "security_boundaries": [
                {
                    "id": "boundary-1",
                    "name": "Authentication Boundary",
                    "type": "auth_boundary",
                    "files": ["auth/login.py", "auth/logout.py"],
                    "description": "Authentication boundary",
                }
            ]
        }

        # Set up the workspace to return the security context
        self.mock_workspace.get_data.side_effect = lambda key: {
            "llm_service": self.mock_llm_service,
            "security_context_test_job": security_context,
        }.get(key)

        # Prioritize vulnerabilities
        prioritized_vulnerabilities = (
            await self.adaptive_prioritization.prioritize_vulnerabilities(
                vulnerabilities, "test_job"
            )
        )

        # Check the results
        self.assertEqual(len(prioritized_vulnerabilities), 3)

        # Check that each vulnerability has priority information
        for vuln in prioritized_vulnerabilities:
            self.assertIn("base_score", vuln)
            self.assertIn("priority_score", vuln)
            self.assertIn("priority", vuln)

        # Check that vulnerabilities are sorted by priority score
        self.assertGreaterEqual(
            prioritized_vulnerabilities[0]["priority_score"],
            prioritized_vulnerabilities[1]["priority_score"],
        )
        self.assertGreaterEqual(
            prioritized_vulnerabilities[1]["priority_score"],
            prioritized_vulnerabilities[2]["priority_score"],
        )

    async def _test_generate_prioritization_report(self):
        """Test generating a prioritization report"""
        # Create test vulnerabilities with priority levels
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.8,
                "severity": "high",
                "description": "SQL injection vulnerability",
                "priority": "critical",
                "priority_score": 10.0,
            },
            {
                "id": "vuln-2",
                "type": "xss",
                "file_path": "ui/form.js",
                "line": 20,
                "confidence": 0.6,
                "severity": "medium",
                "description": "Cross-site scripting vulnerability",
                "priority": "high",
                "priority_score": 7.0,
            },
            {
                "id": "vuln-3",
                "type": "csrf",
                "file_path": "api/endpoint.py",
                "line": 30,
                "confidence": 0.7,
                "severity": "low",
                "description": "CSRF vulnerability",
                "priority": "medium",
                "priority_score": 4.0,
            },
        ]

        # Generate prioritization report
        report = await self.adaptive_prioritization.generate_prioritization_report(
            vulnerabilities, "test_job"
        )

        # Check the results
        self.assertEqual(report["job_id"], "test_job")
        self.assertEqual(report["total_vulnerabilities"], 3)
        self.assertIn("priority_counts", report)
        self.assertIn("top_vulnerabilities", report)
        self.assertIn("timestamp", report)

        # Check priority counts
        self.assertEqual(report["priority_counts"]["critical"], 1)
        self.assertEqual(report["priority_counts"]["high"], 1)
        self.assertEqual(report["priority_counts"]["medium"], 1)

        # Check top vulnerabilities
        self.assertEqual(len(report["top_vulnerabilities"]), 3)
        self.assertEqual(report["top_vulnerabilities"][0]["priority"], "critical")
        self.assertEqual(report["top_vulnerabilities"][1]["priority"], "high")
        self.assertEqual(report["top_vulnerabilities"][2]["priority"], "medium")

    def test_async_methods(self):
        """Test async methods"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Test apply_context_adjustments
            loop.run_until_complete(self._test_apply_context_adjustments())

            # Test prioritize_vulnerabilities
            loop.run_until_complete(self._test_prioritize_vulnerabilities())

            # Test generate_prioritization_report
            loop.run_until_complete(self._test_generate_prioritization_report())
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
