#!/usr/bin/env python3
"""
Agent Extension for integrating agentic improvements with existing agents.
Provides methods for agents to access and use agentic improvements.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Agent, Message
from .mcp_integration import AgentMcpServer

logger = logging.getLogger(__name__)


class AgenticAgentExtension:
    """
    Extension for agents to access and use agentic improvements.
    This class is designed to be used as a mixin or through composition
    to add agentic capabilities to existing agents.
    """

    def __init__(self, agent):
        """
        Initialize the agent extension.

        Args:
            agent: The agent to extend
        """
        self.agent = agent
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{agent.id}")
        self._agentic_initialized = False
        self.mcp_server = AgentMcpServer(agent)

    async def initialize_agentic_capabilities(self):
        """Initialize agentic capabilities for the agent"""
        if self._agentic_initialized:
            return

        self.logger.info(f"Initializing agentic capabilities for agent {self.agent.id}")

        # Get agentic components from workspace
        self.agentic_manager = self.agent.workspace.get_data("agentic_manager")
        if not self.agentic_manager:
            self.logger.warning(
                "Agentic manager not found in workspace, creating mock components for testing"
            )
            # Create mock components for testing
            self.agentic_manager = MockAgenticManager()
            self.agent.workspace.store_data("agentic_manager", self.agentic_manager)
            # We'll continue with mock components

        # Get or create other components
        self.prioritizer = self.agent.workspace.get_data("agentic_prioritizer")
        if not self.prioritizer:
            self.prioritizer = MockAgenticPrioritizer()
            self.agent.workspace.store_data("agentic_prioritizer", self.prioritizer)

        self.reasoning = self.agent.workspace.get_data("agentic_reasoning")
        if not self.reasoning:
            self.reasoning = MockAgenticReasoning()
            self.agent.workspace.store_data("agentic_reasoning", self.reasoning)

        self.monitor = self.agent.workspace.get_data("agentic_monitor")
        if not self.monitor:
            self.monitor = MockAgenticMonitor()
            self.agent.workspace.store_data("agentic_monitor", self.monitor)

        self.knowledge = self.agent.workspace.get_data("agentic_knowledge")
        if not self.knowledge:
            self.knowledge = MockAgenticKnowledge()
            self.agent.workspace.store_data("agentic_knowledge", self.knowledge)

        self.learning = self.agent.workspace.get_data("agentic_learning")
        if not self.learning:
            self.learning = MockAgenticLearning()
            self.agent.workspace.store_data("agentic_learning", self.learning)

        # Subscribe to knowledge sharing messages
        self.agent.workspace.subscribe(self.agent.id, "NEW_KNOWLEDGE_AVAILABLE")

        # Subscribe to specific message types based on agent type
        agent_type = self.agent.model.agent_type
        if agent_type == "threat_detection":
            self.agent.workspace.subscribe(self.agent.id, "THREAT_DETECTION_START")
            self.logger.info(
                f"Subscribed agent {self.agent.id} to THREAT_DETECTION_START messages"
            )
        elif agent_type == "prioritization":
            self.agent.workspace.subscribe(self.agent.id, "PRIORITIZATION_START")
            self.logger.info(
                f"Subscribed agent {self.agent.id} to PRIORITIZATION_START messages"
            )
        elif agent_type == "threat_model_assembler":
            self.agent.workspace.subscribe(self.agent.id, "THREAT_MODEL_ASSEMBLY_START")
            self.logger.info(
                f"Subscribed agent {self.agent.id} to THREAT_MODEL_ASSEMBLY_START messages"
            )
        elif agent_type == "code_graph":
            self.agent.workspace.subscribe(self.agent.id, "CODE_GRAPH_GENERATION_START")
            self.logger.info(
                f"Subscribed agent {self.agent.id} to CODE_GRAPH_GENERATION_START messages"
            )

        # Always set to initialized, even with mock components
        self._agentic_initialized = True
        self.logger.info(f"Agentic capabilities initialized for agent {self.agent.id}")
        
        # Start MCP server
        self.logger.info(f"Starting MCP server for agent {self.agent.id}")
        asyncio.create_task(self._start_mcp_server())

    def share_knowledge(
        self,
        knowledge_type: str,
        knowledge_data: Dict[str, Any],
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
    ) -> Optional[str]:
        """
        Share knowledge with other agents.

        Args:
            knowledge_type: The type of knowledge being shared
            knowledge_data: The knowledge data
            confidence: The confidence level in this knowledge (0.0-1.0)
            tags: Optional list of tags for categorizing the knowledge

        Returns:
            The ID of the registered knowledge or None if sharing failed
        """
        if not self._agentic_initialized or not self.knowledge:
            self.logger.warning(
                "Cannot share knowledge: agentic capabilities not initialized"
            )
            return None

        try:
            knowledge_id = self.knowledge.register_knowledge(
                self.agent.id, knowledge_type, knowledge_data, confidence, tags
            )
            self.logger.info(
                f"Shared knowledge of type {knowledge_type} with ID {knowledge_id}"
            )
            return knowledge_id
        except Exception as e:
            self.logger.error(f"Error sharing knowledge: {e}", exc_info=True)
            return None

    def query_knowledge(
        self,
        knowledge_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """
        Query knowledge shared by other agents.

        Args:
            knowledge_type: Optional type to filter by
            tags: Optional list of tags to filter by
            min_confidence: Minimum confidence threshold

        Returns:
            List of matching knowledge entries
        """
        if not self._agentic_initialized or not self.knowledge:
            self.logger.warning(
                "Cannot query knowledge: agentic capabilities not initialized"
            )
            return []

        try:
            results = self.knowledge.query_knowledge(
                knowledge_type, tags, min_confidence
            )
            self.logger.debug(
                f"Found {len(results)} knowledge entries of type {knowledge_type}"
            )

            # Record usage of knowledge
            for result in results:
                self.knowledge.use_knowledge(self.agent.id, result["id"])

            return results
        except Exception as e:
            self.logger.error(f"Error querying knowledge: {e}", exc_info=True)
            return []

    def start_reasoning_chain(
        self, topic: str, initial_insight: Dict[str, Any]
    ) -> Optional[str]:
        """
        Start a new collaborative reasoning chain.

        Args:
            topic: The topic for the reasoning chain
            initial_insight: The initial insight to start the chain

        Returns:
            The ID of the new reasoning chain or None if creation failed
        """
        if not self._agentic_initialized or not self.reasoning:
            self.logger.warning(
                "Cannot start reasoning chain: agentic capabilities not initialized"
            )
            return None

        try:
            chain_id = self.reasoning.start_reasoning_chain(
                topic, initial_insight, self.agent.id
            )
            self.logger.info(
                f"Started reasoning chain on topic '{topic}' with ID {chain_id}"
            )
            return chain_id
        except Exception as e:
            self.logger.error(f"Error starting reasoning chain: {e}", exc_info=True)
            return None

    def contribute_to_reasoning(
        self, chain_id: str, insight: Dict[str, Any], confidence: float = 0.5
    ) -> bool:
        """
        Contribute to an existing reasoning chain.

        Args:
            chain_id: The ID of the reasoning chain
            insight: The insight to contribute
            confidence: The confidence level in this insight (0.0-1.0)

        Returns:
            True if the contribution was successful, False otherwise
        """
        if not self._agentic_initialized or not self.reasoning:
            self.logger.warning(
                "Cannot contribute to reasoning: agentic capabilities not initialized"
            )
            return False

        try:
            success = self.reasoning.contribute_insight(
                chain_id, self.agent.id, insight, confidence
            )
            if success:
                self.logger.info(f"Contributed to reasoning chain {chain_id}")
            else:
                self.logger.warning(
                    f"Failed to contribute to reasoning chain {chain_id}"
                )
            return success
        except Exception as e:
            self.logger.error(
                f"Error contributing to reasoning chain: {e}", exc_info=True
            )
            return False

    def record_performance(self, task_type: str, metrics: Dict[str, Any]):
        """
        Record performance metrics for learning and improvement.

        Args:
            task_type: The type of task performed
            metrics: The performance metrics
        """
        if not self._agentic_initialized or not self.learning:
            return

        try:
            self.learning.record_performance(self.agent.id, task_type, metrics)
        except Exception as e:
            self.logger.error(f"Error recording performance: {e}", exc_info=True)

    def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get improvement suggestions based on performance history.

        Returns:
            List of improvement suggestions
        """
        if not self._agentic_initialized or not self.learning:
            return []

        try:
            return self.learning.get_improvement_suggestions(self.agent.id)
        except Exception as e:
            self.logger.error(
                f"Error getting improvement suggestions: {e}", exc_info=True
            )
            return []

    async def handle_agentic_message(
        self, message: Message
    ) -> Optional[Dict[str, Any]]:
        """
        Handle messages related to agentic improvements.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        if not self._agentic_initialized:
            return None

        message_type = message.message_type

        if message_type == "NEW_KNOWLEDGE_AVAILABLE":
            # Process new knowledge notification
            knowledge_id = message.content.get("knowledge_id")
            knowledge_type = message.content.get("knowledge_type")
            provider = message.content.get("provider")

            # Skip if we're the provider
            if provider == self.agent.id:
                return None

            self.logger.debug(
                f"Received notification of new knowledge {knowledge_id} of type {knowledge_type} from {provider}"
            )

            # Decide whether to use this knowledge based on agent-specific logic
            # This should be overridden by specific agent implementations
            return await self._process_new_knowledge(
                knowledge_id, knowledge_type, provider
            )

        return None

    async def _process_new_knowledge(
        self, knowledge_id: str, knowledge_type: str, provider: str
    ) -> Optional[Dict[str, Any]]:
        """
        Process new knowledge notification.
        This method should be overridden by specific agent implementations.

        Args:
            knowledge_id: The ID of the new knowledge
            knowledge_type: The type of the new knowledge
            provider: The ID of the agent that provided the knowledge

        Returns:
            Optional response data
        """
        # Default implementation just logs the notification
        self.logger.debug(
            f"Processing new knowledge {knowledge_id} of type {knowledge_type} from {provider}"
        )
        return None
        
    async def _start_mcp_server(self):
        """Start the MCP server for this agent"""
        try:
            success = await self.mcp_server.start()
            if success:
                self.logger.info(f"MCP server for agent {self.agent.id} started successfully")
            else:
                self.logger.warning(f"Failed to start MCP server for agent {self.agent.id}")
        except Exception as e:
            self.logger.error(f"Error starting MCP server: {e}", exc_info=True)
    
    async def shutdown(self):
        """Shutdown the agent extension"""
        # Stop MCP server
        if hasattr(self, 'mcp_server'):
            try:
                await self.mcp_server.stop()
                self.logger.info(f"MCP server for agent {self.agent.id} stopped successfully")
            except Exception as e:
                self.logger.error(f"Error stopping MCP server: {e}", exc_info=True)


# Mock implementations of agentic components for testing
class MockAgenticManager:
    """Mock implementation of the agentic manager for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.agents = {}

    def register_agent(self, agent_id, agent_type):
        self.agents[agent_id] = agent_type
        return True


class MockAgenticKnowledge:
    """Mock implementation of the agentic knowledge component for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.knowledge_store = {}
        self.knowledge_usage = {}
        self.next_id = 1

    def register_knowledge(
        self, provider_id, knowledge_type, knowledge_data, confidence=1.0, tags=None
    ):
        knowledge_id = f"knowledge_{self.next_id}"
        self.next_id += 1

        self.knowledge_store[knowledge_id] = {
            "id": knowledge_id,
            "provider": provider_id,
            "type": knowledge_type,
            "data": knowledge_data,
            "confidence": confidence,
            "tags": tags or [],
            "timestamp": asyncio.get_event_loop().time(),
        }

        return knowledge_id

    def query_knowledge(self, knowledge_type=None, tags=None, min_confidence=0.5):
        results = []

        for knowledge_id, knowledge in self.knowledge_store.items():
            # Filter by type if specified
            if knowledge_type and knowledge["type"] != knowledge_type:
                continue

            # Filter by tags if specified
            if tags and not all(tag in knowledge["tags"] for tag in tags):
                continue

            # Filter by confidence
            if knowledge["confidence"] < min_confidence:
                continue

            results.append(knowledge)

        return results

    def use_knowledge(self, agent_id, knowledge_id):
        if knowledge_id not in self.knowledge_usage:
            self.knowledge_usage[knowledge_id] = []

        self.knowledge_usage[knowledge_id].append(
            {"agent_id": agent_id, "timestamp": asyncio.get_event_loop().time()}
        )

        return True


class MockAgenticReasoning:
    """Mock implementation of the agentic reasoning component for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.reasoning_chains = {}
        self.next_id = 1

    def start_reasoning_chain(self, topic, initial_insight, agent_id):
        chain_id = f"chain_{self.next_id}"
        self.next_id += 1

        self.reasoning_chains[chain_id] = {
            "id": chain_id,
            "topic": topic,
            "creator": agent_id,
            "insights": [
                {
                    "agent_id": agent_id,
                    "insight": initial_insight,
                    "confidence": 1.0,
                    "timestamp": asyncio.get_event_loop().time(),
                }
            ],
            "status": "active",
            "created_at": asyncio.get_event_loop().time(),
        }

        return chain_id

    def contribute_insight(self, chain_id, agent_id, insight, confidence=0.5):
        if chain_id not in self.reasoning_chains:
            return False

        chain = self.reasoning_chains[chain_id]

        if chain["status"] != "active":
            return False

        chain["insights"].append(
            {
                "agent_id": agent_id,
                "insight": insight,
                "confidence": confidence,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

        return True


class MockAgenticPrioritizer:
    """Mock implementation of the agentic prioritizer for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.priorities = {}

    def prioritize(self, items, context=None):
        # Simple mock implementation that just returns the items with random priorities
        import random

        result = []
        for i, item in enumerate(items):
            priority = random.choice(["critical", "high", "medium", "low"])
            result.append(
                {"item": item, "priority": priority, "score": random.random()}
            )

        return result


class MockAgenticMonitor:
    """Mock implementation of the agentic monitor for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.activities = {}

    def record_agent_activity(self, agent_id, job_id=None):
        if agent_id not in self.activities:
            self.activities[agent_id] = []

        self.activities[agent_id].append(
            {"timestamp": asyncio.get_event_loop().time(), "job_id": job_id}
        )

        return True


class MockAgenticLearning:
    """Mock implementation of the agentic learning component for testing"""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.performance_records = {}

    def record_performance(self, agent_id, task_type, metrics):
        if agent_id not in self.performance_records:
            self.performance_records[agent_id] = []

        self.performance_records[agent_id].append(
            {
                "task_type": task_type,
                "metrics": metrics,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

        return True

    def get_improvement_suggestions(self, agent_id):
        # Return mock suggestions
        return [
            {
                "suggestion": "Consider optimizing processing time for better performance",
                "confidence": 0.8,
                "based_on": "performance metrics",
            },
            {
                "suggestion": "Increase memory efficiency for large-scale operations",
                "confidence": 0.7,
                "based_on": "resource usage patterns",
            },
        ]
