#!/usr/bin/env python3
"""
Collaborative Reasoning Framework for the autonomous threat modeling system.
Enables agents to share insights and build on each other's findings.
"""

import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class CollaborativeReasoning:
    """
    Enables agents to collaboratively reason about security concerns by
    sharing insights and building on each other's findings.
    """

    def __init__(self, workspace):
        """
        Initialize the collaborative reasoning framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.reasoning_chains = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def start_reasoning_chain(
        self, topic: str, initial_insight: Dict[str, Any], agent_id: str
    ) -> str:
        """
        Start a new reasoning chain on a security topic.

        Args:
            topic: The security topic for this reasoning chain
            initial_insight: The initial insight to start the chain
            agent_id: The ID of the agent starting the chain

        Returns:
            The ID of the new reasoning chain
        """
        chain_id = str(uuid.uuid4())

        # Add metadata to the insight
        insight_with_metadata = initial_insight.copy()
        insight_with_metadata.update(
            {
                "agent": agent_id,
                "timestamp": time.time(),
                "confidence": initial_insight.get("confidence", 0.5),
            }
        )

        self.reasoning_chains[chain_id] = {
            "id": chain_id,
            "topic": topic,
            "insights": [insight_with_metadata],
            "contributors": [agent_id],
            "confidence": initial_insight.get("confidence", 0.5),
            "created_at": time.time(),
            "updated_at": time.time(),
            "status": "active",
        }

        self.logger.info(
            f"Started reasoning chain {chain_id} on topic '{topic}' by agent {agent_id}"
        )

        # Store in workspace for persistence
        self.workspace.store_data(
            f"reasoning_chain_{chain_id}", self.reasoning_chains[chain_id]
        )

        return chain_id

    def contribute_insight(
        self,
        chain_id: str,
        agent_id: str,
        insight: Dict[str, Any],
        confidence: float = 0.5,
    ) -> bool:
        """
        Add an insight to an existing reasoning chain.

        Args:
            chain_id: The ID of the reasoning chain
            agent_id: The ID of the contributing agent
            insight: The insight to add to the chain
            confidence: The confidence level in this insight (0.0-1.0)

        Returns:
            True if the insight was added successfully, False otherwise
        """
        if chain_id not in self.reasoning_chains:
            self.logger.warning(
                f"Attempted to contribute to non-existent reasoning chain {chain_id}"
            )
            return False

        chain = self.reasoning_chains[chain_id]

        # Add the new insight with metadata
        insight_with_metadata = insight.copy()
        insight_with_metadata.update(
            {
                "agent": agent_id,
                "timestamp": time.time(),
                "confidence": confidence,
                "references": insight.get("references", []),
            }
        )

        chain["insights"].append(insight_with_metadata)
        chain["updated_at"] = time.time()

        # Update chain metadata
        if agent_id not in chain["contributors"]:
            chain["contributors"].append(agent_id)

        # Update overall confidence using Bayesian update
        prior_confidence = chain["confidence"]
        chain["confidence"] = (prior_confidence + confidence) / 2

        self.logger.info(
            f"Agent {agent_id} contributed insight to chain {chain_id}, new confidence: {chain['confidence']:.2f}"
        )

        # Update in workspace for persistence
        self.workspace.store_data(f"reasoning_chain_{chain_id}", chain)

        return True

    def get_reasoning_chains(
        self, topic: Optional[str] = None, min_confidence: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Get reasoning chains, optionally filtered by topic and confidence.

        Args:
            topic: Optional topic to filter by
            min_confidence: Minimum confidence threshold

        Returns:
            List of matching reasoning chains
        """
        results = []
        for chain in self.reasoning_chains.values():
            if (topic is None or chain["topic"] == topic) and chain[
                "confidence"
            ] >= min_confidence:
                results.append(chain)

        # Sort by confidence (descending)
        results.sort(key=lambda c: c["confidence"], reverse=True)
        return results

    def get_chain_by_id(self, chain_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific reasoning chain by ID.

        Args:
            chain_id: The ID of the reasoning chain

        Returns:
            The reasoning chain or None if not found
        """
        return self.reasoning_chains.get(chain_id)

    def get_agent_contributions(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all insights contributed by a specific agent.

        Args:
            agent_id: The ID of the agent

        Returns:
            List of insights contributed by the agent
        """
        contributions = []
        for chain in self.reasoning_chains.values():
            for insight in chain["insights"]:
                if insight.get("agent") == agent_id:
                    # Add chain context to the insight
                    insight_with_context = insight.copy()
                    insight_with_context["chain_id"] = chain["id"]
                    insight_with_context["chain_topic"] = chain["topic"]
                    contributions.append(insight_with_context)

        return contributions

    def close_reasoning_chain(self, chain_id: str, conclusion: Dict[str, Any]) -> bool:
        """
        Close a reasoning chain with a conclusion.

        Args:
            chain_id: The ID of the reasoning chain
            conclusion: The conclusion of the reasoning chain

        Returns:
            True if the chain was closed successfully, False otherwise
        """
        if chain_id not in self.reasoning_chains:
            return False

        chain = self.reasoning_chains[chain_id]
        chain["status"] = "closed"
        chain["conclusion"] = conclusion
        chain["closed_at"] = time.time()

        self.logger.info(f"Closed reasoning chain {chain_id} with conclusion")

        # Update in workspace for persistence
        self.workspace.store_data(f"reasoning_chain_{chain_id}", chain)

        return True

    def get_related_chains(
        self, topic: str, threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Find reasoning chains related to a given topic.

        Args:
            topic: The topic to find related chains for
            threshold: Similarity threshold (0.0-1.0)

        Returns:
            List of related reasoning chains
        """
        # Simple keyword matching for now
        topic_keywords = set(topic.lower().split())
        related_chains = []

        for chain in self.reasoning_chains.values():
            chain_topic = chain["topic"].lower()
            chain_keywords = set(chain_topic.split())

            # Calculate Jaccard similarity
            intersection = len(topic_keywords.intersection(chain_keywords))
            union = len(topic_keywords.union(chain_keywords))
            similarity = intersection / union if union > 0 else 0

            if similarity >= threshold:
                chain_copy = chain.copy()
                chain_copy["similarity"] = similarity
                related_chains.append(chain_copy)

        # Sort by similarity (descending)
        related_chains.sort(key=lambda c: c["similarity"], reverse=True)
        return related_chains
