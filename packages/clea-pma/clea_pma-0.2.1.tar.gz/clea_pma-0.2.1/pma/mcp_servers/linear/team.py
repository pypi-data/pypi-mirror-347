import requests
from typing import Any

from pma.integrations.linear import LinearClient
from pma.mcp_servers.linear.issues import ISSUE_NODE_FIELDS
from pma.utils.constants import LINEAR_BASE_URL


def fct_search_users(
    name: str = None,
) -> list[Any]:
    linear_api_key = LinearClient().api_key
    headers = {
        "Authorization": linear_api_key,
        "Content-Type": "application/json"
    }
    graphql_query = {
        "query": f"""
            query SearchTeamMembers($userFilter: UserFilter) {{
                users(filter: $userFilter) {{
                    nodes {{
                        active
                        assignedIssues {{
                            nodes {{
                                {ISSUE_NODE_FIELDS}
                            }}
                        }}
                        displayName
                        email
                        name
                    }}
                }}
            }}
        """,
        "variables": {
            "userFilter": {
                "name": {
                    **({"name": {"contains": name}} if name else {}),
                },
            },
        }
    }
    resp = requests.post(LINEAR_BASE_URL, headers=headers, json=graphql_query)
    print(resp.json())
    return resp.json()["data"]["users"]["nodes"]
