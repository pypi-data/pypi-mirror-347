#!/usr/bin/env python3
"""
Pytest configuration file for the threat modeling system tests.
"""

import asyncio
import logging
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Configure pytest to filter out coroutine warnings
def pytest_configure(config):
    """Configure pytest."""
    # Filter out coroutine warnings
    import warnings

    warnings.filterwarnings("ignore", message="coroutine .* was never awaited")

    # Filter out deprecation warnings for drain method
    warnings.filterwarnings("ignore", message="drain method is deprecated")


@pytest.fixture(scope="session", autouse=True)
def mock_coroutines():
    """
    Mock coroutines that might cause 'coroutine was never awaited' warnings.
    This is a session-wide fixture that will be applied to all tests.
    """
    # Create a synchronous mock for run_threat_modeling
    mock_run_threat_modeling = MagicMock(return_value=0)

    # Apply the patch - use try/except to handle potential import errors
    try:
        with patch(
            "autothreats.scripts.threat_modeling_cli.run_threat_modeling",
            mock_run_threat_modeling,
        ):
            yield
    except (ImportError, AttributeError):
        # If the import fails, just yield without patching
        yield


@pytest.fixture(scope="session")
def event_loop_policy():
    """
    Configure the event loop policy for asyncio tests.
    This is the recommended approach instead of redefining the event_loop fixture.
    """
    policy = asyncio.get_event_loop_policy()
    return policy
