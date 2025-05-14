#!/usr/bin/env python3
"""
Simplified Context-Aware Security module for the autonomous threat modeling system.
Provides context-aware security analysis for the simplified architecture.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import SharedWorkspace
from ..utils.llm_service import LLMService

logger = logging.getLogger(__name__)


class SimplifiedContextAwareSecurity:
    """
    Simplified Context-Aware Security module that enhances threat detection
    by understanding the security context of the codebase.
    """

    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the context-aware security module.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.llm_service = workspace.get_data("llm_service")

        # Initialize cache for context analysis
        self.context_cache = {}

    async def analyze_security_context(
        self, codebase: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Analyze the security context of a codebase.

        Args:
            codebase: The codebase to analyze
            job_id: The ID of the job

        Returns:
            Security context analysis results
        """
        self.logger.info(f"Analyzing security context for job {job_id}")

        # Check cache first
        cache_key = f"security_context_{job_id}"
        cached_result = self.workspace.get_cached_analysis(cache_key)
        if cached_result:
            self.logger.info(f"Using cached security context analysis for job {job_id}")
            return cached_result

        # Extract security-relevant files
        security_files = self._identify_security_files(codebase)

        # Analyze security patterns
        security_patterns = await self._analyze_security_patterns(
            security_files, job_id
        )

        # Identify security boundaries
        security_boundaries = self._identify_security_boundaries(
            codebase, security_patterns
        )

        # Create security context
        security_context = {
            "job_id": job_id,
            "security_files": security_files,
            "security_patterns": security_patterns,
            "security_boundaries": security_boundaries,
            "timestamp": asyncio.get_event_loop().time(),
        }

        # Cache the result
        self.workspace.cache_analysis(cache_key, security_context)

        return security_context

    def _identify_security_files(
        self, codebase: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify security-relevant files in the codebase.

        Args:
            codebase: The codebase to analyze

        Returns:
            List of security-relevant files
        """
        security_files = []

        # Security-relevant file patterns
        security_patterns = [
            "auth",
            "login",
            "password",
            "crypt",
            "hash",
            "security",
            "secure",
            "permission",
            "access",
            "token",
            "jwt",
            "oauth",
            "saml",
            "ldap",
            "cert",
            "tls",
            "ssl",
            "encrypt",
            "decrypt",
            "sign",
            "verify",
            "firewall",
            "waf",
            "csrf",
            "xss",
            "injection",
            "sanitize",
            "validate",
        ]

        # Check each file for security relevance
        for file_path, file_content in codebase.get("files", {}).items():
            # Check if file path contains security-relevant patterns
            path_relevance = any(
                pattern in file_path.lower() for pattern in security_patterns
            )

            # Check if file content contains security-relevant patterns
            content_relevance = False
            if file_content:
                # Only check the first 1000 characters for performance
                sample = file_content[:1000].lower()
                content_relevance = any(
                    pattern in sample for pattern in security_patterns
                )

            # If file is security-relevant, add to list
            if path_relevance or content_relevance:
                security_files.append(
                    {
                        "file_path": file_path,
                        "path_relevance": path_relevance,
                        "content_relevance": content_relevance,
                        "relevance_score": (
                            0.8 if path_relevance and content_relevance else 0.5
                        ),
                    }
                )

        return security_files

    async def _analyze_security_patterns(
        self, security_files: List[Dict[str, Any]], job_id: str
    ) -> Dict[str, Any]:
        """
        Analyze security patterns in the identified security files.

        Args:
            security_files: List of security-relevant files
            job_id: The ID of the job

        Returns:
            Security patterns analysis
        """
        # Initialize patterns
        security_patterns = {
            "authentication": [],
            "authorization": [],
            "encryption": [],
            "input_validation": [],
            "output_encoding": [],
            "session_management": [],
            "error_handling": [],
            "logging": [],
        }

        # If LLM service is available, use it for pattern analysis
        if self.llm_service:
            try:
                # Analyze up to 5 most relevant security files
                top_files = sorted(
                    security_files,
                    key=lambda x: x.get("relevance_score", 0),
                    reverse=True,
                )[:5]

                for file_info in top_files:
                    file_path = file_info.get("file_path")
                    file_content = self.workspace.get_data(
                        f"codebase_files_{job_id}_{file_path}"
                    )

                    if not file_content:
                        continue

                    # Create prompt for security pattern analysis
                    prompt = f"""Analyze the following code file for security patterns:

File path: {file_path}

```
{file_content[:5000]}  # Limit to 5000 characters for LLM context window
```

Identify security patterns in the following categories:
1. Authentication
2. Authorization
3. Encryption
4. Input Validation
5. Output Encoding
6. Session Management
7. Error Handling
8. Logging

For each identified pattern, provide:
- Category
- Description
- Strength (strong, moderate, weak)
- Location (line number or function name)

Return your analysis as a JSON object with categories as keys and arrays of patterns as values.
"""

                    # Get AI response
                    response = await self.llm_service.generate_text_async(
                        prompt=prompt,
                        max_tokens=1000,
                        temperature=0.2,
                    )

                    # Parse response
                    try:
                        import json
                        import re

                        # Extract JSON from response
                        json_match = re.search(r"\{.*\}", response, re.DOTALL)
                        if json_match:
                            patterns = json.loads(json_match.group(0))

                            # Merge patterns
                            for category, items in patterns.items():
                                if category in security_patterns and isinstance(
                                    items, list
                                ):
                                    for item in items:
                                        item["file_path"] = file_path
                                        security_patterns[category].append(item)
                    except Exception as e:
                        self.logger.error(f"Error parsing security patterns: {e}")

            except Exception as e:
                self.logger.error(f"Error analyzing security patterns: {e}")

        return security_patterns

    def _identify_security_boundaries(
        self, codebase: Dict[str, Any], security_patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify security boundaries in the codebase.

        Args:
            codebase: The codebase to analyze
            security_patterns: Security patterns analysis

        Returns:
            List of security boundaries
        """
        boundaries = []

        # Identify potential security boundaries based on patterns
        auth_files = set(
            item.get("file_path")
            for item in security_patterns.get("authentication", [])
        )
        auth_files.update(
            item.get("file_path") for item in security_patterns.get("authorization", [])
        )

        # Add authentication/authorization boundary
        if auth_files:
            boundaries.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": "Authentication/Authorization Boundary",
                    "type": "auth_boundary",
                    "files": list(auth_files),
                    "description": "Boundary between authenticated and unauthenticated parts of the application",
                }
            )

        # Add input validation boundary
        input_files = set(
            item.get("file_path")
            for item in security_patterns.get("input_validation", [])
        )
        if input_files:
            boundaries.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": "Input Validation Boundary",
                    "type": "input_boundary",
                    "files": list(input_files),
                    "description": "Boundary for validating external input",
                }
            )

        # Add encryption boundary
        encryption_files = set(
            item.get("file_path") for item in security_patterns.get("encryption", [])
        )
        if encryption_files:
            boundaries.append(
                {
                    "id": str(uuid.uuid4()),
                    "name": "Encryption Boundary",
                    "type": "encryption_boundary",
                    "files": list(encryption_files),
                    "description": "Boundary for encrypting/decrypting sensitive data",
                }
            )

        return boundaries

    async def enhance_vulnerability_detection(
        self, vulnerabilities: List[Dict[str, Any]], security_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Enhance vulnerability detection using security context.

        Args:
            vulnerabilities: List of detected vulnerabilities
            security_context: Security context analysis

        Returns:
            Enhanced list of vulnerabilities
        """
        enhanced_vulnerabilities = []

        # Security boundaries from context
        boundaries = security_context.get("security_boundaries", [])
        boundary_files = set()
        for boundary in boundaries:
            boundary_files.update(boundary.get("files", []))

        # Enhance each vulnerability with context
        for vuln in vulnerabilities:
            # Create a copy of the vulnerability
            enhanced_vuln = dict(vuln)

            # Check if vulnerability is in a security boundary
            file_path = vuln.get("file_path", "")
            if file_path in boundary_files:
                # Increase confidence for vulnerabilities in security boundaries
                enhanced_vuln["confidence"] = min(
                    1.0, vuln.get("confidence", 0.5) + 0.2
                )
                enhanced_vuln["in_security_boundary"] = True

                # Find which boundaries the vulnerability is in
                vuln_boundaries = []
                for boundary in boundaries:
                    if file_path in boundary.get("files", []):
                        vuln_boundaries.append(boundary.get("name"))

                enhanced_vuln["security_boundaries"] = vuln_boundaries
            else:
                enhanced_vuln["in_security_boundary"] = False

            # Add to enhanced list
            enhanced_vulnerabilities.append(enhanced_vuln)

        return enhanced_vulnerabilities
