#!/usr/bin/env python3
"""
Integration module for the multi-stage AI agent algorithm.
Connects the multi-stage agent orchestrator with the existing threat modeling system.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..simplified_base import Message, SharedWorkspace
from .multi_stage_agent import MultiStageAgentOrchestrator

logger = logging.getLogger(__name__)


class MultiStageAgentIntegration:
    """
    Integrates the multi-stage AI agent algorithm with the existing threat modeling system.
    Provides methods to start and manage multi-stage pipelines.
    """

    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the multi-stage agent integration.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        
        # Create or get the multi-stage agent orchestrator
        self.orchestrator = workspace.get_data("multi_stage_orchestrator")
        if not self.orchestrator:
            self.orchestrator = MultiStageAgentOrchestrator(workspace)
            workspace.store_data("multi_stage_orchestrator", self.orchestrator)
            self.logger.info("Created new multi-stage agent orchestrator")
        else:
            self.logger.info("Using existing multi-stage agent orchestrator")
        
        # Subscribe to relevant message types
        self._subscribe_to_messages()
        
        # Track active pipelines
        self.active_pipelines = {}
        self._tasks = []

    def _subscribe_to_messages(self):
        """Subscribe to relevant message types"""
        message_types = [
            "SYSTEM_INIT",
            "THREAT_DETECTION_START",
            "MULTI_STAGE_PIPELINE_START",
            "MULTI_STAGE_PIPELINE_COMPLETE",
            "MULTI_STAGE_PIPELINE_FAILED",
            "MULTI_STAGE_PIPELINE_STATUS",
        ]
        
        for message_type in message_types:
            self.workspace.subscribe("multi_stage_agent_integration", message_type)
        
        self.logger.info(f"Subscribed to {len(message_types)} message types")

    async def handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle messages for multi-stage agent integration.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        message_type = message.message_type
        self.logger.debug(f"Handling message of type {message_type}")
        
        if message_type == "SYSTEM_INIT":
            # System initialization, nothing to do
            return None
        
        elif message_type == "THREAT_DETECTION_START":
            # Intercept threat detection start message and start multi-stage pipeline
            return await self._handle_threat_detection_start(message)
        
        elif message_type == "MULTI_STAGE_PIPELINE_START":
            # Start a new multi-stage pipeline
            return await self._handle_pipeline_start(message)
        
        elif message_type == "MULTI_STAGE_PIPELINE_STATUS":
            # Get the status of a pipeline
            return self._handle_pipeline_status(message)
        
        elif message_type == "MULTI_STAGE_PIPELINE_COMPLETE":
            # Handle pipeline completion
            return await self._handle_pipeline_complete(message)
        
        elif message_type == "MULTI_STAGE_PIPELINE_FAILED":
            # Handle pipeline failure
            return await self._handle_pipeline_failed(message)
        
        return None

    async def _handle_threat_detection_start(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle threat detection start message by starting a multi-stage pipeline.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        self.logger.info("Intercepting threat detection start message")
        
        # Extract job ID and codebase ID from message
        job_id = message.content.get("job_id")
        codebase_id = message.content.get("codebase_id")
        
        if not job_id or not codebase_id:
            self.logger.error("Missing job_id or codebase_id in message")
            return None
        
        # Check if multi-stage analysis is enabled
        system_config = self.workspace.get_data("system_config", {})
        enable_multi_stage = system_config.get("enable_multi_stage", True)
        
        if not enable_multi_stage:
            self.logger.info("Multi-stage analysis is disabled, forwarding message")
            return None
        
        # Start a multi-stage pipeline
        pipeline_id = await self.orchestrator.start_pipeline(job_id, codebase_id)
        self.active_pipelines[pipeline_id] = {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "status": "running",
        }
        
        self.logger.info(f"Started multi-stage pipeline {pipeline_id} for job {job_id}")
        
        # Return a response to prevent the original message from being processed
        return {
            "status": "handled",
            "message": "Threat detection started via multi-stage pipeline",
            "pipeline_id": pipeline_id,
        }

    async def _handle_pipeline_start(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle pipeline start message.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        self.logger.info("Handling pipeline start message")
        
        # Extract job ID and codebase ID from message
        job_id = message.content.get("job_id")
        codebase_id = message.content.get("codebase_id")
        
        if not job_id or not codebase_id:
            self.logger.error("Missing job_id or codebase_id in message")
            return {
                "status": "error",
                "message": "Missing job_id or codebase_id in message",
            }
        
        # Start a multi-stage pipeline
        pipeline_id = await self.orchestrator.start_pipeline(job_id, codebase_id)
        self.active_pipelines[pipeline_id] = {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "status": "running",
        }
        
        self.logger.info(f"Started multi-stage pipeline {pipeline_id} for job {job_id}")
        
        return {
            "status": "success",
            "message": "Multi-stage pipeline started",
            "pipeline_id": pipeline_id,
        }

    def _handle_pipeline_status(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle pipeline status message.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        self.logger.info("Handling pipeline status message")
        
        # Extract pipeline ID from message
        pipeline_id = message.content.get("pipeline_id")
        
        if not pipeline_id:
            self.logger.error("Missing pipeline_id in message")
            return {
                "status": "error",
                "message": "Missing pipeline_id in message",
            }
        
        # Get pipeline status
        status = self.orchestrator.get_pipeline_status(pipeline_id)
        
        return {
            "status": "success",
            "message": "Pipeline status retrieved",
            "pipeline_id": pipeline_id,
            "pipeline_status": status,
        }

    async def _handle_pipeline_complete(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle pipeline complete message.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        self.logger.info("Handling pipeline complete message")
        
        # Extract pipeline ID and results from message
        pipeline_id = message.content.get("pipeline_id")
        results = message.content.get("results", {})
        
        if not pipeline_id:
            self.logger.error("Missing pipeline_id in message")
            return None
        
        # Update active pipeline status
        if pipeline_id in self.active_pipelines:
            self.active_pipelines[pipeline_id]["status"] = "completed"
        
        # Extract job ID and codebase ID
        job_id = message.content.get("job_id")
        codebase_id = message.content.get("codebase_id")
        
        if not job_id or not codebase_id:
            self.logger.error("Missing job_id or codebase_id in message")
            return None
        
        # Create and publish threat detection complete message
        self.workspace.publish_message(
            Message(
                "THREAT_DETECTION_COMPLETE",
                {
                    "job_id": job_id,
                    "codebase_id": codebase_id,
                    "vulnerabilities": results.get("vulnerabilities", []),
                    "status": "success",
                    "message": "Threat detection complete via multi-stage pipeline",
                    "next_action": "risk_scoring",
                },
                "multi_stage_agent_integration",
            )
        )
        
        self.logger.info(f"Published THREAT_DETECTION_COMPLETE message for job {job_id}")
        
        return {
            "status": "success",
            "message": "Pipeline complete message handled",
            "pipeline_id": pipeline_id,
        }

    async def _handle_pipeline_failed(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Handle pipeline failed message.

        Args:
            message: The message to handle

        Returns:
            Optional response data
        """
        self.logger.info("Handling pipeline failed message")
        
        # Extract pipeline ID and error from message
        pipeline_id = message.content.get("pipeline_id")
        error = message.content.get("error", "Unknown error")
        
        if not pipeline_id:
            self.logger.error("Missing pipeline_id in message")
            return None
        
        # Update active pipeline status
        if pipeline_id in self.active_pipelines:
            self.active_pipelines[pipeline_id]["status"] = "failed"
        
        # Extract job ID and codebase ID
        job_id = message.content.get("job_id")
        codebase_id = message.content.get("codebase_id")
        
        if not job_id or not codebase_id:
            self.logger.error("Missing job_id or codebase_id in message")
            return None
        
        # Create and publish threat detection error message
        self.workspace.publish_message(
            Message(
                "THREAT_DETECTION_ERROR",
                {
                    "job_id": job_id,
                    "codebase_id": codebase_id,
                    "status": "error",
                    "message": f"Threat detection failed: {error}",
                    "error": error,
                },
                "multi_stage_agent_integration",
            )
        )
        
        self.logger.info(f"Published THREAT_DETECTION_ERROR message for job {job_id}")
        
        return {
            "status": "success",
            "message": "Pipeline failed message handled",
            "pipeline_id": pipeline_id,
        }

    async def shutdown(self):
        """Shutdown the multi-stage agent integration"""
        self.logger.info("Shutting down multi-stage agent integration")
        
        # Shutdown the orchestrator
        await self.orchestrator.shutdown()
        
        # Cancel any running tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        self._tasks = []
        self.logger.info("Multi-stage agent integration shutdown complete")


def register_multi_stage_integration(workspace: SharedWorkspace) -> MultiStageAgentIntegration:
    """
    Register the multi-stage agent integration with the workspace.

    Args:
        workspace: The shared workspace instance

    Returns:
        The multi-stage agent integration instance
    """
    integration = MultiStageAgentIntegration(workspace)
    workspace.store_data("multi_stage_integration", integration)
    return integration