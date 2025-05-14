#!/usr/bin/env python3
"""
OpenAI service for the autonomous threat modeling system.
Enhanced with advanced batching, caching, and configuration options.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional

from .base_llm_provider import BaseLLMProvider

logger = logging.getLogger(__name__)

# Try to import OpenAI library, but make it optional
OPENAI_AVAILABLE = False
try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI library not available. Some features will be disabled.")


class OpenAIService(BaseLLMProvider):
    """Service for interacting with OpenAI API with advanced batching and caching improvements"""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize OpenAI service with API key and configuration"""
        super().__init__(api_key, config)

        # Initialize OpenAI client
        self._initialize_client()

        # Initialize event loop for testing environments
        self._loop = None
        self._is_test_environment = False

    def _initialize_client(self):
        """Initialize the OpenAI client"""
        if not OPENAI_AVAILABLE:
            self.logger.warning("OpenAI library not available, skipping API key setup")
            return

        if self.api_key:
            if hasattr(openai, "OpenAI"):
                # Newer API style
                self._openai_client = openai.OpenAI(api_key=self.api_key)
                self._api_version = "new"
                self.logger.info("OpenAI client initialized (new API version)")
            else:
                # Older API style
                openai.api_key = self.api_key
                self._api_version = "old"
                self.logger.info("OpenAI client initialized (old API version)")
        else:
            # Try environment variable
            env_api_key = os.environ.get("OPENAI_API_KEY")
            if env_api_key:
                self.api_key = env_api_key
                if hasattr(openai, "OpenAI"):
                    # Newer API style
                    self._openai_client = openai.OpenAI(api_key=env_api_key)
                    self._api_version = "new"
                else:
                    # Older API style
                    openai.api_key = env_api_key
                    self._api_version = "old"
                self.logger.info("OpenAI API key set from environment variable")
            else:
                # Try to load API key from file as a fallback
                self.logger.info("No API key provided, trying to load from file...")
                api_key = self._load_api_key_from_file()
                if api_key:
                    self.api_key = api_key
                    if hasattr(openai, "OpenAI"):
                        # Newer API style
                        self._openai_client = openai.OpenAI(api_key=api_key)
                        self._api_version = "new"
                    else:
                        # Older API style
                        openai.api_key = api_key
                        self._api_version = "old"
                    self.logger.info("OpenAI API key loaded from file")
                else:
                    self.logger.warning("No OpenAI API key found in any location")

    def _load_api_key_from_file(self):
        """Load API key from file as a fallback"""
        import json

        # Check default locations
        default_locations = [
            os.path.expanduser("~/.openai/api_key.txt"),
            os.path.expanduser("~/.config/openai/api_key.txt"),
            os.path.expanduser("~/.config/threat-modeling/api_key.json"),
            os.path.expanduser("~/.openai/config.json"),
            os.path.expanduser("~/.config/openai/config.json"),
            os.path.expanduser("~/.openai/auth.json"),
            os.path.expanduser("~/.config/openai/auth.json"),
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
                                "openai_api_key",
                                "OPENAI_API_KEY",
                            ]:
                                if key_name in data:
                                    self.logger.info(
                                        f"✓ API key loaded from {location} (top level)"
                                    )
                                    return data[key_name]

                            # Check in nested structures
                            # Check in 'openai' section
                            if "openai" in data and isinstance(data["openai"], dict):
                                openai_section = data["openai"]
                                for key_name in ["api_key", "apiKey", "key", "secret"]:
                                    if key_name in openai_section:
                                        self.logger.info(
                                            f"✓ API key loaded from {location} (openai section)"
                                        )
                                        return openai_section[key_name]

                            # Check in 'credentials' section
                            if "credentials" in data and isinstance(
                                data["credentials"], dict
                            ):
                                creds_section = data["credentials"]
                                for key_name in [
                                    "openai_api_key",
                                    "OPENAI_API_KEY",
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
                                    "openai",
                                    "openai_api_key",
                                    "OPENAI_API_KEY",
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
        """Make an actual request to the OpenAI API"""
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
                f"OpenAI API request: model={model}, max_tokens={max_tokens}, "
                f"temperature={temperature}, system_prompt='{truncated_system}', "
                f"prompt='{truncated_prompt}'"
            )

        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not available")

        if not self.api_key:
            raise ValueError("OpenAI API key not provided")

        try:
            # Get the current event loop or create a new one if needed
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No running event loop
                if self._is_test_environment:
                    # In test environment, use a consistent loop
                    if self._loop is None:
                        self._loop = asyncio.new_event_loop()
                    loop = self._loop
                else:
                    # In normal operation, create a new loop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

            # Use the appropriate API call based on stored version
            if self._api_version == "old":
                # Older API style
                response = await self._run_in_executor(
                    loop,
                    openai.ChatCompletion.create,
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                result = response.choices[0].message.content.strip()
            else:
                # Newer API style
                response = await self._run_in_executor(
                    loop,
                    self._openai_client.chat.completions.create,
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                result = response.choices[0].message.content.strip()

            # Add verbose logging for response
            elapsed = time.time() - start_time
            if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
                truncated_result = result[:500] + "..." if len(result) > 500 else result
                token_estimate = len(prompt.split()) + len(result.split())
                self.logger.debug(
                    f"OpenAI API response in {elapsed:.2f}s: '{truncated_result}' "
                    f"(~{token_estimate} tokens)"
                )
            else:
                self.logger.info(f"OpenAI API request completed in {elapsed:.2f}s")

            return result

        except Exception as e:
            # Handle rate limit errors by falling back to a simpler model
            if model.startswith("gpt-4") and "rate_limit" in str(e).lower():
                self.logger.info("Falling back to GPT-3.5 due to rate limit")
                return await self._make_api_request(
                    prompt, "gpt-4o-mini", max_tokens, temperature, system_prompt
                )
            self.logger.error(f"OpenAI API request failed: {e}")
            raise

    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        return self.config.get("default_model", "gpt-4o-mini")

    @classmethod
    def is_available(cls) -> bool:
        """Check if this provider is available (required libraries installed)"""
        return OPENAI_AVAILABLE

    async def _run_in_executor(self, loop, func, **kwargs):
        """Run a function in an executor with proper event loop handling"""
        return await loop.run_in_executor(None, lambda: func(**kwargs))

    def set_test_environment(self, is_test=True):
        """Mark this service as being used in a test environment"""
        self._is_test_environment = is_test
        if is_test and self._loop is None:
            self._loop = asyncio.new_event_loop()
