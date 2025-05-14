#!/usr/bin/env python3
"""
Configuration generator script for the autonomous threat modeling system.
This script generates a default configuration file in YAML format.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to allow importing from autothreats
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from autothreats.utils.config import DEFAULT_CONFIG, generate_config


def generate_default_config(output_path="./threat-canvas.yaml", force=False):
    """
    Generate a default configuration file.

    Args:
        output_path: Path to save the configuration file
        force: Whether to overwrite existing file

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if file exists and force flag is not set
    if os.path.exists(output_path) and not force:
        logger.error(
            f"Configuration file {output_path} already exists. Use force=True to overwrite."
        )
        return False

    # Generate configuration file
    return generate_config(output_path)


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the configuration generator"""
    parser = argparse.ArgumentParser(
        description="Generate a configuration file for the autonomous threat modeling system"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./threat-canvas.yaml",
        help="Path to save the configuration file (default: ./threat-canvas.yaml)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing configuration file if it exists",
    )
    parser.add_argument(
        "--print",
        "-p",
        action="store_true",
        help="Print the configuration to stdout instead of saving to a file",
    )

    args = parser.parse_args()

    # Check if file exists and force flag is not set
    if os.path.exists(args.output) and not args.force and not args.print:
        logger.error(
            f"Configuration file {args.output} already exists. Use --force to overwrite."
        )
        return 1

    # Print configuration to stdout if requested
    if args.print:
        import yaml

        print(yaml.dump(DEFAULT_CONFIG, default_flow_style=False, sort_keys=False))
        return 0

    # Generate configuration file
    success = generate_config(args.output)

    if success:
        logger.info(f"Configuration file generated at {args.output}")
        return 0
    else:
        logger.error(f"Failed to generate configuration file at {args.output}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
