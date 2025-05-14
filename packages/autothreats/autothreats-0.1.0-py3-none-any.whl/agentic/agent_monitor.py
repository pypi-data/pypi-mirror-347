#!/usr/bin/env python3
"""
Agent Monitoring and Recovery System for the autonomous threat modeling system.
Detects when agents are stuck or not communicating and attempts recovery.
"""

import asyncio
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Set

from ..simplified_base import Message

logger = logging.getLogger(__name__)


class AgentMonitor:
    """
    Monitors agent activity and attempts to recover from stalled or failed states.
    Detects when agents are not responding or processing messages and takes
    corrective action to ensure the system continues to function.
    """

    def __init__(self, workspace):
        """
        Initialize the agent monitoring system.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.agent_heartbeats = {}  # agent_id -> last_heartbeat_time
        self.message_counts = {}  # agent_id -> count of processed messages
        self.stalled_threshold = (
            60  # seconds without activity before considered stalled
        )
        self.critical_threshold = (
            180  # seconds without activity before considered critical
        )
        self.monitoring_task = None
        self.recovery_attempts = {}  # job_id -> count of recovery attempts
        self.max_recovery_attempts = 3  # Maximum number of recovery attempts per job
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._running = False

    async def start_monitoring(self):
        """Start the agent monitoring system"""
        if self._running:
            return

        self._running = True
        self.monitoring_task = asyncio.create_task(self._monitor_loop())
        self.logger.info("Agent monitoring system started")

    async def stop_monitoring(self):
        """Stop the agent monitoring system"""
        if not self._running:
            return

        self._running = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
            self.monitoring_task = None
        self.logger.info("Agent monitoring system stopped")

    async def _monitor_loop(self):
        """Continuously monitor agent activity"""
        while self._running:
            try:
                await self._check_agent_health()
                await asyncio.sleep(10)  # Check every 10 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in agent monitor loop: {e}", exc_info=True)
                await asyncio.sleep(30)  # Back off on error

    async def _check_agent_health(self):
        """Check if any agents are stalled"""
        current_time = time.time()
        active_jobs = self.workspace.get_data("active_jobs", {})

        for job_id, job_info in active_jobs.items():
            # Skip completed or failed jobs
            if job_info.get("status") in ["completed", "failed"]:
                continue

            # Check if job is stalled
            last_activity = job_info.get("last_activity", 0)
            if current_time - last_activity > self.stalled_threshold:
                self.logger.warning(
                    f"Job {job_id} appears stalled (inactive for {current_time - last_activity:.1f}s)"
                )

                # Check if we've exceeded recovery attempts
                if self.recovery_attempts.get(job_id, 0) >= self.max_recovery_attempts:
                    self.logger.error(
                        f"Job {job_id} has exceeded maximum recovery attempts"
                    )
                    continue

                await self._recover_stalled_job(job_id, job_info)

    async def _recover_stalled_job(self, job_id: str, job_info: Dict[str, Any]):
        """
        Attempt to recover a stalled job.

        Args:
            job_id: The ID of the stalled job
            job_info: Information about the job
        """
        self.logger.warning(f"Attempting to recover stalled job: {job_id}")

        # Get the current state of the job
        job_state = self.workspace.get_data(f"job_state_{job_id}", {})

        # Increment recovery attempts
        self.recovery_attempts[job_id] = self.recovery_attempts.get(job_id, 0) + 1
        attempt_num = self.recovery_attempts[job_id]

        # Identify which agent might be stuck
        last_agent = job_state.get("last_active_agent")
        current_stage = job_info.get("status", "unknown")

        # Update job state
        job_state["recovery_attempts"] = attempt_num
        job_state["last_recovery_time"] = time.time()
        self.workspace.store_data(f"job_state_{job_id}", job_state)

        # Send a recovery message to the orchestrator
        self.workspace.publish_message(
            Message(
                "AGENT_RECOVERY_NEEDED",
                {
                    "job_id": job_id,
                    "stalled_agent": last_agent,
                    "current_stage": current_stage,
                    "last_activity": job_info.get("last_activity"),
                    "recovery_attempt": attempt_num,
                    "recovery_strategy": self._determine_recovery_strategy(
                        job_id, attempt_num, current_stage
                    ),
                },
                "agent_monitor",
            )
        )

        self.logger.info(
            f"Sent recovery message for job {job_id}, attempt {attempt_num}"
        )

    def _determine_recovery_strategy(
        self, job_id: str, attempt_num: int, current_stage: str
    ) -> str:
        """
        Determine the appropriate recovery strategy based on the job state.

        Args:
            job_id: The ID of the job
            attempt_num: The number of recovery attempts so far
            current_stage: The current stage of the job

        Returns:
            The recovery strategy to use
        """
        if attempt_num == 1:
            return "retry_current_stage"
        elif attempt_num == 2:
            return "skip_to_next_stage"
        else:
            return "fallback_minimal_analysis"

    def record_agent_activity(self, agent_id: str, job_id: Optional[str] = None):
        """
        Record activity for an agent to update its heartbeat.

        Args:
            agent_id: The ID of the agent
            job_id: Optional job ID associated with the activity
        """
        current_time = time.time()
        self.agent_heartbeats[agent_id] = current_time

        # Update message count
        self.message_counts[agent_id] = self.message_counts.get(agent_id, 0) + 1

        # Update job last activity if provided
        if job_id:
            active_jobs = self.workspace.get_data("active_jobs", {})
            if job_id in active_jobs:
                active_jobs[job_id]["last_activity"] = current_time
                self.workspace.store_data("active_jobs", active_jobs)

                # Update job state
                job_state = self.workspace.get_data(f"job_state_{job_id}", {})
                job_state["last_active_agent"] = agent_id
                job_state["last_activity_time"] = current_time
                self.workspace.store_data(f"job_state_{job_id}", job_state)

    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get the current status of an agent.

        Args:
            agent_id: The ID of the agent

        Returns:
            Dictionary with agent status information
        """
        current_time = time.time()
        last_heartbeat = self.agent_heartbeats.get(agent_id, 0)
        time_since_heartbeat = current_time - last_heartbeat

        status = "active"
        if time_since_heartbeat > self.critical_threshold:
            status = "critical"
        elif time_since_heartbeat > self.stalled_threshold:
            status = "stalled"

        return {
            "agent_id": agent_id,
            "status": status,
            "last_heartbeat": last_heartbeat,
            "time_since_heartbeat": time_since_heartbeat,
            "message_count": self.message_counts.get(agent_id, 0),
        }

    def get_system_health(self) -> Dict[str, Any]:
        """
        Get the overall health of the system.

        Returns:
            Dictionary with system health information
        """
        agent_statuses = {
            agent_id: self.get_agent_status(agent_id)
            for agent_id in self.agent_heartbeats.keys()
        }

        # Count agents by status
        status_counts = {"active": 0, "stalled": 0, "critical": 0}
        for status in agent_statuses.values():
            status_counts[status["status"]] = status_counts.get(status["status"], 0) + 1

        # Get active jobs
        active_jobs = self.workspace.get_data("active_jobs", {})

        return {
            "timestamp": time.time(),
            "agent_count": len(agent_statuses),
            "status_counts": status_counts,
            "active_jobs": len(active_jobs),
            "recovery_attempts": sum(self.recovery_attempts.values()),
            "agent_statuses": agent_statuses,
        }
