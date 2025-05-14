#!/usr/bin/env python3
"""
Simplified orchestrator for the autonomous threat modeling system.
Uses async patterns instead of message-based communication.
"""

import asyncio
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Type

from .agentic.simplified_adaptive_prioritization import SimplifiedAdaptivePrioritization
from .agentic.simplified_context_aware_security import SimplifiedContextAwareSecurity
from .agentic.simplified_explainable_security import SimplifiedExplainableSecurity
from .agentic.simplified_hierarchical_analysis import SimplifiedHierarchicalAnalysis
from .agents.simplified_threat_detection import SimplifiedThreatDetectionAgent
from .simplified_base import Agent, SharedWorkspace

logger = logging.getLogger(__name__)


class SimplifiedOrchestrator:
    """
    Simplified orchestrator for coordinating threat modeling agents.
    Uses direct async calls instead of message passing.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestrator.

        Args:
            config: Optional configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger("SimplifiedOrchestrator")
        self.workspace = None
        self.agents = {}
        self.running = False

        # Generate a unique workspace ID
        self.workspace_id = self.config.get("workspace_id", f"workspace_{uuid.uuid4()}")

        # Configure logging
        log_level = self.config.get("log_level", "INFO")
        if isinstance(log_level, str):
            log_level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.logger.info(
            f"Simplified Orchestrator initialized with workspace ID: {self.workspace_id}"
        )

    async def initialize(self):
        """Initialize the orchestrator and all agents"""
        self.logger.info("Initializing orchestrator...")

        # Create workspace if not already provided
        if self.workspace is None:
            self.logger.info(f"Creating new workspace with ID: {self.workspace_id}")
            self.workspace = SharedWorkspace(self.workspace_id)
            # Start workspace
            await self.workspace.start()
        else:
            self.logger.info("Using existing workspace")
            # If workspace is not running, start it
            if not getattr(self.workspace, "running", False):
                await self.workspace.start()

        # Check for custom agents
        custom_agents = (
            self.workspace.agents if hasattr(self.workspace, "agents") else {}
        )
        has_custom_agents = (
            "security_scanner" in custom_agents or "code_analyzer" in custom_agents
        )

        if has_custom_agents:
            self.logger.info(
                "Custom agents detected in workspace, skipping default agent creation"
            )
            # Add custom agents to our agents dictionary for tracking
            for agent_id, agent in custom_agents.items():
                if agent_id not in self.agents:
                    self.agents[agent_id] = agent
                    self.logger.info(f"Tracking custom agent: {agent_id}")
        else:
            # Create and register default agents
            self.logger.info("No custom agents detected, creating default agents")
            await self._create_agents()

        # Initialize agentic components
        await self._initialize_agentic_components()

        self.running = True
        self.logger.info("Orchestrator initialization complete")

    async def _create_agents(self):
        """Create and register all required agents"""
        self.logger.info("Creating default agents...")

        # Check if agentic improvements are enabled
        enable_agentic = self.config.get("system", {}).get(
            "enable_agentic_improvements", False
        )
        self.logger.info(f"Agentic improvements enabled: {enable_agentic}")

        # Create standard threat detection agent regardless of agentic mode
        threat_detection_config = self.config.get("threat_detection", {})
        threat_detection_agent = SimplifiedThreatDetectionAgent(
            agent_id="threat_detection_agent", config=threat_detection_config
        )
        self.workspace.register_agent(threat_detection_agent)
        self.agents["threat_detection"] = threat_detection_agent

        if enable_agentic:
            # Create agentic agents
            self.logger.info("Creating agentic agents...")

            # Import agentic agents
            # All agentic agents have been removed
            # All agentic agents have been removed
            self.logger.info(
                "Agentic agents have been removed, but standard agents are still available"
            )

        # Multi-stage agent has been removed

        # Initialize all agents
        init_tasks = []
        for agent_id, agent in self.agents.items():
            self.logger.info(f"Initializing agent: {agent_id}")
            init_tasks.append(agent.initialize())

        # Wait for all agents to initialize
        await asyncio.gather(*init_tasks)

        self.logger.info(f"Created and initialized {len(self.agents)} agents")

    async def _initialize_agentic_components(self):
        """Initialize agentic components"""
        self.logger.info("Initializing agentic components...")

        # Create context-aware security component
        context_aware_security = SimplifiedContextAwareSecurity(self.workspace)
        self.workspace.store_data("context_aware_security", context_aware_security)

        # Create adaptive prioritization component
        adaptive_prioritization = SimplifiedAdaptivePrioritization(self.workspace)
        self.workspace.store_data("adaptive_prioritization", adaptive_prioritization)

        # Create hierarchical analysis component
        hierarchical_analysis = SimplifiedHierarchicalAnalysis(self.workspace)
        self.workspace.store_data("hierarchical_analysis", hierarchical_analysis)

        # Create explainable security component
        explainable_security = SimplifiedExplainableSecurity(self.workspace)
        self.workspace.store_data("explainable_security", explainable_security)

        self.logger.info("Agentic components initialized")

    async def shutdown(self):
        """Shutdown the orchestrator and all agents"""
        self.logger.info("Shutting down orchestrator...")

        # Stop workspace
        if self.workspace:
            await self.workspace.stop()

        # Shutdown all agents
        shutdown_tasks = []
        for agent_id, agent in self.agents.items():
            self.logger.info(f"Shutting down agent: {agent_id}")
            shutdown_tasks.append(agent.shutdown())

        # Wait for all agents to shutdown
        await asyncio.gather(*shutdown_tasks)

        self.running = False
        self.logger.info("Orchestrator shutdown complete")

    async def process_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a complete threat modeling job

        Args:
            job_data: Job data including codebase and configuration

        Returns:
            Job results
        """
        if not self.running:
            raise RuntimeError("Orchestrator is not running. Call initialize() first.")

        self.logger.info(f"Processing job: {job_data.get('job_id')}")

        # Check if a specific agent is requested
        if (
            job_data.get("agent_id")
            and job_data.get("agent_id") in self.workspace.agents
        ):
            agent_id = job_data.get("agent_id")
            task_type = job_data.get("task_type", "threat_detection")
            self.logger.info(
                f"Routing job directly to agent: {agent_id} with task type: {task_type}"
            )

            try:
                result = await self.workspace.process_agent_task(
                    agent_id, task_type, job_data
                )

                # If the agent returns an error, propagate it up
                if result.get("status") == "error":
                    return {
                        "job_id": job_data.get("job_id"),
                        "status": "error",
                        "message": f"Agent {agent_id} failed: {result.get('message')}",
                        "details": result.get("details", ""),
                        "results": {agent_id: result},
                    }

                return {
                    "job_id": job_data.get("job_id"),
                    "status": "success",
                    "message": f"Job processed by agent {agent_id}",
                    "results": {agent_id: result},
                }
            except Exception as e:
                error_msg = f"Error processing job with agent {agent_id}: {str(e)}"
                self.logger.error(error_msg)
                return {
                    "job_id": job_data.get("job_id"),
                    "status": "error",
                    "message": error_msg,
                    "details": str(e),
                }

        # Validate job data
        if not job_data.get("job_id"):
            job_data["job_id"] = str(uuid.uuid4())

        if not job_data.get("codebase_id") and job_data.get("codebase"):
            job_data["codebase_id"] = f"codebase_{uuid.uuid4()}"

        job_id = job_data["job_id"]
        codebase_id = job_data.get("codebase_id")
        codebase = job_data.get("codebase")

        # Store codebase in workspace if provided
        if codebase and codebase_id:
            workspace_key = (
                codebase_id
                if codebase_id.startswith("codebase_")
                else f"codebase_{codebase_id}"
            )
            self.workspace.store_data(workspace_key, codebase)
            self.logger.info(f"Stored codebase with key: {workspace_key}")

        # Process the job through the pipeline
        try:
            # Check if agentic improvements are enabled (in config or job data)
            enable_agentic = self.config.get("system", {}).get(
                "enable_agentic_improvements", False
            ) or job_data.get("enable_agentic", False)
            enable_multi_stage = self.config.get(
                "enable_multi_stage", False
            ) or job_data.get("enable_multi_stage", False)

            # Store job data in workspace for knowledge sharing
            self.workspace.store_data(f"job_data_{job_id}", job_data)

            # Check if the task type is supported
            task_type = job_data.get("task_type", "threat_detection")
            if task_type not in [
                "threat_detection",
                "threat_detection_with_prioritization",
                "multi_stage_analysis",
                "agentic_threat_detection",
                "agentic_multi_stage_analysis",
                "scan_security",
                "analyze_code",
            ]:
                self.logger.error(f"Unsupported task type: {task_type}")
                return {
                    "job_id": job_id,
                    "status": "error",
                    "message": f"Unsupported task type: {task_type}",
                    "details": "This task type is not supported by the orchestrator",
                }

            if enable_agentic:
                # Use agentic agents for processing
                self.logger.info(f"Starting agentic threat detection for job {job_id}")

                # Code graph generation has been removed

                # Run threat detection with agentic agent
                threat_detection_result = await self.workspace.process_agent_task(
                    agent_id="threat_detection_agent",
                    task_type="threat_detection",
                    task_data=job_data,
                )

                # Store the threat detection result in the workspace for task chaining
                self.workspace.store_data(
                    f"threat_detection_result_{job_id}", threat_detection_result
                )

                # Store knowledge items for sharing between agents
                if threat_detection_result.get("status") == "success":
                    # Store vulnerabilities for knowledge sharing
                    vulnerabilities = threat_detection_result.get("vulnerabilities", [])
                    self.workspace.store_data(
                        f"knowledge_vulnerabilities_{job_id}", vulnerabilities
                    )

                    # Run prioritization if available
                    if "agentic_prioritization" in self.agents and vulnerabilities:
                        self.logger.info(
                            f"Running agentic prioritization for job {job_id}"
                        )
                        prioritization_data = {
                            "job_id": job_id,
                            "codebase_id": codebase_id,
                            "vulnerabilities": vulnerabilities,
                        }
                        prioritization_result = await self.workspace.process_agent_task(
                            agent_id="agentic_prioritization_agent",
                            task_type="prioritize_vulnerabilities",
                            task_data=prioritization_data,
                        )

                        if prioritization_result.get("status") == "success":
                            # Update vulnerabilities with prioritization
                            prioritized_vulnerabilities = prioritization_result.get(
                                "prioritized_vulnerabilities", []
                            )
                            threat_detection_result["vulnerabilities"] = (
                                prioritized_vulnerabilities
                            )
                            self.workspace.store_data(
                                f"knowledge_prioritized_vulnerabilities_{job_id}",
                                prioritized_vulnerabilities,
                            )
                            self.logger.info(
                                f"Vulnerabilities prioritized successfully for job {job_id}"
                            )
                        else:
                            self.logger.warning(
                                f"Prioritization failed: {prioritization_result.get('message')}"
                            )

                    # Run threat model assembly if available
                    if "agentic_threat_model" in self.agents:
                        self.logger.info(f"Assembling threat model for job {job_id}")
                        threat_model_data = {
                            "job_id": job_id,
                            "codebase_id": codebase_id,
                            "vulnerabilities": threat_detection_result.get(
                                "vulnerabilities", []
                            ),
                            "code_graph": job_data.get("code_graph", {}),
                        }
                        threat_model_result = await self.workspace.process_agent_task(
                            agent_id="agentic_threat_model_agent",
                            task_type="assemble_threat_model",
                            task_data=threat_model_data,
                        )

                        if threat_model_result.get("status") == "success":
                            # Add threat model to result
                            threat_detection_result["threat_model"] = (
                                threat_model_result.get("threat_model", {})
                            )
                            self.workspace.store_data(
                                f"knowledge_threat_model_{job_id}",
                                threat_model_result.get("threat_model", {}),
                            )
                            self.logger.info(
                                f"Threat model assembled successfully for job {job_id}"
                            )
                        else:
                            self.logger.warning(
                                f"Threat model assembly failed: {threat_model_result.get('message')}"
                            )
            elif enable_multi_stage and "multi_stage" in self.agents:
                # Use multi-stage agent for threat detection
                self.logger.info(
                    f"Starting multi-stage threat detection for job {job_id}"
                )
                threat_detection_result = await self.workspace.process_agent_task(
                    agent_id="multi_stage_agent",
                    task_type="threat_detection",
                    task_data=job_data,
                )

                # Store the threat detection result in the workspace for task chaining
                self.workspace.store_data(
                    f"threat_detection_result_{job_id}", threat_detection_result
                )
            else:
                # Check if a custom agent is specified
                if (
                    job_data.get("agent_id")
                    and job_data.get("agent_id") in self.workspace.agents
                ):
                    agent_id = job_data.get("agent_id")
                    self.logger.info(f"Using custom agent {agent_id} for job {job_id}")
                    threat_detection_result = await self.workspace.process_agent_task(
                        agent_id=agent_id, task_type=task_type, task_data=job_data
                    )

                    # Store the result in the workspace with an appropriate key
                    if task_type == "scan_security":
                        self.workspace.store_data(
                            f"security_scan_result_{job_id}", threat_detection_result
                        )
                    elif task_type == "analyze_code":
                        self.workspace.store_data(
                            f"code_analysis_result_{job_id}", threat_detection_result
                        )
                    else:
                        self.workspace.store_data(
                            f"task_result_{job_id}", threat_detection_result
                        )
                else:
                    # Use standard threat detection agent
                    self.logger.info(
                        f"Starting standard threat detection for job {job_id}"
                    )
                    threat_detection_result = await self.workspace.process_agent_task(
                        agent_id="threat_detection_agent",
                        task_type="threat_detection",
                        task_data=job_data,
                    )

                    # Store the threat detection result in the workspace for task chaining
                    self.workspace.store_data(
                        f"threat_detection_result_{job_id}", threat_detection_result
                    )

            if threat_detection_result.get("status") != "success":
                self.logger.error(
                    f"Threat detection failed: {threat_detection_result.get('message')}"
                )
                return {
                    "job_id": job_id,
                    "status": "error",
                    "message": f"Threat detection failed: {threat_detection_result.get('message')}",
                    "results": {"threat_detection": threat_detection_result},
                }

            # Store vulnerabilities in workspace
            vulnerabilities = threat_detection_result.get("vulnerabilities", [])
            self.workspace.store_data(f"vulnerabilities_{job_id}", vulnerabilities)
            self.logger.info(f"Found {len(vulnerabilities)} vulnerabilities")

            # Apply post-processing to vulnerabilities
            processed_vulnerabilities = await self._post_process_vulnerabilities(
                vulnerabilities, job_id, codebase_id
            )

            # Update threat detection result with processed vulnerabilities
            threat_detection_result["vulnerabilities"] = processed_vulnerabilities

            # Return results
            # Special case for threat_detection_with_prioritization task type
            task_type = job_data.get("task_type", "threat_detection")
            if task_type == "threat_detection_with_prioritization":
                # For task chaining test, include vulnerabilities at the top level
                return {
                    "job_id": job_id,
                    "status": "success",
                    "message": "Job processing complete",
                    "vulnerabilities": processed_vulnerabilities,
                    "prioritized_vulnerabilities": processed_vulnerabilities,  # These are already prioritized
                    "results": {
                        "threat_detection": threat_detection_result,
                        "vulnerabilities_count": len(processed_vulnerabilities),
                        "executive_summary": threat_detection_result.get(
                            "executive_summary", "No executive summary available."
                        ),
                    },
                }
            else:
                # Standard response format
                return {
                    "job_id": job_id,
                    "status": "success",
                    "message": "Job processing complete",
                    "results": {
                        "threat_detection": threat_detection_result,
                        "vulnerabilities_count": len(processed_vulnerabilities),
                        "executive_summary": threat_detection_result.get(
                            "executive_summary", "No executive summary available."
                        ),
                    },
                }

        except Exception as e:
            self.logger.exception(f"Error processing job {job_id}: {str(e)}")
            return {
                "job_id": job_id,
                "status": "error",
                "message": f"Error processing job: {str(e)}",
            }

    async def _post_process_vulnerabilities(
        self, vulnerabilities: List[Dict[str, Any]], job_id: str, codebase_id: str
    ) -> List[Dict[str, Any]]:
        """
        Apply post-processing to vulnerabilities

        Args:
            vulnerabilities: List of vulnerabilities
            job_id: Job ID
            codebase_id: Codebase ID

        Returns:
            Processed vulnerabilities
        """
        processed_vulnerabilities = vulnerabilities

        # Get agentic components
        context_aware_security = self.workspace.get_data("context_aware_security")
        adaptive_prioritization = self.workspace.get_data("adaptive_prioritization")
        explainable_security = self.workspace.get_data("explainable_security")

        # Apply context-aware security if not already applied
        if context_aware_security and not any(
            "in_security_boundary" in vuln for vuln in vulnerabilities
        ):
            try:
                # Get codebase
                codebase = self.workspace.get_data(
                    codebase_id
                    if codebase_id.startswith("codebase_")
                    else f"codebase_{codebase_id}"
                )

                # Analyze security context
                security_context = (
                    await context_aware_security.analyze_security_context(
                        codebase, job_id
                    )
                )

                # Enhance vulnerabilities with context
                processed_vulnerabilities = (
                    await context_aware_security.enhance_vulnerability_detection(
                        processed_vulnerabilities, security_context
                    )
                )

                self.logger.info("Applied context-aware security to vulnerabilities")
            except Exception as e:
                self.logger.error(f"Error applying context-aware security: {e}")

        # Apply adaptive prioritization if not already applied
        if adaptive_prioritization and not any(
            "priority" in vuln for vuln in processed_vulnerabilities
        ):
            try:
                # Prioritize vulnerabilities
                processed_vulnerabilities = (
                    await adaptive_prioritization.prioritize_vulnerabilities(
                        processed_vulnerabilities, job_id
                    )
                )

                self.logger.info("Applied adaptive prioritization to vulnerabilities")
            except Exception as e:
                self.logger.error(f"Error applying adaptive prioritization: {e}")

        # Apply explainable security if not already applied
        if explainable_security and not any(
            "detailed_explanation" in vuln for vuln in processed_vulnerabilities
        ):
            try:
                # Add detailed explanations
                processed_vulnerabilities = (
                    await explainable_security.explain_vulnerabilities(
                        processed_vulnerabilities, job_id
                    )
                )

                self.logger.info("Applied explainable security to vulnerabilities")
            except Exception as e:
                self.logger.error(f"Error applying explainable security: {e}")

        return processed_vulnerabilities

    async def detect_threats(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run only the threat detection phase

        Args:
            job_data: Job data including codebase and configuration

        Returns:
            Threat detection results
        """
        if not self.running:
            raise RuntimeError("Orchestrator is not running. Call initialize() first.")

        self.logger.info(f"Running threat detection for job: {job_data.get('job_id')}")

        # Validate job data
        if not job_data.get("job_id"):
            job_data["job_id"] = str(uuid.uuid4())

        if not job_data.get("codebase_id") and job_data.get("codebase"):
            job_data["codebase_id"] = f"codebase_{uuid.uuid4()}"

        job_id = job_data["job_id"]

        # Process threat detection
        try:
            # Check if agentic improvements are enabled
            enable_agentic = self.config.get("system", {}).get(
                "enable_agentic_improvements", False
            )
            enable_multi_stage = self.config.get("enable_multi_stage", False)

            # Store job data in workspace for knowledge sharing
            self.workspace.store_data(f"job_data_{job_id}", job_data)

            if enable_agentic:
                # Use agentic agents for processing
                self.logger.info(f"Starting agentic threat detection for job {job_id}")

                # Code graph generation has been removed

                # Run threat detection with agentic agent
                threat_detection_result = await self.workspace.process_agent_task(
                    agent_id="threat_detection_agent",
                    task_type="threat_detection",
                    task_data=job_data,
                )
            # Multi-stage agent has been removed
            else:
                # Use standard threat detection agent
                self.logger.info(f"Starting standard threat detection for job {job_id}")
                threat_detection_result = await self.workspace.process_agent_task(
                    agent_id="threat_detection_agent",
                    task_type="threat_detection",
                    task_data=job_data,
                )

            return threat_detection_result

        except Exception as e:
            self.logger.exception(
                f"Error in threat detection for job {job_id}: {str(e)}"
            )
            return {
                "job_id": job_id,
                "status": "error",
                "message": f"Error in threat detection: {str(e)}",
            }


async def run_orchestrator(
    config: Dict[str, Any], job_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Helper function to run the orchestrator for a single job

    Args:
        config: Orchestrator configuration
        job_data: Job data

    Returns:
        Job results
    """
    # Create and initialize orchestrator
    orchestrator = SimplifiedOrchestrator(config)
    await orchestrator.initialize()

    try:
        # Process job
        result = await orchestrator.process_job(job_data)
        return result
    finally:
        # Ensure orchestrator is shut down
        await orchestrator.shutdown()


if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(
        description="Run the simplified threat modeling orchestrator"
    )
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--job", help="Path to job data file")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    parser.add_argument(
        "--enable-multi-stage", action="store_true", help="Enable multi-stage agent"
    )

    args = parser.parse_args()

    # Load configuration
    config = {
        "log_level": args.log_level,
        "enable_multi_stage": args.enable_multi_stage,
    }
    if args.config:
        with open(args.config, "r") as f:
            config.update(json.load(f))

    # Load job data
    job_data = {}
    if args.job:
        with open(args.job, "r") as f:
            job_data = json.load(f)
    else:
        print("No job data provided. Use --job to specify a job data file.")
        sys.exit(1)

    # Run orchestrator
    result = asyncio.run(run_orchestrator(config, job_data))

    # Output results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))
