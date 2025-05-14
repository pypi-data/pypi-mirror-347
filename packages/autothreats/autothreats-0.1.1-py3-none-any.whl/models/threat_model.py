#!/usr/bin/env python3
"""
Threat model for the autonomous threat modeling system.
"""

import uuid
from typing import Any, Dict, List, Mapping, Optional


class ThreatScenarioModel:
    """Model for threat scenarios"""

    def __init__(self, scenario_id: str, name: str):
        self.id = scenario_id
        self.name = name
        self.description = ""
        self.attacker_profile = ""
        self.attack_vector = ""
        self.impact = ""
        self.likelihood = 0.0  # 0.0 to 1.0
        self.affected_components: List[str] = []

    def to_dict(self) -> Mapping[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "attacker_profile": self.attacker_profile,
            "attack_vector": self.attack_vector,
            "impact": self.impact,
            "likelihood": self.likelihood,
            "affected_components": self.affected_components,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatScenarioModel":
        """Create a ThreatScenarioModel from a dictionary"""
        scenario_id = data.get("id", str(uuid.uuid4()))
        scenario = cls(scenario_id, data.get("name", "Unnamed Scenario"))
        scenario.description = data.get("description", "")
        scenario.attacker_profile = data.get("attacker_profile", "")
        scenario.attack_vector = data.get("attack_vector", "")
        scenario.impact = data.get("impact", "")
        scenario.likelihood = data.get("likelihood", 0.0)
        scenario.affected_components = data.get("affected_components", [])
        return scenario


class VulnerabilityModel:
    """Model for vulnerabilities"""

    def __init__(
        self,
        id: str = None,
        name: str = "",
        cwe_id: str = "",
        description: str = "",
        file: str = "",
        line: int = 0,
        severity: str = "medium",
        affected_components: List[str] = None,
        detection_confidence: str = "medium",
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.cwe_id = cwe_id
        self.cvss_score = 0.0
        self.affected_components = affected_components or []
        self.remediation = ""
        self.file = file
        self.line = line
        self.severity = severity
        self.detection_confidence = detection_confidence

    def to_dict(self) -> Mapping[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cwe_id": self.cwe_id,
            "cvss_score": self.cvss_score,
            "affected_components": self.affected_components,
            "remediation": self.remediation,
            "file": self.file,
            "line": self.line,
            "severity": self.severity,
            "detection_confidence": self.detection_confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VulnerabilityModel":
        """Create a VulnerabilityModel from a dictionary"""
        vuln = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Unnamed Vulnerability"),
            cwe_id=data.get("cwe_id", ""),
            description=data.get("description", ""),
            file=data.get("file", ""),
            line=data.get("line", 0),
            severity=data.get("severity", "medium"),
        )
        vuln.cvss_score = data.get("cvss_score", 0.0)
        vuln.affected_components = data.get("affected_components", [])
        vuln.remediation = data.get("remediation", "")
        vuln.detection_confidence = data.get("detection_confidence", "medium")
        return vuln


class AttackPathModel:
    """Model for attack paths"""

    def __init__(
        self,
        id: str = None,
        name: str = "",
        description: str = "",
        steps: List[str] = None,
        vulnerability_ids: List[str] = None,
        impact: str = "",
        likelihood: str = "",
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.steps = steps or []
        self.vulnerability_ids = vulnerability_ids or []
        self.impact = impact
        self.likelihood = likelihood

    def to_dict(self) -> Mapping[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "vulnerability_ids": self.vulnerability_ids,
            "impact": self.impact,
            "likelihood": self.likelihood,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AttackPathModel":
        """Create an AttackPathModel from a dictionary"""
        attack_path = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Unnamed Attack Path"),
            description=data.get("description", ""),
            steps=data.get("steps", []),
            vulnerability_ids=data.get("vulnerability_ids", []),
            impact=data.get("impact", ""),
            likelihood=data.get("likelihood", ""),
        )
        return attack_path


class MitigationModel:
    """Model for mitigations"""

    def __init__(
        self,
        id: str = None,
        name: str = "",
        description: str = "",
        vulnerability_ids: List[str] = None,
        implementation_status: str = "not_implemented",
        priority: str = "medium",
        effort: str = "medium",
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.vulnerability_ids = vulnerability_ids or []
        self.implementation_status = implementation_status
        self.priority = priority
        self.effort = effort

    def to_dict(self) -> Mapping[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "vulnerability_ids": self.vulnerability_ids,
            "implementation_status": self.implementation_status,
            "priority": self.priority,
            "effort": self.effort,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MitigationModel":
        """Create a MitigationModel from a dictionary"""
        mitigation = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Unnamed Mitigation"),
            description=data.get("description", ""),
            vulnerability_ids=data.get("vulnerability_ids", []),
            implementation_status=data.get("implementation_status", "not_implemented"),
            priority=data.get("priority", "medium"),
            effort=data.get("effort", "medium"),
        )
        return mitigation


class ThreatModel:
    """Model for the complete threat model"""

    def __init__(self, model_id: str = None):
        self.id = model_id or str(uuid.uuid4())
        self.title = ""
        self.executive_summary = ""
        self.vulnerabilities: List[VulnerabilityModel] = []
        self.attack_paths: List[AttackPathModel] = []
        self.mitigations: List[MitigationModel] = []
        self.metadata: Dict[str, Any] = {}

    def add_vulnerability(self, vulnerability: VulnerabilityModel):
        """Add a vulnerability to the model"""
        self.vulnerabilities.append(vulnerability)

    def add_attack_path(self, attack_path: AttackPathModel):
        """Add an attack path to the model"""
        self.attack_paths.append(attack_path)

    def add_mitigation(self, mitigation: MitigationModel):
        """Add a mitigation to the model"""
        self.mitigations.append(mitigation)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "executive_summary": self.executive_summary,
            "vulnerabilities": [vuln.to_dict() for vuln in self.vulnerabilities],
            "attack_paths": [path.to_dict() for path in self.attack_paths],
            "mitigations": [mitigation.to_dict() for mitigation in self.mitigations],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatModel":
        """Create a ThreatModel from a dictionary"""
        model = cls(data.get("id", str(uuid.uuid4())))
        model.title = data.get("title", "")
        model.executive_summary = data.get("executive_summary", "")
        model.metadata = data.get("metadata", {})

        # Reconstruct vulnerabilities
        for vuln_data in data.get("vulnerabilities", []):
            vulnerability = VulnerabilityModel.from_dict(vuln_data)
            model.add_vulnerability(vulnerability)

        # Reconstruct attack paths
        for path_data in data.get("attack_paths", []):
            attack_path = AttackPathModel.from_dict(path_data)
            model.add_attack_path(attack_path)

        # Reconstruct mitigations
        for mitigation_data in data.get("mitigations", []):
            mitigation = MitigationModel.from_dict(mitigation_data)
            model.add_mitigation(mitigation)

        return model


class ThreatModelModel:
    """Model for the final threat model"""

    def __init__(self, model_id: str):
        self.id = model_id
        self.title = ""
        self.executive_summary = ""
        self.asset_inventory: List[Mapping[str, Any]] = []
        self.data_flow_diagrams: List[Mapping[str, Any]] = []
        self.threat_scenarios: List[ThreatScenarioModel] = (
            []
        )  # List of ThreatScenarioModel
        self.vulnerabilities: List[VulnerabilityModel] = (
            []
        )  # List of VulnerabilityModel
        self.commit_threats: List[Mapping[str, Any]] = (
            []
        )  # List of commit-based threats
        self.recommendations: List[Mapping[str, Any]] = []
        self.metadata: Mapping[str, Any] = {}

    def add_threat_scenario(self, scenario: ThreatScenarioModel):
        """Add a threat scenario to the model"""
        self.threat_scenarios.append(scenario)

    def add_vulnerability(self, vulnerability: VulnerabilityModel):
        """Add a vulnerability to the model"""
        self.vulnerabilities.append(vulnerability)

    def add_commit_threat(self, commit_threat: Mapping[str, Any]):
        """Add a commit-based threat to the model"""
        self.commit_threats.append(commit_threat)

    def add_recommendation(self, recommendation: Mapping[str, Any]):
        """Add a recommendation to the model"""
        self.recommendations.append(recommendation)

    def to_dict(self) -> Mapping[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "executive_summary": self.executive_summary,
            "asset_inventory": self.asset_inventory,
            "data_flow_diagrams": self.data_flow_diagrams,
            "threat_scenarios": [
                scenario.to_dict() for scenario in self.threat_scenarios
            ],
            "vulnerabilities": [vuln.to_dict() for vuln in self.vulnerabilities],
            "commit_threats": self.commit_threats,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreatModelModel":
        """Create a ThreatModelModel from a dictionary"""
        model_id = data.get("id", str(uuid.uuid4()))
        model = cls(model_id)
        model.title = data.get("title", "")
        model.executive_summary = data.get("executive_summary", "")
        model.asset_inventory = data.get("asset_inventory", [])
        model.data_flow_diagrams = data.get("data_flow_diagrams", [])
        model.commit_threats = data.get("commit_threats", [])
        model.recommendations = data.get("recommendations", [])
        model.metadata = data.get("metadata", {})

        # Reconstruct threat scenarios
        for scenario_data in data.get("threat_scenarios", []):
            scenario = ThreatScenarioModel.from_dict(scenario_data)
            model.add_threat_scenario(scenario)

        # Reconstruct vulnerabilities
        for vuln_data in data.get("vulnerabilities", []):
            vulnerability = VulnerabilityModel.from_dict(vuln_data)
            model.add_vulnerability(vulnerability)

        return model
