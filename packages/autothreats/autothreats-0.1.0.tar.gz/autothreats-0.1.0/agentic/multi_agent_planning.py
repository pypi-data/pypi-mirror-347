#!/usr/bin/env python3
"""
Multi-Agent Planning module for the autonomous threat modeling system.
Enables coordinated planning and execution of complex security analysis tasks.
"""

import asyncio
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class MultiAgentPlanning:
    """
    Enables coordinated planning and execution of complex security analysis tasks
    across multiple agents.
    """

    def __init__(self, workspace):
        """
        Initialize the multi-agent planning framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.plans = {}
        self.task_assignments = {}
        self.task_results = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    async def create_analysis_plan(
        self, codebase_model: Dict[str, Any], job_id: str
    ) -> str:
        """
        Create a security analysis plan for a codebase.

        Args:
            codebase_model: The codebase model to analyze
            job_id: The ID of the analysis job

        Returns:
            The ID of the created plan
        """
        plan_id = str(uuid.uuid4())

        # Determine analysis requirements based on codebase characteristics
        analysis_requirements = self._determine_analysis_requirements(codebase_model)

        # Create a plan with dependencies between tasks
        plan = self._create_analysis_plan(analysis_requirements, job_id)

        # Store the plan
        self.plans[plan_id] = plan
        self.workspace.store_data(f"analysis_plan_{plan_id}", plan)

        self.logger.info(f"Created analysis plan {plan_id} for job {job_id}")

        return plan_id

    def _determine_analysis_requirements(
        self, codebase_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determine analysis requirements based on codebase characteristics.

        Args:
            codebase_model: The codebase model to analyze

        Returns:
            Analysis requirements
        """
        requirements = {
            "language_analysis": True,  # Always needed
            "dependency_analysis": True,  # Always needed
            "code_graph_analysis": True,  # Always needed
            "commit_history_analysis": False,  # Optional
            "threat_scenario_analysis": True,  # Always needed
            "threat_simulation": False,  # Optional
            "detailed_vulnerability_analysis": False,  # Optional
            "priority_levels": {},
        }

        # Check if git history is available
        if codebase_model.get("has_git_history", False):
            requirements["commit_history_analysis"] = True

        # Check codebase size to determine if detailed analysis is needed
        file_count = len(codebase_model.get("files", []))
        if file_count > 1000:
            # Large codebase - prioritize critical components
            requirements["detailed_vulnerability_analysis"] = False
        else:
            # Smaller codebase - can do more detailed analysis
            requirements["detailed_vulnerability_analysis"] = True
            requirements["threat_simulation"] = True

        # Check for high-risk technologies
        technologies = codebase_model.get("technologies", {})
        languages = technologies.get("languages", {})
        frameworks = technologies.get("frameworks", [])

        # Set priority levels for different analysis types
        priority_levels = {}

        # Prioritize based on languages
        for lang, details in languages.items():
            if lang.lower() in ["javascript", "php", "python"]:
                # Higher priority for languages with more security issues
                priority_levels[lang] = "high"
            elif lang.lower() in ["java", "c#", "typescript"]:
                priority_levels[lang] = "medium"
            else:
                priority_levels[lang] = "low"

        # Prioritize based on frameworks
        for framework in frameworks:
            if framework.lower() in ["express", "django", "flask", "laravel"]:
                # Web frameworks get higher priority
                priority_levels[framework] = "high"

        requirements["priority_levels"] = priority_levels

        return requirements

    def _create_analysis_plan(
        self, requirements: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Create an analysis plan based on requirements.

        Args:
            requirements: Analysis requirements
            job_id: The ID of the analysis job

        Returns:
            The analysis plan
        """
        # Create tasks with dependencies
        tasks = []

        # Phase 1: Code ingestion and basic analysis
        tasks.append(
            {
                "id": f"task_{uuid.uuid4()}",
                "name": "code_ingestion",
                "description": "Ingest code from repository",
                "agent_type": "code_ingestion",
                "dependencies": [],
                "priority": "high",
                "status": "pending",
                "job_id": job_id,
            }
        )

        tasks.append(
            {
                "id": f"task_{uuid.uuid4()}",
                "name": "normalization",
                "description": "Normalize code representation",
                "agent_type": "normalization",
                "dependencies": ["code_ingestion"],
                "priority": "high",
                "status": "pending",
                "job_id": job_id,
            }
        )

        tasks.append(
            {
                "id": f"task_{uuid.uuid4()}",
                "name": "language_identification",
                "description": "Identify programming languages",
                "agent_type": "language_identification",
                "dependencies": ["normalization"],
                "priority": "high",
                "status": "pending",
                "job_id": job_id,
            }
        )

        # Phase 2: Parallel analysis tasks
        code_graph_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "code_graph_generation",
            "description": "Generate code graph",
            "agent_type": "code_graph",
            "dependencies": ["language_identification"],
            "priority": (
                "high" if requirements.get("code_graph_analysis", True) else "medium"
            ),
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(code_graph_task)

        dependency_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "dependency_extraction",
            "description": "Extract dependencies",
            "agent_type": "dependency_extraction",
            "dependencies": ["language_identification"],
            "priority": (
                "high" if requirements.get("dependency_analysis", True) else "medium"
            ),
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(dependency_task)

        # Optional commit history analysis
        if requirements.get("commit_history_analysis", False):
            commit_history_task = {
                "id": f"task_{uuid.uuid4()}",
                "name": "commit_history_analysis",
                "description": "Analyze commit history",
                "agent_type": "commit_history",
                "dependencies": ["code_ingestion"],
                "priority": "medium",
                "status": "pending",
                "job_id": job_id,
            }
            tasks.append(commit_history_task)
        else:
            commit_history_task = None

        # Phase 3: Context analysis
        context_dependencies = [
            "language_identification",
            "code_graph_generation",
            "dependency_extraction",
        ]
        if commit_history_task:
            context_dependencies.append("commit_history_analysis")

        context_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "context_analysis",
            "description": "Analyze application context",
            "agent_type": "context",
            "dependencies": context_dependencies,
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(context_task)

        # Phase 4: Threat analysis
        threat_scenario_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "threat_scenario",
            "description": "Generate threat scenarios",
            "agent_type": "threat_scenario",
            "dependencies": ["context_analysis"],
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(threat_scenario_task)

        # Optional threat simulation
        if requirements.get("threat_simulation", False):
            threat_simulation_task = {
                "id": f"task_{uuid.uuid4()}",
                "name": "threat_simulation",
                "description": "Simulate threat scenarios",
                "agent_type": "threat_simulation",
                "dependencies": ["threat_scenario"],
                "priority": "medium",
                "status": "pending",
                "job_id": job_id,
            }
            tasks.append(threat_simulation_task)
            threat_detection_dependencies = [
                "context_analysis",
                "threat_scenario",
                "threat_simulation",
            ]
        else:
            threat_detection_dependencies = ["context_analysis", "threat_scenario"]

        # Phase 5: Vulnerability detection and analysis
        threat_detection_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "threat_detection",
            "description": "Detect security vulnerabilities",
            "agent_type": "threat_detection",
            "dependencies": threat_detection_dependencies,
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(threat_detection_task)

        validation_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "threat_validation",
            "description": "Validate detected threats",
            "agent_type": "threat_validation",
            "dependencies": ["threat_detection"],
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(validation_task)

        # Phase 6: Risk assessment and prioritization
        risk_scoring_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "risk_scoring",
            "description": "Score security risks",
            "agent_type": "risk_scoring",
            "dependencies": ["threat_validation"],
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(risk_scoring_task)

        prioritization_task = {
            "id": f"task_{uuid.uuid4()}",
            "name": "prioritization",
            "description": "Prioritize security risks",
            "agent_type": "prioritization",
            "dependencies": ["risk_scoring"],
            "priority": "high",
            "status": "pending",
            "job_id": job_id,
        }
        tasks.append(prioritization_task)

        # Create the complete plan
        plan = {
            "id": str(uuid.uuid4()),
            "job_id": job_id,
            "created_at": time.time(),
            "updated_at": time.time(),
            "status": "created",
            "tasks": tasks,
            "requirements": requirements,
        }

        return plan

    async def assign_tasks_to_agents(self, plan_id: str) -> Dict[str, List[str]]:
        """
        Assign tasks to appropriate agents.

        Args:
            plan_id: The ID of the analysis plan

        Returns:
            Dictionary mapping agent IDs to task IDs
        """
        plan = self.plans.get(plan_id)
        if not plan:
            self.logger.error(f"Plan {plan_id} not found")
            return {}

        # Get available agents from workspace
        available_agents = {}
        for agent_id in self.workspace.get_agent_ids():
            agent_type = agent_id.split("_")[0] if "_" in agent_id else agent_id
            available_agents[agent_type] = agent_id

        # Assign tasks to agents
        assignments: Dict[str, List[str]] = {}
        for task in plan["tasks"]:
            agent_type = task["agent_type"]
            if agent_type in available_agents:
                agent_id = available_agents[agent_type]
                if agent_id not in assignments:
                    assignments[agent_id] = []
                assignments[agent_id].append(task["id"])
            else:
                self.logger.warning(
                    f"No agent available for task {task['id']} of type {agent_type}"
                )

        # Store assignments
        self.task_assignments[plan_id] = assignments
        self.workspace.store_data(f"task_assignments_{plan_id}", assignments)

        # Use a list comprehension instead of a generator to avoid type issues
        task_counts = [len(tasks) for tasks in assignments.values()]
        self.logger.info(
            f"Assigned {sum(task_counts)} tasks to {len(assignments)} agents for plan {plan_id}"
        )

        return assignments

    async def execute_plan(self, plan_id: str) -> Dict[str, Any]:
        """
        Execute an analysis plan.

        Args:
            plan_id: The ID of the analysis plan

        Returns:
            Execution results
        """
        plan = self.plans.get(plan_id)
        if not plan:
            self.logger.error(f"Plan {plan_id} not found")
            return {"status": "error", "message": f"Plan {plan_id} not found"}

        # Update plan status
        plan["status"] = "executing"
        plan["updated_at"] = time.time()
        self.workspace.store_data(f"analysis_plan_{plan_id}", plan)

        # Get task assignments
        assignments = self.task_assignments.get(plan_id)
        if not assignments:
            assignments = await self.assign_tasks_to_agents(plan_id)

        # Execute tasks in dependency order
        results = {}
        pending_tasks = {task["id"]: task for task in plan["tasks"]}
        completed_tasks = set()

        # Continue until all tasks are completed or max iterations reached
        max_iterations = 100  # Safety limit
        iteration = 0

        while pending_tasks and iteration < max_iterations:
            iteration += 1

            # Find tasks that can be executed (all dependencies satisfied)
            executable_tasks = []
            for task_id, task in list(pending_tasks.items()):
                dependencies = task["dependencies"]
                if all(
                    dep in completed_tasks
                    or dep not in [t["name"] for t in plan["tasks"]]
                    for dep in dependencies
                ):
                    executable_tasks.append(task)
                    del pending_tasks[task_id]

            if not executable_tasks:
                # No tasks can be executed, might be a dependency cycle
                self.logger.warning(
                    f"No executable tasks found in iteration {iteration}, possible dependency cycle"
                )
                break

            # Execute tasks in parallel
            execution_tasks = []
            for task in executable_tasks:
                execution_tasks.append(self._execute_task(task, plan["job_id"]))

            # Wait for all tasks to complete
            task_results = await asyncio.gather(
                *execution_tasks, return_exceptions=True
            )

            # Process results
            for i, result in enumerate(task_results):
                task = executable_tasks[i]
                if isinstance(result, Exception):
                    self.logger.error(
                        f"Error executing task {task['id']}: {str(result)}"
                    )
                    results[task["id"]] = {"status": "error", "message": str(result)}
                else:
                    results[task["id"]] = result  # type: ignore
                    completed_tasks.add(task["name"])

            # Update plan status
            plan["updated_at"] = time.time()
            self.workspace.store_data(f"analysis_plan_{plan_id}", plan)

        # Check if all tasks completed
        if not pending_tasks:
            plan["status"] = "completed"
        else:
            plan["status"] = "incomplete"
            self.logger.warning(
                f"Plan {plan_id} execution incomplete, {len(pending_tasks)} tasks remaining"
            )

        # Update plan
        plan["updated_at"] = time.time()
        self.workspace.store_data(f"analysis_plan_{plan_id}", plan)

        # Store results
        self.task_results[plan_id] = results
        self.workspace.store_data(f"task_results_{plan_id}", results)

        return {
            "plan_id": plan_id,
            "status": plan["status"],
            "completed_tasks": len(completed_tasks),
            "total_tasks": len(plan["tasks"]),
            "results": results,
        }

    async def _execute_task(self, task: Dict[str, Any], job_id: str) -> Dict[str, Any]:
        """
        Execute a single task.

        Args:
            task: The task to execute
            job_id: The ID of the analysis job

        Returns:
            Task execution result
        """
        task_id = task["id"]
        task_name = task["name"]
        agent_type = task["agent_type"]

        self.logger.info(
            f"Executing task {task_id} ({task_name}) with agent {agent_type}"
        )

        # Update task status
        task["status"] = "executing"
        task["started_at"] = time.time()

        try:
            # Determine message type based on task name
            message_type = f"{task_name.upper()}_START"

            # Create message content
            content = {"job_id": job_id, "task_id": task_id}

            # Send message to agent
            response_future: asyncio.Future[Dict[str, Any]] = asyncio.Future()

            # Register callback for response
            def handle_response(response_message):
                if not response_future.done():
                    response_future.set_result(response_message.content)

            # Register temporary subscription for response
            response_message_type = f"{task_name.upper()}_COMPLETE"
            self.workspace.subscribe_once(response_message_type, handle_response)

            # Send the message
            self.workspace.publish_message(
                message_type, content, sender="multi_agent_planning"
            )

            # Wait for response with timeout
            try:
                response = await asyncio.wait_for(
                    response_future, timeout=600
                )  # 10 minute timeout

                # Update task status
                task["status"] = "completed"
                task["completed_at"] = time.time()

                return {"task_id": task_id, "status": "completed", "result": response}

            except asyncio.TimeoutError:
                self.logger.error(f"Timeout waiting for response to task {task_id}")
                task["status"] = "timeout"
                return {
                    "task_id": task_id,
                    "status": "timeout",
                    "message": "Task execution timed out",
                }

        except Exception as e:
            self.logger.exception(f"Error executing task {task_id}: {str(e)}")
            task["status"] = "error"
            return {"task_id": task_id, "status": "error", "message": str(e)}

    def get_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a plan by ID.

        Args:
            plan_id: The ID of the plan

        Returns:
            The plan or None if not found
        """
        return self.plans.get(plan_id)

    def get_plan_status(self, plan_id: str) -> Dict[str, Any]:
        """
        Get the status of a plan.

        Args:
            plan_id: The ID of the plan

        Returns:
            Plan status information
        """
        plan = self.plans.get(plan_id)
        if not plan:
            return {"status": "not_found"}

        # Count tasks by status
        task_counts: Dict[str, int] = {}
        for task in plan["tasks"]:
            status = task.get("status", "pending")
            task_counts[status] = task_counts.get(status, 0) + 1

        return {
            "plan_id": plan_id,
            "status": plan.get("status", "unknown"),
            "created_at": plan.get("created_at"),
            "updated_at": plan.get("updated_at"),
            "job_id": plan.get("job_id"),
            "task_counts": task_counts,
            "total_tasks": len(plan["tasks"]),
        }

    async def plan_security_analysis(
        self, codebase_model: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Plan and execute a security analysis for a codebase.

        Args:
            codebase_model: The codebase model to analyze
            job_id: The ID of the analysis job

        Returns:
            Analysis results
        """
        # Create the analysis plan
        plan_id = await self.create_analysis_plan(codebase_model, job_id)

        # Assign tasks to agents
        assignments = await self.assign_tasks_to_agents(plan_id)

        # Execute the plan
        results = await self.execute_plan(plan_id)

        return {
            "plan_id": plan_id,
            "job_id": job_id,
            "status": results.get("status"),
            "completed_tasks": results.get("completed_tasks"),
            "total_tasks": results.get("total_tasks"),
        }
