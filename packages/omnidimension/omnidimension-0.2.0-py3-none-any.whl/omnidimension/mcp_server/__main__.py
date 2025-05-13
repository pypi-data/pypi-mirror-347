#!/usr/bin/env python3
"""
Entry point for the Omnidimension MCP Server.

This module serves as the entry point when running the MCP server using:
`python -m omnidimension.mcp_server` or `python -m omnidim_mcp_server`
"""

import os
import argparse
import logging
import uvicorn
from .server import create_app


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Omnidimension MCP Server")
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1", 
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to"
    )
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Omnidimension API key (can also be set via OMNIDIM_API_KEY env var)"
    )
    return parser.parse_args()


def main():
    """Run the MCP server."""
    args = parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("OMNIDIM_API_KEY")
    if not api_key:
        logging.error("No API key provided. Please set OMNIDIM_API_KEY environment variable or use --api-key")
        return 1
    
    # Create FastAPI app with the API key
    app = create_app(api_key)
    
    # Run the server
    logging.info(f"Starting Omnidimension MCP Server on {args.host}:{args.port}")
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level=args.log_level
    )
    return 0


if __name__ == "__main__":
    exit(main())