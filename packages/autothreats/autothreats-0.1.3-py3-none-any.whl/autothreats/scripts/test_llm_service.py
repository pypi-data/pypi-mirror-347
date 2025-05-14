#!/usr/bin/env python3
"""
Test script for the LLM service with both OpenAI and Anthropic support.
This script demonstrates how to use the unified LLM service with different providers.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from autothreats.utils.llm_service import LLMService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_llm_service")


async def test_llm_service(config: Dict[str, Any], prompt: str):
    """Test the LLM service with the given configuration and prompt"""
    logger.info("Initializing LLM service...")
    llm_service = LLMService(config)

    # Test OpenAI if enabled
    if config.get("enable_openai", True):
        logger.info("Testing OpenAI...")
        try:
            openai_response = await llm_service.generate_text_async(
                prompt=prompt,
                provider="openai",
                model=config.get("openai_model", "gpt-4o-mini"),
                max_tokens=100,
                temperature=0.7,
                system_prompt="You are a helpful assistant.",
            )
            logger.info(f"OpenAI response: {openai_response}")
        except Exception as e:
            logger.error(f"Error with OpenAI: {e}")

    # Test Anthropic if enabled
    if config.get("enable_anthropic", False):
        logger.info("Testing Anthropic...")
        try:
            anthropic_response = await llm_service.generate_text_async(
                prompt=prompt,
                provider="anthropic",
                model=config.get("anthropic_model", "claude-3-sonnet-20240229"),
                max_tokens=100,
                temperature=0.7,
                system_prompt="You are a helpful assistant.",
            )
            logger.info(f"Anthropic response: {anthropic_response}")
        except Exception as e:
            logger.error(f"Error with Anthropic: {e}")

    # Test batch generation if enabled
    if config.get("test_batch", False):
        logger.info("Testing batch generation...")
        prompts = [f"{prompt} (variation {i+1})" for i in range(3)]

        # Test with default provider
        try:
            batch_responses = await llm_service.batch_generate_texts(
                prompts=prompts,
                max_tokens=100,
                temperature=0.7,
                system_prompt="You are a helpful assistant.",
                batch_key="test_batch",
            )

            for i, response in enumerate(batch_responses):
                logger.info(f"Batch response {i+1}: {response}")
        except Exception as e:
            logger.error(f"Error with batch generation: {e}")


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Test the LLM service with different providers"
    )

    # Add arguments
    parser.add_argument(
        "--prompt",
        default="Explain the concept of threat modeling in cybersecurity",
        help="The prompt to send to the LLM",
    )
    parser.add_argument(
        "--openai-key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (defaults to OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--anthropic-key",
        default=os.environ.get("ANTHROPIC_API_KEY"),
        help="Anthropic API key (defaults to ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "anthropic"],
        help="Default provider to use",
    )
    parser.add_argument(
        "--openai-model", default="gpt-4o-mini", help="OpenAI model to use"
    )
    parser.add_argument(
        "--anthropic-model",
        default="claude-3-sonnet-20240229",
        help="Anthropic model to use",
    )
    parser.add_argument(
        "--enable-anthropic", action="store_true", help="Enable Anthropic provider"
    )
    parser.add_argument(
        "--test-batch", action="store_true", help="Test batch generation"
    )

    args = parser.parse_args()

    # Create configuration
    config = {
        "default_provider": args.provider,
        "openai_api_key": args.openai_key,
        "anthropic_api_key": args.anthropic_key,
        "enable_openai": bool(args.openai_key),
        "enable_anthropic": args.enable_anthropic and bool(args.anthropic_key),
        "openai_model": args.openai_model,
        "anthropic_model": args.anthropic_model,
        "test_batch": args.test_batch,
        "cache_enabled": True,
        "batch_enabled": True,
    }

    # Validate configuration
    if not config["openai_api_key"] and not (
        config["enable_anthropic"] and config["anthropic_api_key"]
    ):
        logger.info("No API keys provided via arguments or environment variables.")
        logger.info("Attempting to load API keys from default locations...")

        # Try to load OpenAI API key from file
        try:
            from autothreats.utils.openai_service import OpenAIService

            openai_service = OpenAIService()
            if openai_service.api_key:
                logger.info("Successfully loaded OpenAI API key from file")
                config["openai_api_key"] = openai_service.api_key
                config["enable_openai"] = True
        except Exception as e:
            logger.warning(f"Error loading OpenAI API key: {e}")

        # Try to load Anthropic API key from file if enabled
        if args.enable_anthropic:
            try:
                from autothreats.utils.anthropic_service import AnthropicService

                anthropic_service = AnthropicService()
                if anthropic_service.api_key:
                    logger.info("Successfully loaded Anthropic API key from file")
                    config["anthropic_api_key"] = anthropic_service.api_key
                    config["enable_anthropic"] = True
            except Exception as e:
                logger.warning(f"Error loading Anthropic API key: {e}")

        # Check if we have at least one API key now
        if not config["openai_api_key"] and not (
            config["enable_anthropic"] and config["anthropic_api_key"]
        ):
            logger.error("No API keys found. Please provide at least one API key.")
            sys.exit(1)

    # Run the test
    asyncio.run(test_llm_service(config, args.prompt))


if __name__ == "__main__":
    main()
