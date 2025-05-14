#!/usr/bin/env python3
"""
Command-line interface for Threat Canvas - an advanced autonomous threat modeling system.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

import yaml

from autothreats.system import System as ThreatModelingSystem

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Version
__version__ = "0.1.0"


def load_config_file(config_file: str) -> Dict[str, Any]:
    """Load configuration from a JSON or YAML file"""
    if not os.path.exists(config_file):
        logger.error(f"Configuration file not found: {config_file}")
        return {}

    try:
        with open(config_file, "r") as f:
            if config_file.endswith(".json"):
                return json.load(f)
            elif config_file.endswith((".yaml", ".yml")):
                try:
                    import yaml

                    return yaml.safe_load(f)
                except ImportError:
                    logger.error(
                        "YAML support requires PyYAML. Install with: pip install pyyaml"
                    )
                    return {}
            else:
                # Try JSON first, then YAML
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    try:
                        import yaml

                        f.seek(0)  # Reset file pointer
                        return yaml.safe_load(f)
                    except ImportError:
                        logger.error(
                            "YAML support requires PyYAML. Install with: pip install pyyaml"
                        )
                        return {}
                    except Exception as e:
                        logger.error(f"Failed to parse config file: {e}")
                        return {}
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        return {}


async def run_threat_modeling(args):
    """Run the threat modeling system with CLI arguments"""
    # Set default output directory
    output_dir = args.output or os.getcwd()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load configuration from file if specified
    config = {}
    if args.config:
        config = load_config_file(args.config)

    # Override with command line arguments
    if not "openai" in config:
        config["openai"] = {}

    if args.api_key:
        config["openai"]["api_key"] = args.api_key

    config["output_dir"] = output_dir

    # Add agent-specific configurations from command line
    if args.max_commits:
        if "agents" not in config:
            config["agents"] = {}
        if "commit_history" not in config["agents"]:
            config["agents"]["commit_history"] = {}
        config["agents"]["commit_history"]["max_commits"] = args.max_commits

    # Add max_files configuration if specified
    if args.max_files:
        if "agents" not in config:
            config["agents"] = {}
        if "code_ingestion" not in config["agents"]:
            config["agents"]["code_ingestion"] = {}
        config["agents"]["code_ingestion"]["max_files"] = args.max_files
        # Also update lightweight_max_files to match
        config["agents"]["code_ingestion"]["lightweight_max_files"] = args.max_files
        logger.info(f"Maximum files to process set to: {args.max_files}")

    # Handle RedFlag options
    if args.enable_redflag:
        config["enable_redflag"] = True
    elif args.disable_redflag:
        config["enable_redflag"] = False

    # Handle CodeShield options
    if args.enable_codeshield:
        config["enable_codeshield"] = True
    elif args.disable_codeshield:
        config["enable_codeshield"] = False

    # Configure agentic improvements
    if args.enable_agentic:
        if "system" not in config:
            config["system"] = {}
        config["system"]["enable_agentic_improvements"] = True
        logger.info("Agentic improvements enabled")

    # Initialize the system
    try:
        # Try to import Anthropic library
        import anthropic

        anthropic_available = True
    except ImportError:
        anthropic_available = False
        logger.warning(
            "Anthropic library not available. Using OpenAI as the default provider."
        )
        # Set OpenAI as the provider if Anthropic is not available
        if "llm" not in config:
            config["llm"] = {}
        config["llm"]["provider"] = "openai"

    # Configure mock mode if specified
    if args.mock_mode:
        logger.info("Running in mock mode - no actual API calls will be made")
        if "system" not in config:
            config["system"] = {}
        config["system"]["mock_mode"] = True
        # Set mock provider
        if "llm" not in config:
            config["llm"] = {}
        config["llm"]["provider"] = "mock"

    system = ThreatModelingSystem(config=config)
    await system.initialize()

    try:
        # Start the analysis
        logger.info(
            f"Starting {'lightweight' if args.lightweight else 'complete'} analysis for codebase: {args.codebase}"
        )
        job_id = await system.analyze_codebase(
            args.codebase, lightweight=args.lightweight, verbose=args.verbose
        )

        # Wait for completion
        while True:
            status = await system.get_job_status(job_id)
            if status["status"] in ["complete", "error", "canceled"]:
                break

            # Display progress
            progress = await system.get_analysis_progress(job_id)
            progress_pct = progress.get("progress_percentage", 0)
            current_stage = progress.get("current_stage", "")

            logger.info(f"Progress: {progress_pct}% - {current_stage}")

            # Wait before checking again
            await asyncio.sleep(5)

        # Get results
        if status["status"] == "complete":
            # Get threat model
            threat_model = await system.get_threat_model(job_id)

            # Save threat model to file
            json_path = os.path.join(output_dir, f"threat_model_{job_id}.json")
            with open(json_path, "w") as f:
                import json

                json.dump(threat_model, f, indent=2)

            # Get HTML report
            html_report = await system.get_html_report(job_id)

            # Save HTML report to file
            html_path = os.path.join(output_dir, f"threat_model_{job_id}.html")
            with open(html_path, "w") as f:
                f.write(html_report)

            logger.info(f"Threat model generated successfully. Output saved to:")
            logger.info(f"  - JSON: {json_path}")
            logger.info(f"  - HTML: {html_path}")

            return 0
        else:
            logger.error(f"Analysis failed with status: {status['status']}")
            if "error" in status:
                logger.error(f"Error: {status['error']}")

            return 1
    except Exception as e:
        logger.exception(f"Error during analysis: {e}")
        return 1
    finally:
        # Shutdown the system
        await system.shutdown()
        logger.info("System shutdown complete")


def load_api_key(api_key_file=None):
    """Load OpenAI API key from file or environment variable"""
    # Check environment variable first
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        logger.info("Using API key from environment variable")
        return api_key

    # Check API key file
    if api_key_file and os.path.exists(api_key_file):
        try:
            with open(api_key_file, "r", errors="replace") as f:
                content = f.read().strip()

                # Try to parse as JSON
                try:
                    import json

                    data = json.loads(content)
                    # Look for common key names
                    for key_name in ["api_key", "apiKey", "key", "secret"]:
                        if key_name in data:
                            logger.info(f"✓ API key loaded from {api_key_file}")
                            return data[key_name]
                except json.JSONDecodeError:
                    # Not JSON, assume plain text
                    logger.info(f"✓ API key loaded from {api_key_file}")
                    return content
        except Exception as e:
            logger.warning(f"Error loading API key from {api_key_file}: {e}")

    # Check default locations
    default_locations = [
        os.path.expanduser("~/.openai/api_key.txt"),
        os.path.expanduser("~/.config/openai/api_key.txt"),
        os.path.expanduser("~/.config/threat-modeling/api_key.json"),
    ]

    for location in default_locations:
        if os.path.exists(location):
            return load_api_key(location)

    logger.warning("No OpenAI API key found. Some features will be limited.")
    return None


def main():
    """Main entry point for the CLI"""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description=f"Threat Canvas v{__version__} - Advanced Autonomous Threat Modeling System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("codebase", help="Path to the codebase to analyze")

    parser.add_argument(
        "--output",
        "-o",
        help="Directory to save output files (default: current directory)",
    )

    parser.add_argument(
        "--config", "-c", help="Path to configuration file (JSON or YAML)"
    )

    parser.add_argument(
        "--lightweight",
        "-l",
        action="store_true",
        help="Run in lightweight mode (faster but less comprehensive)",
    )

    parser.add_argument(
        "--api-key-file", "-k", help="Path to file containing OpenAI API key"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument("--log-file", help="Path to log file for detailed logging")

    parser.add_argument(
        "--version", action="version", version=f"Threat Canvas v{__version__}"
    )

    # Advanced options
    advanced_group = parser.add_argument_group("Advanced Options")

    advanced_group.add_argument(
        "--max-commits", type=int, help="Maximum number of commits to analyze"
    )

    advanced_group.add_argument(
        "--max-files",
        type=int,
        help="Maximum number of files to process (default: 10000)",
    )

    advanced_group.add_argument(
        "--model", help="OpenAI model to use (e.g., gpt-4o-mini, gpt-4)"
    )

    # Security tools options
    security_group = parser.add_argument_group("Security Tools Options")

    security_group.add_argument(
        "--enable-redflag", action="store_true", help="Enable RedFlag security analysis"
    )

    security_group.add_argument(
        "--disable-redflag",
        action="store_true",
        help="Disable RedFlag security analysis",
    )

    security_group.add_argument(
        "--enable-codeshield",
        action="store_true",
        help="Enable CodeShield security analysis",
    )

    security_group.add_argument(
        "--disable-codeshield",
        action="store_true",
        help="Disable CodeShield security analysis",
    )

    advanced_group.add_argument(
        "--no-cache", action="store_true", help="Disable caching of API requests"
    )

    advanced_group.add_argument(
        "--enable-agentic",
        action="store_true",
        help="Enable agentic improvements for enhanced agent collaboration and resilience",
    )

    advanced_group.add_argument(
        "--mock-mode",
        action="store_true",
        help="Run in mock mode for testing without API calls",
    )

    advanced_group.add_argument(
        "--export-config", help="Export default configuration to a file and exit"
    )

    # Parse arguments
    args = parser.parse_args()

    # Configure logging - enable verbose by default to help diagnose agent communication issues
    from autothreats.utils.logging_config import configure_logging

    configure_logging(verbose=True, log_file=args.log_file or "threat_modeling.log")

    # Load API key
    args.api_key = load_api_key(args.api_key_file)

    # Handle export config option
    if args.export_config:
        export_default_config(args.export_config)
        logger.info(f"Default configuration exported to {args.export_config}")
        sys.exit(0)

    # Run the threat modeling system
    try:
        exit_code = asyncio.run(run_threat_modeling(args))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Error running threat modeling: {e}")
        sys.exit(1)


def export_default_config(output_file: str):
    """Export default configuration to a file"""
    default_config = {
        "openai": {
            "api_key": "your-api-key-here",
            "default_model": "gpt-4o-mini",
            "cache_enabled": True,
            "cache_ttl": 3600,
            "batch_enabled": True,
            "max_batch_size": 20,
            "max_concurrent_requests": 5,
        },
        "agents": {
            "default": {"enabled": True},
            "commit_history": {"max_commits": 30, "max_recent_commits": 30},
            "code_ingestion": {
                "max_files": 100000,  # Increased from 10000 to handle larger codebases
                "lightweight_max_files": 100000,
                "max_file_size": 61440,  # 60KB
            },
        },
        "system": {
            "enable_agentic_improvements": False,  # Disabled by default, enable with --enable-agentic flag
            "lightweight": False,
        },
        "workspace": {"parallel_operations": 8},
        # Security tools configuration
        "enable_redflag": False,  # Disabled by default, enable with --enable-redflag
        "redflag_config": {"redflag_path": "redflag", "risk_threshold": 7},
        "enable_codeshield": False,  # Disabled by default, enable with --enable-codeshield
        "codeshield_config": {
            "languages": ["python", "javascript", "java", "go", "ruby", "php", "c"],
            "severity_threshold": "medium",
            "block_mode": False,
        },
        "auto_install_security_tools": True,
    }

    try:
        with open(output_file, "w") as f:
            if output_file.endswith(".json"):
                json.dump(default_config, f, indent=2)
            elif output_file.endswith((".yaml", ".yml")):
                try:
                    import yaml

                    yaml.dump(default_config, f, default_flow_style=False)
                except ImportError:
                    logger.error(
                        "YAML support requires PyYAML. Using JSON format instead."
                    )
                    json.dump(default_config, f, indent=2)
            else:
                # Default to JSON
                json.dump(default_config, f, indent=2)
    except Exception as e:
        logger.error(f"Error exporting configuration: {e}")


if __name__ == "__main__":
    main()
