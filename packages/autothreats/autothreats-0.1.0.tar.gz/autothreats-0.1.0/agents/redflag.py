#!/usr/bin/env python3
"""
RedFlag Agent module for the autonomous threat modeling system.
Responsible for analyzing code changes using RedFlag.
"""

import asyncio
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from ..simplified_base import Agent, AgentController, Message
from ..types import MessageType
from ..utils.redflag_service import RedFlagService

logger = logging.getLogger(__name__)


class RedFlagController(AgentController):
    """Controller for RedFlag agent"""

    async def initialize(self):
        """Initialize controller resources"""
        self.logger.info("Initializing RedFlag Controller")
        self.model.update_state("status", "initialized")

        # Initialize RedFlag service
        redflag_config = self.model.config.get("redflag_config", {})
        self.redflag_service = RedFlagService(redflag_config)

    async def shutdown(self):
        """Clean up resources when shutting down"""
        self.logger.info("Shutting down RedFlag Controller")
        self.model.update_state("status", "shutdown")

    async def handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """Handle incoming messages"""
        if message.message_type == MessageType.REDFLAG_ANALYSIS_START.value:
            return await self._handle_redflag_analysis_start(message)

        self.logger.debug(f"Unhandled message type: {message.message_type}")
        return None

    def scan_codebase(self, codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Scan a codebase with RedFlag"""
        if not hasattr(self, "redflag_service"):
            error_msg = "RedFlag service not initialized"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        # Call the RedFlag service to scan the codebase
        return self.redflag_service.scan_codebase(codebase)

    async def _handle_scan_request(self, message: Message) -> Dict[str, Any]:
        """Handle scan request message"""
        job_id = message.content.get("job_id")
        codebase = message.content.get("codebase")
        codebase_id = message.content.get("codebase_id")

        if not job_id or not codebase:
            error_msg = "Missing job_id or codebase in message"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        # Scan the codebase
        result = self.scan_codebase(codebase)

        # Add job_id and codebase_id to the result
        result["job_id"] = job_id
        result["codebase_id"] = codebase_id

        return result

    async def _handle_redflag_analysis_start(self, message: Message) -> Dict[str, Any]:
        """Handle RedFlag analysis start message"""
        job_id = message.content.get("job_id")
        codebase_path = message.content.get("codebase_path")
        codebase_id = message.content.get("codebase_id")
        branch = message.content.get("branch", "main")

        if not job_id or not codebase_path:
            error_msg = "Missing job_id or codebase_path in message"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        try:
            self.logger.info(f"Starting RedFlag analysis for job {job_id}")

            # Convert to absolute path if it's relative
            abs_codebase_path = os.path.abspath(codebase_path)

            # Run RedFlag analysis on the codebase
            results = await self.redflag_service.analyze_codebase(
                abs_codebase_path, branch
            )

            if results.get("status") != "success":
                return {
                    "status": "error",
                    "message": f"RedFlag analysis failed: {results.get('message', 'Unknown error')}",
                }

            # Process results
            high_risk_changes = []
            for file_result in results["results"].get("files", []):
                if file_result.get("risk_score", 0) > 7:  # Threshold for high risk
                    high_risk_changes.append(
                        {
                            "file": file_result["file_path"],
                            "risk_score": file_result["risk_score"],
                            "risk_factors": file_result.get("risk_factors", []),
                            "recommendations": file_result.get("recommendations", []),
                        }
                    )

            # Store results in workspace
            if hasattr(self, "workspace") and self.workspace:
                self.workspace.store_data(
                    f"redflag_results_{job_id}", results["results"]
                )
                self.workspace.store_data(
                    f"high_risk_changes_{job_id}", high_risk_changes
                )

            # Send REDFLAG_ANALYSIS_COMPLETE message
            if hasattr(self, "workspace") and self.workspace:
                self.workspace.publish_message(
                    Message(
                        MessageType.REDFLAG_ANALYSIS_COMPLETE.value,
                        {
                            "job_id": job_id,
                            "codebase_id": codebase_id,
                            "high_risk_changes": high_risk_changes,
                        },
                        self.model.id,
                    )
                )

            return {
                "job_id": job_id,
                "codebase_id": codebase_id,
                "status": "success",
                "message": f"RedFlag analysis complete, found {len(high_risk_changes)} high-risk changes",
                "high_risk_changes": high_risk_changes,
            }

        except Exception as e:
            error_msg = f"Error during RedFlag analysis: {str(e)}"
            self.logger.exception(error_msg)
            return {"status": "error", "message": error_msg}


class RedFlagAgent(Agent):
    """Agent for analyzing code changes using RedFlag"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "redflag", config)
        self.logger = logging.getLogger(f"RedFlagAgent.{agent_id}")

    def _create_controller(self) -> AgentController:
        return RedFlagController(self.model)
