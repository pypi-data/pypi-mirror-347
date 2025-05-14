#!/usr/bin/env python3
"""
Service for integrating with RedFlag security analysis tool.
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RedFlagService:
    """
    Service for integrating with RedFlag security analysis tool.
    """

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the RedFlag service.

        Args:
            api_key: Optional API key for RedFlag
            config: Optional configuration for RedFlag
        """
        self.api_key = api_key
        self.config = config or {}
        self.logger = logging.getLogger("RedFlagService")
        self.initialized = False

        # Try to import RedFlag
        try:
            import redflag

            self.redflag = redflag
            self.initialized = True
            self.logger.info("RedFlag service initialized successfully")
        except ImportError:
            self.logger.warning("RedFlag not installed, service will be limited")
            self.redflag = None

    def is_available(self) -> bool:
        """
        Check if RedFlag is available.

        Returns:
            bool: True if RedFlag is available, False otherwise
        """
        return self.initialized and self.redflag is not None

    async def analyze_codebase(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze a codebase using RedFlag.

        Args:
            codebase: Codebase dictionary with files

        Returns:
            List of vulnerabilities found
        """
        if not self.is_available():
            self.logger.warning("RedFlag not available, skipping analysis")
            return []

        try:
            self.logger.info("Starting RedFlag analysis")

            # Extract files from codebase
            files = codebase.get("files", {})

            # Create temporary directory for analysis
            import os
            import tempfile

            with tempfile.TemporaryDirectory() as temp_dir:
                # Write files to temporary directory
                for file_path, content in files.items():
                    # Create directory structure
                    full_path = os.path.join(temp_dir, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)

                    # Write file
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)

                # Run RedFlag analysis
                self.logger.info(f"Running RedFlag analysis on {len(files)} files")
                results = self.redflag.analyze_directory(temp_dir)

                # Convert results to standard format
                vulnerabilities = self._convert_results(results)

                self.logger.info(
                    f"RedFlag analysis complete, found {len(vulnerabilities)} vulnerabilities"
                )
                return vulnerabilities

        except Exception as e:
            self.logger.error(f"Error during RedFlag analysis: {e}")
            return []

    def _convert_results(self, results: Any) -> List[Dict[str, Any]]:
        """
        Convert RedFlag results to standard vulnerability format.

        Args:
            results: RedFlag analysis results

        Returns:
            List of vulnerabilities in standard format
        """
        vulnerabilities = []

        try:
            # Process results based on RedFlag's output format
            # This is a placeholder implementation since we don't have the actual RedFlag API
            for result in results:
                vulnerability = {
                    "vulnerability_type": result.get("type", "Unknown"),
                    "severity": result.get("severity", "Medium"),
                    "file_path": result.get("file", "Unknown"),
                    "line_numbers": result.get("lines", [0]),
                    "description": result.get("description", "No description provided"),
                    "remediation": result.get("remediation", "No remediation provided"),
                    "cwe_id": result.get("cwe", "Unknown"),
                    "confidence": result.get("confidence", 0.5),
                    "source": "RedFlag",
                }
                vulnerabilities.append(vulnerability)
        except Exception as e:
            self.logger.error(f"Error converting RedFlag results: {e}")

        return vulnerabilities
