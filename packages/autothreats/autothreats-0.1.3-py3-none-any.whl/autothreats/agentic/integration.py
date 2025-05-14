#!/usr/bin/env python3
"""
Integration module for agentic improvements in the autonomous threat modeling system.
Provides functions to integrate agentic improvements into the existing system.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, Optional

from ..simplified_base import Message, SharedWorkspace

logger = logging.getLogger(__name__)


class AgenticImprovementsManager:
    """
    Manages the integration of agentic agents into the threat modeling system.
    Initializes and coordinates both agentic and normal agents, using agentic versions
    when duplicates exist.
    """

    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the agentic improvements manager.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Check if LLM service exists in workspace, create a mock one if not
        llm_service = workspace.get_data("llm_service")
        if not llm_service:
            self.logger.info(
                "LLM service not found in workspace, creating a mock service"
            )
            # Create a simple mock LLM service
            from unittest.mock import MagicMock

            mock_llm = MagicMock()

            # Add async method for text generation
            async def mock_generate_text_async(prompt):
                return f"Mock response for: {prompt[:50]}..."

            mock_llm.generate_text_async = mock_generate_text_async

            # Store in workspace
            workspace.store_data("llm_service", mock_llm)
            self.logger.info("Mock LLM service created and stored in workspace")

        # Import components here to avoid circular imports
        from .adaptive_prioritization import AdaptiveAgentPrioritizer

        # Import agent integration functions
        from .agent_integration import (
            initialize_agentic_agents,
            register_agentic_agents,
            shutdown_agentic_agents,
        )
        from .agent_learning import AgentLearningSystem
        from .agent_monitor import AgentMonitor
        from .causal_reasoning import CausalReasoning
        from .collaborative_reasoning import CollaborativeReasoning
        from .context_aware_analysis import ContextAwareAnalysis
        from .context_aware_security import ContextAwareSecurity
        from .continuous_learning import ContinuousLearning
        from .explainable_security import ExplainableSecurity
        from .hierarchical_analysis import HierarchicalAnalysis
        from .knowledge_sharing import KnowledgeSharingProtocol
        from .multi_agent_planning import MultiAgentPlanning
        from .multi_stage_integration import register_multi_stage_integration

        # Initialize agentic improvement components
        self.prioritizer = AdaptiveAgentPrioritizer(workspace)
        self.reasoning = CollaborativeReasoning(workspace)
        self.monitor = AgentMonitor(workspace)
        self.knowledge = KnowledgeSharingProtocol(workspace)
        self.learning = AgentLearningSystem(workspace)
        self.causal_reasoning = CausalReasoning(workspace)
        self.multi_agent_planning = MultiAgentPlanning(workspace)
        self.explainable_security = ExplainableSecurity(workspace)
        self.continuous_learning = ContinuousLearning(workspace)
        self.context_aware_security = ContextAwareSecurity(workspace)
        self.hierarchical_analysis = HierarchicalAnalysis(workspace)
        self.context_aware_analysis = ContextAwareAnalysis(workspace)

        # Initialize multi-stage agent integration
        self.multi_stage_integration = register_multi_stage_integration(workspace)

        # Track initialization status
        self.initialized = False
        self._tasks = []
        self.agentic_agents = []

    async def initialize(self):
        """Initialize all agentic agents and components alongside normal agents"""
        if self.initialized:
            return

        self.logger.info("Initializing agentic agents alongside normal agents")

        # Start the agent monitor
        await self.monitor.start_monitoring()

        # Subscribe to relevant message types
        self._subscribe_to_messages()

        # Store components in workspace for access by agents
        self.workspace.store_data("agentic_prioritizer", self.prioritizer)
        self.workspace.store_data("agentic_reasoning", self.reasoning)
        self.workspace.store_data("agentic_monitor", self.monitor)
        self.workspace.store_data("agentic_knowledge", self.knowledge)
        self.workspace.store_data("agentic_learning", self.learning)
        self.workspace.store_data("agentic_causal_reasoning", self.causal_reasoning)
        self.workspace.store_data(
            "agentic_multi_agent_planning", self.multi_agent_planning
        )
        self.workspace.store_data(
            "agentic_explainable_security", self.explainable_security
        )
        self.workspace.store_data(
            "agentic_continuous_learning", self.continuous_learning
        )
        self.workspace.store_data(
            "agentic_context_aware_security", self.context_aware_security
        )
        self.workspace.store_data(
            "agentic_hierarchical_analysis", self.hierarchical_analysis
        )
        self.workspace.store_data(
            "agentic_context_aware_analysis", self.context_aware_analysis
        )

        # Store multi-stage integration in workspace
        self.workspace.store_data(
            "multi_stage_integration", self.multi_stage_integration
        )

        # Store manager in workspace first so agents can access it during initialization
        self.workspace.store_data("agentic_manager", self)

        # Register and initialize agentic agents
        system_config = self.workspace.get_data("system_config", {})

        # Import the functions directly
        try:
            # First try to import from the module
            from autothreats.agentic.agent_integration import (
                initialize_agentic_agents,
                initialize_all_agents,
                register_agentic_agents,
                register_all_agents,
                shutdown_agentic_agents,
                shutdown_all_agents,
            )

            self.logger.info(
                "Successfully imported agent_integration functions using absolute import"
            )
        except ImportError:
            # If that fails, try relative import
            try:
                from .agent_integration import (
                    initialize_agentic_agents,
                    initialize_all_agents,
                    register_agentic_agents,
                    register_all_agents,
                    shutdown_agentic_agents,
                    shutdown_all_agents,
                )

                self.logger.info(
                    "Successfully imported agent_integration functions using relative import"
                )
            except ImportError as e:
                self.logger.error(f"Failed to import agent_integration functions: {e}")

                # Define fallback empty functions
                def register_agentic_agents(workspace, config):
                    self.logger.warning(
                        "Using fallback empty register_agentic_agents function"
                    )
                    return []

                def register_all_agents(workspace, config):
                    self.logger.warning(
                        "Using fallback empty register_all_agents function"
                    )
                    return []

                async def initialize_agentic_agents(agents):
                    self.logger.warning(
                        "Using fallback empty initialize_agentic_agents function"
                    )
                    pass

                async def initialize_all_agents(agents):
                    self.logger.warning(
                        "Using fallback empty initialize_all_agents function"
                    )
                    pass

                async def shutdown_agentic_agents(agents):
                    self.logger.warning(
                        "Using fallback empty shutdown_agentic_agents function"
                    )
                    pass

                async def shutdown_all_agents(agents):
                    self.logger.warning(
                        "Using fallback empty shutdown_all_agents function"
                    )
                    pass

        # Register and initialize the agents
        self.all_agents = register_all_agents(self.workspace, system_config)
        await initialize_all_agents(self.all_agents)

        # Keep track of agentic agents separately
        self.agentic_agents = [
            agent for agent in self.all_agents if agent.id.startswith("agentic_")
        ]

        # Mark as initialized
        self.initialized = True
        self.logger.info(
            f"Agentic and normal agents initialized with {len(self.all_agents)} total agents ({len(self.agentic_agents)} agentic agents)"
        )

        # Delay publishing the initialization message to ensure subscribers are registered
        # We'll create a task to publish it after a short delay and store a reference to it
        init_message_task = asyncio.create_task(
            self._publish_initialization_message_with_delay()
        )
        self._tasks.append(init_message_task)

        # Add error handling for the task
        def on_init_message_done(task):
            try:
                task.result()
            except Exception as e:
                self.logger.error(f"Error publishing initialization message: {e}")

        init_message_task.add_done_callback(on_init_message_done)

    async def shutdown(self):
        """Shutdown all agentic improvement components"""
        if not self.initialized:
            return

        self.logger.info("Shutting down agentic and normal agents")

        # Shut down all agents
        if hasattr(self, "all_agents") and self.all_agents:
            await shutdown_all_agents(self.all_agents)
            self.logger.info(f"Shut down {len(self.all_agents)} total agents")
            self.all_agents = []
            self.agentic_agents = []

        # Stop the agent monitor
        await self.monitor.stop_monitoring()

        # Shut down multi-stage integration
        if hasattr(self, "multi_stage_integration"):
            await self.multi_stage_integration.shutdown()
            self.logger.info("Multi-stage integration shut down")

        # Cancel any running tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        self._tasks = []

        # Mark as not initialized
        self.initialized = False
        self.logger.info("Agentic and normal agents shut down")

    def _subscribe_to_messages(self):
        """Subscribe to relevant message types for agentic improvements"""
        # Define message types to subscribe to
        message_types = [
            "SYSTEM_INIT",
            "CODE_INGESTION_COMPLETE",
            "CODE_NORMALIZATION_COMPLETE",
            "LANGUAGE_IDENTIFICATION_COMPLETE",
            "CODE_GRAPH_GENERATION_START",
            "CODE_GRAPH_GENERATION_COMPLETE",
            "DEPENDENCY_EXTRACTION_COMPLETE",
            "COMMIT_HISTORY_ANALYSIS_COMPLETE",
            "CONTEXT_ANALYSIS_COMPLETE",
            "THREAT_DETECTION_START",
            "THREAT_DETECTION_COMPLETE",
            "THREAT_VALIDATION_COMPLETE",
            "RISK_SCORING_COMPLETE",
            "PRIORITIZATION_START",
            "PRIORITIZATION_COMPLETE",
            "THREAT_MODEL_ASSEMBLY_START",
            "THREAT_MODEL_ASSEMBLY_COMPLETE",
            "THREAT_MODEL_COMPLETE",
            "AGENT_RECOVERY_NEEDED",
            "NEW_KNOWLEDGE_AVAILABLE",
        ]

        # Create handler for each message type
        for message_type in message_types:
            self.workspace.subscribe("agentic_improvements_manager", message_type)

        self.logger.info(f"Subscribed to {len(message_types)} message types")

    async def handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle messages for agentic improvements.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        message_type = message.message_type
        self.logger.debug(f"Handling message of type {message_type}")

        # Record agent activity for monitoring
        if "agent_id" in message.content:
            agent_id = message.content["agent_id"]
            job_id = message.content.get("job_id")
            self.monitor.record_agent_activity(agent_id, job_id)

        # Check if this message should be routed to an agentic agent
        if self._should_route_to_agentic_agent(message_type):
            await self._route_message_to_agentic_agent(message)

        # Handle specific message types
        if message_type == "SYSTEM_INIT":
            # Initialize codebase analysis for adaptive prioritization
            job_id = message.content.get("job_id")
            codebase_id = message.content.get("codebase_id")
            if codebase_id:
                codebase_model = self.workspace.get_data(f"codebase_{codebase_id}")
                if codebase_model:
                    # Schedule context analysis in background
                    task = asyncio.create_task(
                        self._analyze_codebase_context(codebase_model)
                    )
                    self._tasks.append(task)

        elif message_type == "AGENT_RECOVERY_NEEDED":
            # Handle agent recovery
            job_id = message.content.get("job_id")
            stalled_agent = message.content.get("stalled_agent")
            recovery_strategy = message.content.get("recovery_strategy")

            if job_id and stalled_agent:
                # Implement recovery strategy
                await self._implement_recovery_strategy(
                    job_id, stalled_agent, recovery_strategy
                )

        return None

    async def _analyze_codebase_context(self, codebase_model):
        """
        Analyze codebase context for adaptive prioritization.

        Args:
            codebase_model: The codebase model to analyze
        """
        try:
            self.logger.info(
                "Starting codebase context analysis for adaptive prioritization"
            )

            # Get job ID from codebase model
            job_id = codebase_model.get("job_id", str(uuid.uuid4()))

            # Standard context analysis for adaptive prioritization
            context_scores = self.prioritizer.analyze_codebase_context(codebase_model)
            agent_priorities = self.prioritizer.prioritize_agents(context_scores)

            self.logger.info(
                f"Completed codebase context analysis with {len(context_scores)} context scores"
            )
            self.logger.info(f"Assigned priorities to {len(agent_priorities)} agents")

            # Store results in workspace
            self.workspace.store_data("agentic_context_scores", context_scores)
            self.workspace.store_data("agentic_agent_priorities", agent_priorities)

            # For large codebases, use hierarchical analysis
            if len(codebase_model.get("files", {})) > 1000:
                self.logger.info(
                    f"Large codebase detected ({len(codebase_model.get('files', {}))} files). Using hierarchical analysis."
                )

                # Schedule hierarchical analysis in background
                task = asyncio.create_task(
                    self.hierarchical_analysis.analyze_large_codebase(
                        codebase_model, job_id
                    )
                )
                self._tasks.append(task)

                # Schedule context-aware analysis in background
                task = asyncio.create_task(
                    self.context_aware_analysis.analyze_code_context(
                        codebase_model, job_id
                    )
                )
                self._tasks.append(task)

                self.logger.info(
                    "Scheduled hierarchical and context-aware analysis for large codebase"
                )

        except Exception as e:
            self.logger.error(f"Error analyzing codebase context: {e}", exc_info=True)

    async def _implement_recovery_strategy(
        self, job_id: str, stalled_agent: str, recovery_strategy: str
    ):
        """
        Implement a recovery strategy for a stalled agent.

        Args:
            job_id: The ID of the job
            stalled_agent: The ID of the stalled agent
            recovery_strategy: The recovery strategy to implement
        """
        self.logger.info(
            f"Implementing recovery strategy '{recovery_strategy}' for agent {stalled_agent} on job {job_id}"
        )

        if recovery_strategy == "retry_current_stage":
            # Resend the last message to the agent
            self.workspace.publish_message(
                Message(
                    "RETRY_STAGE",
                    {"job_id": job_id, "agent_id": stalled_agent},
                    "agentic_improvements_manager",
                )
            )

        elif recovery_strategy == "skip_to_next_stage":
            # Skip the current stage and move to the next one
            self.workspace.publish_message(
                Message(
                    "SKIP_STAGE",
                    {"job_id": job_id, "agent_id": stalled_agent},
                    "agentic_improvements_manager",
                )
            )

        elif recovery_strategy == "fallback_minimal_analysis":
            # Use minimal analysis to complete the job
            self.workspace.publish_message(
                Message(
                    "USE_MINIMAL_ANALYSIS",
                    {"job_id": job_id, "agent_id": stalled_agent},
                    "agentic_improvements_manager",
                )
            )

        else:
            self.logger.warning(f"Unknown recovery strategy: {recovery_strategy}")

    def _should_route_to_agentic_agent(self, message_type: str) -> bool:
        """
        Determine if a message should be routed to an agentic agent.

        Args:
            message_type: The type of message

        Returns:
            True if the message should be routed to an agentic agent, False otherwise
        """
        # Map of message types to agent types that should handle them
        message_to_agent_map = {
            "CODE_GRAPH_GENERATION_START": "code_graph",
            "THREAT_DETECTION_START": "threat_detection",
            "PRIORITIZATION_START": "prioritization",
            "THREAT_MODEL_ASSEMBLY_START": "threat_model_assembler",
        }

        return message_type in message_to_agent_map

    async def _route_message_to_agentic_agent(self, message: Message):
        """
        Route a message to the appropriate agentic agent.

        Args:
            message: The message to route
        """
        message_type = message.message_type

        # Map of message types to agent types
        message_to_agent_map = {
            "CODE_GRAPH_GENERATION_START": "code_graph",
            "THREAT_DETECTION_START": "threat_detection",
            "PRIORITIZATION_START": "prioritization",
            "THREAT_MODEL_ASSEMBLY_START": "threat_model_assembler",
        }

        agent_type = message_to_agent_map.get(message_type)
        if not agent_type:
            return

        # Find the appropriate agentic agent
        for agent in self.agentic_agents:
            if agent.model.agent_type == agent_type:
                self.logger.info(
                    f"Routing message of type {message_type} to agentic agent {agent.id}"
                )
                try:
                    # Process the message with the agentic agent
                    await agent.process_message(message)
                except Exception as e:
                    self.logger.error(
                        f"Error processing message with agentic agent {agent.id}: {e}",
                        exc_info=True,
                    )
                return

        self.logger.warning(f"No agentic agent found for message type {message_type}")

    async def _publish_initialization_message_with_delay(self):
        """Publish initialization message with a delay to ensure subscribers are registered"""
        try:
            # Wait a short time to ensure all agents are registered and subscriptions are set up
            # Use a shorter timeout to prevent hanging
            await asyncio.sleep(0.5)

            self.logger.info(
                "Publishing delayed AGENTIC_IMPROVEMENTS_INITIALIZED message"
            )

            # Publish initialization message
            self.workspace.publish_message(
                Message(
                    "AGENTIC_IMPROVEMENTS_INITIALIZED",
                    {
                        "components": [
                            "adaptive_prioritization",
                            "collaborative_reasoning",
                            "agent_monitor",
                            "knowledge_sharing",
                            "agent_learning",
                            "causal_reasoning",
                            "multi_agent_planning",
                            "explainable_security",
                            "continuous_learning",
                            "context_aware_security",
                            "hierarchical_analysis",
                            "context_aware_analysis",
                        ]
                    },
                    "agentic_improvements_manager",
                )
            )
        except Exception as e:
            self.logger.error(f"Error publishing initialization message: {e}")
