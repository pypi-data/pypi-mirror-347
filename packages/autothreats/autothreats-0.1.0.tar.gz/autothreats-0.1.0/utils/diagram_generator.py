#!/usr/bin/env python3
"""
Diagram generator module for creating Mermaid diagrams from threat model data.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Generator for Mermaid diagrams from threat model data"""

    def __init__(self):
        self.logger = logging.getLogger("DiagramGenerator")

    def generate_threat_flow_diagram(self, threat_model: Dict[str, Any]) -> str:
        """
        Generate a Mermaid flowchart diagram showing threat flows

        Args:
            threat_model: The threat model data

        Returns:
            Mermaid diagram syntax as string
        """
        threats = threat_model.get("threats", [])

        # Start diagram
        diagram = "flowchart TD\n"

        # Add nodes for each component
        components = self._extract_components(threat_model)
        for comp_id, comp_name in components.items():
            diagram += f"    {comp_id}[{comp_name}]\n"

        if not threats:
            # Add a message node when no threats are identified
            message_id = "no_threats_message"
            diagram += f'    {message_id}[/"No threats identified"/]\n'

            # Connect to the system component if it exists
            if "system" in components:
                diagram += f"    {message_id} -.-> system\n"

            # Style the message node
            diagram += f"    style {message_id} fill:#f9f9f9,stroke:#999999,stroke-width:1px,color:#666666,font-style:italic\n"
            return diagram

        # Add threat flows
        for i, threat in enumerate(threats):
            # Ensure threat is a dictionary
            if not isinstance(threat, dict):
                self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                continue

            threat_id = f"threat_{i+1}"
            source = self._get_component_id(
                threat.get("source", "external"), components
            )
            target = self._get_component_id(threat.get("target", "system"), components)
            name = threat.get("name", f"Threat {i+1}")
            severity = threat.get("severity", "medium").lower()

            # Add threat node
            diagram += f"    {threat_id}{{<b>{name}</b>}}\n"

            # Add flow with color based on severity
            color = self._severity_to_color(severity)
            diagram += f"    {source} -->|{severity}| {threat_id}\n"
            diagram += f"    {threat_id} -->|{severity}| {target}\n"

            # Add styling based on severity
            diagram += f"    style {threat_id} fill:{color},color:white\n"

        return diagram

    def generate_attack_tree_diagram(self, threat_model: Dict[str, Any]) -> str:
        """
        Generate a Mermaid diagram showing attack trees

        Args:
            threat_model: The threat model data

        Returns:
            Mermaid diagram syntax as string
        """
        threats = threat_model.get("threats", [])

        # Start diagram
        diagram = "graph TD\n"

        # Create root node
        diagram += '    root["Attack Vectors"]\n'

        if not threats:
            # Add a message node when no threats are identified
            no_threats_id = "no_threats"
            diagram += f'    {no_threats_id}["No threats identified"]\n'
            diagram += f"    root --> {no_threats_id}\n"
            diagram += f"    style {no_threats_id} fill:#f9f9f9,stroke:#999999,stroke-width:1px,color:#666666,font-style:italic\n"
            return diagram

        # Group threats by category
        categories: dict[str, list[tuple[int, dict[str, Any]]]] = {}
        for i, threat in enumerate(threats):
            # Ensure threat is a dictionary
            if not isinstance(threat, dict):
                self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                continue

            category = threat.get("category", "Uncategorized")
            if category not in categories:
                categories[category] = []
            categories[category].append((i, threat))

        # Add category nodes
        for cat_id, category in enumerate(categories.keys()):
            cat_node_id = f"cat_{cat_id+1}"
            diagram += f'    {cat_node_id}["{category}"]\n'
            diagram += f"    root --> {cat_node_id}\n"

            # Add threat nodes for this category
            for i, threat in categories[category]:
                threat_id = f"threat_{i+1}"
                name = threat.get("name", f"Threat {i+1}")
                severity = threat.get("severity", "medium").lower()

                # Add threat node
                diagram += f'    {threat_id}["{name}"]\n'
                diagram += f"    {cat_node_id} --> {threat_id}\n"

                # Add styling based on severity
                color = self._severity_to_color(severity)
                diagram += f"    style {threat_id} fill:{color},color:white\n"

                # Add mitigation nodes if available
                mitigations = threat.get("mitigations", [])
                # Ensure mitigations is a list
                if not isinstance(mitigations, list):
                    self.logger.warning(
                        f"Mitigations is not a list, using empty list instead"
                    )
                    mitigations = []

                for j, mitigation in enumerate(mitigations):
                    # Ensure mitigation is a dictionary
                    if not isinstance(mitigation, dict):
                        self.logger.warning(
                            f"Skipping non-dictionary mitigation: {mitigation}"
                        )
                        continue

                    mit_id = f"mit_{i+1}_{j+1}"
                    mit_name = mitigation.get("name", f"Mitigation {j+1}")
                    diagram += f'    {mit_id}("{mit_name}")\n'
                    diagram += f"    {threat_id} --> {mit_id}\n"
                    diagram += f"    style {mit_id} fill:#90EE90\n"

        return diagram

    def generate_component_diagram(self, threat_model: Dict[str, Any]) -> str:
        """
        Generate a Mermaid component diagram showing system architecture

        Args:
            threat_model: The threat model data

        Returns:
            Mermaid diagram syntax as string
        """
        components = self._extract_components(threat_model)

        # Start diagram
        diagram = "graph LR\n"

        if not components:
            # Add a default component if none are identified
            diagram += '    system["System"]\n'
            diagram += '    no_components["No components identified"]\n'
            diagram += "    system --- no_components\n"
            diagram += "    style no_components fill:#f9f9f9,stroke:#999999,stroke-width:1px,color:#666666,font-style:italic\n"
            return diagram

        # Add nodes for each component
        for comp_id, comp_name in components.items():
            diagram += f"    {comp_id}[{comp_name}]\n"

        # Add connections between components
        connections = threat_model.get("connections", [])

        # If no connections but multiple components, add default connections
        if not connections and len(components) > 1:
            comp_ids = list(components.keys())
            for i in range(len(comp_ids) - 1):
                diagram += f"    {comp_ids[i]} -->|connects to| {comp_ids[i+1]}\n"
        else:
            # Add defined connections
            for i, connection in enumerate(connections):
                # Ensure connection is a dictionary
                if not isinstance(connection, dict):
                    self.logger.warning(
                        f"Skipping non-dictionary connection: {connection}"
                    )
                    continue

                source = self._get_component_id(
                    connection.get("source", ""), components
                )
                target = self._get_component_id(
                    connection.get("target", ""), components
                )
                label = connection.get("type", "connects to")
                diagram += f"    {source} -->|{label}| {target}\n"

        # Add threat indicators
        threats = threat_model.get("threats", [])
        # Ensure threats is a list
        if not isinstance(threats, list):
            self.logger.warning("Threats is not a list, using empty list instead")
            threats = []

        for i, threat in enumerate(threats):
            # Ensure threat is a dictionary
            if not isinstance(threat, dict):
                self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                continue

            target_comp = threat.get("target_component", "")
            if target_comp:
                target = self._get_component_id(target_comp, components)
                severity = threat.get("severity", "medium").lower()
                color = self._severity_to_color(severity)
                diagram += f"    style {target} stroke:{color},stroke-width:4px\n"

        return diagram

    def generate_risk_matrix_diagram(self, threat_model: Dict[str, Any]) -> str:
        """
        Generate a Mermaid diagram showing risk matrix

        Args:
            threat_model: The threat model data

        Returns:
            Mermaid diagram syntax as string
        """
        threats = threat_model.get("threats", [])

        # Start diagram
        diagram = "quadrantChart\n"
        diagram += "    title Risk Matrix\n"
        diagram += "    x-axis Low Impact --> High Impact\n"
        diagram += "    y-axis Low Likelihood --> High Likelihood\n"

        # Add quadrant labels
        diagram += "    quadrant-1 High Risk\n"
        diagram += "    quadrant-2 Medium Risk\n"
        diagram += "    quadrant-3 Low Risk\n"
        diagram += "    quadrant-4 Medium Risk\n"

        if not threats:
            # Add a placeholder point in the low risk quadrant
            diagram += '    "No threats identified": [0.2, 0.2]\n'
            return diagram

        # Add threats as points
        for i, threat in enumerate(threats):
            # Ensure threat is a dictionary
            if not isinstance(threat, dict):
                self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                continue

            name = threat.get("name", f"Threat {i+1}")
            impact = threat.get("impact", 0.5)
            likelihood = threat.get("likelihood", 0.5)

            # Normalize values to 0-1 range if needed
            if isinstance(impact, str):
                impact = self._normalize_risk_value(impact)
            if isinstance(likelihood, str):
                likelihood = self._normalize_risk_value(likelihood)

            diagram += f'    "{name}": [{impact}, {likelihood}]\n'

        return diagram

    def _extract_components(self, threat_model: Dict[str, Any]) -> Dict[str, str]:
        """Extract components from threat model"""
        components: dict[str, str] = {}

        # Extract from components list if available
        components_list = threat_model.get("components", [])
        # Ensure components is a list
        if not isinstance(components_list, list):
            self.logger.warning("Components is not a list, using empty list instead")
            components_list = []

        for comp in components_list:
            # Ensure component is a dictionary
            if not isinstance(comp, dict):
                self.logger.warning(f"Skipping non-dictionary component: {comp}")
                continue

            comp_id = self._sanitize_id(
                comp.get("id", comp.get("name", f"comp_{len(components)+1}"))
            )
            components[comp_id] = comp.get("name", comp_id)

        # Extract from threats if no components defined
        if not components:
            threats = threat_model.get("threats", [])
            # Ensure threats is a list
            if not isinstance(threats, list):
                self.logger.warning("Threats is not a list, using empty list instead")
                threats = []

            for threat in threats:
                # Ensure threat is a dictionary
                if not isinstance(threat, dict):
                    self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                    continue

                source = threat.get("source", "")
                target = threat.get("target", "")

                if source:
                    source_id = self._sanitize_id(source)
                    if source_id not in components:
                        components[source_id] = source

                if target:
                    target_id = self._sanitize_id(target)
                    if target_id not in components:
                        components[target_id] = target

        # Add system component if empty
        if not components:
            components["system"] = "System"

        return components

    def _get_component_id(self, component_name: str, components: Dict[str, str]) -> str:
        """Get component ID from name, or create if not exists"""
        # Handle empty component name
        if not component_name:
            component_name = "Unknown Component"

        # Check if component name exists
        for comp_id, comp_name in components.items():
            if comp_name == component_name:
                return comp_id

        # Create new component ID if not found
        new_id = self._sanitize_id(component_name)

        # Check for ID collision and make unique if needed
        base_id = new_id
        counter = 1
        while new_id in components:
            new_id = f"{base_id}_{counter}"
            counter += 1

        # Add the new component to the components dictionary
        components[new_id] = component_name

        return new_id

    def _sanitize_id(self, name: str) -> str:
        """Convert a name to a valid Mermaid ID"""
        # Handle empty or None input
        if not name:
            return "unknown_id"

        # Replace spaces and special chars with underscore
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = "n_" + sanitized
        # Ensure we have a valid ID (not empty)
        if not sanitized:
            sanitized = "unknown_id"
        return sanitized

    def _severity_to_color(self, severity: str) -> str:
        """Convert severity to color"""
        severity_colors = {
            "critical": "#CC0000",  # Dark red
            "high": "#FF0000",  # Red
            "medium": "#FFA500",  # Orange
            "low": "#FFFF00",  # Yellow
            "info": "#00BFFF",  # Blue
        }
        return severity_colors.get(severity.lower(), "#808080")  # Default gray

    def _normalize_risk_value(self, value: str) -> float:
        """Convert string risk values to normalized float"""
        value_map = {
            "critical": 0.9,
            "high": 0.7,
            "medium": 0.5,
            "low": 0.3,
            "info": 0.1,
        }
        return value_map.get(value.lower(), 0.5)

    def _generate_empty_diagram(self, message: str) -> str:
        """Generate an empty diagram with a message"""
        # Create a unique ID for the empty node
        node_id = f"empty_{hash(message) % 10000}"

        return f"""graph TD
    {node_id}["{message}"]
    style {node_id} fill:#f9f9f9,stroke:#999999,stroke-width:1px,color:#666666,font-style:italic
    classDef empty-message font-style:italic,color:#666666
    class {node_id} empty-message
"""


def generate_all_diagrams(threat_model: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate all diagram types for a threat model

    Args:
        threat_model: The threat model data

    Returns:
        Dictionary of diagram name to Mermaid syntax
    """
    # Check if threat_model is a string and try to convert it
    if isinstance(threat_model, str):
        try:
            logger.info(
                "Converting string threat model to dictionary for diagram generation"
            )
            threat_model = json.loads(threat_model)
        except json.JSONDecodeError:
            logger.error(
                "Failed to parse threat model string as JSON for diagram generation"
            )
            # Return empty diagrams if parsing fails
            return {
                "threat_flow": 'graph TD\n    error["Error parsing threat model"]',
                "attack_tree": 'graph TD\n    error["Error parsing threat model"]',
                "component": 'graph LR\n    error["Error parsing threat model"]',
                "risk_matrix": 'quadrantChart\n    title Risk Matrix\n    x-axis Low Impact --> High Impact\n    y-axis Low Likelihood --> High Likelihood\n    "Error": [0.5, 0.5]',
            }

    generator = DiagramGenerator()

    # Initialize with empty diagrams
    diagrams = {
        "threat_flow": 'graph TD\n    error["Error generating diagram"]',
        "attack_tree": 'graph TD\n    error["Error generating diagram"]',
        "component": 'graph LR\n    error["Error generating diagram"]',
        "risk_matrix": 'quadrantChart\n    title Risk Matrix\n    x-axis Low Impact --> High Impact\n    y-axis Low Likelihood --> High Likelihood\n    "Error": [0.5, 0.5]',
    }

    # Try to generate each diagram separately to prevent one failure from affecting others
    try:
        diagrams["threat_flow"] = generator.generate_threat_flow_diagram(threat_model)
    except Exception as e:
        import traceback

        logger.error(f"Error generating threat flow diagram: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        diagrams["attack_tree"] = generator.generate_attack_tree_diagram(threat_model)
    except Exception as e:
        import traceback

        logger.error(f"Error generating attack tree diagram: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        diagrams["component"] = generator.generate_component_diagram(threat_model)
    except Exception as e:
        import traceback

        logger.error(f"Error generating component diagram: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    try:
        diagrams["risk_matrix"] = generator.generate_risk_matrix_diagram(threat_model)
    except Exception as e:
        import traceback

        logger.error(f"Error generating risk matrix diagram: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")

    return diagrams
