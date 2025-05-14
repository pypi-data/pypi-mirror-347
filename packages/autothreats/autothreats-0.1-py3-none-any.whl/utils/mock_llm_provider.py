#!/usr/bin/env python3
"""
Mock LLM provider for testing the threat modeling system without making actual API calls.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from .base_llm_provider import BaseLLMProvider

logger = logging.getLogger(__name__)


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing"""

    def __init__(
        self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize the mock provider"""
        super().__init__(api_key, config or {})
        self.logger.info("Initialized Mock LLM Provider")

    async def _make_api_request(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        system_prompt: str,
    ) -> str:
        """Mock API request that returns predefined responses based on the prompt"""
        self.logger.info(f"Mock API request: model={model}, max_tokens={max_tokens}")

        # Generate a response based on the prompt
        if "diagram" in prompt.lower() or "visualization" in prompt.lower():
            return self._generate_mock_diagram_response(prompt)
        elif "attack tree" in prompt.lower():
            return self._generate_mock_diagram_response(prompt)
        elif "mermaid" in prompt.lower():
            return self._generate_mock_diagram_response(prompt)
        elif "vulnerability" in prompt.lower() or "security" in prompt.lower():
            return self._generate_mock_vulnerability_response(prompt)
        elif "context" in prompt.lower() or "analyze" in prompt.lower():
            return self._generate_mock_context_response(prompt)
        elif "summary" in prompt.lower() or "report" in prompt.lower():
            return self._generate_mock_summary_response(prompt)
        elif "threat" in prompt.lower() and "model" in prompt.lower():
            return self._generate_mock_threat_model_response(prompt)
        else:
            return self._generate_generic_response(prompt)

    def _generate_mock_vulnerability_response(self, prompt: str) -> str:
        """Generate a mock response for vulnerability analysis"""
        # Check for specific vulnerability types in the prompt
        if "sql injection" in prompt.lower() or "cwe-89" in prompt.lower():
            return json.dumps(
                {
                    "is_applicable": True,
                    "applicability_explanation": "SQL injection is applicable to this language",
                    "detailed_description": "The code is vulnerable to SQL injection because it concatenates user input directly into SQL queries without proper sanitization.",
                    "data_flow_analysis": "User input flows from the request parameter to the SQL query without validation.",
                    "input_validation_assessment": "No input validation or sanitization is performed.",
                    "false_positive_likelihood": "low",
                    "false_positive_explanation": "This is a clear case of SQL injection.",
                    "impact": "An attacker could execute arbitrary SQL commands, potentially accessing, modifying, or deleting data.",
                    "exploitation_difficulty": "low",
                    "exploitation_prerequisites": [
                        "Access to the application interface"
                    ],
                    "remediation": [
                        "Use parameterized queries",
                        "Implement input validation",
                        "Apply principle of least privilege",
                    ],
                    "language_specific_remediation": "Use prepared statements with parameterized queries",
                    "attack_vectors": [
                        "Inject malicious SQL through user input fields"
                    ],
                    "mitre_relevance": "This vulnerability relates to the Command and Scripting Interpreter technique in the MITRE ATT&CK framework.",
                }
            )
        elif (
            "xss" in prompt.lower()
            or "cross-site" in prompt.lower()
            or "cwe-79" in prompt.lower()
        ):
            # Check if this is for a non-web language
            if any(
                lang in prompt.lower() for lang in ["c", "c++", "cpp", "rust", "go"]
            ):
                return json.dumps(
                    {
                        "is_applicable": False,
                        "applicability_explanation": "XSS vulnerabilities are specific to web applications and are not applicable to C/C++/Rust/Go code that doesn't generate HTML or JavaScript.",
                        "detailed_description": "This is not a valid XSS vulnerability because the language doesn't produce web content. XSS is not applicable to this language.",
                        "false_positive_likelihood": "high",
                        "false_positive_explanation": "This is a false positive. XSS requires a web context.",
                    }
                )
            else:
                return json.dumps(
                    {
                        "is_applicable": True,
                        "applicability_explanation": "XSS is applicable to web technologies",
                        "detailed_description": "The code is vulnerable to XSS because it directly inserts user input into the DOM without sanitization.",
                        "data_flow_analysis": "User input flows from the request to the DOM without proper encoding.",
                        "input_validation_assessment": "No input validation or sanitization is performed.",
                        "false_positive_likelihood": "low",
                        "false_positive_explanation": "This is a clear case of XSS.",
                        "impact": "An attacker could execute arbitrary JavaScript in users' browsers.",
                        "exploitation_difficulty": "low",
                        "exploitation_prerequisites": ["Access to input fields"],
                        "remediation": [
                            "Use context-appropriate encoding",
                            "Implement CSP",
                            "Validate input",
                        ],
                        "language_specific_remediation": "Use a library like DOMPurify to sanitize HTML",
                        "attack_vectors": [
                            "Inject malicious scripts through user input fields"
                        ],
                        "mitre_relevance": "This vulnerability relates to the Drive-by Compromise technique in the MITRE ATT&CK framework.",
                    }
                )
        else:
            # Generic vulnerability response
            return json.dumps(
                {
                    "is_applicable": True,
                    "applicability_explanation": "This vulnerability type is applicable to the code language",
                    "detailed_description": "The code contains potential security issues that should be addressed.",
                    "data_flow_analysis": "Data flows from external sources to sensitive operations without sufficient validation.",
                    "input_validation_assessment": "Input validation is insufficient or missing.",
                    "false_positive_likelihood": "medium",
                    "false_positive_explanation": "This may be a vulnerability depending on the context.",
                    "impact": "The vulnerability could potentially lead to security issues.",
                    "exploitation_difficulty": "medium",
                    "exploitation_prerequisites": ["Access to the application"],
                    "remediation": [
                        "Implement proper input validation",
                        "Follow security best practices",
                    ],
                    "language_specific_remediation": "Follow language-specific security guidelines",
                    "attack_vectors": ["Exploit input handling weaknesses"],
                    "mitre_relevance": "This vulnerability relates to several techniques in the MITRE ATT&CK framework.",
                }
            )

    def _generate_mock_context_response(self, prompt: str) -> str:
        """Generate a mock response for context analysis"""
        return json.dumps(
            {
                "application_type": "web",
                "technologies": {
                    "languages": ["JavaScript", "Python", "HTML", "CSS"],
                    "frameworks": ["React", "Flask"],
                    "databases": ["PostgreSQL"],
                    "other": ["Docker", "Nginx"],
                },
                "security_features": {
                    "authentication": True,
                    "authorization": True,
                    "input_validation": False,
                    "encryption": False,
                },
                "entry_points": {
                    "api_endpoints": ["/api/users", "/api/products", "/api/auth"],
                    "user_interfaces": ["login", "dashboard", "profile"],
                },
                "data_handling": {
                    "sensitive_data": True,
                    "data_storage": "database",
                    "data_transmission": "https",
                },
            }
        )

    def _generate_mock_summary_response(self, prompt: str) -> str:
        """Generate a mock response for summary or report generation"""
        return """
        # Security Analysis Summary
        
        ## Overview
        The application is a web-based system with several security concerns that should be addressed.
        
        ## Key Findings
        1. SQL Injection vulnerabilities in database queries
        2. Cross-Site Scripting (XSS) in user interface components
        3. Insufficient input validation throughout the application
        4. Weak authentication mechanisms
        
        ## Recommendations
        1. Implement parameterized queries for all database operations
        2. Add proper output encoding for all user-generated content
        3. Enhance input validation across all entry points
        4. Strengthen authentication with multi-factor authentication
        
        ## Risk Assessment
        The overall risk is MEDIUM to HIGH based on the identified vulnerabilities.
        """

    def _generate_mock_threat_model_response(self, prompt: str) -> str:
        """Generate a mock response for threat model generation"""
        return json.dumps(
            {
                "threats": [
                    {
                        "id": "THREAT-001",
                        "name": "SQL Injection",
                        "description": "Attacker can inject malicious SQL code via unsanitized user input",
                        "cwe_id": "CWE-89",
                        "severity": "high",
                        "likelihood": "medium",
                        "impact": "high",
                        "affected_components": ["database", "api", "user_input"],
                        "attack_vectors": [
                            "User input fields",
                            "API parameters",
                            "Search functionality",
                        ],
                        "mitigations": [
                            "Use parameterized queries",
                            "Implement input validation",
                            "Apply principle of least privilege for database accounts",
                        ],
                        "references": [
                            "https://owasp.org/www-community/attacks/SQL_Injection",
                            "https://cwe.mitre.org/data/definitions/89.html",
                        ],
                    },
                    {
                        "id": "THREAT-002",
                        "name": "Cross-Site Scripting (XSS)",
                        "description": "Attacker can inject malicious scripts that execute in users' browsers",
                        "cwe_id": "CWE-79",
                        "severity": "medium",
                        "likelihood": "high",
                        "impact": "medium",
                        "affected_components": ["frontend", "user_interface", "forms"],
                        "attack_vectors": [
                            "Comment fields",
                            "Profile information",
                            "Message content",
                        ],
                        "mitigations": [
                            "Implement content security policy",
                            "Use context-appropriate output encoding",
                            "Sanitize user input",
                        ],
                        "references": [
                            "https://owasp.org/www-community/attacks/xss/",
                            "https://cwe.mitre.org/data/definitions/79.html",
                        ],
                    },
                    {
                        "id": "THREAT-003",
                        "name": "Insecure Authentication",
                        "description": "Weaknesses in authentication allow attackers to impersonate users",
                        "cwe_id": "CWE-287",
                        "severity": "high",
                        "likelihood": "medium",
                        "impact": "high",
                        "affected_components": [
                            "authentication",
                            "session_management",
                            "login",
                        ],
                        "attack_vectors": [
                            "Weak password policies",
                            "Session fixation",
                            "Credential stuffing",
                        ],
                        "mitigations": [
                            "Implement multi-factor authentication",
                            "Use secure session management",
                            "Enforce strong password policies",
                        ],
                        "references": [
                            "https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication",
                            "https://cwe.mitre.org/data/definitions/287.html",
                        ],
                    },
                ],
                "attack_paths": [
                    {
                        "id": "PATH-001",
                        "name": "Data Exfiltration via SQL Injection",
                        "steps": [
                            "Attacker identifies vulnerable input field",
                            "Attacker injects SQL code to extract sensitive data",
                            "Attacker exfiltrates data from database",
                        ],
                        "threats": ["THREAT-001"],
                        "severity": "high",
                    },
                    {
                        "id": "PATH-002",
                        "name": "Account Takeover",
                        "steps": [
                            "Attacker exploits authentication weakness",
                            "Attacker gains access to user account",
                            "Attacker performs unauthorized actions",
                        ],
                        "threats": ["THREAT-003"],
                        "severity": "high",
                    },
                ],
                "risk_matrix": {
                    "high_impact_high_likelihood": ["THREAT-001"],
                    "high_impact_medium_likelihood": ["THREAT-003"],
                    "medium_impact_high_likelihood": ["THREAT-002"],
                    "medium_impact_medium_likelihood": [],
                    "low_impact_high_likelihood": [],
                    "low_impact_medium_likelihood": [],
                    "high_impact_low_likelihood": [],
                    "medium_impact_low_likelihood": [],
                    "low_impact_low_likelihood": [],
                },
            }
        )

    def _generate_mock_diagram_response(self, prompt: str) -> str:
        """Generate a mock response for diagram generation"""
        if "mermaid" in prompt.lower():
            # Return a Mermaid diagram
            return """graph TD
                A[User Input] -->|Unsanitized| B{SQL Injection}
                B -->|Successful Attack| C[Data Breach]
                B -->|Failed Attack| D[Normal Operation]
                
                E[Authentication] -->|Weak Passwords| F{Account Compromise}
                F -->|Successful Attack| G[Unauthorized Access]
                F -->|Failed Attack| H[Normal Operation]
                
                I[Web Interface] -->|Unvalidated Input| J{Cross-Site Scripting}
                J -->|Successful Attack| K[Session Hijacking]
                J -->|Failed Attack| L[Normal Operation]
            """
        elif "attack tree" in prompt.lower():
            # Return an attack tree
            return """Attack Goal: Compromise User Data
            ├── SQL Injection
            │   ├── Identify vulnerable input field
            │   ├── Craft malicious SQL query
            │   └── Extract sensitive data
            ├── Authentication Bypass
            │   ├── Brute force credentials
            │   ├── Exploit session management
            │   └── Credential stuffing
            └── Cross-Site Scripting
                ├── Identify vulnerable input field
                ├── Inject malicious script
                └── Steal user session
            """
        else:
            # Return a generic diagram description
            return """Threat Flow Diagram showing three main vulnerabilities:
            1. SQL Injection (High Risk)
            2. Cross-Site Scripting (Medium Risk)
            3. Authentication Bypass (High Risk)
            
            Attack vectors are mapped to affected components with mitigations identified for each threat.
            """

    def _generate_generic_response(self, prompt: str) -> str:
        """Generate a generic response for any other prompt"""
        return "This is a mock response for testing purposes. In a real scenario, this would be generated by an actual LLM. mock response"

    def get_default_model(self) -> str:
        """Get the default model for this provider"""
        return "mock-model"

    @classmethod
    def is_available(cls) -> bool:
        """Check if this provider is available"""
        return True
