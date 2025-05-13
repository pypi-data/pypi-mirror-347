"""Entry point for the omnidim_mcp_server module.

This module provides a symbolic link to omnidimension.mcp_server.__main__,
allowing the MCP server to be run using `python -m omnidim_mcp_server`.
"""

from omnidimension.mcp_server.__main__ import main

if __name__ == "__main__":
    exit(main())