#!/usr/bin/env python3
"""
Base LLM provider class for the autonomous threat modeling system.
This module defines the interface that all LLM providers must implement.
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


class BaseLLMProvider(ABC):
    """Base class for all LLM providers"""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the LLM provider with API key and configuration"""
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config or {}

        # Cache configuration
        self.cache_enabled = self.config.get("cache_enabled", True)
        self.cache_ttl = self.config.get("cache_ttl", 3600)  # 1 hour default
        self.max_cache_size = self.config.get(
            "max_cache_size", 1000
        )  # Limit cache size
        self.request_cache: Dict[str, Dict[str, Any]] = (
            {}
        )  # Cache for requests: {cache_key: {"result": result, "timestamp": time}}

        # Rate limiting configuration
        max_concurrent = self.config.get("max_concurrent_requests", 3)
        self.request_semaphore = asyncio.Semaphore(max_concurrent)

        # Batching configuration
        self.batch_enabled = self.config.get("batch_enabled", True)
        self.batch_window = self.config.get(
            "batch_window", 0.1
        )  # 100ms window for batching
        self.max_batch_size = self.config.get("max_batch_size", 20)
        self.batched_requests: Dict[
            str, List[Tuple[str, asyncio.Future, str, str, int, float]]
        ] = defaultdict(
            list
        )  # {model: [(prompt, future, cache_key, system_prompt, max_tokens, temperature)]}
        self.batch_tasks: Dict[str, asyncio.Task] = {}  # {model: task}

        # Precompile regex patterns for JSON extraction
        self.json_pattern = re.compile(r"(\{.*\})", re.DOTALL)

    @abstractmethod
    async def _make_api_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
    ) -> str:
        """Make an actual request to the LLM API"""
        pass

    async def generate_text_async(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        cache_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        batch_key: Optional[str] = None,
    ) -> str:
        """
        Generate text from a prompt asynchronously with caching and batching

        Args:
            prompt: The user prompt to send to the model
            model: The model to use (provider-specific)
            max_tokens: Maximum tokens in the response
            temperature: Temperature for generation
            cache_key: Optional custom cache key
            system_prompt: Optional system prompt
            batch_key: Optional key for batching similar requests

        Returns:
            Generated text or error message
        """
        # Set default model if not provided
        if model is None:
            model = self.get_default_model()

        # Set default system prompt if not provided
        if system_prompt is None:
            system_prompt = """You are an expert security vulnerability analyst specializing in code review and threat modeling.
            
Your primary responsibilities are:
1. Accurately identify security vulnerabilities in code across multiple programming languages
2. Analyze data flows to trace how untrusted input could lead to security issues
3. Evaluate input validation and sanitization mechanisms
4. Distinguish genuine vulnerabilities from false positives with high precision
5. Provide language-specific, actionable remediation guidance
6. Assess exploitation difficulty and prerequisites
7. Connect vulnerabilities to real-world attack techniques and tactics

Always consider the specific programming language context when analyzing code. Different languages have different security models, common vulnerabilities, and best practices. Never identify web-specific vulnerabilities like XSS in non-web languages like C.

Base your analysis strictly on the provided code evidence. Avoid speculation about code you cannot see. When uncertain, clearly indicate your confidence level and explain your reasoning."""

        # Generate cache key if not provided
        if cache_key is None:
            # Create a more robust hash using content
            hash_input = f"{prompt}_{model}_{max_tokens}_{temperature}_{system_prompt}"
            cache_key = hashlib.md5(hash_input.encode()).hexdigest()

        # Check cache first if enabled
        if self.cache_enabled and cache_key in self.request_cache:
            cache_entry = self.request_cache[cache_key]
            # Check if cache entry is still valid
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                self.logger.info(f"Cache hit for request {cache_key[:10]}...")
                return cache_entry["result"]
            else:
                # Remove expired cache entry
                del self.request_cache[cache_key]

        # Clean cache if it exceeds max size
        if self.cache_enabled and len(self.request_cache) >= self.max_cache_size:
            self._clean_cache()

        # If batching is enabled and a batch key is provided, use batched request
        if self.batch_enabled and batch_key:
            return await self._batch_request(
                prompt,
                model,
                max_tokens,
                temperature,
                system_prompt,
                cache_key,
                batch_key,
            )

        # Otherwise, use regular request with semaphore
        async with self.request_semaphore:
            try:
                result = await self._make_api_request(
                    prompt, model, max_tokens, temperature, system_prompt
                )

                # Cache the result if caching is enabled
                if self.cache_enabled:
                    self.request_cache[cache_key] = {
                        "result": result,
                        "timestamp": time.time(),
                        "size": (
                            len(result) if result else 0
                        ),  # Track size for cache management
                    }
                return result

            except Exception as e:
                self.logger.error(f"Error generating text: {e}")
                # Return a meaningful error message that won't break JSON parsing
                return json.dumps(
                    {
                        "error": str(e),
                        "message": f"Error generating text with {self.__class__.__name__}",
                    }
                )

    async def _batch_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
        cache_key: str,
        batch_key: str,
    ) -> str:
        """Add request to batch and wait for result"""
        # Create a future to receive the result
        future: asyncio.Future = asyncio.Future()

        # Add to batch queue
        batch_id = f"{model}_{batch_key}"
        self.batched_requests[batch_id].append(
            (prompt, future, cache_key, system_prompt, max_tokens, temperature)
        )

        # Start batch processor if not already running
        if batch_id not in self.batch_tasks or self.batch_tasks[batch_id].done():
            self.batch_tasks[batch_id] = asyncio.create_task(
                self._process_batch(batch_id, model)
            )

        # Wait for result
        return await future

    async def _process_batch(self, batch_id: str, model: str):
        """Process a batch of requests after a short delay"""
        try:
            # Wait for batch window to collect requests
            await asyncio.sleep(self.batch_window)

            # Get all requests in the current batch
            requests = self.batched_requests.pop(batch_id, [])
            if not requests:
                return

            self.logger.info(
                f"Processing batch of {len(requests)} requests for model {model}"
            )

            # Process in sub-batches to avoid exceeding API limits
            for i in range(0, len(requests), self.max_batch_size):
                sub_batch = requests[i : i + self.max_batch_size]

                # Process this sub-batch
                async with self.request_semaphore:
                    try:
                        # Group requests by system prompt for more efficient batching
                        grouped_requests = {}
                        for (
                            prompt,
                            future,
                            cache_key,
                            system_prompt,
                            max_tokens,
                            temperature,
                        ) in sub_batch:
                            # Check cache again (might have been added since request was queued)
                            if self.cache_enabled and cache_key in self.request_cache:
                                cache_entry = self.request_cache[cache_key]
                                if (
                                    time.time() - cache_entry["timestamp"]
                                    < self.cache_ttl
                                ):
                                    future.set_result(cache_entry["result"])
                                    continue

                            # Group by system prompt
                            key = (system_prompt, max_tokens, temperature)
                            if key not in grouped_requests:
                                grouped_requests[key] = []
                            grouped_requests[key].append((prompt, future, cache_key))

                        # Process each group in parallel
                        tasks = []
                        for (
                            system_prompt,
                            max_tokens,
                            temperature,
                        ), group in grouped_requests.items():
                            for prompt, future, cache_key in group:
                                tasks.append(
                                    self._process_single_request(
                                        prompt,
                                        model,
                                        max_tokens,
                                        temperature,
                                        system_prompt,
                                        future,
                                        cache_key,
                                    )
                                )

                        # Wait for all requests to complete
                        if tasks:
                            await asyncio.gather(*tasks)

                    except Exception as e:
                        # Set exception for all futures in this sub-batch
                        for _, future, _, _, _, _ in sub_batch:
                            if not future.done():
                                future.set_exception(e)

                # Small delay between sub-batches
                if i + self.max_batch_size < len(requests):
                    await asyncio.sleep(0.5)

        except Exception as e:
            self.logger.error(f"Error processing batch {batch_id}: {e}")
            # Set exception for any remaining futures
            for _, future, _, _, _, _ in self.batched_requests.get(batch_id, []):
                if not future.done():
                    future.set_exception(e)

    async def _process_single_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
        future: asyncio.Future,
        cache_key: str,
    ):
        """Process a single request and set its result"""
        try:
            # Make the API request
            result = await self._make_api_request(
                prompt, model, max_tokens, temperature, system_prompt
            )

            # Cache the result
            if self.cache_enabled:
                self.request_cache[cache_key] = {
                    "result": result,
                    "timestamp": time.time(),
                    "size": len(result) if result else 0,
                }

            # Set the result in the future if not already done
            if not future.done():
                future.set_result(result)
        except Exception as e:
            # Set exception if future not already done
            if not future.done():
                future.set_exception(e)

    def _clean_cache(self):
        """Clean the cache when it exceeds the maximum size"""
        if not self.request_cache:
            return

        # Strategy 1: Remove expired entries
        current_time = time.time()
        expired_keys = [
            k
            for k, v in self.request_cache.items()
            if current_time - v["timestamp"] > self.cache_ttl
        ]

        for key in expired_keys:
            del self.request_cache[key]

        # If still too large, remove oldest entries
        if len(self.request_cache) > self.max_cache_size:
            # Sort by timestamp (oldest first)
            sorted_items = sorted(
                self.request_cache.items(), key=lambda x: x[1]["timestamp"]
            )

            # Remove oldest items until we're under the limit
            items_to_remove = len(self.request_cache) - self.max_cache_size
            for i in range(items_to_remove):
                if i < len(sorted_items):
                    del self.request_cache[sorted_items[i][0]]

    async def batch_generate_texts(
        self,
        prompts: List[str],
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        batch_key: Optional[str] = None,
    ) -> List[str]:
        """
        Generate multiple texts in an efficient way with improved batching

        Args:
            prompts: List of prompts to process
            model: Model to use
            max_tokens: Maximum tokens per response
            temperature: Temperature for generation
            system_prompt: Optional system prompt
            batch_key: Optional batch key for grouping similar requests

        Returns:
            List of generated texts
        """
        # Set default model if not provided
        if model is None:
            model = self.get_default_model()

        # If batch_key is provided, use it to batch all requests together
        if batch_key and self.batch_enabled:
            tasks = []
            for i, prompt in enumerate(prompts):
                # Create a unique cache key for each prompt
                hash_input = (
                    f"{prompt}_{model}_{max_tokens}_{temperature}_{system_prompt or ''}"
                )
                cache_key = hashlib.md5(hash_input.encode()).hexdigest()

                # Add to tasks
                tasks.append(
                    self.generate_text_async(
                        prompt=prompt,
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        cache_key=cache_key,
                        system_prompt=system_prompt,
                        batch_key=f"{batch_key}_{i//self.max_batch_size}",  # Group into sub-batches
                    )
                )

            # Process all tasks
            return await asyncio.gather(*tasks)
        else:
            # Process in batches with semaphore control
            results = []

            # Determine optimal batch size based on config
            batch_size = min(self.config.get("batch_size", 5), 20)

            for i in range(0, len(prompts), batch_size):
                batch = prompts[i : i + batch_size]
                batch_tasks = [
                    self.generate_text_async(
                        prompt=prompt,
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system_prompt=system_prompt,
                    )
                    for prompt in batch
                ]
                batch_results = await asyncio.gather(*batch_tasks)
                results.extend(batch_results)

                # Add a small delay between batches to avoid rate limiting
                if i + batch_size < len(prompts):
                    await asyncio.sleep(self.config.get("batch_delay", 1))

            return results

    def update_config(self, config_updates: Dict[str, Any]):
        """Update service configuration"""
        # Update config dictionary
        self.config.update(config_updates)

        # Update all derived settings at once
        self.cache_enabled = self.config.get("cache_enabled", self.cache_enabled)
        self.cache_ttl = self.config.get("cache_ttl", self.cache_ttl)
        self.max_cache_size = self.config.get("max_cache_size", self.max_cache_size)
        self.batch_enabled = self.config.get("batch_enabled", self.batch_enabled)
        self.batch_window = self.config.get("batch_window", self.batch_window)
        self.max_batch_size = self.config.get("max_batch_size", self.max_batch_size)

        # Update semaphore if max_concurrent_requests changed
        if "max_concurrent_requests" in config_updates:
            self.request_semaphore = asyncio.Semaphore(
                config_updates["max_concurrent_requests"]
            )

    def clear_cache(self):
        """Clear the request cache"""
        self.request_cache.clear()
        self.logger.info("Request cache cleared")

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        pass

    @classmethod
    def is_available(cls) -> bool:
        """Check if this provider is available (required libraries installed)"""
        return True
