#!/usr/bin/env python3
"""
Simplified Base Agent class with agentic improvements integration.
Extends the standard Agent class with agentic capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Agent, SharedWorkspace

logger = logging.getLogger(__name__)


class SimplifiedAgenticAgent(Agent):
    """
    Simplified base class for agents with agentic capabilities.
    Extends the standard Agent class with agentic improvements.
    """

    def __init__(
        self, agent_id: str, agent_type: str, config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the agentic agent.

        Args:
            agent_id: The ID of the agent
            agent_type: The type of agent
            config: Optional configuration
        """
        super().__init__(agent_id, agent_type, config)
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{agent_id}")
        self.knowledge_store = {}
        self.reasoning_chains = {}
        self.performance_history = []

    async def initialize(self):
        """Initialize the agent with agentic capabilities"""
        self.logger.info(
            f"Initializing agent {self.id} of type {self.model.agent_type}"
        )

        # Initialize the base agent first
        self.logger.debug(f"Agent {self.id}: Initializing base agent capabilities")
        await super().initialize()
        self.logger.debug(f"Agent {self.id}: Base agent initialization complete")

        # Check if workspace is available and agentic improvements are enabled
        if self.workspace:
            self.logger.debug(
                f"Agent {self.id}: Workspace is available, checking agentic configuration"
            )
            system_config = self.workspace.get_data("system_config", {})
            enable_agentic = system_config.get("enable_agentic_improvements", False)

            self.logger.info(
                f"Agent {self.id}: Agentic improvements enabled: {enable_agentic}"
            )

            if enable_agentic:
                # Initialize agentic capabilities
                self.logger.info(f"Agent {self.id}: Initializing agentic capabilities")
                await self._initialize_agentic_capabilities()
                self.logger.info(
                    f"Agent {self.id}: Agentic capabilities initialized successfully"
                )
        else:
            self.logger.warning(
                f"Agent {self.id}: No workspace available, skipping agentic initialization"
            )

        self.logger.info(f"Agent {self.id} initialization complete")

    async def _initialize_agentic_capabilities(self):
        """Initialize agentic capabilities"""
        # Initialize knowledge store
        self.knowledge_store = {}

        # Initialize reasoning chains
        self.reasoning_chains = {}

        # Initialize performance history
        self.performance_history = []

        # Register with the workspace
        if self.workspace:
            self.workspace.store_data(f"agentic_agent_{self.id}", self)

    async def process_task(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a task with agentic capabilities.

        Args:
            task_type: The type of task to process
            task_data: The data for the task

        Returns:
            Result data
        """
        # Log detailed information about the task being processed
        self.logger.info(
            f"Agent {self.id} ({self.model.agent_type}) processing task: {task_type}"
        )
        self.logger.debug(f"Task details: {task_data}")

        # Check if this is an agentic task
        agentic_task_types = [
            "knowledge_sharing",
            "collaborative_reasoning",
            "performance_analysis",
        ]

        if task_type in agentic_task_types:
            # Handle with agentic capabilities
            self.logger.info(f"Agent {self.id} handling agentic task: {task_type}")
            result = await self._handle_agentic_task(task_type, task_data)
            self.logger.info(f"Agent {self.id} completed agentic task processing")
            return result

        # Otherwise, process with standard agent
        self.logger.info(f"Agent {self.id} processing standard task: {task_type}")
        result = await self._handle_standard_task(task_type, task_data)
        self.logger.info(f"Agent {self.id} completed standard task processing")
        return result

    async def _handle_agentic_task(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle an agentic task"""
        if task_type == "knowledge_sharing":
            return await self._handle_knowledge_sharing(task_data)
        elif task_type == "collaborative_reasoning":
            return await self._handle_collaborative_reasoning(task_data)
        elif task_type == "performance_analysis":
            return await self._handle_performance_analysis(task_data)
        else:
            return {
                "status": "error",
                "message": f"Unsupported agentic task type: {task_type}",
            }

    async def _handle_standard_task(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a standard task"""
        # This should be implemented by subclasses
        return {
            "status": "error",
            "message": "Standard task handling not implemented",
        }

    async def _handle_knowledge_sharing(
        self, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a knowledge sharing task"""
        knowledge_type = task_data.get("knowledge_type")
        knowledge_data = task_data.get("knowledge_data")
        confidence = task_data.get("confidence", 1.0)
        tags = task_data.get("tags", [])

        if not knowledge_type or not knowledge_data:
            return {
                "status": "error",
                "message": "Missing required parameters for knowledge sharing",
            }

        knowledge_id = self.share_knowledge(
            knowledge_type, knowledge_data, confidence, tags
        )

        return {
            "status": "success",
            "knowledge_id": knowledge_id,
            "message": "Knowledge shared successfully",
        }

    async def _handle_collaborative_reasoning(
        self, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a collaborative reasoning task"""
        action = task_data.get("action")

        if action == "start_chain":
            topic = task_data.get("topic")
            initial_insight = task_data.get("initial_insight")

            if not topic or not initial_insight:
                return {
                    "status": "error",
                    "message": "Missing required parameters for starting reasoning chain",
                }

            chain_id = self.start_reasoning_chain(topic, initial_insight)

            return {
                "status": "success",
                "chain_id": chain_id,
                "message": "Reasoning chain started successfully",
            }

        elif action == "contribute":
            chain_id = task_data.get("chain_id")
            insight = task_data.get("insight")
            confidence = task_data.get("confidence", 0.5)

            if not chain_id or not insight:
                return {
                    "status": "error",
                    "message": "Missing required parameters for contributing to reasoning chain",
                }

            success = self.contribute_to_reasoning(chain_id, insight, confidence)

            return {
                "status": "success" if success else "error",
                "chain_id": chain_id,
                "message": (
                    "Contribution added successfully"
                    if success
                    else "Failed to add contribution"
                ),
            }

        else:
            return {
                "status": "error",
                "message": f"Unsupported collaborative reasoning action: {action}",
            }

    async def _handle_performance_analysis(
        self, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle a performance analysis task"""
        action = task_data.get("action")

        if action == "record_performance":
            task_type = task_data.get("task_type")
            metrics = task_data.get("metrics")

            if not task_type or not metrics:
                return {
                    "status": "error",
                    "message": "Missing required parameters for recording performance",
                }

            self.record_performance(task_type, metrics)

            return {
                "status": "success",
                "message": "Performance recorded successfully",
            }

        elif action == "get_suggestions":
            suggestions = self.get_improvement_suggestions()

            return {
                "status": "success",
                "suggestions": suggestions,
                "message": "Improvement suggestions retrieved successfully",
            }

        else:
            return {
                "status": "error",
                "message": f"Unsupported performance analysis action: {action}",
            }

    def share_knowledge(
        self,
        knowledge_type: str,
        knowledge_data: Dict[str, Any],
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Share knowledge with other agents.

        Args:
            knowledge_type: The type of knowledge being shared
            knowledge_data: The knowledge data
            confidence: The confidence level in this knowledge (0.0-1.0)
            tags: Optional list of tags for categorizing the knowledge

        Returns:
            The ID of the registered knowledge
        """
        self.logger.info(
            f"Agent {self.id} sharing knowledge of type: {knowledge_type} "
            f"with confidence: {confidence}"
        )
        if tags:
            self.logger.info(f"Knowledge tags: {tags}")

        self.logger.debug(f"Knowledge data: {knowledge_data}")

        # Generate a unique ID for this knowledge
        knowledge_id = f"knowledge_{len(self.knowledge_store) + 1}"

        # Store the knowledge
        self.knowledge_store[knowledge_id] = {
            "type": knowledge_type,
            "data": knowledge_data,
            "confidence": confidence,
            "tags": tags or [],
            "agent_id": self.id,
            "timestamp": asyncio.get_event_loop().time(),
        }

        # Share with workspace if available
        if self.workspace:
            self.workspace.store_data(
                f"knowledge_{knowledge_id}", self.knowledge_store[knowledge_id]
            )

        self.logger.info(f"Knowledge shared successfully with ID: {knowledge_id}")
        return knowledge_id

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
        results = []

        # First check workspace for shared knowledge
        if self.workspace:
            for key, value in self.workspace.get_all_data().items():
                if key.startswith("knowledge_"):
                    # Check if it matches the filters
                    if knowledge_type and value.get("type") != knowledge_type:
                        continue

                    if tags and not all(tag in value.get("tags", []) for tag in tags):
                        continue

                    if value.get("confidence", 0) < min_confidence:
                        continue

                    results.append(value)

        # Then check local knowledge store
        for knowledge_id, knowledge in self.knowledge_store.items():
            # Check if it matches the filters
            if knowledge_type and knowledge.get("type") != knowledge_type:
                continue

            if tags and not all(tag in knowledge.get("tags", []) for tag in tags):
                continue

            if knowledge.get("confidence", 0) < min_confidence:
                continue

            # Check if it's already in results
            if not any(
                r.get("timestamp") == knowledge.get("timestamp") for r in results
            ):
                results.append(knowledge)

        return results

    def start_reasoning_chain(self, topic: str, initial_insight: Dict[str, Any]) -> str:
        """
        Start a new collaborative reasoning chain.

        Args:
            topic: The topic for the reasoning chain
            initial_insight: The initial insight to start the chain

        Returns:
            The ID of the new reasoning chain
        """
        # Generate a unique ID for this reasoning chain
        chain_id = f"reasoning_{len(self.reasoning_chains) + 1}"

        # Create the reasoning chain
        self.reasoning_chains[chain_id] = {
            "topic": topic,
            "insights": [
                {
                    "agent_id": self.id,
                    "insight": initial_insight,
                    "confidence": 1.0,
                    "timestamp": asyncio.get_event_loop().time(),
                }
            ],
            "created_by": self.id,
            "created_at": asyncio.get_event_loop().time(),
            "last_updated": asyncio.get_event_loop().time(),
        }

        # Share with workspace if available
        if self.workspace:
            self.workspace.store_data(
                f"reasoning_{chain_id}", self.reasoning_chains[chain_id]
            )

        return chain_id

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
        # Check if the chain exists in local store
        if chain_id in self.reasoning_chains:
            # Add the insight
            self.reasoning_chains[chain_id]["insights"].append(
                {
                    "agent_id": self.id,
                    "insight": insight,
                    "confidence": confidence,
                    "timestamp": asyncio.get_event_loop().time(),
                }
            )

            # Update last_updated
            self.reasoning_chains[chain_id][
                "last_updated"
            ] = asyncio.get_event_loop().time()

            # Share with workspace if available
            if self.workspace:
                self.workspace.store_data(
                    f"reasoning_{chain_id}", self.reasoning_chains[chain_id]
                )

            return True

        # Check if the chain exists in workspace
        elif self.workspace and self.workspace.get_data(f"reasoning_{chain_id}"):
            # Get the chain from workspace
            chain = self.workspace.get_data(f"reasoning_{chain_id}")

            # Add the insight
            chain["insights"].append(
                {
                    "agent_id": self.id,
                    "insight": insight,
                    "confidence": confidence,
                    "timestamp": asyncio.get_event_loop().time(),
                }
            )

            # Update last_updated
            chain["last_updated"] = asyncio.get_event_loop().time()

            # Store back in workspace
            self.workspace.store_data(f"reasoning_{chain_id}", chain)

            # Also store in local cache
            self.reasoning_chains[chain_id] = chain

            return True

        return False

    def record_performance(self, task_type: str, metrics: Dict[str, Any]):
        """
        Record performance metrics for learning and improvement.

        Args:
            task_type: The type of task performed
            metrics: The performance metrics
        """
        # Add to performance history
        self.performance_history.append(
            {
                "task_type": task_type,
                "metrics": metrics,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

        # Limit history size
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]

    def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get improvement suggestions based on performance history.

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Simple analysis of performance history
        if len(self.performance_history) > 0:
            # Group by task type
            task_types = {}
            for entry in self.performance_history:
                task_type = entry["task_type"]
                if task_type not in task_types:
                    task_types[task_type] = []
                task_types[task_type].append(entry)

            # Analyze each task type
            for task_type, entries in task_types.items():
                # Calculate average processing time
                avg_time = sum(
                    entry["metrics"].get("processing_time", 0) for entry in entries
                ) / len(entries)

                # Check if processing time is increasing
                if len(entries) > 5:
                    recent_avg = (
                        sum(
                            entry["metrics"].get("processing_time", 0)
                            for entry in entries[-5:]
                        )
                        / 5
                    )
                    if recent_avg > avg_time * 1.2:
                        suggestions.append(
                            {
                                "task_type": task_type,
                                "suggestion": "Processing time is increasing, consider optimization",
                                "metrics": {
                                    "avg_time": avg_time,
                                    "recent_avg": recent_avg,
                                },
                            }
                        )

        return suggestions

    async def shutdown(self):
        """Clean up resources when shutting down"""
        self.logger.info(f"Shutting down agent {self.id}")

        # Clean up knowledge store
        self.knowledge_store.clear()

        # Clean up reasoning chains
        self.reasoning_chains.clear()

        # Clean up performance history
        self.performance_history.clear()

        # Call base shutdown
        await super().shutdown()

        self.logger.info(f"Agent {self.id} shutdown complete")
