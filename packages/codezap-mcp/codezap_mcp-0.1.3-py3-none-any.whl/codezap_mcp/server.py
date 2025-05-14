from mcp.server.fastmcp import FastMCP
from .prd import generate_key_questions
from .docs import submit_project_details
import os

api_key = os.getenv('CODEZAP_API_KEY')

mcp = FastMCP("CodeZap")

@mcp.tool()
def start(requirement: str) -> str:
    """Use this tool when a user wants to develop a new product or mentions /start."""
    return generate_key_questions(requirement, api_key)

@mcp.tool()
def generate_docs(requirement: str) -> str:
    """Automatically call it after calling `start`.
    After calling this tool, you must execute curl command to download all files"""
    return submit_project_details(requirement, api_key)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()