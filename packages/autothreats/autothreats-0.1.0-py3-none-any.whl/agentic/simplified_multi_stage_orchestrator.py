#!/usr/bin/env python3
"""
Simplified Multi-Stage Agent Orchestrator for the autonomous threat modeling system.
Coordinates multiple specialized agents to work together in a pipeline for enhanced threat detection.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import SharedWorkspace

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
        
        # Define the pipeline stages
        self._define_pipeline_stages()

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
                "id": "risk_scoring",
                "name": "Risk Scoring",
                "description": "Assign risk scores to validated vulnerabilities",
                "agent_type": "risk_scoring",
                "dependencies": ["vulnerability_validation"],
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
        
        # Add callback for when the pipeline completes
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

            self.logger.info(f"Pipeline {pipeline_id} completed successfully")

        except Exception as e:
            self.logger.error(f"Error running pipeline {pipeline_id}: {e}")
            self.pipeline_status[pipeline_id]["status"] = "failed"
            self.pipeline_status[pipeline_id]["error"] = str(e)
            self.pipeline_status[pipeline_id]["end_time"] = asyncio.get_event_loop().time()

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

        # If this is a parallel stage, execute it directly
        if stage["parallel"]:
            if stage_id == "vulnerability_pattern_matching":
                return await self._execute_pattern_matching(codebase, job_id, pipeline_id)
            elif stage_id == "semantic_vulnerability_analysis":
                return await self._execute_semantic_analysis(codebase, job_id, pipeline_id, previous_results)
            elif stage_id == "cross_component_analysis":
                return await self._execute_cross_component_analysis(codebase, job_id, pipeline_id, previous_results)
            else:
                self.logger.warning(f"Unknown parallel stage {stage_id}, using default implementation")
                return {
                    "status": "completed",
                    "stage_id": stage_id,
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "results": {"message": f"Default implementation for {stage_id}"},
                }
        else:
            # For non-parallel stages, use a simplified implementation
            return await self._execute_simplified_stage(stage, pipeline_id, job_id, codebase_id, codebase, previous_results)

    async def _execute_simplified_stage(
        self,
        stage: Dict[str, Any],
        pipeline_id: str,
        job_id: str,
        codebase_id: str,
        codebase: Dict[str, Any],
        previous_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a simplified stage implementation.

        Args:
            stage: The stage to execute
            pipeline_id: The ID of the pipeline
            job_id: The ID of the job
            codebase_id: The ID of the codebase
            codebase: The codebase to analyze
            previous_results: Results from previous stages

        Returns:
            The result of the stage execution
        """
        stage_id = stage["id"]
        
        # Simplified implementations for each stage
        if stage_id == "context_analysis":
            # Try to use the agentic context agent first
            agentic_context_agent = None
            try:
                if hasattr(self.workspace, 'agents'):
                    agentic_context_agent = self.workspace.agents.get("agentic_context_agent")
            except (AttributeError, TypeError):
                self.logger.debug("Workspace agents attribute not accessible")
                
            if agentic_context_agent:
                self.logger.info(f"Using agentic context agent for context analysis in job {job_id}")
                # Prepare parameters for the agent
                params = {
                    "codebase_id": codebase.get("id", "unknown"),
                    "job_id": job_id,
                    "lightweight": False
                }
                
                # Call the agent to analyze context
                result = await agentic_context_agent.process(params)
                
                # Extract context from result
                context = result.get("context", {})
                
                return {
                    "status": "completed",
                    "stage_id": stage_id,
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "context": context,
                }
            
            # Fall back to context-aware security component if agent not available
            context_aware_security = self.workspace.get_data("context_aware_security")
            if context_aware_security:
                self.logger.info(f"Using context-aware security for context analysis in job {job_id}")
                security_context = await context_aware_security.analyze_security_context(codebase, job_id)
                return {
                    "status": "completed",
                    "stage_id": stage_id,
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "security_context": security_context,
                }
            
        elif stage_id == "code_graph_generation":
            # Simplified code graph generation
            # Just create a basic graph with files and directories
            nodes = {}
            edges = []
            
            # Add file nodes
            for file_path in codebase.get("files", {}).keys():
                file_id = f"file_{uuid.uuid4()}"
                nodes[file_id] = {
                    "id": file_id,
                    "type": "file",
                    "name": file_path,
                    "file": file_path,
                }
                
                # Add directory nodes and edges
                dir_path = "/".join(file_path.split("/")[:-1])
                if dir_path:
                    dir_id = f"dir_{dir_path}"
                    if dir_id not in nodes:
                        nodes[dir_id] = {
                            "id": dir_id,
                            "type": "directory",
                            "name": dir_path,
                        }
                    
                    # Add edge from directory to file
                    edges.append({
                        "source": dir_id,
                        "target": file_id,
                        "type": "contains",
                    })
            
            code_graph = {
                "nodes": nodes,
                "edges": edges,
            }
            
            return {
                "status": "completed",
                "stage_id": stage_id,
                "job_id": job_id,
                "pipeline_id": pipeline_id,
                "code_graph": code_graph,
            }
            
        elif stage_id == "vulnerability_validation":
            # Combine vulnerabilities from previous stages
            vulnerabilities = []
            for prev_stage_id, prev_result in previous_results.items():
                if "vulnerabilities" in prev_result:
                    vulnerabilities.extend(prev_result["vulnerabilities"])
            
            # Simple validation: remove duplicates and low confidence vulnerabilities
            validated_vulnerabilities = []
            seen_vulns = set()
            
            for vuln in vulnerabilities:
                # Create a key for deduplication
                vuln_key = f"{vuln.get('file_path', '')}:{vuln.get('line', 0)}:{vuln.get('type', '')}"
                
                # Skip duplicates and low confidence vulnerabilities
                if vuln_key not in seen_vulns and vuln.get("confidence", 0) >= 0.5:
                    seen_vulns.add(vuln_key)
                    validated_vulnerabilities.append(vuln)
            
            return {
                "status": "completed",
                "stage_id": stage_id,
                "job_id": job_id,
                "pipeline_id": pipeline_id,
                "vulnerabilities": validated_vulnerabilities,
                "count": len(validated_vulnerabilities),
            }
            
        elif stage_id == "risk_scoring":
            # Get vulnerabilities from previous stage
            vulnerabilities = []
            if "vulnerability_validation" in previous_results:
                vulnerabilities = previous_results["vulnerability_validation"].get("vulnerabilities", [])
            
            # Assign risk scores based on severity and confidence
            scored_vulnerabilities = []
            for vuln in vulnerabilities:
                # Create a copy of the vulnerability
                scored_vuln = dict(vuln)
                
                # Calculate risk score
                severity = vuln.get("severity", "medium")
                confidence = vuln.get("confidence", 0.5)
                
                severity_scores = {
                    "critical": 10.0,
                    "high": 8.0,
                    "medium": 5.0,
                    "low": 2.0,
                    "info": 1.0,
                }
                
                risk_score = severity_scores.get(severity.lower(), 5.0) * confidence
                scored_vuln["risk_score"] = risk_score
                
                scored_vulnerabilities.append(scored_vuln)
            
            return {
                "status": "completed",
                "stage_id": stage_id,
                "job_id": job_id,
                "pipeline_id": pipeline_id,
                "vulnerabilities": scored_vulnerabilities,
                "count": len(scored_vulnerabilities),
            }
            
        elif stage_id == "prioritization":
            # Get adaptive prioritization component if available
            adaptive_prioritization = self.workspace.get_data("adaptive_prioritization")
            if adaptive_prioritization and "risk_scoring" in previous_results:
                vulnerabilities = previous_results["risk_scoring"].get("vulnerabilities", [])
                prioritized_vulnerabilities = await adaptive_prioritization.prioritize_vulnerabilities(
                    vulnerabilities,
                    job_id
                )
                
                return {
                    "status": "completed",
                    "stage_id": stage_id,
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": prioritized_vulnerabilities,
                    "count": len(prioritized_vulnerabilities),
                }
            
        elif stage_id == "threat_model_assembly":
            # Get explainable security component if available
            explainable_security = self.workspace.get_data("explainable_security")
            if explainable_security and "prioritization" in previous_results:
                vulnerabilities = previous_results["prioritization"].get("vulnerabilities", [])
                
                # Add detailed explanations
                explained_vulnerabilities = await explainable_security.explain_vulnerabilities(
                    vulnerabilities,
                    job_id
                )
                
                # Generate executive summary
                executive_summary = await explainable_security.generate_executive_summary(
                    explained_vulnerabilities,
                    job_id
                )
                
                # Create threat model
                threat_model = {
                    "job_id": job_id,
                    "codebase_id": codebase_id,
                    "vulnerabilities": explained_vulnerabilities,
                    "vulnerability_count": len(explained_vulnerabilities),
                    "executive_summary": executive_summary,
                    "generated_at": asyncio.get_event_loop().time(),
                }
                
                return {
                    "status": "completed",
                    "stage_id": stage_id,
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "threat_model": threat_model,
                }
        
        # Default implementation for other stages
        return {
            "status": "completed",
            "stage_id": stage_id,
            "job_id": job_id,
            "pipeline_id": pipeline_id,
            "message": f"Simplified implementation for {stage_id}",
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
                                "file_path": file_path,
                                "line": i + 1,
                                "code": line.strip(),
                                "confidence": 0.7,
                                "description": f"Potential {vuln_type} vulnerability detected",
                                "detection_method": "pattern_matching",
                                "severity": "high" if vuln_type in ["sql_injection", "command_injection"] else "medium",
                            })
        
        return {
            "status": "completed",
            "stage_id": "vulnerability_pattern_matching",
            "job_id": job_id,
            "pipeline_id": pipeline_id,
            "vulnerabilities": vulnerabilities,
            "count": len(vulnerabilities),
        }

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
        
        # Get context-aware security component if available
        context_aware_security = self.workspace.get_data("context_aware_security")
        if context_aware_security:
            try:
                # Analyze security context
                security_context = await context_aware_security.analyze_security_context(
                    codebase,
                    job_id
                )
                
                # Extract security patterns
                security_patterns = security_context.get("security_patterns", {})
                
                # Convert security patterns to vulnerabilities
                vulnerabilities = []
                
                # Process authentication patterns
                for auth_pattern in security_patterns.get("authentication", []):
                    if auth_pattern.get("strength") == "weak":
                        vulnerabilities.append({
                            "id": str(uuid.uuid4()),
                            "type": "weak_authentication",
                            "file_path": auth_pattern.get("file_path", ""),
                            "line": auth_pattern.get("location", 0),
                            "code": "",
                            "confidence": 0.6,
                            "description": f"Weak authentication mechanism: {auth_pattern.get('description', '')}",
                            "detection_method": "semantic_analysis",
                            "severity": "high",
                        })
                
                # Process authorization patterns
                for auth_pattern in security_patterns.get("authorization", []):
                    if auth_pattern.get("strength") == "weak":
                        vulnerabilities.append({
                            "id": str(uuid.uuid4()),
                            "type": "weak_authorization",
                            "file_path": auth_pattern.get("file_path", ""),
                            "line": auth_pattern.get("location", 0),
                            "code": "",
                            "confidence": 0.6,
                            "description": f"Weak authorization mechanism: {auth_pattern.get('description', '')}",
                            "detection_method": "semantic_analysis",
                            "severity": "high",
                        })
                
                # Process encryption patterns
                for encrypt_pattern in security_patterns.get("encryption", []):
                    if encrypt_pattern.get("strength") == "weak":
                        vulnerabilities.append({
                            "id": str(uuid.uuid4()),
                            "type": "weak_encryption",
                            "file_path": encrypt_pattern.get("file_path", ""),
                            "line": encrypt_pattern.get("location", 0),
                            "code": "",
                            "confidence": 0.6,
                            "description": f"Weak encryption: {encrypt_pattern.get('description', '')}",
                            "detection_method": "semantic_analysis",
                            "severity": "high",
                        })
                
                return {
                    "status": "completed",
                    "stage_id": "semantic_vulnerability_analysis",
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "vulnerabilities": vulnerabilities,
                    "count": len(vulnerabilities),
                }
            except Exception as e:
                self.logger.error(f"Error in semantic analysis: {e}")
        
        # Fallback implementation
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
        
        # Simplified cross-component analysis
        vulnerabilities = []
        
        # Analyze data flows between components
        data_flows = []
        for edge in code_graph.get("edges", []):
            if edge.get("type") in ["calls", "imports", "uses", "contains"]:
                data_flows.append(edge)
        
        # Check for security-critical components
        for flow in data_flows:
            source = flow.get("source", "")
            target = flow.get("target", "")
            
            # Get source and target nodes
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
                # Create vulnerability
                vulnerabilities.append({
                    "id": str(uuid.uuid4()),
                    "type": "cross_component_vulnerability",
                    "file_path": source_node.get("file", "") or target_node.get("file", ""),
                    "line": 0,
                    "code": "",
                    "confidence": 0.6,
                    "description": f"Potential security issue in data flow from {source_name} to {target_name}",
                    "detection_method": "cross_component_analysis",
                    "severity": "medium",
                })
        
        return {
            "status": "completed",
            "stage_id": "cross_component_analysis",
            "job_id": job_id,
            "pipeline_id": pipeline_id,
            "vulnerabilities": vulnerabilities,
            "count": len(vulnerabilities),
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