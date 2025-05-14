#!/usr/bin/env python3
"""
Report generator module for creating HTML reports with Mermaid diagrams.
"""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .diagram_generator import generate_all_diagrams

logger = logging.getLogger(__name__)

try:
    import jinja2

    JINJA2_AVAILABLE = True
except ImportError:
    logger.warning(
        "Jinja2 library not available. HTML report generation will be disabled."
    )
    JINJA2_AVAILABLE = False


class ReportGenerator:
    """Generator for HTML reports with Mermaid diagrams"""

    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the report generator

        Args:
            template_dir: Directory containing templates (optional)
        """
        self.logger = logging.getLogger("ReportGenerator")

        # Set template directory
        if template_dir:
            self.template_dir = template_dir
        else:
            # Use default template directory
            module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.template_dir = os.path.join(module_dir, "templates")

        self.logger.info(f"Using template directory: {self.template_dir}")

        # Initialize Jinja2 environment if available
        if JINJA2_AVAILABLE:
            self.jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.template_dir),
                autoescape=jinja2.select_autoescape(["html", "xml"]),
            )
        else:
            self.jinja_env = None

    def generate_html_report(
        self, threat_model: Dict[str, Any], version: str = "0.1.0"
    ) -> str:
        """
        Generate an HTML report with Mermaid diagrams

        Args:
            threat_model: The threat model data
            version: Version string

        Returns:
            HTML report as string
        """
        if not JINJA2_AVAILABLE:
            self.logger.error(
                "Jinja2 library not available. Cannot generate HTML report."
            )
            return self._generate_fallback_html(threat_model)

        try:
            # Check if threat_model is a string (possibly JSON) and convert to dict if needed
            if isinstance(threat_model, str):
                try:
                    self.logger.info("Converting string threat model to dictionary")
                    threat_model = json.loads(threat_model)
                except json.JSONDecodeError:
                    self.logger.error("Failed to parse threat model string as JSON")
                    return self._generate_fallback_html(
                        {"error": "Invalid threat model format"}
                    )

            # Generate diagrams
            diagrams = generate_all_diagrams(threat_model)

            # Prepare template data
            template_data = self._prepare_template_data(threat_model, diagrams, version)

            # Render template
            template = self.jinja_env.get_template("report_template.html")
            html_report = template.render(**template_data)

            return html_report

        except Exception as e:
            self.logger.error(f"Error generating HTML report: {e}")
            # Ensure threat_model is a dictionary before passing to _generate_fallback_html
            if isinstance(threat_model, str):
                try:
                    threat_model = json.loads(threat_model)
                except json.JSONDecodeError:
                    threat_model = {"project_name": "Error", "threats": []}
            return self._generate_fallback_html(threat_model)

    def save_html_report(
        self, threat_model: Dict[str, Any], output_path: str, version: str = "0.1.0"
    ) -> str:
        """
        Generate and save an HTML report

        Args:
            threat_model: The threat model data
            output_path: Path to save the report
            version: Version string

        Returns:
            Path to the saved report
        """
        # Check if threat_model is a string and try to convert it
        if isinstance(threat_model, str):
            try:
                self.logger.info(
                    "Converting string threat model to dictionary for saving report"
                )
                threat_model = json.loads(threat_model)
            except json.JSONDecodeError:
                self.logger.error(
                    "Failed to parse threat model string as JSON for saving report"
                )
                threat_model = {"project_name": "Error", "threats": []}

        try:
            html_report = self.generate_html_report(threat_model, version)

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

            # Write report to file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_report)

            self.logger.info(f"HTML report saved to {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error saving HTML report: {e}")
            # Generate a fallback HTML file if there's an error
            try:
                # Ensure threat_model is a dictionary
                if isinstance(threat_model, str):
                    try:
                        threat_model = json.loads(threat_model)
                    except json.JSONDecodeError:
                        threat_model = {"project_name": "Error", "threats": []}

                fallback_html = self._generate_fallback_html(threat_model)

                # Try to save the fallback HTML
                os.makedirs(
                    os.path.dirname(os.path.abspath(output_path)), exist_ok=True
                )
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(fallback_html)

                self.logger.info(f"Fallback HTML report saved to {output_path}")
                return output_path
            except Exception as inner_e:
                self.logger.error(f"Error saving fallback HTML report: {inner_e}")
                return ""

    def _prepare_template_data(
        self, threat_model: Dict[str, Any], diagrams: Dict[str, str], version: str
    ) -> Dict[str, Any]:
        """Prepare data for the template"""
        # Extract basic information
        project_name = threat_model.get("project_name", "Unnamed Project")

        # Count threats by severity
        threats = threat_model.get("threats", [])
        # Ensure threats is a list
        if not isinstance(threats, list):
            self.logger.warning("Threats is not a list, using empty list instead")
            threats = []

        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

        for threat in threats:
            # Ensure threat is a dictionary
            if not isinstance(threat, dict):
                self.logger.warning(f"Skipping non-dictionary threat: {threat}")
                continue

            severity = threat.get("severity", "medium").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1

        # Generate executive summary if not provided
        executive_summary = threat_model.get("executive_summary", "")
        if not executive_summary:
            executive_summary = self._generate_executive_summary(
                threat_model, severity_counts
            )

        # Generate system description if not provided
        system_description = threat_model.get("system_description", "")
        if not system_description:
            system_description = self._generate_system_description(threat_model)

        # Prepare template data
        template_data = {
            "report_title": f"Threat Model: {project_name}",
            "generation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": executive_summary,
            "system_description": system_description,
            "total_threats": len(threats),
            "critical_threats": severity_counts["critical"],
            "high_threats": severity_counts["high"],
            "medium_threats": severity_counts["medium"],
            "low_threats": severity_counts["low"],
            "threats": threats,
            "recommendations": self._ensure_list(
                threat_model.get("recommendations", [])
            ),
            "component_diagram": self._get_diagram(diagrams, "component"),
            "threat_flow_diagram": self._get_diagram(diagrams, "threat_flow"),
            "attack_tree_diagram": self._get_diagram(diagrams, "attack_tree"),
            "risk_matrix_diagram": self._get_diagram(diagrams, "risk_matrix"),
            "commit_history_analysis": self._ensure_dict(
                threat_model.get("commit_history_analysis", {})
            ),
            "version": version,
            "current_year": datetime.datetime.now().year,
        }

        return template_data

    def _ensure_list(self, value: Any) -> List[Any]:
        """Ensure that a value is a list"""
        if value is None:
            return []
        if isinstance(value, list):
            return value
        self.logger.warning(f"Converting non-list value to list: {value}")
        return [value]

    def _ensure_dict(self, value: Any) -> Dict[str, Any]:
        """Ensure that a value is a dictionary"""
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                # Try to parse as JSON
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    self.logger.warning(
                        f"Converted string to dictionary via JSON parsing"
                    )
                    return parsed
            except json.JSONDecodeError:
                pass
        self.logger.warning(f"Converting non-dict value to empty dict: {value}")
        return {}

    def _get_diagram(self, diagrams: Dict[str, str], diagram_type: str) -> str:
        """Safely get a diagram from the diagrams dictionary"""
        if not isinstance(diagrams, dict):
            self.logger.warning(f"Diagrams is not a dictionary: {diagrams}")
            return f'graph TD\n    error["Error: Invalid diagrams data"]'

        diagram = diagrams.get(diagram_type, "")
        if not diagram:
            self.logger.warning(f"Missing {diagram_type} diagram")
            return f'graph TD\n    error["No {diagram_type} diagram available"]'

        return diagram

    def _generate_executive_summary(
        self, threat_model: Dict[str, Any], severity_counts: Dict[str, int]
    ) -> str:
        """Generate an executive summary if not provided"""
        project_name = threat_model.get("project_name", "the system")
        total_threats = sum(severity_counts.values())

        if total_threats == 0:
            return f"No security threats were identified in {project_name}."

        critical_high = severity_counts["critical"] + severity_counts["high"]

        if critical_high > 0:
            risk_level = "high"
        elif severity_counts["medium"] > 0:
            risk_level = "moderate"
        else:
            risk_level = "low"

        summary = f"The security analysis of {project_name} identified {total_threats} potential threats, "
        summary += f"including {severity_counts['critical']} critical, {severity_counts['high']} high, "
        summary += f"{severity_counts['medium']} medium, and {severity_counts['low']} low severity issues. "
        summary += (
            f"Overall, the system presents a {risk_level} level of security risk. "
        )

        if critical_high > 0:
            summary += "Immediate attention is recommended for the critical and high severity threats."
        elif severity_counts["medium"] > 0:
            summary += "Addressing the medium severity threats is recommended as part of regular security maintenance."
        else:
            summary += "The identified low severity threats should be monitored as part of routine security practices."

        return summary

    def _generate_system_description(self, threat_model: Dict[str, Any]) -> str:
        """Generate a system description if not provided"""
        project_name = threat_model.get("project_name", "The system")
        components = threat_model.get("components", [])

        # Ensure components is a list
        if not isinstance(components, list):
            self.logger.warning("Components is not a list, using empty list instead")
            components = []

        if not components:
            return f"{project_name} was analyzed for security threats. No detailed system information was provided."

        description = f"{project_name} consists of {len(components)} main components. "

        # List components
        component_names = []
        for i, comp in enumerate(components):
            # Ensure component is a dictionary
            if not isinstance(comp, dict):
                self.logger.warning(f"Skipping non-dictionary component: {comp}")
                component_names.append(f"Component {i+1}")
            else:
                component_names.append(comp.get("name", f"Component {i+1}"))
        if len(component_names) > 1:
            description += (
                "These include "
                + ", ".join(component_names[:-1])
                + f" and {component_names[-1]}. "
            )
        else:
            description += f"This includes {component_names[0]}. "

        # Add data flows if available
        connections = threat_model.get("connections", [])
        # Ensure connections is a list
        if not isinstance(connections, list):
            self.logger.warning("Connections is not a list, using empty list instead")
            connections = []

        if connections:
            description += f"There are {len(connections)} identified data flows between components. "

        return description

    def _generate_fallback_html(self, threat_model: Dict[str, Any]) -> str:
        """Generate a simple HTML report when Jinja2 is not available"""
        # Check if threat_model is a string and try to convert it
        if isinstance(threat_model, str):
            try:
                threat_model = json.loads(threat_model)
            except json.JSONDecodeError:
                threat_model = {"project_name": "Error", "threats": []}

        project_name = threat_model.get("project_name", "Unnamed Project")
        threats = threat_model.get("threats", [])

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Threat Model: {project_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2 {{ color: #0066cc; }}
        .threat {{ margin: 10px 0; padding: 10px; border: 1px solid #ccc; }}
        .critical {{ background-color: #ffcccc; }}
        .high {{ background-color: #ffddcc; }}
        .medium {{ background-color: #ffffcc; }}
        .low {{ background-color: #ccffcc; }}
    </style>
</head>
<body>
    <h1>Threat Model: {project_name}</h1>
    <p>Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <h2>Identified Threats</h2>
"""

        for threat in threats:
            name = threat.get("name", "Unnamed Threat")
            severity = threat.get("severity", "medium").lower()
            description = threat.get("description", "No description provided.")

            html += f"""
    <div class="threat {severity}">
        <h3>{name} ({severity.upper()})</h3>
        <p>{description}</p>
    </div>
"""

        html += """
    <p>Note: This is a simplified report. Install Jinja2 for full report generation.</p>
</body>
</html>
"""

        return html


def generate_html_report(
    threat_model: Dict[str, Any],
    output_path: Optional[str] = None,
    version: str = "0.1.0",
) -> str:
    """
    Generate an HTML report with Mermaid diagrams

    Args:
        threat_model: The threat model data
        output_path: Path to save the report (optional)
        version: Version string

    Returns:
        HTML report as string or path to saved report if output_path is provided
    """
    generator = ReportGenerator()

    # Check if threat_model is a string (possibly JSON) and convert to dict if needed
    if isinstance(threat_model, str):
        try:
            logger.info("Converting string threat model to dictionary")
            threat_model = json.loads(threat_model)
        except json.JSONDecodeError:
            logger.error("Failed to parse threat model string as JSON")
            return generator._generate_fallback_html(
                {"error": "Invalid threat model format"}
            )

    try:
        if output_path:
            return generator.save_html_report(threat_model, output_path, version)
        else:
            return generator.generate_html_report(threat_model, version)
    except Exception as e:
        logger.error(f"Error in standalone generate_html_report: {e}")
        # Ensure threat_model is a dictionary before passing to _generate_fallback_html
        if isinstance(threat_model, str):
            try:
                threat_model = json.loads(threat_model)
            except json.JSONDecodeError:
                threat_model = {"project_name": "Error", "threats": []}
        return generator._generate_fallback_html(threat_model)
