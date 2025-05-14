#!/usr/bin/env python3
"""
Tests for the simplified hierarchical analysis component.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.agentic.simplified_hierarchical_analysis import (
    SimplifiedHierarchicalAnalysis,
)
from autothreats.simplified_base import SharedWorkspace


class TestSimplifiedHierarchicalAnalysis(unittest.TestCase):
    """Test the SimplifiedHierarchicalAnalysis class"""

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

        # Create the hierarchical analysis component
        self.hierarchical_analysis = SimplifiedHierarchicalAnalysis(self.mock_workspace)

    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.hierarchical_analysis.workspace, self.mock_workspace)
        self.assertIsNotNone(self.hierarchical_analysis.logger)
        self.assertEqual(self.hierarchical_analysis.llm_service, self.mock_llm_service)
        self.assertEqual(self.hierarchical_analysis.analysis_cache, {})

    async def _test_identify_components(self):
        """Test identifying components"""
        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
                "auth/logout.py": "def logout():\n    # Log out user\n    return True",
                "api/users.py": "def get_user(user_id):\n    # Get user\n    return user",
                "api/posts.py": "def get_post(post_id):\n    # Get post\n    return post",
                "ui/components/button.js": "function Button() {\n    // Button component\n    return <button>Click me</button>\n}",
                "ui/components/form.js": "function Form() {\n    // Form component\n    return <form>Form</form>\n}",
                "ui/pages/home.js": "function HomePage() {\n    // Home page\n    return <div>Home</div>\n}",
            }
        }

        # Identify components
        components = await self.hierarchical_analysis._identify_components(codebase)

        # Check the results
        self.assertGreater(len(components), 0)

        # Check that components were identified by directory
        auth_component = next((c for c in components if c["name"] == "auth"), None)
        api_component = next((c for c in components if c["name"] == "api"), None)
        ui_components_component = next(
            (c for c in components if c["name"] == "ui/components"), None
        )

        self.assertIsNotNone(auth_component)
        self.assertIsNotNone(api_component)
        self.assertIsNotNone(ui_components_component)

        # Check that the auth component has the correct files
        self.assertEqual(len(auth_component["files"]), 2)
        self.assertIn("auth/login.py", auth_component["files"])
        self.assertIn("auth/logout.py", auth_component["files"])

        # Check that the auth component has the correct purpose
        self.assertEqual(auth_component["purpose"], "authentication")

        # Check that the auth component has the correct languages
        self.assertIn("python", auth_component["languages"])

    def test_determine_component_languages(self):
        """Test determining component languages"""
        # Create test files
        files = [
            "auth/login.py",
            "auth/logout.py",
            "api/users.js",
            "api/posts.ts",
        ]

        # Create file contents
        file_contents = {
            "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
            "auth/logout.py": "def logout():\n    # Log out user\n    return True",
            "api/users.js": "function getUser(userId) {\n    // Get user\n    return user;\n}",
            "api/posts.ts": "function getPost(postId: number): Post {\n    // Get post\n    return post;\n}",
        }

        # Determine languages for Python files
        python_languages = self.hierarchical_analysis._determine_component_languages(
            ["auth/login.py", "auth/logout.py"], file_contents
        )

        # Check that Python was detected
        self.assertEqual(len(python_languages), 1)
        self.assertEqual(python_languages[0], "python")

        # Determine languages for JavaScript and TypeScript files
        js_languages = self.hierarchical_analysis._determine_component_languages(
            ["api/users.js", "api/posts.ts"], file_contents
        )

        # Check that JavaScript and TypeScript were detected
        self.assertEqual(len(js_languages), 2)
        self.assertIn("javascript", js_languages)
        self.assertIn("typescript", js_languages)

    def test_map_extension_to_language(self):
        """Test mapping extensions to languages"""
        # Test common extensions
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("py"), "python"
        )
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("js"), "javascript"
        )
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("ts"), "typescript"
        )
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("java"), "java"
        )
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("html"), "html"
        )
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("css"), "css"
        )

        # Test unknown extension
        self.assertEqual(
            self.hierarchical_analysis._map_extension_to_language("xyz"), "unknown"
        )

    def test_determine_component_purpose(self):
        """Test determining component purpose"""
        # Test authentication directory
        self.assertEqual(
            self.hierarchical_analysis._determine_component_purpose(
                "auth", ["auth/login.py", "auth/logout.py"]
            ),
            "authentication",
        )

        # Test API directory
        self.assertEqual(
            self.hierarchical_analysis._determine_component_purpose(
                "api", ["api/users.js", "api/posts.ts"]
            ),
            "api",
        )

        # Test UI directory
        self.assertEqual(
            self.hierarchical_analysis._determine_component_purpose(
                "ui/components", ["ui/components/button.js", "ui/components/form.js"]
            ),
            "user_interface",
        )

        # Test database directory
        self.assertEqual(
            self.hierarchical_analysis._determine_component_purpose(
                "db", ["db/models.py", "db/queries.py"]
            ),
            "data_access",
        )

        # Test unknown directory
        self.assertEqual(
            self.hierarchical_analysis._determine_component_purpose(
                "misc", ["misc/utils.py", "misc/helpers.py"]
            ),
            "unknown",
        )

    def test_determine_extension_purpose(self):
        """Test determining extension purpose"""
        # Test source code extensions
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("py"), "source_code"
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("js"), "source_code"
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("java"),
            "source_code",
        )

        # Test UI extensions
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("html"),
            "user_interface",
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("jsx"),
            "user_interface",
        )

        # Test styling extensions
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("css"), "styling"
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("scss"), "styling"
        )

        # Test configuration extensions
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("json"),
            "configuration",
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("yaml"),
            "configuration",
        )

        # Test unknown extension
        self.assertEqual(
            self.hierarchical_analysis._determine_extension_purpose("xyz"), "unknown"
        )

    def test_analyze_component_relationships(self):
        """Test analyzing component relationships"""
        # Create test components
        components = [
            {
                "id": "comp-1",
                "name": "auth",
                "type": "directory",
                "files": ["auth/login.py", "auth/logout.py"],
                "file_count": 2,
                "languages": ["python"],
                "purpose": "authentication",
            },
            {
                "id": "comp-2",
                "name": "api",
                "type": "directory",
                "files": ["api/users.py", "api/posts.py"],
                "file_count": 2,
                "languages": ["python"],
                "purpose": "api",
            },
            {
                "id": "comp-3",
                "name": "api/users",
                "type": "directory",
                "files": ["api/users/create.py", "api/users/delete.py"],
                "file_count": 2,
                "languages": ["python"],
                "purpose": "api",
            },
        ]

        # Analyze component relationships
        relationships = self.hierarchical_analysis._analyze_component_relationships(
            components
        )

        # Check the results
        self.assertGreater(len(relationships), 0)

        # Check that the api component contains the api/users component
        api_users_relationship = next(
            (
                r
                for r in relationships
                if r["source"] == "comp-2" and r["target"] == "comp-3"
            ),
            None,
        )

        self.assertIsNotNone(api_users_relationship)
        self.assertEqual(api_users_relationship["type"], "contains")

    async def _test_detect_vulnerabilities_in_component(self):
        """Test detecting vulnerabilities in a component"""
        # Create a test component
        component = {
            "id": "comp-1",
            "name": "auth",
            "type": "directory",
            "files": ["auth/login.py", "auth/logout.py"],
            "file_count": 2,
            "languages": ["python"],
            "purpose": "authentication",
        }

        # Create a test component codebase
        component_codebase = {
            "id": "component_comp-1",
            "files": {
                "auth/login.py": 'def login(username, password):\n    query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"\n    return execute_query(query)',
                "auth/logout.py": "def logout():\n    # Log out user\n    return True",
            },
        }

        # Detect vulnerabilities
        vulnerabilities = (
            await self.hierarchical_analysis._detect_vulnerabilities_in_component(
                component, component_codebase, "test_job"
            )
        )

        # Check the results
        self.assertGreater(len(vulnerabilities), 0)

        # Check that the SQL injection vulnerability was detected
        sql_injection_vuln = next(
            (v for v in vulnerabilities if v["pattern"] == "sql_injection"), None
        )

        self.assertIsNotNone(sql_injection_vuln)
        self.assertEqual(sql_injection_vuln["file_path"], "auth/login.py")
        self.assertEqual(sql_injection_vuln["severity"], "high")

    def test_determine_vulnerability_severity(self):
        """Test determining vulnerability severity"""
        # Test high severity patterns
        self.assertEqual(
            self.hierarchical_analysis._determine_vulnerability_severity(
                "sql_injection", "authentication"
            ),
            "high",
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_vulnerability_severity(
                "xss", "user_interface"
            ),
            "high",
        )

        # Test medium severity patterns
        self.assertEqual(
            self.hierarchical_analysis._determine_vulnerability_severity(
                "missing_authorization", "api"
            ),
            "high",  # Elevated to high because it's in a critical component
        )
        self.assertEqual(
            self.hierarchical_analysis._determine_vulnerability_severity(
                "insecure_api", "utility"
            ),
            "medium",
        )

        # Test low severity patterns with critical component (should be elevated to medium)
        self.assertEqual(
            self.hierarchical_analysis._determine_vulnerability_severity(
                "debug_code", "authentication"
            ),
            "medium",  # Elevated to medium because it's in a critical component
        )

    async def _test_analyze_component_vulnerabilities(self):
        """Test analyzing component vulnerabilities"""
        # Create test components
        components = [
            {
                "id": "comp-1",
                "name": "auth",
                "type": "directory",
                "files": ["auth/login.py", "auth/logout.py"],
                "file_count": 2,
                "languages": ["python"],
                "purpose": "authentication",
            },
            {
                "id": "comp-2",
                "name": "api",
                "type": "directory",
                "files": ["api/users.py", "api/posts.py"],
                "file_count": 2,
                "languages": ["python"],
                "purpose": "api",
            },
        ]

        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": 'def login(username, password):\n    query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"\n    return execute_query(query)',
                "auth/logout.py": "def logout():\n    # Log out user\n    return True",
                "api/users.py": "def get_user(user_id):\n    # Get user\n    return user",
                "api/posts.py": "def get_post(post_id):\n    # Get post\n    return post",
            }
        }

        # Analyze component vulnerabilities
        component_vulnerabilities = (
            await self.hierarchical_analysis._analyze_component_vulnerabilities(
                components, codebase, "test_job"
            )
        )

        # Check the results
        self.assertEqual(len(component_vulnerabilities), 2)
        self.assertIn("comp-1", component_vulnerabilities)
        self.assertIn("comp-2", component_vulnerabilities)

        # Check that vulnerabilities were found in the auth component
        self.assertGreater(len(component_vulnerabilities["comp-1"]), 0)

    async def _test_analyze_codebase_hierarchically(self):
        """Test analyzing a codebase hierarchically"""
        # Create a test codebase
        codebase = {
            "files": {
                "auth/login.py": 'def login(username, password):\n    query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"\n    return execute_query(query)',
                "auth/logout.py": "def logout():\n    # Log out user\n    return True",
                "api/users.py": "def get_user(user_id):\n    # Get user\n    return user",
                "api/posts.py": "def get_post(post_id):\n    # Get post\n    return post",
                "ui/components/button.js": "function Button() {\n    // Button component\n    return <button>Click me</button>\n}",
                "ui/components/form.js": "function Form() {\n    // Form component\n    return <form>Form</form>\n}",
                "ui/pages/home.js": "function HomePage() {\n    // Home page\n    return <div>Home</div>\n}",
            }
        }

        # Analyze codebase hierarchically
        hierarchical_analysis = (
            await self.hierarchical_analysis.analyze_codebase_hierarchically(
                codebase, "test_job"
            )
        )

        # Check the results
        self.assertEqual(hierarchical_analysis["job_id"], "test_job")
        self.assertIn("components", hierarchical_analysis)
        self.assertIn("component_relationships", hierarchical_analysis)
        self.assertIn("component_vulnerabilities", hierarchical_analysis)
        self.assertIn("timestamp", hierarchical_analysis)

        # Check that components were identified
        self.assertGreater(len(hierarchical_analysis["components"]), 0)

        # Check that component relationships were identified
        self.assertGreater(len(hierarchical_analysis["component_relationships"]), 0)

        # Check that component vulnerabilities were identified
        self.assertGreater(len(hierarchical_analysis["component_vulnerabilities"]), 0)

    async def _test_merge_component_vulnerabilities(self):
        """Test merging component vulnerabilities"""
        # Create test hierarchical analysis
        hierarchical_analysis = {
            "job_id": "test_job",
            "components": [
                {
                    "id": "comp-1",
                    "name": "auth",
                    "type": "directory",
                    "files": ["auth/login.py", "auth/logout.py"],
                    "file_count": 2,
                    "languages": ["python"],
                    "purpose": "authentication",
                },
                {
                    "id": "comp-2",
                    "name": "api",
                    "type": "directory",
                    "files": ["api/users.py", "api/posts.py"],
                    "file_count": 2,
                    "languages": ["python"],
                    "purpose": "api",
                },
            ],
            "component_relationships": [],
            "component_vulnerabilities": {
                "comp-1": [
                    {
                        "id": "vuln-1",
                        "component_id": "comp-1",
                        "file_path": "auth/login.py",
                        "line": 2,
                        "pattern": "sql_injection",
                        "code": 'query = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"',
                        "description": "Potential sql injection vulnerability",
                        "severity": "high",
                        "confidence": 0.7,
                        "detection_method": "hierarchical_pattern_matching",
                    }
                ],
                "comp-2": [
                    {
                        "id": "vuln-2",
                        "component_id": "comp-2",
                        "file_path": "api/users.py",
                        "line": 5,
                        "pattern": "missing_input_validation",
                        "code": "return user",
                        "description": "Potential missing input validation vulnerability",
                        "severity": "medium",
                        "confidence": 0.6,
                        "detection_method": "hierarchical_pattern_matching",
                    }
                ],
            },
        }

        # Merge component vulnerabilities
        merged_vulnerabilities = (
            await self.hierarchical_analysis.merge_component_vulnerabilities(
                hierarchical_analysis
            )
        )

        # Check the results
        self.assertEqual(len(merged_vulnerabilities), 2)

        # Check that both vulnerabilities were included
        self.assertTrue(any(v["id"] == "vuln-1" for v in merged_vulnerabilities))
        self.assertTrue(any(v["id"] == "vuln-2" for v in merged_vulnerabilities))

    def test_async_methods(self):
        """Test async methods"""
        # Set up the mock LLM service to return a valid response
        self.mock_llm_service.generate_text_async.return_value = """
        {
            "components": [
                {
                    "id": "comp-1",
                    "name": "auth",
                    "type": "directory",
                    "files": ["auth/login.py", "auth/logout.py"],
                    "file_count": 2,
                    "languages": ["python"],
                    "purpose": "authentication"
                }
            ]
        }
        """

        # Create a mock codebase for testing
        mock_codebase = {
            "files": {
                "auth/login.py": "def login(username, password):\n    # Check credentials\n    return True",
                "auth/logout.py": "def logout():\n    # Log out user\n    return True",
            }
        }

        # Create a new event loop for this test
        old_loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Test analyze_codebase_hierarchically
            result = loop.run_until_complete(
                self.hierarchical_analysis.analyze_codebase_hierarchically(
                    mock_codebase, "test_job"
                )
            )

            # Verify the result
            self.assertIsNotNone(result)
            self.assertIn("components", result)
            self.assertIn("component_relationships", result)
            self.assertIn("component_vulnerabilities", result)

            # Test identify_components
            loop.run_until_complete(self._test_identify_components())

            # Test detect_vulnerabilities_in_component
            loop.run_until_complete(self._test_detect_vulnerabilities_in_component())

            # Test analyze_component_vulnerabilities
            loop.run_until_complete(self._test_analyze_component_vulnerabilities())

            # Test analyze_codebase_hierarchically
            loop.run_until_complete(self._test_analyze_codebase_hierarchically())

            # Test merge_component_vulnerabilities
            loop.run_until_complete(self._test_merge_component_vulnerabilities())
        finally:
            # Clean up the loop
            loop.close()
            asyncio.set_event_loop(old_loop)


if __name__ == "__main__":
    unittest.main()
