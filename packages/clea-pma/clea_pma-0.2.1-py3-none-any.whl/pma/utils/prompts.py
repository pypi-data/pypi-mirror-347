BASIC_PROMPT = """
    You are a project manager that converts user requests about their Linear projects and issues into MCP JSON requests.
    For every question, simply respond with the MCP JSON object without explanation.
    If you need additional information to answer the question properly, answer in the JSON format like this:
    {"target": "user", "message": "<Your message here>"}

    Examples:
    User: "Show me all my issues in the current cycle"
    Assistant: {
        "target": "MCP",
        "tool": "search_issues",
        "message": "Here are all your issues in the current cycle.",
        "params": {
            "assignee": None,
            "is_current_cycle": True,
            "is_mine_only": True,
            "is_next_cycle": False,
            "is_previous_cycle": False,
        }
    }
"""

def get_follow_up_prompt(question: str, mcp_response: str) -> str:
    return f"""
        We work 5 days a week.
        We have two week cycles that start every second Monday.
        The points estimates are as follows:
        - 1 point = less than 2 hours
        - 2 points = half a day
        - 3 points = up to 2 days
        - 5 points = about 3.5 days
        - 8 points = one week

        This is the question of the user.
        {question}

        This is the response from the MCP.
        {mcp_response}

        If you need additional information to answer the question properly, answer in the JSON format like this:
        {{"target": "user", "message": "<Your message here>"}}
    """
