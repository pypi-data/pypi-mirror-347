#!/usr/bin/env python3
"""
MCP Integration for Agentic Agents.
Provides functionality to expose agentic agents through the Model Context Protocol.
"""

import asyncio
import json
import logging
import os
import sys
import threading
import socket
import time
from typing import Any, Dict, List, Optional

# Import MCP SDK if available, otherwise provide mock implementation
MCP_AVAILABLE = False
try:
    # First try the standard import path
    try:
        from modelcontextprotocol.server import Server, StdioServerTransport
        from modelcontextprotocol.types import (
            CallToolRequestSchema,
            ListToolsRequestSchema,
            McpError,
            ErrorCode,
        )
        MCP_AVAILABLE = True
    except ImportError:
        # Try alternative import paths
        try:
            from mcp.server import Server, StdioServerTransport
            from mcp.types import (
                CallToolRequestSchema,
                ListToolsRequestSchema,
                McpError,
                ErrorCode,
            )
            MCP_AVAILABLE = True
        except ImportError:
            pass
except Exception as e:
    logging.warning(f"Error importing MCP SDK: {e}")

# If MCP is not available, provide mock implementation
if not MCP_AVAILABLE:
    logging.warning("MCP SDK not available, using mock implementation")
    
    class Server:
        def __init__(self, *args, **kwargs):
            pass
        
        def setRequestHandler(self, *args, **kwargs):
            pass
        
        async def start(self, *args, **kwargs):
            pass
        
        async def close(self):
            pass
    
    class StdioServerTransport:
        pass
    
    class CallToolRequestSchema:
        pass
    
    class ListToolsRequestSchema:
        pass
    
    class McpError:
        pass
    
    class ErrorCode:
        pass

logger = logging.getLogger(__name__)


class AgentMcpServer:
    """
    MCP Server for exposing agentic agent capabilities through the Model Context Protocol.
    """

    def __init__(self, agent):
        """
        Initialize the MCP server for an agent.

        Args:
            agent: The agentic agent to expose
        """
        self.agent = agent
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{agent.id}")
        self.server = None
        self.server_thread = None
        self.running = False
        
        # Get base MCP port from environment or use default
        base_port = int(os.environ.get("MCP_BASE_PORT", 8080))
        
        # Calculate unique port for this agent based on agent ID
        # This ensures each agent gets its own port
        import hashlib
        agent_hash = int(hashlib.md5(agent.id.encode()).hexdigest(), 16) % 1000
        self.port = base_port + agent_hash
        
        # Check if the port is already in use, if so, find an available port
        self.port = self._find_available_port(self.port, base_port, base_port + 2000)
        
        # Get MCP host from environment or use default
        self.host = os.environ.get("MCP_HOST", "localhost")
        
        # Store the unique endpoint URL
        self.endpoint_url = f"http://{self.host}:{self.port}/mcp"
        
    def _find_available_port(self, preferred_port, min_port, max_port):
        """Find an available port, starting with the preferred port"""
        for port in range(preferred_port, max_port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((self.host, port))
                    return port
                except socket.error:
                    continue
        
        # If no port is available in the range, try a random port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, 0))
            return s.getsockname()[1]
        
        # Determine if we should use stdio transport
        self.use_stdio = os.environ.get("MCP_USE_STDIO", "false").lower() == "true"

    async def start(self):
        """Start the MCP server"""
        if not MCP_AVAILABLE:
            self.logger.warning("MCP SDK not available, skipping MCP server initialization")
            return False
        
        if self.running:
            self.logger.warning("MCP server already running")
            return True
        
        try:
            self.logger.info(f"Starting MCP server for agent {self.agent.id}")
            
            # Create server
            self.server = Server(
                {
                    "name": f"agentic-agent-{self.agent.id}",
                    "version": "0.1.0",
                },
                {
                    "capabilities": {
                        "tools": {},
                    },
                }
            )
            
            # Set up request handlers
            self.setup_request_handlers()
            
            # Start server
            if self.use_stdio:
                # Use stdio transport
                self.logger.info("Using stdio transport for MCP server")
                transport = StdioServerTransport()
                await self.server.start(transport)
            else:
                # Start server in a separate thread
                self.logger.info(f"Starting MCP server on {self.host}:{self.port}")
                try:
                    self.server_thread = threading.Thread(
                        target=self._run_server_thread,
                        daemon=True,
                    )
                    self.server_thread.start()
                    
                    # Wait a moment to ensure the server starts
                    time.sleep(0.5)
                    
                    # Check if the server is running
                    if not self._check_server_running():
                        self.logger.warning(f"MCP server on {self.host}:{self.port} failed to start")
                        return False
                except Exception as e:
                    self.logger.error(f"Error starting MCP server thread: {e}", exc_info=True)
                    return False
            
            self.running = True
            self.logger.info(f"MCP server for agent {self.agent.id} started successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Error starting MCP server: {e}", exc_info=True)
            return False

    def _check_server_running(self):
        """Check if the server is running by attempting to connect to it"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((self.host, self.port))
                return result == 0
        except Exception:
            return False

    def _run_server_thread(self):
        """Run the MCP server in a separate thread"""
        try:
            # Try to import FastAPI and uvicorn
            try:
                import uvicorn
                from fastapi import FastAPI, Request
                from fastapi.middleware.cors import CORSMiddleware
                
                # Create FastAPI app
                app = FastAPI()
                
                # Add CORS middleware
                app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                
                # Add routes
                @app.post("/mcp/call")
                async def call_tool(request: Request):
                    # Handle tool call
                    try:
                        data = await request.json()
                        tool_name = data.get("name")
                        tool_args = data.get("arguments", {})
                        
                        # Call the appropriate agent method
                        result = await self._handle_tool_call(tool_name, tool_args)
                        return {"result": result}
                    except Exception as e:
                        return {"error": str(e)}
                
                @app.get("/mcp/list")
                async def list_tools():
                    # Return list of available tools
                    return {"tools": self._get_available_tools()}
                
                # Add health check endpoint
                @app.get("/mcp/health")
                async def health_check():
                    return {"status": "ok", "agent_id": self.agent.id}
                
                # Run the server
                uvicorn.run(app, host=self.host, port=self.port)
            except ImportError:
                self.logger.error("FastAPI or uvicorn not available, MCP server cannot start")
                return
        except Exception as e:
            self.logger.error(f"Error in MCP server thread: {e}", exc_info=True)

    def setup_request_handlers(self):
        """Set up request handlers for the MCP server"""
        if not self.server:
            return
        
        # Set up handler for listing tools
        self.server.setRequestHandler(
            ListToolsRequestSchema,
            lambda _: {"tools": self._get_available_tools()}
        )
        
        # Set up handler for calling tools
        self.server.setRequestHandler(
            CallToolRequestSchema,
            self._handle_call_tool_request
        )

    async def _handle_call_tool_request(self, request):
        """Handle a call tool request"""
        tool_name = request.params.name
        tool_args = request.params.arguments
        
        try:
            result = await self._handle_tool_call(tool_name, tool_args)
            return {"result": result}
        except Exception as e:
            self.logger.error(f"Error handling tool call: {e}", exc_info=True)
            raise McpError(
                ErrorCode.TOOL_EXECUTION_ERROR,
                f"Error executing tool {tool_name}: {str(e)}"
            )

    async def _handle_tool_call(self, tool_name, tool_args):
        """Handle a tool call by dispatching to the appropriate agent method"""
        self.logger.info(f"Handling tool call: {tool_name} with args: {tool_args}")
        
        # Map tool names to agent methods
        tool_handlers = {
            "share_knowledge": self._handle_share_knowledge,
            "query_knowledge": self._handle_query_knowledge,
            "start_reasoning_chain": self._handle_start_reasoning_chain,
            "contribute_to_reasoning": self._handle_contribute_to_reasoning,
            "process_task": self._handle_process_task,
        }
        
        # Get the handler for this tool
        handler = tool_handlers.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Call the handler
        return await handler(tool_args)

    async def _handle_share_knowledge(self, args):
        """Handle a share_knowledge tool call"""
        knowledge_type = args.get("knowledge_type")
        knowledge_data = args.get("knowledge_data", {})
        confidence = float(args.get("confidence", 1.0))
        tags = args.get("tags", [])
        
        if not knowledge_type:
            raise ValueError("knowledge_type is required")
        
        knowledge_id = self.agent.share_knowledge(
            knowledge_type, knowledge_data, confidence, tags
        )
        
        return {
            "knowledge_id": knowledge_id,
            "success": knowledge_id is not None,
        }

    async def _handle_query_knowledge(self, args):
        """Handle a query_knowledge tool call"""
        knowledge_type = args.get("knowledge_type")
        tags = args.get("tags", [])
        min_confidence = float(args.get("min_confidence", 0.5))
        
        results = self.agent.query_knowledge(knowledge_type, tags, min_confidence)
        
        return {
            "results": results,
            "count": len(results),
        }

    async def _handle_start_reasoning_chain(self, args):
        """Handle a start_reasoning_chain tool call"""
        topic = args.get("topic")
        initial_insight = args.get("initial_insight", {})
        
        if not topic:
            raise ValueError("topic is required")
        
        chain_id = self.agent.start_reasoning_chain(topic, initial_insight)
        
        return {
            "chain_id": chain_id,
            "success": chain_id is not None,
        }

    async def _handle_contribute_to_reasoning(self, args):
        """Handle a contribute_to_reasoning tool call"""
        chain_id = args.get("chain_id")
        insight = args.get("insight", {})
        confidence = float(args.get("confidence", 0.5))
        
        if not chain_id:
            raise ValueError("chain_id is required")
        
        success = self.agent.contribute_to_reasoning(chain_id, insight, confidence)
        
        return {
            "success": success,
        }

    async def _handle_process_task(self, args):
        """Handle a process_task tool call"""
        task_type = args.get("task_type")
        task_data = args.get("task_data", {})
        
        if not task_type:
            raise ValueError("task_type is required")
        
        # Create a message to process
        from autothreats.simplified_base import Message
        message = Message(task_type, task_data, "mcp_client")
        
        # Process the message
        result = await self.agent.process_message(message)
        
        return result or {"status": "processed"}

    def _get_available_tools(self):
        """Get the list of available tools for this agent"""
        tools = [
            {
                "name": "share_knowledge",
                "description": "Share knowledge with other agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "knowledge_type": {
                            "type": "string",
                            "description": "The type of knowledge being shared",
                        },
                        "knowledge_data": {
                            "type": "object",
                            "description": "The knowledge data",
                        },
                        "confidence": {
                            "type": "number",
                            "description": "The confidence level in this knowledge (0.0-1.0)",
                            "default": 1.0,
                        },
                        "tags": {
                            "type": "array",
                            "description": "Optional list of tags for categorizing the knowledge",
                            "items": {
                                "type": "string",
                            },
                        },
                    },
                    "required": ["knowledge_type", "knowledge_data"],
                },
            },
            {
                "name": "query_knowledge",
                "description": "Query knowledge shared by other agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "knowledge_type": {
                            "type": "string",
                            "description": "Optional type to filter by",
                        },
                        "tags": {
                            "type": "array",
                            "description": "Optional list of tags to filter by",
                            "items": {
                                "type": "string",
                            },
                        },
                        "min_confidence": {
                            "type": "number",
                            "description": "Minimum confidence threshold",
                            "default": 0.5,
                        },
                    },
                },
            },
            {
                "name": "start_reasoning_chain",
                "description": "Start a new collaborative reasoning chain",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic for the reasoning chain",
                        },
                        "initial_insight": {
                            "type": "object",
                            "description": "The initial insight to start the chain",
                        },
                    },
                    "required": ["topic"],
                },
            },
            {
                "name": "contribute_to_reasoning",
                "description": "Contribute to an existing reasoning chain",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chain_id": {
                            "type": "string",
                            "description": "The ID of the reasoning chain",
                        },
                        "insight": {
                            "type": "object",
                            "description": "The insight to contribute",
                        },
                        "confidence": {
                            "type": "number",
                            "description": "The confidence level in this insight (0.0-1.0)",
                            "default": 0.5,
                        },
                    },
                    "required": ["chain_id", "insight"],
                },
            },
            {
                "name": "process_task",
                "description": "Process a task with this agent",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_type": {
                            "type": "string",
                            "description": "The type of task to process",
                        },
                        "task_data": {
                            "type": "object",
                            "description": "The data for the task",
                        },
                    },
                    "required": ["task_type"],
                },
            },
        ]
        
        return tools

    async def stop(self):
        """Stop the MCP server"""
        if not self.running:
            return
        
        try:
            self.logger.info(f"Stopping MCP server for agent {self.agent.id}")
            
            if self.server:
                await self.server.close()
                self.server = None
            
            self.running = False
            self.logger.info(f"MCP server for agent {self.agent.id} stopped successfully")
        except Exception as e:
            self.logger.error(f"Error stopping MCP server: {e}", exc_info=True)