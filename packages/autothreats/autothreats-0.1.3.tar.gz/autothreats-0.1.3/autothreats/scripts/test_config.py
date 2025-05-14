#!/usr/bin/env python3
"""
Test script for the configuration system.
This script loads a configuration file and prints its contents.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml

# Add parent directory to path to allow importing from autothreats
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from autothreats.utils.config import generate_config, load_config, validate_config

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the configuration test script"""
    parser = argparse.ArgumentParser(description="Test the configuration system")
    parser.add_argument("--config", "-c", help="Path to configuration file")
    parser.add_argument(
        "--generate", "-g", action="store_true", help="Generate a configuration file"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./test-config.yaml",
        help="Path to save the generated configuration file",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format (yaml or json)",
    )

    args = parser.parse_args()

    # Generate configuration file if requested
    if args.generate:
        logger.info(f"Generating configuration file at {args.output}")
        success = generate_config(args.output)
        if success:
            logger.info(f"Configuration file generated successfully at {args.output}")
        else:
            logger.error(f"Failed to generate configuration file at {args.output}")
        return 0 if success else 1

    # Load configuration
    config = load_config(args.config)

    # Validate configuration
    errors = validate_config(config)
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        return 1

    # Print configuration
    logger.info("Configuration loaded successfully")

    if args.format == "yaml":
        print(yaml.dump(config, default_flow_style=False, sort_keys=False))
    else:
        print(json.dumps(config, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
