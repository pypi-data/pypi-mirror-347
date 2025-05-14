#!/usr/bin/env python3
"""
Base Agent class with agentic improvements integration.
Extends the standard Agent class with agentic capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Agent, AgentController, Message
from .agent_extension import AgenticAgentExtension

logger = logging.getLogger(__name__)


class AgenticAgent(Agent):
    """
    Base class for agents with agentic capabilities.
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
        self.agentic_extension = AgenticAgentExtension(self)
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{agent_id}")

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
        try:
            if self.workspace:
                self.logger.debug(
                    f"Agent {self.id}: Workspace is available, checking agentic configuration"
                )
                try:
                    system_config = self.workspace.get_data("system_config", {})
                    enable_agentic = system_config.get(
                        "enable_agentic_improvements", False
                    )

                    self.logger.info(
                        f"Agent {self.id}: Agentic improvements enabled: {enable_agentic}"
                    )

                    if enable_agentic:
                        # Initialize agentic capabilities
                        self.logger.info(
                            f"Agent {self.id}: Initializing agentic capabilities"
                        )
                        await self.agentic_extension.initialize_agentic_capabilities()
                        self.logger.info(
                            f"Agent {self.id}: Agentic capabilities initialized successfully"
                        )
                except Exception as e:
                    self.logger.warning(
                        f"Agent {self.id}: Error accessing workspace data: {str(e)}"
                    )
                    self.logger.warning(
                        f"Agent {self.id}: Continuing with basic initialization"
                    )
            else:
                self.logger.warning(
                    f"Agent {self.id}: No workspace available, skipping agentic initialization"
                )
        except Exception as e:
            self.logger.warning(
                f"Agent {self.id}: Error during agentic initialization: {str(e)}"
            )
            self.logger.warning(
                f"Agent {self.id}: Continuing with basic initialization"
            )

        self.logger.info(f"Agent {self.id} initialization complete")

    async def process_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Process a message with agentic capabilities.

        Args:
            message: The message to process

        Returns:
            Optional response data
        """
        # Log detailed information about the message being processed
        self.logger.info(
            f"Agent {self.id} ({self.model.agent_type}) processing message: {message.message_type}"
        )
        self.logger.debug(f"Message details: {message.to_dict()}")

        # Check if this is an agentic message
        agentic_message_types = [
            "NEW_KNOWLEDGE_AVAILABLE",
            "RETRY_STAGE",
            "SKIP_STAGE",
            "USE_MINIMAL_ANALYSIS",
        ]

        if message.message_type in agentic_message_types:
            # Handle with agentic extension
            self.logger.info(
                f"Agent {self.id} handling agentic message: {message.message_type}"
            )
            result = await self.agentic_extension.handle_agentic_message(message)
            self.logger.info(f"Agent {self.id} completed agentic message processing")
            return result

        # Otherwise, process with standard agent
        self.logger.info(
            f"Agent {self.id} processing standard message: {message.message_type}"
        )
        result = await super().process_message(message)
        self.logger.info(f"Agent {self.id} completed standard message processing")
        return result

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
        self.logger.info(
            f"Agent {self.id} sharing knowledge of type: {knowledge_type} "
            f"with confidence: {confidence}"
        )
        if tags:
            self.logger.info(f"Knowledge tags: {tags}")

        self.logger.debug(f"Knowledge data: {knowledge_data}")

        knowledge_id = self.agentic_extension.share_knowledge(
            knowledge_type, knowledge_data, confidence, tags
        )

        if knowledge_id:
            self.logger.info(f"Knowledge shared successfully with ID: {knowledge_id}")
        else:
            self.logger.warning(f"Failed to share knowledge of type: {knowledge_type}")

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
        return self.agentic_extension.query_knowledge(
            knowledge_type, tags, min_confidence
        )

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
        return self.agentic_extension.start_reasoning_chain(topic, initial_insight)

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
        return self.agentic_extension.contribute_to_reasoning(
            chain_id, insight, confidence
        )

    def record_performance(self, task_type: str, metrics: Dict[str, Any]):
        """
        Record performance metrics for learning and improvement.

        Args:
            task_type: The type of task performed
            metrics: The performance metrics
        """
        self.agentic_extension.record_performance(task_type, metrics)

    def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get improvement suggestions based on performance history.

        Returns:
            List of improvement suggestions
        """
        return self.agentic_extension.get_improvement_suggestions()


class AgenticAgentController(AgentController):
    """
    Base controller class for agentic agents.
    Extends the standard AgentController with agentic capabilities.
    """

    async def handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle a message with agentic capabilities.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        # Add a timeout to prevent getting stuck
        try:
            # Set a reasonable timeout for message processing
            return await asyncio.wait_for(
                self._handle_message_with_monitoring(message),
                timeout=30.0,  # 30 second timeout
            )
        except asyncio.TimeoutError:
            self.logger.error(
                f"Timeout while processing message {message.message_type} in agent {self.model.id}"
            )
            return {
                "status": "error",
                "message": f"Timeout while processing message {message.message_type}",
                "details": "The operation took too long and was aborted to prevent system lockup",
            }
        except Exception as e:
            self.logger.error(
                f"Unexpected error in handle_message for {message.message_type}: {str(e)}",
                exc_info=True,
            )
            return {
                "status": "error",
                "message": f"Error processing message: {str(e)}",
                "details": "An unexpected error occurred during message processing",
            }

    async def _handle_message_with_monitoring(
        self, message: Message
    ) -> Optional[Dict[str, Any]]:
        """Internal method to handle message with monitoring"""
        # Record agent activity for monitoring
        if hasattr(self, "agent") and hasattr(self.agent, "agentic_extension"):
            agentic_extension = self.agent.agentic_extension
            if hasattr(agentic_extension, "monitor") and agentic_extension.monitor:
                job_id = message.content.get("job_id")
                agentic_extension.monitor.record_agent_activity(self.model.id, job_id)

        # Process the message with standard controller
        start_time = asyncio.get_event_loop().time()
        result = await self._handle_message_impl(message)
        end_time = asyncio.get_event_loop().time()

        # Record performance metrics if agentic improvements are enabled
        if hasattr(self, "agent") and hasattr(self.agent, "agentic_extension"):
            processing_time = end_time - start_time
            self.agent.record_performance(
                message.message_type,
                {
                    "processing_time": processing_time,
                    "message_type": message.message_type,
                    "job_id": message.content.get("job_id"),
                },
            )

        return result

    async def _handle_message_impl(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Implementation of message handling.
        This method should be overridden by specific controller implementations.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        # Default implementation just logs the message
        self.logger.debug(f"Received message of type {message.message_type}")
        return None
