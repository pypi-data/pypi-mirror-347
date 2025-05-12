import requests
from typing import Any

from pma.integrations.linear import LinearClient
from pma.utils.constants import LINEAR_BASE_URL

ISSUE_NODE_FIELDS = """
    assignee {
        email
    }
    cycle {
        name
        number
    }
    description
    dueDate
    estimate
    project {
        name
    }
    state {
        name
    }
    title
    url
"""

def fct_search_issues(
    # Assignee
    assignee: str = None,
    is_mine_only: bool = False,
    # Cycle
    is_current_cycle: bool = False,
    is_next_cycle: bool = False,
    is_previous_cycle: bool = False
) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": f"""
            query SearchIssues($issueFilter: IssueFilter, $cycleFilter: CycleFilter) {{
                issues(filter: $issueFilter) {{
                    nodes {{
                        {ISSUE_NODE_FIELDS}
                    }}
                }}
                cycles(filter: $cycleFilter) {{
                    nodes {{
                        name
                    }}
                }}
            }}
        """,
        "variables": {
            "issueFilter": {
                "assignee": {
                    **({"isMe": {"eq": True}} if is_mine_only else {}),
                    **({"name": {"contains": assignee}} if assignee else {}),
                },
                "cycle": {
                    **({"isActive": {"eq": True}} if is_current_cycle else {}),
                    **({"isNext": {"eq": True}} if is_next_cycle else {}),
                    **({"isPrevious": {"eq": True}} if is_previous_cycle else {}),
                }
            },
            "cycleFilter": {
                **({"isActive": {"eq": True}} if is_current_cycle else {}),
            }
        }
    }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    return resp.json()["data"]["issues"]["nodes"]
