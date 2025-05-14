#!/usr/bin/env python3
"""
Anthropic service for the autonomous threat modeling system.
Provides integration with Anthropic's Claude models.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional

from .base_llm_provider import BaseLLMProvider

logger = logging.getLogger(__name__)

# Try to import Anthropic library, but make it optional
ANTHROPIC_AVAILABLE = False
try:
    import anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    logger.warning("Anthropic library not available. Claude features will be disabled.")


class AnthropicService(BaseLLMProvider):
    """Service for interacting with Anthropic API with advanced batching and caching"""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Anthropic service with API key and configuration"""
        super().__init__(api_key, config)

        # Initialize Anthropic client
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Anthropic client"""
        if not ANTHROPIC_AVAILABLE:
            self.logger.warning(
                "Anthropic library not available, skipping API key setup"
            )
            return

        if self.api_key:
            self._anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            self.logger.info("Anthropic client initialized")
        else:
            # Try environment variable
            env_api_key = os.environ.get("ANTHROPIC_API_KEY")
            if env_api_key:
                self.api_key = env_api_key
                self._anthropic_client = anthropic.Anthropic(api_key=env_api_key)
                self.logger.info("Anthropic API key set from environment variable")
            else:
                # Try to load API key from file as a fallback
                self.logger.info("No API key provided, trying to load from file...")
                api_key = self._load_api_key_from_file()
                if api_key:
                    self.api_key = api_key
                    self._anthropic_client = anthropic.Anthropic(api_key=api_key)
                    self.logger.info("Anthropic API key loaded from file")
                else:
                    self.logger.warning("No Anthropic API key found in any location")

    def _load_api_key_from_file(self):
        """Load API key from file as a fallback"""
        import json

        # Check default locations
        default_locations = [
            os.path.expanduser("~/.anthropic/api_key.txt"),
            os.path.expanduser("~/.config/anthropic/api_key.txt"),
            os.path.expanduser("~/.config/threat-modeling/api_key.json"),
            os.path.expanduser("~/.anthropic/config.json"),
            os.path.expanduser("~/.config/anthropic/config.json"),
            os.path.expanduser("~/.anthropic/auth.json"),
            os.path.expanduser("~/.config/anthropic/auth.json"),
            # Also check OpenAI locations as fallback
            os.path.expanduser("~/.openai/api_key.txt"),
            os.path.expanduser("~/.config/openai/api_key.txt"),
            os.path.expanduser("~/.openai/config.json"),
            os.path.expanduser("~/.config/openai/config.json"),
        ]

        for location in default_locations:
            if os.path.exists(location):
                try:
                    with open(location, "r") as f:
                        content = f.read().strip()

                        # Try to parse as JSON
                        try:
                            data = json.loads(content)
                            # Look for common key names at the top level
                            for key_name in [
                                "api_key",
                                "apiKey",
                                "key",
                                "secret",
                                "anthropic_api_key",
                                "ANTHROPIC_API_KEY",
                            ]:
                                if key_name in data:
                                    self.logger.info(
                                        f"✓ API key loaded from {location} (top level)"
                                    )
                                    return data[key_name]

                            # Check in nested structures
                            # Check in 'anthropic' section
                            if "anthropic" in data and isinstance(
                                data["anthropic"], dict
                            ):
                                anthropic_section = data["anthropic"]
                                for key_name in ["api_key", "apiKey", "key", "secret"]:
                                    if key_name in anthropic_section:
                                        self.logger.info(
                                            f"✓ API key loaded from {location} (anthropic section)"
                                        )
                                        return anthropic_section[key_name]

                            # Check in 'credentials' section
                            if "credentials" in data and isinstance(
                                data["credentials"], dict
                            ):
                                creds_section = data["credentials"]
                                for key_name in [
                                    "anthropic_api_key",
                                    "ANTHROPIC_API_KEY",
                                    "api_key",
                                    "apiKey",
                                ]:
                                    if key_name in creds_section:
                                        self.logger.info(
                                            f"✓ API key loaded from {location} (credentials section)"
                                        )
                                        return creds_section[key_name]

                            # Check in 'api_keys' section
                            if "api_keys" in data and isinstance(
                                data["api_keys"], dict
                            ):
                                keys_section = data["api_keys"]
                                for key_name in [
                                    "anthropic",
                                    "anthropic_api_key",
                                    "ANTHROPIC_API_KEY",
                                ]:
                                    if key_name in keys_section:
                                        self.logger.info(
                                            f"✓ API key loaded from {location} (api_keys section)"
                                        )
                                        return keys_section[key_name]
                        except json.JSONDecodeError:
                            # Not JSON, assume plain text
                            self.logger.info(
                                f"✓ API key loaded from {location} (plain text)"
                            )
                            return content
                except Exception as e:
                    self.logger.warning(f"Error loading API key from {location}: {e}")

        return None

    async def _make_api_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
    ) -> str:
        """Make an actual request to the Anthropic API"""
        start_time = time.time()

        # Add verbose logging
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            truncated_prompt = prompt[:500] + "..." if len(prompt) > 500 else prompt
            truncated_system = (
                system_prompt[:200] + "..."
                if len(system_prompt) > 200
                else system_prompt
            )
            self.logger.debug(
                f"Anthropic API request: model={model}, max_tokens={max_tokens}, "
                f"temperature={temperature}, system_prompt='{truncated_system}', "
                f"prompt='{truncated_prompt}'"
            )

        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic library not available")

        if not self.api_key:
            raise ValueError("Anthropic API key not provided")

        try:
            # Create message content
            messages = []

            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Add user prompt
            messages.append({"role": "user", "content": prompt})

            # Make the API call
            response = await asyncio.to_thread(
                self._anthropic_client.messages.create,
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Extract the response content
            result = response.content[0].text.strip()

            # Add verbose logging for response
            elapsed = time.time() - start_time
            if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
                truncated_result = result[:500] + "..." if len(result) > 500 else result
                token_estimate = len(prompt.split()) + len(result.split())
                self.logger.debug(
                    f"Anthropic API response in {elapsed:.2f}s: '{truncated_result}' "
                    f"(~{token_estimate} tokens)"
                )
            else:
                self.logger.info(f"Anthropic API request completed in {elapsed:.2f}s")

            return result

        except Exception as e:
            self.logger.error(f"Anthropic API request failed: {e}")
            raise

    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        return self.config.get("default_model", "claude-3-sonnet-20240229")

    @classmethod
    def is_available(cls) -> bool:
        """Check if this provider is available (required libraries installed)"""
        return ANTHROPIC_AVAILABLE
