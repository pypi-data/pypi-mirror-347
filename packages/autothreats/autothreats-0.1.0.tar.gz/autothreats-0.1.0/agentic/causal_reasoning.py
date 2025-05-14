#!/usr/bin/env python3
"""
Causal Reasoning module for the autonomous threat modeling system.
Enables agents to reason about cause-effect relationships in security vulnerabilities.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class CausalReasoning:
    """
    Enables agents to reason about cause-effect relationships in security vulnerabilities
    and generate counterfactual scenarios to test security assumptions.
    """

    def __init__(self, workspace):
        """
        Initialize the causal reasoning framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.causal_graphs = {}
        self.counterfactuals = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def construct_causal_graph(
        self, vulnerability_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Construct a causal graph for a vulnerability.

        Args:
            vulnerability_data: Data about the vulnerability

        Returns:
            A causal graph representing cause-effect relationships
        """
        graph_id = str(uuid.uuid4())

        # Extract key elements from vulnerability data
        vuln_type = vulnerability_data.get("type", "unknown")
        entry_points = vulnerability_data.get("entry_points", [])
        affected_components = vulnerability_data.get("affected_components", [])
        attack_vectors = vulnerability_data.get("attack_vectors", [])

        # Create nodes for the causal graph
        nodes = {
            "entry_points": entry_points,
            "components": affected_components,
            "attack_vectors": attack_vectors,
            "vulnerability": {
                "id": vulnerability_data.get("id", ""),
                "type": vuln_type,
                "description": vulnerability_data.get("description", ""),
                "severity": vulnerability_data.get("severity", "medium"),
            },
        }

        # Create edges (causal relationships)
        edges = []

        # Entry points lead to affected components
        for entry in entry_points:
            for component in affected_components:
                edges.append(
                    {
                        "from": f"entry:{entry.get('id', '')}",
                        "to": f"component:{component.get('id', '')}",
                        "relationship": "accesses",
                    }
                )

        # Components contain the vulnerability
        for component in affected_components:
            edges.append(
                {
                    "from": f"component:{component.get('id', '')}",
                    "to": f"vulnerability:{vulnerability_data.get('id', '')}",
                    "relationship": "contains",
                }
            )

        # Vulnerability enables attack vectors
        for vector in attack_vectors:
            edges.append(
                {
                    "from": f"vulnerability:{vulnerability_data.get('id', '')}",
                    "to": f"vector:{vector.get('id', '')}",
                    "relationship": "enables",
                }
            )

        # Create the complete graph
        causal_graph = {
            "id": graph_id,
            "vulnerability_id": vulnerability_data.get("id", ""),
            "nodes": nodes,
            "edges": edges,
            "created_at": asyncio.get_event_loop().time(),
        }

        # Store in memory and workspace
        self.causal_graphs[graph_id] = causal_graph
        self.workspace.store_data(f"causal_graph_{graph_id}", causal_graph)

        self.logger.info(
            f"Created causal graph {graph_id} for vulnerability {vulnerability_data.get('id', '')}"
        )

        return causal_graph

    def identify_critical_nodes(
        self, causal_graph: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify critical nodes in a causal graph.

        Args:
            causal_graph: The causal graph to analyze

        Returns:
            List of critical nodes
        """
        if not causal_graph:
            return []

        # Get graph elements
        nodes = causal_graph.get("nodes", {})
        edges = causal_graph.get("edges", [])

        # Calculate node centrality (number of connections)
        centrality = {}
        for edge in edges:
            from_node = edge.get("from", "")
            to_node = edge.get("to", "")

            centrality[from_node] = centrality.get(from_node, 0) + 1
            centrality[to_node] = centrality.get(to_node, 0) + 1

        # Identify critical nodes (high centrality)
        critical_nodes = []
        for node_id, count in centrality.items():
            if count >= 2:  # Nodes with at least 2 connections
                node_type, node_id_value = node_id.split(":", 1)

                # Find the node data
                node_data = None
                if node_type == "entry":
                    for entry in nodes.get("entry_points", []):
                        if entry.get("id", "") == node_id_value:
                            node_data = entry
                            break
                elif node_type == "component":
                    for component in nodes.get("components", []):
                        if component.get("id", "") == node_id_value:
                            node_data = component
                            break
                elif node_type == "vulnerability":
                    node_data = nodes.get("vulnerability")
                elif node_type == "vector":
                    for vector in nodes.get("attack_vectors", []):
                        if vector.get("id", "") == node_id_value:
                            node_data = vector
                            break

                if node_data:
                    critical_nodes.append(
                        {
                            "id": node_id,
                            "type": node_type,
                            "data": node_data,
                            "centrality": count,
                        }
                    )

        # Sort by centrality (descending)
        critical_nodes.sort(key=lambda x: x["centrality"], reverse=True)

        return critical_nodes

    def generate_counterfactuals(
        self, causal_graph: Dict[str, Any], critical_nodes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate counterfactual scenarios for a causal graph.

        Args:
            causal_graph: The causal graph to analyze
            critical_nodes: List of critical nodes

        Returns:
            List of counterfactual scenarios
        """
        if not causal_graph or not critical_nodes:
            return []

        counterfactuals = []
        graph_id = causal_graph.get("id", "")
        vulnerability_id = causal_graph.get("vulnerability_id", "")

        # Generate counterfactuals for each critical node
        for node in critical_nodes:
            node_id = node.get("id", "")
            node_type = node.get("type", "")

            # Skip vulnerability nodes (we want to focus on preventable elements)
            if node_type == "vulnerability":
                continue

            # Create counterfactual scenario
            counterfactual_id = str(uuid.uuid4())
            counterfactual = {
                "id": counterfactual_id,
                "graph_id": graph_id,
                "vulnerability_id": vulnerability_id,
                "modified_node": node,
                "scenario": self._generate_scenario_for_node(node, causal_graph),
                "mitigation": self._generate_mitigation_for_node(node, causal_graph),
                "created_at": asyncio.get_event_loop().time(),
            }

            counterfactuals.append(counterfactual)

        # Store counterfactuals
        self.counterfactuals[graph_id] = counterfactuals
        self.workspace.store_data(f"counterfactuals_{graph_id}", counterfactuals)

        self.logger.info(
            f"Generated {len(counterfactuals)} counterfactual scenarios for graph {graph_id}"
        )

        return counterfactuals

    def _generate_scenario_for_node(
        self, node: Dict[str, Any], causal_graph: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a counterfactual scenario for a specific node.

        Args:
            node: The node to generate a scenario for
            causal_graph: The causal graph

        Returns:
            A counterfactual scenario
        """
        node_type = node.get("type", "")
        node_data = node.get("data", {})

        if node_type == "entry":
            # What if this entry point was secured?
            return {
                "title": f"Secure entry point: {node_data.get('name', '')}",
                "description": f"What if the entry point {node_data.get('name', '')} implemented proper authentication and authorization?",
                "impact": "This would prevent unauthorized access to the affected components, potentially preventing the vulnerability from being exploited.",
            }
        elif node_type == "component":
            # What if this component was hardened?
            return {
                "title": f"Harden component: {node_data.get('name', '')}",
                "description": f"What if the component {node_data.get('name', '')} was hardened against the specific vulnerability type?",
                "impact": "This would eliminate the vulnerability at its source, preventing all associated attack vectors.",
            }
        elif node_type == "vector":
            # What if this attack vector was mitigated?
            return {
                "title": f"Mitigate attack vector: {node_data.get('name', '')}",
                "description": f"What if the attack vector {node_data.get('name', '')} was specifically mitigated?",
                "impact": "This would prevent exploitation of the vulnerability through this specific attack path, though other vectors might still exist.",
            }
        else:
            # Generic scenario
            return {
                "title": "Implement security controls",
                "description": "What if appropriate security controls were implemented at this point in the system?",
                "impact": "This would reduce the likelihood of successful exploitation.",
            }

    def _generate_mitigation_for_node(
        self, node: Dict[str, Any], causal_graph: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a mitigation for a specific node.

        Args:
            node: The node to generate a mitigation for
            causal_graph: The causal graph

        Returns:
            A mitigation strategy
        """
        node_type = node.get("type", "")
        node_data = node.get("data", {})

        if node_type == "entry":
            # Mitigation for entry points
            return {
                "title": "Implement access controls",
                "description": f"Implement strong authentication and authorization for the {node_data.get('name', '')} entry point.",
                "steps": [
                    "Require authentication for all access",
                    "Implement proper authorization checks",
                    "Validate all input parameters",
                    "Implement rate limiting to prevent brute force attacks",
                ],
                "effort": "medium",
            }
        elif node_type == "component":
            # Mitigation for components
            return {
                "title": "Secure component implementation",
                "description": f"Harden the {node_data.get('name', '')} component against potential vulnerabilities.",
                "steps": [
                    "Review and refactor code to follow secure coding practices",
                    "Implement input validation and output encoding",
                    "Add security unit tests",
                    "Consider using a more secure library or framework",
                ],
                "effort": "high",
            }
        elif node_type == "vector":
            # Mitigation for attack vectors
            return {
                "title": "Block attack vector",
                "description": f"Implement specific controls to block the {node_data.get('name', '')} attack vector.",
                "steps": [
                    "Add specific validation for this attack pattern",
                    "Implement monitoring for this attack pattern",
                    "Add security headers or other protective measures",
                ],
                "effort": "medium",
            }
        else:
            # Generic mitigation
            return {
                "title": "Implement defense in depth",
                "description": "Add multiple layers of security controls.",
                "steps": [
                    "Review security architecture",
                    "Implement appropriate controls",
                    "Test effectiveness of controls",
                ],
                "effort": "medium",
            }

    def analyze_attack_path(self, vulnerability_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an attack path for a vulnerability.

        Args:
            vulnerability_data: Data about the vulnerability

        Returns:
            Analysis results including causal graph, critical points, and counterfactuals
        """
        # Construct the causal graph
        causal_graph = self.construct_causal_graph(vulnerability_data)

        # Identify critical nodes
        critical_points = self.identify_critical_nodes(causal_graph)

        # Generate counterfactual scenarios
        counterfactuals = self.generate_counterfactuals(causal_graph, critical_points)

        # Return the complete analysis
        return {
            "vulnerability_id": vulnerability_data.get("id", ""),
            "causal_graph": causal_graph,
            "critical_points": critical_points,
            "counterfactuals": counterfactuals,
        }

    def get_causal_graph(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a causal graph by ID.

        Args:
            graph_id: The ID of the causal graph

        Returns:
            The causal graph or None if not found
        """
        return self.causal_graphs.get(graph_id)

    def get_counterfactuals(self, graph_id: str) -> List[Dict[str, Any]]:
        """
        Get counterfactuals for a causal graph.

        Args:
            graph_id: The ID of the causal graph

        Returns:
            List of counterfactual scenarios
        """
        return self.counterfactuals.get(graph_id, [])
