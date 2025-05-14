#!/usr/bin/env python3
"""
Adaptive Agent Prioritization module for the autonomous threat modeling system.
Dynamically adjusts agent priorities based on security context.
"""

import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AdaptiveAgentPrioritizer:
    """
    Dynamically prioritizes agents based on the security context of the codebase.
    Analyzes the codebase to determine which security aspects are most relevant,
    then assigns priorities to agents based on their specialties.
    """

    def __init__(self, workspace):
        """
        Initialize the prioritizer with a workspace reference.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.agent_priorities = {}
        self.context_weights = {
            "crypto": [
                "crypto",
                "encryption",
                "hash",
                "signature",
                "key",
                "certificate",
                "tls",
                "ssl",
            ],
            "auth": [
                "authentication",
                "authorization",
                "login",
                "session",
                "token",
                "password",
                "credential",
            ],
            "input": [
                "validation",
                "sanitization",
                "parsing",
                "injection",
                "xss",
                "csrf",
                "sql",
                "command",
            ],
            "memory": [
                "buffer",
                "allocation",
                "pointer",
                "free",
                "overflow",
                "leak",
                "race",
                "null",
            ],
            "network": [
                "socket",
                "http",
                "request",
                "response",
                "api",
                "endpoint",
                "protocol",
                "packet",
            ],
            "filesystem": [
                "file",
                "path",
                "directory",
                "upload",
                "download",
                "read",
                "write",
                "permission",
            ],
        }
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def analyze_codebase_context(self, codebase_model) -> Dict[str, float]:
        """
        Analyze codebase to determine security context weights.

        Args:
            codebase_model: The codebase model containing files and metadata

        Returns:
            Dictionary mapping context types to normalized scores
        """
        self.logger.info("Analyzing codebase for security context")
        context_scores = {ctx: 0 for ctx in self.context_weights}

        # Count occurrences of context keywords in files
        for file_path, file_content in codebase_model.files.items():
            file_path_lower = file_path.lower()
            file_content_lower = (
                file_content.lower() if isinstance(file_content, str) else ""
            )

            for context, keywords in self.context_weights.items():
                for keyword in keywords:
                    if keyword in file_path_lower:
                        context_scores[
                            context
                        ] += 2  # Higher weight for keywords in file paths
                    if keyword in file_content_lower:
                        context_scores[context] += 1

        # Normalize scores
        total = sum(context_scores.values()) or 1
        normalized_scores = {
            ctx: score / total for ctx, score in context_scores.items()
        }

        self.logger.info(f"Security context analysis complete: {normalized_scores}")
        return normalized_scores

    def prioritize_agents(self, context_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Assign priorities to agents based on security context.

        Args:
            context_scores: Dictionary mapping context types to normalized scores

        Returns:
            Dictionary mapping agent IDs to priority scores
        """
        self.logger.info("Prioritizing agents based on security context")

        # Map agents to contexts they handle best
        agent_contexts = {
            "threat_detection": ["crypto", "auth", "input", "memory", "network"],
            "code_graph": ["memory", "auth", "filesystem"],
            "threat_validation": ["crypto", "input", "network"],
            "risk_scoring": ["auth", "input", "memory", "network"],
            "threat_model_assembler": [
                "crypto",
                "auth",
                "input",
                "memory",
                "network",
                "filesystem",
            ],
            "context": ["auth", "crypto", "filesystem"],
            "dependency_extraction": ["crypto", "network"],
            "language_identification": [],  # Not security-focused
            "normalization": [],  # Not security-focused
            "code_ingestion": ["filesystem"],
            "prioritization": ["auth", "input", "memory", "network"],
            "threat_scenario": ["auth", "input", "memory", "network"],
            "threat_simulation": ["auth", "input", "memory", "network", "crypto"],
            "commit_history": ["auth", "crypto", "input"],
        }

        # Calculate agent priorities
        for agent_id, contexts in agent_contexts.items():
            priority = sum(context_scores.get(ctx, 0) for ctx in contexts)
            # Ensure minimum priority of 0.1 for all agents
            self.agent_priorities[agent_id] = max(priority, 0.1)

        self.logger.info(f"Agent priorities assigned: {self.agent_priorities}")
        return self.agent_priorities

    def get_agent_priority(self, agent_id: str) -> float:
        """
        Get the priority for a specific agent.

        Args:
            agent_id: The ID of the agent

        Returns:
            Priority score for the agent (0.0-1.0)
        """
        return self.agent_priorities.get(agent_id, 0.5)  # Default to medium priority

    def adjust_message_processing_order(
        self, messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Adjust the processing order of messages based on agent priorities.

        Args:
            messages: List of message dictionaries

        Returns:
            Reordered list of messages
        """
        if not self.agent_priorities:
            return messages

        # Sort messages by recipient agent priority (descending)
        return sorted(
            messages,
            key=lambda m: self.agent_priorities.get(m.get("recipient_id", ""), 0.5),
            reverse=True,
        )
