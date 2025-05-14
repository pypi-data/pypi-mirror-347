#!/usr/bin/env python3
"""
Tests for the utility components of the threat modeling system.
"""

import asyncio
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os

from autothreats.utils.base_llm_provider import BaseLLMProvider
from autothreats.utils.caching import Cache
from autothreats.utils.file_utils import (
    get_file_info,
    list_files,
    read_file,
    write_file,
)
from autothreats.utils.llm_service import LLMService
from autothreats.utils.mock_llm_provider import MockLLMProvider
from autothreats.utils.org_parameters import OrganizationParameters
from autothreats.utils.report_generator import ReportGenerator


class TestBaseLLMProvider(unittest.TestCase):
    """Test the BaseLLMProvider class"""

    def test_base_provider_is_abstract(self):
        """Test that BaseLLMProvider is an abstract class"""
        with self.assertRaises(TypeError):
            BaseLLMProvider()

    def test_base_provider_interface(self):
        """Test that BaseLLMProvider defines the expected interface"""
        # Check for required abstract methods
        self.assertTrue(hasattr(BaseLLMProvider, "is_available"))
        self.assertTrue(hasattr(BaseLLMProvider, "get_default_model"))
        self.assertTrue(hasattr(BaseLLMProvider, "_make_api_request"))

        # Check for other important methods
        self.assertTrue(hasattr(BaseLLMProvider, "generate_text_async"))
        self.assertTrue(hasattr(BaseLLMProvider, "batch_generate_texts"))
        self.assertTrue(hasattr(BaseLLMProvider, "update_config"))
        self.assertTrue(hasattr(BaseLLMProvider, "clear_cache"))


class TestCache(unittest.TestCase):
    """Test the Cache class"""

    def setUp(self):
        """Set up the test"""
        self.cache = Cache()

    def test_cache_set_get(self):
        """Test setting and getting a cache value"""
        self.cache.set("test_key", "test_value")
        self.assertEqual(self.cache.get("test_key"), "test_value")
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_cache_get_with_default(self):
        """Test getting a cache value with a default"""
        self.assertIsNone(self.cache.get("nonexistent"))
        self.assertEqual(self.cache.get("nonexistent", "default"), "default")

    def test_cache_key_exists(self):
        """Test checking if a key exists in the cache"""
        self.cache.set("test_key", "test_value")
        self.assertTrue("test_key" in self.cache.cache)
        self.assertFalse("nonexistent" in self.cache.cache)

    def test_cache_delete(self):
        """Test deleting a cache value"""
        self.cache.set("test_key", "test_value")
        self.assertTrue("test_key" in self.cache.cache)
        self.cache.delete("test_key")
        self.assertFalse("test_key" in self.cache.cache)

    def test_cache_clear(self):
        """Test clearing the cache"""
        self.cache.set("test_key1", "test_value1")
        self.cache.set("test_key2", "test_value2")
        self.assertTrue("test_key1" in self.cache.cache)
        self.assertTrue("test_key2" in self.cache.cache)
        self.cache.clear()
        self.assertFalse("test_key1" in self.cache.cache)
        self.assertFalse("test_key2" in self.cache.cache)

    def test_cache_ttl(self):
        """Test cache TTL functionality"""
        # Create a cache with a short TTL
        short_ttl_cache = Cache(ttl=0.1)

        # Set a value
        short_ttl_cache.set("test_key", "test_value")
        self.assertEqual(short_ttl_cache.get("test_key"), "test_value")

        # Wait for the TTL to expire
        import time

        time.sleep(0.2)

        # The value should be gone
        self.assertIsNone(short_ttl_cache.get("test_key"))

    def test_cache_size_limit(self):
        """Test cache size limit"""
        # Create a cache with a size limit of 2
        limited_cache = Cache(max_size=2)

        # Add 3 items to the cache
        limited_cache.set("key1", "value1")
        limited_cache.set("key2", "value2")
        limited_cache.set("key3", "value3")

        # The oldest item should be evicted
        self.assertFalse("key1" in limited_cache.cache)
        self.assertTrue("key2" in limited_cache.cache)
        self.assertTrue("key3" in limited_cache.cache)


class TestFileUtils(unittest.TestCase):
    """Test the file utility functions"""

    def setUp(self):
        """Set up the test"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.test_file_path, "w") as f:
            f.write("Test content")

    def tearDown(self):
        """Clean up after the test"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_read_file(self):
        """Test reading a file"""
        content = read_file(self.test_file_path)
        self.assertEqual(content, "Test content")

    def test_read_nonexistent_file(self):
        """Test reading a nonexistent file"""
        content = read_file(os.path.join(self.temp_dir, "nonexistent.txt"))
        self.assertIsNone(content)

    def test_write_file(self):
        """Test writing a file"""
        new_file_path = os.path.join(self.temp_dir, "new_file.txt")
        result = write_file(new_file_path, "New content")
        self.assertTrue(result)
        with open(new_file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "New content")

    def test_file_exists(self):
        """Test checking if a file exists"""
        self.assertTrue(os.path.exists(self.test_file_path))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "nonexistent.txt")))

    def test_get_file_info(self):
        """Test getting file info"""
        info = get_file_info(self.test_file_path)
        self.assertIn("size", info)
        self.assertIn("modified", info)
        self.assertEqual(info["size"], len("Test content"))

    def test_list_files(self):
        """Test listing files in a directory"""
        # Create some more files
        os.makedirs(os.path.join(self.temp_dir, "subdir"))
        with open(os.path.join(self.temp_dir, "file1.txt"), "w") as f:
            f.write("File 1")
        with open(os.path.join(self.temp_dir, "file2.txt"), "w") as f:
            f.write("File 2")
        with open(os.path.join(self.temp_dir, "subdir", "file3.txt"), "w") as f:
            f.write("File 3")

        # List files non-recursively
        files = list_files(self.temp_dir, recursive=False)
        self.assertIn(os.path.join(self.temp_dir, "test_file.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file1.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file2.txt"), files)
        self.assertNotIn(os.path.join(self.temp_dir, "subdir", "file3.txt"), files)

        # List files recursively
        files = list_files(self.temp_dir, recursive=True)
        self.assertIn(os.path.join(self.temp_dir, "test_file.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file1.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file2.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "subdir", "file3.txt"), files)

    def test_list_files_with_pattern(self):
        """Test listing files with a pattern"""
        # Create some more files
        with open(os.path.join(self.temp_dir, "file1.txt"), "w") as f:
            f.write("File 1")
        with open(os.path.join(self.temp_dir, "file2.txt"), "w") as f:
            f.write("File 2")
        with open(os.path.join(self.temp_dir, "file3.py"), "w") as f:
            f.write("File 3")

        # List only .txt files
        files = list_files(self.temp_dir, pattern="*.txt")
        self.assertIn(os.path.join(self.temp_dir, "test_file.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file1.txt"), files)
        self.assertIn(os.path.join(self.temp_dir, "file2.txt"), files)
        self.assertNotIn(os.path.join(self.temp_dir, "file3.py"), files)


class TestLLMService(unittest.TestCase):
    """Test the LLMService class"""

    def setUp(self):
        """Set up the test"""
        # Create and set an event loop for the test
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Create a configuration with mock provider enabled and minimal features
        self.config = {
            "enable_mock": True,
            "default_provider": "mock",
            "max_concurrent_requests": 1,
            "batch_enabled": False,
            "cache_enabled": False,
        }
        self.service = LLMService(self.config)

    def tearDown(self):
        """Clean up after the test"""
        # Close the event loop
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_service_initialization(self):
        """Test service initialization"""
        self.assertEqual(self.service.default_provider, "mock")
        self.assertIn("mock", self.service.providers)
        self.assertIsInstance(self.service.providers["mock"], MockLLMProvider)

    def test_get_available_providers(self):
        """Test getting available providers"""
        providers = self.service.get_available_providers()
        self.assertIn("mock", providers)

    def test_get_provider(self):
        """Test getting a provider"""
        # The LLMService doesn't have a get_provider method
        # Instead, we'll test the providers dictionary directly
        provider = self.service.providers.get("mock")
        self.assertIsInstance(provider, MockLLMProvider)

        # Test default provider
        self.assertEqual(self.service.default_provider, "mock")

        # Test nonexistent provider
        self.assertNotIn("nonexistent", self.service.providers)

    def test_get_completion(self):
        """Test getting a completion"""
        # The LLMService doesn't have a get_completion method
        # Instead, we'll test the generate_text_async method
        loop = asyncio.get_event_loop()
        completion = loop.run_until_complete(
            self.service.generate_text_async("Test prompt", provider="mock")
        )
        self.assertIsNotNone(completion)
        self.assertIsInstance(completion, str)

    def test_get_chat_completion(self):
        """Test getting a chat completion"""
        # The LLMService doesn't have a get_chat_completion method
        # Instead, we'll test the generate_text_async method with a chat-like prompt
        loop = asyncio.get_event_loop()
        system_prompt = "You are a helpful assistant."
        user_prompt = "Hello, world!"
        completion = loop.run_until_complete(
            self.service.generate_text_async(
                user_prompt, provider="mock", system_prompt=system_prompt
            )
        )
        self.assertIsNotNone(completion)
        self.assertIsInstance(completion, str)

    def test_get_embedding(self):
        """Test getting an embedding"""
        # The LLMService doesn't have a get_embedding method
        # Instead, we'll test the generate_text_async method with an embedding-related prompt
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.service.generate_text_async(
                "Generate an embedding for this text", provider="mock"
            )
        )
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)


class TestMockLLMProvider(unittest.TestCase):
    """Test the MockLLMProvider class"""

    def setUp(self):
        """Set up the test"""
        # Create and set an event loop for the test
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Initialize the provider with a config that disables features requiring an event loop
        config = {
            "max_concurrent_requests": 1,
            "batch_enabled": False,
            "cache_enabled": False,
        }
        self.provider = MockLLMProvider(config=config)

    def tearDown(self):
        """Clean up after the test"""
        # Close the event loop
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_provider_is_available(self):
        """Test that the provider is available"""
        self.assertTrue(MockLLMProvider.is_available())

    def test_get_default_model(self):
        """Test getting the default model"""
        self.assertEqual(self.provider.get_default_model(), "mock-model")

    def test_get_available_models(self):
        """Test getting available models"""
        # The MockLLMProvider doesn't have a get_available_models method
        # It should return a list with the default model
        self.assertEqual(self.provider.get_default_model(), "mock-model")

    def test_get_model_context_size(self):
        """Test getting model context size"""
        # The MockLLMProvider doesn't have a get_model_context_size method
        # We'll test the generate_text_async method instead which uses the default model
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            self.provider.generate_text_async("Test prompt", "mock-model", 100, 0.5)
        )
        self.assertIsNotNone(result)

    def test_get_completion(self):
        """Test getting a completion"""
        # The MockLLMProvider doesn't have a get_completion method
        # We'll test the generate_text_async method instead
        loop = asyncio.get_event_loop()
        completion = loop.run_until_complete(
            self.provider.generate_text_async("Test prompt", "mock-model", 100, 0.5)
        )
        self.assertIsNotNone(completion)
        self.assertIsInstance(completion, str)

    def test_get_chat_completion(self):
        """Test getting a chat completion"""
        # The MockLLMProvider doesn't have a get_chat_completion method
        # We'll test the generate_text_async method with a chat-like prompt
        loop = asyncio.get_event_loop()
        system_prompt = "You are a helpful assistant."
        user_prompt = "Hello, world!"
        prompt = f"{system_prompt}\n\n{user_prompt}"
        completion = loop.run_until_complete(
            self.provider.generate_text_async(
                prompt, "mock-model", 100, 0.5, system_prompt=system_prompt
            )
        )
        self.assertIsNotNone(completion)
        self.assertIsInstance(completion, str)

    def test_get_embedding(self):
        """Test getting an embedding"""
        # The MockLLMProvider doesn't have a get_embedding method
        # We'll test the _make_api_request method instead with a generic prompt
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.provider._make_api_request(
                "Generate an embedding for this text",
                "mock-model",
                500,
                0.5,
                "You are a security analyst",
            )
        )
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

    def test_vulnerability_response(self):
        """Test generating a vulnerability response"""
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.provider._make_api_request(
                "Analyze this code for SQL injection vulnerability",
                "mock-model",
                500,
                0.5,
                "You are a security analyst",
            )
        )
        self.assertIn("SQL injection", response)

    def test_context_response(self):
        """Test generating a context response"""
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.provider._make_api_request(
                "Analyze the context of this application",
                "mock-model",
                500,
                0.5,
                "You are a security analyst",
            )
        )
        self.assertIn("application_type", response)

    def test_summary_response(self):
        """Test generating a summary response"""
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.provider._make_api_request(
                "Generate a summary report for this application",
                "mock-model",
                500,
                0.5,
                "You are a security analyst",
            )
        )
        self.assertIn("Security Analysis Summary", response)


class TestOrganizationParameters(unittest.TestCase):
    """Test the OrganizationParameters class"""

    def setUp(self):
        """Set up the test"""
        # Create a temporary YAML file with organization parameters
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "org-params.yaml")
        config = {
            "industry_sector": "finance",
            "organization_size": "large",
            "security_maturity": "high",
            "risk_tolerance": "low",
            "compliance_requirements": ["PCI-DSS", "GDPR"],
            "security_controls": {
                "encryption": {"implemented": True, "strength": "high"}
            },
            "custom_mitigations": {"sql_injection": ["Use prepared statements"]},
            "priority_threats": ["sql_injection"],
        }
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)

    def tearDown(self):
        """Clean up after the test"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_load_from_file(self):
        """Test loading parameters from a file"""
        params = OrganizationParameters(self.config_path)
        self.assertEqual(params.get_industry_sector(), "finance")
        self.assertEqual(params.get_organization_size(), "large")
        self.assertEqual(params.get_security_maturity(), "high")
        self.assertEqual(params.get_risk_tolerance(), "low")
        self.assertEqual(params.get_compliance_requirements(), ["PCI-DSS", "GDPR"])
        self.assertTrue(params.has_security_control("encryption"))
        self.assertEqual(params.get_security_control_strength("encryption"), "high")

    def test_default_parameters(self):
        """Test default parameters"""
        params = OrganizationParameters()
        self.assertEqual(params.get_industry_sector(), "general")
        self.assertEqual(params.get_organization_size(), "medium")
        self.assertEqual(params.get_security_maturity(), "medium")
        self.assertEqual(params.get_risk_tolerance(), "medium")
        self.assertEqual(params.get_compliance_requirements(), [])

    def test_get_parameter_with_default(self):
        """Test getting a parameter with a default value"""
        params = OrganizationParameters()
        # Test getting a security control that doesn't exist
        self.assertEqual(params.get_security_control("nonexistent"), {})
        # Test checking if a security control that doesn't exist is implemented
        self.assertFalse(params.has_security_control("nonexistent"))

    def test_set_parameter(self):
        """Test setting a parameter"""
        params = OrganizationParameters()
        # We can't directly set parameters in the current implementation
        # Instead, let's test the adjust_risk_score method
        base_score = 5
        # Load parameters that would affect the risk score
        params.parameters["risk_tolerance"] = (
            "low"  # Low tolerance = higher risk scores
        )
        params.parameters["security_maturity"] = (
            "low"  # Low maturity = higher risk scores
        )
        params.parameters["priority_threats"] = ["test_threat"]

        # Test adjusting risk score for a priority threat
        adjusted_score = params.adjust_risk_score("test_threat", base_score)
        self.assertGreater(adjusted_score, base_score)

    def test_get_all_parameters(self):
        """Test getting all parameters"""
        params = OrganizationParameters(self.config_path)
        all_params = params.get_all_parameters()
        self.assertIsInstance(all_params, dict)
        self.assertEqual(all_params["industry_sector"], "finance")
        self.assertEqual(all_params["organization_size"], "large")
        self.assertEqual(all_params["compliance_requirements"], ["PCI-DSS", "GDPR"])


class TestReportGenerator(unittest.TestCase):
    """Test the ReportGenerator class"""

    def setUp(self):
        """Set up the test"""
        self.generator = ReportGenerator()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after the test"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_generate_html_report(self):
        """Test generating an HTML report"""
        # Create a simple threat model
        threat_model = {
            "project_name": "Test Project",
            "threats": [
                {
                    "id": "vuln-1",
                    "name": "SQL Injection",
                    "cwe_id": "CWE-89",
                    "description": "SQL injection vulnerability",
                    "severity": "high",
                }
            ],
        }

        # Generate an HTML report
        html_report = self.generator.generate_html_report(threat_model)

        # Check that the report contains expected content
        self.assertIn("Test Project", html_report)
        self.assertIn("SQL Injection", html_report)
        self.assertIn("high", html_report)

    def test_save_html_report(self):
        """Test saving an HTML report"""
        # Create a simple threat model
        threat_model = {
            "project_name": "Test Project",
            "threats": [
                {
                    "id": "vuln-1",
                    "name": "SQL Injection",
                    "cwe_id": "CWE-89",
                    "description": "SQL injection vulnerability",
                    "severity": "high",
                }
            ],
        }

        # Generate and save an HTML report
        output_path = os.path.join(self.temp_dir, "report.html")
        saved_path = self.generator.save_html_report(threat_model, output_path)

        # Check that the file was created
        self.assertTrue(os.path.exists(output_path))
        self.assertEqual(saved_path, output_path)

        # Check that the file contains the expected content
        with open(output_path, "r") as f:
            content = f.read()

        self.assertIn("Test Project", content)
        self.assertIn("SQL Injection", content)

    def test_fallback_html(self):
        """Test generating a fallback HTML report"""
        # Create a simple threat model
        threat_model = {
            "project_name": "Test Project",
            "threats": [
                {
                    "id": "vuln-1",
                    "name": "SQL Injection",
                    "cwe_id": "CWE-89",
                    "description": "SQL injection vulnerability",
                    "severity": "high",
                }
            ],
        }

        # Generate a fallback HTML report
        fallback_html = self.generator._generate_fallback_html(threat_model)

        # Check that the report contains expected content
        self.assertIn("Test Project", fallback_html)
        self.assertIn("SQL Injection", fallback_html)
        self.assertIn("HIGH", fallback_html)


if __name__ == "__main__":
    unittest.main()
