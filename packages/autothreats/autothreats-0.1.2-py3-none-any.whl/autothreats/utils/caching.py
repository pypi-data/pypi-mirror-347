#!/usr/bin/env python3
"""
Caching utilities for the autonomous threat modeling system.
Provides a simple in-memory cache with optional persistence.
"""

import json
import logging
import os
import time
from typing import Any, Dict, Optional, Tuple, Union

logger = logging.getLogger(__name__)


class Cache:
    """
    Simple in-memory cache with optional persistence to disk.
    Used for caching expensive operations like LLM calls.
    """

    def __init__(
        self,
        name: str = "default",
        ttl: int = 3600,
        max_size: int = 1000,
        persist_path: Optional[str] = None,
    ):
        """
        Initialize a new cache instance.

        Args:
            name: Name of the cache for identification
            ttl: Time-to-live in seconds for cache entries (default: 1 hour)
            max_size: Maximum number of entries to store in the cache
            persist_path: Optional path to persist cache to disk
        """
        self.name = name
        self.ttl = ttl
        self.max_size = max_size
        self.persist_path = persist_path
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.hits = 0
        self.misses = 0

        # Load from disk if persist_path is provided
        if persist_path and os.path.exists(persist_path):
            self._load_from_disk()

        logger.debug(f"Initialized cache '{name}' with ttl={ttl}s, max_size={max_size}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache.

        Args:
            key: Cache key
            default: Default value to return if key not found

        Returns:
            Cached value or default if not found
        """
        if key in self.cache:
            value, timestamp = self.cache[key]

            # Check if entry has expired
            if time.time() - timestamp > self.ttl:
                logger.debug(f"Cache '{self.name}': Entry for key '{key}' expired")
                del self.cache[key]
                self.misses += 1
                return default

            self.hits += 1
            logger.debug(f"Cache '{self.name}': Hit for key '{key}'")
            return value

        self.misses += 1
        logger.debug(f"Cache '{self.name}': Miss for key '{key}'")
        return default

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        # Enforce max size by removing oldest entries if needed
        if len(self.cache) >= self.max_size and key not in self.cache:
            # Sort by timestamp and remove oldest
            oldest_key = sorted(self.cache.items(), key=lambda x: x[1][1])[0][0]
            del self.cache[oldest_key]
            logger.debug(f"Cache '{self.name}': Removed oldest entry '{oldest_key}'")

        self.cache[key] = (value, time.time())
        logger.debug(f"Cache '{self.name}': Set value for key '{key}'")

        # Persist to disk if configured
        if self.persist_path:
            self._persist_to_disk()

    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.

        Args:
            key: Cache key to delete

        Returns:
            True if key was found and deleted, False otherwise
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache '{self.name}': Deleted key '{key}'")

            # Persist changes if configured
            if self.persist_path:
                self._persist_to_disk()

            return True
        return False

    def clear(self) -> None:
        """Clear all entries from the cache."""
        self.cache.clear()
        logger.debug(f"Cache '{self.name}': Cleared all entries")

        # Persist changes if configured
        if self.persist_path:
            self._persist_to_disk()

    def _persist_to_disk(self) -> None:
        """Persist cache to disk if persist_path is set."""
        if not self.persist_path:
            return

        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)

            # Convert to serializable format
            serializable = {
                "name": self.name,
                "ttl": self.ttl,
                "max_size": self.max_size,
                "entries": {
                    k: (v, ts)
                    for k, (v, ts) in self.cache.items()
                    if isinstance(v, (str, int, float, bool, list, dict, type(None)))
                },
            }

            with open(self.persist_path, "w") as f:
                json.dump(serializable, f)

            logger.debug(
                f"Cache '{self.name}': Persisted {len(serializable['entries'])} entries to {self.persist_path}"
            )
        except Exception as e:
            logger.error(f"Cache '{self.name}': Failed to persist to disk: {str(e)}")

    def _load_from_disk(self) -> None:
        """Load cache from disk if persist_path is set."""
        if not self.persist_path or not os.path.exists(self.persist_path):
            return

        try:
            with open(self.persist_path, "r", errors="replace") as f:
                data = json.load(f)

            # Update cache settings
            self.name = data.get("name", self.name)
            self.ttl = data.get("ttl", self.ttl)
            self.max_size = data.get("max_size", self.max_size)

            # Load entries
            entries = data.get("entries", {})
            current_time = time.time()

            # Only load non-expired entries
            for key, (value, timestamp) in entries.items():
                if current_time - timestamp <= self.ttl:
                    self.cache[key] = (value, timestamp)

            logger.debug(
                f"Cache '{self.name}': Loaded {len(self.cache)} entries from {self.persist_path}"
            )
        except Exception as e:
            logger.error(f"Cache '{self.name}': Failed to load from disk: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "name": self.name,
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl": self.ttl,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": (
                self.hits / (self.hits + self.misses)
                if (self.hits + self.misses) > 0
                else 0
            ),
            "persisted": self.persist_path is not None,
        }
