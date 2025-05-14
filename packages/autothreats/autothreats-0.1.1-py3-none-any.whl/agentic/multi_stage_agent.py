#!/usr/bin/env python3
"""
Multi-Stage AI Agent Algorithm for the autonomous threat modeling system.
Coordinates multiple specialized agents to work together in a pipeline for enhanced threat detection.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Message, SharedWorkspace
from .agent_extension import AgenticAgentExtension
from .causal_reasoning import CausalReasoning
from .collaborative_reasoning import CollaborativeReasoning
from .context_aware_analysis import ContextAwareAnalysis
from .knowledge_sharing import KnowledgeSharingProtocol

logger = logging.getLogger(__name__)


class MultiStageAgentOrchestrator:
    """
    Orchestrates a multi-stage AI agent pipeline for enhanced threat detection.
    Coordinates specialized agents to work together in a sequential and parallel manner.
    """

    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the multi-stage agent orchestrator.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.pipeline_stages = []
        self.active_pipelines = {}
        self.stage_results = {}
        self.pipeline_status = {}
        self._tasks = []

        # Get components from workspace
        self.context_analysis = workspace.get_data("agentic_context_aware_analysis")
        if not self.context_analysis:
            self.context_analysis = ContextAwareAnalysis(workspace)
            workspace.store_data("agentic_context_aware_analysis", self.context_analysis)

        self.causal_reasoning = workspace.get_data("agentic_causal_reasoning")
        if not self.causal_reasoning:
            self.causal_reasoning = CausalReasoning(workspace)
            workspace.store_data("agentic_causal_reasoning", self.causal_reasoning)

        self.collaborative_reasoning = workspace.get_data("agentic_reasoning")
        if not self.collaborative_reasoning:
            self.collaborative_reasoning = CollaborativeReasoning(workspace)
            workspace.store_data("agentic_reasoning", self.collaborative_reasoning)

        self.knowledge_sharing = workspace.get_data("agentic_knowledge")
def _define_pipeline_stages(self):
        """Define the stages of the multi-stage agent pipeline"""
        self.pipeline_stages = [
            {
                "id": "context_analysis",
                "name": "Context Analysis",
                "description": "Analyze the codebase context to understand structure and relationships",
                "agent_type": "context",
                "dependencies": [],
                "parallel": False,
            },
            {
                "id": "code_graph_generation",
                "name": "Code Graph Generation",
                "description": "Generate a graph representation of the code",
                "agent_type": "code_graph",
                "dependencies": ["context_analysis"],
                "parallel": False,
            },
            {
                "id": "vulnerability_pattern_matching",
                "name": "Vulnerability Pattern Matching",
                "description": "Identify potential vulnerabilities using pattern matching",
                "agent_type": "threat_detection",
                "dependencies": ["code_graph_generation"],
                "parallel": True,
            },
            {
                "id": "semantic_vulnerability_analysis",
                "name": "Semantic Vulnerability Analysis",
                "description": "Analyze code semantics to identify complex vulnerabilities",
                "agent_type": "threat_detection",
                "dependencies": ["code_graph_generation"],
                "parallel": True,
            },
            {
                "id": "cross_component_analysis",
                "name": "Cross-Component Analysis",
                "description": "Analyze interactions between components for vulnerabilities",
                "agent_type": "threat_detection",
                "dependencies": ["code_graph_generation"],
                "parallel": True,
            },
            {
                "id": "vulnerability_validation",
                "name": "Vulnerability Validation",
                "description": "Validate identified vulnerabilities to reduce false positives",
                "agent_type": "threat_validation",
                "dependencies": [
                    "vulnerability_pattern_matching",
                    "semantic_vulnerability_analysis",
                    "cross_component_analysis",
                ],
                "parallel": False,
            },
            {
                "id": "causal_analysis",
                "name": "Causal Analysis",
                "description": "Analyze causal relationships between vulnerabilities",
                "agent_type": "causal_reasoning",
                "dependencies": ["vulnerability_validation"],
                "parallel": False,
            },
            {
                "id": "risk_scoring",
                "name": "Risk Scoring",
                "description": "Assign risk scores to validated vulnerabilities",
                "agent_type": "risk_scoring",
                "dependencies": ["vulnerability_validation", "causal_analysis"],
                "parallel": False,
            },
            {
                "id": "prioritization",
                "name": "Prioritization",
                "description": "Prioritize vulnerabilities based on risk and context",
                "agent_type": "prioritization",
                "dependencies": ["risk_scoring"],
                "parallel": False,
            },
            {
                "id": "threat_model_assembly",
                "name": "Threat Model Assembly",
                "description": "Assemble the final threat model",
                "agent_type": "threat_model_assembler",
                "dependencies": ["prioritization"],
                "parallel": False,
            },
        ]

        self.logger.info(f"Defined {len(self.pipeline_stages)} pipeline stages")

    async def start_pipeline(self, job_id: str, codebase_id: str) -> str:
        """
        Start a new multi-stage agent pipeline.

        Args:
            job_id: The ID of the job
            codebase_id: The ID of the codebase to analyze

        Returns:
            The ID of the pipeline
        """
        pipeline_id = str(uuid.uuid4())
        self.logger.info(f"Starting pipeline {pipeline_id} for job {job_id}")

        # Initialize pipeline status
        self.pipeline_status[pipeline_id] = {
            "id": pipeline_id,
            "job_id": job_id,
            "codebase_id": codebase_id,
            "status": "running",
            "current_stage": None,
            "completed_stages": [],
            "failed_stages": [],
            "start_time": asyncio.get_event_loop().time(),
            "end_time": None,
        }

        # Initialize stage results
        self.stage_results[pipeline_id] = {}

        # Start the pipeline
        task = asyncio.create_task(self._run_pipeline(pipeline_id, job_id, codebase_id))
        self._tasks.append(task)

        # Add error handling for the task
async def _run_pipeline(self, pipeline_id: str, job_id: str, codebase_id: str):
        """
        Run the multi-stage agent pipeline.

        Args:
            pipeline_id: The ID of the pipeline
            job_id: The ID of the job
            codebase_id: The ID of the codebase to analyze
        """
        self.logger.info(f"Running pipeline {pipeline_id}")

        try:
            # Get the codebase
            codebase = self.workspace.get_data(f"codebase_{codebase_id}")
            if not codebase:
                raise ValueError(f"Codebase {codebase_id} not found")

            # Execute each stage in the pipeline
            for stage in self.pipeline_stages:
                stage_id = stage["id"]
                self.logger.info(f"Starting stage {stage_id} for pipeline {pipeline_id}")

                # Update pipeline status
                self.pipeline_status[pipeline_id]["current_stage"] = stage_id

                # Check if dependencies are satisfied
                dependencies_satisfied = True
                for dependency in stage["dependencies"]:
                    if dependency not in self.pipeline_status[pipeline_id]["completed_stages"]:
                        dependencies_satisfied = False
                        self.logger.warning(
                            f"Dependency {dependency} not satisfied for stage {stage_id}"
                        )
                        break

                if not dependencies_satisfied:
                    self.logger.error(
                        f"Dependencies not satisfied for stage {stage_id}, skipping"
                    )
                    self.pipeline_status[pipeline_id]["failed_stages"].append(stage_id)
                    continue

                # Execute the stage
                try:
                    result = await self._execute_stage(
                        stage, pipeline_id, job_id, codebase_id, codebase
                    )
                    self.stage_results[pipeline_id][stage_id] = result
                    self.pipeline_status[pipeline_id]["completed_stages"].append(stage_id)
                    self.logger.info(f"Completed stage {stage_id} for pipeline {pipeline_id}")
                except Exception as e:
                    self.logger.error(f"Error executing stage {stage_id}: {e}")
                    self.pipeline_status[pipeline_id]["failed_stages"].append(stage_id)
                    # Continue with the next stage if this one fails

            # Update pipeline status
            self.pipeline_status[pipeline_id]["current_stage"] = None
            self.pipeline_status[pipeline_id]["status"] = "completed"
            self.pipeline_status[pipeline_id]["end_time"] = asyncio.get_event_loop().time()

            # Publish pipeline completion message
            self.workspace.publish_message(
                Message(
                    "MULTI_STAGE_PIPELINE_COMPLETE",
                    {
                        "pipeline_id": pipeline_id,
                        "job_id": job_id,
                        "codebase_id": codebase_id,
                        "status": "completed",
                        "results": self._get_pipeline_results(pipeline_id),
                    },
                    "multi_stage_agent_orchestrator",
                )
            )

            self.logger.info(f"Pipeline {pipeline_id} completed successfully")

        except Exception as e:
            self.logger.error(f"Error running pipeline {pipeline_id}: {e}")
            self.pipeline_status[pipeline_id]["status"] = "failed"
            self.pipeline_status[pipeline_id]["error"] = str(e)
            self.pipeline_status[pipeline_id]["end_time"] = asyncio.get_event_loop().time()

            # Publish pipeline failure message
            self.workspace.publish_message(
                Message(
                    "MULTI_STAGE_PIPELINE_FAILED",
                    {
                        "pipeline_id": pipeline_id,
                        "job_id": job_id,
                        "codebase_id": codebase_id,
                        "status": "failed",
                        "error": str(e),
                    },
                    "multi_stage_agent_orchestrator",
                )
            )

    async def _execute_stage(
        self,
        stage: Dict[str, Any],
        pipeline_id: str,
        job_id: str,
        codebase_id: str,
        codebase: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a stage in the pipeline.

        Args:
            stage: The stage to execute
            pipeline_id: The ID of the pipeline
            job_id: The ID of the job
            codebase_id: The ID of the codebase
            codebase: The codebase to analyze

        Returns:
            The result of the stage execution
        """
        stage_id = stage["id"]
        agent_type = stage["agent_type"]

        self.logger.info(f"Executing stage {stage_id} with agent type {agent_type}")

        # Get previous stage results if needed
        previous_results = {}
        for dependency in stage["dependencies"]:
            if dependency in self.stage_results.get(pipeline_id, {}):
                previous_results[dependency] = self.stage_results[pipeline_id][dependency]

        # Create message content
        message_content = {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "pipeline_id": pipeline_id,
            "stage_id": stage_id,
            "previous_results": previous_results,
        }

        # Determine message type based on agent type
        message_type_map = {
            "context": "CONTEXT_ANALYSIS_START",
            "code_graph": "CODE_GRAPH_GENERATION_START",
            "threat_detection": "THREAT_DETECTION_START",
            "threat_validation": "THREAT_VALIDATION_START",
            "causal_reasoning": "CAUSAL_ANALYSIS_START",
            "risk_scoring": "RISK_SCORING_START",
            "prioritization": "PRIORITIZATION_START",
            "threat_model_assembler": "THREAT_MODEL_ASSEMBLY_START",
        }

        message_type = message_type_map.get(agent_type, f"{stage_id.upper()}_START")

        # Create and publish message
        message = Message(
            message_type,
            message_content,
            "multi_stage_agent_orchestrator",
        )

        # If this is a parallel stage, execute it directly
        if stage["parallel"]:
            return await self._execute_parallel_stage(stage, message, codebase)
        else:
            # Otherwise, publish the message and wait for response
            response_future = asyncio.Future()
            
            # Subscribe to response message
            response_message_type = message_type.replace("_START", "_COMPLETE")
            
            def message_handler(response_message):
                if not response_future.done():
                    response_future.set_result(response_message.content)
            
            subscription_id = self.workspace.subscribe_with_callback(
async def _execute_parallel_stage(
        self, stage: Dict[str, Any], message: Message, codebase: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a parallel stage directly without waiting for agent response.

        Args:
            stage: The stage to execute
            message: The message to process
            codebase: The codebase to analyze

        Returns:
            The result of the stage execution
        """
        stage_id = stage["id"]
        self.logger.info(f"Executing parallel stage {stage_id} directly")

        # Extract necessary information from message
        job_id = message.content.get("job_id")
        pipeline_id = message.content.get("pipeline_id")
        previous_results = message.content.get("previous_results", {})

        # Execute based on stage type
        if stage_id == "vulnerability_pattern_matching":
            # Implement pattern matching logic
            return await self._execute_pattern_matching(codebase, job_id, pipeline_id)
        
        elif stage_id == "semantic_vulnerability_analysis":
            # Implement semantic analysis logic
            return await self._execute_semantic_analysis(codebase, job_id, pipeline_id, previous_results)
        
        elif stage_id == "cross_component_analysis":
            # Implement cross-component analysis logic
            return await self._execute_cross_component_analysis(codebase, job_id, pipeline_id, previous_results)
        
        else:
            self.logger.warning(f"Unknown parallel stage {stage_id}, using default implementation")
            # Default implementation for unknown parallel stages
            return {
                "status": "completed",
                "stage_id": stage_id,
                "job_id": job_id,
                "pipeline_id": pipeline_id,
                "results": {"message": f"Default implementation for {stage_id}"},
            }

    async def _execute_pattern_matching(
        self, codebase: Dict[str, Any], job_id: str, pipeline_id: str
    ) -> Dict[str, Any]:
        """
        Execute vulnerability pattern matching.

        Args:
            codebase: The codebase to analyze
            job_id: The ID of the job
            pipeline_id: The ID of the pipeline

        Returns:
            The result of pattern matching
        """
        self.logger.info(f"Executing vulnerability pattern matching for job {job_id}")
        
        # Find an agent that can perform pattern matching
        agent_id = None
        for agent in self.workspace.get_data("all_agents", []):
            if agent.model.agent_type == "threat_detection":
                agent_id = agent.id
                break
        
        if not agent_id:
            self.logger.warning("No threat detection agent found, using simplified pattern matching")
            # Simplified pattern matching implementation
            vulnerabilities = []
            
            # Define some basic patterns to look for
            patterns = {
                "sql_injection": [
                    r"execute\(\s*[\"']SELECT.*\+",
                    r"execute\(\s*[\"']INSERT.*\+",
                    r"execute\(\s*[\"']UPDATE.*\+",
                    r"execute\(\s*[\"']DELETE.*\+",
                ],
                "xss": [
                    r"innerHTML\s*=",
                    r"document\.write\(",
                    r"eval\(",
                ],
                "command_injection": [
                    r"exec\(",
                    r"spawn\(",
                    r"system\(",
                    r"popen\(",
                ],
            }
            
            import re

            # Scan files for patterns
            for file_path, file_content in codebase.get("files", {}).items():
                for vuln_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        compiled_pattern = re.compile(pattern, re.IGNORECASE)
                        for i, line in enumerate(file_content.split("\n")):
                            if compiled_pattern.search(line):
                                vulnerabilities.append({
                                    "id": str(uuid.uuid4()),
                                    "type": vuln_type,
                                    "file": file_path,
                                    "line": i + 1,
                                    "code": line.strip(),
                                    "confidence": 0.7,
                                    "description": f"Potential {vuln_type} vulnerability detected",
                                    "detection_method": "pattern_matching",
                                })
            
            return {
                "status": "completed",
                "stage_id": "vulnerability_pattern_matching",
                "job_id": job_id,
                "pipeline_id": pipeline_id,
                "vulnerabilities": vulnerabilities,
                "count": len(vulnerabilities),
            }
        
        # Use the agent to perform pattern matching
        message = Message(
            "THREAT_DETECTION_START",
            {
                "job_id": job_id,
                "codebase_id": codebase.get("id"),
                "codebase": codebase,
                "context": {"detection_method": "pattern_matching"},
            },
            "multi_stage_agent_orchestrator",
        )
        
        # Create a future to receive the response
        response_future = asyncio.Future()
        
        def message_handler(response_message):
            if not response_future.done():
                response_future.set_result(response_message.content)
        
        subscription_id = self.workspace.subscribe_with_callback(
            "multi_stage_agent_orchestrator",
            "THREAT_DETECTION_COMPLETE",
            message_handler,
            {"job_id": job_id},
        )
        
        try:
            # Send the message to the agent
            self.workspace.publish_message(message)
            
            # Wait for response with timeout
            try:
async def _execute_semantic_analysis(
        self, 
        codebase: Dict[str, Any], 
        job_id: str, 
        pipeline_id: str,
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute semantic vulnerability analysis.

        Args:
            codebase: The codebase to analyze
            job_id: The ID of the job
            pipeline_id: The ID of the pipeline
            previous_results: Results from previous stages

        Returns:
            The result of semantic analysis
        """
        self.logger.info(f"Executing semantic vulnerability analysis for job {job_id}")
        
        # Get code graph from previous results
        code_graph = previous_results.get("code_graph_generation", {}).get("code_graph", {})
        
        # Use context-aware analysis to find semantic vulnerabilities
        if self.context_analysis:
            try:
                semantic_model = await self.context_analysis._build_semantic_model(codebase, job_id)
                relationships = self.context_analysis._identify_cross_component_relationships(semantic_model)
                security_implications = await self.context_analysis._analyze_security_implications(relationships, job_id)
                
                # Convert security implications to vulnerabilities
                vulnerabilities = []
                for implication in security_implications:
                    vulnerabilities.append({
                        "id": implication.get("id", str(uuid.uuid4())),
                        "type": implication.get("type", "semantic_vulnerability"),
                        "file": implication.get("file", ""),
                        "line": implication.get("line", 0),
                        "code": implication.get("code", ""),
                        "confidence": implication.get("confidence", 0.6),
                        "description": implication.get("description", "Semantic vulnerability detected"),
                        "detection_method": "semantic_analysis",
                    })
                
                return {
                    "status": "completed",
                    "stage_id": "semantic_vulnerability_analysis",
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": vulnerabilities,
                    "count": len(vulnerabilities),
                    "semantic_model": semantic_model,
                }
            except Exception as e:
                self.logger.error(f"Error in semantic analysis: {e}")
        
        # Fallback implementation if context analysis is not available
        self.logger.warning("Context analysis not available, using simplified semantic analysis")
        return {
            "status": "completed",
            "stage_id": "semantic_vulnerability_analysis",
            "job_id": job_id,
            "pipeline_id": pipeline_id,
            "vulnerabilities": [],
            "count": 0,
        }

    async def _execute_cross_component_analysis(
        self, 
        codebase: Dict[str, Any], 
        job_id: str, 
        pipeline_id: str,
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute cross-component vulnerability analysis.

        Args:
            codebase: The codebase to analyze
            job_id: The ID of the job
            pipeline_id: The ID of the pipeline
            previous_results: Results from previous stages

        Returns:
            The result of cross-component analysis
        """
        self.logger.info(f"Executing cross-component analysis for job {job_id}")
        
        # Get code graph from previous results
        code_graph = previous_results.get("code_graph_generation", {}).get("code_graph", {})
        
        # Use collaborative reasoning to find cross-component vulnerabilities
        if self.collaborative_reasoning:
            try:
                # Start a reasoning chain for cross-component vulnerabilities
                chain_id = self.collaborative_reasoning.start_reasoning_chain(
                    "cross_component_vulnerabilities",
                    {
                        "job_id": job_id,
                        "pipeline_id": pipeline_id,
                        "description": "Analyzing cross-component vulnerabilities",
                    }
                )
                
                # Analyze data flows between components
                data_flows = []
                for edge in code_graph.get("edges", []):
                    if edge.get("type") in ["calls", "imports", "uses"]:
                        data_flows.append(edge)
                
                # Identify potential vulnerabilities in data flows
                vulnerabilities = []
                for flow in data_flows:
                    source = flow.get("source", "")
                    target = flow.get("target", "")
                    
                    # Check if source or target are security-critical
                    source_node = code_graph.get("nodes", {}).get(source, {})
                    target_node = code_graph.get("nodes", {}).get(target, {})
                    
                    source_name = source_node.get("name", "").lower()
                    target_name = target_node.get("name", "").lower()
                    
                    # Check for security-critical keywords
                    security_keywords = [
                        "auth", "login", "password", "token", "secret", "key",
                        "encrypt", "decrypt", "hash", "sign", "verify", "validate"
                    ]
                    
                    is_security_critical = False
                    for keyword in security_keywords:
                        if keyword in source_name or keyword in target_name:
                            is_security_critical = True
                            break
                    
                    if is_security_critical:
                        # Add to reasoning chain
                        self.collaborative_reasoning.contribute_to_reasoning(
                            chain_id,
                            {
                                "source": source,
                                "target": target,
                                "flow_type": flow.get("type"),
                                "security_critical": True,
                            },
                            0.7
                        )
                        
                        # Create vulnerability
                        vulnerabilities.append({
                            "id": str(uuid.uuid4()),
                            "type": "cross_component_vulnerability",
                            "source_component": source,
                            "target_component": target,
                            "flow_type": flow.get("type"),
                            "confidence": 0.7,
                            "description": f"Potential security issue in data flow from {source_name} to {target_name}",
                            "detection_method": "cross_component_analysis",
                        })
                
                return {
                    "status": "completed",
                    "stage_id": "cross_component_analysis",
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": vulnerabilities,
                    "count": len(vulnerabilities),
                    "reasoning_chain_id": chain_id,
                }
            except Exception as e:
                self.logger.error(f"Error in cross-component analysis: {e}")
        
        # Fallback implementation if collaborative reasoning is not available
        self.logger.warning("Collaborative reasoning not available, using simplified cross-component analysis")
        return {
            "status": "completed",
            "stage_id": "cross_component_analysis",
            "job_id": job_id,
            "pipeline_id": pipeline_id,
            "vulnerabilities": [],
            "count": 0,
        }

    def _get_pipeline_results(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get the results of a pipeline.

        Args:
            pipeline_id: The ID of the pipeline

        Returns:
            The results of the pipeline
        """
        # Combine results from all stages
        results = {
            "pipeline_id": pipeline_id,
            "status": self.pipeline_status[pipeline_id]["status"],
            "job_id": self.pipeline_status[pipeline_id]["job_id"],
            "codebase_id": self.pipeline_status[pipeline_id]["codebase_id"],
            "completed_stages": self.pipeline_status[pipeline_id]["completed_stages"],
            "failed_stages": self.pipeline_status[pipeline_id]["failed_stages"],
            "start_time": self.pipeline_status[pipeline_id]["start_time"],
            "end_time": self.pipeline_status[pipeline_id]["end_time"],
            "stage_results": {},
        }

        # Add vulnerabilities from all stages
        all_vulnerabilities = []
        for stage_id, stage_result in self.stage_results.get(pipeline_id, {}).items():
            results["stage_results"][stage_id] = stage_result
            if "vulnerabilities" in stage_result:
                all_vulnerabilities.extend(stage_result["vulnerabilities"])

        # Deduplicate vulnerabilities
        unique_vulnerabilities = {}
        for vuln in all_vulnerabilities:
            vuln_id = vuln.get("id")
            if vuln_id not in unique_vulnerabilities:
                unique_vulnerabilities[vuln_id] = vuln
            else:
                # If duplicate, keep the one with higher confidence
                if vuln.get("confidence", 0) > unique_vulnerabilities[vuln_id].get("confidence", 0):
                    unique_vulnerabilities[vuln_id] = vuln

        results["vulnerabilities"] = list(unique_vulnerabilities.values())
        results["vulnerability_count"] = len(results["vulnerabilities"])

        return results

    def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get the status of a pipeline.

        Args:
            pipeline_id: The ID of the pipeline

        Returns:
            The status of the pipeline
        """
        if pipeline_id not in self.pipeline_status:
            return {"error": f"Pipeline {pipeline_id} not found"}

        return self.pipeline_status[pipeline_id]

    async def shutdown(self):
        """Shutdown the multi-stage agent orchestrator"""
        self.logger.info("Shutting down multi-stage agent orchestrator")

        # Cancel any running tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        self._tasks = []
        self.logger.info("Multi-stage agent orchestrator shutdown complete")
                result = await asyncio.wait_for(response_future, timeout=300.0)  # 5 minute timeout
                return {
                    "status": "completed",
                    "stage_id": "vulnerability_pattern_matching",
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": result.get("vulnerabilities", []),
                    "count": len(result.get("vulnerabilities", [])),
                }
            except asyncio.TimeoutError:
                self.logger.error("Timeout waiting for pattern matching response")
                return {
                    "status": "timeout",
                    "stage_id": "vulnerability_pattern_matching",
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": [],
                    "count": 0,
                }
        finally:
            # Unsubscribe from response message
            self.workspace.unsubscribe(subscription_id)
                "multi_stage_agent_orchestrator",
                response_message_type,
                message_handler,
                {"job_id": job_id, "pipeline_id": pipeline_id, "stage_id": stage_id},
            )
            
            try:
                # Publish the message
                self.workspace.publish_message(message)
                
                # Wait for response with timeout
                try:
                    result = await asyncio.wait_for(response_future, timeout=300.0)  # 5 minute timeout
                    return result
                except asyncio.TimeoutError:
                    self.logger.error(f"Timeout waiting for response to {message_type}")
                    raise TimeoutError(f"Timeout waiting for response to {message_type}")
            finally:
                # Unsubscribe from response message
                self.workspace.unsubscribe(subscription_id)
        def on_pipeline_done(task):
            try:
                task.result()
            except Exception as e:
                self.logger.error(f"Error running pipeline {pipeline_id}: {e}")
                self.pipeline_status[pipeline_id]["status"] = "failed"
                self.pipeline_status[pipeline_id]["error"] = str(e)
                self.pipeline_status[pipeline_id]["end_time"] = asyncio.get_event_loop().time()

        task.add_done_callback(on_pipeline_done)

        return pipeline_id
        if not self.knowledge_sharing:
            self.knowledge_sharing = KnowledgeSharingProtocol(workspace)
            workspace.store_data("agentic_knowledge", self.knowledge_sharing)

        # Define the pipeline stages
        self._define_pipeline_stages()