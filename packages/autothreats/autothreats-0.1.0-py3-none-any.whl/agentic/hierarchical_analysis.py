#!/usr/bin/env python3
"""
Hierarchical Analysis module for the autonomous threat modeling system.
Enables analysis of large codebases by breaking them down into hierarchical subsystems.
"""

import asyncio
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Message
from .multi_agent_planning import MultiAgentPlanning

logger = logging.getLogger(__name__)


class HierarchicalAnalysis:
    """
    Enables analysis of large codebases by breaking them down into hierarchical subsystems.
    This is particularly useful for massive projects like Linux.
    """

    def __init__(self, workspace):
        """
        Initialize the hierarchical analysis framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.subsystems = {}
        self.subsystem_plans = {}
        self.subsystem_results = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Get the multi-agent planning component if available
        self.planner = workspace.get_data("multi_agent_planning")
        if not self.planner:
            self.planner = MultiAgentPlanning(workspace)
            workspace.store_data("multi_agent_planning", self.planner)

    async def analyze_large_codebase(
        self, codebase_model: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Analyze a large codebase using hierarchical analysis.

        Args:
            codebase_model: The codebase model to analyze
            job_id: The ID of the analysis job

        Returns:
            Analysis results
        """
        # Identify subsystems in the codebase
        subsystems = self._identify_subsystems(codebase_model)

        # Store subsystems
        self.subsystems[job_id] = subsystems
        self.workspace.store_data(f"subsystems_{job_id}", subsystems)

        # Create analysis plans for each subsystem
        subsystem_plans = await self._create_subsystem_plans(subsystems, job_id)

        # Execute subsystem analysis plans
        subsystem_results = await self._execute_subsystem_plans(subsystem_plans, job_id)

        # Integrate results from subsystems
        integrated_results = self._integrate_subsystem_results(
            subsystem_results, job_id
        )

        # Store integrated results
        self.workspace.store_data(f"hierarchical_analysis_{job_id}", integrated_results)

        return integrated_results

    def _identify_subsystems(
        self, codebase_model: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify subsystems within a large codebase.

        Args:
            codebase_model: The codebase model to analyze

        Returns:
            List of identified subsystems
        """
        subsystems = []
        files = codebase_model.get("files", {})

        # Group files by directory structure
        directory_groups = {}
        for file_path in files:
            # Split path and use first level as subsystem identifier
            parts = file_path.split("/")
            if len(parts) > 1:
                # For Linux kernel, use the top-level directory as subsystem
                subsystem_id = parts[0]
                if subsystem_id not in directory_groups:
                    directory_groups[subsystem_id] = []
                directory_groups[subsystem_id].append(file_path)

        # Create subsystem models
        for subsystem_id, subsystem_files in directory_groups.items():
            # Skip very small subsystems or non-code directories
            if len(subsystem_files) < 5:
                continue

            # Skip common non-code directories
            if subsystem_id.lower() in ["docs", "tests", "examples", "samples"]:
                continue

            # Create subsystem model
            subsystem = {
                "id": f"subsystem_{subsystem_id}",
                "name": subsystem_id,
                "file_count": len(subsystem_files),
                "files": subsystem_files,
                "security_relevance": self._assess_security_relevance(
                    subsystem_id, subsystem_files
                ),
            }
            subsystems.append(subsystem)

        # Sort subsystems by security relevance (descending)
        subsystems.sort(key=lambda x: x["security_relevance"], reverse=True)

        return subsystems

    def _assess_security_relevance(self, subsystem_id: str, files: List[str]) -> float:
        """
        Assess the security relevance of a subsystem.

        Args:
            subsystem_id: The ID of the subsystem
            files: List of files in the subsystem

        Returns:
            Security relevance score (0.0 to 1.0)
        """
        # Base relevance score
        relevance = 0.5

        # Adjust based on subsystem name
        high_relevance_keywords = [
            "security",
            "auth",
            "crypt",
            "ssl",
            "tls",
            "key",
            "cert",
            "password",
            "login",
            "user",
            "access",
            "perm",
            "priv",
            "network",
            "net",
            "socket",
            "input",
            "usb",
            "driver",
            "syscall",
            "system",
            "kernel",
            "module",
            "memory",
            "mm",
            "fs",
            "file",
            "io_uring",
        ]

        for keyword in high_relevance_keywords:
            if keyword in subsystem_id.lower():
                relevance += 0.2
                break

        # Check file extensions and names
        security_file_patterns = [
            ".c",
            ".h",
            ".rs",
            ".go",
            ".py",
            ".js",
            ".ts",
            ".java",
            "security",
            "auth",
            "crypt",
            "ssl",
            "tls",
            "password",
            "login",
            "user",
            "access",
            "perm",
            "priv",
        ]

        security_file_count = 0
        for file_path in files:
            for pattern in security_file_patterns:
                if pattern in file_path.lower():
                    security_file_count += 1
                    break

        # Adjust relevance based on proportion of security-related files
        if files:
            security_ratio = security_file_count / len(files)
            relevance += security_ratio * 0.3

        # Cap relevance at 1.0
        return min(1.0, relevance)

    async def _create_subsystem_plans(
        self, subsystems: List[Dict[str, Any]], job_id: str
    ) -> Dict[str, Any]:
        """
        Create analysis plans for each subsystem.

        Args:
            subsystems: List of identified subsystems
            job_id: The ID of the analysis job

        Returns:
            Dictionary mapping subsystem IDs to analysis plans
        """
        subsystem_plans = {}

        # Create a plan for each subsystem
        for subsystem in subsystems:
            subsystem_id = subsystem["id"]

            # Create a mini-codebase model for the subsystem
            subsystem_codebase = {
                "id": f"codebase_{subsystem_id}",
                "files": {file: True for file in subsystem["files"]},
                "file_count": subsystem["file_count"],
                "security_relevance": subsystem["security_relevance"],
            }

            # Create a plan for the subsystem
            plan_id = await self.planner.create_analysis_plan(
                subsystem_codebase, job_id
            )
            subsystem_plans[subsystem_id] = plan_id

        # Store subsystem plans
        self.subsystem_plans[job_id] = subsystem_plans
        self.workspace.store_data(f"subsystem_plans_{job_id}", subsystem_plans)

        return subsystem_plans

    async def _execute_subsystem_plans(
        self, subsystem_plans: Dict[str, str], job_id: str
    ) -> Dict[str, Any]:
        """
        Execute analysis plans for each subsystem.

        Args:
            subsystem_plans: Dictionary mapping subsystem IDs to plan IDs
            job_id: The ID of the analysis job

        Returns:
            Dictionary mapping subsystem IDs to analysis results
        """
        subsystem_results = {}

        # Execute plans for high-priority subsystems first
        # For large codebases, we may need to limit the number of subsystems analyzed
        max_subsystems = 10  # Limit for very large codebases

        # Sort subsystems by priority (based on security relevance)
        sorted_subsystems = sorted(
            subsystem_plans.keys(),
            key=lambda x: self.subsystems[job_id][
                next(i for i, s in enumerate(self.subsystems[job_id]) if s["id"] == x)
            ]["security_relevance"],
            reverse=True,
        )

        # Limit to max_subsystems
        subsystems_to_analyze = sorted_subsystems[:max_subsystems]

        # Execute plans for selected subsystems
        for subsystem_id in subsystems_to_analyze:
            plan_id = subsystem_plans[subsystem_id]

            # Execute the plan
            result = await self.planner.execute_plan(plan_id)
            subsystem_results[subsystem_id] = result

        # Store subsystem results
        self.subsystem_results[job_id] = subsystem_results
        self.workspace.store_data(f"subsystem_results_{job_id}", subsystem_results)

        return subsystem_results

    def _integrate_subsystem_results(
        self, subsystem_results: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Integrate results from subsystems into a unified analysis.

        Args:
            subsystem_results: Dictionary mapping subsystem IDs to analysis results
            job_id: The ID of the analysis job

        Returns:
            Integrated analysis results
        """
        # Collect all threats from subsystems
        all_threats = []
        subsystem_threats = {}

        for subsystem_id, result in subsystem_results.items():
            # Extract threats from subsystem result
            threats = result.get("results", {}).get("threats", [])
            subsystem_threats[subsystem_id] = threats
            all_threats.extend(threats)

        # Deduplicate threats
        unique_threats = self._deduplicate_threats(all_threats)

        # Identify cross-subsystem threats
        cross_subsystem_threats = self._identify_cross_subsystem_threats(
            subsystem_threats
        )

        # Create integrated results
        integrated_results = {
            "job_id": job_id,
            "analysis_type": "hierarchical",
            "subsystems_analyzed": len(subsystem_results),
            "total_threats_found": len(all_threats),
            "unique_threats": len(unique_threats),
            "cross_subsystem_threats": len(cross_subsystem_threats),
            "threats": unique_threats,
            "cross_subsystem_threats": cross_subsystem_threats,
            "subsystem_results": subsystem_results,
        }

        return integrated_results

    def _deduplicate_threats(
        self, threats: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Deduplicate threats based on similarity.

        Args:
            threats: List of threats to deduplicate

        Returns:
            List of deduplicated threats
        """
        if not threats:
            return []

        # Group similar threats
        threat_groups = []

        for threat in threats:
            # Check if this threat is similar to any existing group
            found_group = False

            for group in threat_groups:
                if self._are_threats_similar(threat, group[0]):
                    group.append(threat)
                    found_group = True
                    break

            if not found_group:
                # Create a new group
                threat_groups.append([threat])

        # Merge similar threats in each group
        unique_threats = []

        for group in threat_groups:
            if len(group) == 1:
                # Only one threat in the group, no merging needed
                unique_threats.append(group[0])
            else:
                # Merge similar threats
                merged_threat = self._merge_similar_threats(group)
                unique_threats.append(merged_threat)

        return unique_threats

    def _are_threats_similar(
        self, threat1: Dict[str, Any], threat2: Dict[str, Any]
    ) -> bool:
        """
        Check if two threats are similar.

        Args:
            threat1: First threat
            threat2: Second threat

        Returns:
            True if threats are similar, False otherwise
        """
        # Check if threats have the same type
        if threat1.get("type") != threat2.get("type"):
            return False

        # Check if threats affect the same components
        components1 = set(
            c.get("name", "") for c in threat1.get("affected_components", [])
        )
        components2 = set(
            c.get("name", "") for c in threat2.get("affected_components", [])
        )

        # If there's significant overlap in affected components, consider them similar
        if components1 and components2:
            overlap = len(components1.intersection(components2))
            union = len(components1.union(components2))

            if overlap / union > 0.5:  # More than 50% overlap
                return True

        return False

    def _merge_similar_threats(self, threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge similar threats into a single threat.

        Args:
            threats: List of similar threats to merge

        Returns:
            Merged threat
        """
        if not threats:
            return {}

        # Use the first threat as a base
        base_threat = threats[0].copy()

        # Collect all affected components
        all_components = []
        for threat in threats:
            all_components.extend(threat.get("affected_components", []))

        # Deduplicate components
        unique_components = []
        component_names = set()

        for component in all_components:
            name = component.get("name", "")
            if name and name not in component_names:
                component_names.add(name)
                unique_components.append(component)

        # Update the base threat
        base_threat["affected_components"] = unique_components

        # Take the highest severity
        severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        max_severity = base_threat.get("severity", "medium")

        for threat in threats[1:]:
            severity = threat.get("severity", "medium")
            if severity_levels.get(severity, 0) > severity_levels.get(max_severity, 0):
                max_severity = severity

        base_threat["severity"] = max_severity

        # Indicate that this is a merged threat
        base_threat["merged"] = True
        base_threat["merged_count"] = len(threats)

        return base_threat

    def _identify_cross_subsystem_threats(
        self, subsystem_threats: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Identify threats that span multiple subsystems.

        Args:
            subsystem_threats: Dictionary mapping subsystem IDs to threats

        Returns:
            List of cross-subsystem threats
        """
        cross_subsystem_threats = []

        # Collect all components affected by threats in each subsystem
        subsystem_components = {}

        for subsystem_id, threats in subsystem_threats.items():
            components = set()

            for threat in threats:
                for component in threat.get("affected_components", []):
                    components.add(component.get("name", ""))

            subsystem_components[subsystem_id] = components

        # Identify components that appear in multiple subsystems
        shared_components = {}

        for subsystem_id, components in subsystem_components.items():
            for component in components:
                if component not in shared_components:
                    shared_components[component] = []
                shared_components[component].append(subsystem_id)

        # Filter to components that appear in multiple subsystems
        cross_subsystem_components = {
            component: subsystems
            for component, subsystems in shared_components.items()
            if len(subsystems) > 1
        }

        # Identify threats that affect these cross-subsystem components
        for component, subsystems in cross_subsystem_components.items():
            # Collect threats that affect this component
            component_threats = []

            for subsystem_id in subsystems:
                for threat in subsystem_threats.get(subsystem_id, []):
                    if any(
                        c.get("name", "") == component
                        for c in threat.get("affected_components", [])
                    ):
                        component_threats.append((subsystem_id, threat))

            if len(component_threats) > 1:
                # Create a cross-subsystem threat
                cross_subsystem_threat = {
                    "id": f"cross_subsystem_threat_{uuid.uuid4()}",
                    "type": "Cross-Subsystem Vulnerability",
                    "description": f"Vulnerability affecting component {component} across multiple subsystems",
                    "affected_component": component,
                    "affected_subsystems": subsystems,
                    "related_threats": [
                        {
                            "subsystem_id": subsystem_id,
                            "threat_id": threat.get("id", ""),
                            "threat_type": threat.get("type", ""),
                            "severity": threat.get("severity", "medium"),
                        }
                        for subsystem_id, threat in component_threats
                    ],
                }

                cross_subsystem_threats.append(cross_subsystem_threat)

        return cross_subsystem_threats
