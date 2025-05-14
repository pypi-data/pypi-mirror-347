#!/usr/bin/env python3
"""
Helper classes and functions for tests.
"""

import os
import sys
from typing import Any, Dict

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autothreats.simplified_base import Agent


class ConcreteTestAgent(Agent):
    """Concrete implementation of Agent for testing"""

    def __init__(
        self,
        agent_id: str,
        agent_type: str = "test_agent",
        config: Dict[str, Any] = None,
    ):
        super().__init__(agent_id, agent_type, config or {})
        self.test_data = {}
        self._agent_type = agent_type

    @property
    def type(self):
        """Get the agent type"""
        return self._agent_type

    async def initialize(self):
        """Initialize the agent"""
        self.model.update_state("status", "initialized")

    async def _process_task_impl(
        self, task_type: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a task and return a result"""
        # Check for required parameters based on task type
        if task_type == "test_task":
            # For test_missing_required_parameters test
            if not task_data:
                return {
                    "status": "error",
                    "message": "Missing required parameters",
                    "details": "This task requires parameters",
                }

            return {
                "status": "success",
                "message": "Test task processed successfully",
                "task_data": task_data,
            }
        elif task_type == "generate_text":
            if task_data.get("require_llm") and hasattr(self, "llm_service"):
                try:
                    result = await self.llm_service.generate_text(
                        task_data.get("text", "")
                    )
                    return {"status": "success", "result": result}
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"LLM service error: {str(e)}",
                    }
            return {"status": "success", "result": "Mock generated text"}
        elif task_type == "run_tool":
            if task_data.get("tool") and hasattr(self, "external_tools"):
                tool_name = task_data.get("tool")
                if tool_name in self.external_tools:
                    try:
                        result = await self.external_tools[tool_name].run(
                            task_data.get("params", {})
                        )
                        return {"status": "success", "result": result}
                    except Exception as e:
                        return {"status": "error", "message": f"Tool error: {str(e)}"}
            return {"status": "success", "result": "Mock tool result"}
        elif task_type == "fetch_url":
            if task_data.get("require_network") and hasattr(self, "network_client"):
                # Add retry logic for network requests
                max_retries = (
                    getattr(self, "retry_count", 0) + 1
                )  # Default to 1 attempt (no retries)
                last_error = None

                for attempt in range(max_retries):
                    try:
                        result = await self.network_client.request(
                            task_data.get("url", "")
                        )
                        return {"status": "success", "result": result}
                    except Exception as e:
                        last_error = e
                        if attempt < max_retries - 1:
                            # Log retry attempt
                            self.logger.info(
                                f"Network request failed, retrying ({attempt+1}/{max_retries}): {str(e)}"
                            )

                # If we get here, all retries failed
                return {
                    "status": "error",
                    "message": f"Network error after {max_retries} attempts: {str(last_error)}",
                }

            return {"status": "success", "result": "Mock network result"}
        elif task_type == "parse_json":
            try:
                import json

                parsed = json.loads(task_data.get("json_data", "{}"))
                return {"status": "success", "result": parsed}
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid JSON data"}
        elif task_type == "process_text":
            text = task_data.get("text", "")
            if len(text) > 1024 * 1024:  # 1MB
                return {"status": "error", "message": "Input too large"}
            return {"status": "success", "result": f"Processed {len(text)} characters"}
        elif task_type == "process_list":
            # Handle empty list
            items = task_data.get("list", [])
            return {"status": "success", "result": f"Processed {len(items)} items"}
        elif task_type == "process_dict":
            # Handle empty dict
            dict_data = task_data.get("dict", {})
            return {"status": "success", "result": f"Processed {len(dict_data)} keys"}
        elif task_type == "run_command":
            command = task_data.get("command", "")
            args = task_data.get("args", [])

            # Check for command injection
            if ";" in command or "|" in command or "&" in command:
                return {"status": "error", "message": "Invalid command"}

            for arg in args:
                if ";" in arg or "|" in arg or "&" in arg:
                    return {"status": "error", "message": "Invalid command"}

            return {"status": "success", "result": "Command executed"}
        else:
            return {
                "status": "error",
                "message": f"Unsupported task type: {task_type}",
                "details": "This agent only supports test tasks",
            }

    async def shutdown(self):
        """Clean up resources when shutting down"""
        self.model.update_state("status", "shutdown")
        self.test_data = {}
