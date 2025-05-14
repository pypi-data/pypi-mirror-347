#!/usr/bin/env python3
"""
Context-Aware Security module for the autonomous threat modeling system.
Enables security analysis that incorporates broader context.
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class ContextAwareSecurity:
    """
    Enables security analysis that incorporates broader context,
    including architectural, business domain, and deployment environment.
    """

    def __init__(self, workspace):
        """
        Initialize the context-aware security framework.

        Args:
            workspace: The shared workspace instance
        """
        self.workspace = workspace
        self.context_cache = {}
        self.domain_knowledge = {}
        self.deployment_contexts = {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Get LLM service from workspace if available
        self.llm_service = workspace.get_data("llm_service")
        if not self.llm_service:
            self.logger.warning(
                "LLM service not found in workspace, context analysis will be limited"
            )

    async def gather_architectural_context(
        self, code_segment: Dict[str, Any], codebase_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gather architectural context for a code segment.

        Args:
            code_segment: The code segment to analyze
            codebase_model: The codebase model

        Returns:
            Architectural context
        """
        segment_id = code_segment.get("id", str(uuid.uuid4()))
        file_path = code_segment.get("file_path", "")

        # Check cache
        cache_key = f"arch_context_{segment_id}"
        if cache_key in self.context_cache:
            return self.context_cache[cache_key]

        # Extract architectural layers
        layers = await self._identify_architectural_layers(code_segment, codebase_model)

        # Create architectural context
        arch_context = {
            "id": f"arch_{segment_id}",
            "segment_id": segment_id,
            "file_path": file_path,
            "architectural_layers": layers,
            "created_at": asyncio.get_event_loop().time(),
        }

        # Store in cache
        self.context_cache[cache_key] = arch_context

        self.logger.debug(
            f"Gathered architectural context for segment {segment_id} with {len(layers)} layers"
        )

        return arch_context

    async def _identify_architectural_layers(
        self, code_segment: Dict[str, Any], codebase_model: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Identify architectural layers for a code segment.

        Args:
            code_segment: The code segment to analyze
            codebase_model: The codebase model

        Returns:
            List of architectural layers
        """
        layers = []
        file_path = code_segment.get("file_path", "")

        # Define common architectural layers
        common_layers = [
            {
                "name": "presentation",
                "patterns": ["ui", "view", "component", "page", "screen", "template"],
            },
            {
                "name": "application",
                "patterns": [
                    "controller",
                    "service",
                    "manager",
                    "coordinator",
                    "facade",
                ],
            },
            {
                "name": "domain",
                "patterns": ["model", "entity", "domain", "business", "core"],
            },
            {
                "name": "infrastructure",
                "patterns": [
                    "repository",
                    "dao",
                    "gateway",
                    "adapter",
                    "client",
                    "provider",
                ],
            },
            {
                "name": "persistence",
                "patterns": ["database", "storage", "repository", "dao", "entity"],
            },
            {
                "name": "security",
                "patterns": ["auth", "security", "permission", "access", "crypto"],
            },
        ]

        # Check file path against layer patterns
        for layer in common_layers:
            for pattern in layer["patterns"]:
                if pattern.lower() in file_path.lower():
                    layers.append(
                        {
                            "name": layer["name"],
                            "confidence": 0.7,
                            "description": f"{layer['name']} layer",
                        }
                    )
                    break

        return layers

    async def incorporate_domain_knowledge(
        self, code_segment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Incorporate business domain knowledge into analysis.

        Args:
            code_segment: The code segment to analyze

        Returns:
            Domain knowledge context
        """
        segment_id = code_segment.get("id", str(uuid.uuid4()))
        file_path = code_segment.get("file_path", "")

        # Check cache
        cache_key = f"domain_context_{segment_id}"
        if cache_key in self.context_cache:
            return self.context_cache[cache_key]

        # Extract domain concepts
        domain_context = {
            "id": f"domain_{segment_id}",
            "segment_id": segment_id,
            "file_path": file_path,
            "domain_concepts": [],
            "business_rules": [],
            "security_requirements": [],
            "created_at": asyncio.get_event_loop().time(),
        }

        # Extract domain concepts from code
        code_content = code_segment.get("content", "")
        if code_content:
            domain_concepts = await self._extract_domain_concepts(
                code_content, file_path
            )
            domain_context["domain_concepts"] = domain_concepts

        # Extract business rules
        business_rules = await self._extract_business_rules(code_content, file_path)
        domain_context["business_rules"] = business_rules

        # Extract security requirements
        security_requirements = await self._extract_security_requirements(
            code_content, file_path
        )
        domain_context["security_requirements"] = security_requirements

        # Store in cache
        self.context_cache[cache_key] = domain_context

        self.logger.debug(
            f"Incorporated domain knowledge for segment {segment_id} with {len(domain_context['domain_concepts'])} concepts"
        )

        return domain_context

    async def _extract_domain_concepts(
        self, code_content: str, file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract domain concepts from code.

        Args:
            code_content: The code content
            file_path: The file path

        Returns:
            List of domain concepts
        """
        concepts = []

        # Use LLM for domain concept extraction if available
        if self.llm_service and code_content:
            try:
                # Truncate code content if too long
                if len(code_content) > 2000:
                    code_content = code_content[:2000] + "..."

                # Create prompt for AI
                prompt = f"""
You are an expert in domain-driven design and business analysis.
Analyze the following code and identify domain concepts, entities, and value objects.

File path: {file_path}

Code:
```
{code_content}
```

Extract domain concepts from this code. For each concept, provide:
1. The name of the concept
2. The type (Entity, Value Object, Service, etc.)
3. A brief description
4. Security implications, if any

Format your response as a JSON array of concept objects, each with these fields:
- name: The name of the concept
- type: The type of concept
- description: A brief description
- security_implications: Security implications, if any

Only include concepts that are clearly represented in the code.
"""

                # Generate concepts using LLM
                response = await self.llm_service.generate_text_async(prompt)

                if response and not response.startswith("Error"):
                    # Parse the response as JSON
                    try:
                        if response.strip().startswith(
                            "["
                        ) and response.strip().endswith("]"):
                            concepts = json.loads(response)
                        else:
                            # Try to extract JSON array from text
                            import re

                            json_match = re.search(r"\[.*\]", response, re.DOTALL)
                            if json_match:
                                concepts = json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        self.logger.warning(
                            f"Error parsing AI domain concepts: Invalid JSON"
                        )
            except Exception as e:
                self.logger.warning(
                    f"Error extracting domain concepts with AI: {str(e)}"
                )

        return concepts

    async def _extract_business_rules(
        self, code_content: str, file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract business rules from code.

        Args:
            code_content: The code content
            file_path: The file path

        Returns:
            List of business rules
        """
        # Placeholder implementation
        return []

    async def _extract_security_requirements(
        self, code_content: str, file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract security requirements from code.

        Args:
            code_content: The code content
            file_path: The file path

        Returns:
            List of security requirements
        """
        # Placeholder implementation
        return []
