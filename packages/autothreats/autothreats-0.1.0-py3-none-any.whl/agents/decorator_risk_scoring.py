#!/usr/bin/env python3
"""
Decorator-based Risk Scoring Agent for the autonomous threat modeling system.
Uses the decorator API for simplified implementation.
"""

import asyncio
import json
import logging
import math
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from ..types import MessageType
from ..utils.agent_decorators import agent

logger = logging.getLogger(__name__)

@agent(agent_id="risk_scoring", agent_type="risk_scoring")
async def risk_scoring(agent, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process risk scoring tasks.
    
    Args:
        agent: The agent instance
        task_type: The type of task to process
        task_data: The data for the task
        
    Returns:
        Result data
    """
    agent.logger.info(f"Processing task of type: {task_type}")
    
    # Initialize risk models if not already initialized
    if not hasattr(agent, "severity_levels"):
        _initialize_risk_models(agent)
    
    # Handle risk scoring task
    if task_type in ["risk_scoring", "score_risks"]:
        # Extract parameters
        job_id = task_data.get("job_id")
        codebase_id = task_data.get("codebase_id")
        vulnerabilities = task_data.get("vulnerabilities", []) or []
        simulated_scenarios = task_data.get("simulated_scenarios", []) or []
        context = task_data.get("context", {}) or {}
        lightweight = task_data.get("lightweight", False)
        
        # Check for missing parameters
        if not job_id or not codebase_id:
            error_msg = "Missing required parameters: job_id or codebase_id"
            agent.logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg
            }
        
        try:
            agent.logger.info(f"Starting risk scoring for job {job_id}")
            
            # Score risks
            risk_scores, risk_metrics = await _score_risks(
                agent,
                vulnerabilities,
                simulated_scenarios,
                context,
                lightweight
            )
            
            # Store risk scores and metrics in workspace
            agent.workspace.store_data(f"risk_scores_{job_id}", risk_scores)
            agent.workspace.store_data(f"risk_metrics_{job_id}", risk_metrics)
            
            agent.logger.info(f"Risk scoring complete for job {job_id}")
            
            # Return success
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
            agent.logger.exception(error_msg)
            
            return {
                "status": "error",
                "message": error_msg,
                "job_id": job_id,
                "codebase_id": codebase_id,
            }
    else:
        return {
            "status": "error",
            "message": f"Unsupported task type: {task_type}"
        }

def _initialize_risk_models(agent):
    """Initialize risk scoring models and constants"""
    # Risk severity levels
    agent.severity_levels = {
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
    agent.risk_thresholds = {
        "acceptable": 4.0,  # Risks below this score are generally acceptable
        "acceptable_with_review": 7.0,  # Risks below this score may be acceptable with review
        "unacceptable": 10.0,  # Risks above acceptable_with_review are generally unacceptable
    }

    # Business impact weights
    agent.business_impact_weights = {
        "financial": 0.4,  # Financial impact weight
        "operational": 0.3,  # Operational impact weight
        "reputational": 0.2,  # Reputational impact weight
        "compliance": 0.1,  # Compliance impact weight
    }

    # Risk calculation formulas
    agent.risk_formulas = {
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

async def _score_risks(
    agent,
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
            score = await _score_vulnerability(
                agent, vulnerability, context, lightweight
            )
            vulnerability_scores.append(score)

    risk_scores["vulnerabilities"] = vulnerability_scores

    # Score scenarios
    scenario_scores = []
    if simulated_scenarios is not None:
        for scenario in simulated_scenarios:
            score = await _score_scenario(agent, scenario, context, lightweight)
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
        for severity, range_info in agent.severity_levels.items():
            if range_info["min_score"] <= overall_risk <= range_info["max_score"]:
                risk_scores["risk_severity"] = severity
                break

    # Calculate risk metrics
    risk_metrics = await _calculate_risk_metrics(
        agent, vulnerability_scores, scenario_scores, context, lightweight
    )

    return risk_scores, risk_metrics

async def _score_vulnerability(
    agent,
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
        agent.logger.warning(
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
    likelihood = _calculate_likelihood(agent, vulnerability, context)

    # Calculate risk score using standard formula
    risk_score = agent.risk_formulas["standard"](impact, likelihood)

    # Determine risk severity level
    severity = "info"
    severity_color = "#0066cc"  # Default blue
    for level, range_info in agent.severity_levels.items():
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
    business_impact = _calculate_business_impact(
        agent, vulnerability, context, risk_score, lightweight
    )

    # Risk acceptance level
    acceptance_level = "acceptable"
    if risk_score >= agent.risk_thresholds["unacceptable"]:
        acceptance_level = "unacceptable"
    elif risk_score >= agent.risk_thresholds["acceptable_with_review"]:
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
    agent,
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
        agent.logger.warning(
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
        risk_score = agent.risk_formulas["standard"](impact, likelihood)

    # Determine risk severity level
    severity = "info"
    severity_color = "#0066cc"  # Default blue
    for level, range_info in agent.severity_levels.items():
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
    business_impact = _calculate_business_impact_for_scenario(
        agent, scenario, context, risk_score, lightweight
    )

    # Risk acceptance level
    acceptance_level = "acceptable"
    if risk_score >= agent.risk_thresholds["unacceptable"]:
        acceptance_level = "unacceptable"
    elif risk_score >= agent.risk_thresholds["acceptable_with_review"]:
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
    agent, vulnerability: Dict[str, Any], context: Dict[str, Any]
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

    # Adjust based on exposure
    exposure = vulnerability.get("exposure", "internal").lower()
    exposure_adjustment = {"public": 2.0, "external": 1.0, "internal": 0.0, "isolated": -1.0}.get(
        exposure, 0.0
    )

    # Adjust based on authentication required
    auth_required = vulnerability.get("authentication_required", True)
    auth_adjustment = -1.0 if auth_required else 1.0

    # Calculate final likelihood
    likelihood = base_likelihood + confidence_adjustment + cwe_adjustment + exposure_adjustment + auth_adjustment

    # Ensure likelihood is within bounds
    likelihood = max(1.0, min(10.0, likelihood))

    return likelihood

def _calculate_business_impact(
    agent,
    vulnerability: Dict[str, Any],
    context: Dict[str, Any],
    risk_score: float,
    lightweight: bool = False,
) -> Dict[str, Any]:
    """Calculate business impact of a vulnerability"""
    # Default impact values
    business_impact = {
        "financial": 5.0,
        "operational": 5.0,
        "reputational": 5.0,
        "compliance": 5.0,
        "overall": 5.0,
    }

    # If lightweight mode, return default values
    if lightweight:
        return business_impact

    # Adjust financial impact based on vulnerability type
    cwe_id = vulnerability.get("cwe_id", "")
    severity = vulnerability.get("severity", "medium").lower()

    # Financial impact adjustments
    high_financial_impact_cwes = ["CWE-89", "CWE-78", "CWE-79", "CWE-352", "CWE-798"]
    if cwe_id in high_financial_impact_cwes:
        business_impact["financial"] = 8.0
    elif severity == "high" or severity == "critical":
        business_impact["financial"] = 7.0
    elif severity == "medium":
        business_impact["financial"] = 5.0
    else:
        business_impact["financial"] = 3.0

    # Operational impact adjustments
    high_operational_impact_cwes = ["CWE-400", "CWE-20", "CWE-22", "CWE-434", "CWE-502"]
    if cwe_id in high_operational_impact_cwes:
        business_impact["operational"] = 8.0
    elif severity == "high" or severity == "critical":
        business_impact["operational"] = 7.0
    elif severity == "medium":
        business_impact["operational"] = 5.0
    else:
        business_impact["operational"] = 3.0

    # Reputational impact adjustments
    high_reputational_impact_cwes = ["CWE-200", "CWE-359", "CWE-532", "CWE-798"]
    if cwe_id in high_reputational_impact_cwes:
        business_impact["reputational"] = 8.0
    elif severity == "high" or severity == "critical":
        business_impact["reputational"] = 7.0
    elif severity == "medium":
        business_impact["reputational"] = 5.0
    else:
        business_impact["reputational"] = 3.0

    # Compliance impact adjustments
    high_compliance_impact_cwes = ["CWE-256", "CWE-311", "CWE-327", "CWE-798"]
    if cwe_id in high_compliance_impact_cwes:
        business_impact["compliance"] = 8.0
    elif severity == "high" or severity == "critical":
        business_impact["compliance"] = 7.0
    elif severity == "medium":
        business_impact["compliance"] = 5.0
    else:
        business_impact["compliance"] = 3.0

    # Calculate overall business impact using weights
    overall_impact = 0.0
    for impact_type, weight in agent.business_impact_weights.items():
        overall_impact += business_impact[impact_type] * weight

    business_impact["overall"] = round(overall_impact, 1)

    return business_impact

def _calculate_business_impact_for_scenario(
    agent,
    scenario: Dict[str, Any],
    context: Dict[str, Any],
    risk_score: float,
    lightweight: bool = False,
) -> Dict[str, Any]:
    """Calculate business impact of a threat scenario"""
    # Default impact values
    business_impact = {
        "financial": 5.0,
        "operational": 5.0,
        "reputational": 5.0,
        "compliance": 5.0,
        "overall": 5.0,
    }

    # If lightweight mode, return default values
    if lightweight:
        return business_impact

    # Extract impact information from scenario
    impact_text = scenario.get("impact", "").lower()
    attack_vector = scenario.get("attack_vector", "").lower()
    threat_type = scenario.get("threat_type", "").lower()

    # Financial impact adjustments
    if "financial" in impact_text or "money" in impact_text or "fraud" in impact_text:
        business_impact["financial"] = 8.0
    elif "data breach" in impact_text or "theft" in impact_text:
        business_impact["financial"] = 7.0
    elif risk_score >= 7.0:
        business_impact["financial"] = 7.0
    elif risk_score >= 4.0:
        business_impact["financial"] = 5.0
    else:
        business_impact["financial"] = 3.0

    # Operational impact adjustments
    if "denial of service" in impact_text or "availability" in impact_text:
        business_impact["operational"] = 8.0
    elif "disruption" in impact_text or "degradation" in impact_text:
        business_impact["operational"] = 7.0
    elif risk_score >= 7.0:
        business_impact["operational"] = 7.0
    elif risk_score >= 4.0:
        business_impact["operational"] = 5.0
    else:
        business_impact["operational"] = 3.0

    # Reputational impact adjustments
    if "data breach" in impact_text or "privacy" in impact_text:
        business_impact["reputational"] = 8.0
    elif "public" in impact_text or "customer" in impact_text:
        business_impact["reputational"] = 7.0
    elif risk_score >= 7.0:
        business_impact["reputational"] = 7.0
    elif risk_score >= 4.0:
        business_impact["reputational"] = 5.0
    else:
        business_impact["reputational"] = 3.0

    # Compliance impact adjustments
    if "compliance" in impact_text or "regulatory" in impact_text or "legal" in impact_text:
        business_impact["compliance"] = 8.0
    elif "data breach" in impact_text or "privacy" in impact_text:
        business_impact["compliance"] = 7.0
    elif risk_score >= 7.0:
        business_impact["compliance"] = 7.0
    elif risk_score >= 4.0:
        business_impact["compliance"] = 5.0
    else:
        business_impact["compliance"] = 3.0

    # Calculate overall business impact using weights
    overall_impact = 0.0
    for impact_type, weight in agent.business_impact_weights.items():
        overall_impact += business_impact[impact_type] * weight

    business_impact["overall"] = round(overall_impact, 1)

    return business_impact

async def _calculate_risk_metrics(
    agent,
    vulnerability_scores: List[Dict[str, Any]],
    scenario_scores: List[Dict[str, Any]],
    context: Dict[str, Any],
    lightweight: bool = False,
) -> Dict[str, Any]:
    """Calculate risk metrics based on scored vulnerabilities and scenarios"""
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
        "risk_trend": "stable",  # Default value
    }

    # Combine all scores
    all_scores = vulnerability_scores + scenario_scores

    # Calculate risk distribution
    for score in all_scores:
        severity = score.get("risk_severity", "info")
        risk_metrics["risk_distribution"][severity] = risk_metrics["risk_distribution"].get(severity, 0) + 1

    # Calculate risk acceptance
    for score in all_scores:
        acceptance = score.get("acceptance_level", "acceptable")
        risk_metrics["risk_acceptance"][acceptance] = risk_metrics["risk_acceptance"].get(acceptance, 0) + 1

    # Calculate top risks (highest risk scores)
    sorted_scores = sorted(all_scores, key=lambda x: x.get("risk_score", 0), reverse=True)
    risk_metrics["top_risks"] = sorted_scores[:5]  # Top 5 risks

    # Calculate risk by component
    component_risks = {}
    for score in all_scores:
        component_risk = score.get("component_risk", {})
        for component, risk in component_risk.items():
            if component not in component_risks:
                component_risks[component] = 0
            component_risks[component] += risk
    risk_metrics["risk_by_component"] = component_risks

    # Calculate risk by category
    category_risks = {}
    for score in all_scores:
        category = score.get("category", "unknown")
        risk_score = score.get("risk_score", 0)
        if category not in category_risks:
            category_risks[category] = 0
        category_risks[category] += risk_score
    risk_metrics["risk_by_category"] = category_risks

    return risk_metrics