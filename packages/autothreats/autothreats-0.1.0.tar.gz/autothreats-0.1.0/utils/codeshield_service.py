#!/usr/bin/env python3
"""
Service for integrating with CodeShield security analysis tool.
"""

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class CodeShieldService:
    """
    Service for integrating with CodeShield security analysis tool.
    """

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the CodeShield service.
        
        Args:
            api_key: Optional API key for CodeShield
            config: Optional configuration for CodeShield
        """
        self.api_key = api_key
        self.config = config or {}
        self.logger = logging.getLogger("CodeShieldService")
        self.initialized = False
        
        # Try to import CodeShield
        try:
            import codeshield
            self.codeshield = codeshield
            self.initialized = True
            self.logger.info("CodeShield service initialized successfully")
        except ImportError:
            self.logger.warning("CodeShield not installed, service will be limited")
            self.codeshield = None
            
    def is_available(self) -> bool:
        """
        Check if CodeShield is available.
        
        Returns:
            bool: True if CodeShield is available, False otherwise
        """
        return self.initialized and self.codeshield is not None
        
    async def analyze_codebase(self, codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze a codebase using CodeShield.
        
        Args:
            codebase: Codebase dictionary with files
            
        Returns:
            List of vulnerabilities found
        """
        if not self.is_available():
            self.logger.warning("CodeShield not available, skipping analysis")
            return []
            
        try:
            self.logger.info("Starting CodeShield analysis")
            
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
                
                # Run CodeShield analysis
                self.logger.info(f"Running CodeShield analysis on {len(files)} files")
                
                # Configure CodeShield with API key if available
                if self.api_key:
                    self.codeshield.configure(api_key=self.api_key)
                
                # Run analysis
                results = self.codeshield.scan_directory(temp_dir)
                
                # Convert results to standard format
                vulnerabilities = self._convert_results(results)
                
                self.logger.info(f"CodeShield analysis complete, found {len(vulnerabilities)} vulnerabilities")
                return vulnerabilities
                
        except Exception as e:
            self.logger.error(f"Error during CodeShield analysis: {e}")
            return []
            
    def _convert_results(self, results: Any) -> List[Dict[str, Any]]:
        """
        Convert CodeShield results to standard vulnerability format.
        
        Args:
            results: CodeShield analysis results
            
        Returns:
            List of vulnerabilities in standard format
        """
        vulnerabilities = []
        
        try:
            # Process results based on CodeShield's output format
            # This is a placeholder implementation since we don't have the actual CodeShield API
            for result in results:
                # Map CodeShield severity to standard severity
                severity_map = {
                    "critical": "Critical",
                    "high": "High",
                    "medium": "Medium",
                    "low": "Low",
                    "info": "Low",
                }
                
                severity = severity_map.get(result.get("severity", "").lower(), "Medium")
                
                vulnerability = {
                    "vulnerability_type": result.get("type", "Unknown"),
                    "severity": severity,
                    "file_path": result.get("file_path", "Unknown"),
                    "line_numbers": result.get("line_numbers", [0]),
                    "description": result.get("description", "No description provided"),
                    "remediation": result.get("remediation", "No remediation provided"),
                    "cwe_id": result.get("cwe_id", "Unknown"),
                    "confidence": result.get("confidence", 0.5),
                    "source": "CodeShield",
                }
                vulnerabilities.append(vulnerability)
        except Exception as e:
            self.logger.error(f"Error converting CodeShield results: {e}")
            
        return vulnerabilities
