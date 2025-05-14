#!/usr/bin/env python3
"""
Unified LLM service for the autonomous threat modeling system.
Provides a common interface for multiple LLM providers (OpenAI, Anthropic).
"""

import asyncio
import importlib
import inspect
import logging
import os
from typing import Any, Dict, List, Literal, Optional, Type, Union

from .base_llm_provider import BaseLLMProvider

logger = logging.getLogger(__name__)


class LLMService:
    """Unified service for interacting with multiple LLM providers"""

    # Registry of available providers
    _provider_registry: Dict[str, Type[BaseLLMProvider]] = {}

    @classmethod
    def register_provider(
        cls, provider_name: str, provider_class: Type[BaseLLMProvider]
    ):
        """Register a new provider class"""
        cls._provider_registry[provider_name.lower()] = provider_class
        logger.info(f"Registered LLM provider: {provider_name}")

    @classmethod
    def auto_discover_providers(cls):
        """Auto-discover and register all available providers"""
        # Import known provider modules
        try:
            from . import anthropic_service, mock_llm_provider, openai_service

            # Find all BaseLLMProvider subclasses
            for module in [openai_service, anthropic_service, mock_llm_provider]:
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseLLMProvider)
                        and obj != BaseLLMProvider
                    ):
                        # Extract provider name from class name (e.g., OpenAIService -> openai)
                        provider_name = (
                            name.lower()
                            .replace("service", "")
                            .replace("llmprovider", "")
                        )
                        cls.register_provider(provider_name, obj)
        except ImportError as e:
            logger.warning(f"Error importing core provider modules: {e}")

        # Try to import mock_anthropic_service explicitly
        try:
            from . import mock_anthropic_service

            for name, obj in inspect.getmembers(mock_anthropic_service):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseLLMProvider)
                    and obj != BaseLLMProvider
                ):
                    provider_name = name.lower().replace("service", "")
                    cls.register_provider(provider_name, obj)
        except ImportError as e:
            logger.warning(f"Error importing mock_anthropic_service: {e}")

        # Try to discover additional providers in the same directory
        try:
            import importlib.util
            import os
            import pkgutil
            import sys

            # Get the directory of the current module
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Scan for potential provider modules
            for finder, name, _ in pkgutil.iter_modules([current_dir]):
                if name.endswith("_service") and name not in [
                    "openai_service",
                    "anthropic_service",
                    "llm_service",
                    "base_llm_provider",
                    "mock_anthropic_service",  # Skip this as we already tried to import it
                ]:
                    try:
                        # Import the module using absolute import
                        module_name = f"autothreats.utils.{name}"
                        if module_name not in sys.modules:
                            spec = finder.find_spec(name)
                            if spec:
                                module = importlib.util.module_from_spec(spec)
                                sys.modules[module_name] = module
                                spec.loader.exec_module(module)

                                # Find provider classes
                                for class_name, obj in inspect.getmembers(module):
                                    if (
                                        inspect.isclass(obj)
                                        and issubclass(obj, BaseLLMProvider)
                                        and obj != BaseLLMProvider
                                    ):
                                        # Extract provider name
                                        provider_name = name.lower().replace(
                                            "_service", ""
                                        )
                                        cls.register_provider(provider_name, obj)
                    except Exception as e:
                        logger.warning(
                            f"Error loading potential provider module {name}: {e}"
                        )
        except Exception as e:
            logger.warning(f"Error during provider auto-discovery: {e}")

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize LLM service with configuration"""
        self.logger = logging.getLogger("LLMService")
        self.config = config or {}

        # Auto-discover available providers
        if not LLMService._provider_registry:
            LLMService.auto_discover_providers()

        # Determine default provider
        self.default_provider = self.config.get("default_provider", "openai").lower()

        # Initialize provider instances
        self.providers: Dict[str, BaseLLMProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all enabled providers"""
        # Initialize OpenAI if enabled
        if self.config.get("enable_openai", True):
            # Try to get API key from config or environment
            api_key = self.config.get("openai_api_key") or os.environ.get(
                "OPENAI_API_KEY"
            )

            # If no API key is provided, the OpenAIService will try to load it from file
            self._init_provider(
                "openai",
                api_key,
                self.config.get("openai_config", {}),
            )

            # If the provider was initialized successfully and has an API key, update the config
            if "openai" in self.providers and self.providers["openai"].api_key:
                self.config["openai_api_key"] = self.providers["openai"].api_key
                self.logger.info("OpenAI API key loaded successfully")

        # Initialize Anthropic if enabled
        if self.config.get("enable_anthropic", False):
            # Try to get API key from config or environment
            api_key = self.config.get("anthropic_api_key") or os.environ.get(
                "ANTHROPIC_API_KEY"
            )

            # If no API key is provided, the AnthropicService will try to load it from file
            self._init_provider(
                "anthropic",
                api_key,
                self.config.get("anthropic_config", {}),
            )

            # If the provider was initialized successfully and has an API key, update the config
            if "anthropic" in self.providers and self.providers["anthropic"].api_key:
                self.config["anthropic_api_key"] = self.providers["anthropic"].api_key
                self.logger.info("Anthropic API key loaded successfully")

        # Initialize Mock provider if enabled
        if self.config.get("enable_mock", False):
            self._init_provider(
                "mock",
                None,  # Mock provider doesn't need an API key
                self.config.get("mock_config", {}),
            )

        # Initialize any other configured providers
        for key, value in self.config.items():
            if key.endswith("_enabled") and value:
                provider_name = key.replace("_enabled", "")
                if provider_name not in ["openai", "anthropic"]:
                    api_key = self.config.get(
                        f"{provider_name}_api_key"
                    ) or os.environ.get(f"{provider_name.upper()}_API_KEY")
                    provider_config = self.config.get(f"{provider_name}_config", {})
                    self._init_provider(provider_name, api_key, provider_config)

        # Validate that at least one provider is available
        if not self.providers:
            self.logger.warning(
                "No LLM providers available. Please configure at least one provider."
            )

    def _init_provider(
        self,
        provider_name: str,
        api_key: Optional[str],
        provider_config: Dict[str, Any],
    ):
        """Initialize a specific provider"""
        provider_name = provider_name.lower()
        if provider_name in LLMService._provider_registry:
            provider_class = LLMService._provider_registry[provider_name]

            # Check if provider is available (required libraries installed)
            if provider_class.is_available():
                try:
                    # Initialize the provider - it will try to load API key from file if not provided
                    self.providers[provider_name] = provider_class(
                        api_key, provider_config
                    )

                    # Check if the provider has an API key after initialization
                    if self.providers[provider_name].api_key:
                        self.logger.info(
                            f"Initialized {provider_name} provider with API key"
                        )
                    else:
                        self.logger.warning(
                            f"Initialized {provider_name} provider without API key"
                        )

                        # If this is the default provider and it has no API key, try to find another provider
                        if provider_name == self.default_provider:
                            self.logger.warning(
                                f"Default provider {provider_name} has no API key, looking for alternatives"
                            )
                except Exception as e:
                    self.logger.error(
                        f"Error initializing {provider_name} provider: {e}"
                    )
            else:
                self.logger.warning(
                    f"{provider_name} provider not available (required libraries not installed)"
                )
        else:
            self.logger.warning(f"Unknown provider: {provider_name}")

    async def generate_text_async(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        batch_key: Optional[str] = None,
    ) -> str:
        """
        Generate text from a prompt using the specified or default provider

        Args:
            prompt: The user prompt to send to the model
            provider: The provider to use (openai, anthropic, etc.)
            model: The model to use (provider-specific)
            max_tokens: Maximum tokens in the response
            temperature: Temperature for generation
            system_prompt: Optional system prompt
            batch_key: Optional key for batching similar requests

        Returns:
            Generated text or error message
        """
        # Determine which provider to use
        active_provider = provider or self.default_provider
        active_provider = active_provider.lower()

        # Use the appropriate service
        if active_provider in self.providers:
            provider_instance = self.providers[active_provider]

            return await provider_instance.generate_text_async(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
                batch_key=batch_key,
            )
        else:
            error_msg = f"Provider '{active_provider}' not available. Please check configuration."
            self.logger.error(error_msg)
            return error_msg

    async def batch_generate_texts(
        self,
        prompts: List[str],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        batch_key: Optional[str] = None,
    ) -> List[str]:
        """
        Generate multiple texts using the specified or default provider

        Args:
            prompts: List of prompts to process
            provider: The provider to use (openai, anthropic, etc.)
            model: The model to use (provider-specific)
            max_tokens: Maximum tokens per response
            temperature: Temperature for generation
            system_prompt: Optional system prompt
            batch_key: Optional batch key for grouping similar requests

        Returns:
            List of generated texts
        """
        # Determine which provider to use
        active_provider = provider or self.default_provider
        active_provider = active_provider.lower()

        # Use the appropriate service
        if active_provider in self.providers:
            provider_instance = self.providers[active_provider]

            return await provider_instance.batch_generate_texts(
                prompts=prompts,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
                batch_key=batch_key,
            )
        else:
            error_msg = f"Provider '{active_provider}' not available. Please check configuration."
            self.logger.error(error_msg)
            return [error_msg] * len(prompts)

    def update_config(self, config_updates: Dict[str, Any]):
        """Update service configuration"""
        # Update main config
        self.config.update(config_updates)

        # Update default provider if specified
        if "default_provider" in config_updates:
            self.default_provider = config_updates["default_provider"].lower()

        # Update provider configurations
        for provider_name, provider in self.providers.items():
            if f"{provider_name}_config" in config_updates:
                provider.update_config(config_updates[f"{provider_name}_config"])

    def clear_caches(self):
        """Clear caches for all providers"""
        for provider in self.providers.values():
            provider.clear_cache()

    def get_available_providers(self) -> List[str]:
        """Get a list of available provider names"""
        return list(self.providers.keys())

    def add_provider(
        self,
        provider_name: str,
        provider_class: Type[BaseLLMProvider],
        api_key: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Add a new provider at runtime

        Args:
            provider_name: Name of the provider
            provider_class: Provider class (must inherit from BaseLLMProvider)
            api_key: API key for the provider
            config: Configuration for the provider
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise TypeError("Provider class must inherit from BaseLLMProvider")

        # Register the provider class
        LLMService.register_provider(provider_name, provider_class)

        # Initialize the provider
        self._init_provider(provider_name, api_key, config or {})
