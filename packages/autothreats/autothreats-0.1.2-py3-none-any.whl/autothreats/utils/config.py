#!/usr/bin/env python3
"""
Configuration utilities for the autonomous threat modeling system.
Provides functionality to load, save, and generate configuration files in YAML format.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Union

import yaml

logger = logging.getLogger(__name__)

# Default configuration locations
DEFAULT_CONFIG_LOCATIONS = [
    "./threat-canvas.yaml",
    "./threat-canvas.yml",
    "~/.config/threat-canvas/config.yaml",
    "~/.threat-canvas/config.yaml",
]

# Default configuration template
DEFAULT_CONFIG = {
    "project_name": "Threat Canvas Project",
    "system": {
        "output_dir": "./output",
        "parallel_operations": 8,
        "lightweight": False,
        "enable_agentic_improvements": True,
    },
    "openai": {
        "api_key": "",  # Will be populated from environment or key file
        "default_model": "gpt-4o-mini",
        "cache_enabled": True,
        "cache_ttl": 3600,  # 1 hour
        "batch_enabled": True,
        "batch_window": 0.1,  # 100ms
        "max_batch_size": 20,
        "max_concurrent_requests": 5,
        "batch_size": 5,
        "batch_delay": 1,
    },
    "anthropic": {
        "api_key": "",  # Will be populated from environment or key file
        "default_model": "claude-3-sonnet-20240229",
        "cache_enabled": True,
        "cache_ttl": 3600,  # 1 hour
    },
    "agents": {
        # Default configuration for all agents
        "default": {
            "enabled": True,
        },
        # Agent-specific configurations
        "commit_history": {
            "enabled": True,
            "security_keywords": [
                "password",
                "token",
                "api_key",
                "secret",
                "private_key",
                "credential",
                "auth",
                "authenticate",
                "oauth",
                "certificate",
                "ssl",
                "https",
                "encrypt",
                "decrypt",
                "hash",
                "md5",
                "sha",
                "crypt",
                "salt",
                "vulnerability",
                "exploit",
                "attack",
                "xss",
                "injection",
                "csrf",
                "security",
                "secure",
                "insecure",
                "threat",
                "risk",
                "sensitive",
                "permission",
                "access",
                "authorization",
                "role",
                "privilege",
                "firewall",
                "backdoor",
                "bypass",
                "breach",
                "mitigation",
                "fix security",
                "security issue",
                "security bug",
                "cve",
                "vuln",
            ],
        },
        "code_ingestion": {
            "enabled": True,
            "max_files": 100000,  # Increased from 5000 to handle larger codebases
            "max_file_size": 60 * 1024,  # 60KB
            "ignored_patterns": [
                ".git",
                ".svn",
                ".hg",
                ".vscode",
                ".idea",
                "node_modules",
                "venv",
                "env",
                ".env",
                "__pycache__",
                ".pytest_cache",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                "*.so",
                "*.o",
                "*.a",
                "*.dll",
                "*.exe",
                "*.zip",
                "*.tar",
                "*.gz",
                "*.rar",
                "*.7z",
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.gif",
                "*.pdf",
                "*.doc",
                "*.docx",
                "*.mp3",
                "*.mp4",
                "*.avi",
            ],
        },
        # Add configurations for other agents as needed
    },
    "workspace": {
        "parallel_operations": 8,
    },
    "llm": {
        "provider": "openai",  # Default LLM provider
        "fallback_providers": [
            "anthropic"
        ],  # Fallback providers in order of preference
    },
}


def load_config(config_path: Optional[str] = None) -> Mapping[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file. If None, will search in default locations.

    Returns:
        Loaded configuration as a dictionary
    """
    # If config_path is provided, try to load it
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, "r", errors="replace") as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.warning(f"Error loading configuration from {config_path}: {e}")
            logger.warning("Falling back to default configuration")
            return DEFAULT_CONFIG.copy()

    # Otherwise, search in default locations
    for location in DEFAULT_CONFIG_LOCATIONS:
        expanded_path = os.path.expanduser(location)
        if os.path.exists(expanded_path):
            try:
                with open(expanded_path, "r", errors="replace") as f:
                    config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {expanded_path}")
                return config
            except Exception as e:
                logger.warning(f"Error loading configuration from {expanded_path}: {e}")
                continue

    # If no configuration file is found, return default configuration
    logger.info("No configuration file found, using default configuration")
    return DEFAULT_CONFIG.copy()


def save_config(config: Mapping[str, Any], config_path: str) -> bool:
    """
    Save configuration to a YAML file.

    Args:
        config: Configuration dictionary
        config_path: Path to save the configuration file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)

        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration to {config_path}: {e}")
        return False


def generate_config(
    output_path: str,
    template: Optional[Mapping[str, Any]] = None,
    project_name: Optional[str] = None,
    output_dir: Optional[str] = None,
    llm_provider: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    mock_mode: bool = False,
) -> bool:
    """
    Generate a configuration file with default values.

    Args:
        output_path: Path to save the configuration file
        template: Optional template to use instead of the default
        project_name: Optional project name
        output_dir: Optional output directory
        llm_provider: Optional LLM provider
        openai_api_key: Optional OpenAI API key
        mock_mode: Whether to enable mock mode

    Returns:
        True if successful, False otherwise
    """
    config = template or DEFAULT_CONFIG.copy()

    # Add project name if provided
    if project_name:
        config["project_name"] = project_name

    # Update output directory if provided
    if output_dir:
        if "system" not in config:
            config["system"] = {}
        config["system"]["output_dir"] = output_dir

    # Update LLM provider if provided
    if llm_provider:
        if "llm" not in config:
            config["llm"] = {}
        config["llm"]["provider"] = llm_provider

    # Add OpenAI API key if provided
    if openai_api_key:
        if "openai" not in config:
            config["openai"] = {}
        config["openai"]["api_key"] = openai_api_key
    else:
        # Try to get API keys from environment
        env_openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        if env_openai_api_key:
            config["openai"]["api_key"] = env_openai_api_key

    # Try to get Anthropic API key from environment
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_api_key:
        config["anthropic"]["api_key"] = anthropic_api_key

    # Enable mock mode if requested
    if mock_mode:
        config["mock_mode"] = True
        if "llm" not in config:
            config["llm"] = {}
        config["llm"]["provider"] = "mock"

    return save_config(config, output_path)


def merge_configs(
    base_config: Mapping[str, Any], override_config: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Merge two configuration dictionaries, with override_config taking precedence.

    Args:
        base_config: Base configuration
        override_config: Configuration to override base with

    Returns:
        Merged configuration
    """

    # Helper function for deep merge
    def deep_merge(
        source: Mapping[str, Any], destination: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        for key, value in source.items():
            if (
                key in destination
                and isinstance(destination[key], dict)
                and isinstance(value, dict)
            ):
                deep_merge(value, destination[key])
            else:
                destination[key] = value
        return destination

    # Create a copy of base config
    merged_config: Mapping[str, Any] = {}
    deep_merge(base_config, merged_config)

    # Merge with override config
    deep_merge(override_config, merged_config)

    return merged_config


def get_config_with_cli_overrides(
    config: Mapping[str, Any], cli_args: Mapping[str, Any]
) -> Mapping[str, Any]:
    """
    Override configuration with command-line arguments.

    Args:
        config: Base configuration
        cli_args: Command-line arguments

    Returns:
        Configuration with CLI overrides applied
    """
    # Create a copy of the config
    result_config = config.copy()

    # Apply CLI overrides
    if cli_args.get("output"):
        result_config["system"] = result_config.get("system", {})
        result_config["system"]["output_dir"] = cli_args["output"]

    if cli_args.get("lightweight") is not None:
        result_config["system"] = result_config.get("system", {})
        result_config["system"]["lightweight"] = cli_args["lightweight"]

    # Add API key if provided
    if cli_args.get("api_key"):
        # Add to top-level config for easier access
        result_config["api_key"] = cli_args["api_key"]

        # Add to openai section for backward compatibility
        result_config["openai"] = result_config.get("openai", {})
        result_config["openai"]["api_key"] = cli_args["api_key"]

        # Add to llm section for consistency
        result_config["llm"] = result_config.get("llm", {})
        result_config["llm"]["api_key"] = cli_args["api_key"]

        logger.info("API key added to configuration")

    # Handle RedFlag options
    if cli_args.get("enable_redflag"):
        result_config["enable_redflag"] = True
    elif cli_args.get("disable_redflag"):
        result_config["enable_redflag"] = False

    # Handle CodeShield options
    if cli_args.get("enable_codeshield"):
        result_config["enable_codeshield"] = True
    elif cli_args.get("disable_codeshield"):
        result_config["enable_codeshield"] = False

    # Handle Agentic Improvements options
    if cli_args.get("enable_agentic"):
        result_config["system"] = result_config.get("system", {})
        result_config["system"]["enable_agentic_improvements"] = True
    elif cli_args.get("disable_agentic"):
        result_config["system"] = result_config.get("system", {})
        result_config["system"]["enable_agentic_improvements"] = False

    return result_config


def validate_config(config: Mapping[str, Any]) -> List[str]:
    """
    Validate configuration and return a list of validation errors.

    Args:
        config: Configuration to validate

    Returns:
        List of validation error messages, empty if valid
    """
    errors = []

    # Check for required sections
    required_sections = ["system", "agents", "workspace"]
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required configuration section: {section}")

    # Check for LLM provider configuration
    llm_config = config.get("llm", {})
    provider = llm_config.get("provider")

    if provider:
        if provider not in ["openai", "anthropic"]:
            errors.append(f"Unsupported LLM provider: {provider}")

        # Check if the provider configuration exists
        if provider not in config:
            errors.append(f"Missing configuration for LLM provider: {provider}")

    return errors
