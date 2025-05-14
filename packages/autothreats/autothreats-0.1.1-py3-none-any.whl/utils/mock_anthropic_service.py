#!/usr/bin/env python3
"""
Mock Anthropic service for the autonomous threat modeling system.
This is used when the Anthropic library is not available.
"""

import logging
from typing import Any, Dict, Optional

from .base_llm_provider import BaseLLMProvider

logger = logging.getLogger(__name__)


class MockAnthropicService(BaseLLMProvider):
    """Mock service for Anthropic API when the library is not available"""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize mock Anthropic service"""
        super().__init__(api_key, config)
        self.logger.info("Initialized Mock Anthropic Service (for testing/integration)")

    async def _make_api_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
    ) -> str:
        """Mock API request that returns a placeholder response"""
        self.logger.info(
            f"Mock Anthropic API request: model={model}, max_tokens={max_tokens}"
        )
        return "This is a mock response from the Anthropic API. The actual Anthropic library is not available."

    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        return self.config.get("default_model", "claude-3-sonnet-20240229")

    @classmethod
    def is_available(cls) -> bool:
        """This mock implementation is always available"""
        return True
