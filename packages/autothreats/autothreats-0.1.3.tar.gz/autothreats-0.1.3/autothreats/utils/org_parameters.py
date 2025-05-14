#!/usr/bin/env python3
"""
Organization Parameters module for the autonomous threat modeling system.
Responsible for loading and managing organization-specific parameters.
"""

import logging
import os
from typing import Any, Collection, Dict, List, Mapping, Optional, cast

import yaml
from typing_extensions import TypeAlias

# Add type stubs for yaml
YAMLData: TypeAlias = Mapping[str, Any]

logger = logging.getLogger(__name__)


class OrganizationParameters:
    """Class for managing organization-specific parameters"""

    def __init__(self, yaml_path: Optional[str] = None):
        """Initialize organization parameters"""
        self.parameters = {
            "security_controls": {},
            "compliance_requirements": [],
            "risk_tolerance": "medium",
            "industry_sector": "general",
            "organization_size": "medium",
            "security_maturity": "medium",
            "custom_mitigations": {},
            "custom_threats": {},
            "excluded_threats": [],
            "priority_threats": [],
        }

        if yaml_path:
            self.load_from_yaml(yaml_path)

    def load_from_yaml(self, yaml_path: str) -> bool:
        """Load organization parameters from YAML file"""
        try:
            if not os.path.exists(yaml_path):
                logger.error(f"YAML file not found: {yaml_path}")
                return False

            with open(yaml_path, "r", errors="replace") as file:
                yaml_data = yaml.safe_load(file)

            if not yaml_data or not isinstance(yaml_data, dict):
                logger.error(f"Invalid YAML format in {yaml_path}")
                return False

            # Update parameters with YAML data
            if "security_controls" in yaml_data and isinstance(
                yaml_data["security_controls"], dict
            ):
                self.parameters["security_controls"] = yaml_data["security_controls"]

            if "compliance_requirements" in yaml_data and isinstance(
                yaml_data["compliance_requirements"], list
            ):
                self.parameters["compliance_requirements"] = yaml_data[
                    "compliance_requirements"
                ]

            if "risk_tolerance" in yaml_data and isinstance(
                yaml_data["risk_tolerance"], str
            ):
                self.parameters["risk_tolerance"] = yaml_data["risk_tolerance"].lower()

            if "industry_sector" in yaml_data and isinstance(
                yaml_data["industry_sector"], str
            ):
                self.parameters["industry_sector"] = yaml_data[
                    "industry_sector"
                ].lower()

            if "organization_size" in yaml_data and isinstance(
                yaml_data["organization_size"], str
            ):
                self.parameters["organization_size"] = yaml_data[
                    "organization_size"
                ].lower()

            if "security_maturity" in yaml_data and isinstance(
                yaml_data["security_maturity"], str
            ):
                self.parameters["security_maturity"] = yaml_data[
                    "security_maturity"
                ].lower()

            if "custom_mitigations" in yaml_data and isinstance(
                yaml_data["custom_mitigations"], dict
            ):
                self.parameters["custom_mitigations"] = yaml_data["custom_mitigations"]

            if "custom_threats" in yaml_data and isinstance(
                yaml_data["custom_threats"], dict
            ):
                self.parameters["custom_threats"] = yaml_data["custom_threats"]

            if "excluded_threats" in yaml_data and isinstance(
                yaml_data["excluded_threats"], list
            ):
                self.parameters["excluded_threats"] = yaml_data["excluded_threats"]

            if "priority_threats" in yaml_data and isinstance(
                yaml_data["priority_threats"], list
            ):
                self.parameters["priority_threats"] = yaml_data["priority_threats"]

            logger.info(f"Successfully loaded organization parameters from {yaml_path}")
            return True

        except Exception as e:
            logger.error(
                f"Error loading organization parameters from {yaml_path}: {str(e)}"
            )
            return False

    def get_security_control(self, control_name: str) -> Mapping[str, Any]:
        """Get information about a specific security control"""
        return self.parameters["security_controls"].get(control_name, {})

    def has_security_control(self, control_name: str) -> bool:
        """Check if a specific security control is implemented"""
        control = self.get_security_control(control_name)
        return control.get("implemented", False)

    def get_security_control_strength(self, control_name: str) -> str:
        """Get the strength of a specific security control"""
        control = self.get_security_control(control_name)
        return control.get("strength", "medium")

    def get_compliance_requirements(self) -> List[str]:
        """Get the list of compliance requirements"""
        return cast(List[str], self.parameters["compliance_requirements"])

    def get_risk_tolerance(self) -> str:
        """Get the organization's risk tolerance"""
        return cast(str, self.parameters["risk_tolerance"])

    def get_industry_sector(self) -> str:
        """Get the organization's industry sector"""
        return cast(str, self.parameters["industry_sector"])

    def get_organization_size(self) -> str:
        """Get the organization's size"""
        return cast(str, self.parameters["organization_size"])

    def get_security_maturity(self) -> str:
        """Get the organization's security maturity level"""
        return cast(str, self.parameters["security_maturity"])

    def get_custom_mitigations(self, threat_type: str) -> List[str]:
        """Get custom mitigations for a specific threat type"""
        mitigations = self.parameters["custom_mitigations"].get(threat_type, [])
        return cast(List[str], mitigations)

    def get_custom_threats(self, category: str) -> List[Mapping[str, Any]]:
        """Get custom threats for a specific category"""
        threats = self.parameters["custom_threats"].get(category, [])
        return cast(List[Mapping[str, Any]], threats)

    def is_threat_excluded(self, threat_name: str) -> bool:
        """Check if a specific threat is excluded"""
        return threat_name in self.parameters["excluded_threats"]

    def is_threat_priority(self, threat_name: str) -> bool:
        """Check if a specific threat is a priority"""
        return threat_name in self.parameters["priority_threats"]

    def adjust_risk_score(self, threat_name: str, base_score: int) -> int:
        """Adjust risk score based on organization parameters"""
        # Adjust based on risk tolerance
        risk_tolerance = cast(str, self.parameters["risk_tolerance"])
        risk_tolerance_factor = {
            "low": 1.2,  # Low tolerance = higher risk scores
            "medium": 1.0,  # Medium tolerance = unchanged risk scores
            "high": 0.8,  # High tolerance = lower risk scores
        }.get(risk_tolerance, 1.0)

        # Adjust based on security maturity
        security_maturity = cast(str, self.parameters["security_maturity"])
        security_maturity_factor = {
            "low": 1.2,  # Low maturity = higher risk scores
            "medium": 1.0,  # Medium maturity = unchanged risk scores
            "high": 0.8,  # High maturity = lower risk scores
        }.get(security_maturity, 1.0)

        # Adjust based on priority
        priority_factor = 1.5 if self.is_threat_priority(threat_name) else 1.0

        # Calculate adjusted score
        adjusted_score = (
            base_score
            * risk_tolerance_factor
            * security_maturity_factor
            * priority_factor
        )

        # Ensure score is between 1-10
        return max(1, min(10, round(adjusted_score)))

    def get_all_parameters(self) -> Mapping[str, Any]:
        """Get all organization parameters"""
        return self.parameters
