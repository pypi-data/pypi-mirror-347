#!/usr/bin/env python3
"""
Simplified Adaptive Prioritization module for the autonomous threat modeling system.
Provides intelligent prioritization of vulnerabilities based on context and severity.
"""

import asyncio
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

from ..simplified_base import SharedWorkspace
from ..utils.llm_service import LLMService

logger = logging.getLogger(__name__)


class SimplifiedAdaptivePrioritization:
    """
    Simplified Adaptive Prioritization module that intelligently prioritizes
    vulnerabilities based on context, severity, and exploitability.
    """

    def __init__(self, workspace: SharedWorkspace):
        """
        Initialize the adaptive prioritization module.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.llm_service = workspace.get_data("llm_service")
        
        # Initialize cache for prioritization
        self.prioritization_cache = {}
        
    async def prioritize_vulnerabilities(self, vulnerabilities: List[Dict[str, Any]], job_id: str) -> List[Dict[str, Any]]:
        """
        Prioritize vulnerabilities based on context, severity, and exploitability.
        
        Args:
            vulnerabilities: List of vulnerabilities to prioritize
            job_id: The ID of the job
            
        Returns:
            Prioritized list of vulnerabilities
        """
        self.logger.info(f"Prioritizing {len(vulnerabilities)} vulnerabilities for job {job_id}")
        
        # Check cache first
        cache_key = f"prioritized_vulnerabilities_{job_id}"
        cached_result = self.workspace.get_cached_analysis(cache_key)
        if cached_result:
            self.logger.info(f"Using cached prioritization for job {job_id}")
            return cached_result
        
        # If no vulnerabilities, return empty list
        if not vulnerabilities:
            return []
        
        # Calculate base scores for each vulnerability
        scored_vulnerabilities = self._calculate_base_scores(vulnerabilities)
        
        # Apply context-based adjustments
        adjusted_vulnerabilities = await self._apply_context_adjustments(scored_vulnerabilities, job_id)
        
        # Apply exploitability adjustments
        exploitability_adjusted = self._apply_exploitability_adjustments(adjusted_vulnerabilities)
        
        # Sort vulnerabilities by priority score
        prioritized_vulnerabilities = sorted(
            exploitability_adjusted,
            key=lambda x: x.get("priority_score", 0),
            reverse=True
        )
        
        # Add priority levels
        prioritized_vulnerabilities = self._add_priority_levels(prioritized_vulnerabilities)
        
        # Cache the result
        self.workspace.cache_analysis(cache_key, prioritized_vulnerabilities)
        
        return prioritized_vulnerabilities
    
    def _calculate_base_scores(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate base priority scores for vulnerabilities.
        
        Args:
            vulnerabilities: List of vulnerabilities
            
        Returns:
            List of vulnerabilities with base scores
        """
        scored_vulnerabilities = []
        
        # Severity weights
        severity_weights = {
            "critical": 10.0,
            "high": 8.0,
            "medium": 5.0,
            "low": 2.0,
            "info": 1.0,
        }
        
        # Calculate base score for each vulnerability
        for vuln in vulnerabilities:
            # Create a copy of the vulnerability
            scored_vuln = dict(vuln)
            
            # Get severity (default to medium if not specified)
            severity = vuln.get("severity", "medium").lower()
            
            # Get confidence (default to 0.5 if not specified)
            confidence = vuln.get("confidence", 0.5)
            
            # Calculate base score
            base_score = severity_weights.get(severity, 5.0) * confidence
            
            # Add base score to vulnerability
            scored_vuln["base_score"] = base_score
            scored_vuln["priority_score"] = base_score
            
            scored_vulnerabilities.append(scored_vuln)
        
        return scored_vulnerabilities
    
    async def _apply_context_adjustments(self, vulnerabilities: List[Dict[str, Any]], job_id: str) -> List[Dict[str, Any]]:
        """
        Apply context-based adjustments to vulnerability scores.
        
        Args:
            vulnerabilities: List of vulnerabilities with base scores
            job_id: The ID of the job
            
        Returns:
            List of vulnerabilities with adjusted scores
        """
        adjusted_vulnerabilities = []
        
        # Get security context if available
        security_context = self.workspace.get_data(f"security_context_{job_id}")
        
        # Apply adjustments based on context
        for vuln in vulnerabilities:
            # Create a copy of the vulnerability
            adjusted_vuln = dict(vuln)
            
            # Start with base score
            adjusted_score = vuln.get("base_score", 5.0)
            
            # Apply security boundary adjustment
            if security_context and vuln.get("in_security_boundary", False):
                # Increase score for vulnerabilities in security boundaries
                adjusted_score *= 1.2
                adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["security_boundary"]
            
            # Apply file type adjustment
            file_path = vuln.get("file_path", "")
            if file_path:
                # Increase score for vulnerabilities in security-critical file types
                if any(ext in file_path.lower() for ext in [".auth.", "security.", "crypto.", "password."]):
                    adjusted_score *= 1.3
                    adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["security_critical_file"]
                
                # Adjust based on file extension
                if file_path.endswith(".js") or file_path.endswith(".ts"):
                    # JavaScript/TypeScript files (client-side)
                    if any(pattern in vuln.get("description", "").lower() for pattern in ["xss", "csrf", "injection"]):
                        adjusted_score *= 1.2
                        adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["client_side_vulnerability"]
                
                elif file_path.endswith(".py") or file_path.endswith(".java") or file_path.endswith(".go"):
                    # Server-side files
                    if any(pattern in vuln.get("description", "").lower() for pattern in ["sql injection", "command injection", "path traversal"]):
                        adjusted_score *= 1.2
                        adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["server_side_vulnerability"]
            
            # Apply pattern-based adjustments
            description = vuln.get("description", "").lower()
            if "password" in description or "credential" in description or "key" in description:
                adjusted_score *= 1.3
                adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["credential_related"]
            
            if "injection" in description:
                adjusted_score *= 1.2
                adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["injection_vulnerability"]
            
            if "bypass" in description or "authentication" in description:
                adjusted_score *= 1.25
                adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + ["auth_related"]
            
            # Update priority score
            adjusted_vuln["priority_score"] = adjusted_score
            
            adjusted_vulnerabilities.append(adjusted_vuln)
        
        return adjusted_vulnerabilities
    
    def _apply_exploitability_adjustments(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply exploitability adjustments to vulnerability scores.
        
        Args:
            vulnerabilities: List of vulnerabilities with adjusted scores
            
        Returns:
            List of vulnerabilities with exploitability adjustments
        """
        exploitability_adjusted = []
        
        # Exploitability factors
        exploitability_factors = {
            "sql injection": 1.3,
            "xss": 1.2,
            "csrf": 1.1,
            "command injection": 1.4,
            "path traversal": 1.2,
            "authentication bypass": 1.3,
            "authorization bypass": 1.25,
            "hardcoded credential": 1.2,
            "weak encryption": 1.15,
            "insecure deserialization": 1.3,
            "xxe": 1.2,
            "ssrf": 1.25,
            "open redirect": 1.1,
            "race condition": 1.05,
            "buffer overflow": 1.2,
            "integer overflow": 1.1,
        }
        
        # Apply exploitability adjustments
        for vuln in vulnerabilities:
            # Create a copy of the vulnerability
            adjusted_vuln = dict(vuln)
            
            # Start with current score
            adjusted_score = vuln.get("priority_score", 5.0)
            
            # Check for exploitability factors
            description = vuln.get("description", "").lower()
            for factor, multiplier in exploitability_factors.items():
                if factor in description:
                    adjusted_score *= multiplier
                    adjusted_vuln["adjustment_factors"] = adjusted_vuln.get("adjustment_factors", []) + [f"exploitable_{factor.replace(' ', '_')}"]
                    break
            
            # Apply confidence adjustment
            confidence = vuln.get("confidence", 0.5)
            adjusted_score *= (0.5 + confidence / 2)  # Scale by confidence (0.5 to 1.0 range)
            
            # Update priority score
            adjusted_vuln["priority_score"] = adjusted_score
            
            exploitability_adjusted.append(adjusted_vuln)
        
        return exploitability_adjusted
    
    def _add_priority_levels(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add priority levels to vulnerabilities based on scores.
        
        Args:
            vulnerabilities: List of vulnerabilities with priority scores
            
        Returns:
            List of vulnerabilities with priority levels
        """
        prioritized_vulnerabilities = []
        
        # If no vulnerabilities, return empty list
        if not vulnerabilities:
            return []
        
        # Get score ranges
        max_score = max(vuln.get("priority_score", 0) for vuln in vulnerabilities)
        min_score = min(vuln.get("priority_score", 0) for vuln in vulnerabilities)
        score_range = max_score - min_score
        
        # Define priority level thresholds
        if score_range > 0:
            critical_threshold = min_score + score_range * 0.8
            high_threshold = min_score + score_range * 0.6
            medium_threshold = min_score + score_range * 0.4
            low_threshold = min_score + score_range * 0.2
        else:
            # If all scores are the same, use absolute thresholds
            critical_threshold = 8.0
            high_threshold = 6.0
            medium_threshold = 4.0
            low_threshold = 2.0
        
        # Add priority levels
        for vuln in vulnerabilities:
            # Create a copy of the vulnerability
            prioritized_vuln = dict(vuln)
            
            # Get priority score
            score = vuln.get("priority_score", 0)
            
            # Determine priority level
            if score >= critical_threshold:
                priority_level = "critical"
            elif score >= high_threshold:
                priority_level = "high"
            elif score >= medium_threshold:
                priority_level = "medium"
            elif score >= low_threshold:
                priority_level = "low"
            else:
                priority_level = "info"
            
            # Add priority level
            prioritized_vuln["priority"] = priority_level
            
            prioritized_vulnerabilities.append(prioritized_vuln)
        
        return prioritized_vulnerabilities
    
    async def generate_prioritization_report(self, vulnerabilities: List[Dict[str, Any]], job_id: str) -> Dict[str, Any]:
        """
        Generate a report on vulnerability prioritization.
        
        Args:
            vulnerabilities: List of prioritized vulnerabilities
            job_id: The ID of the job
            
        Returns:
            Prioritization report
        """
        # Count vulnerabilities by priority
        priority_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
        }
        
        for vuln in vulnerabilities:
            priority = vuln.get("priority", "medium")
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Get top vulnerabilities
        top_vulnerabilities = sorted(
            vulnerabilities,
            key=lambda x: x.get("priority_score", 0),
            reverse=True
        )[:5]
        
        # Create report
        report = {
            "job_id": job_id,
            "total_vulnerabilities": len(vulnerabilities),
            "priority_counts": priority_counts,
            "top_vulnerabilities": top_vulnerabilities,
            "timestamp": asyncio.get_event_loop().time(),
        }
        
        return report