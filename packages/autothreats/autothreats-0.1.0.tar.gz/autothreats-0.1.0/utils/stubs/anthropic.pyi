"""Type stubs for anthropic module."""

from typing import Any, Dict, List, Optional, Union

class Anthropic:
    """Anthropic API client."""

    def __init__(self, api_key: str):
        """Initialize the Anthropic client."""
        pass

    def completions(
        self,
        prompt: str,
        model: str,
        max_tokens_to_sample: int,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate completions."""
        pass

    async def completions_async(
        self,
        prompt: str,
        model: str,
        max_tokens_to_sample: int,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate completions asynchronously."""
        pass
