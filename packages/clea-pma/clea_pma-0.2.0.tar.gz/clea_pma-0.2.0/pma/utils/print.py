from rich import print
from pma.utils.constants import AGENT_NAME

def print_agent_message(message: str):
    print(f"\n[blue]{AGENT_NAME}:[/blue] {message}\n")
