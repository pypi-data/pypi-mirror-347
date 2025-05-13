"""MCP Tools for Omnidimension SDK.

This module defines the MCP tools that interact with the Omnidimension API.
"""

import base64
import logging
import uuid
from typing import Dict, List, Optional, Any, Union

from fastmcp import MCPTool, MCPToolParam, MCPToolParamSchema
from pydantic import BaseModel, Field

from omnidimension import Client
from .server import sessions, get_client

# Configure logger
logger = logging.getLogger(__name__)


# Authentication Tool
authenticate_tool = MCPTool(
    name="authenticate",
    description="Authenticate with the Omnidimension API using your API key",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "api_key": MCPToolParam(
                type="string",
                description="Your Omnidimension API key"
            )
        },
        required=["api_key"]
    ),
    fn=lambda params, context: {
        "session_id": _authenticate(params["api_key"], context.get("session_id"))
    }
)


def _authenticate(api_key: str, session_id: Optional[str] = None) -> str:
    """Authenticate with the Omnidimension API and store the client.
    
    Args:
        api_key: The API key to authenticate with.
        session_id: Optional session ID to use for storing the client.
            If not provided, a new session ID will be generated.
            
    Returns:
        The session ID for the authenticated client.
        
    Raises:
        Exception: If authentication fails.
    """
    try:
        # Create a new client with the provided API key
        client = Client(api_key=api_key)
        
        # Generate a session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Store the client in the sessions dictionary
        sessions[session_id] = client
        
        return session_id
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise Exception(f"Authentication failed: {str(e)}")


# Agent Tools
list_agents_tool = MCPTool(
    name="list_agents",
    description="List all agents for the authenticated user",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "page": MCPToolParam(
                type="integer",
                description="Page number for pagination (default: 1)"
            ),
            "page_size": MCPToolParam(
                type="integer",
                description="Number of items per page (default: 30)"
            )
        }
    ),
    fn=lambda params, context: get_client(context.get("session_id")).agent.list(
        page=params.get("page", 1),
        page_size=params.get("page_size", 30)
    )["json"]
)


get_agent_tool = MCPTool(
    name="get_agent",
    description="Get a specific agent by ID",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "agent_id": MCPToolParam(
                type="integer",
                description="The ID of the agent to retrieve"
            )
        },
        required=["agent_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).agent.get(
        agent_id=params["agent_id"]
    )["json"]
)


create_agent_tool = MCPTool(
    name="create_agent",
    description="Create a custom agent with the provided configuration",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "name": MCPToolParam(
                type="string",
                description="Name for the agent"
            ),
            "context_breakdown": MCPToolParam(
                type="array",
                description="List of context breakdowns, each containing 'title' and 'body'"
            ),
            "additional_params": MCPToolParam(
                type="object",
                description="Additional optional parameters to include in the API request"
            )
        },
        required=["name", "context_breakdown"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).agent.create(
        name=params["name"],
        context_breakdown=params["context_breakdown"],
        **(params.get("additional_params", {}))
    )["json"]
)


update_agent_tool = MCPTool(
    name="update_agent",
    description="Update an existing agent",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "agent_id": MCPToolParam(
                type="integer",
                description="The ID of the agent to update"
            ),
            "data": MCPToolParam(
                type="object",
                description="The updated agent data"
            )
        },
        required=["agent_id", "data"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).agent.update(
        agent_id=params["agent_id"],
        data=params["data"]
    )["json"]
)


delete_agent_tool = MCPTool(
    name="delete_agent",
    description="Delete an agent",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "agent_id": MCPToolParam(
                type="integer",
                description="The ID of the agent to delete"
            )
        },
        required=["agent_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).agent.delete(
        agent_id=params["agent_id"]
    )["json"]
)


# Knowledge Base Tools
list_knowledge_base_tool = MCPTool(
    name="list_knowledge_base",
    description="Get all knowledge base files for the authenticated user",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={}
    ),
    fn=lambda params, context: get_client(context.get("session_id")).knowledge_base.list()["json"]
)


upload_knowledge_base_tool = MCPTool(
    name="upload_knowledge_base",
    description="Upload a file to the knowledge base",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "file_data": MCPToolParam(
                type="string",
                description="Base64 encoded file content"
            ),
            "filename": MCPToolParam(
                type="string",
                description="Name of the file (must end with .pdf)"
            )
        },
        required=["file_data", "filename"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).knowledge_base.create(
        file_data=params["file_data"],
        filename=params["filename"]
    )["json"]
)


delete_knowledge_base_tool = MCPTool(
    name="delete_knowledge_base",
    description="Delete a file from the knowledge base",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "file_id": MCPToolParam(
                type="integer",
                description="ID of the file to delete"
            )
        },
        required=["file_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).knowledge_base.delete(
        file_id=params["file_id"]
    )["json"]
)


attach_knowledge_base_tool = MCPTool(
    name="attach_knowledge_base",
    description="Attach multiple files to an agent",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "file_ids": MCPToolParam(
                type="array",
                description="List of file IDs to attach"
            ),
            "agent_id": MCPToolParam(
                type="integer",
                description="ID of the agent to attach files to"
            )
        },
        required=["file_ids", "agent_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).knowledge_base.attach(
        file_ids=params["file_ids"],
        agent_id=params["agent_id"]
    )["json"]
)


detach_knowledge_base_tool = MCPTool(
    name="detach_knowledge_base",
    description="Detach multiple files from an agent",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "file_ids": MCPToolParam(
                type="array",
                description="List of file IDs to detach"
            ),
            "agent_id": MCPToolParam(
                type="integer",
                description="ID of the agent to detach files from"
            )
        },
        required=["file_ids", "agent_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).knowledge_base.detach(
        file_ids=params["file_ids"],
        agent_id=params["agent_id"]
    )["json"]
)


# Call Tools
dispatch_call_tool = MCPTool(
    name="dispatch_call",
    description="Dispatch a call to agent with the provided call context",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "agent_id": MCPToolParam(
                type="integer",
                description="ID for the agent"
            ),
            "to_number": MCPToolParam(
                type="string",
                description="Valid phone number with country code"
            ),
            "call_context": MCPToolParam(
                type="string",
                description="Call context to be passed to agent during call"
            )
        },
        required=["agent_id", "to_number"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).call.dispatch_call(
        agent_id=params["agent_id"],
        to_number=params["to_number"],
        call_context=params.get("call_context", "")
    )["json"]
)


get_call_logs_tool = MCPTool(
    name="get_call_logs",
    description="Get all call logs for the authenticated user",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "page": MCPToolParam(
                type="integer",
                description="Page number for pagination (default: 1)"
            ),
            "page_size": MCPToolParam(
                type="integer",
                description="Number of items per page (default: 30)"
            ),
            "agent_id": MCPToolParam(
                type="integer",
                description="Filter by agent ID (optional)"
            )
        }
    ),
    fn=lambda params, context: get_client(context.get("session_id")).call.get_call_logs(
        page=params.get("page", 1),
        page_size=params.get("page_size", 30),
        agent_id=params.get("agent_id")
    )["json"]
)


get_call_log_tool = MCPTool(
    name="get_call_log",
    description="Get a specific call log by ID",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "call_log_id": MCPToolParam(
                type="integer",
                description="The ID of the call log to retrieve"
            )
        },
        required=["call_log_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).call.get_call_log(
        call_log_id=params["call_log_id"]
    )["json"]
)


# Integration Tools
create_custom_api_integration_tool = MCPTool(
    name="create_custom_api_integration",
    description="Create a custom API integration",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "name": MCPToolParam(
                type="string",
                description="Name for the integration"
            ),
            "url": MCPToolParam(
                type="string",
                description="URL for the API endpoint"
            ),
            "method": MCPToolParam(
                type="string",
                description="HTTP method (GET, POST, PUT, DELETE, PATCH)"
            ),
            "description": MCPToolParam(
                type="string",
                description="Description of the integration"
            ),
            "headers": MCPToolParam(
                type="array",
                description="Headers for the API request"
            ),
            "body_type": MCPToolParam(
                type="string",
                description="Body type (none, json, form)"
            ),
            "body_content": MCPToolParam(
                type="string",
                description="Body content for the request"
            ),
            "body_params": MCPToolParam(
                type="array",
                description="Body parameters for the request"
            ),
            "query_params": MCPToolParam(
                type="array",
                description="Query parameters for the request"
            )
        },
        required=["name", "url", "method"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).integrations.create_custom_api_integration(
        name=params["name"],
        url=params["url"],
        method=params["method"],
        description=params.get("description", ""),
        headers=params.get("headers"),
        body_type=params.get("body_type"),
        body_content=params.get("body_content"),
        body_params=params.get("body_params"),
        query_params=params.get("query_params")
    )["json"]
)


create_cal_integration_tool = MCPTool(
    name="create_cal_integration",
    description="Create a Cal.com integration",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "name": MCPToolParam(
                type="string",
                description="Name for the integration"
            ),
            "cal_api_key": MCPToolParam(
                type="string",
                description="Cal.com API key"
            ),
            "cal_id": MCPToolParam(
                type="string",
                description="Cal.com ID"
            ),
            "cal_timezone": MCPToolParam(
                type="string",
                description="Cal.com timezone"
            ),
            "description": MCPToolParam(
                type="string",
                description="Description of the integration"
            )
        },
        required=["name", "cal_api_key", "cal_id", "cal_timezone"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).integrations.create_cal_integration(
        name=params["name"],
        cal_api_key=params["cal_api_key"],
        cal_id=params["cal_id"],
        cal_timezone=params["cal_timezone"],
        description=params.get("description", "")
    )["json"]
)


get_user_integrations_tool = MCPTool(
    name="get_user_integrations",
    description="Get all integrations available for the authenticated user",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={}
    ),
    fn=lambda params, context: get_client(context.get("session_id")).integrations.get_user_integrations()["json"]
)


get_agent_integrations_tool = MCPTool(
    name="get_agent_integrations",
    description="Get all integrations for a specific agent",
    param_schema=MCPToolParamSchema(
        type="object",
        properties={
            "agent_id": MCPToolParam(
                type="integer",
                description="ID of the agent to get integrations for"
            )
        },
        required=["agent_id"]
    ),
    fn=lambda params, context: get_client(context.get("session_id")).integrations.get_agent_integrations(
        agent_id=params["agent_id"]
    )["json"]
)