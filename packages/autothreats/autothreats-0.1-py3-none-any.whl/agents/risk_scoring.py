#!/usr/bin/env python3
"""
Risk Scoring Agent module for the autonomous threat modeling system.
Responsible for scoring risks and calculating risk metrics.
"""

import asyncio
import json
import logging
import math
import os
import re
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..message_types import MessageType
from ..simplified_base import Agent, AgentController, Message

logger = logging.getLogger(__name__)


class RiskScoringController(AgentController):
    """Controller for risk scoring agent"""

    async def initialize(self):
        """Initialize controller resources"""
        self.logger.info("Initializing Risk Scoring Controller")
        self.model.update_state("status", "initialized")

        # Initialize risk scoring models
        self._initialize_risk_models()

    def _initialize_risk_models(self):
        """Initialize risk scoring models and constants"""
        # Risk severity levels
        self.severity_levels = {
            "critical": {
                "min_score": 9.0,
                "max_score": 10.0,
                "color": "#cc0000",
                "label": "Critical",
            },  # Dark red
            "high": {
                "min_score": 7.0,
                "max_score": 8.9,
                "color": "#ff5500",
                "label": "High",
            },  # Red-orange
            "medium": {
                "min_score": 4.0,
                "max_score": 6.9,
                "color": "#ffcc00",
                "label": "Medium",
            },  # Yellow
            "low": {
                "min_score": 0.1,
                "max_score": 3.9,
                "color": "#00cc00",
                "label": "Low",
            },  # Green
            "info": {
                "min_score": 0.0,
                "max_score": 0.0,
                "color": "#0066cc",
                "label": "Info",
            },  # Blue
        }

        # Risk acceptance thresholds
        self.risk_thresholds = {
            "acceptable": 4.0,  # Risks below this score are generally acceptable
            "acceptable_with_review": 7.0,  # Risks below this score may be acceptable with review
            "unacceptable": 10.0,  # Risks above acceptable_with_review are generally unacceptable
        }

        # Business impact weights
        self.business_impact_weights = {
            "financial": 0.4,  # Financial impact weight
            "operational": 0.3,  # Operational impact weight
            "reputational": 0.2,  # Reputational impact weight
            "compliance": 0.1,  # Compliance impact weight
        }

        # Risk calculation formulas
        self.risk_formulas = {
            "standard": lambda impact, likelihood: (impact * likelihood) / 10,
            "dread": lambda impact, likelihood, ease, affected_users, discoverability: (
                impact * 0.3
            )
            + (likelihood * 0.2)
            + (ease * 0.2)
            + (affected_users * 0.15)
            + (discoverability * 0.15),
            "owasp": lambda impact, likelihood: (impact + likelihood) / 2,
        }

    async def handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """Handle incoming messages"""
        if message.message_type == MessageType.RISK_SCORING_START.value:
            return await self._handle_risk_scoring_start(message)

        self.logger.debug(f"Unhandled message type: {message.message_type}")
        return None

    async def shutdown(self):
        """Shut down controller resources"""
        self.logger.info("Shutting down Risk Scoring Controller")

    async def _handle_risk_scoring_start(self, message: Message) -> Dict[str, Any]:
        """Handle risk scoring start message"""
        job_id = message.content.get("job_id")
        codebase_id = message.content.get("codebase_id")
        vulnerabilities = message.content.get("vulnerabilities", []) or []
        simulated_scenarios = message.content.get("simulated_scenarios", []) or []
        context = (
            message.content.get("context") or {}
        )  # Ensure context is always a dictionary
        lightweight = message.content.get("lightweight", False)

        if not job_id or not codebase_id:
            error_msg = "Missing job_id or codebase_id in message"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}

        try:
            self.logger.info(f"Starting risk scoring for job {job_id}")

            # Score risks
            risk_scores, risk_metrics = await self._score_risks(
                vulnerabilities, simulated_scenarios, context, lightweight
            )

            # Store risk scores and metrics in workspace
            if hasattr(self, "workspace") and self.workspace:
                self.workspace.store_data(f"risk_scores_{job_id}", risk_scores)
                self.workspace.store_data(f"risk_metrics_{job_id}", risk_metrics)

            self.logger.info(f"Risk scoring complete for job {job_id}")

            # Send RISK_SCORING_COMPLETE message to notify orchestrator
            if hasattr(self, "workspace") and self.workspace:
                self.workspace.publish_message(
                    Message(
                        MessageType.RISK_SCORING_COMPLETE.value,
                        {
                            "job_id": job_id,
                            "codebase_id": codebase_id,
                            "risk_scores": risk_scores,
                            "risk_metrics": risk_metrics,
                        },
                        self.model.id,
                    )
                )
                self.logger.info(f"Sent RISK_SCORING_COMPLETE message for job {job_id}")

            return {
                "job_id": job_id,
                "codebase_id": codebase_id,
                "risk_scores": risk_scores,
                "risk_metrics": risk_metrics,
                "status": "success",
                "message": "Risk scoring complete",
                "next_action": "prioritization",
            }

        except Exception as e:
            error_msg = f"Error during risk scoring: {str(e)}"
            self.logger.exception(error_msg)

            # Send error message to orchestrator
            if hasattr(self, "workspace") and self.workspace:
                self.workspace.publish_message(
                    Message(
                        MessageType.SYSTEM_ERROR.value,
                        {"job_id": job_id, "error": error_msg, "stage": "risk_scoring"},
                        self.model.id,
                    )
                )
                self.logger.info(f"Sent SYSTEM_ERROR message for job {job_id}")

            return {"status": "error", "message": error_msg}

    async def _score_risks(
        self,
        vulnerabilities: List[Dict[str, Any]],
        simulated_scenarios: List[Dict[str, Any]],
        context: Dict[str, Any],
        lightweight: bool = False,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Score risks for vulnerabilities and scenarios"""
        # Ensure context is a dictionary
        if context is None:
            context = {}
        # Initialize results
        risk_scores = {
            "vulnerabilities": [],
            "scenarios": [],
            "overall_risk_score": 0.0,
            "risk_severity": "low",
        }

        risk_metrics = {
            "risk_distribution": {},
            "top_risks": [],
            "risk_by_component": {},
            "risk_by_category": {},
            "risk_acceptance": {
                "acceptable": 0,
                "acceptable_with_review": 0,
                "unacceptable": 0,
            },
            "risk_trend": "stable",  # Default value, would be calculated based on historical data
        }

        # Score vulnerabilities
        vulnerability_scores = []
        if vulnerabilities is not None:
            for vulnerability in vulnerabilities:
                score = await self._score_vulnerability(
                    vulnerability, context, lightweight
                )
                vulnerability_scores.append(score)

        risk_scores["vulnerabilities"] = vulnerability_scores

        # Score scenarios
        scenario_scores = []
        if simulated_scenarios is not None:
            for scenario in simulated_scenarios:
                score = await self._score_scenario(scenario, context, lightweight)
                scenario_scores.append(score)

        risk_scores["scenarios"] = scenario_scores

        # Calculate overall risk score
        all_scores = [
            score.get("risk_score", 0)
            for score in vulnerability_scores + scenario_scores
        ]
        if all_scores:
            # Use a weighted approach that emphasizes higher risks
            # Sort scores in descending order
            all_scores.sort(reverse=True)

            # Apply weight decay for lower scores
            weighted_sum = 0
            weight_sum = 0

            for i, score in enumerate(all_scores):
                # Use exponential decay for weights
                weight = math.exp(
                    -0.2 * i
                )  # Decay factor determines how quickly weights decrease
                weighted_sum += score * weight
                weight_sum += weight

            # Calculate weighted average
            if weight_sum > 0:
                overall_risk = weighted_sum / weight_sum
            else:
                overall_risk = 0

            # Round to one decimal place
            overall_risk = round(overall_risk, 1)
            risk_scores["overall_risk_score"] = overall_risk

            # Set risk severity based on overall score
            for severity, range_info in self.severity_levels.items():
                if range_info["min_score"] <= overall_risk <= range_info["max_score"]:
                    risk_scores["risk_severity"] = severity
                    break

        # Calculate risk metrics
        risk_metrics = await self._calculate_risk_metrics(
            vulnerability_scores, scenario_scores, context, lightweight
        )

        return risk_scores, risk_metrics

    async def _score_vulnerability(
        self,
        vulnerability: Dict[str, Any],
        context: Dict[str, Any],
        lightweight: bool = False,
    ) -> Dict[str, Any]:
        """Score a vulnerability"""
        # Ensure context is a dictionary
        if context is None:
            context = {}

        # Ensure vulnerability is a dictionary
        if vulnerability is None or not isinstance(vulnerability, dict):
            self.logger.warning(
                f"Skipping scoring for non-dictionary vulnerability: {vulnerability}"
            )
            return {
                "risk_score": 0.0,
                "impact": 0.0,
                "likelihood": 0.0,
                "risk_severity": "info",
                "severity_color": "#0066cc",
                "component_risk": {},
                "business_impact": {},
                "acceptance_level": "acceptable",
                "error": "Invalid vulnerability data format",
            }

        # Create a copy to avoid modifying the original
        scored_vulnerability = dict(vulnerability)

        # Get CVSS score if available, or use a default value
        cvss_score = vulnerability.get("cvss_score", 5.0)

        # Map CVSS score to impact and likelihood
        impact = min(10, cvss_score * 1.1)  # CVSS score slightly adjusted for impact
        likelihood = self._calculate_likelihood(vulnerability, context)

        # Calculate risk score using standard formula
        risk_score = self.risk_formulas["standard"](impact, likelihood)

        # Determine risk severity level
        severity = "info"
        severity_color = "#0066cc"  # Default blue
        for level, range_info in self.severity_levels.items():
            if range_info["min_score"] <= risk_score <= range_info["max_score"]:
                severity = level
                severity_color = range_info["color"]
                break

        # Calculate component risk contribution
        components = vulnerability.get("affected_components", [])
        component_risk = {}

        if components:
            risk_per_component = risk_score / len(components)
            for component in components:
                component_risk[component] = risk_per_component

        # Business impact analysis
        business_impact = self._calculate_business_impact(
            vulnerability, context, risk_score, lightweight
        )

        # Risk acceptance level
        acceptance_level = "acceptable"
        if risk_score >= self.risk_thresholds["unacceptable"]:
            acceptance_level = "unacceptable"
        elif risk_score >= self.risk_thresholds["acceptable_with_review"]:
            acceptance_level = "acceptable_with_review"

        # Add risk scoring to vulnerability
        scored_vulnerability.update(
            {
                "risk_score": round(risk_score, 1),
                "impact": round(impact, 1),
                "likelihood": round(likelihood, 1),
                "risk_severity": severity,
                "severity_color": severity_color,
                "component_risk": component_risk,
                "business_impact": business_impact,
                "acceptance_level": acceptance_level,
            }
        )

        return scored_vulnerability

    async def _score_scenario(
        self,
        scenario: Dict[str, Any],
        context: Dict[str, Any],
        lightweight: bool = False,
    ) -> Dict[str, Any]:
        """Score a threat scenario"""
        # Ensure context is a dictionary
        if context is None:
            context = {}

        # Ensure scenario is a dictionary
        if scenario is None or not isinstance(scenario, dict):
            self.logger.warning(
                f"Skipping scoring for non-dictionary scenario: {scenario}"
            )
            return {
                "risk_score": 0.0,
                "impact": 0.0,
                "likelihood": 0.0,
                "risk_severity": "info",
                "severity_color": "#0066cc",
                "error": "Invalid scenario data format",
            }

        # Create a copy to avoid modifying the original
        scored_scenario = dict(scenario)

        # Use scenario's existing risk score if available, otherwise calculate
        if "refined_risk_score" in scenario:
            risk_score = float(scenario["refined_risk_score"])
        elif "risk_score" in scenario:
            risk_score = float(scenario["risk_score"])
        else:
            # Calculate from impact and likelihood
            impact_text = scenario.get("impact", "").lower()

            # Map impact text to numeric value
            impact = 5.0  # Default medium impact
            if "critical" in impact_text or "severe" in impact_text:
                impact = 9.0
            elif "high" in impact_text or "significant" in impact_text:
                impact = 7.0
            elif "medium" in impact_text or "moderate" in impact_text:
                impact = 5.0
            elif "low" in impact_text or "minor" in impact_text:
                impact = 3.0

            # Get likelihood
            likelihood_text = scenario.get("likelihood", "medium").lower()
            likelihood = {"high": 9.0, "medium": 5.0, "low": 2.0}.get(
                likelihood_text, 5.0
            )

            # Adjust likelihood based on feasibility if available
            if "feasibility_score" in scenario:
                feasibility = float(scenario["feasibility_score"])
                likelihood = (likelihood + feasibility) / 2

            # Calculate risk score
            risk_score = self.risk_formulas["standard"](impact, likelihood)

        # Determine risk severity level
        severity = "info"
        severity_color = "#0066cc"  # Default blue
        for level, range_info in self.severity_levels.items():
            if range_info["min_score"] <= risk_score <= range_info["max_score"]:
                severity = level
                severity_color = range_info["color"]
                break

        # Component risk contribution
        components = scenario.get("affected_components", [])
        component_risk = {}

        if components:
            risk_per_component = risk_score / len(components)
            for component in components:
                component_risk[component] = risk_per_component

        # Business impact analysis
        business_impact = self._calculate_business_impact_for_scenario(
            scenario, context, risk_score, lightweight
        )

        # Risk acceptance level
        acceptance_level = "acceptable"
        if risk_score >= self.risk_thresholds["unacceptable"]:
            acceptance_level = "unacceptable"
        elif risk_score >= self.risk_thresholds["acceptable_with_review"]:
            acceptance_level = "acceptable_with_review"

        # Add risk scoring to scenario
        scored_scenario.update(
            {
                "risk_score": round(risk_score, 1),
                "risk_severity": severity,
                "severity_color": severity_color,
                "component_risk": component_risk,
                "business_impact": business_impact,
                "acceptance_level": acceptance_level,
            }
        )

        return scored_scenario

    def _calculate_likelihood(
        self, vulnerability: Dict[str, Any], context: Dict[str, Any]
    ) -> float:
        """Calculate the likelihood of a vulnerability being exploited"""
        # Start with a base likelihood (1-10)
        base_likelihood = 5.0

        # Adjust based on various factors

        # Adjust based on detection confidence
        confidence = vulnerability.get("detection_confidence", "medium").lower()
        confidence_adjustment = {"high": 2.0, "medium": 0.0, "low": -1.0}.get(
            confidence, 0.0
        )

        # Adjust based on vulnerability type (CWE)
        cwe_id = vulnerability.get("cwe_id", "")
        cwe_adjustment = 0.0

        high_likelihood_cwes = ["CWE-89", "CWE-79", "CWE-22", "CWE-352", "CWE-798"]
        medium_likelihood_cwes = ["CWE-287", "CWE-285", "CWE-20", "CWE-200", "CWE-611"]
        low_likelihood_cwes = ["CWE-327", "CWE-329", "CWE-338", "CWE-502"]

        if cwe_id in high_likelihood_cwes:
            cwe_adjustment = 2.0
        elif cwe_id in medium_likelihood_cwes:
            cwe_adjustment = 0.0
        elif cwe_id in low_likelihood_cwes:
            cwe_adjustment = -1.0

        # Adjust based on application type
        app_type = "unknown"
        if context is not None:
            app_type = context.get("application_type", {}).get("type", "unknown")
        app_adjustment = 0.0

        if app_type == "web" and cwe_id in ["CWE-79", "CWE-89", "CWE-352"]:
            app_adjustment = (
                1.5  # Web apps are more likely to have XSS, SQLi, CSRF exploited
            )
        elif app_type == "api" and cwe_id in ["CWE-20", "CWE-285", "CWE-287"]:
            app_adjustment = 1.0  # APIs are more likely to have auth/input validation issues exploited

        # Adjust based on security features
        security_features = (
            {} if context is None else context.get("security_features", {})
        )
        feature_adjustment = 0.0

        # If relevant security feature is present, reduce likelihood
        if cwe_id == "CWE-79" and security_features.get("xss_protection", {}).get(
            "present", False
        ):
            feature_adjustment -= 2.0
        elif cwe_id == "CWE-89" and security_features.get("input_validation", {}).get(
            "present", False
        ):
            feature_adjustment -= 2.0
        elif cwe_id == "CWE-352" and security_features.get("csrf_protection", {}).get(
            "present", False
        ):
            feature_adjustment -= 2.0
        elif (cwe_id == "CWE-287" or cwe_id == "CWE-798") and security_features.get(
            "authentication", {}
        ).get("present", False):
            feature_adjustment -= 1.0  # Less reduction as auth can still have issues
        elif cwe_id == "CWE-285" and security_features.get("authorization", {}).get(
            "present", False
        ):
            feature_adjustment -= (
                1.0  # Less reduction as authorization can still have issues
            )

        # Calculate final likelihood
        likelihood = (
            base_likelihood
            + confidence_adjustment
            + cwe_adjustment
            + app_adjustment
            + feature_adjustment
        )

        # Ensure likelihood is within 1-10 range
        likelihood = max(1.0, min(10.0, likelihood))

        return likelihood

    def _calculate_business_impact(
        self,
        vulnerability: Dict[str, Any],
        context: Dict[str, Any],
        risk_score: float,
        lightweight: bool = False,
    ) -> Dict[str, Any]:
        """Calculate the business impact of a vulnerability"""
        # Ensure context is a dictionary
        if context is None:
            context = {}
        if lightweight:
            # Simplified business impact for lightweight mode
            return {
                "overall": round(risk_score / 10 * 100, 1),  # Percentage impact
                "financial": "medium",
                "operational": "medium",
                "reputational": "medium",
                "compliance": "medium",
            }

        # Get factors that influence business impact
        cwe_id = vulnerability.get("cwe_id", "")
        cvss_score = vulnerability.get("cvss_score", 5.0)
        affected_components = vulnerability.get("affected_components", [])

        # Base impact values (1-10)
        financial_impact = 5.0
        operational_impact = 5.0
        reputational_impact = 5.0
        compliance_impact = 5.0

        # Adjust financial impact based on vulnerability type
        if cwe_id in [
            "CWE-89",
            "CWE-78",
            "CWE-502",
        ]:  # SQL injection, command injection, deserialization
            financial_impact = 8.0  # High financial impact - could lead to data breach or system compromise
        elif cwe_id in ["CWE-79", "CWE-352"]:  # XSS, CSRF
            financial_impact = (
                6.0  # Medium-high - could lead to account compromise or data theft
            )
        elif cwe_id in [
            "CWE-798",
            "CWE-287",
            "CWE-285",
        ]:  # Credentials, auth, authz issues
            financial_impact = 7.0  # Medium-high - could lead to unauthorized access

        # Adjust operational impact
        if cwe_id in [
            "CWE-78",
            "CWE-502",
            "CWE-22",
        ]:  # Command injection, deserialization, path traversal
            operational_impact = 9.0  # Could cause system outage or data corruption
        elif cwe_id in ["CWE-89", "CWE-20"]:  # SQL injection, input validation
            operational_impact = 7.0  # Could impact database operations

        # Adjust reputational impact
        if cwe_id in [
            "CWE-798",
            "CWE-287",
            "CWE-285",
            "CWE-89",
        ]:  # Auth issues, SQL injection
            reputational_impact = 8.0  # High reputational impact from data breaches
        elif cwe_id in ["CWE-79", "CWE-352"]:  # XSS, CSRF
            reputational_impact = 6.0  # Medium-high - visible security issues

        # Adjust compliance impact
        if cwe_id in ["CWE-89", "CWE-798", "CWE-287", "CWE-285"]:  # Data access related
            compliance_impact = (
                9.0  # High compliance impact - violates data protection regulations
            )
        elif cwe_id in ["CWE-327", "CWE-329"]:  # Crypto issues
            compliance_impact = 8.0  # High - violates security standards

        # Adjust based on application type and context
        app_type = "unknown"
        if context is not None:
            app_type = context.get("application_type", {}).get("type", "unknown")

        if app_type == "web" or app_type == "api":
            reputational_impact += (
                1.0  # Customer-facing applications have higher reputational impact
            )

        # Check for sensitive data handling
        has_sensitive_data = False
        if context is not None:
            has_sensitive_data = (
                len(context.get("data_handling", {}).get("sensitive_data_types", []))
                > 0
            )

        if has_sensitive_data:
            financial_impact += 1.0
            reputational_impact += 2.0
            compliance_impact += 2.0

        # Ensure all impacts are within 1-10 range
        financial_impact = max(1.0, min(10.0, financial_impact))
        operational_impact = max(1.0, min(10.0, operational_impact))
        reputational_impact = max(1.0, min(10.0, reputational_impact))
        compliance_impact = max(1.0, min(10.0, compliance_impact))

        # Convert numeric impacts to textual ratings
        impact_ratings = {
            (0, 3.9): "low",
            (4.0, 6.9): "medium",
            (7.0, 8.9): "high",
            (9.0, 10.0): "critical",
        }

        financial_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= financial_impact <= max_val
            ),
            "medium",
        )
        operational_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= operational_impact <= max_val
            ),
            "medium",
        )
        reputational_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= reputational_impact <= max_val
            ),
            "medium",
        )
        compliance_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= compliance_impact <= max_val
            ),
            "medium",
        )

        # Calculate overall business impact as weighted average
        overall_impact = (
            financial_impact * self.business_impact_weights["financial"]
            + operational_impact * self.business_impact_weights["operational"]
            + reputational_impact * self.business_impact_weights["reputational"]
            + compliance_impact * self.business_impact_weights["compliance"]
        )

        # Convert to percentage for easier understanding
        overall_percentage = round(overall_impact / 10 * 100, 1)

        return {
            "overall": overall_percentage,
            "financial": financial_rating,
            "operational": operational_rating,
            "reputational": reputational_rating,
            "compliance": compliance_rating,
        }

    def _calculate_business_impact_for_scenario(
        self,
        scenario: Dict[str, Any],
        context: Dict[str, Any],
        risk_score: float,
        lightweight: bool = False,
    ) -> Dict[str, Any]:
        """Calculate the business impact of a threat scenario"""
        # Ensure context is a dictionary
        if context is None:
            context = {}
        if lightweight:
            # Simplified business impact for lightweight mode
            return {
                "overall": round(risk_score / 10 * 100, 1),  # Percentage impact
                "financial": "medium",
                "operational": "medium",
                "reputational": "medium",
                "compliance": "medium",
            }

        # Extract information from scenario
        name = scenario.get("name", "").lower()
        impact_text = scenario.get("impact", "").lower()

        # Base impact values (1-10)
        financial_impact = 5.0
        operational_impact = 5.0
        reputational_impact = 5.0
        compliance_impact = 5.0

        # Adjust based on scenario name/type
        if "sql injection" in name or "data breach" in name:
            financial_impact = 8.0
            reputational_impact = 9.0
            compliance_impact = 9.0
        elif "xss" in name or "cross-site scripting" in name:
            reputational_impact = 7.0
            operational_impact = 5.0
        elif "csrf" in name or "cross-site request forgery" in name:
            operational_impact = 6.0
            reputational_impact = 6.0
        elif "authentication" in name or "broken auth" in name:
            financial_impact = 7.0
            reputational_impact = 8.0
            compliance_impact = 8.0
        elif "authorization" in name or "access control" in name:
            financial_impact = 7.0
            operational_impact = 6.0
            compliance_impact = 8.0
        elif "injection" in name:
            financial_impact = 7.0
            operational_impact = 8.0
        elif "dos" in name or "denial of service" in name:
            operational_impact = 9.0
            financial_impact = 7.0
        elif "information disclosure" in name or "data exposure" in name:
            reputational_impact = 8.0
            compliance_impact = 9.0

        # Adjust based on impact text
        if "financial" in impact_text or "monetary" in impact_text:
            financial_impact += 1.0
        if "operation" in impact_text or "availability" in impact_text:
            operational_impact += 1.0
        if "reputation" in impact_text or "customer trust" in impact_text:
            reputational_impact += 1.0
        if (
            "compliance" in impact_text
            or "regulatory" in impact_text
            or "gdpr" in impact_text
            or "hipaa" in impact_text
        ):
            compliance_impact += 1.0
        if "sensitive data" in impact_text or "personal data" in impact_text:
            compliance_impact += 1.0
            reputational_impact += 1.0

        # Adjust based on application type and context
        app_type = context.get("application_type", {}).get("type", "unknown")

        if app_type == "web" or app_type == "api":
            reputational_impact += (
                1.0  # Customer-facing applications have higher reputational impact
            )

        # Check for sensitive data handling
        has_sensitive_data = (
            len(context.get("data_handling", {}).get("sensitive_data_types", [])) > 0
        )

        if has_sensitive_data:
            financial_impact += 1.0
            reputational_impact += 2.0
            compliance_impact += 2.0

        # Ensure all impacts are within 1-10 range
        financial_impact = max(1.0, min(10.0, financial_impact))
        operational_impact = max(1.0, min(10.0, operational_impact))
        reputational_impact = max(1.0, min(10.0, reputational_impact))
        compliance_impact = max(1.0, min(10.0, compliance_impact))

        # Convert numeric impacts to textual ratings
        impact_ratings = {
            (0, 3.9): "low",
            (4.0, 6.9): "medium",
            (7.0, 8.9): "high",
            (9.0, 10.0): "critical",
        }

        financial_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= financial_impact <= max_val
            ),
            "medium",
        )
        operational_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= operational_impact <= max_val
            ),
            "medium",
        )
        reputational_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= reputational_impact <= max_val
            ),
            "medium",
        )
        compliance_rating = next(
            (
                rating
                for (min_val, max_val), rating in impact_ratings.items()
                if min_val <= compliance_impact <= max_val
            ),
            "medium",
        )

        # Calculate overall business impact as weighted average
        overall_impact = (
            financial_impact * self.business_impact_weights["financial"]
            + operational_impact * self.business_impact_weights["operational"]
            + reputational_impact * self.business_impact_weights["reputational"]
            + compliance_impact * self.business_impact_weights["compliance"]
        )

        # Convert to percentage for easier understanding
        overall_percentage = round(overall_impact / 10 * 100, 1)

        return {
            "overall": overall_percentage,
            "financial": financial_rating,
            "operational": operational_rating,
            "reputational": reputational_rating,
            "compliance": compliance_rating,
        }

    async def _calculate_risk_metrics(
        self,
        vulnerability_scores: List[Dict[str, Any]],
        scenario_scores: List[Dict[str, Any]],
        context: Dict[str, Any],
        lightweight: bool = False,
    ) -> Dict[str, Any]:
        """Calculate risk metrics based on the scored vulnerabilities and scenarios"""
        # Ensure context is a dictionary
        if context is None:
            context = {}
        # Initialize metrics
        risk_metrics = {
            "risk_distribution": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0,
            },
            "top_risks": [],
            "risk_by_component": {},
            "risk_by_category": {},
            "risk_acceptance": {
                "acceptable": 0,
                "acceptable_with_review": 0,
                "unacceptable": 0,
            },
            "risk_trend": "stable",  # Default value, would be calculated based on historical data
        }

        # Combine vulnerabilities and scenarios for analysis
        all_risks = (
            vulnerability_scores + scenario_scores
            if vulnerability_scores is not None and scenario_scores is not None
            else []
        )
        if vulnerability_scores is not None and scenario_scores is None:
            all_risks = vulnerability_scores
        elif vulnerability_scores is None and scenario_scores is not None:
            all_risks = scenario_scores

        # Calculate risk distribution
        for risk in all_risks:
            severity = risk.get("risk_severity", "info")
            risk_metrics["risk_distribution"][severity] += 1

            # Update risk acceptance counts
            acceptance_level = risk.get("acceptance_level", "acceptable")
            risk_metrics["risk_acceptance"][acceptance_level] += 1

            # Update risk by component
            for component, component_risk in risk.get("component_risk", {}).items():
                if component not in risk_metrics["risk_by_component"]:
                    risk_metrics["risk_by_component"][component] = 0
                risk_metrics["risk_by_component"][component] += component_risk

            # Update risk by category
            category = "unknown"
            if "cwe_id" in risk:
                # For vulnerabilities, use CWE category
                cwe_id = risk.get("cwe_id", "")
                if "CWE-89" in cwe_id or "CWE-78" in cwe_id or "CWE-20" in cwe_id:
                    category = "injection"
                elif "CWE-79" in cwe_id:
                    category = "xss"
                elif "CWE-352" in cwe_id:
                    category = "csrf"
                elif "CWE-287" in cwe_id or "CWE-798" in cwe_id:
                    category = "authentication"
                elif "CWE-285" in cwe_id:
                    category = "authorization"
                elif "CWE-327" in cwe_id or "CWE-329" in cwe_id:
                    category = "cryptography"
                elif "CWE-22" in cwe_id:
                    category = "path_traversal"
                elif "CWE-502" in cwe_id:
                    category = "deserialization"
                elif "CWE-200" in cwe_id:
                    category = "information_disclosure"
                elif "CWE-611" in cwe_id:
                    category = "xxe"
                else:
                    category = "other"
            else:
                # For scenarios, extract from name
                name = risk.get("name", "").lower()
                if "sql" in name or "injection" in name:
                    category = "injection"
                elif "xss" in name or "cross-site script" in name:
                    category = "xss"
                elif "csrf" in name or "cross-site request" in name:
                    category = "csrf"
                elif "auth" in name:
                    category = "authentication"
                elif "access" in name or "authori" in name:
                    category = "authorization"
                elif "data" in name or "information" in name:
                    category = "information_disclosure"
                elif "dos" in name or "denial" in name:
                    category = "denial_of_service"
                else:
                    category = "other"

            if category not in risk_metrics["risk_by_category"]:
                risk_metrics["risk_by_category"][category] = 0

            risk_metrics["risk_by_category"][category] += risk.get("risk_score", 0)

        # Identify top risks (highest risk scores)
        sorted_risks = sorted(
            all_risks, key=lambda r: r.get("risk_score", 0), reverse=True
        )
        top_count = min(5, len(sorted_risks))  # Top 5 or all if fewer

        risk_metrics["top_risks"] = []
        for i in range(top_count):
            risk = sorted_risks[i]
            risk_metrics["top_risks"].append(
                {
                    "id": risk.get("id"),
                    "name": risk.get("name"),
                    "risk_score": risk.get("risk_score", 0),
                    "risk_severity": risk.get("risk_severity", "info"),
                    "severity_color": risk.get("severity_color", "#0066cc"),
                    "type": "vulnerability" if "cwe_id" in risk else "scenario",
                }
            )

        # Round component and category risk scores
        for component in risk_metrics["risk_by_component"]:
            risk_metrics["risk_by_component"][component] = round(
                risk_metrics["risk_by_component"][component], 1
            )

        for category in risk_metrics["risk_by_category"]:
            risk_metrics["risk_by_category"][category] = round(
                risk_metrics["risk_by_category"][category], 1
            )

        # Sort components and categories by risk score
        risk_metrics["risk_by_component"] = dict(
            sorted(
                risk_metrics["risk_by_component"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        risk_metrics["risk_by_category"] = dict(
            sorted(
                risk_metrics["risk_by_category"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        return risk_metrics


class RiskScoringAgent(Agent):
    """Agent for scoring risks and calculating risk metrics"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, "risk_scoring", config)
        self.logger = logging.getLogger(f"RiskScoringAgent.{agent_id}")

    def _create_controller(self) -> AgentController:
        return RiskScoringController(self.model)
