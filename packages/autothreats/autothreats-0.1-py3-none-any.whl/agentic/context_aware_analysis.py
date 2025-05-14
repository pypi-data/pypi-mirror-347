#!/usr/bin/env python3
"""
Context-Aware Analysis module for the autonomous threat modeling system.
Enhances security analysis with deep contextual understanding of code relationships.
"""

import asyncio
import logging
import os
import re
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import Message
from .causal_reasoning import CausalReasoning

logger = logging.getLogger(__name__)


class ContextAwareAnalysis:
    """
    Enhances security analysis with deep contextual understanding of code relationships.
    Particularly useful for large codebases with complex interactions.
    """

    def __init__(self, workspace):
        """
        Initialize the context-aware analysis framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.context_models = {}
        self.semantic_relationships = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Get the causal reasoning component if available
        self.causal_reasoning = workspace.get_data("causal_reasoning")
        if not self.causal_reasoning:
            self.causal_reasoning = CausalReasoning(workspace)
            workspace.store_data("causal_reasoning", self.causal_reasoning)

        # Get LLM service from workspace if available
        self.llm_service = workspace.get_data("llm_service")
        if not self.llm_service:
            self.logger.warning(
                "LLM service not found in workspace, context analysis will be limited"
            )

    async def analyze_code_context(
        self, codebase_model: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Perform context-aware analysis on a codebase.

        Args:
            codebase_model: The codebase model to analyze
            job_id: The ID of the analysis job

        Returns:
            Context analysis results
        """
        # Build semantic model of the codebase
        semantic_model = await self._build_semantic_model(codebase_model, job_id)

        # Identify cross-component relationships
        relationships = self._identify_cross_component_relationships(semantic_model)

        # Analyze security implications of relationships
        security_implications = await self._analyze_security_implications(
            relationships, job_id
        )

        # Create context model
        context_model = {
            "job_id": job_id,
            "semantic_model": semantic_model,
            "relationships": relationships,
            "security_implications": security_implications,
        }

        # Store context model
        self.context_models[job_id] = context_model
        self.workspace.store_data(f"context_model_{job_id}", context_model)

        return context_model

    async def _build_semantic_model(
        self, codebase_model: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Build a semantic model of the codebase.

        Args:
            codebase_model: The codebase model to analyze
            job_id: The ID of the analysis job

        Returns:
            Semantic model of the codebase
        """
        # Get code graph if available
        code_graph = self.workspace.get_data(f"code_graph_{job_id}")
        if not code_graph:
            self.logger.warning(
                f"Code graph not found for job {job_id}, semantic model will be limited"
            )
            code_graph = {"nodes": {}, "edges": []}

        # Get normalized representation if available
        normalized_representation = self.workspace.get_data(
            f"normalized_representation_{job_id}"
        )
        if not normalized_representation:
            self.logger.warning(f"Normalized representation not found for job {job_id}")
            normalized_representation = {}

        # Extract components from code graph
        components = self._extract_components_from_graph(code_graph)

        # Extract data flows from code graph
        data_flows = self._extract_data_flows_from_graph(code_graph)

        # Extract control flows from code graph
        control_flows = self._extract_control_flows_from_graph(code_graph)

        # Identify trust boundaries
        trust_boundaries = self._identify_trust_boundaries(components, data_flows)

        # Identify security-critical components
        security_critical_components = self._identify_security_critical_components(
            components, normalized_representation
        )

        # Create semantic model
        semantic_model = {
            "components": components,
            "data_flows": data_flows,
            "control_flows": control_flows,
            "trust_boundaries": trust_boundaries,
            "security_critical_components": security_critical_components,
        }

        return semantic_model

    def _extract_components_from_graph(
        self, code_graph: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract components from code graph.

        Args:
            code_graph: The code graph to analyze

        Returns:
            List of components
        """
        components = []

        # Extract components from nodes
        for node_id, node in code_graph.get("nodes", {}).items():
            # Skip synthetic nodes
            if node.get("attributes", {}).get("synthetic", False):
                continue

            # Create component
            component = {
                "id": node_id,
                "type": node.get("type", "unknown"),
                "name": node.get("name", ""),
                "file": node.get("file", ""),
                "attributes": node.get("attributes", {}),
                "security_relevance": self._assess_component_security_relevance(node),
            }

            components.append(component)

        return components

    def _assess_component_security_relevance(self, node: Dict[str, Any]) -> float:
        """
        Assess the security relevance of a component.

        Args:
            node: The node to assess

        Returns:
            Security relevance score (0.0 to 1.0)
        """
        # Base relevance score
        relevance = 0.3

        # Check node type
        node_type = node.get("type", "")
        if node_type == "class":
            relevance += 0.1
        elif node_type == "function":
            relevance += 0.05

        # Check node name for security-related keywords
        name = node.get("name", "").lower()
        security_keywords = [
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
            "validate",
            "sanitize",
            "escape",
            "filter",
            "check",
            "token",
            "secret",
            "credential",
            "session",
            "cookie",
        ]

        for keyword in security_keywords:
            if keyword in name:
                relevance += 0.2
                break

        # Check file path for security-related keywords
        file_path = node.get("file", "").lower()
        for keyword in security_keywords:
            if keyword in file_path:
                relevance += 0.1
                break

        # Cap relevance at 1.0
        return min(1.0, relevance)

    def _extract_data_flows_from_graph(
        self, code_graph: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract data flows from code graph.

        Args:
            code_graph: The code graph to analyze

        Returns:
            List of data flows
        """
        data_flows = []

        # Extract data flows from edges
        for edge in code_graph.get("edges", []):
            edge_type = edge.get("type", "")

            # Consider certain edge types as data flows
            if edge_type in ["calls", "imports", "belongs_to"]:
                # Create data flow
                data_flow = {
                    "source": edge.get("source", ""),
                    "target": edge.get("target", ""),
                    "type": edge_type,
                    "attributes": edge.get("attributes", {}),
                }

                data_flows.append(data_flow)

        return data_flows

    def _extract_control_flows_from_graph(
        self, code_graph: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract control flows from code graph.

        Args:
            code_graph: The code graph to analyze

        Returns:
            List of control flows
        """
        control_flows = []

        # Extract control flows from edges
        for edge in code_graph.get("edges", []):
            edge_type = edge.get("type", "")

            # Consider certain edge types as control flows
            if edge_type in ["calls", "extends", "method_of"]:
                # Create control flow
                control_flow = {
                    "source": edge.get("source", ""),
                    "target": edge.get("target", ""),
                    "type": edge_type,
                    "attributes": edge.get("attributes", {}),
                }

                control_flows.append(control_flow)

        return control_flows

    def _identify_trust_boundaries(
        self, components: List[Dict[str, Any]], data_flows: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Identify trust boundaries in the codebase.

        Args:
            components: List of components
            data_flows: List of data flows

        Returns:
            List of trust boundaries
        """
        trust_boundaries = []

        # Create a map of component IDs to components
        component_map = {component["id"]: component for component in components}

        # Identify potential trust boundaries based on component types and data flows
        for data_flow in data_flows:
            source_id = data_flow.get("source", "")
            target_id = data_flow.get("target", "")

            source = component_map.get(source_id)
            target = component_map.get(target_id)

            if not source or not target:
                continue

            # Check if this data flow crosses a potential trust boundary
            if self._is_trust_boundary_crossing(source, target):
                # Create trust boundary
                trust_boundary = {
                    "id": f"trust_boundary_{uuid.uuid4()}",
                    "source_component": source_id,
                    "target_component": target_id,
                    "data_flow": data_flow,
                    "boundary_type": self._determine_boundary_type(source, target),
                }

                trust_boundaries.append(trust_boundary)

        return trust_boundaries

    def _is_trust_boundary_crossing(
        self, source: Dict[str, Any], target: Dict[str, Any]
    ) -> bool:
        """
        Check if a data flow between two components crosses a trust boundary.

        Args:
            source: Source component
            target: Target component

        Returns:
            True if the data flow crosses a trust boundary, False otherwise
        """
        # Check component types
        source_type = source.get("type", "")
        target_type = target.get("type", "")

        # Check component names for boundary indicators
        source_name = source.get("name", "").lower()
        target_name = target.get("name", "").lower()

        boundary_indicators = [
            ("external", "internal"),
            ("public", "private"),
            ("user", "system"),
            ("input", "process"),
            ("client", "server"),
            ("frontend", "backend"),
            ("untrusted", "trusted"),
        ]

        for untrusted, trusted in boundary_indicators:
            if (untrusted in source_name and trusted in target_name) or (
                untrusted in source_type and trusted in target_type
            ):
                return True

        # Check security relevance
        source_relevance = source.get("security_relevance", 0.0)
        target_relevance = target.get("security_relevance", 0.0)

        # If there's a significant difference in security relevance, consider it a boundary
        if abs(source_relevance - target_relevance) > 0.3:
            return True

        return False

    def _determine_boundary_type(
        self, source: Dict[str, Any], target: Dict[str, Any]
    ) -> str:
        """
        Determine the type of trust boundary between two components.

        Args:
            source: Source component
            target: Target component

        Returns:
            Type of trust boundary
        """
        source_name = source.get("name", "").lower()
        target_name = target.get("name", "").lower()

        # Check for specific boundary types
        if "user" in source_name and "system" in target_name:
            return "user-system"
        elif "client" in source_name and "server" in target_name:
            return "client-server"
        elif "frontend" in source_name and "backend" in target_name:
            return "frontend-backend"
        elif "external" in source_name and "internal" in target_name:
            return "external-internal"
        elif "public" in source_name and "private" in target_name:
            return "public-private"
        elif "input" in source_name and "process" in target_name:
            return "input-processing"
        else:
            return "generic"

    def _identify_security_critical_components(
        self,
        components: List[Dict[str, Any]],
        normalized_representation: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Identify security-critical components in the codebase.

        Args:
            components: List of components
            normalized_representation: Normalized representation of the codebase

        Returns:
            List of security-critical components
        """
        security_critical_components = []

        # Security-critical patterns to look for
        security_patterns = {
            "authentication": [
                "login",
                "auth",
                "authenticate",
                "verify",
                "password",
                "credential",
            ],
            "authorization": [
                "authorize",
                "permission",
                "access",
                "role",
                "priv",
                "right",
            ],
            "cryptography": [
                "crypt",
                "encrypt",
                "decrypt",
                "hash",
                "sign",
                "verify",
                "key",
                "cert",
            ],
            "input_validation": [
                "validate",
                "sanitize",
                "escape",
                "filter",
                "clean",
                "check",
            ],
            "session_management": ["session", "token", "cookie", "jwt", "oauth"],
            "logging": ["log", "audit", "monitor", "trace"],
        }

        # Check each component for security-critical patterns
        for component in components:
            component_name = component.get("name", "").lower()
            component_file = component.get("file", "").lower()

            # Check for security-critical patterns in component name and file
            matched_patterns = []

            for category, patterns in security_patterns.items():
                for pattern in patterns:
                    if pattern in component_name or pattern in component_file:
                        matched_patterns.append(category)
                        break

            # If component matches any security patterns, consider it security-critical
            if matched_patterns:
                security_critical_component = component.copy()
                security_critical_component["security_categories"] = list(
                    set(matched_patterns)
                )
                security_critical_components.append(security_critical_component)

        return security_critical_components

    def _identify_cross_component_relationships(
        self, semantic_model: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify relationships between components across the codebase.

        Args:
            semantic_model: Semantic model of the codebase

        Returns:
            List of cross-component relationships
        """
        relationships = []

        # Extract components and flows from semantic model
        components = semantic_model.get("components", [])
        data_flows = semantic_model.get("data_flows", [])
        control_flows = semantic_model.get("control_flows", [])
        trust_boundaries = semantic_model.get("trust_boundaries", [])

        # Create a map of component IDs to components
        component_map = {component["id"]: component for component in components}

        # Identify relationships based on data flows
        for data_flow in data_flows:
            source_id = data_flow.get("source", "")
            target_id = data_flow.get("target", "")

            source = component_map.get(source_id)
            target = component_map.get(target_id)

            if not source or not target:
                continue

            # Create relationship
            relationship = {
                "id": f"relationship_{uuid.uuid4()}",
                "type": "data_flow",
                "source_component": source,
                "target_component": target,
                "flow": data_flow,
                "crosses_trust_boundary": self._crosses_trust_boundary(
                    source_id, target_id, trust_boundaries
                ),
            }

            relationships.append(relationship)

        # Identify relationships based on control flows
        for control_flow in control_flows:
            source_id = control_flow.get("source", "")
            target_id = control_flow.get("target", "")

            source = component_map.get(source_id)
            target = component_map.get(target_id)

            if not source or not target:
                continue

            # Create relationship
            relationship = {
                "id": f"relationship_{uuid.uuid4()}",
                "type": "control_flow",
                "source_component": source,
                "target_component": target,
                "flow": control_flow,
                "crosses_trust_boundary": self._crosses_trust_boundary(
                    source_id, target_id, trust_boundaries
                ),
            }

            relationships.append(relationship)

        return relationships

    def _crosses_trust_boundary(
        self, source_id: str, target_id: str, trust_boundaries: List[Dict[str, Any]]
    ) -> bool:
        """
        Check if a relationship crosses a trust boundary.

        Args:
            source_id: ID of the source component
            target_id: ID of the target component
            trust_boundaries: List of trust boundaries

        Returns:
            True if the relationship crosses a trust boundary, False otherwise
        """
        for boundary in trust_boundaries:
            if (
                boundary.get("source_component") == source_id
                and boundary.get("target_component") == target_id
            ):
                return True

        return False

    async def _analyze_security_implications(
        self, relationships: List[Dict[str, Any]], job_id: str
    ) -> List[Dict[str, Any]]:
        """
        Analyze security implications of relationships.

        Args:
            relationships: List of relationships
            job_id: The ID of the analysis job

        Returns:
            List of security implications
        """
        security_implications = []

        # Analyze relationships that cross trust boundaries
        boundary_crossing_relationships = [
            r for r in relationships if r.get("crosses_trust_boundary", False)
        ]

        for relationship in boundary_crossing_relationships:
            # Create a vulnerability model for causal reasoning
            vulnerability_data = self._create_vulnerability_model_from_relationship(
                relationship
            )

            # Use causal reasoning to analyze the vulnerability
            analysis_result = await self.causal_reasoning.analyze_attack_path(
                vulnerability_data
            )

            # Create security implication
            security_implication = {
                "id": f"security_implication_{uuid.uuid4()}",
                "relationship": relationship,
                "vulnerability": vulnerability_data,
                "causal_analysis": analysis_result,
                "severity": self._determine_severity(relationship, analysis_result),
            }

            security_implications.append(security_implication)

        # Store security implications
        self.semantic_relationships[job_id] = security_implications
        self.workspace.store_data(
            f"security_implications_{job_id}", security_implications
        )

        return security_implications

    def _create_vulnerability_model_from_relationship(
        self, relationship: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a vulnerability model from a relationship.

        Args:
            relationship: The relationship to analyze

        Returns:
            Vulnerability model for causal reasoning
        """
        source_component = relationship.get("source_component", {})
        target_component = relationship.get("target_component", {})
        flow = relationship.get("flow", {})

        # Create entry points
        entry_points = [
            {
                "id": source_component.get("id", ""),
                "name": source_component.get("name", ""),
                "type": source_component.get("type", ""),
                "description": f"Entry point from {source_component.get('name', '')}",
            }
        ]

        # Create affected components
        affected_components = [
            {
                "id": target_component.get("id", ""),
                "name": target_component.get("name", ""),
                "type": target_component.get("type", ""),
                "description": f"Target component {target_component.get('name', '')}",
            }
        ]

        # Create attack vectors
        attack_vectors = [
            {
                "id": f"vector_{uuid.uuid4()}",
                "name": f"Attack via {flow.get('type', '')} flow",
                "description": f"Attack through {flow.get('type', '')} from {source_component.get('name', '')} to {target_component.get('name', '')}",
            }
        ]

        # Create vulnerability model
        vulnerability_data = {
            "id": f"vulnerability_{uuid.uuid4()}",
            "type": "Trust Boundary Violation",
            "description": f"Potential security vulnerability due to trust boundary crossing from {source_component.get('name', '')} to {target_component.get('name', '')}",
            "severity": "medium",
            "entry_points": entry_points,
            "affected_components": affected_components,
            "attack_vectors": attack_vectors,
        }

        return vulnerability_data

    def _determine_severity(
        self, relationship: Dict[str, Any], analysis_result: Dict[str, Any]
    ) -> str:
        """
        Determine the severity of a security implication.

        Args:
            relationship: The relationship
            analysis_result: The causal analysis result

        Returns:
            Severity level (low, medium, high, critical)
        """
        # Start with medium severity
        severity = "medium"

        # Check critical points from causal analysis
        critical_points = analysis_result.get("critical_points", [])
        if len(critical_points) > 3:
            severity = "high"
        elif len(critical_points) > 5:
            severity = "critical"

        # Check source component security relevance
        source_component = relationship.get("source_component", {})
        source_relevance = source_component.get("security_relevance", 0.0)

        if source_relevance > 0.7:
            # Increase severity for highly security-relevant components
            if severity == "medium":
                severity = "high"
            elif severity == "high":
                severity = "critical"

        # Check if relationship crosses a trust boundary
        if relationship.get("crosses_trust_boundary", False):
            # Increase severity for trust boundary crossings
            if severity == "low":
                severity = "medium"
            elif severity == "medium":
                severity = "high"

        return severity

    async def enhance_threat_model(
        self, threat_model: Dict[str, Any], job_id: str
    ) -> Dict[str, Any]:
        """
        Enhance a threat model with context-aware analysis.

        Args:
            threat_model: The threat model to enhance
            job_id: The ID of the analysis job

        Returns:
            Enhanced threat model
        """
        # Get context model
        context_model = self.context_models.get(job_id)
        if not context_model:
            self.logger.warning(
                f"Context model not found for job {job_id}, threat model enhancement will be limited"
            )
            return threat_model

        # Get security implications
        security_implications = self.semantic_relationships.get(job_id, [])

        # Enhance threats with context information
        enhanced_threats = []

        for threat in threat_model.get("threats", []):
            # Find related security implications
            related_implications = self._find_related_implications(
                threat, security_implications
            )

            # Enhance threat with context information
            enhanced_threat = threat.copy()
            enhanced_threat["context_aware"] = True
            enhanced_threat["related_implications"] = related_implications

            # Add cross-component relationships
            enhanced_threat["cross_component_relationships"] = (
                self._find_related_relationships(
                    threat, context_model.get("relationships", [])
                )
            )

            # Add trust boundary information
            enhanced_threat["trust_boundaries"] = self._find_related_trust_boundaries(
                threat,
                context_model.get("semantic_model", {}).get("trust_boundaries", []),
            )

            enhanced_threats.append(enhanced_threat)

        # Create enhanced threat model
        enhanced_model = threat_model.copy()
        enhanced_model["threats"] = enhanced_threats
        enhanced_model["context_aware"] = True
        enhanced_model["security_implications"] = security_implications

        return enhanced_model

    def _find_related_implications(
        self, threat: Dict[str, Any], security_implications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Find security implications related to a threat.

        Args:
            threat: The threat
            security_implications: List of security implications

        Returns:
            List of related security implications
        """
        related_implications = []

        # Get affected components from threat
        threat_components = set()
        for component in threat.get("affected_components", []):
            component_id = component.get("id", "")
            if component_id:
                threat_components.add(component_id)

        # Find implications that affect the same components
        for implication in security_implications:
            relationship = implication.get("relationship", {})
            source = relationship.get("source_component", {})
            target = relationship.get("target_component", {})

            source_id = source.get("id", "")
            target_id = target.get("id", "")

            if source_id in threat_components or target_id in threat_components:
                related_implications.append(implication)

        return related_implications

    def _find_related_relationships(
        self, threat: Dict[str, Any], relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Find relationships related to a threat.

        Args:
            threat: The threat
            relationships: List of relationships

        Returns:
            List of related relationships
        """
        related_relationships = []

        # Get affected components from threat
        threat_components = set()
        for component in threat.get("affected_components", []):
            component_id = component.get("id", "")
            if component_id:
                threat_components.add(component_id)

        # Find relationships that involve the affected components
        for relationship in relationships:
            source = relationship.get("source_component", {})
            target = relationship.get("target_component", {})

            source_id = source.get("id", "")
            target_id = target.get("id", "")

            if source_id in threat_components or target_id in threat_components:
                related_relationships.append(relationship)

        return related_relationships

    def analyze_codebase_context(self, codebase: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the context of a codebase.
        This is a synchronous wrapper around the async analyze_code_context method.

        Args:
            codebase: The codebase to analyze

        Returns:
            Context analysis results
        """
        # Create a new event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Generate a job ID
        job_id = str(uuid.uuid4())

        # Run the async method in the event loop
        context = loop.run_until_complete(self.analyze_code_context(codebase, job_id))

        # Extract the most relevant information for the test
        result = {
            "application_type": self._determine_application_type(codebase),
            "technologies": self._extract_technologies(codebase),
            "security_features": self._identify_security_features(codebase, context),
        }

        return result

    def _determine_application_type(self, codebase: Dict[str, Any]) -> str:
        """Determine the type of application based on the codebase"""
        files = codebase.get("files", {})
        file_paths = list(files.keys())

        # Check for web application indicators
        web_indicators = [
            ".html",
            ".css",
            ".js",
            "index.html",
            "app.js",
            "routes",
            "views",
            "controllers",
            "flask",
            "django",
            "express",
            "react",
            "angular",
            "vue",
        ]
        for indicator in web_indicators:
            for path in file_paths:
                if indicator in path.lower():
                    return "web"

        # Check for mobile application indicators
        mobile_indicators = [
            "android",
            "ios",
            "swift",
            "kotlin",
            "activity",
            "viewcontroller",
            "manifest.xml",
            "info.plist",
        ]
        for indicator in mobile_indicators:
            for path in file_paths:
                if indicator in path.lower():
                    return "mobile"

        # Check for desktop application indicators
        desktop_indicators = [
            "main.cpp",
            "window",
            "gui",
            "qt",
            "gtk",
            "wx",
            "electron",
        ]
        for indicator in desktop_indicators:
            for path in file_paths:
                if indicator in path.lower():
                    return "desktop"

        # Default to generic
        return "generic"

    def _extract_technologies(self, codebase: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract technologies used in the codebase"""
        files = codebase.get("files", {})
        file_paths = list(files.keys())

        # Identify languages
        languages = set()
        language_extensions = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".c": "c",
            ".cpp": "c++",
            ".cs": "c#",
            ".go": "go",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".rs": "rust",
        }

        for path in file_paths:
            for ext, lang in language_extensions.items():
                if path.endswith(ext):
                    languages.add(lang)

        # Identify frameworks
        frameworks = set()
        framework_indicators = {
            "django": ["django", "settings.py", "urls.py", "views.py"],
            "flask": ["flask", "app.py", "route"],
            "express": ["express", "app.js", "router"],
            "react": ["react", "jsx", "component"],
            "angular": ["angular", "component.ts", "module.ts"],
            "vue": ["vue", ".vue"],
            "spring": ["spring", "application.properties", "controller"],
            "rails": ["rails", "gemfile"],
        }

        for framework, indicators in framework_indicators.items():
            for indicator in indicators:
                for path in file_paths:
                    if indicator in path.lower():
                        frameworks.add(framework)
                        break

        return {"languages": list(languages), "frameworks": list(frameworks)}

    def _identify_security_features(
        self, codebase: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, bool]:
        """Identify security features in the codebase"""
        files = codebase.get("files", {})
        file_contents = list(files.values())

        # Check for authentication
        auth_patterns = [
            "auth",
            "login",
            "password",
            "credential",
            "session",
            "token",
            "jwt",
            "oauth",
            "authenticate",
        ]
        has_auth = any(
            pattern in content.lower()
            for pattern in auth_patterns
            for content in file_contents
        )

        # Check for authorization
        authz_patterns = [
            "authorize",
            "permission",
            "role",
            "access control",
            "acl",
            "rbac",
            "privilege",
        ]
        has_authz = any(
            pattern in content.lower()
            for pattern in authz_patterns
            for content in file_contents
        )

        # Check for encryption
        encryption_patterns = [
            "encrypt",
            "decrypt",
            "crypto",
            "cipher",
            "aes",
            "rsa",
            "hash",
            "md5",
            "sha",
            "ssl",
            "tls",
            "https",
        ]
        has_encryption = any(
            pattern in content.lower()
            for pattern in encryption_patterns
            for content in file_contents
        )

        return {
            "authentication": has_auth,
            "authorization": has_authz,
            "encryption": has_encryption,
        }

    def _find_related_trust_boundaries(
        self, threat: Dict[str, Any], trust_boundaries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Find trust boundaries related to a threat.

        Args:
            threat: The threat
            trust_boundaries: List of trust boundaries

        Returns:
            List of related trust boundaries
        """
        related_boundaries = []

        # Get affected components from threat
        threat_components = set()
        for component in threat.get("affected_components", []):
            component_id = component.get("id", "")
            if component_id:
                threat_components.add(component_id)

        # Find trust boundaries that involve the affected components
        for boundary in trust_boundaries:
            source_id = boundary.get("source_component", "")
            target_id = boundary.get("target_component", "")

            if source_id in threat_components or target_id in threat_components:
                related_boundaries.append(boundary)

        return related_boundaries
