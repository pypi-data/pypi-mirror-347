from fastmcp import FastMCP
from typing import Any

from pma.mcp_servers.linear.issues import fct_search_issues
from pma.mcp_servers.linear.team import fct_search_users


linear_mcp = FastMCP(name="LinearMCPServer")

@linear_mcp.tool()
def search_issues(
    assignee: str | None = None,
    is_current_cycle: bool = False,
    is_mine_only: bool = False,
    is_next_cycle: bool = False,
    is_previous_cycle: bool = False,
) -> list[Any]:
    """Search for my own issues in Linear"""
    return fct_search_issues(
        assignee=assignee,
        is_current_cycle=is_current_cycle,
        is_mine_only=is_mine_only,
        is_next_cycle=is_next_cycle,
        is_previous_cycle=is_previous_cycle,
    )

@linear_mcp.tool()
def search_users(
    name: str = None,
) -> list[Any]:
    """Search for team members and users in Linear"""
    return fct_search_users(name=name)
