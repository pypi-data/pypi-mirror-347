import anthropic
import json
import keyring
import os
import traceback
import typer
from alive_progress import alive_bar
from fastmcp import Client
from rich import print

from pma.integrations.linear import LinearClient
from pma.mcp_servers.linear.mcp_server import linear_mcp
from pma.utils.constants import ANTHROPIC_MODEL
from pma.utils.print import print_agent_message
from pma.utils.prompts import BASIC_PROMPT, get_follow_up_prompt

app = typer.Typer()

@app.command()
async def run():
    # Anthropic API key
    anthropic_api_key = os.getenv(
        "ANTHROPIC_API_KEY",
        keyring.get_password('samdouble_project_manager_assistant', 'anthropic_api_key'),
    )
    if anthropic_api_key:
        print("[green]\u2713 Anthropic API key found in environment variables[/green]")
    else:
        anthropic_api_key = typer.prompt("Enter the Anthropic API key")
        keyring.set_password('samdouble_project_manager_assistant', 'anthropic_api_key', anthropic_api_key)
        print("Anthropic API key saved")

    # Linear API key
    linear_api_key = os.getenv(
        "LINEAR_API_KEY",
        keyring.get_password('samdouble_project_manager_assistant', 'linear_api_key'),
    )
    if linear_api_key:
        print("[green]\u2713 Linear API key found in environment variables[/green]")
    else:
        linear_api_key = typer.prompt("Enter the Linear API key")
        keyring.set_password('samdouble_project_manager_assistant', 'linear_api_key', linear_api_key)
        print("Linear API key saved")

    LinearClient(linear_api_key)

    client = anthropic.Anthropic(
        api_key=anthropic_api_key,
    )

    print_agent_message("You can start conversing with me. I'm your project manager assistant and hopefully competent at it.")

    messages = []
    messages.append({
        "role": "user",
        "content": BASIC_PROMPT,
    })
    async with Client(linear_mcp) as linear_mcp_client:
        # tools = await linear_mcp_client.list_tools()
        # print(tools)
        while True:
            user_input = typer.prompt(">")
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                print_agent_message("Exiting the conversation. Talk to you next time!")
                break

            messages.append({"role": "user", "content": user_input})

            with alive_bar(enrich_print=False, monitor=False, receipt=False, stats=False, theme="smooth", title="Thinking..."):
                message = client.messages.create(
                    model=ANTHROPIC_MODEL,
                    max_tokens=16384,
                    messages=messages,
                )
                message_text = message.content[0].text
                messages.append({"role": "assistant", "content": message_text})
                try:
                    message_json = json.loads(message_text, strict=False)
                    if message_json.get("target") == "MCP":
                        mcp_result = await linear_mcp_client.call_tool(message_json.get('tool'), message_json.get('params'))
                        # Ask the LLM to answer the user's question
                        messages.append({"role": "user", "content": get_follow_up_prompt(user_input, mcp_result[0].text if len(mcp_result) > 0 else "")})
                        aggregated_message = client.messages.create(
                            model=ANTHROPIC_MODEL,
                            max_tokens=16384,
                            messages=messages,
                        )
                        aggregated_message_text = aggregated_message.content[0].text
                        messages.append({"role": "assistant", "content": aggregated_message_text})
                        aggregated_message_json = json.loads(aggregated_message_text)
                        print_agent_message(aggregated_message_json.get('message'))
                        print("\n")
                    elif message_json.get("target") == "user":
                        print_agent_message(message_json.get('message'))
                except Exception as e:
                    print_agent_message(f"[red]Could not parse answer:[/red] {e} {message_text} {traceback.format_exc()}")
                    continue
