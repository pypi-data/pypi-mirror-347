"""MCP Server implementation for Omnidimension SDK.

This module provides the FastAPI application that implements the MCP server
for interacting with Omnidimension services.
"""

import logging
from typing import Dict, List, Optional, Any, Union

from fastapi import FastAPI, Depends, HTTPException, status
from fastmcp import MCPRouter, MCPTool, MCPToolParam, MCPToolParamSchema
from pydantic import BaseModel, Field

from omnidimension import Client
from .tools import (
    authenticate_tool,
    list_agents_tool,
    get_agent_tool,
    create_agent_tool,
    update_agent_tool,
    delete_agent_tool,
    list_knowledge_base_tool,
    upload_knowledge_base_tool,
    delete_knowledge_base_tool,
    attach_knowledge_base_tool,
    detach_knowledge_base_tool,
    dispatch_call_tool,
    get_call_logs_tool,
    get_call_log_tool,
    create_custom_api_integration_tool,
    create_cal_integration_tool,
    get_user_integrations_tool,
    get_agent_integrations_tool
)

# Configure logger
logger = logging.getLogger(__name__)

# Store API keys and clients for authenticated sessions
sessions: Dict[str, Client] = {}


def create_app(default_api_key: Optional[str] = None) -> FastAPI:
    """Create and configure the FastAPI application for the MCP server.
    
    Args:
        default_api_key: Optional default API key to use for all requests
            if no session-specific key is provided.
            
    Returns:
        FastAPI application configured with MCP routes and tools.
    """
    app = FastAPI(title="Omnidimension MCP Server")
    
    # Create MCP router
    mcp_router = MCPRouter()
    
    # Add all tools to the router
    mcp_router.add_tool(authenticate_tool)
    mcp_router.add_tool(list_agents_tool)
    mcp_router.add_tool(get_agent_tool)
    mcp_router.add_tool(create_agent_tool)
    mcp_router.add_tool(update_agent_tool)
    mcp_router.add_tool(delete_agent_tool)
    mcp_router.add_tool(list_knowledge_base_tool)
    mcp_router.add_tool(upload_knowledge_base_tool)
    mcp_router.add_tool(delete_knowledge_base_tool)
    mcp_router.add_tool(attach_knowledge_base_tool)
    mcp_router.add_tool(detach_knowledge_base_tool)
    mcp_router.add_tool(dispatch_call_tool)
    mcp_router.add_tool(get_call_logs_tool)
    mcp_router.add_tool(get_call_log_tool)
    mcp_router.add_tool(create_custom_api_integration_tool)
    mcp_router.add_tool(create_cal_integration_tool)
    mcp_router.add_tool(get_user_integrations_tool)
    mcp_router.add_tool(get_agent_integrations_tool)
    
    # Add the MCP router to the app
    app.include_router(mcp_router.router)
    
    # Store default API key if provided
    if default_api_key:
        try:
            # Validate the API key by creating a client
            client = Client(api_key=default_api_key)
            # Store the client in the default session
            sessions["default"] = client
            logger.info("Default API key configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure default API key: {str(e)}")
    
    @app.get("/")
    async def root():
        """Root endpoint that returns basic server information."""
        return {
            "name": "Omnidimension MCP Server",
            "version": "0.1.0",
            "status": "running"
        }
    
    return app


def get_client(session_id: str) -> Client:
    """Get the Omnidimension client for the given session ID.
    
    Args:
        session_id: The session ID to get the client for.
        
    Returns:
        The Omnidimension client for the session.
        
    Raises:
        HTTPException: If no client is found for the session ID.
    """
    # Try to get the client for the session
    client = sessions.get(session_id) or sessions.get("default")
    
    # If no client is found, raise an exception
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please use the authenticate tool first."
        )
    
    return client