#!/usr/bin/env python3
"""
Decorator-based Threat Detection Agent for the autonomous threat modeling system.
Uses the decorator API for simplified implementation.
"""

import asyncio
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from ..models.codebase_model import CodebaseModel
from ..models.threat_model import VulnerabilityModel
from ..utils.agent_decorators import agent
from ..utils.llm_service import LLMService
from ..utils.org_parameters import OrganizationParameters

logger = logging.getLogger(__name__)

@agent(agent_id="threat_detection", agent_type="threat_detection")
async def threat_detection(agent, task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process threat detection tasks.
    
    Args:
        agent: The agent instance
        task_type: The type of task to process
        task_data: The data for the task
        
    Returns:
        Result data
    """
    agent.logger.info(f"Processing task of type: {task_type}")
    
    # Initialize services if not already initialized
    if not hasattr(agent, "llm_service") or agent.llm_service is None:
        # Initialize LLM service with configuration
        llm_config = {
            "default_provider": agent.model.config.get("llm_provider", "openai"),
            "openai_api_key": agent.model.config.get("openai_api_key"),
            "anthropic_api_key": agent.model.config.get("anthropic_api_key"),
            "enable_openai": True,
            "enable_anthropic": agent.model.config.get("enable_anthropic", False),
            "openai_model": agent.model.config.get("openai_model", "gpt-4o-mini"),
            "anthropic_model": agent.model.config.get("anthropic_model", "claude-3-sonnet-20240229"),
        }
        agent.llm_service = LLMService(llm_config)
        
    if not hasattr(agent, "org_parameters") or agent.org_parameters is None:
        # Load organization parameters if provided
        org_params_path = agent.model.config.get("org_parameters_path")
        if org_params_path:
            agent.org_parameters = OrganizationParameters(org_params_path)
        else:
            agent.org_parameters = OrganizationParameters()
    
    # Handle threat detection task
    if task_type in ["threat_detection", "threat_detection_start"]:
        # Validate required parameters
        job_id = task_data.get("job_id")
        codebase_id = task_data.get("codebase_id")
        
        # Check for missing parameters
        missing_params = []
        if not job_id:
            missing_params.append("job_id")
        if not codebase_id:
            missing_params.append("codebase_id")
                
        if missing_params:
            error_msg = f"Missing required parameters: {', '.join(missing_params)}"
            agent.logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "missing_parameters": missing_params,
            }
        
        # Get codebase from workspace
        codebase = agent.workspace.get_data(codebase_id)
        if not codebase:
            return {
                "status": "error",
                "message": f"Codebase not found: {codebase_id}"
            }
        
        # Convert to CodebaseModel if needed
        if isinstance(codebase, dict):
            codebase_model = CodebaseModel.from_dict(codebase)
        elif isinstance(codebase, CodebaseModel):
            codebase_model = codebase
        else:
            return {
                "status": "error",
                "message": f"Invalid codebase format: {type(codebase)}"
            }
        
        # Detect vulnerabilities
        vulnerabilities = []
        
        # Process each file in the codebase
        for file_path, content in codebase_model.files.items():
            # Skip if content is not a string
            if not isinstance(content, str):
                continue
                
            # Skip binary files and very large files
            if len(content) > 100000:  # Skip files larger than 100KB
                continue
                
            # Check for common security issues
            if "password" in content.lower() or "secret" in content.lower():
                vulnerabilities.append({
                    "name": "Hardcoded Secret",
                    "description": "Potential hardcoded secret or password found",
                    "severity": "high",
                    "cwe_id": "CWE-798",
                    "location": file_path,
                    "line_number": _find_line_number(content, ["password", "secret"]),
                    "remediation": "Store secrets in environment variables or a secure vault"
                })
                
            if "exec(" in content.lower() or "eval(" in content.lower():
                vulnerabilities.append({
                    "name": "Code Injection",
                    "description": "Potential code injection vulnerability",
                    "severity": "high",
                    "cwe_id": "CWE-94",
                    "location": file_path,
                    "line_number": _find_line_number(content, ["exec(", "eval("]),
                    "remediation": "Avoid using eval() or exec() with user input"
                })
                
            if "sql" in content.lower() and ("'" in content or '"' in content):
                vulnerabilities.append({
                    "name": "SQL Injection",
                    "description": "Potential SQL injection vulnerability",
                    "severity": "high",
                    "cwe_id": "CWE-89",
                    "location": file_path,
                    "line_number": _find_line_number(content, ["sql", "query"]),
                    "remediation": "Use parameterized queries or an ORM"
                })
        
        # Use LLM for more advanced detection if available
        if agent.llm_service:
            try:
                # Select a sample of files for LLM analysis (to avoid token limits)
                sample_files = list(codebase_model.files.items())[:5]
                
                # Create a prompt for the LLM
                prompt = "Analyze the following code for security vulnerabilities:\n\n"
                for file_path, content in sample_files:
                    # Truncate very large files
                    if len(content) > 1000:
                        content = content[:1000] + "...[truncated]"
                    prompt += f"File: {file_path}\n```\n{content}\n```\n\n"
                prompt += "\nIdentify any security vulnerabilities in the code above. For each vulnerability, provide:\n"
                prompt += "1. The vulnerability name\n2. Description\n3. Severity (high, medium, low)\n4. CWE ID if applicable\n5. File location\n6. Remediation steps\n"
                
                # Get response from LLM
                llm_response = await agent.llm_service.generate_text_async(prompt)
                
                # Parse LLM response to extract vulnerabilities
                # This is a simplified parsing logic
                if "vulnerability" in llm_response.lower():
                    sections = re.split(r'\n\s*\d+\.\s+', llm_response)
                    for section in sections[1:]:  # Skip the first split which is before the first number
                        lines = section.strip().split('\n')
                        if len(lines) >= 3:
                            vuln_name = lines[0].strip()
                            description = lines[1].strip()
                            
                            # Try to extract severity
                            severity = "medium"  # Default
                            for line in lines:
                                if "severity" in line.lower():
                                    if "high" in line.lower():
                                        severity = "high"
                                    elif "medium" in line.lower():
                                        severity = "medium"
                                    elif "low" in line.lower():
                                        severity = "low"
                            
                            # Try to extract CWE
                            cwe_id = ""
                            for line in lines:
                                cwe_match = re.search(r'CWE-\d+', line)
                                if cwe_match:
                                    cwe_id = cwe_match.group(0)
                            
                            # Try to extract file location
                            location = ""
                            for line in lines:
                                if "file" in line.lower() and ":" in line:
                                    location = line.split(":", 1)[1].strip()
                            
                            # Try to extract remediation
                            remediation = ""
                            for i, line in enumerate(lines):
                                if "remediation" in line.lower() or "fix" in line.lower():
                                    if i < len(lines) - 1:
                                        remediation = lines[i+1].strip()
                            
                            vulnerabilities.append({
                                "name": vuln_name,
                                "description": description,
                                "severity": severity,
                                "cwe_id": cwe_id,
                                "location": location,
                                "remediation": remediation
                            })
            except Exception as e:
                agent.logger.error(f"Error during LLM analysis: {e}")
        
        # Return results
        return {
            "job_id": job_id,
            "codebase_id": codebase_id,
            "vulnerabilities": vulnerabilities,
            "status": "success",
            "message": f"Found {len(vulnerabilities)} potential vulnerabilities",
        }
    else:
        return {
            "status": "error",
            "message": f"Unsupported task type: {task_type}"
        }

def _find_line_number(content: str, patterns: List[str]) -> Optional[int]:
    """Find the line number where any of the patterns first appears"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for pattern in patterns:
            if pattern in line.lower():
                return i + 1
    return None