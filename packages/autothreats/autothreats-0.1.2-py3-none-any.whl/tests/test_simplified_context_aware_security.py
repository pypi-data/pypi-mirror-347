#!/usr/bin/env python3
"""
Tests for the simplified context-aware security component.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.agentic.simplified_context_aware_security import (
    SimplifiedContextAwareSecurity,
)
from autothreats.simplified_base import SharedWorkspace


class TestSimplifiedContextAwareSecurity(unittest.TestCase):
    """Test the SimplifiedContextAwareSecurity class"""

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
            "authentication": [
                {
                    "category": "Authentication",
                    "description": "Basic password authentication",
                    "strength": "moderate",
                    "location": "login_function"
                }
            ],
            "authorization": [
                {
                    "category": "Authorization",
                    "description": "Role-based access control",
                    "strength": "strong",
                    "location": "check_permissions"
                }
            ]
        }
        """
        )

        # Set up the workspace to return the LLM service
        self.mock_workspace.get_data.side_effect = lambda key: (
            self.mock_llm_service if key == "llm_service" else None
        )

        # Create the context-aware security component
        self.context_aware_security = SimplifiedContextAwareSecurity(
            self.mock_workspace
        )

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.context_aware_security.workspace, self.mock_workspace)
        self.assertIsNotNone(self.context_aware_security.logger)
        self.assertEqual(self.context_aware_security.llm_service, self.mock_llm_service)
        self.assertEqual(self.context_aware_security.context_cache, {})

    def test_identify_security_files(self):
        """Test identifying security files"""
        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
                "utils/helpers.py": "def format_date(date):\n    return date.strftime('%Y-%m-%d')",
                "security/encryption.py": "def encrypt(data, key):\n    # Encrypt data\n    return encrypted_data",
            }
        }

        # Identify security files
        security_files = self.context_aware_security._identify_security_files(codebase)

        # Check the results
        self.assertEqual(len(security_files), 2)
        self.assertTrue(
            any(file["file_path"] == "auth/login.py" for file in security_files)
        )
        self.assertTrue(
            any(
                file["file_path"] == "security/encryption.py" for file in security_files
            )
        )
        self.assertFalse(
            any(file["file_path"] == "utils/helpers.py" for file in security_files)
        )

    async def _test_analyze_security_patterns(self):
        """Test analyzing security patterns"""
        # Create test security files
        security_files = [
            {
                "file_path": "auth/login.py",
                "path_relevance": True,
                "content_relevance": True,
                "relevance_score": 0.8,
            },
            {
                "file_path": "security/encryption.py",
                "path_relevance": True,
                "content_relevance": True,
                "relevance_score": 0.8,
            },
        ]

        # Set up the workspace to return file contents
        self.mock_workspace.get_data.side_effect = lambda key: {
            "llm_service": self.mock_llm_service,
            "codebase_files_test_job_auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
            "codebase_files_test_job_security/encryption.py": "def encrypt(data, key):\n    # Encrypt data\n    return encrypted_data",
        }.get(key)

        # Analyze security patterns
        patterns = await self.context_aware_security._analyze_security_patterns(
            security_files, "test_job"
        )

        # Check the results
        self.assertIn("authentication", patterns)
        self.assertIn("authorization", patterns)
        self.assertIn("encryption", patterns)

    def test_identify_security_boundaries(self):
        """Test identifying security boundaries"""
        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
                "auth/permissions.py": "def check_permissions(user, resource):\n    # Check permissions\n    return True",
                "security/encryption.py": "def encrypt(data, key):\n    # Encrypt data\n    return encrypted_data",
            }
        }

        # Create security patterns
        security_patterns = {
            "authentication": [
                {
                    "file_path": "auth/login.py",
                    "description": "Basic password authentication",
                    "strength": "moderate",
                    "location": "login_function",
                }
            ],
            "authorization": [
                {
                    "file_path": "auth/permissions.py",
                    "description": "Role-based access control",
                    "strength": "strong",
                    "location": "check_permissions",
                }
            ],
            "encryption": [
                {
                    "file_path": "security/encryption.py",
                    "description": "AES encryption",
                    "strength": "strong",
                    "location": "encrypt_function",
                }
            ],
        }

        # Identify security boundaries
        boundaries = self.context_aware_security._identify_security_boundaries(
            codebase, security_patterns
        )

        # Check the results
        self.assertEqual(len(boundaries), 2)
        self.assertTrue(
            any(boundary["type"] == "auth_boundary" for boundary in boundaries)
        )
        self.assertTrue(
            any(boundary["type"] == "encryption_boundary" for boundary in boundaries)
        )

    async def _test_analyze_security_context(self):
        """Test analyzing security context"""
        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
                "auth/permissions.py": "def check_permissions(user, resource):\n    # Check permissions\n    return True",
                "security/encryption.py": "def encrypt(data, key):\n    # Encrypt data\n    return encrypted_data",
            }
        }

        # Set up the workspace to return file contents
        self.mock_workspace.get_data.side_effect = lambda key: {
            "llm_service": self.mock_llm_service,
            "codebase_files_test_job_auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
            "codebase_files_test_job_auth/permissions.py": "def check_permissions(user, resource):\n    # Check permissions\n    return True",
            "codebase_files_test_job_security/encryption.py": "def encrypt(data, key):\n    # Encrypt data\n    return encrypted_data",
        }.get(key)

        # Analyze security context
        context = await self.context_aware_security.analyze_security_context(
            codebase, "test_job"
        )

        # Check the results
        self.assertEqual(context["job_id"], "test_job")
        self.assertIn("security_files", context)
        self.assertIn("security_patterns", context)
        self.assertIn("security_boundaries", context)
        self.assertIn("timestamp", context)

    async def _test_enhance_vulnerability_detection(self):
        """Test enhancing vulnerability detection"""
        # Create test vulnerabilities
        vulnerabilities = [
            {
                "id": "vuln-1",
                "type": "sql_injection",
                "file_path": "auth/login.py",
                "line": 10,
                "confidence": 0.7,
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

        # Enhance vulnerability detection
        enhanced_vulnerabilities = (
            await self.context_aware_security.enhance_vulnerability_detection(
                vulnerabilities, security_context
            )
        )

        # Check the results
        self.assertEqual(len(enhanced_vulnerabilities), 2)

        # Check that the vulnerability in the security boundary was enhanced
        auth_vuln = next(
            v for v in enhanced_vulnerabilities if v["file_path"] == "auth/login.py"
        )
        self.assertTrue(auth_vuln["in_security_boundary"])
        self.assertGreater(
            auth_vuln["confidence"], 0.7
        )  # Confidence should be increased
        self.assertIn("security_boundaries", auth_vuln)
        self.assertEqual(auth_vuln["security_boundaries"], ["Authentication Boundary"])

        # Check that the other vulnerability was not enhanced
        ui_vuln = next(
            v for v in enhanced_vulnerabilities if v["file_path"] == "ui/form.js"
        )
        self.assertFalse(ui_vuln["in_security_boundary"])

    def test_async_methods(self):
        """Test async methods"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Test analyze_security_patterns
            loop.run_until_complete(self._test_analyze_security_patterns())

            # Test analyze_security_context
            loop.run_until_complete(self._test_analyze_security_context())

            # Test enhance_vulnerability_detection
            loop.run_until_complete(self._test_enhance_vulnerability_detection())
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
