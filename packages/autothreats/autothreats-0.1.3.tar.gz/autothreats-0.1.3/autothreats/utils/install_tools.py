#!/usr/bin/env python3
"""
Utility module for installing required security tools.
"""

import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def install_all_tools() -> bool:
    """
    Install all required security tools.

    Returns:
        bool: True if all tools were installed successfully, False otherwise
    """
    logger.info("Installing all required security tools...")

    # List of tools to install
    tools = [
        {
            "name": "RedFlag",
            "installer": install_redflag,
            "required": False,
        },
        {
            "name": "CodeShield",
            "installer": install_codeshield,
            "required": False,
        },
    ]

    # Track success
    all_success = True

    # Install each tool
    for tool in tools:
        try:
            name = tool["name"]
            installer = tool["installer"]
            required = tool["required"]

            logger.info(f"Installing {name}...")
            success = installer()

            if success:
                logger.info(f"✓ {name} installed successfully")
            else:
                logger.warning(f"✗ {name} installation failed")
                if required:
                    all_success = False
        except Exception as e:
            logger.error(f"Error installing {tool['name']}: {e}")
            if tool["required"]:
                all_success = False

    return all_success


def install_redflag() -> bool:
    """
    Install RedFlag security tool.

    Returns:
        bool: True if installed successfully, False otherwise
    """
    try:
        # Check if RedFlag is already installed
        try:
            import redflag

            logger.info("RedFlag is already installed")
            return True
        except ImportError:
            pass

        # Install RedFlag
        logger.info("Installing RedFlag...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "redflag"])

        # Verify installation
        try:
            import redflag

            logger.info("RedFlag installed successfully")
            return True
        except ImportError:
            logger.warning("RedFlag installation verification failed")
            return False
    except Exception as e:
        logger.error(f"Error installing RedFlag: {e}")
        return False


def install_codeshield() -> bool:
    """
    Install CodeShield security tool.

    Returns:
        bool: True if installed successfully, False otherwise
    """
    try:
        # Check if CodeShield is already installed
        try:
            import codeshield

            logger.info("CodeShield is already installed")
            return True
        except ImportError:
            pass

        # Install CodeShield
        logger.info("Installing CodeShield...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "codeshield"])

        # Verify installation
        try:
            import codeshield

            logger.info("CodeShield installed successfully")
            return True
        except ImportError:
            logger.warning("CodeShield installation verification failed")
            return False
    except Exception as e:
        logger.error(f"Error installing CodeShield: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Install all tools
    success = install_all_tools()

    if success:
        logger.info("All tools installed successfully")
        sys.exit(0)
    else:
        logger.error("Some required tools could not be installed")
        sys.exit(1)
