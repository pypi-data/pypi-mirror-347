#!/usr/bin/env python3
"""
Base classes and utilities for async tests
"""

import asyncio
import unittest

import pytest


class AsyncTestCase(unittest.IsolatedAsyncioTestCase):
    """Base class for async tests"""

    async def asyncSetUp(self):
        """Set up the test"""
        pass

    async def asyncTearDown(self):
        """Tear down the test"""
        pass


def async_test(func):
    """Decorator for async test methods"""

    @pytest.mark.asyncio
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
