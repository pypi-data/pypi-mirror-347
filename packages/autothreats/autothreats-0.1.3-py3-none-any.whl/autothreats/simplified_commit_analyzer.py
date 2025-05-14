#!/usr/bin/env python3
"""
Simplified commit history analyzer for the autonomous threat modeling system.
Analyzes git commits to identify security-related changes and generate threat scenarios.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SimplifiedCommitAnalyzer:
    """Analyzes git commit history to identify security-related changes"""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the commit analyzer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger("SimplifiedCommitAnalyzer")

        # Initialize security patterns from config or defaults
        self.security_keywords = self.config.get(
            "security_keywords",
            [
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
        )

        self.suspicious_patterns = self.config.get(
            "suspicious_patterns",
            [
                # Hardcoded credentials
                r"(?:password|passwd|pwd|secret|token|api_key)s?\s*[:=]\s*[\'\"][^\'\"]+[\'\"]",
                # Disabling security features
                r"disable[_\s]*(ssl|security|cert|verification|check)",
                # Setting insecure flags
                r"(verify|secure|check|strict)\s*[:=]\s*(false|0|no|none)",
                # Potential backdoors
                r"backdoor|bypass|exploit|hack",
            ],
        )

        # Initialize LLM service if available
        self.llm_service = None
        if "llm_service" in self.config:
            self.llm_service = self.config["llm_service"]

    async def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Analyze the git commit history of a repository

        Args:
            repo_path: Path to the git repository

        Returns:
            Dictionary with commit history analysis results
        """
        self.logger.info(f"Analyzing commit history for repository: {repo_path}")

        # Check if the path is a git repository
        if not os.path.exists(os.path.join(repo_path, ".git")):
            self.logger.warning(f"Path is not a git repository: {repo_path}")
            return {
                "status": "skipped",
                "message": f"Path is not a git repository: {repo_path}",
                "commit_history": [],
                "security_commits": [],
                "threat_scenarios": [],
            }

        # Get commit history
        commits = await self._get_commits(repo_path)
        self.logger.info(f"Found {len(commits)} commits in repository")

        # Identify security-related commits
        security_commits = []
        for commit in commits:
            is_security_related = await self._is_security_related_commit(
                repo_path, commit
            )
            if is_security_related:
                security_commits.append(commit)

        self.logger.info(f"Identified {len(security_commits)} security-related commits")

        # Generate threat scenarios from security commits
        threat_scenarios = await self._generate_threat_scenarios(
            repo_path, security_commits
        )

        return {
            "status": "success",
            "message": f"Analyzed {len(commits)} commits, found {len(security_commits)} security-related commits",
            "commit_history": commits,
            "security_commits": security_commits,
            "threat_scenarios": threat_scenarios,
        }

    async def _get_commits(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get the git commit history"""
        commits = []

        try:
            # Use configured max_commits limit
            max_commits = self.config.get("max_commits", 30)
            git_log_cmd = [
                "git",
                "-C",
                repo_path,
                "log",
                "--pretty=format:%H||%an||%ae||%at||%s",
                f"--max-count={max_commits}",
            ]

            proc = await asyncio.create_subprocess_exec(
                *git_log_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                self.logger.error(
                    f"Git log command failed: {stderr.decode('utf-8', errors='replace')}"
                )
                return []

            # Parse commit log
            for line in stdout.decode("utf-8", errors="replace").splitlines():
                parts = line.split("||")
                if len(parts) == 5:
                    commit_hash, author_name, author_email, timestamp, subject = parts

                    # Convert timestamp to datetime
                    commit_time = datetime.fromtimestamp(int(timestamp))

                    commits.append(
                        {
                            "hash": commit_hash,
                            "author": {"name": author_name, "email": author_email},
                            "timestamp": int(timestamp),
                            "date": commit_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "subject": subject,
                            "is_security_related": False,
                        }
                    )

            # Enrich with stats for recent commits
            max_recent = self.config.get("max_recent_commits", 10)
            recent_commits = commits[:max_recent]

            # Process recent commits in parallel for better performance
            tasks = []
            for commit in recent_commits:
                tasks.append(self._add_commit_stats(repo_path, commit))

            await asyncio.gather(*tasks)

            return commits

        except Exception as e:
            self.logger.error(f"Error getting commit history: {str(e)}")
            return []

    async def _add_commit_stats(self, repo_path: str, commit: Dict[str, Any]):
        """Add file stats to a commit"""
        try:
            # Get stats for the commit
            git_show_cmd = [
                "git",
                "-C",
                repo_path,
                "show",
                "--stat",
                "--format=",
                commit["hash"],
            ]

            proc = await asyncio.create_subprocess_exec(
                *git_show_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                return

            # Parse stats output
            stats_output = stdout.decode("utf-8", errors="replace")

            # Extract files changed
            files_changed = []
            for line in stats_output.splitlines():
                if "|" in line and "+" in line and "-" in line:
                    file_name = line.split("|")[0].strip()
                    files_changed.append(file_name)

            # Count insertions and deletions
            summary_line = (
                stats_output.splitlines()[-1] if stats_output.splitlines() else ""
            )
            insertions = 0
            deletions = 0

            if "insertion" in summary_line:
                insertions_match = re.search(r"(\d+) insertion", summary_line)
                if insertions_match:
                    insertions = int(insertions_match.group(1))

            if "deletion" in summary_line:
                deletions_match = re.search(r"(\d+) deletion", summary_line)
                if deletions_match:
                    deletions = int(deletions_match.group(1))

            # Add stats to commit
            commit["stats"] = {
                "files_changed": files_changed,
                "files_count": len(files_changed),
                "insertions": insertions,
                "deletions": deletions,
            }

        except Exception as e:
            self.logger.error(f"Error adding commit stats: {str(e)}")

    async def _is_security_related_commit(
        self, repo_path: str, commit: Dict[str, Any]
    ) -> bool:
        """Determine if a commit is security-related"""
        # Check commit message for security keywords
        commit_msg = commit["subject"].lower()
        if any(keyword in commit_msg for keyword in self.security_keywords):
            commit["is_security_related"] = True
            commit["security_indicators"] = ["security-related commit message"]
            return True

        # Check modified files and their content
        try:
            # Get commit diff
            git_show_cmd = ["git", "-C", repo_path, "show", commit["hash"]]

            proc = await asyncio.create_subprocess_exec(
                *git_show_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                return False

            # Use errors='replace' to handle non-UTF-8 characters
            diff_output = stdout.decode("utf-8", errors="replace")

            # Look for suspicious patterns in the diff
            indicators = []
            for pattern in self.suspicious_patterns:
                if re.search(pattern, diff_output, re.IGNORECASE):
                    indicators.append(f"suspicious pattern: {pattern}")

            # Check for sensitive file modifications
            sensitive_files = [
                "password",
                "secret",
                "credential",
                "certificate",
                "key",
                "auth",
                "oauth",
                "security",
                "firebase",
                "aws",
                "gcp",
                "azure",
            ]

            for file in commit.get("stats", {}).get("files_changed", []):
                file_lower = file.lower()
                if any(sensitive in file_lower for sensitive in sensitive_files):
                    indicators.append(f"sensitive file modified: {file}")

            if indicators:
                commit["is_security_related"] = True
                commit["security_indicators"] = indicators
                commit["diff"] = diff_output[:2000]  # Store truncated diff for analysis
                return True

            return False

        except Exception as e:
            self.logger.error(f"Error checking if commit is security-related: {str(e)}")
            return False

    async def _generate_threat_scenarios(
        self, repo_path: str, security_commits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate threat scenarios from security-related commits"""
        threat_scenarios = []

        # Group commits by security type
        security_types = {}

        for commit in security_commits:
            # Determine security type from commit
            security_type = await self._determine_security_type(commit)

            if security_type not in security_types:
                security_types[security_type] = []

            security_types[security_type].append(commit)

        # Generate a threat scenario for each security type
        for security_type, commits in security_types.items():
            # Skip unknown security types with few commits
            if security_type == "unknown" and len(commits) < 2:
                continue

            # Create a threat scenario
            threat_id = f"threat-{len(threat_scenarios) + 1}"

            # Generate threat details based on security type
            threat_details = self._get_threat_details_for_type(security_type)

            # Customize threat details based on commits
            threat_details = await self._customize_threat_details(
                threat_details, commits, repo_path
            )

            # Create the threat scenario
            threat_scenario = {
                "id": threat_id,
                "name": threat_details["name"],
                "description": threat_details["description"],
                "attacker_profile": threat_details["attacker_profile"],
                "attack_vector": threat_details["attack_vector"],
                "impact": threat_details["impact"],
                "likelihood": threat_details["likelihood"],
                "affected_components": self._extract_affected_components(commits),
                "related_commits": [commit["hash"] for commit in commits],
                "security_type": security_type,
            }

            threat_scenarios.append(threat_scenario)

        # If we have LLM service, enhance threat scenarios
        if self.llm_service and threat_scenarios:
            try:
                enhanced_scenarios = await self._enhance_threat_scenarios_with_llm(
                    threat_scenarios, security_commits
                )
                threat_scenarios = enhanced_scenarios
            except Exception as e:
                self.logger.error(
                    f"Error enhancing threat scenarios with LLM: {str(e)}"
                )

        return threat_scenarios

    async def _determine_security_type(self, commit: Dict[str, Any]) -> str:
        """Determine the security type of a commit"""
        # Check commit message and diff for security type indicators
        commit_text = commit["subject"].lower()
        diff_text = commit.get("diff", "").lower()

        combined_text = commit_text + " " + diff_text

        # Check for authentication issues
        if re.search(r"authentica|login|password|credential", combined_text):
            return "authentication"

        # Check for authorization issues
        elif re.search(r"authoriz|permission|access|role", combined_text):
            return "authorization"

        # Check for XSS
        elif re.search(r"xss|cross.?site", combined_text):
            return "cross-site-scripting"

        # Check for injection
        elif re.search(r"inject|sql", combined_text):
            return "injection"

        # Check for CSRF
        elif re.search(r"csrf|cross.?site.?request", combined_text):
            return "csrf"

        # Check for cryptography
        elif re.search(r"encrypt|decrypt|hash|md5|sha|crypt", combined_text):
            return "cryptography"

        # Check for transport security
        elif re.search(r"ssl|tls|https|certificate", combined_text):
            return "transport-security"

        # Default to unknown
        return "unknown"

    def _get_threat_details_for_type(self, security_type: str) -> Dict[str, Any]:
        """Get threat details template for a security type"""
        # Default threat details
        default_threat = {
            "name": "Generic Security Vulnerability",
            "description": "A security vulnerability that could potentially be exploited by attackers",
            "attacker_profile": "External attacker with moderate skills",
            "attack_vector": "Exploitation of security vulnerability",
            "impact": "Unauthorized access to system resources",
            "likelihood": 0.5,
        }

        # Security type specific threat details
        threat_details = {
            "authentication": {
                "name": "Authentication Bypass",
                "description": "Attacker bypasses authentication to gain unauthorized access",
                "attacker_profile": "External attacker with moderate skills",
                "attack_vector": "Exploitation of authentication vulnerability",
                "impact": "Unauthorized access to user accounts and sensitive data",
                "likelihood": 0.7,
            },
            "authorization": {
                "name": "Authorization Bypass",
                "description": "Attacker bypasses authorization controls to access restricted resources",
                "attacker_profile": "Authenticated user with malicious intent",
                "attack_vector": "Exploitation of authorization vulnerability",
                "impact": "Unauthorized access to restricted resources and data",
                "likelihood": 0.6,
            },
            "cross-site-scripting": {
                "name": "Cross-Site Scripting (XSS) Attack",
                "description": "Attacker injects malicious scripts into web pages viewed by users",
                "attacker_profile": "External attacker with web exploitation skills",
                "attack_vector": "Injection of malicious scripts into web pages",
                "impact": "Theft of user credentials, session hijacking, or malware distribution",
                "likelihood": 0.8,
            },
            "injection": {
                "name": "Injection Attack",
                "description": "Attacker injects malicious code or commands into application inputs",
                "attacker_profile": "External attacker with moderate technical skills",
                "attack_vector": "Injection of malicious input into application",
                "impact": "Unauthorized data access, data corruption, or remote code execution",
                "likelihood": 0.7,
            },
            "csrf": {
                "name": "Cross-Site Request Forgery (CSRF)",
                "description": "Attacker tricks users into performing unwanted actions on authenticated applications",
                "attacker_profile": "External attacker with web exploitation skills",
                "attack_vector": "Social engineering and exploitation of CSRF vulnerability",
                "impact": "Unauthorized actions performed on behalf of authenticated users",
                "likelihood": 0.6,
            },
            "cryptography": {
                "name": "Cryptographic Vulnerability",
                "description": "Attacker exploits weaknesses in cryptographic implementation",
                "attacker_profile": "Sophisticated attacker with cryptographic knowledge",
                "attack_vector": "Exploitation of cryptographic weaknesses",
                "impact": "Exposure of sensitive data or bypass of security controls",
                "likelihood": 0.5,
            },
            "transport-security": {
                "name": "Transport Layer Security Vulnerability",
                "description": "Attacker exploits weaknesses in transport layer security",
                "attacker_profile": "Network attacker with moderate skills",
                "attack_vector": "Man-in-the-middle attack or exploitation of TLS vulnerability",
                "impact": "Interception of sensitive data or session hijacking",
                "likelihood": 0.6,
            },
        }

        return threat_details.get(security_type, default_threat)

    async def _customize_threat_details(
        self,
        threat_details: Dict[str, Any],
        commits: List[Dict[str, Any]],
        repo_path: str,
    ) -> Dict[str, Any]:
        """Customize threat details based on commits"""
        # Create a copy of the threat details to customize
        custom_details = threat_details.copy()

        # Extract file types from commits to determine affected components
        file_extensions = set()
        for commit in commits:
            for file in commit.get("stats", {}).get("files_changed", []):
                _, ext = os.path.splitext(file)
                if ext:
                    file_extensions.add(ext.lower())

        # Customize description based on file types
        if (
            ".js" in file_extensions
            or ".jsx" in file_extensions
            or ".ts" in file_extensions
        ):
            custom_details["description"] += " in the frontend JavaScript code"
        elif ".py" in file_extensions:
            custom_details["description"] += " in the backend Python code"
        elif ".java" in file_extensions:
            custom_details["description"] += " in the Java application code"
        elif ".php" in file_extensions:
            custom_details["description"] += " in the PHP application code"

        # Adjust likelihood based on commit recency
        recent_commits = [
            c
            for c in commits
            if c.get("timestamp", 0) > (datetime.now().timestamp() - 30 * 24 * 60 * 60)
        ]
        if recent_commits:
            # Increase likelihood for recent security issues
            custom_details["likelihood"] = min(0.9, custom_details["likelihood"] + 0.2)

        return custom_details

    def _extract_affected_components(self, commits: List[Dict[str, Any]]) -> List[str]:
        """Extract affected components from commits"""
        components = set()

        # Extract components from file paths
        for commit in commits:
            for file in commit.get("stats", {}).get("files_changed", []):
                # Try to determine component from file path
                parts = file.split("/")
                if len(parts) > 1:
                    # Use first directory as component
                    component = parts[0].capitalize()
                    components.add(component)
                else:
                    # Use file extension as component type
                    _, ext = os.path.splitext(file)
                    if ext:
                        component_type = ext[1:].upper()  # Remove dot and capitalize
                        components.add(f"{component_type} Component")

        # If no components found, use generic component
        if not components:
            components.add("Unknown Component")

        return list(components)

    async def _enhance_threat_scenarios_with_llm(
        self,
        threat_scenarios: List[Dict[str, Any]],
        security_commits: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Enhance threat scenarios with LLM insights"""
        if not self.llm_service:
            return threat_scenarios

        enhanced_scenarios = []

        for scenario in threat_scenarios:
            # Get related commits for this scenario
            related_commits = [
                c for c in security_commits if c["hash"] in scenario["related_commits"]
            ]

            # Prepare commit information for LLM
            commit_info = []
            for commit in related_commits[
                :3
            ]:  # Limit to 3 commits to avoid token limits
                commit_info.append(
                    {
                        "hash": commit["hash"][:8],
                        "subject": commit["subject"],
                        "date": commit["date"],
                        "indicators": commit.get("security_indicators", []),
                        "files_changed": commit.get("stats", {}).get(
                            "files_changed", []
                        )[
                            :5
                        ],  # Limit files
                    }
                )

            # Create prompt for LLM
            prompt = f"""
            Analyze the following security-related git commits and enhance the threat scenario:
            
            Threat Scenario:
            - Name: {scenario["name"]}
            - Description: {scenario["description"]}
            - Security Type: {scenario["security_type"]}
            - Affected Components: {", ".join(scenario["affected_components"])}
            
            Related Commits:
            {json.dumps(commit_info, indent=2)}
            
            Please provide a more detailed and specific threat scenario based on these commits.
            Include specific attack vectors, potential impact, and realistic attacker profile.
            
            Respond in JSON format with the following fields:
            {{
              "name": "Enhanced threat name",
              "description": "Detailed threat description",
              "attacker_profile": "Specific attacker profile",
              "attack_vector": "Specific attack vector",
              "impact": "Detailed impact description",
              "likelihood": Likelihood as float between 0 and 1
            }}
            """

            try:
                # Call LLM service
                response = await self.llm_service.generate_text(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.3,
                )

                # Parse JSON response
                json_match = re.search(r"{.*}", response, re.DOTALL)
                if json_match:
                    enhanced = json.loads(json_match.group(0))

                    # Update scenario with enhanced details
                    scenario.update(enhanced)

                enhanced_scenarios.append(scenario)

            except Exception as e:
                self.logger.error(f"Error enhancing threat scenario with LLM: {str(e)}")
                enhanced_scenarios.append(scenario)

        return enhanced_scenarios
