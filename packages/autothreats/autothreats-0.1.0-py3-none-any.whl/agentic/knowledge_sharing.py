#!/usr/bin/env python3
"""
Dynamic Knowledge Sharing Protocol for the autonomous threat modeling system.
Enables agents to share knowledge and insights dynamically.
"""

import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Message

logger = logging.getLogger(__name__)


class KnowledgeSharingProtocol:
    """
    Enables agents to dynamically share knowledge and insights.
    Provides a structured way for agents to register, query, and use
    knowledge from other agents in the system.
    """

    def __init__(self, workspace):
        """
        Initialize the knowledge sharing protocol.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.knowledge_base = {}
        self.knowledge_types = {
            "security_pattern": "Recurring security-related code patterns",
            "vulnerability": "Potential security vulnerabilities",
            "dependency_risk": "Security risks in dependencies",
            "attack_vector": "Potential attack vectors",
            "security_control": "Implemented security controls",
            "threat_scenario": "Potential threat scenarios",
            "code_insight": "General insights about the code",
            "historical_context": "Historical context from commit history",
            "architectural_insight": "Insights about the system architecture",
        }
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def register_knowledge(
        self,
        agent_id: str,
        knowledge_type: str,
        knowledge_data: Dict[str, Any],
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Register a piece of knowledge in the shared knowledge base.

        Args:
            agent_id: The ID of the agent registering the knowledge
            knowledge_type: The type of knowledge being registered
            knowledge_data: The knowledge data
            confidence: The confidence level in this knowledge (0.0-1.0)
            tags: Optional list of tags for categorizing the knowledge

        Returns:
            The ID of the registered knowledge
        """
        # Validate knowledge type
        if knowledge_type not in self.knowledge_types:
            self.logger.warning(
                f"Unknown knowledge type: {knowledge_type}, defaulting to code_insight"
            )
            knowledge_type = "code_insight"

        knowledge_id = str(uuid.uuid4())
        timestamp = time.time()

        # Ensure knowledge_data has a summary
        if "summary" not in knowledge_data:
            # Extract first 100 chars of the first value as a fallback summary
            for key, value in knowledge_data.items():
                if isinstance(value, str) and value:
                    knowledge_data["summary"] = value[:100] + (
                        "..." if len(value) > 100 else ""
                    )
                    break
            if "summary" not in knowledge_data:
                knowledge_data["summary"] = f"{knowledge_type} from {agent_id}"

        # Add container/pod information for distributed tracing
        container_id = os.environ.get("HOSTNAME", "unknown")
        pod_name = os.environ.get("POD_NAME", container_id)

        knowledge_entry = {
            "id": knowledge_id,
            "agent_id": agent_id,
            "type": knowledge_type,
            "data": knowledge_data,
            "confidence": confidence,
            "created_at": timestamp,
            "updated_at": timestamp,
            "tags": tags or [],
            "references": [],
            "used_by": [],
            "usage_count": 0,
            "feedback": {},
            "source": {
                "container_id": container_id,
                "pod_name": pod_name,
                "timestamp": timestamp,
                "distributed_id": f"{agent_id}_{timestamp}_{container_id}",
            },
            # Add chunk information if available
            "chunk_info": knowledge_data.get("chunk_info", {}),
        }

        self.knowledge_base[knowledge_id] = knowledge_entry

        # Store in workspace for persistence with retry mechanism for distributed reliability
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.workspace.store_data(f"knowledge_{knowledge_id}", knowledge_entry)
                break
            except Exception as e:
                retry_count += 1
                self.logger.warning(
                    f"Retry {retry_count}/{max_retries} storing knowledge: {str(e)}"
                )
                time.sleep(0.5)  # Short delay before retry

        if retry_count == max_retries:
            self.logger.error(
                f"Failed to store knowledge {knowledge_id} after {max_retries} retries"
            )

        self.logger.info(
            f"Agent {agent_id} registered {knowledge_type} knowledge with ID {knowledge_id}"
        )

        # Notify other agents about new knowledge with enhanced distributed information
        message_content = {
            "knowledge_id": knowledge_id,
            "knowledge_type": knowledge_type,
            "provider": agent_id,
            "summary": knowledge_data.get("summary", ""),
            "tags": tags or [],
            "confidence": confidence,
            "distributed_info": {
                "container_id": container_id,
                "pod_name": pod_name,
                "timestamp": timestamp,
                "distributed_id": f"{agent_id}_{timestamp}_{container_id}",
            },
            # Include chunk information if this knowledge relates to a specific file chunk
            "chunk_info": knowledge_data.get("chunk_info", {}),
        }

        # Add file path information if available for better cross-agent correlation
        if "file_path" in knowledge_data:
            message_content["file_path"] = knowledge_data["file_path"]

        # Try to publish message with retry mechanism for reliability
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.workspace.publish_message(
                    Message("NEW_KNOWLEDGE_AVAILABLE", message_content, agent_id)
                )
                break
            except Exception as e:
                retry_count += 1
                self.logger.warning(
                    f"Retry {retry_count}/{max_retries} publishing knowledge message: {str(e)}"
                )
                time.sleep(0.5)  # Short delay before retry

        if retry_count == max_retries:
            self.logger.error(
                f"Failed to publish knowledge message for {knowledge_id} after {max_retries} retries"
            )

        return knowledge_id

    def update_knowledge(
        self, knowledge_id: str, agent_id: str, updates: Dict[str, Any]
    ) -> bool:
        """
        Update an existing knowledge entry.

        Args:
            knowledge_id: The ID of the knowledge to update
            agent_id: The ID of the agent updating the knowledge
            updates: The updates to apply

        Returns:
            True if the knowledge was updated successfully, False otherwise
        """
        if knowledge_id not in self.knowledge_base:
            self.logger.warning(
                f"Attempted to update non-existent knowledge {knowledge_id}"
            )
            return False

        knowledge = self.knowledge_base[knowledge_id]

        # Only the original agent or a designated reviewer can update knowledge
        if agent_id != knowledge["agent_id"] and agent_id not in knowledge.get(
            "reviewers", []
        ):
            self.logger.warning(
                f"Agent {agent_id} not authorized to update knowledge {knowledge_id}"
            )
            return False

        # Update the knowledge
        if "data" in updates:
            knowledge["data"].update(updates["data"])

        if "confidence" in updates:
            knowledge["confidence"] = updates["confidence"]

        if "tags" in updates:
            knowledge["tags"] = list(set(knowledge["tags"] + updates["tags"]))

        knowledge["updated_at"] = time.time()

        # Store in workspace for persistence
        self.workspace.store_data(f"knowledge_{knowledge_id}", knowledge)

        self.logger.info(f"Agent {agent_id} updated knowledge {knowledge_id}")

        return True

    def use_knowledge(
        self, agent_id: str, knowledge_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Record that an agent has used a piece of knowledge and return the knowledge.

        Args:
            agent_id: The ID of the agent using the knowledge
            knowledge_id: The ID of the knowledge being used

        Returns:
            The knowledge data if found, None otherwise
        """
        if knowledge_id not in self.knowledge_base:
            return None

        knowledge = self.knowledge_base[knowledge_id]

        # Record usage
        if agent_id not in knowledge["used_by"]:
            knowledge["used_by"].append(agent_id)
        knowledge["usage_count"] += 1

        # Store in workspace for persistence
        self.workspace.store_data(f"knowledge_{knowledge_id}", knowledge)

        self.logger.debug(f"Agent {agent_id} used knowledge {knowledge_id}")

        return knowledge

    def provide_feedback(
        self, agent_id: str, knowledge_id: str, feedback_type: str, feedback_data: Any
    ) -> bool:
        """
        Provide feedback on a piece of knowledge.

        Args:
            agent_id: The ID of the agent providing feedback
            knowledge_id: The ID of the knowledge to provide feedback on
            feedback_type: The type of feedback (e.g., "usefulness", "accuracy")
            feedback_data: The feedback data

        Returns:
            True if feedback was recorded successfully, False otherwise
        """
        if knowledge_id not in self.knowledge_base:
            return False

        knowledge = self.knowledge_base[knowledge_id]

        # Record feedback
        if "feedback" not in knowledge:
            knowledge["feedback"] = {}

        if agent_id not in knowledge["feedback"]:
            knowledge["feedback"][agent_id] = {}

        knowledge["feedback"][agent_id][feedback_type] = {
            "data": feedback_data,
            "timestamp": time.time(),
        }

        # Store in workspace for persistence
        self.workspace.store_data(f"knowledge_{knowledge_id}", knowledge)

        self.logger.info(
            f"Agent {agent_id} provided {feedback_type} feedback on knowledge {knowledge_id}"
        )

        return True

    def query_knowledge(
        self,
        knowledge_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.0,
        agent_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query the knowledge base for specific types of knowledge.

        Args:
            knowledge_type: Optional type to filter by
            tags: Optional list of tags to filter by
            min_confidence: Minimum confidence threshold
            agent_id: Optional agent ID to filter by

        Returns:
            List of matching knowledge entries
        """
        results = []

        for k_id, knowledge in self.knowledge_base.items():
            # Apply filters
            if knowledge_type and knowledge["type"] != knowledge_type:
                continue

            if tags and not any(tag in knowledge["tags"] for tag in tags):
                continue

            if knowledge["confidence"] < min_confidence:
                continue

            if agent_id and knowledge["agent_id"] != agent_id:
                continue

            results.append(knowledge)

        # Sort by confidence and then by usage count
        results.sort(key=lambda k: (k["confidence"], k["usage_count"]), reverse=True)

        return results

    def get_knowledge_by_id(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific knowledge entry by ID.

        Args:
            knowledge_id: The ID of the knowledge

        Returns:
            The knowledge entry or None if not found
        """
        return self.knowledge_base.get(knowledge_id)

    def add_reference(self, knowledge_id: str, reference_id: str) -> bool:
        """
        Add a reference from one knowledge entry to another.

        Args:
            knowledge_id: The ID of the knowledge entry
            reference_id: The ID of the referenced knowledge entry

        Returns:
            True if the reference was added successfully, False otherwise
        """
        if (
            knowledge_id not in self.knowledge_base
            or reference_id not in self.knowledge_base
        ):
            return False

        knowledge = self.knowledge_base[knowledge_id]

        if reference_id not in knowledge["references"]:
            knowledge["references"].append(reference_id)

        # Store in workspace for persistence
        self.workspace.store_data(f"knowledge_{knowledge_id}", knowledge)

        return True

    def get_related_knowledge(self, knowledge_id: str) -> List[Dict[str, Any]]:
        """
        Get knowledge entries related to a specific entry.

        Args:
            knowledge_id: The ID of the knowledge entry

        Returns:
            List of related knowledge entries
        """
        if knowledge_id not in self.knowledge_base:
            return []

        knowledge = self.knowledge_base[knowledge_id]
        related = []

        # Get referenced knowledge
        for ref_id in knowledge["references"]:
            if ref_id in self.knowledge_base:
                related.append(self.knowledge_base[ref_id])

        # Get knowledge that references this entry
        for k_id, k in self.knowledge_base.items():
            if knowledge_id in k["references"] and k_id != knowledge_id:
                related.append(k)

        # Get knowledge with similar tags
        if knowledge["tags"]:
            for k_id, k in self.knowledge_base.items():
                if k_id != knowledge_id and k_id not in [r["id"] for r in related]:
                    common_tags = set(knowledge["tags"]).intersection(k["tags"])
                    if common_tags:
                        k_copy = k.copy()
                        k_copy["common_tags"] = list(common_tags)
                        related.append(k_copy)

        return related
